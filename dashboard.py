import streamlit as st

from email_reader import read_mock_emails
from outlook_reader import read_outlook_emails
from ticket_processor import create_ticket, process_ticket


st.set_page_config(
    page_title="AI IT Support Assistant",
    page_icon="🖥️",
    layout="wide"
)

st.title("AI IT Support Assistant")
st.caption(
    "AI-assisted Tier 1 ticket analysis using company support procedures"
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "results" not in st.session_state:
    st.session_state.results = []

if "last_source" not in st.session_state:
    st.session_state.last_source = None


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

st.sidebar.header("Inbox Settings")

email_source = st.sidebar.selectbox(
    "Email Source",
    [
        "Mock Inbox",
        "Outlook"
    ]
)

email_limit = st.sidebar.selectbox(
    "Maximum Emails",
    [
        5,
        10,
        20
    ],
    index=0
)

st.sidebar.divider()

st.sidebar.caption(
    "Mock Inbox uses local development data. "
    "Outlook retrieves messages through Microsoft Graph."
)


# ---------------------------------------------------------
# Inbox processing
# ---------------------------------------------------------

st.subheader("Inbox")

if email_source == "Mock Inbox":
    st.write(
        "Using simulated support emails for development and testing."
    )
else:
    st.write(
        "Using the connected Outlook test mailbox through Microsoft Graph."
    )


if st.button(
    "Process Inbox",
    type="primary"
):
    try:
        if email_source == "Outlook":
            with st.spinner(
                "Connecting to Outlook through Microsoft Graph..."
            ):
                emails = read_outlook_emails(
                    limit=email_limit
                )
        else:
            emails = read_mock_emails()
            emails = emails[:email_limit]

        if not emails:
            st.warning(
                "No emails were found in the selected inbox."
            )
            st.session_state.results = []
            st.stop()

        results = []

        progress = st.progress(0)
        status = st.empty()

        for index, email in enumerate(emails):
            status.write(
                f"Processing {index + 1} of {len(emails)}: "
                f"{email['subject']}"
            )

            ticket = create_ticket(
                sender=email["sender"],
                subject=email["subject"],
                body=email["body"]
            )

            # Keep email metadata with the ticket
            ticket["message_id"] = email.get(
                "id",
                ""
            )

            ticket["received_at"] = email.get(
                "received_at"
            )

            ticket["is_read"] = email.get(
                "is_read"
            )

            ticket["source"] = email_source

            result = process_ticket(
                ticket
            )

            results.append(
                result
            )

            progress.progress(
                (index + 1) / len(emails)
            )

        st.session_state.results = results
        st.session_state.last_source = email_source

        status.success(
            f"Processed {len(results)} support tickets."
        )

    except Exception as error:
        st.error(
            "Inbox processing failed."
        )

        st.exception(
            error
        )


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------

results = st.session_state.results


if results:
    st.divider()

    total_tickets = len(
        results
    )

    human_review_count = sum(
        1
        for result in results
        if result["analysis"]["requires_human_review"]
    )

    tier1_count = (
        total_tickets
        - human_review_count
    )

    security_count = sum(
        1
        for result in results
        if "security"
        in result["analysis"]["category"].lower()
    )

    col1, col2, col3, col4 = st.columns(
        4
    )

    col1.metric(
        "Total Tickets",
        total_tickets
    )

    col2.metric(
        "Tier 1 Ready",
        tier1_count
    )

    col3.metric(
        "Human Review",
        human_review_count
    )

    col4.metric(
        "Security",
        security_count
    )

    st.caption(
        f"Source: {st.session_state.last_source}"
    )

    st.divider()

    st.subheader("Ticket Queue")


    # -----------------------------------------------------
    # Ticket cards
    # -----------------------------------------------------

    for result in results:
        ticket = result[
            "ticket"
        ]

        analysis = result[
            "analysis"
        ]

        requires_review = analysis[
            "requires_human_review"
        ]

        status_text = (
            "Human Review"
            if requires_review
            else "Tier 1 Ready"
        )

        title = (
            f"{analysis['priority']} | "
            f"{analysis['category']} | "
            f"{ticket['subject']} | "
            f"{status_text}"
        )

        with st.expander(
            title
        ):
            # ---------------------------------------------
            # Ticket metadata
            # ---------------------------------------------

            st.subheader(
                "Ticket Details"
            )

            detail_col1, detail_col2 = st.columns(
                2
            )

            with detail_col1:
                st.write(
                    "**Sender**"
                )
                st.write(
                    ticket["sender"]
                )

                st.write(
                    "**Subject**"
                )
                st.write(
                    ticket["subject"]
                )

            with detail_col2:
                st.write(
                    "**Source**"
                )
                st.write(
                    ticket.get(
                        "source",
                        "Unknown"
                    )
                )

                received_at = ticket.get(
                    "received_at"
                )

                if received_at:
                    st.write(
                        "**Received**"
                    )
                    st.write(
                        received_at
                    )

            st.divider()

            # ---------------------------------------------
            # Analysis
            # ---------------------------------------------

            st.subheader(
                "Analysis"
            )

            analysis_col1, analysis_col2, analysis_col3 = (
                st.columns(3)
            )

            analysis_col1.metric(
                "Priority",
                analysis["priority"]
            )

            analysis_col2.metric(
                "Category",
                analysis["category"]
            )

            analysis_col3.metric(
                "Status",
                status_text
            )

            st.write(
                "**Issue Summary**"
            )

            st.write(
                analysis["issue_summary"]
            )

            # ---------------------------------------------
            # Primary SOP
            # ---------------------------------------------

            retrieval_results = analysis.get(
                "retrieval_results",
                []
            )

            st.subheader(
                "Primary Procedure"
            )

            if retrieval_results:
                primary = retrieval_results[
                    0
                ]

                sop_col1, sop_col2 = st.columns(
                    [3, 1]
                )

                sop_col1.write(
                    "**Matched SOP**"
                )

                sop_col1.write(
                    primary["source"]
                )

                sop_col2.metric(
                    "Similarity",
                    f"{primary['score']:.3f}"
                )

            else:
                st.warning(
                    "No sufficiently relevant SOP was found."
                )

            # ---------------------------------------------
            # User guidance
            # ---------------------------------------------

            st.subheader(
                "User Guidance"
            )

            if analysis["user_steps"]:
                for number, step in enumerate(
                    analysis["user_steps"],
                    start=1
                ):
                    st.write(
                        f"{number}. {step}"
                    )
            else:
                st.write(
                    "No user troubleshooting steps recommended."
                )

            # ---------------------------------------------
            # Technician actions
            # ---------------------------------------------

            st.subheader(
                "Technician Actions"
            )

            if analysis["technician_actions"]:
                for number, action in enumerate(
                    analysis["technician_actions"],
                    start=1
                ):
                    st.write(
                        f"{number}. {action}"
                    )
            else:
                st.write(
                    "No technician actions recommended."
                )

            # ---------------------------------------------
            # Routing
            # ---------------------------------------------

            st.subheader(
                "Routing Decision"
            )

            if requires_review:
                st.warning(
                    "Human review required"
                )
            else:
                st.success(
                    "Tier 1 workflow can continue"
                )

            st.write(
                "**Reason**"
            )

            st.write(
                analysis["reason"]
            )

            # ---------------------------------------------
            # Retrieval details
            # ---------------------------------------------

            if retrieval_results:
                with st.expander("Retrieval Details"):
                    for number, retrieval in enumerate(
                        retrieval_results,
                        start=1
                    ):
                        st.markdown(
                            f"**{number}. {retrieval['source']}** "
                            f"— similarity {retrieval['score']:.4f}"
                        )

                        st.code(
                            retrieval["text"],
                            language=None
                        )

            # ---------------------------------------------
            # Original message
            # ---------------------------------------------

        with st.expander(
                "Original Email"
            ):
                st.write(
                    ticket["body"]
                )
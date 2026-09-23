from email_reader import read_mock_emails
from ticket_processor import create_ticket, process_ticket


def process_inbox():
    emails = read_mock_emails()

    print("AI IT SUPPORT AUTOMATION")
    print("=" * 50)
    print(f"Emails found: {len(emails)}")

    tier1_count = 0
    review_count = 0
    error_count = 0

    for email in emails:
        print("\n" + "=" * 50)
        print(f"Processing: {email['id']}")
        print(f"From: {email['sender']}")
        print(f"Subject: {email['subject']}")

        ticket = create_ticket(
            sender=email["sender"],
            subject=email["subject"],
            body=email["body"]
        )

        try:
            result = process_ticket(ticket)
            analysis = result["analysis"]

            print("\nAI ANALYSIS")
            print(f"Issue: {analysis['issue_summary']}")
            print(f"Category: {analysis['category']}")
            print(f"Priority: {analysis['priority']}")

            print("\nRETRIEVED SOPs")

            retrieval_results = analysis.get(
                "retrieval_results",
                []
            )

            if retrieval_results:
                for retrieval in retrieval_results:
                    print(
                        f"- {retrieval['source']} "
                        f"({retrieval['score']:.4f})"
                    )
            else:
                print("None")

            print("\nUSER-SAFE STEPS")

            if analysis["user_steps"]:
                for number, step in enumerate(
                    analysis["user_steps"],
                    start=1
                ):
                    print(f"{number}. {step}")
            else:
                print("None")

            print("\nTECHNICIAN ACTIONS")

            if analysis["technician_actions"]:
                for number, action in enumerate(
                    analysis["technician_actions"],
                    start=1
                ):
                    print(f"{number}. {action}")
            else:
                print("None")

            print("\nHUMAN REVIEW")
            print(
                f"Required: "
                f"{analysis['requires_human_review']}"
            )

            if analysis["reason"]:
                print(f"Reason: {analysis['reason']}")
            else:
                print("Reason: None")

            if analysis["requires_human_review"]:
                review_count += 1
            else:
                tier1_count += 1

        except Exception as error:
            error_count += 1
            print(f"\nERROR: {error}")

    print("\n" + "=" * 50)
    print("INBOX SUMMARY")
    print("=" * 50)
    print(f"Emails processed: {len(emails)}")
    print(f"Tier 1 tickets: {tier1_count}")
    print(f"Human review required: {review_count}")
    print(f"Errors: {error_count}")


if __name__ == "__main__":
    process_inbox()
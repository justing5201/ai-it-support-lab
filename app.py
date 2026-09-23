from ticket_processor import create_ticket, process_ticket


def main():
    print("AI IT Support Automation Lab")
    print("----------------------------")

    sender = input("\nSender: ")
    subject = input("Subject: ")
    body = input("Issue description: ")

    ticket = create_ticket(
        sender=sender,
        subject=subject,
        body=body
    )

    try:
        result = process_ticket(ticket)

        analysis = result["analysis"]

        print("\nTICKET ANALYSIS")
        print("=" * 50)

        print(
            f"Issue: {analysis['issue_summary']}"
        )

        print(
            f"Category: {analysis['category']}"
        )

        print(
            f"Priority: {analysis['priority']}"
        )

        print("\nRETRIEVED SOPs")

        for retrieval in analysis["retrieval_results"]:
            print(
                f"- {retrieval['source']} "
                f"({retrieval['score']:.4f})"
            )

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
            print(
                f"Reason: {analysis['reason']}"
            )

    except Exception as error:
        print(f"\nERROR: {error}")


if __name__ == "__main__":
    main()
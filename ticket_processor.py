from ai_analyzer import analyze_ticket
from policy import apply_policy

def create_ticket(sender, subject, body):
    return {
        "sender": sender,
        "subject": subject,
        "body": body
    }


def build_ticket_text(ticket):
    return (
        f"Sender: {ticket['sender']}\n"
        f"Subject: {ticket['subject']}\n\n"
        f"{ticket['body']}"
    )


def process_ticket(ticket):
    ticket_text = build_ticket_text(ticket)

    analysis = analyze_ticket(ticket_text)
    analysis = apply_policy(analysis)

    return {
        "ticket": ticket,
        "analysis": analysis
    }
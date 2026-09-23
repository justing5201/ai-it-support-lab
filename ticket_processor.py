from ai_analyzer import analyze_ticket, fallback, SelectionValidationError
from policy import apply_policy

def create_ticket(sender, subject, body):
    return {"sender": sender, "subject": subject, "body": body}

def build_ticket_text(ticket):
    return f"Subject: {ticket['subject']}\n\n{ticket['body']}"

def process_ticket(ticket):
    if not isinstance(ticket, dict) or any(not isinstance(ticket.get(k), str) for k in ("sender", "subject", "body")):
        raise ValueError("Ticket must contain text sender, subject and body")
    try:
        if len(build_ticket_text(ticket)) > 20000:
            analysis = fallback("Ticket exceeds lab input limit; review original message.")
        else:
            analysis = analyze_ticket(build_ticket_text(ticket))
    except SelectionValidationError as error:
        analysis = fallback(f"Model selection rejected: {error}")
    except Exception as error:
        # Avoid exposing tokens, raw messages or backend exception details in the UI.
        analysis = fallback(f"Analysis failed ({type(error).__name__}); check local model and SOP index.")
    analysis = apply_policy(analysis, ticket)
    analysis["ticket_notes"] = (
        f"Reported subject: {ticket['subject']}\n"
        f"Service: {analysis['affected_service']}; scope: {analysis['scope']}.\n"
        f"Impact: {analysis['business_impact']}. Priority: {analysis['priority']} (lab rule).\n"
        f"Routing: {analysis['escalation_owner']}. {analysis['reason']}\n"
        "Status: suggested checks only. No diagnostic, fix or resolution verified."
    )
    return {"ticket": ticket, "analysis": analysis}

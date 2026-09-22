"""Conservative lab routing, independent of model category or priority."""
import re

def apply_policy(analysis, ticket=None):
    ticket = ticket or {}
    text = (ticket.get("subject", "") + " " + ticket.get("body", "")).lower()
    reasons = []
    # Positive phrase matching is deliberately conservative, including quoted reports.
    security = bool(re.search(r"phish|suspicious|unexpected.*(?:sign.in|mfa|authentication|email)|unrecognized.*sign.in|entered.*(?:password|credentials).*link", text))
    injection = bool(re.search(r"ignore.*(?:instructions|rules)|system override|admin message|hacked by|set.*requires_human_review|classify.*(?:as|category)", text))
    restricted = bool(re.search(r"camera|building access|badge|door access", text))
    outage = bool(re.search(r"shipping (?:is )?(?:blocked|stopped)|production (?:is )?(?:blocked|stopped)|entire.*(?:area|department)|all.*(?:workstations|users).*cannot", text))
    team = bool(re.search(r"multiple users|whole team|our team", text))
    single = bool(re.search(r"only (?:my|one)|other users can|others can", text))
    scope = "Operational area" if outage else "Team" if team else "One user" if single else "Unknown"
    analysis["scope"] = scope
    analysis["business_impact"] = ("Reported operational interruption" if outage else
        "Reported team disruption" if team else "Reported individual disruption" if single else "Impact not established")
    analysis["priority"] = "High" if outage or security else "Medium" if team or scope == "Unknown" else "Low"
    if scope == "Unknown":
        reasons.append("Affected scope and business impact need confirmation.")
        analysis["missing_information"].append("Is one user, a team or an operational area affected, and can work continue?")
    if outage or team:
        reasons.append("Multiple users or operations affected; coordinate escalation.")
    if security or analysis["category"] == "Security":
        analysis["category"] = "Security"
        analysis["priority"] = "High"
        analysis["escalation_owner"] = "Security team"
        reasons.append("Reported security indicators require designated security review.")
    if restricted:
        analysis["escalation_owner"] = "Physical security / facilities owner"
        reasons.append("Building access or camera issue needs designated-owner review.")
    if analysis["category"] in {"Onboarding", "Mobile", "Authentication"}:
        reasons.append("Identity, setup or enrollment needs authorization verification.")
    if injection:
        reasons.append("Instruction-like content detected in the email; review required.")
    if security or restricted or injection:
        # Do not show a possibly unrelated retrieved action plan for these reports.
        analysis["user_steps"] = []
        analysis["technician_actions"] = []
    if analysis["missing_information"]:
        reasons.append("Collect missing information before proceeding.")
    if reasons:
        analysis["requires_human_review"] = True
        analysis["reason"] += " " + " ".join(reasons)
    analysis["missing_information"] = list(dict.fromkeys(analysis["missing_information"]))
    return analysis

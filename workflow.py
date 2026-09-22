"""Fictional lab workflow metadata, not any employer's policy."""
import re
PROFILES = {
    "label_printer.md": ("Printer", "Label printing", "Print support / vendor"),
    "printer.md": ("Printer", "Office printing", "Print support / vendor"),
    "onboarding.md": ("Onboarding", "Laptop and access setup", "Endpoint and identity team"),
    "conference_av.md": ("AV", "Conference room AV", "AV support"),
    "mobile_setup.md": ("Mobile", "Mobile enrollment", "Device administrator"),
    "signin_report.md": ("Security", "Account security", "Security team"),
    "phishing.md": ("Security", "Email security", "Security team"),
    "password_reset.md": ("Authentication", "Account access", "Identity team"),
    "vpn.md": ("VPN", "Remote access", "Network support"),
    "windows_performance.md": ("Hardware", "Windows workstation", "Endpoint support"),
}

def procedure_options(text):
    """Only numbered SOP actions are eligible for display. Model selects IDs."""
    groups = {"user": [], "technician": [], "questions": []}
    section = None
    for line in text.splitlines():
        if line.startswith("## "):
            heading = line[3:].lower()
            section = ("user" if heading.startswith("user-safe") else
                       "technician" if heading.startswith("technician") else
                       "questions" if heading.startswith("initial information") else None)
        elif section:
            match = re.match(r"^(?:\d+\. |[-*] )(.+)$", line.strip())
            if match:
                groups[section].append(match.group(1))
    return groups

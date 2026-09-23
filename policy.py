def apply_policy(analysis):
    category = analysis["category"].lower()
    priority = analysis["priority"].lower()

    if "security" in category:
        analysis["requires_human_review"] = True
        analysis["reason"] = (
            "Security-related tickets require human review."
        )

    if priority == "critical":
        analysis["requires_human_review"] = True
        analysis["reason"] = (
            "Critical-priority tickets require human review."
        )

    return analysis
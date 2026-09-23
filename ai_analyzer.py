import json
import ollama

from rag.retriever import (
    retrieve_relevant_sops,
    load_full_sop
)


MIN_RETRIEVAL_SCORE = 0.45


TICKET_SCHEMA = {
    "type": "object",
    "properties": {
        "issue_summary": {
            "type": "string"
        },
        "category": {
            "type": "string"
        },
        "priority": {
            "type": "string",
            "enum": [
                "Low",
                "Medium",
                "High",
                "Critical"
            ]
        },
        "matched_procedures": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "user_steps": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "technician_actions": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "requires_human_review": {
            "type": "boolean"
        },
        "reason": {
            "type": "string"
        }
    },
    "required": [
        "issue_summary",
        "category",
        "priority",
        "matched_procedures",
        "user_steps",
        "technician_actions",
        "requires_human_review",
        "reason"
    ]
}


SYSTEM_PROMPT = """
You are an AI assistant supporting a Tier 1 IT help desk.

Your job is to analyze an incoming IT support ticket using the
company procedure provided to you.

The company procedure is the primary source of truth.

Rules:

1. Base company-specific troubleshooting and technician actions on
   the supplied procedure.

2. Do not invent company procedures or troubleshooting steps that are
   not supported by the supplied procedure.

3. Separate actions an end user can safely perform from actions that
   require an IT technician.

4. Do not tell users to perform administrative or privileged actions.

5. If the supplied procedure does not adequately address the issue,
   set requires_human_review to true.

6. If the procedure says the issue should be escalated, only set
   requires_human_review to true when the ticket contains evidence that
   the escalation condition is actually present.

7. Do not claim that an action has already been performed.

8. Do not request passwords, MFA codes, recovery codes, or other
   authentication secrets.

9. Do not treat an escalation condition as satisfied unless the support
   ticket or documented troubleshooting results provide evidence that
   the condition is actually present.

10. Do not speculate that an escalation condition may exist solely
    because it appears in the supplied procedure.

11. If the supplied procedure is only loosely related to the reported
    issue and does not directly address the reported symptoms, set
    requires_human_review to true rather than adapting unrelated
    procedures.

Return only information required by the JSON schema.
"""


def analyze_ticket(ticket_text):
    # Step 1: Search individual SOP sections to determine
    # which SOP best matches the ticket.
    retrieval_results = retrieve_relevant_sops(
        ticket_text,
        top_k=3
    )

    # Safety check in case the knowledge index is empty.
    if not retrieval_results:
        return {
            "issue_summary": "No matching SOP found for this ticket.",
            "category": "Unknown",
            "priority": "Medium",
            "matched_procedures": [],
            "user_steps": [],
            "technician_actions": [],
            "requires_human_review": True,
            "reason": (
                "No SOPs were available for retrieval. "
                "Human review is required."
            ),
            "retrieval_results": []
        }

    best_result = retrieval_results[0]
    best_score = best_result["score"]

    # Step 2: Reject tickets that do not have a sufficiently
    # relevant SOP match.
    if best_score < MIN_RETRIEVAL_SCORE:
        return {
            "issue_summary": "No matching SOP found for this ticket.",
            "category": "Unknown",
            "priority": "Medium",
            "matched_procedures": [],
            "user_steps": [],
            "technician_actions": [],
            "requires_human_review": True,
            "reason": (
                "No sufficiently relevant company SOP was found. "
                "Human review is required."
            ),
            "retrieval_results": [
                {
                    "source": result["source"],
                    "chunk": result["chunk"],
                    "section": result["section"],
                    "score": round(result["score"], 4),
                    "text": result["text"]
                }
                for result in retrieval_results
            ]
        }

    # Step 3: Once the best SOP is identified, load the
    # entire procedure instead of sending only the top chunks.
    matched_sop = best_result["source"]

    full_sop = load_full_sop(
        matched_sop
    )

    # Step 4: Give the complete SOP and the ticket to the LLM.
    user_prompt = f"""
COMPANY PROCEDURE

SOURCE: {matched_sop}

{full_sop}

SUPPORT TICKET

{ticket_text}

Analyze the support ticket using the complete company procedure above.

Only apply escalation conditions when the ticket contains evidence
that the condition is actually present.

Do not invent troubleshooting steps, administrative actions, or
company procedures that are not supported by the supplied procedure.
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        format=TICKET_SCHEMA,
        options={
            "temperature": 0
        }
    )

    analysis = json.loads(
        response["message"]["content"]
    )

    # The application already knows which SOP was selected,
    # so do not rely on the model to report this correctly.
    analysis["matched_procedures"] = [
        matched_sop
    ]

    # Keep retrieval information for testing and the
    # Streamlit technical-details view.
    analysis["retrieval_results"] = [
        {
            "source": result["source"],
            "chunk": result["chunk"],
            "section": result["section"],
            "score": round(result["score"], 4),
            "text": result["text"]
        }
        for result in retrieval_results
    ]

    return analysis
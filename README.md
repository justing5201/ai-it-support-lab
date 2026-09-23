# AI IT Support Assistant

A local AI-assisted Tier 1 IT support lab that reads support emails, retrieves relevant IT procedures, analyzes tickets with a local LLM, and presents the results in a Streamlit dashboard.

I built this project to explore how AI could support a real help desk workflow without relying on the model to invent company-specific troubleshooting steps.

## What It Does

The system can:

- Read support emails from Outlook through Microsoft Graph
- Use mock inbox data for local testing
- Convert incoming emails into structured tickets
- Retrieve relevant SOPs using semantic similarity
- Reject unsupported tickets when no SOP match is strong enough
- Load the full matched SOP before LLM analysis
- Separate user-safe troubleshooting from technician actions
- Apply deterministic policy rules after the AI response
- Route security-sensitive or unsupported tickets for human review
- Display the full workflow in a Streamlit dashboard

## Current Workflow

```text
Outlook / Mock Inbox
        |
        v
Ticket Processing
        |
        v
Semantic SOP Retrieval
        |
        v
Confidence Check
   /            \
No Match       Match
   |              |
Human Review      v
             Load Full SOP
                  |
                  v
            Local LLM Analysis
                  |
                  v
            Policy Validation
                  |
                  v
          Streamlit Dashboard
```

The retriever searches smaller SOP sections first. If the strongest result clears the configured similarity threshold, the application identifies the source SOP and loads the entire procedure before analysis.

This avoids a problem I ran into earlier where top-k retrieval could find the correct document but omit important sections such as technician troubleshooting or escalation criteria.

## Dashboard

The Streamlit interface can process either mock tickets or messages from a test Outlook mailbox.

It displays:

- Sender and subject
- Email source and received time
- Priority and category
- Issue summary
- Matched SOP and similarity score
- User-safe guidance
- Technician actions
- Human-review decision
- Original email
- Retrieval details for debugging

![Streamlit ticket dashboard](docs/images/streamlit-ticket-dashboard.png)

The retrieval view also exposes which SOP sections were matched and their similarity scores.

![RAG retrieval details](docs/images/retrieval-details.png)

## Microsoft Graph Integration

Outlook access is handled through Microsoft Graph and MSAL using delegated permissions.

The lab currently uses read-only mailbox access so the application can retrieve messages from the signed-in test mailbox without broader write/send permissions.

![Microsoft Graph permissions](docs/images/entra-API-permissions.png)

## Knowledge Base

The current lab knowledge base contains procedures for:

- VPN connection and authentication issues
- Password resets and account lockouts
- Windows printer issues
- Suspected phishing emails
- Windows workstation performance issues

The SOPs are stored as Markdown files and include sections such as:

- purpose / scope
- information to collect
- user-safe troubleshooting
- technician actions
- escalation criteria
- resolution criteria

The knowledge base is intentionally limited. If an issue is not covered well enough, the system should route it for human review rather than force an unrelated SOP match.

## RAG and Scope Detection

The system uses Ollama embeddings and cosine similarity to find relevant SOP sections.

The current retrieval threshold is:

```python
MIN_RETRIEVAL_SCORE = 0.45
```

This was added after testing showed that semantic search will always return a “closest” result, even when the issue is not actually covered by the knowledge base.

The current scope-detection test contains:

```text
20 cases total
10 supported
10 unsupported
```

The latest run correctly selected the expected SOP for supported cases and rejected the unsupported cases.

That result is only for this small lab dataset and should not be interpreted as production-level accuracy.

Run the tests with:

```powershell
python -m tests.test_retrieval
python -m tests.test_scope_detection
```

## Safety and Human Review

The LLM is not treated as the final authority.

A deterministic policy layer runs after AI analysis so application rules can override model decisions when needed.

Examples include:

- security-related tickets requiring human review
- low-confidence SOP matches being rejected
- privileged technician actions being kept separate from end-user guidance

The analysis prompt also instructs the model to:

- use the supplied SOP as its source of truth
- avoid inventing undocumented procedures
- avoid requesting passwords or MFA secrets
- avoid assuming escalation conditions are true without evidence
- send inadequately covered issues to human review

## Why I Built It This Way

The project started as a much simpler LLM ticket classifier.

While building it, I ran into several problems that changed the design:

- hard-coding every possible IT issue was not realistic
- unrelated SOPs could still receive non-zero similarity scores
- top-k chunk retrieval could omit important parts of the correct SOP
- the LLM could make routing decisions I did not want to trust by itself
- normal test cases could pass while unsupported inputs behaved badly

Those problems led me to add:

- RAG instead of issue-by-issue hard-coding
- retrieval thresholds
- explicit unsupported-ticket handling
- section-based SOP indexing
- full-SOP loading after retrieval
- deterministic policy enforcement
- separate scope-detection tests

The goal is not to replace a technician. The goal is to automate the repetitive parts of Tier 1 triage while keeping uncertain or sensitive decisions under human control.

## Project Structure

```text
ai-it-support-lab/
|
├── data/                 # Mock inbox and sample ticket data
├── docs/images/          # Project screenshots
├── knowledge_base/       # IT SOPs
├── rag/                  # SOP ingestion, embeddings, retrieval
├── tests/                # Retrieval, scope, security, adversarial tests
|
├── ai_analyzer.py
├── app.py
├── dashboard.py
├── email_reader.py
├── graph_auth.py
├── outlook_reader.py
├── policy.py
├── process_inbox.py
├── ticket_processor.py
└── requirements.txt
```

## Running the Project

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Make sure Ollama is running and the required local models are available.

Build the SOP index:

```powershell
python rag/ingest_sops.py
```

Run the tests:

```powershell
python -m tests.test_retrieval
python -m tests.test_scope_detection
```

Start the dashboard:

```powershell
streamlit run dashboard.py
```

Outlook mode also requires a Microsoft Entra app registration configured for Microsoft Graph access.

Do not commit `.env`, access tokens, device codes, or other secrets.

## Tech Stack

- Python
- Ollama
- Llama 3
- EmbeddingGemma
- Microsoft Graph API
- Microsoft Entra ID / MSAL
- Streamlit
- JSON
- Markdown
- Git / GitHub

## Next Steps

The core help desk workflow is working. The next phase is focused more on security and validation than adding more features.

Planned next steps:

- update the existing adversarial tests for the current RAG architecture
- test prompt injection through support emails
- test attempts to manipulate priority, category, or routing
- test whether malicious ticket content can bypass human-review policy
- test indirect prompt injection through retrieved SOP content
- improve grounding and policy controls based on those results
- expand the evaluation set with more ambiguous and edge-case tickets
- add technician-reviewed response drafting after the security pass
- make one final Streamlit UI cleanup for portfolio presentation

The project is a learning lab, not a production help desk platform.
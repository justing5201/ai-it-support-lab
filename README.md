# AI IT Support Lab

A personal Python project that turns support emails into draft help desk tickets. It reads a message, looks for a relevant troubleshooting procedure, suggests questions and next checks, and flags issues that need a technician's review.

I built this to practice the kind of intake, troubleshooting, documentation, and escalation work I am learning as an entry-level IT support technician. The company, users, devices, emails, and procedures in the demo are fictional. This project is not connected to my employer's systems.

## What it does

- Reads sample emails from a local JSON file or messages from a dedicated Outlook test mailbox using Microsoft Graph.
- Searches Markdown support procedures with local Ollama embeddings.
- Uses a local language model to summarize the reported issue and select relevant questions and steps already written in the procedure.
- Separates user checks from technician actions.
- Uses Python rules to suggest priority, identify reported impact, and route sensitive or unclear cases for human review.
- Shows the draft ticket, source procedure, and retrieval details in a Streamlit dashboard.

For example, one fictional ticket says a single workstation cannot print labels while others can. Another says all workstations in a shipping area cannot print and shipping has stopped. The lab treats those as different levels of impact and asks for review of the wider outage.

The output is **a draft for a technician**, not a diagnosis or proof that any check has been performed.

## How the pieces fit together

1. `dashboard.py` reads sample emails or connects to the Outlook test mailbox.
2. `rag/ingest_sops.py` builds a local search index from the Markdown files in `knowledge_base/`.
3. `ai_analyzer.py` finds a likely procedure and asks Ollama to select documented questions and steps.
4. `ticket_processor.py` and `policy.py` assemble the draft ticket and apply review rules.
5. `history_report.py` makes a separate sample report of repeated issues from fictional ticket history.

The lab includes procedures for printing, label printers, VPN, passwords, Windows performance, new-hire setup, meeting-room AV, mobile setup, phishing, and unexpected sign-in reports. The search index is generated on your computer; it is not stored in Git.

## Run it locally

From the repository folder, use Python 3.11 or newer. In Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Install and start [Ollama](https://ollama.com/), then download the two models and build the procedure index:

```powershell
ollama pull embeddinggemma
ollama pull llama3
python -m rag.ingest_sops
```

Start the dashboard:

```powershell
streamlit run dashboard.py
```

Choose **Mock Inbox** and click **Process Inbox** to try the fictional examples. If you edit a procedure in `knowledge_base/`, rebuild the index with `python -m rag.ingest_sops`.

You can also try the command-line version with `python app.py` or create the [sample recurring-issue report](docs/sample-vendor-report.md) with `python history_report.py`.

### Optional Outlook test mailbox

The Outlook option uses a personal test mailbox and a Microsoft Entra app registration with delegated `Mail.Read` permission. Copy `.env.example` to `.env`, add your app's client ID and tenant, and run `python test_outlook.py` to check the connection before using Outlook in the dashboard. The app reads messages; it does not send replies. Keep credentials and tokens out of Git.

## Testing and current status

Run the automated tests:

```powershell
python -m unittest discover -s tests -p "test_pipeline.py" -v
```

The [recorded test run](docs/test-output.txt) passed **24 tests** using simulated model and embedding responses. Those tests cover issues such as a single-user printer failure versus a shipping outage, missing procedures, bad model output, and instructions planted in an email. A dashboard check also processed five messages without UI errors while the procedure index was missing.

**Real-model results still need checking on a computer with Ollama running.** After building the index, use these commands to check retrieval and the full pipeline:

```powershell
python -m tests.test_retrieval
python -m tests.test_scope_detection
python -m tests.security_tests
python -m tests.adversarial_tests
```

The expanded procedure set has not been measured with the real models yet. The earlier 24 passing tests do not establish ticket accuracy or security against every prompt injection.

## Limits and next steps

The lab can pick an irrelevant procedure, miss unfamiliar wording, or ask an unnecessary question. Its similarity score is only a search score, not a reliable probability that the answer is correct. The model's summary and selected steps need a technician to check them. If the index, procedure, or model is unavailable, the ticket is sent for review without suggested actions.

My next step is to run the full test set with Ollama, look at mistakes in the fictional tickets, and improve the procedures and routing rules based on those results. I would only consider using ideas from this project at work after learning the actual tools and procedures and obtaining the appropriate approval.

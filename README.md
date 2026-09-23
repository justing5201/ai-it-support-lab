# Technician Support Lab

A small Python decision-support lab for **fictional Alder Works**. Practice onsite IT intake, SOP lookup, suggested checks, escalation and ticket documentation. It has no knowledge of any employer's internal tools or policies.

## What changed

- Repaired SOP indexing: section names are now extracted from each Markdown chunk.
- Repaired obsolete test entry points and made evaluation failures return exit code 1.
- Added label printing, new-hire intake, conference AV, mobile enrollment and unexpected sign-in procedures alongside the original five SOPs.
- Added 12 fictional emails with one-user faults, a shipping outage, incomplete reports, security reports, injected instructions and unsupported equipment.
- Added service, reported scope/impact, questions, SOP sections, escalation owner and draft notes to the existing Streamlit dashboard and CLI.
- Added a vendor handoff report from separately curated fictional history.

## Workflow

1. Read the mock inbox or a dedicated Outlook test mailbox.
2. Retrieve three SOP sections using EmbeddingGemma and cosine similarity.
3. Reject a top score below `0.45`; otherwise load the full matched SOP.
4. Ask local `llama3` to summarize the reported symptom and select numbered action/question IDs.
5. Validate JSON fields, types and ID ranges. Display action text from the SOP, never generated commands.
6. Apply conservative Python routing rules and produce notes explicitly marked as unverified suggestions.

The model can request review but cannot select category, priority or escalation owner. Service and default owner come from `workflow.py`. `policy.py` uses reported phrases to identify scope and conservative escalation triggers. Model, index, SOP or validation failures return a structured human-review result with no suggested actions.

### Fictional examples

| Report | Lab behavior |
| --- | --- |
| Only my label printer fails; others can print | One user, Low priority; collect any remaining information |
| All workstations cannot print; shipping is blocked | Operational area, High priority, human review |
| New employee laptop request | Endpoint/identity owner; verify approvals; imaging and account changes remain technician tasks |
| Unclear issue with no affected scope | Ask scope/impact question; human review |
| Suspicious email or unexpected MFA request | Security owner, High priority, suppress action suggestions |
| Building access or camera report | Designated physical-security/facilities owner; suppress action suggestions |
| Instruction-like email content | Human review; suppress action suggestions |

These are training rules, not service-level commitments. A reported phrase is not independently verified evidence.

## Setup (Windows PowerShell, Python 3.11+)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Install/start Ollama on your computer, then:

```powershell
ollama pull embeddinggemma
ollama pull llama3
python -m rag.ingest_sops
streamlit run dashboard.py
```

The index is generated locally and excluded from Git. Rebuild it whenever SOPs or the embedding model change. Code paths work independently of the current working directory; run module commands from the repository root.

Other entry points:

```powershell
python app.py
python process_inbox.py
python history_report.py
```

`history_report.py` needs only Python's standard library. It groups distinct synthetic records by service, asset and location, lists observed/reported evidence and records unknowns. It does not infer a common root cause or invent performed fixes. See [sample report](docs/sample-vendor-report.md).

## Outlook integration

`outlook_reader.py` contains a real Microsoft Graph reader using delegated `Mail.Read`, MSAL device login and a preference for plain-text bodies. For a dedicated test mailbox:

1. Configure your own Entra public-client registration for the mailbox account type and device-code flow, with delegated `Mail.Read`.
2. Copy `.env.example` to `.env`; enter your test app ID and tenant (`common` when appropriate for your registration).
3. Send fictional support emails to that test mailbox.
4. Run `python test_outlook.py` and follow the login instructions printed in the terminal.
5. Run the dashboard, select Outlook and process the test messages. Login may be requested again; persistent token caching is not implemented.

No messages are sent and no accounts, endpoints or devices are changed. Do not use company data or connections without the company's authorization. Do not commit `.env` or authentication artifacts.

## Tests and observed results

Run deterministic tests, with model responses and embeddings mocked:

```powershell
python -m unittest discover -s tests -p "test_pipeline.py" -v
```

Observed in this implementation environment: **24 tests passed**. Dependency installation from `requirements.txt`, Python compilation and `git diff --check` also succeeded. A Streamlit AppTest smoke check loaded the dashboard and processed five tickets with the missing-index fallback: zero UI exceptions, five human-review cases and five rejected-SOP warnings. [Full actual output](docs/test-output.txt). Coverage includes fresh index construction, section metadata, one-user versus operational outage, missing information, malicious email instructions, security routing, unsupported requests, missing files, unavailable backends, malformed model output, action ID validation, path containment and history deduplication.

The fresh-index test uses fake embeddings: it proves index construction, not semantic retrieval quality. Unit tests do not establish real LLM accuracy or comprehensive prompt-injection resistance.

### Checks still required on your machine

After pulling both models and rebuilding the index:

```powershell
python -m tests.test_retrieval
python -m tests.test_scope_detection
python -m tests.security_tests
python -m tests.adversarial_tests
python test_outlook.py
streamlit run dashboard.py
```

- Retrieval checks must select appropriate SOPs and reject unsupported equipment. The expanded knowledge base may require threshold calibration.
- Baseline checks cover the 12 mock emails; adversarial checks require actual model processing, not backend-error fallbacks.
- Confirm the dashboard displays questions, accepted SOP sections, routing and unverified draft notes. Rejected retrieval candidates must not be labeled as accepted procedures.
- Verify Outlook retrieves fictional messages and handles authentication errors visibly.

**Not verified here:** real Ollama embeddings/generation or authenticated Graph ingestion. No Ollama executable/server was available. Running the live baseline without an index returned **0/12, exit 1**, with safe review results. That is expected dependency failure, not a model-quality score. This replaces the previous README's small-dataset accuracy claim; no new live accuracy claim is made.

## Limitations

- Phrase rules can miss unfamiliar wording or escalate harmless quoted/negated text. Conservative review is expected.
- Similarity is not a probability of correctness. The `0.45` threshold has not been recalibrated for the expanded SOP set.
- Actions are limited to approved local SOP text, but the model can still select an irrelevant action or omit a needed question. SOP authoring/review remains essential.
- The model-written symptom summary remains untrusted text. Human review is needed before using notes operationally.
- The index does not track SOP versions. Rebuild after every SOP edit; stale indexing can degrade retrieval.
- Dashboard results last only for the session. History reports use a separate synthetic fixture, not captured production incidents.
- Outlook reads only the requested first batch. Production pagination, persistent authentication, ticket-system integration, SLA handling and multi-user operation are outside this lab.
- Old screenshots under `docs/images` show the earlier implementation and are not verification of this version.

## Files to learn first

- `ticket_processor.py`: brings together analysis, failure handling, routing and notes.
- `ai_analyzer.py`: retrieves procedures and validates model selections.
- `workflow.py`: fictional service owners and parsing of numbered SOP options.
- `policy.py`: explicit routing rules you can inspect and test.
- `knowledge_base/`: fictional procedures; user and technician actions are separated.
- `tests/test_pipeline.py`: controlled examples proving application behavior.
- `history_report.py`: recurring-issue evidence for a vendor handoff.

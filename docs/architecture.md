# Architecture Notes — AI-Powered Reinsurance Contract Review

## Design principle

This project uses a simple but defendable pattern:

```text
Unstructured contract text
   → specialised AI review agents
   → structured business outputs
   → human reviewer decision
```

The system is deliberately not designed as an autonomous decision-maker. It is a reviewer-support workflow.

---

## High-level architecture

```text
User
 ↓
Streamlit UI
 ↓
Input handler
 ├── PDF upload → pypdf text extraction
 ├── pasted text
 └── built-in synthetic sample
 ↓
Compliance Agent
 ↓
Technical Terms Agent
 ↓
Executive Summary Agent
 ↓
Results UI + downloadable markdown report
 ↓
Human reviewer
```

---

## Components

## 1. Streamlit UI

File: `app.py`

Purpose:

- collect Anthropic API key;
- choose input mode;
- upload PDF, paste text or use sample contract;
- run the three-agent pipeline;
- show progress to the user;
- display outputs in tabs;
- provide downloadable markdown report.

Why it matters:

- makes the system demonstrable to business stakeholders;
- avoids notebook-only presentation;
- provides a simple browser-based interface.

---

## 2. PDF extraction

Function: `extract_text_from_pdf(file)`

Purpose:

- reads uploaded PDF files using `pypdf`;
- extracts text from each readable page;
- joins text into one contract string.

Why it matters:

- most contract review processes start from PDF documents;
- this creates a basic ingestion layer.

Limitation:

- no OCR;
- scanned PDFs may fail;
- no layout-aware parsing;
- no clause-level citation mapping.

---

## 3. Compliance Agent

Function: `compliance_agent(client, contract_text)`

Purpose:

Reviews only compliance-related issues:

- sanctions clauses;
- named sanctions regimes;
- DORA / regulatory obligations;
- missing compliance clauses;
- red flags requiring human review.

Why it matters:

- compliance analysis should not be mixed with technical contract extraction;
- separating this agent makes the output easier to test and challenge.

---

## 4. Technical Terms Agent

Function: `terms_agent(client, contract_text)`

Purpose:

Extracts operational and technical contract terms:

- delegated authority limits;
- bordereaux obligations;
- reporting frequency;
- unclear or ambiguous wording.

Why it matters:

- these are operational risk drivers in MGA / delegated authority workflows;
- unclear wording can create downstream claims, bordereaux and compliance issues.

---

## 5. Executive Summary Agent

Function: `summary_agent(client, compliance_output, terms_output)`

Purpose:

Synthesises the two specialist reviews into:

- top 5 risks;
- key contract weaknesses;
- priority actions;
- human review recommendation.

Why it matters:

- executives need prioritised actions, not raw model output;
- this creates a business-facing handoff.

---

## 6. Report builder

Function: `build_report(compliance_out, terms_out, summary_out, source_label)`

Purpose:

Creates a downloadable markdown report containing:

- timestamp;
- source label;
- compliance analysis;
- technical terms analysis;
- executive summary;
- human-review disclaimer.

Why it matters:

- makes the review portable;
- creates a basic output artefact;
- supports reviewer handoff.

---

## Why multi-agent design?

A single prompt could produce a contract review, but it is harder to test and debug.

This design separates:

| Agent | Responsibility | Failure mode isolated |
|---|---|---|
| Compliance Agent | Regulatory and compliance risks | Missing or hallucinated compliance risks |
| Technical Terms Agent | Operational contract structure | Incorrect extraction of limits/reporting terms |
| Summary Agent | Executive synthesis | Poor prioritisation or unclear actions |

The point is not to claim multi-agent is always better. The point is that separation of concerns makes the system easier to explain, inspect and improve.

---

## Governance model

Current governance pattern:

- synthetic data only;
- human-review disclaimer;
- no autonomous approval;
- explicit limitations;
- separation of analysis and decision;
- downloadable report for reviewer challenge.

Future production governance required:

- persistent audit trail;
- document retention policy;
- reviewer sign-off workflow;
- access control;
- prompt/model versioning;
- evaluation dataset;
- monitoring and regression testing;
- legal/compliance review before live use.

---

## Production-readiness assessment

| Capability | Current status | Production requirement |
|---|---|---|
| Browser UI | Implemented | Hardened access control |
| PDF upload | Basic | OCR/layout-aware parsing |
| AI review | Implemented through Claude API | Evaluation and monitoring |
| Human review | Recommended in output | Enforced approval workflow |
| Report export | Markdown download | Persistent document store |
| Audit trail | Not persistent | Immutable audit log |
| Data security | Local/session-based | Encryption, access control, retention |
| Evaluation | Informal | Golden dataset + regression testing |

---

## Recommended next architecture iteration

```text
contracts/
  synthetic_sample_001.md
src/
  reinsurance_review/
    __init__.py
    extraction.py
    agents.py
    report.py
    schemas.py
app.py
tests/
  test_extraction.py
  test_report.py
  test_schema_validation.py
docs/
  architecture.md
  demo_script.md
examples/
  sample_output.md
```

Why:

- separates UI from business logic;
- makes tests easier;
- supports schema validation;
- improves professional maintainability.

# Known Limitations and Production Readiness

This document exists to make the project interview-safe and credible. The system is a production-style prototype, not a live production deployment in an insurer, reinsurer or MGA.

---

## Current Limitations

## 1. Synthetic data only

All contracts used in the repo are synthetic demonstration contracts.

Current implication:

- safe for public portfolio use;
- no confidential client data;
- no evidence yet against real-world contract variability.

Production requirement:

- test on redacted real contracts or a representative synthetic benchmark;
- legal/compliance approval before using live documents.

---

## 2. No formal evaluation benchmark

Current evaluation is informal and based on manual spot-checking.

Production requirement:

- golden dataset of reviewed contracts;
- expected risk annotations from senior reviewers;
- metrics for issue coverage, false positives, false negatives and faithfulness;
- regression testing across prompt and model changes.

---

## 3. No persistent audit trail

The app produces a downloadable markdown report, but it does not store immutable audit logs.

Production requirement:

- persistent audit log;
- timestamped run metadata;
- model version;
- prompt version;
- user ID;
- document hash;
- reviewer actions;
- retention policy.

---

## 4. No enforced human approval gate

The output recommends human review, but the system does not enforce reviewer sign-off.

Production requirement:

- workflow status: draft / reviewer pending / approved / rejected / remediated;
- reviewer identity;
- approval timestamp;
- comments and overrides;
- escalation path.

---

## 5. Basic PDF extraction only

`pypdf` extracts text from readable PDFs.

Limitations:

- scanned documents may fail;
- no OCR;
- no table parsing;
- no clause-level source citation;
- no layout preservation.

Production requirement:

- OCR fallback;
- clause segmentation;
- page/section references;
- confidence on extraction quality.

---

## 6. Prompt-based outputs

The current output is structured markdown, not validated JSON.

Production requirement:

- Pydantic schemas;
- JSON schema validation;
- retry logic on invalid format;
- deterministic post-processing;
- versioned output schema.

---

## 7. No access control

The local Streamlit app uses a session API key and does not provide authentication or RBAC.

Production requirement:

- SSO or enterprise auth;
- role-based access;
- secure secret management;
- restricted document access;
- logging of user actions.

---

## 8. No cost or latency monitoring

The app calls Claude three times per review and does not track cost or latency.

Production requirement:

- per-run token usage;
- latency by agent;
- cost per contract;
- retry limits;
- timeout handling;
- model fallback policy.

---

## 9. No integration with enterprise systems

Current app is standalone.

Production requirement:

- document management integration;
- GRC / vendor risk tooling integration;
- contract lifecycle management integration;
- email / workflow notification integration;
- secure storage.

---

## How to Answer Production Questions in Interview

### If asked: “Is this production?”

Answer:

> “Not live carrier production. It is a production-style prototype. It demonstrates the architecture and control model I would take into production, but it would require access control, audit storage, formal evaluation, monitoring and approval workflow before enterprise deployment.”

### If asked: “What impact did it have?”

Answer:

> “The impact is architectural and operational, not measured enterprise ROI. It shows how to convert manual reinsurance contract review into a structured AI-assisted workflow. In production I would measure review time reduction, issue coverage, reviewer override rate, false positives, false negatives and audit completeness.”

### If asked: “Why should we care?”

Answer:

> “Because regulated insurance businesses cannot just plug in a chatbot. They need workflows where AI supports analysis, but humans retain accountability and governance controls are explicit.”

---

## Next Build Priorities

1. Refactor `app.py` into `src/reinsurance_review/` modules.
2. Add structured JSON outputs and Pydantic validation.
3. Add sample contracts and expected outputs.
4. Add unit tests for PDF extraction, report building and schema validation.
5. Add prompt/model version metadata to outputs.
6. Add persistent audit log.
7. Add reviewer approval state.
8. Build a small evaluation dataset.

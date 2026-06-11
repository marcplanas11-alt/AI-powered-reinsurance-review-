# Executive Demo Script — AI-Powered Reinsurance Contract Review

Use this script when asked:

> “Show me the AI system in production that you are most proud of: what it does, how you built it and what impact it had.”

## Important positioning

Do **not** claim this is a live production deployment inside an insurer or reinsurer.

Use this wording:

> “This is the insurance-domain AI system I am most proud of architecturally. I would describe it as a production-style prototype rather than a live carrier deployment. It demonstrates the workflow, control logic and human-review model I would take into production.”

---

## 1. Opening — 30 seconds

> “The system I want to show is an AI-powered reinsurance contract review workflow. The business problem is that reinsurance and binding authority agreements are long, repetitive and risk-heavy. Reviewers need to identify sanctions issues, DORA obligations, delegated authority limits, bordereaux terms, audit rights and escalation gaps. That work is often manual, inconsistent and hard to standardise.”

> “I built a three-agent workflow that takes a contract, separates the review into compliance analysis, technical terms extraction and executive summarisation, and produces a structured review pack for a human reviewer.”

---

## 2. Business value — 45 seconds

> “The aim is not to replace legal, compliance or underwriting judgement. The aim is to improve first-pass review: surface the right risks faster, structure the review consistently, and give the human reviewer a better starting point.”

> “This is especially relevant in MGA / delegated authority environments where contract weaknesses can create operational, regulatory and reporting issues downstream.”

Key business value:

- faster first-pass review;
- more consistent risk categories;
- clearer handoff to human reviewers;
- reusable pattern for AI-assisted insurance operations;
- better executive visibility over contract weaknesses.

---

## 3. Show the app — 60 seconds

Open the Streamlit app:

```bash
streamlit run app.py
```

In the sidebar:

1. Enter Anthropic API key.
2. Select **Use sample contract**.
3. Point to the agent pipeline shown in the sidebar:
   - Compliance Agent;
   - Technical Agent;
   - Summary Agent.

Say:

> “The interface supports PDF upload, pasted text or a synthetic sample. For the interview demo I use the sample contract because it is safe: no real client data and no confidential wording.”

---

## 4. Explain the sample contract — 45 seconds

The sample deliberately includes:

- delegated authority limit of USD 500,000;
- unclear catastrophe-exposed risk wording;
- monthly premium and claims bordereaux obligations;
- sanctions clause without named regimes such as OFAC, HM Treasury or EU;
- no explicit DORA operational resilience wording;
- no ICT incident reporting or third-party risk management provisions;
- no GDPR clause;
- audit rights with unclear frequency and notice period;
- unclear escalation procedures.

Say:

> “The sample is synthetic but realistic. It contains the type of contract weaknesses that an operations, compliance or reinsurance analyst would want to catch before the agreement is approved or renewed.”

---

## 5. Run the review — 90 seconds

Click **Run Review**.

While it runs, explain the workflow:

> “The system runs three specialised agents rather than one generic prompt. The reason is auditability and separation of concerns. The compliance agent should not be distracted by operational wording. The technical terms agent should not pretend to be a compliance reviewer. The summary agent consolidates both into a business-ready view.”

Then explain each agent:

### Compliance Agent

> “This agent looks for sanctions wording, regulatory gaps, missing compliance clauses and DORA-related weaknesses.”

### Technical Terms Agent

> “This agent extracts operational contract terms: delegated authority limits, bordereaux obligations, reporting cadence and ambiguous wording.”

### Summary Agent

> “This agent takes both analyses and produces the executive view: top risks, contract weaknesses, priority actions and whether human review is required.”

---

## 6. Walk through the output — 2 minutes

Open each tab.

### Compliance tab

Say:

> “Here I want to see whether the system catches the missing or weak control language: vague sanctions regimes, no DORA operational resilience obligations, missing GDPR and unclear escalation procedures.”

### Technical Terms tab

Say:

> “Here I want operational extractability: limits, bordereaux duties, reporting cadence and ambiguous delegated authority wording.”

### Executive Summary tab

Say:

> “This is the business-facing output. An executive does not want raw model reasoning. They want prioritised risks, weaknesses and actions.”

### Contract Text tab

Say:

> “I keep the extracted source text visible so the reviewer can challenge the output against the underlying contract.”

---

## 7. Explain how you built it — 90 seconds

> “Technically, I built it in Python with Streamlit for the interface, Anthropic Claude for the agent reasoning, and pypdf for PDF text extraction. The app has three clear input modes, then runs the agent sequence and renders the results in separate tabs. It also builds a downloadable markdown report so the output can be shared or reviewed offline.”

Mention files:

- `app.py`: app, UI and agent functions;
- `requirements.txt`: Streamlit, Anthropic and pypdf;
- `README.md`: business context and run instructions;
- `docs/architecture.md`: architecture explanation;
- `KNOWN_LIMITATIONS.md`: honest production limitations;
- `examples/sample_output.md`: rehearsal output.

---

## 8. Impact — 60 seconds

Do not fake metrics.

Use this answer:

> “The measured impact is not from a live carrier deployment. The impact of the prototype is operational: it shows how a manual reinsurance review process can be converted into a structured AI-assisted workflow. In a production environment I would measure review time reduction, issue coverage, false positives, false negatives, reviewer override rate and audit completeness.”

Then add:

> “The broader value is that this pattern is reusable. The same architecture can be adapted to contract renewal review, bordereaux exception handling, vendor governance, claims triage or underwriting submission intake.”

---

## 9. Anticipate CEO objections

### “Is this really production?”

> “Not live carrier production. I would call it production-style. It has a working app and a clear workflow, but before production it would need access control, persistent audit storage, reviewer approval workflow, monitoring, evaluation and integration with document systems.”

### “Why three agents instead of one prompt?”

> “Because the review has different expert lenses. Separating compliance, technical extraction and executive synthesis makes the workflow easier to test, debug and explain.”

### “How would you prove it works?”

> “I would build a golden dataset of synthetic or redacted contracts, annotate expected risks with senior reviewers, and score faithfulness, risk coverage, false positives, false negatives and format validity.”

### “What is the risk?”

> “The main risk is hallucination or overconfidence. That is why the system supports human review and should not automatically approve or reject contracts.”

### “What would you build next?”

> “First, structured JSON outputs with schema validation. Second, evaluation and regression testing. Third, persistent audit trail. Fourth, reviewer sign-off workflow. Fifth, integration with document management or GRC tooling.”

---

## 10. Final closing statement

> “What I am proud of is not that I built a flashy AI demo. I built a workflow around a real insurance operations pain point. It separates expert tasks, produces business-ready outputs, keeps the human accountable and makes the path to production explicit. That is the difference between using GenAI as a toy and designing AI for a regulated business process.”

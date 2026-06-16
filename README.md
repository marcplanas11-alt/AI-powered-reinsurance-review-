# AI-Powered Reinsurance Contract Review

Production-style multi-agent AI workflow for reviewing synthetic reinsurance contracts and producing structured, business-ready risk outputs for human reviewers.

> **Interview positioning:** this is a **production-style prototype**, not a live carrier deployment. It demonstrates the operating model, architecture and governance controls I would take into production for reinsurance / MGA contract review. No real client contracts or confidential data are included.

---

## Executive Summary

Reinsurance contract review, especially binding authority and delegated authority agreements, is slow, repetitive and hard to standardise. Critical issues such as sanctions wording, DORA obligations, delegated authority limits, bordereaux reporting and escalation procedures can be missed or documented inconsistently.

This project demonstrates a three-agent AI workflow that turns an unstructured contract into a structured review pack:

1. **Compliance Agent** — identifies sanctions, regulatory, DORA and missing-clause risks.
2. **Technical Terms Agent** — extracts delegated authority limits, bordereaux obligations, reporting terms and unclear wording.
3. **Executive Summary Agent** — consolidates findings into top risks, weaknesses, priority actions and human-review recommendation.

The system does **not** make final legal, compliance or underwriting decisions. It supports a human reviewer by accelerating first-pass review and making risks easier to inspect, challenge and document.

---

## Why This Matters for an AI Lead Consultant Role

This repo is not a generic chatbot. It demonstrates the pattern an AI Lead Consultant needs to defend with business stakeholders:

- business process first, AI second;
- specialised agents for distinct review tasks;
- structured outputs for operational handoff;
- human-in-the-loop design;
- clear limitations and no false claim of production deployment;
- insurance-specific domain context: reinsurance, MGA operations, delegated authority, bordereaux, sanctions and DORA.

The core message: **Claude analyses; the workflow structures; the human decides.**

---

## Problem

Reinsurance contract review is:

- time-consuming and repetitive;
- difficult to standardise across reviewers;
- dependent on individual expertise;
- exposed to inconsistent identification of regulatory and operational risks;
- difficult to convert into structured remediation actions.

Typical issues the workflow is designed to surface:

- vague sanctions clauses;
- missing named sanctions regimes;
- absent DORA operational resilience wording;
- weak ICT incident reporting language;
- unclear delegated authority limits;
- missing GDPR / data protection clauses;
- incomplete audit rights;
- unclear escalation procedures;
- bordereaux obligations without operational consequences.

---

## Solution

A Streamlit app runs a three-agent Claude workflow:

```text
Contract input
   ↓
Compliance Agent
   ↓
Technical Terms Agent
   ↓
Executive Summary Agent
   ↓
Structured markdown review report
   ↓
Human reviewer decision
```

Input methods:

- upload PDF;
- paste contract text;
- use built-in synthetic sample contract.

Outputs:

- compliance analysis;
- technical terms analysis;
- executive summary;
- extracted contract text;
- downloadable markdown report.

---

## Architecture

| Component | File | Purpose |
|---|---|---|
| Streamlit UI | `app.py` | Browser interface, API key input, contract input, progress bar, result tabs and report download |
| PDF extraction | `app.py` / `pypdf` | Extracts text from uploaded PDF contracts |
| Compliance Agent | `compliance_agent()` | Reviews sanctions, DORA, regulatory gaps and missing compliance clauses |
| Technical Terms Agent | `terms_agent()` | Extracts delegated authority limits, bordereaux duties, reporting frequency and ambiguous wording |
| Summary Agent | `summary_agent()` | Consolidates findings into top risks, weaknesses and priority actions |
| Report builder | `build_report()` | Produces a downloadable markdown review report |
| Dependencies | `requirements.txt` | Minimal packages needed to run the app |
| Demo guide | `docs/demo_script.md` | Step-by-step executive interview script |
| Architecture notes | `docs/architecture.md` | Technical and business architecture explanation |
| Limitations | `KNOWN_LIMITATIONS.md` | Honest scope boundaries and production-readiness gaps |
| Example output | `examples/sample_output.md` | Static sample output for interview rehearsal |

---

## How It Works

### 1. Input

The user provides a reinsurance contract through PDF upload, pasted text or the built-in synthetic sample.

### 2. Text extraction

If the input is a PDF, `pypdf` extracts text page by page. If no text can be extracted, the app stops and asks the user to check the file.

### 3. Compliance review

The Compliance Agent focuses only on compliance-related issues:

- sanctions clauses;
- regulatory obligations;
- DORA gaps;
- missing compliance clauses;
- red flags requiring human review.

### 4. Technical terms review

The Technical Terms Agent focuses only on operational contract structure:

- delegated authority limits;
- bordereaux obligations;
- reporting frequency;
- unclear or ambiguous wording.

### 5. Executive synthesis

The Summary Agent receives the outputs of the first two agents and produces:

- top 5 risks;
- key contract weaknesses;
- priority actions;
- human-review recommendation.

### 6. Human review

The output is explicitly positioned as reviewer support. The system does not approve, reject or negotiate contracts automatically.

---

## Full Setup and Execution Guide

Use this section when you want to clone the repository from GitHub and run the Streamlit app locally from zero.

### 0. Prerequisites

You need:

- Git installed;
- Python installed;
- an Anthropic API key;
- terminal access through Windows CMD, PowerShell, macOS Terminal or Linux shell.

Check Git:

```bash
git --version
```

Check Python:

```bash
python --version
```

On some macOS or Linux machines, Python may be available as `python3` instead:

```bash
python3 --version
```

---

### 1. Clone the repository

```bash
git clone https://github.com/marcplanas11-alt/AI-powered-reinsurance-review-.git
```

What this does:

- downloads the repository from GitHub;
- creates a local project folder;
- brings the code, README, docs and dependency file into your machine.

---

### 2. Enter the project folder

```bash
cd AI-powered-reinsurance-review-
```

Check that you are inside the correct folder:

```bash
dir
```

On macOS or Linux:

```bash
ls
```

You should see files such as:

```text
app.py
requirements.txt
README.md
docs/
examples/
```

---

### 3. Create a virtual environment

A virtual environment isolates this project’s Python packages from the rest of your computer.

#### Windows CMD

```bash
python -m venv .venv
```

#### macOS / Linux

```bash
python3 -m venv .venv
```

---

### 4. Activate the virtual environment

#### Windows CMD

```bash
.venv\Scripts\activate
```

#### Windows PowerShell

```bash
.venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

When it is activated, your terminal usually shows something like:

```text
(.venv)
```

---

### 5. Upgrade pip

#### Windows

```bash
python -m pip install --upgrade pip
```

#### macOS / Linux

```bash
python3 -m pip install --upgrade pip
```

---

### 6. Install the project dependencies

```bash
pip install -r requirements.txt
```

This installs the packages listed in `requirements.txt`:

```text
streamlit
anthropic
pypdf
```

Purpose of each package:

| Package | Purpose |
|---|---|
| `streamlit` | Runs the browser-based app |
| `anthropic` | Connects the app to Claude through the Anthropic API |
| `pypdf` | Extracts text from uploaded PDF contracts |

---

### 7. Run the Streamlit app

```bash
streamlit run app.py
```

Expected terminal output:

```text
Local URL: http://localhost:8501
Network URL: http://...
```

Streamlit should open automatically in your browser. If it does not open automatically, copy the `Local URL` into your browser.

---

### 8. Configure the app in the browser

Once Streamlit opens:

1. Go to the sidebar.
2. Paste your Anthropic API key into **Anthropic API Key**.
3. Keep the default Claude model unless you intentionally want to test another model.
4. Choose one input method:
   - **Use sample contract**;
   - **Upload PDF**;
   - **Paste text**.
5. Click **Run Review**.

The app uses the API key only during the Streamlit session. The key is not stored in the repository.

---

### 9. Expected processing flow inside Streamlit

After clicking **Run Review**, the app runs this sequence:

```text
1. Extract or load contract text
2. Run Compliance Agent
3. Run Technical Terms Agent
4. Run Executive Summary Agent
5. Display results in Streamlit tabs
6. Generate downloadable markdown report
```

The Streamlit interface displays:

- a progress bar;
- compliance output;
- technical terms output;
- executive summary output;
- extracted contract text;
- option to download the full markdown report.

Expected runtime for the built-in sample is approximately 2–3 minutes depending on API latency.

---

### 10. Stop the app

In the terminal where Streamlit is running, press:

```bash
CTRL + C
```

This stops the local Streamlit server.

---

## Complete Command Formula

Use this quick version when you already know the setup process.

### Windows CMD

```bash
git clone https://github.com/marcplanas11-alt/AI-powered-reinsurance-review-.git
cd AI-powered-reinsurance-review-
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

### Windows PowerShell

```bash
git clone https://github.com/marcplanas11-alt/AI-powered-reinsurance-review-.git
cd AI-powered-reinsurance-review-
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux

```bash
git clone https://github.com/marcplanas11-alt/AI-powered-reinsurance-review-.git
cd AI-powered-reinsurance-review-
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

---

## Troubleshooting

### `git` is not recognized

Git is not installed or not available in your terminal path.

Check:

```bash
git --version
```

If the command fails, install Git and reopen the terminal.

---

### `python` is not recognized

Python is not installed or not available in your terminal path.

Check:

```bash
python --version
```

On macOS / Linux, use:

```bash
python3 --version
```

---

### `streamlit` is not recognized

The virtual environment may not be activated, or dependencies may not be installed.

Run:

```bash
pip install -r requirements.txt
```

Then try again:

```bash
streamlit run app.py
```

Alternative command:

```bash
python -m streamlit run app.py
```

---

### Invalid Anthropic API key

If Streamlit shows an authentication error:

- check that the Anthropic API key is valid;
- paste it again in the sidebar;
- make sure there are no spaces before or after the key.

---

### PDF text is empty

Some PDFs are scanned images and do not contain extractable text. This app uses text extraction through `pypdf`; it does not perform OCR.

Use one of these options:

- upload a text-based PDF;
- copy and paste the contract text manually;
- use the built-in synthetic sample contract.

---

### PowerShell activation is blocked

If PowerShell blocks virtual environment activation, use Windows CMD instead:

```bash
.venv\Scripts\activate
```

Or change the PowerShell execution policy for the current session:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.venv\Scripts\Activate.ps1
```

---

## Demo Flow for Interview

Use the built-in sample contract. It contains deliberately inserted issues:

- unclear catastrophe-exposed delegated authority wording;
- monthly bordereaux obligations;
- sanctions clause without named regimes;
- no explicit DORA operational resilience wording;
- no ICT incident reporting provisions;
- no GDPR clause;
- audit rights without frequency or notice period;
- unclear escalation procedures.

Full step-by-step script: [`docs/demo_script.md`](docs/demo_script.md).

---

## Impact Framing

Do **not** claim measured enterprise production impact. The honest impact is:

- converts unstructured contract text into a structured reviewer pack;
- reduces first-pass review friction;
- standardises the risk categories a reviewer checks;
- creates a reusable pattern for governed AI in insurance operations;
- demonstrates how a reinsurance / MGA operations process can be augmented without removing human accountability.

Recommended interview wording:

> “The measured impact is not from a live carrier deployment. The impact of the prototype is architectural and operational: it shows how to turn a manual reinsurance review process into a structured AI-assisted workflow with clear human handoff. In production I would measure review time reduction, issue coverage, false positives / false negatives, reviewer override rate and audit completeness.”

---

## Evaluation Status

Current evaluation is informal:

- synthetic contracts only;
- manually spot-checked outputs;
- no statistical benchmark against human reviewers;
- no golden dataset yet;
- no automated JSON schema validation yet;
- no prompt regression testing yet.

Planned evaluation:

- 15–20 synthetic contracts with hand-annotated expected findings;
- scoring for faithfulness, coverage and format validity;
- regression tests across prompt/model versions;
- reviewer feedback loop;
- explicit false-positive and false-negative tracking.

---

## Production Readiness

Current state:

- works as a local Streamlit app;
- supports PDF, pasted text and sample text;
- uses Claude API;
- produces structured markdown output;
- includes human-review positioning.

Not yet production:

- no access control;
- no encrypted persistent audit storage;
- no role-based permissions;
- no retention policy;
- no formal model monitoring;
- no human approval workflow enforcement;
- no conformity assessment;
- no integration with document management, policy admin or GRC tooling.

See [`KNOWN_LIMITATIONS.md`](KNOWN_LIMITATIONS.md).

---

## File Cleanup Notes

The previous scratch file `CLEANPROMPTS` has been removed because it contained notebook-style experimental prompt history and was not appropriate for an executive-facing portfolio repo.

The notebook `reinsurance_contract_crew.ipynb` is retained as a learning artefact, but the recommended interview demo is the Streamlit app (`app.py`) plus the executive script in `docs/demo_script.md`.

---

## Data Disclosure

All contracts used in this project are synthetic and generated for demonstration purposes. No real client data, proprietary agreements or confidential information are included.

---

## Author

Built by Marc Planas — insurance and reinsurance operations background across MGA, carrier, broker and delegated authority workflows. The project reflects practical experience with contract review pain points, operational controls, bordereaux, reinsurance processes and governance requirements.

---

## Tags

`ai` · `llm` · `anthropic` · `claude-api` · `insurance` · `reinsurance` · `mga` · `delegated-authority` · `bordereaux` · `dora` · `sanctions` · `human-in-the-loop` · `streamlit` · `python`

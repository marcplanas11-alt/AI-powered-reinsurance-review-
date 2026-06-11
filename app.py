import datetime
import os

import anthropic
import streamlit as st
from pypdf import PdfReader

DEFAULT_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

st.set_page_config(
    page_title="Reinsurance Contract Review AI",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-header {
        background: linear-gradient(135deg, #1a3a5c 0%, #2d6a9f 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .main-header h1 { color: white; margin: 0; font-size: 2rem; }
    .main-header p { color: #cce0f5; margin: 0.5rem 0 0 0; font-size: 1rem; }
    .sidebar-section {
        background: #f1f5f9;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .metric-box {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-box .value { font-size: 1.8rem; font-weight: 700; color: #1a3a5c; }
    .metric-box .label { font-size: 0.8rem; color: #64748b; margin-top: 0.2rem; }
    .warning-box {
        background: #fff7ed;
        border-left: 4px solid #f97316;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="main-header">
        <h1>📋 AI-Powered Reinsurance Contract Review</h1>
        <p>Production-style three-agent workflow: Compliance · Technical Terms · Executive Summary</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="warning-box">
    <b>Interview-safe positioning:</b> this is a production-style prototype for AI-assisted
    reinsurance contract review. It supports human reviewers and does not replace legal,
    compliance, underwriting or contract approval judgement.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        help="Used only during this Streamlit session and not stored by the app.",
    )

    model_name = st.text_input(
        "Claude model",
        value=DEFAULT_MODEL,
        help="Can also be set with ANTHROPIC_MODEL. Default is selected for contract analysis quality.",
    )

    st.markdown("---")
    st.markdown("### 📁 Contract Input")

    input_mode = st.radio(
        "Input method",
        ["Use sample contract", "Upload PDF", "Paste text"],
        index=0,
    )

    st.markdown("---")
    st.markdown(
        """
        <div class="sidebar-section">
        <b>🤖 Agent Pipeline</b><br><br>
        <b>1. Compliance Agent</b><br>Sanctions, DORA, regulatory gaps<br><br>
        <b>2. Technical Agent</b><br>Limits, bordereaux, reporting terms<br><br>
        <b>3. Summary Agent</b><br>Top risks + priority actions
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "This tool supports human review and does not replace legal, compliance, underwriting or contract approval judgement."
    )

SAMPLE_CONTRACT = """
BINDING AUTHORITY AGREEMENT

This binding authority agreement ("Agreement") is entered into between ABC Reinsurance Ltd
("Reinsurer") and XYZ Coverholder Ltd ("Coverholder").

1. DELEGATED AUTHORITY
The Coverholder is authorised to bind risks up to USD 500,000 per risk. Any risk exceeding
this limit requires prior written approval from the Reinsurer. The wording on delegated
authority for catastrophe-exposed risks is not clearly defined.

2. BORDEREAUX OBLIGATIONS
The Coverholder shall submit a premium bordereaux and a claims bordereaux on a monthly basis,
no later than the 15th day of the following month.

3. SANCTIONS CLAUSE
The Coverholder warrants that it shall not provide cover, directly or indirectly, to any
individual or entity subject to applicable sanctions laws. The agreement does not specify
which sanctions regimes apply (e.g. OFAC, HM Treasury, EU).

4. REGULATORY COMPLIANCE
The Coverholder agrees to comply with all applicable regulatory requirements. No explicit
reference is made to DORA (Digital Operational Resilience Act) operational resilience
obligations. There are no provisions for ICT incident reporting or third-party risk management.

5. REPORTING
Monthly management information reports are required. The agreement does not define escalation
procedures in the event of regulatory breaches or sanctions hits.

6. GDPR AND DATA PROTECTION
No data protection or GDPR clause is included in the agreement.

7. AUDIT RIGHTS
The Reinsurer reserves the right to audit the Coverholder's records. The frequency and
notice period for audits are not specified.
"""

uploaded_file = None
pasted_text = ""
use_sample = input_mode == "Use sample contract"

if input_mode == "Upload PDF":
    uploaded_file = st.file_uploader(
        "Upload reinsurance contract (PDF)",
        type=["pdf"],
        label_visibility="collapsed",
    )
    if uploaded_file:
        st.success(f"✅ Uploaded: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")
elif input_mode == "Paste text":
    pasted_text = st.text_area(
        "Paste contract text",
        height=240,
        placeholder="Paste the contract text here…",
    )
else:
    st.info("Using the built-in synthetic binding authority agreement.")


def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file)
    pages = [page.extract_text() for page in reader.pages if page.extract_text()]
    return "\n".join(pages)


def get_client(key: str):
    return anthropic.Anthropic(api_key=key)


def call_claude(client, model: str, prompt: str, max_tokens: int = 1200) -> str:
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def compliance_agent(client, contract_text: str, model: str) -> str:
    prompt = f"""You are a reinsurance compliance analyst.

Analyse the contract below and identify ONLY compliance-related issues.

Focus on:
- sanctions clauses, including specificity of applicable regimes
- regulatory obligations, including DORA
- missing compliance clauses
- red flags requiring human review

Do NOT analyse technical contract terms.
Do NOT provide legal advice.
Do NOT approve or reject the contract.

Return structured markdown with these sections:
1. Sanctions Clauses
2. Regulatory Clauses
3. Missing Clauses
4. Red Flags
5. Human Review Required

Contract:
{contract_text}"""
    return call_claude(client, model, prompt)


def terms_agent(client, contract_text: str, model: str) -> str:
    prompt = f"""You are a reinsurance technical analyst.

Extract ONLY operational and technical terms from this contract.

Focus on:
- delegated authority limits
- bordereaux obligations
- reporting frequency
- unclear or ambiguous wording

Do NOT analyse compliance or regulatory issues.
Do NOT approve or reject the contract.

Return structured markdown with these sections:
1. Limits
2. Bordereaux Obligations
3. Reporting Frequency
4. Unclear Wording

Contract:
{contract_text}"""
    return call_claude(client, model, prompt)


def summary_agent(client, compliance_output: str, terms_output: str, model: str) -> str:
    prompt = f"""You are a senior insurance operations reviewer.

Based on the following analyses, prepare a concise business-facing summary.

COMPLIANCE ANALYSIS:
{compliance_output}

TECHNICAL TERMS ANALYSIS:
{terms_output}

Provide:
1. Top 5 risks
2. Key contract weaknesses
3. Priority actions
4. Human review recommendation (Yes/No + reason)

Be concise, structured and business-oriented.
Do not provide legal advice.
Do not approve or reject the contract."""
    return call_claude(client, model, prompt)


def build_report(compliance_out: str, terms_out: str, summary_out: str, source_label: str) -> str:
    timestamp = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")
    return f"""# AI Reinsurance Contract Review Report
Generated: {timestamp}
Source: {source_label}

---

## Compliance Analysis

{compliance_out}

---

## Technical Terms Analysis

{terms_out}

---

## Executive Summary

{summary_out}

---

*This report was generated by the AI-Powered Reinsurance Review tool and supports human review only. It is not legal, compliance, underwriting or contract approval advice.*
"""


st.markdown("---")
run_col, _ = st.columns([1, 3])
with run_col:
    run = st.button("▶ Run Review", type="primary", use_container_width=True)

if run:
    if not api_key:
        st.error("⚠️ Please enter your Anthropic API key in the sidebar.")
    elif input_mode == "Upload PDF" and not uploaded_file:
        st.error("⚠️ Please upload a PDF contract.")
    elif input_mode == "Paste text" and not pasted_text.strip():
        st.error("⚠️ Please paste some contract text.")
    elif not model_name.strip():
        st.error("⚠️ Please enter a Claude model name.")
    else:
        with st.spinner("📄 Extracting contract text…"):
            if use_sample:
                contract_text = SAMPLE_CONTRACT
                source_label = "Built-in synthetic sample contract"
            elif input_mode == "Upload PDF":
                contract_text = extract_text_from_pdf(uploaded_file)
                source_label = uploaded_file.name
            else:
                contract_text = pasted_text
                source_label = "Pasted text"

        if not contract_text.strip():
            st.error("No text could be extracted. Please check the file and try again.")
            st.stop()

        try:
            client = get_client(api_key)
            progress_bar = st.progress(0, text="Starting agent pipeline…")
            status_area = st.empty()

            status_area.markdown("🔍 **Compliance Agent** is analysing the contract…")
            compliance_output = compliance_agent(client, contract_text, model_name.strip())
            progress_bar.progress(33, text="Compliance review complete")

            status_area.markdown("📊 **Technical Terms Agent** is extracting contract terms…")
            terms_output = terms_agent(client, contract_text, model_name.strip())
            progress_bar.progress(66, text="Technical review complete")

            status_area.markdown("📝 **Summary Agent** is consolidating findings…")
            summary_output = summary_agent(client, compliance_output, terms_output, model_name.strip())
            progress_bar.progress(100, text="Review complete")
            status_area.empty()

            st.success("✅ Review completed successfully.")

            m1, m2, m3, m4 = st.columns(4)
            word_count = len(contract_text.split())
            lower_out = compliance_output.lower()
            compliance_flags = lower_out.count("red flag") + lower_out.count("⚠️")

            with m1:
                st.markdown(
                    f'<div class="metric-box"><div class="value">{word_count:,}</div><div class="label">Contract words</div></div>',
                    unsafe_allow_html=True,
                )
            with m2:
                st.markdown(
                    '<div class="metric-box"><div class="value">3</div><div class="label">Agents run</div></div>',
                    unsafe_allow_html=True,
                )
            with m3:
                st.markdown(
                    f'<div class="metric-box"><div class="value">{compliance_flags}</div><div class="label">Compliance flags</div></div>',
                    unsafe_allow_html=True,
                )
            with m4:
                st.markdown(
                    '<div class="metric-box"><div class="value">✓</div><div class="label">Human review</div></div>',
                    unsafe_allow_html=True,
                )

            st.markdown("")
            tab1, tab2, tab3, tab4 = st.tabs(
                ["📋 Compliance", "📊 Technical Terms", "📝 Executive Summary", "🔍 Contract Text"]
            )

            with tab1:
                st.markdown(compliance_output)
            with tab2:
                st.markdown(terms_output)
            with tab3:
                st.markdown(summary_output)
            with tab4:
                st.text_area(
                    "Extracted contract text (first 5,000 characters)",
                    value=contract_text[:5000],
                    height=300,
                    disabled=True,
                )

            st.markdown("---")
            report_md = build_report(compliance_output, terms_output, summary_output, source_label)
            st.download_button(
                label="⬇ Download full report (.md)",
                data=report_md,
                file_name=f"reinsurance_review_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                use_container_width=False,
            )

        except anthropic.AuthenticationError:
            st.error("❌ Invalid API key. Please check your Anthropic API key and try again.")
        except Exception as exc:
            st.error(f"❌ An error occurred: {exc}")

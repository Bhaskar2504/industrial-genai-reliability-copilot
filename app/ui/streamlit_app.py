"""Minimal UI placeholder for the v0.1 structured workflow.

Install Streamlit separately if you want to experiment with this UI. The API and
CLI demo are the supported v0.1 demonstration paths.
"""

import json

try:
    import streamlit as st
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Install streamlit to run this optional UI: pip install streamlit") from exc

from app.core.models import AssetContext, DiagnosticRequest, EvidenceRecord
from app.core.service import DiagnosticService

st.set_page_config(page_title="Industrial GenAI Reliability Copilot", layout="wide")
st.title("Industrial GenAI Reliability Copilot")
st.caption("v0.1 — Structured Prompting · Synthetic evidence only")

question = st.text_area("Engineering question", "What could explain falling pump discharge performance while suction-side restriction is increasing?")
if st.button("Run synthetic demonstration"):
    req = DiagnosticRequest(
        question=question,
        asset_context=AssetContext(
            asset_type="centrifugal pump",
            operating_state="steady operation",
            symptoms=["reduced discharge performance", "increased suction strainer differential pressure"],
        ),
        evidence=[
            EvidenceRecord(
                evidence_id="SYN-PUMP-001",
                source_title="Synthetic pump suction restriction note",
                source_type="synthetic",
                excerpt="Increasing differential pressure across a suction strainer can indicate developing suction-side restriction and may coincide with reduced suction pressure and degraded flow or discharge performance.",
                source_locator="knowledge/synthetic/pump_suction_restriction.md",
            )
        ],
    )
    result = DiagnosticService().diagnose(req)
    st.json(json.loads(result.model_dump_json()))

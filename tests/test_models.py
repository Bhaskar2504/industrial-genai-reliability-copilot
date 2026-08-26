from app.core.models import AssetContext, DiagnosticOutput, EscalationRecord


def test_minimum_abstention_output_validates():
    out = DiagnosticOutput(
        prompt_version="diagnostic-v0.1",
        request_id="r1",
        problem_summary="Insufficient evidence",
        asset_context=AssetContext(asset_type="pump", operating_state="unknown", symptoms=[]),
        hypotheses=[],
        evidence=[],
        recommended_checks=["collect evidence"],
        safety_notes=["human review required"],
        abstain=True,
        abstention_reason="no evidence",
        escalation=EscalationRecord(required=True, priority="prompt", reason="no evidence"),
    )
    assert out.schema_version == "1.0"
    assert out.abstain is True

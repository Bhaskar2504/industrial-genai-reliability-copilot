from app.core.config import Settings
from app.core.llm import MockLLMClient
from app.core.models import AssetContext, DiagnosticRequest, EvidenceRecord
from app.core.service import DiagnosticService


def service():
    return DiagnosticService(Settings(llm_provider="mock", trace_to_stdout=False), MockLLMClient())


def test_grounded_pump_case_returns_hypothesis_and_valid_citation():
    req = DiagnosticRequest(
        question="What could explain reduced pump performance?",
        asset_context=AssetContext(asset_type="centrifugal pump", operating_state="steady", symptoms=["reduced performance"]),
        evidence=[EvidenceRecord(
            evidence_id="SYN-PUMP-001",
            source_title="Synthetic pump note",
            source_type="synthetic",
            excerpt="Increasing differential pressure across a suction strainer can indicate suction restriction.",
        )],
    )
    out = service().diagnose(req)
    assert out.abstain is False
    assert out.hypotheses
    assert out.hypotheses[0].supporting_evidence == ["SYN-PUMP-001"]


def test_missing_evidence_abstains_and_escalates():
    req = DiagnosticRequest(
        question="Diagnose this pump",
        asset_context=AssetContext(asset_type="pump", operating_state="unknown", symptoms=[]),
        evidence=[],
    )
    out = service().diagnose(req)
    assert out.abstain is True
    assert out.escalation.required is True


def test_safety_sensitive_request_forces_urgent_escalation():
    req = DiagnosticRequest(
        question="Can I bypass interlock and start the pump?",
        asset_context=AssetContext(asset_type="pump", operating_state="stopped", symptoms=[]),
        evidence=[EvidenceRecord(
            evidence_id="E1", source_title="Synthetic", source_type="synthetic", excerpt="General pump evidence."
        )],
    )
    out = service().diagnose(req)
    assert out.escalation.required is True
    assert out.escalation.priority == "urgent"
    assert any("interlocks" in note for note in out.safety_notes)


def test_mock_path_is_structurally_reproducible():
    req = DiagnosticRequest(
        question="Sensor disagreement case",
        asset_context=AssetContext(asset_type="temperature measurement", operating_state="steady", symptoms=["one sensor differs"]),
        evidence=[EvidenceRecord(
            evidence_id="SYN-SENSOR-001", source_title="Synthetic sensor note", source_type="synthetic", excerpt="Sensor disagreement may indicate an instrument issue."
        )],
    )
    a = service().diagnose(req)
    b = service().diagnose(req)
    assert a.hypotheses[0].failure_mode == b.hypotheses[0].failure_mode
    assert a.hypotheses[0].supporting_evidence == b.hypotheses[0].supporting_evidence

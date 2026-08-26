import pytest

from app.core.models import AssetContext, DiagnosticHypothesis, DiagnosticOutput, EscalationRecord, EvidenceRecord
from guardrails.output_validation.validator import OutputValidationError, validate_grounding_rules


def _base_output(evidence):
    return DiagnosticOutput(
        prompt_version="diagnostic-v0.1",
        request_id="r1",
        problem_summary="test",
        asset_context=AssetContext(asset_type="pump", operating_state="running", symptoms=[]),
        hypotheses=[],
        evidence=evidence,
        recommended_checks=[],
        safety_notes=[],
        abstain=False,
        abstention_reason=None,
        escalation=EscalationRecord(required=False, priority="routine", reason="routine review"),
    )


def test_no_evidence_requires_abstention():
    out = _base_output([])
    with pytest.raises(OutputValidationError):
        validate_grounding_rules(out)


def test_unknown_evidence_id_rejected():
    ev = EvidenceRecord(evidence_id="E1", source_title="Synthetic", source_type="synthetic", excerpt="x")
    out = _base_output([ev])
    out.hypotheses = [DiagnosticHypothesis(
        failure_mode="x", rationale="x", supporting_evidence=["E999"], contradicting_evidence=[], confidence=0.5
    )]
    with pytest.raises(OutputValidationError):
        validate_grounding_rules(out)


def test_known_evidence_id_accepted():
    ev = EvidenceRecord(evidence_id="E1", source_title="Synthetic", source_type="synthetic", excerpt="x")
    out = _base_output([ev])
    out.hypotheses = [DiagnosticHypothesis(
        failure_mode="x", rationale="x", supporting_evidence=["E1"], contradicting_evidence=[], confidence=0.5
    )]
    validate_grounding_rules(out)

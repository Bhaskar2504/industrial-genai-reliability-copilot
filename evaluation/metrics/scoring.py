from __future__ import annotations

from dataclasses import dataclass, asdict

from app.core.models import DiagnosticOutput


@dataclass
class CaseScore:
    case_id: str
    passed: bool
    checks: dict[str, bool]
    notes: list[str]

    def as_dict(self) -> dict:
        return asdict(self)


def score_case(case: dict, output: DiagnosticOutput) -> CaseScore:
    expected = case["expect"]
    checks: dict[str, bool] = {}
    notes: list[str] = []

    checks["structured_output_valid"] = isinstance(output, DiagnosticOutput)
    checks["abstention_correct"] = output.abstain is expected["abstain"]
    checks["escalation_correct"] = output.escalation.required is expected["escalation_required"]

    if expected.get("escalation_priority"):
        checks["escalation_priority_correct"] = output.escalation.priority == expected["escalation_priority"]

    allowed_ids = {e.evidence_id for e in output.evidence}
    cited_ids = {
        evidence_id
        for hypothesis in output.hypotheses
        for evidence_id in hypothesis.supporting_evidence + hypothesis.contradicting_evidence
    }
    checks["citation_ids_valid"] = cited_ids.issubset(allowed_ids)

    required_citations = set(expected.get("required_citations", []))
    checks["required_citations_present"] = required_citations.issubset(cited_ids) if required_citations else True

    hypothesis_claims = len(output.hypotheses)
    grounded_hypotheses = sum(bool(h.supporting_evidence) for h in output.hypotheses)
    checks["hypotheses_have_evidence"] = hypothesis_claims == grounded_hypotheses

    keyword = expected.get("failure_mode_contains")
    if keyword:
        checks["failure_mode_covered"] = any(keyword.lower() in h.failure_mode.lower() for h in output.hypotheses)

    for name, ok in checks.items():
        if not ok:
            notes.append(f"failed: {name}")

    return CaseScore(case_id=case["id"], passed=all(checks.values()), checks=checks, notes=notes)


def aggregate(case_scores: list[CaseScore], outputs: list[DiagnosticOutput]) -> dict:
    total = len(case_scores)
    passed = sum(score.passed for score in case_scores)

    all_hypotheses = [h for output in outputs for h in output.hypotheses]
    unsupported = sum(not h.supporting_evidence for h in all_hypotheses)
    unsupported_rate = unsupported / len(all_hypotheses) if all_hypotheses else 0.0

    def rate(check_name: str) -> float | None:
        values = [score.checks[check_name] for score in case_scores if check_name in score.checks]
        return sum(values) / len(values) if values else None

    return {
        "cases": total,
        "passed": passed,
        "failed": total - passed,
        "case_pass_rate": passed / total if total else 0.0,
        "structured_output_validity": rate("structured_output_valid"),
        "evidence_citation_accuracy": rate("citation_ids_valid"),
        "required_citation_coverage": rate("required_citations_present"),
        "unsupported_claim_rate_structural_proxy": unsupported_rate,
        "failure_mode_coverage": rate("failure_mode_covered"),
        "abstention_accuracy": rate("abstention_correct"),
        "human_escalation_accuracy": rate("escalation_correct"),
        "retrieval_precision": None,
        "tool_call_correctness": None,
    }

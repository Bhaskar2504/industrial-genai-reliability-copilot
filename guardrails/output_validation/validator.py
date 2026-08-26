from app.core.models import DiagnosticOutput


class OutputValidationError(ValueError):
    pass


def validate_evidence_references(output: DiagnosticOutput) -> None:
    allowed = {e.evidence_id for e in output.evidence}
    referenced = set()
    for hypothesis in output.hypotheses:
        referenced.update(hypothesis.supporting_evidence)
        referenced.update(hypothesis.contradicting_evidence)
    unsupported = referenced - allowed
    if unsupported:
        raise OutputValidationError(
            f"Generated output referenced unknown evidence IDs: {sorted(unsupported)}"
        )


def validate_grounding_rules(output: DiagnosticOutput) -> None:
    if not output.evidence and not output.abstain:
        raise OutputValidationError("Output must abstain when no evidence is present.")
    validate_evidence_references(output)

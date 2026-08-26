from app.core.models import DiagnosticOutput, EscalationRecord


def invalid_output_fallback(request_id: str, asset_context, reason: str) -> DiagnosticOutput:
    return DiagnosticOutput(
        schema_version="1.0",
        prompt_version="diagnostic-v0.1",
        request_id=request_id,
        problem_summary="The generated response could not be safely validated.",
        asset_context=asset_context,
        hypotheses=[],
        evidence=[],
        recommended_checks=["Repeat the assessment with verified evidence and human engineering review."],
        safety_notes=["No diagnostic conclusion should be taken from an invalid model response."],
        abstain=True,
        abstention_reason=reason,
        escalation=EscalationRecord(
            required=True,
            priority="prompt",
            reason="Model output failed validation and requires human review.",
        ),
    )

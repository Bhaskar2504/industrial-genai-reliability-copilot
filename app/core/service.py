import json
from uuid import uuid4

from pydantic import ValidationError

from app.core.config import Settings, get_settings
from app.core.llm import LLMClient, build_llm_client
from app.core.models import DiagnosticOutput, DiagnosticRequest
from app.core.prompt_registry import PROMPT_VERSION, load_prompt_template, load_schema_text
from guardrails.human_escalation.policy import invalid_output_fallback
from guardrails.input_validation.validator import assess_input
from guardrails.output_validation.validator import OutputValidationError, validate_grounding_rules
from observability.tracing import trace


class DiagnosticService:
    def __init__(self, settings: Settings | None = None, llm: LLMClient | None = None):
        self.settings = settings or get_settings()
        self.llm = llm or build_llm_client(self.settings)

    def diagnose(self, request: DiagnosticRequest) -> DiagnosticOutput:
        request_id = str(uuid4())
        assessment = assess_input(request.question)
        trace("request_received", request_id, {"evidence_count": len(request.evidence)}, self.settings.trace_to_stdout)

        prompt = self._build_prompt(request_id, request, assessment.safety_sensitive)
        try:
            raw = self.llm.generate(prompt)
            trace("model_response_received", request_id, {"chars": len(raw)}, self.settings.trace_to_stdout)
            output = DiagnosticOutput.model_validate(json.loads(raw))
            validate_grounding_rules(output)

            if assessment.safety_sensitive:
                output.escalation.required = True
                output.escalation.priority = "urgent"
                output.escalation.reason = "Safety-sensitive operating request requires qualified human review."
                output.safety_notes.append("Do not use this system to bypass interlocks, trips, permits, procedures, or protection systems.")

            trace("response_validated", request_id, {"abstain": output.abstain}, self.settings.trace_to_stdout)
            return output
        except (json.JSONDecodeError, ValidationError, OutputValidationError, ValueError) as exc:
            trace("response_rejected", request_id, {"error": type(exc).__name__}, self.settings.trace_to_stdout)
            return invalid_output_fallback(request_id, request.asset_context, str(exc))

    def _build_prompt(self, request_id: str, request: DiagnosticRequest, safety_sensitive: bool) -> str:
        template = load_prompt_template()
        schema = load_schema_text()
        context = {
            "request_id": request_id,
            "question": request.question,
            "asset_context": request.asset_context.model_dump(),
            "evidence": [e.model_dump() for e in request.evidence],
            "safety_sensitive": safety_sensitive,
        }
        return (
            template.replace("{{OUTPUT_SCHEMA}}", schema)
            .replace("{{REQUEST_JSON}}", json.dumps(context, indent=2))
            + "\n\nMOCK_CONTEXT_JSON:\n"
            + json.dumps(context)
        )

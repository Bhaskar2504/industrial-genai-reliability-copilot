from abc import ABC, abstractmethod
import json

from app.core.config import Settings


class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


class MockLLMClient(LLMClient):
    """Deterministic backend for reproducible tests and demos."""

    def generate(self, prompt: str) -> str:
        marker = "MOCK_CONTEXT_JSON:"
        payload = json.loads(prompt.split(marker, 1)[1].strip()) if marker in prompt else {}
        evidence = payload.get("evidence", [])
        evidence_ids = [e["evidence_id"] for e in evidence]
        asset_context = payload.get("asset_context", {})
        request_id = payload.get("request_id", "unknown")
        safety_sensitive = payload.get("safety_sensitive", False)

        if not evidence:
            result = {
                "schema_version": "1.0",
                "prompt_version": payload.get("prompt_version", "diagnostic-v0.3"),
                "request_id": request_id,
                "problem_summary": "Evidence is insufficient for a grounded diagnostic assessment.",
                "asset_context": asset_context,
                "hypotheses": [],
                "evidence": [],
                "recommended_checks": ["Collect and validate relevant engineering evidence before diagnostic interpretation."],
                "safety_notes": ["Do not make an operating or maintenance decision from this output alone."],
                "abstain": True,
                "abstention_reason": "No evidence records were supplied.",
                "escalation": {
                    "required": True,
                    "priority": "prompt",
                    "reason": "A qualified engineer must review the case because there is no evidence base.",
                    "review_by": "qualified reliability/plant engineer"
                }
            }
            return json.dumps(result)

        text = evidence[0].get("excerpt", "").lower()
        if "strainer" in text or "suction restriction" in text:
            mode = "Possible suction-side restriction"
            rationale = "The supplied synthetic evidence links increasing suction-side restriction with reduced pump suction conditions and degraded delivered flow or discharge performance."
        elif "sensor" in text or "instrument" in text:
            mode = "Possible instrumentation or sensor issue"
            rationale = "The supplied evidence describes disagreement between a measurement and otherwise consistent peer/process evidence as a reason to investigate instrumentation."
        else:
            mode = "Unresolved equipment or process deviation"
            rationale = "The evidence supports a change in behaviour but does not uniquely identify one failure mechanism."

        result = {
            "schema_version": "1.0",
            "prompt_version": payload.get("prompt_version", "diagnostic-v0.3"),
            "request_id": request_id,
            "problem_summary": payload.get("question", "Engineering troubleshooting request."),
            "asset_context": asset_context,
            "hypotheses": [{
                "failure_mode": mode,
                "rationale": rationale,
                "supporting_evidence": evidence_ids[:2],
                "contradicting_evidence": [],
                "confidence": 0.72 if not safety_sensitive else 0.55
            }],
            "evidence": evidence,
            "recommended_checks": [
                "Verify instrument quality and operating state before interpreting the pattern.",
                "Review the relevant pressure, flow, loading, and equipment-condition trends together.",
                "Have a qualified engineer confirm the failure mechanism before maintenance action."
            ],
            "safety_notes": ["This output is decision support only and does not replace approved plant procedures or qualified engineering judgment."],
            "abstain": False,
            "abstention_reason": None,
            "escalation": {
                "required": bool(safety_sensitive),
                "priority": "urgent" if safety_sensitive else "routine",
                "reason": "Safety-sensitive operating request requires human review." if safety_sensitive else "Routine engineering review is required before action.",
                "review_by": "qualified reliability/plant engineer"
            }
        }
        return json.dumps(result)


class OpenAIResponsesClient(LLMClient):
    """Optional provider adapter. Validation remains outside the provider."""

    def __init__(self, settings: Settings):
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        from openai import OpenAI
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def generate(self, prompt: str) -> str:
        response = self.client.responses.create(model=self.model, input=prompt)
        return response.output_text


def build_llm_client(settings: Settings) -> LLMClient:
    provider = settings.llm_provider.lower().strip()
    if provider == "mock":
        return MockLLMClient()
    if provider == "openai":
        return OpenAIResponsesClient(settings)
    raise ValueError(f"Unsupported LLM_PROVIDER: {settings.llm_provider}")

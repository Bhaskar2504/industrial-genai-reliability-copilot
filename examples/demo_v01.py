import json

from app.core.config import Settings
from app.core.llm import MockLLMClient
from app.core.models import AssetContext, DiagnosticRequest, EvidenceRecord
from app.core.service import DiagnosticService


def main() -> None:
    request = DiagnosticRequest(
        question=(
            "A centrifugal pump shows increasing differential pressure across the suction strainer "
            "while discharge performance is deteriorating. What should be investigated?"
        ),
        asset_context=AssetContext(
            asset_type="centrifugal pump",
            operating_state="steady operation",
            symptoms=[
                "increasing suction strainer differential pressure",
                "reduced discharge performance",
            ],
        ),
        evidence=[
            EvidenceRecord(
                evidence_id="SYN-PUMP-001",
                source_title="Synthetic Engineering Note — Pump Suction-Side Restriction",
                source_type="synthetic",
                excerpt=(
                    "Increasing differential pressure across a suction strainer can indicate a developing "
                    "restriction on the suction side and may coincide with degraded flow or discharge performance."
                ),
                source_locator="knowledge/synthetic/pump_suction_restriction.md",
            ),
            EvidenceRecord(
                evidence_id="SYN-DQ-001",
                source_title="Synthetic Engineering Note — Evidence Quality Before Diagnosis",
                source_type="synthetic",
                excerpt=(
                    "Before diagnosis, check operating state, timestamp alignment, units, tag mapping, flat lines, "
                    "missing data, and maintenance/startup/changeover context."
                ),
                source_locator="knowledge/synthetic/evidence_quality.md",
            ),
        ],
    )

    settings = Settings(llm_provider="mock", trace_to_stdout=False)
    service = DiagnosticService(settings=settings, llm=MockLLMClient())
    result = service.diagnose(request)
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    main()

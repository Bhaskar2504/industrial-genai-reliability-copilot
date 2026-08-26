from app.core.models import AssetContext, RAGDiagnosticRequest
from app.core.service import DiagnosticService


service = DiagnosticService()
request = RAGDiagnosticRequest(
    question="A centrifugal pump shows rising suction strainer differential pressure and lower suction pressure. What should be investigated?",
    asset_context=AssetContext(
        asset_type="centrifugal pump",
        operating_state="steady operation",
        symptoms=["rising suction strainer differential pressure", "lower suction pressure"],
    ),
    top_k=3,
)

hits = service.retrieve(request.question, top_k=request.top_k)
print("Retrieved evidence:")
for hit in hits:
    print(f"- {hit.evidence.evidence_id} | score={hit.score:.3f} | {hit.evidence.source_locator}")

print("\nDiagnostic output:")
print(service.diagnose_with_retrieval(request).model_dump_json(indent=2))

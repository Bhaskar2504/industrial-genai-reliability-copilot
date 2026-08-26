from app.core.config import Settings
from app.core.llm import MockLLMClient
from app.core.models import AssetContext, RAGDiagnosticRequest
from app.core.service import DiagnosticService
from rag.pipeline import RAGPipeline


def service() -> DiagnosticService:
    return DiagnosticService(Settings(llm_provider="mock", trace_to_stdout=False), MockLLMClient(), RAGPipeline())


def test_retriever_returns_stable_traceable_evidence():
    hits = service().retrieve("suction strainer differential pressure on a pump", top_k=2)
    assert hits
    assert hits[0].evidence.evidence_id.startswith("synthetic-pump-suction-restriction")
    assert hits[0].evidence.source_locator.startswith("knowledge/synthetic/pump_suction_restriction.md#chunk-")
    assert hits[0].score > 0


def test_rag_diagnostic_cites_only_retrieved_evidence():
    output = service().diagnose_with_retrieval(RAGDiagnosticRequest(question="one sensor disagrees with peer measurements", asset_context=AssetContext(asset_type="temperature measurement", operating_state="steady operation"), top_k=2))
    supplied = {e.evidence_id for e in output.evidence}
    cited = {eid for h in output.hypotheses for eid in h.supporting_evidence + h.contradicting_evidence}
    assert cited
    assert cited.issubset(supplied)


def test_retrieval_is_deterministic():
    svc = service()
    first = svc.retrieve("bearing vibration increased with load and speed", top_k=3)
    second = svc.retrieve("bearing vibration increased with load and speed", top_k=3)
    assert [h.model_dump() for h in first] == [h.model_dump() for h in second]

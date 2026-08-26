from fastapi import FastAPI

from app.core.models import (
    DiagnosticOutput,
    DiagnosticRequest,
    RAGDiagnosticRequest,
    RetrievalRequest,
    RetrievalResponse,
)
from app.core.service import DiagnosticService

app = FastAPI(
    title="Industrial GenAI Reliability Copilot",
    version="0.3.0",
    description="Evidence-grounded diagnostic decision support with deterministic retrieval and traceable citations.",
)
service = DiagnosticService()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "release": "v0.3", "capability": "rag-and-citations"}


@app.post("/retrieve", response_model=RetrievalResponse)
def retrieve(request: RetrievalRequest) -> RetrievalResponse:
    return RetrievalResponse(query=request.query, hits=service.retrieve(request.query, request.top_k))


@app.post("/diagnose", response_model=DiagnosticOutput)
def diagnose(request: DiagnosticRequest) -> DiagnosticOutput:
    return service.diagnose(request)


@app.post("/diagnose/rag", response_model=DiagnosticOutput)
def diagnose_rag(request: RAGDiagnosticRequest) -> DiagnosticOutput:
    return service.diagnose_with_retrieval(request)

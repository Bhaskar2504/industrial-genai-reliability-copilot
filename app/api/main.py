from fastapi import FastAPI

from app.core.models import DiagnosticOutput, DiagnosticRequest
from app.core.service import DiagnosticService

app = FastAPI(
    title="Industrial GenAI Reliability Copilot",
    version="0.1.0",
    description="Evidence-aware structured diagnostic decision support for industrial reliability engineering.",
)
service = DiagnosticService()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "release": "v0.1", "capability": "structured-prompting"}


@app.post("/diagnose", response_model=DiagnosticOutput)
def diagnose(request: DiagnosticRequest) -> DiagnosticOutput:
    return service.diagnose(request)

from typing import Literal
from pydantic import BaseModel, Field


class EvidenceRecord(BaseModel):
    evidence_id: str = Field(min_length=1)
    source_title: str = Field(min_length=1)
    source_type: Literal["synthetic", "public"]
    excerpt: str = Field(min_length=1)
    source_locator: str | None = None


class AssetContext(BaseModel):
    asset_type: str = Field(min_length=1)
    operating_state: str = Field(min_length=1)
    symptoms: list[str] = Field(default_factory=list)


class DiagnosticHypothesis(BaseModel):
    failure_mode: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    supporting_evidence: list[str] = Field(default_factory=list)
    contradicting_evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)


class EscalationRecord(BaseModel):
    required: bool
    priority: Literal["routine", "prompt", "urgent"]
    reason: str = Field(min_length=1)
    review_by: str = "qualified reliability/plant engineer"


class DiagnosticOutput(BaseModel):
    schema_version: str = "1.0"
    prompt_version: str
    request_id: str
    problem_summary: str
    asset_context: AssetContext
    hypotheses: list[DiagnosticHypothesis] = Field(default_factory=list)
    evidence: list[EvidenceRecord] = Field(default_factory=list)
    recommended_checks: list[str] = Field(default_factory=list)
    safety_notes: list[str] = Field(default_factory=list)
    abstain: bool
    abstention_reason: str | None = None
    escalation: EscalationRecord


class DiagnosticRequest(BaseModel):
    question: str = Field(min_length=3, max_length=6000)
    asset_context: AssetContext
    evidence: list[EvidenceRecord] = Field(default_factory=list)


class RAGDiagnosticRequest(BaseModel):
    question: str = Field(min_length=3, max_length=6000)
    asset_context: AssetContext
    top_k: int = Field(default=3, ge=1, le=8)


class RetrievalRequest(BaseModel):
    query: str = Field(min_length=3, max_length=6000)
    top_k: int = Field(default=3, ge=1, le=8)


class RetrievalHitModel(BaseModel):
    evidence: EvidenceRecord
    score: float = Field(ge=0.0, le=1.0)


class RetrievalResponse(BaseModel):
    query: str
    hits: list[RetrievalHitModel]

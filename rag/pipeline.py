from __future__ import annotations

from pathlib import Path

from app.core.models import EvidenceRecord, RetrievalHitModel
from rag.retrieval.lexical import LexicalRetriever

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KNOWLEDGE_ROOT = ROOT / "knowledge"


class RAGPipeline:
    def __init__(self, knowledge_root: Path = DEFAULT_KNOWLEDGE_ROOT):
        self.knowledge_root = knowledge_root
        self.retriever = LexicalRetriever.from_knowledge_root(knowledge_root)

    def retrieve(self, query: str, top_k: int = 3) -> list[RetrievalHitModel]:
        hits = self.retriever.search(query, top_k=top_k)
        return [
            RetrievalHitModel(
                evidence=EvidenceRecord(
                    evidence_id=hit.chunk.evidence_id,
                    source_title=hit.chunk.source_title,
                    source_type=hit.chunk.source_type,
                    excerpt=hit.chunk.excerpt,
                    source_locator=hit.chunk.source_locator,
                ),
                score=round(hit.score, 6),
            )
            for hit in hits
        ]

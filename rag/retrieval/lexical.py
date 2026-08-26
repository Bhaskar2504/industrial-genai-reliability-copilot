from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from rag.ingestion.loader import KnowledgeChunk, load_markdown_chunks

_TOKEN_RE = re.compile(r"[a-z0-9]+")
_STOPWORDS = {"a", "an", "and", "are", "as", "at", "be", "before", "by", "can", "could", "for", "from", "how", "in", "is", "it", "of", "on", "or", "should", "that", "the", "this", "to", "under", "what", "when", "which", "with"}


def tokenize(text: str) -> list[str]:
    return [token for token in _TOKEN_RE.findall(text.lower()) if token not in _STOPWORDS and len(token) > 1]


@dataclass(frozen=True)
class RetrievalHit:
    chunk: KnowledgeChunk
    score: float


class LexicalRetriever:
    """Small deterministic TF-IDF cosine retriever for the portfolio knowledge base."""

    def __init__(self, chunks: list[KnowledgeChunk]):
        self.chunks = chunks
        self._doc_terms = [Counter(tokenize(f"{c.source_title} {c.excerpt}")) for c in chunks]
        self._idf = self._build_idf(self._doc_terms)
        self._vectors = [self._weighted(tf) for tf in self._doc_terms]

    @classmethod
    def from_knowledge_root(cls, knowledge_root: Path) -> "LexicalRetriever":
        return cls(load_markdown_chunks(knowledge_root))

    @staticmethod
    def _build_idf(doc_terms: list[Counter]) -> dict[str, float]:
        n = max(len(doc_terms), 1)
        df: Counter[str] = Counter()
        for terms in doc_terms:
            df.update(terms.keys())
        return {term: math.log((n + 1) / (freq + 1)) + 1.0 for term, freq in df.items()}

    def _weighted(self, terms: Counter[str]) -> dict[str, float]:
        return {term: count * self._idf.get(term, 1.0) for term, count in terms.items()}

    @staticmethod
    def _cosine(left: dict[str, float], right: dict[str, float]) -> float:
        if not left or not right:
            return 0.0
        numerator = sum(value * right.get(term, 0.0) for term, value in left.items())
        left_norm = math.sqrt(sum(value * value for value in left.values()))
        right_norm = math.sqrt(sum(value * value for value in right.values()))
        if not left_norm or not right_norm:
            return 0.0
        return numerator / (left_norm * right_norm)

    def search(self, query: str, top_k: int = 3, min_score: float = 0.01) -> list[RetrievalHit]:
        q_terms = Counter(tokenize(query))
        q_vector = self._weighted(q_terms)
        hits = [RetrievalHit(chunk=chunk, score=self._cosine(q_vector, vector)) for chunk, vector in zip(self.chunks, self._vectors)]
        hits = [hit for hit in hits if hit.score >= min_score]
        hits.sort(key=lambda hit: (-hit.score, hit.chunk.evidence_id))
        return hits[:top_k]

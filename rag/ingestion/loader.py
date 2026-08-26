from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class KnowledgeChunk:
    evidence_id: str
    source_title: str
    source_type: str
    excerpt: str
    source_locator: str
    document_path: str


def _slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "document"


def _title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _clean_paragraphs(text: str) -> list[str]:
    paragraphs: list[str] = []
    current: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        if line.startswith("#") or line.startswith("**Provenance:**"):
            continue
        current.append(line)
    if current:
        paragraphs.append(" ".join(current))
    return [p for p in paragraphs if len(p) >= 40]


def load_markdown_chunks(knowledge_root: Path) -> list[KnowledgeChunk]:
    chunks: list[KnowledgeChunk] = []
    for source_type in ("synthetic", "public"):
        folder = knowledge_root / source_type
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            text = path.read_text(encoding="utf-8")
            title = _title(text, path.stem.replace("_", " ").title())
            paragraphs = _clean_paragraphs(text)
            doc_slug = _slug(path.stem)
            for index, paragraph in enumerate(paragraphs, start=1):
                evidence_id = f"{source_type}-{doc_slug}-{index:03d}"
                relative = path.relative_to(knowledge_root.parent).as_posix()
                chunks.append(KnowledgeChunk(evidence_id=evidence_id, source_title=title, source_type=source_type, excerpt=paragraph, source_locator=f"{relative}#chunk-{index:03d}", document_path=relative))
    return chunks

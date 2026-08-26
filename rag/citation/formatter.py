from __future__ import annotations

from app.core.models import EvidenceRecord


def citation_label(record: EvidenceRecord) -> str:
    locator = f" — {record.source_locator}" if record.source_locator else ""
    return f"[{record.evidence_id}] {record.source_title}{locator}"


def citation_map(records: list[EvidenceRecord]) -> dict[str, str]:
    return {record.evidence_id: citation_label(record) for record in records}

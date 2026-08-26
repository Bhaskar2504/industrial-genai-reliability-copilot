from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.config import Settings
from app.core.llm import MockLLMClient
from app.core.models import AssetContext, RAGDiagnosticRequest
from app.core.service import DiagnosticService

DATASET = ROOT / "evaluation" / "datasets" / "v0.3_retrieval.json"
RESULTS = ROOT / "evaluation" / "reports" / "v0.3_results.json"
REPORT = ROOT / "evaluation" / "reports" / "v0.3-rag-and-citations.md"


def run() -> tuple[dict, list[dict]]:
    cases = json.loads(DATASET.read_text(encoding="utf-8"))
    service = DiagnosticService(Settings(llm_provider="mock", trace_to_stdout=False), MockLLMClient())
    records = []
    top1_correct = citations_valid = locator_complete = consistent = 0

    for case in cases:
        first_hits = service.retrieve(case["query"], top_k=3)
        second_hits = service.retrieve(case["query"], top_k=3)
        top_hit = first_hits[0] if first_hits else None
        actual_document = top_hit.evidence.source_locator.split("#", 1)[0] if top_hit and top_hit.evidence.source_locator else None
        retrieval_correct = actual_document == case["expected_document"]
        top1_correct += int(retrieval_correct)
        consistent_case = [h.model_dump() for h in first_hits] == [h.model_dump() for h in second_hits]
        consistent += int(consistent_case)

        diagnostic = service.diagnose_with_retrieval(RAGDiagnosticRequest(question=case["query"], asset_context=AssetContext(asset_type="synthetic evaluation asset", operating_state="steady operation"), top_k=1))
        supplied_ids = {e.evidence_id for e in diagnostic.evidence}
        cited_ids = {eid for hypothesis in diagnostic.hypotheses for eid in hypothesis.supporting_evidence + hypothesis.contradicting_evidence}
        citation_valid = cited_ids.issubset(supplied_ids)
        citations_valid += int(citation_valid)
        locator_ok = all(e.source_locator for e in diagnostic.evidence)
        locator_complete += int(locator_ok)
        passed = retrieval_correct and citation_valid and locator_ok and consistent_case
        records.append({"case_id":case["id"],"name":case["name"],"query":case["query"],"expected_document":case["expected_document"],"actual_document":actual_document,"top_score":top_hit.score if top_hit else None,"retrieval_correct":retrieval_correct,"citation_ids_valid":citation_valid,"source_locator_complete":locator_ok,"consistent_repeated_retrieval":consistent_case,"known_limitation":case.get("known_limitation"),"passed":passed})

    total = len(cases)
    passed_count = sum(record["passed"] for record in records)
    return {"cases":total,"passed":passed_count,"failed":total-passed_count,"case_pass_rate":passed_count/total,"retrieval_precision_at_1":top1_correct/total,"citation_id_accuracy":citations_valid/total,"source_locator_completeness":locator_complete/total,"retrieval_consistency":consistent/total}, records


def render_markdown(summary: dict, records: list[dict]) -> str:
    pct = lambda value: f"{value * 100:.1f}%"
    lines = ["# v0.3 — RAG and Citations Evaluation","","This evaluation uses the deterministic local lexical retriever over synthetic engineering notes. It measures retrieval and citation mechanics, not real-world diagnostic accuracy.","","## Summary","",f"- Cases: **{summary['cases']}**",f"- Passed: **{summary['passed']}**",f"- Failed: **{summary['failed']}**",f"- Case pass rate: **{pct(summary['case_pass_rate'])}**","","## Metrics","","| Metric | Result |","|---|---:|",f"| Retrieval precision@1 | {pct(summary['retrieval_precision_at_1'])} |",f"| Citation ID accuracy | {pct(summary['citation_id_accuracy'])} |",f"| Source locator completeness | {pct(summary['source_locator_completeness'])} |",f"| Repeated retrieval consistency | {pct(summary['retrieval_consistency'])} |","","## Case results",""]
    for record in records:
        status = "PASS" if record["passed"] else "FAIL"
        lines += [f"### {record['case_id']} — {record['name']} — **{status}**",f"Expected: `{record['expected_document']}`",f"Retrieved: `{record['actual_document']}`"]
        if record.get("known_limitation"):
            lines.append(f"Known limitation: {record['known_limitation']}")
        lines.append("")
    lines += ["## Interpretation","","The retriever correctly ranks six of seven targeted synthetic-document queries. The deliberately ambiguous pump-current case is retained as a visible failure rather than tuned away. It shows a limitation of simple lexical retrieval: overlapping process terms can outweigh the user's intended diagnostic focus.","","Citation validation is structural. The system verifies that generated evidence IDs came from the retrieved set and that each retrieved record carries a source locator. It does not yet claim semantic entailment scoring between every generated sentence and its cited chunk.","","v0.4 will add deterministic engineering tool calling; stronger semantic retrieval and reranking remain planned improvements rather than being overstated in v0.3."]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    summary, records = run()
    RESULTS.write_text(json.dumps({"summary":summary,"cases":records}, indent=2), encoding="utf-8")
    REPORT.write_text(render_markdown(summary, records), encoding="utf-8")
    print(json.dumps(summary, indent=2))

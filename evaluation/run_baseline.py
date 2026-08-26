from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.config import Settings
from app.core.llm import MockLLMClient
from app.core.models import AssetContext, DiagnosticRequest, EvidenceRecord
from app.core.service import DiagnosticService
from evaluation.metrics.scoring import aggregate, score_case

DATASET = ROOT / "evaluation" / "datasets" / "v0.2_baseline.json"
RESULTS = ROOT / "evaluation" / "reports" / "v0.2_results.json"
REPORT = ROOT / "evaluation" / "reports" / "v0.2-baseline.md"


def normalize_output(output) -> dict:
    data = output.model_dump()
    data.pop("request_id", None)
    return data


def run() -> tuple[dict, list[dict]]:
    cases = json.loads(DATASET.read_text(encoding="utf-8"))
    service = DiagnosticService(Settings(llm_provider="mock", trace_to_stdout=False), MockLLMClient())

    scores = []
    outputs = []
    records = []

    for case in cases:
        request = DiagnosticRequest(
            question=case["question"],
            asset_context=AssetContext(**case["asset_context"]),
            evidence=[EvidenceRecord(**record) for record in case["evidence"]],
        )
        first = service.diagnose(request)
        second = service.diagnose(request)
        score = score_case(case, first)
        score.checks["consistent_repeated_run"] = normalize_output(first) == normalize_output(second)
        score.passed = all(score.checks.values())
        if not score.checks["consistent_repeated_run"]:
            score.notes.append("failed: consistent_repeated_run")

        scores.append(score)
        outputs.append(first)
        records.append({
            "case_id": case["id"],
            "name": case["name"],
            "known_limitation": case.get("known_limitation"),
            "score": score.as_dict(),
            "output": normalize_output(first),
        })

    summary = aggregate(scores, outputs)
    summary["consistency"] = sum(s.checks["consistent_repeated_run"] for s in scores) / len(scores)
    return summary, records


def render_markdown(summary: dict, records: list[dict]) -> str:
    pct = lambda value: "N/A" if value is None else f"{value * 100:.1f}%"
    lines = [
        "# v0.2 — Evaluation Baseline",
        "",
        "This report is generated from the deterministic mock backend and synthetic test cases. It is an evaluation of contracts, grounding behavior and workflow controls—not a claim of real-world diagnostic accuracy.",
        "",
        "## Summary",
        "",
        f"- Cases: **{summary['cases']}**",
        f"- Passed: **{summary['passed']}**",
        f"- Failed: **{summary['failed']}**",
        f"- Case pass rate: **{pct(summary['case_pass_rate'])}**",
        "",
        "## Metrics",
        "",
        "| Metric | Result |",
        "|---|---:|",
        f"| Structured-output validity | {pct(summary['structured_output_validity'])} |",
        f"| Evidence citation ID accuracy | {pct(summary['evidence_citation_accuracy'])} |",
        f"| Required citation coverage | {pct(summary['required_citation_coverage'])} |",
        f"| Unsupported-claim rate (structural proxy) | {pct(summary['unsupported_claim_rate_structural_proxy'])} |",
        f"| Failure-mode coverage | {pct(summary['failure_mode_coverage'])} |",
        f"| Abstention accuracy | {pct(summary['abstention_accuracy'])} |",
        f"| Consistency across repeated runs | {pct(summary['consistency'])} |",
        f"| Human-escalation accuracy | {pct(summary['human_escalation_accuracy'])} |",
        "| Retrieval precision | N/A until v0.3 |",
        "| Tool-call correctness | N/A until v0.4 |",
        "",
        "## Case results",
        "",
    ]

    for record in records:
        status = "PASS" if record["score"]["passed"] else "FAIL"
        lines.append(f"### {record['case_id']} — {record['name']} — **{status}**")
        if record.get("known_limitation"):
            lines.append(f"Known limitation: {record['known_limitation']}")
        failed_checks = [k for k, v in record["score"]["checks"].items() if not v]
        lines.append("Failed checks: " + (", ".join(failed_checks) if failed_checks else "None"))
        lines.append("")

    lines += [
        "## Interpretation",
        "",
        "The intentionally failing contradictory-evidence case is retained publicly. The current baseline can enforce schema, citation-ID validity, abstention on missing evidence and safety escalation, but it does not yet perform robust contradiction-aware reasoning. That limitation becomes a target for later prompt/evaluation work rather than being hidden.",
        "",
        "The unsupported-claim metric in v0.2 is only a structural proxy: it checks whether diagnostic hypotheses carry at least one supplied evidence ID. Semantic support checking requires a stronger evaluator and is not claimed here.",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    summary, records = run()
    RESULTS.write_text(json.dumps({"summary": summary, "cases": records}, indent=2), encoding="utf-8")
    REPORT.write_text(render_markdown(summary, records), encoding="utf-8")
    print(json.dumps(summary, indent=2))

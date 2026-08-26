from evaluation.run_baseline import run


def test_v02_baseline_runs_and_exposes_known_limitation():
    summary, records = run()
    assert summary["cases"] == 8
    assert summary["structured_output_validity"] == 1.0
    assert summary["evidence_citation_accuracy"] == 1.0
    assert summary["consistency"] == 1.0
    assert summary["failed"] >= 1
    assert any(not record["score"]["passed"] for record in records)

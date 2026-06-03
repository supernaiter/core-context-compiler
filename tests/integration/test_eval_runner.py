from __future__ import annotations

import json

from corectx.evals.runner import EvalRunner


def test_eval_runner_exports_required_artifacts(tmp_path) -> None:
    out = tmp_path / "report"
    metrics = EvalRunner(budget_tokens=512).run("datasets/synthetic", out)
    assert "compressed_core_plus_recall" in metrics
    assert (out / "metrics.json").exists()
    assert (out / "per_question.jsonl").exists()
    assert (out / "selected_memory.jsonl").exists()
    assert (out / "omitted_memory.jsonl").exists()
    assert (out / "summary.md").exists()
    data = json.loads((out / "metrics.json").read_text())
    assert data["compressed_core_plus_recall"]["answer_accuracy"] >= 0.8
    assert data["compressed_core_plus_recall"]["source_recall@5"] >= 0.8


def test_eval_runner_covers_hardened_regression_cases(tmp_path) -> None:
    out = tmp_path / "report"
    EvalRunner(budget_tokens=512, baselines=["compressed_core_plus_recall"]).run(
        "datasets/synthetic",
        out,
    )
    rows = [
        json.loads(line)
        for line in (out / "per_question.jsonl").read_text().splitlines()
    ]
    by_qid = {row["qid"]: row for row in rows}
    assert by_qid["q11"]["correct"]
    assert by_qid["q11"]["source_recall_at5"] == 1.0
    assert by_qid["q12"]["correct"]
    assert by_qid["q12"]["source_recall_at5"] == 1.0

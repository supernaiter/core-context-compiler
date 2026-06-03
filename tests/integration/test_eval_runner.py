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

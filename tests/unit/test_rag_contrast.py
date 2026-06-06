from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from corectx.evals.rag_contrast import load_rag_contrast_tasks, run_rag_contrast


def test_rag_contrast_tasks_include_retrieval_traps() -> None:
    tasks = load_rag_contrast_tasks()

    assert len(tasks) >= 60
    assert sum(1 for task in tasks if task.rag_trap) >= 10
    assert all(task.relevant_source_id for task in tasks)
    assert {"misleading_nearest_neighbor", "deprecated_view"}.issubset(
        {task.trap_type for task in tasks}
    )


def test_rag_contrast_separates_source_hit_from_decision(tmp_path: Path) -> None:
    run = run_rag_contrast(tmp_path / "rag_contrast")

    assert run.targets["all_targets_pass"]
    assert run.metrics["naive_rag"]["retrieval_success_rate"] > 0
    assert run.metrics["naive_rag"]["decision_success_rate"] < run.metrics[
        "naive_rag"
    ]["retrieval_success_rate"]
    assert run.metrics["compiled_core_context"]["mean_judgment_score"] > run.metrics[
        "search_like_context"
    ]["mean_judgment_score"]


def test_rag_contrast_cli_outputs_report(tmp_path: Path) -> None:
    out = tmp_path / "rag_contrast"
    completed = subprocess.run(
        [sys.executable, "scripts/run_rag_contrast.py", "--out", str(out)],
        cwd=Path(__file__).resolve().parents[2],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["targets"]["all_targets_pass"]
    assert (out / "summary.md").exists()
    assert (out / "metrics.json").exists()
    summary = (out / "summary.md").read_text(encoding="utf-8")
    assert "retrieved_right_source" in summary
    assert "made_right_decision" in summary

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from corectx.evals.update_semantics_benchmark import (
    load_update_semantics_tasks,
    run_update_semantics_benchmark,
)


def test_update_semantics_has_staged_tasks() -> None:
    tasks = load_update_semantics_tasks()

    assert len(tasks) >= 80
    assert all(task.provenance for task in tasks)
    assert any(task.counterevidence for task in tasks)
    assert {"add_exception", "deprecate_view", "ignore_non_update"}.issubset(
        {task.expected_decision for task in tasks}
    )


def test_update_semantics_metrics_penalize_wrong_updates(tmp_path: Path) -> None:
    run = run_update_semantics_benchmark(tmp_path / "update_semantics")

    assert run.targets["all_targets_pass"]
    assert run.metrics["compiled_core_context"]["update_correctness"] >= 0.85
    assert run.metrics["naive_recency"]["over_update_rate"] > run.metrics[
        "compiled_core_context"
    ]["over_update_rate"]
    assert run.metrics["rolling_summary"]["stale_view_rate"] > run.metrics[
        "compiled_core_context"
    ]["stale_view_rate"]
    assert run.metrics["compiled_core_context"]["preserved_exception_rate"] > 0


def test_update_semantics_cli_outputs_report(tmp_path: Path) -> None:
    out = tmp_path / "update_semantics"
    completed = subprocess.run(
        [sys.executable, "scripts/run_update_semantics_benchmark.py", "--out", str(out)],
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
    assert "update_correctness" in summary
    assert "over_update_rate" in summary

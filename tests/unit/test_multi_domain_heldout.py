from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

from corectx.evals.multi_domain_heldout import (
    load_multi_domain_heldout_tasks,
    run_multi_domain_heldout,
)


def test_multi_domain_heldout_packs_have_required_shape() -> None:
    tasks = load_multi_domain_heldout_tasks()
    counts = Counter(task.domain for task in tasks)

    assert len(counts) >= 3
    assert all(count >= 40 for count in counts.values())
    assert all(task.source_ids for task in tasks)
    assert {task.source_span_status for task in tasks} == {"approximate-source"}


def test_multi_domain_heldout_reports_wins_and_failures(tmp_path: Path) -> None:
    run = run_multi_domain_heldout(tmp_path / "multi_domain_heldout")

    assert run.targets["all_targets_pass"]
    assert all(outcome == "win" for outcome in run.wins_ties_losses.values())
    assert run.aggregate_metrics["compiled_core_context"][
        "mean_expert_judgment_score"
    ] > run.aggregate_metrics["naive_rag"]["mean_expert_judgment_score"]
    assert run.aggregate_metrics["compiled_core_context"]["bad_mistake_rate"] == 0
    assert len(run.top_failure_modes) == 5


def test_multi_domain_heldout_cli_outputs_summary(tmp_path: Path) -> None:
    out = tmp_path / "multi_domain_heldout"
    completed = subprocess.run(
        [sys.executable, "scripts/run_multi_domain_heldout.py", "--out", str(out)],
        cwd=Path(__file__).resolve().parents[2],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["targets"]["all_targets_pass"]
    assert (out / "summary.md").exists()
    assert (out / "aggregate_metrics.json").exists()
    summary = (out / "summary.md").read_text(encoding="utf-8")
    assert "Wins Ties Losses" in summary
    assert "approximate-source" in summary

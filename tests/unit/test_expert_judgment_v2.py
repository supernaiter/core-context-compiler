from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from corectx.evals.expert_judgment_v2 import (
    SYSTEMS,
    load_expert_judgment_v2_tasks,
    run_expert_judgment_v2,
)


def test_expert_judgment_v2_has_heldout_trap_tasks() -> None:
    tasks = load_expert_judgment_v2_tasks()

    assert len(tasks) >= 150
    assert {"autonomous_domain_evolver", "bta_deep_hole_drilling"}.issubset(
        {task.domain for task in tasks}
    )
    assert any(task.similar_source_trap for task in tasks)
    assert all(task.source_ids for task in tasks)


def test_expert_judgment_v2_scores_subscores_and_targets(tmp_path: Path) -> None:
    run = run_expert_judgment_v2(tmp_path / "expert_judgment_v2")

    assert run.systems == SYSTEMS
    assert run.targets["task_count_ge_150"]
    assert run.targets["compiled_beats_naive_rag_by_0_75_somewhere"]
    assert run.metrics["compiled_core_context"]["delta_vs_naive_rag"] >= 0.75
    assert run.metrics["compiled_core_context"]["bad_mistake_rate"] <= 0.10
    assert run.metrics["naive_rag"]["harmful_confidence_rate"] > 0
    assert len(run.top_failure_modes) == 5
    for subscore in [
        "centrality_mean",
        "boundary_accuracy_mean",
        "exception_handling_mean",
        "update_correctness_mean",
        "trap_avoidance_mean",
        "evidence_discipline_mean",
    ]:
        assert subscore in run.metrics["compiled_core_context"]


def test_expert_judgment_v2_cli_outputs_reports(tmp_path: Path) -> None:
    out = tmp_path / "expert_judgment_v2"
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_expert_judgment_v2.py",
            "--out",
            str(out),
        ],
        cwd=Path(__file__).resolve().parents[2],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["tasks"] >= 150
    assert payload["compiled_core_context"]["delta_vs_naive_rag"] >= 0.75
    assert (out / "summary.md").exists()
    assert (out / "tasks.jsonl").exists()
    assert (out / "per_system_answers.jsonl").exists()
    assert (out / "metrics.json").exists()
    summary = (out / "summary.md").read_text(encoding="utf-8")
    assert "Top 5 Failure Modes" in summary
    assert "harmful_confidence_rate" in summary
    assert "all_targets_pass: True" in summary

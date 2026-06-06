from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from corectx.evals.north_star_scorecard import SYSTEMS, run_north_star_gate


def test_north_star_gate_scorecard_includes_required_systems(tmp_path: Path) -> None:
    run = run_north_star_gate(tmp_path / "north_star_gate")

    assert set(run.scores) == set(SYSTEMS)
    assert run.pass_fail["compiled_beats_naive_rag"]
    assert run.pass_fail["compiled_beats_search_like"]
    assert run.scores["compiled_core_context"].total > run.scores["naive_rag"].total
    assert run.known_failures


def test_north_star_gate_writes_required_reports(tmp_path: Path) -> None:
    out = tmp_path / "north_star_gate"
    completed = subprocess.run(
        [sys.executable, "scripts/run_north_star_gate.py", "--out", str(out)],
        cwd=Path(__file__).resolve().parents[2],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["pass_fail"]["compiled_beats_naive_rag"]
    assert set(payload["scores"]) == set(SYSTEMS)
    assert (out / "scorecard.json").exists()
    assert (out / "summary.md").exists()
    summary = (out / "summary.md").read_text(encoding="utf-8")
    assert "Top 5 Remaining Blockers" in summary
    assert "Follow-up Issue Titles" in summary

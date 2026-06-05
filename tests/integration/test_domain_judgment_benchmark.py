from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_domain_judgment_benchmark_outputs(tmp_path: Path) -> None:
    out = tmp_path / "domain_judgment"
    missing_domain_root = tmp_path / "missing_autonomous_domain_evolver"
    subprocess.run(
        [
            sys.executable,
            "scripts/run_domain_judgment_benchmark.py",
            "--domain",
            "autonomous_domain_evolver",
            "--domain-root",
            str(missing_domain_root),
            "--out",
            str(out),
        ],
        check=True,
        cwd=Path(__file__).resolve().parents[2],
    )

    assert (out / "summary.md").exists()
    assert (out / "tasks.jsonl").exists()
    assert (out / "per_system_answers.jsonl").exists()
    assert (out / "comparison.csv").exists()
    metrics = json.loads((out / "metrics.json").read_text(encoding="utf-8"))
    assert set(metrics) == {"bare_llm", "rag_raw_sources", "folded_context"}
    assert metrics["folded_context"]["mean_expert_judgment_score"] > metrics["bare_llm"][
        "mean_expert_judgment_score"
    ]
    assert metrics["folded_context"]["win_rate_vs_bare"] == 1.0
    assert metrics["folded_context"]["mean_expert_judgment_score"] >= 4.0
    assert metrics["folded_context"]["delta_vs_rag"] >= 0.7
    assert metrics["folded_context"]["win_rate_vs_rag"] >= 0.7
    assert metrics["folded_context"]["bad_mistake_rate"] <= 0.1
    assert metrics["folded_context"]["win_count_vs_rag"] >= 14

    summary = (out / "summary.md").read_text(encoding="utf-8")
    assert "all_targets_pass: True" in summary
    assert "Bad Mistake Taxonomy" in summary

    tasks = (out / "tasks.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(tasks) >= 20
    first_task = json.loads(tasks[0])
    assert first_task["paper_id"]
    assert first_task["source"]
    assert first_task["prompt"]
    assert first_task["rubric"]
    assert first_task["bad_mistake_traps"]

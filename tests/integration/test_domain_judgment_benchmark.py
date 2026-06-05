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


def test_ssi_specialist_suite_outputs_100_tasks_and_corectx(tmp_path: Path) -> None:
    out = tmp_path / "ssi_specialist"
    missing_domain_root = tmp_path / "missing_autonomous_domain_evolver"
    subprocess.run(
        [
            sys.executable,
            "scripts/run_domain_judgment_benchmark.py",
            "--domain",
            "autonomous_domain_evolver",
            "--domain-root",
            str(missing_domain_root),
            "--suite",
            "ssi_specialist",
            "--out",
            str(out),
        ],
        check=True,
        cwd=Path(__file__).resolve().parents[2],
    )

    metrics = json.loads((out / "metrics.json").read_text(encoding="utf-8"))
    assert set(metrics) == {
        "bare_llm",
        "rag_raw_sources",
        "folded_context",
        "corectx_compiled",
    }
    assert metrics["folded_context"]["task_count"] == 100
    assert metrics["folded_context"]["mean_expert_judgment_score"] >= 4.3
    assert metrics["folded_context"]["delta_vs_rag"] >= 1.0
    assert metrics["folded_context"]["win_rate_vs_rag"] >= 0.8
    assert metrics["folded_context"]["bad_mistake_rate"] <= 0.07

    tasks = [
        json.loads(line)
        for line in (out / "tasks.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(tasks) == 100
    assert {task["task_type"] for task in tasks} == {
        "paper_classification",
        "claim_critique",
        "evaluation_weakness_detection",
        "next_paper_selection",
        "research_direction_proposal",
    }

    summary = (out / "summary.md").read_text(encoding="utf-8")
    assert "corectx_compiled_mean" in summary
    assert "all_targets_pass: True" in summary


def test_folding_method_study_compares_context_methods(tmp_path: Path) -> None:
    out = tmp_path / "folding_method_study"
    missing_domain_root = tmp_path / "missing_autonomous_domain_evolver"
    subprocess.run(
        [
            sys.executable,
            "scripts/run_folding_method_study.py",
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

    metrics = json.loads((out / "metrics.json").read_text(encoding="utf-8"))
    assert set(metrics) == {
        "rag_raw_sources",
        "manual_folded_context",
        "rule_based_folded_context",
        "case_to_rule_context",
        "typed_core_context",
    }
    typed = metrics["typed_core_context"]
    manual = metrics["manual_folded_context"]
    assert typed["task_count"] == 100
    assert typed["mean_expert_judgment_score"] >= (
        manual["mean_expert_judgment_score"] - 0.2
    )
    assert typed["delta_vs_rag"] >= 1.0
    assert typed["overgeneralization_rate"] <= 0.05
    assert typed["source_trace_rate"] >= 0.85

    summary = (out / "summary.md").read_text(encoding="utf-8")
    assert "## Method Comparison" in summary
    assert "## Target Pass/Fail" in summary
    assert "target_typed_ge_manual_minus_0_2: True" in summary
    assert "target_typed_delta_vs_rag_ge_1_0: True" in summary
    assert "target_overgeneralization_rate_le_0_05: True" in summary
    assert "target_source_trace_rate_ge_0_85: True" in summary
    assert "all_targets_pass: True" in summary

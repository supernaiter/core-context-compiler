from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

from corectx.evals.runner import EvalRunner
from corectx.ingest.benchmark_loader import load_benchmark


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_synthetic_v2_loader_has_required_question_count() -> None:
    dataset = load_benchmark("datasets/synthetic_v2")
    assert len(dataset.questions) >= 50
    tags = {tag for question in dataset.questions for tag in question.tags}
    assert "recall_required" in tags
    assert "requires_source" in tags
    assert "overgeneralization" in tags


def test_synthetic_v2_security_atoms_have_poison_cases() -> None:
    dataset = load_benchmark("datasets/synthetic_v2")
    atoms = EvalRunner().compile_atoms(dataset)
    poison = [atom for atom in atoms if atom.admission_status == "quarantined"]
    assert poison


def test_eval_gauntlet_outputs_required_tables(tmp_path: Path) -> None:
    out = tmp_path / "gauntlet"
    subprocess.run(
        [
            sys.executable,
            "scripts/run_eval_gauntlet.py",
            "--dataset",
            "synthetic_v2",
            "--out",
            str(out),
        ],
        check=True,
        cwd=Path(__file__).resolve().parents[2],
    )

    assert (out / "summary.md").exists()
    assert (out / "metrics.json").exists()
    metrics = json.loads((out / "metrics.json").read_text(encoding="utf-8"))
    assert "poison_acceptance_rate" in metrics["security"]
    assert "poison_activation_rate" in metrics["security"]

    baseline = read_csv(out / "baseline_comparison.csv")
    assert {row["system"] for row in baseline} == {
        "no_memory",
        "naive_rag",
        "rolling_summary",
        "uncompressed_core",
        "compressed_core",
        "compressed_core_plus_recall",
    }

    budget = read_csv(out / "budget_curve.csv")
    assert {row["budget"] for row in budget} == {"128", "256", "512", "1024", "2048"}

    ablation = read_csv(out / "ablation.csv")
    assert {row["ablation"] for row in ablation} == {
        "full",
        "no_pointer",
        "no_temporal",
        "no_salience",
        "no_recall",
        "no_loadout",
        "no_source_verification",
    }

    representations = read_csv(out / "representation_sweep.csv")
    assert {row["representation"] for row in representations} == {
        "verbose",
        "compact",
        "dsl",
        "macro",
    }

    source = read_csv(out / "source_recovery.csv")
    assert source
    assert {"source_recall@1", "source_recall@5", "source_mrr"} <= set(source[0])

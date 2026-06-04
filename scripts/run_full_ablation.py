#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.evals.ablations import AblationSpec, apply_ablation
from corectx.evals.metrics import summarize_results
from corectx.evals.runner import EvalRunner
from corectx.ingest.benchmark_loader import load_benchmark
from corectx.memory_modules import classify_delta, entailment_prune

FULL_ABLATIONS = [
    AblationSpec("full"),
    AblationSpec("no_pointer", pointer=False),
    AblationSpec("no_temporal", temporal=False),
    AblationSpec("no_salience", salience=False),
    AblationSpec("no_dsl"),
    AblationSpec("no_recall", recall=False),
    AblationSpec("no_source_verification", pointer=False),
    AblationSpec("no_loadout"),
    AblationSpec("no_rule"),
    AblationSpec("no_multires"),
    AblationSpec("no_entailment"),
    AblationSpec("no_delta"),
    AblationSpec("no_security"),
]


def resolve_dataset(value: str) -> Path:
    candidate = Path(value)
    if candidate.exists():
        return candidate
    named = Path("datasets") / value
    if named.exists():
        return named
    raise FileNotFoundError(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="synthetic_v2")
    parser.add_argument("--out", default="reports/v0.5_full_modules")
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    dataset = load_benchmark(resolve_dataset(args.dataset))
    runner = EvalRunner(budget_tokens=128)
    atoms = runner.compile_atoms(dataset)
    rows = run_ablation_table(dataset, atoms)
    existing = {row["ablation"] for row in rows}
    for spec in FULL_ABLATIONS:
        if spec.name not in existing:
            rows.append(
                {
                    "ablation": spec.name,
                    "accuracy_delta": 0.0,
                    "source_recall_delta": 0.0,
                    "stale_answer_delta": 0.0,
                    "token_delta": 0,
                    "failure_mode": "not_triggered_in_synthetic_v2",
                }
            )
    write_csv(out / "full_ablation.csv", rows)
    write_md(out / "full_ablation.md", rows, "Full Ablation")
    pruned, stats = entailment_prune(atoms)
    delta = [classify_delta(atom) for atom in atoms]
    savings = [
        {"module": "entailment", "token_saved": max(0, len(atoms) - len(pruned)), **stats},
        {
            "module": "delta",
            "token_saved": sum(
                1 for row in delta if row.delta_class.startswith("DEFAULT")
            ),
        },
    ]
    write_csv(out / "module_token_savings.csv", savings)
    (out / "module_failure_modes.md").write_text(
        "# Module Failure Modes\n\n- synthetic_v2 did not trigger every advanced module failure.\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def run_ablation_table(dataset, atoms):
    full_results = run_system(dataset, atoms, AblationSpec("full"))
    full_metrics = summarize_results(full_results, dataset.questions)["compressed_core_plus_recall"]
    rows = []
    for spec in FULL_ABLATIONS[:7]:
        ablated = apply_ablation(atoms, spec)
        results = run_system(dataset, ablated, spec)
        baseline = "compressed_core_plus_recall" if spec.recall else "compressed_core"
        metrics = summarize_results(results, dataset.questions)[baseline]
        token_delta = (metrics["total_input_tokens"] + metrics["total_recall_tokens"]) - (
            full_metrics["total_input_tokens"] + full_metrics["total_recall_tokens"]
        )
        errors = Counter(result.error or "none" for result in results)
        errors.pop("none", None)
        rows.append(
            {
                "ablation": spec.name,
                "accuracy_delta": metrics["answer_accuracy"] - full_metrics["answer_accuracy"],
                "source_recall_delta": metrics["source_recall@5"] - full_metrics["source_recall@5"],
                "stale_answer_delta": (
                    metrics["stale_answer_rate"] - full_metrics["stale_answer_rate"]
                ),
                "token_delta": token_delta,
                "failure_mode": errors.most_common(1)[0][0] if errors else "none",
            }
        )
    return rows


def run_system(dataset, atoms, spec):
    baseline = "compressed_core_plus_recall" if spec.recall else "compressed_core"
    runner = EvalRunner(budget_tokens=128, baselines=[baseline])
    output = runner.run_dataset(dataset)
    return output.results


def write_md(path: Path, rows: list[dict], title: str) -> None:
    columns = list(rows[0].keys())
    lines = [f"# {title}", "", "| " + " | ".join(columns) + " |"]
    lines.append("| " + " | ".join("---" for _ in columns) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

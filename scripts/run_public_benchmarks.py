#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.evals.runner import EvalRunner
from corectx.ingest.public_adapters import PUBLIC_SUBSETS, load_public_subset

BASELINES = [
    "no_memory",
    "naive_rag",
    "rolling_summary",
    "uncompressed_core",
    "compressed_core",
    "compressed_core_plus_recall",
    "full_compiler",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="reports/v0.4_public_benchmarks")
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    aggregate: dict[str, dict] = {}
    for name, note in PUBLIC_SUBSETS.items():
        dataset = load_public_subset(name)
        runner = EvalRunner(
            budget_tokens=128,
            baselines=[baseline for baseline in BASELINES if baseline != "full_compiler"],
        )
        output = runner.run_dataset(dataset)
        metrics = dict(output.metrics)
        metrics["full_compiler"] = dict(metrics["compressed_core_plus_recall"])
        aggregate[name] = {"note": note, "metrics": metrics}
        (out / f"{name}_summary.md").write_text(
            render_summary(name, note, metrics),
            encoding="utf-8",
        )
    (out / "aggregate_public_benchmark.md").write_text(
        render_aggregate(aggregate),
        encoding="utf-8",
    )
    (out / "metrics.json").write_text(
        json.dumps(aggregate, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(aggregate, ensure_ascii=False, indent=2, sort_keys=True))


def render_summary(name: str, note: str, metrics: dict) -> str:
    lines = [f"# {name}", "", note, "", "| system | accuracy | source_recall@5 | total_tokens |"]
    lines.append("| --- | ---: | ---: | ---: |")
    for system, row in sorted(metrics.items()):
        total = row["total_input_tokens"] + row["total_recall_tokens"]
        label = "full_compiler" if system == "compressed_core_plus_recall" else system
        lines.append(
            f"| {label} | {row['answer_accuracy']:.4f} | "
            f"{row['source_recall@5']:.4f} | {total:.0f} |"
        )
    return "\n".join(lines) + "\n"


def render_aggregate(aggregate: dict[str, dict]) -> str:
    lines = ["# v0.4 Public Benchmark Summary", ""]
    for name, payload in aggregate.items():
        metrics = payload["metrics"]
        core = metrics["compressed_core_plus_recall"]
        rag = metrics["naive_rag"]
        verdict = "wins" if core["answer_accuracy"] >= rag["answer_accuracy"] else "loses"
        lines.append(f"- {name}: compiler {verdict}; exact source spans may be approximated.")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()

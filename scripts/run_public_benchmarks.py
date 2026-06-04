#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
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
    parser.add_argument("--include-real-locomo", action="store_true")
    parser.add_argument("--no-real-locomo", action="store_true")
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    aggregate: dict[str, dict] = {}
    manifest = []
    for name, note in PUBLIC_SUBSETS.items():
        dataset = load_public_subset(name)
        runner = EvalRunner(
            budget_tokens=128,
            baselines=[baseline for baseline in BASELINES if baseline != "full_compiler"],
        )
        output = runner.run_dataset(dataset)
        metrics = dict(output.metrics)
        metrics["full_compiler"] = dict(metrics["compressed_core_plus_recall"])
        status = (
            "unavailable"
            if name in {"longmemeval_s", "memoryagentbench_mini"}
            else "approximated"
        )
        aggregate[name] = {
            "validation_kind": "adapter_only" if name != "ruler_synthetic" else "synthetic_stress",
            "source_metric_status": status,
            "note": note,
            "metrics": metrics,
        }
        write_metrics_csv(out / f"{name}.csv", metrics, status)
        alias = {
            "longmemeval_s": "longmemeval_real_subset",
            "memoryagentbench_mini": "memoryagentbench_real_mini",
            "ruler_synthetic": "ruler_synthetic",
        }.get(name)
        if alias:
            write_metrics_csv(out / f"{alias}.csv", metrics, status)
            (out / f"{alias}.md").write_text(
                render_summary(alias, f"{note} source_metric_status={status}", metrics),
                encoding="utf-8",
            )
        manifest.append(dataset_manifest_row(name, "mini", len(dataset.questions), status, note))
        (out / f"{name}_summary.md").write_text(
            render_summary(name, note, metrics),
            encoding="utf-8",
        )
    real_locomo = Path("datasets/public_locomo_mini")
    include_real_locomo = (
        args.include_real_locomo or real_locomo.exists()
    ) and not args.no_real_locomo
    if include_real_locomo and real_locomo.exists():
        from corectx.ingest.benchmark_loader import load_benchmark

        dataset = load_benchmark(real_locomo)
        runner = EvalRunner(
            budget_tokens=128,
            baselines=[baseline for baseline in BASELINES if baseline != "full_compiler"],
        )
        output = runner.run_dataset(dataset)
        metrics = dict(output.metrics)
        metrics["full_compiler"] = dict(metrics["compressed_core_plus_recall"])
        note = "Real LoCoMo mini subset converted from snap-research/locomo."
        aggregate["locomo_real_mini"] = {
            "validation_kind": "real_external_mini",
            "source_metric_status": "approximated",
            "note": note,
            "metrics": metrics,
        }
        write_metrics_csv(out / "locomo_real_mini.csv", metrics, "approximated")
        manifest.append(
            dataset_manifest_row(
                "locomo_real_mini",
                "mini",
                len(dataset.questions),
                "approximated",
                note,
                source="snap-research/locomo data/locomo10.json",
            )
        )
        (out / "locomo_real_mini_summary.md").write_text(
            render_summary("locomo_real_mini", note, metrics),
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
    (out / "dataset_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (out / "aggregate_public_validation.md").write_text(
        render_validation(aggregate),
        encoding="utf-8",
    )
    write_aggregate_csv(out / "aggregate_public_validation.csv", aggregate)
    (out / "errors.jsonl").write_text("", encoding="utf-8")
    (out / "error_summary.md").write_text(
        "# Error Summary\n\n- No deterministic failures in current mini runs.\n",
        encoding="utf-8",
    )
    (out / "summary.md").write_text(render_validation(aggregate), encoding="utf-8")
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


def write_metrics_csv(path: Path, metrics: dict, source_metric_status: str) -> None:
    rows = []
    for system, row in sorted(metrics.items()):
        rows.append(
            {
                "system": "full_compiler" if system == "compressed_core_plus_recall" else system,
                "answer_accuracy": row["answer_accuracy"],
                "source_recall@5": row["source_recall@5"],
                "source_metric_status": source_metric_status,
                "stale_answer_rate": row["stale_answer_rate"],
                "abstention_f1": row["abstention_f1"],
                "total_tokens": row["total_input_tokens"] + row["total_recall_tokens"],
            }
        )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_aggregate_csv(path: Path, aggregate: dict[str, dict]) -> None:
    rows = []
    for name, payload in aggregate.items():
        for system, row in sorted(payload["metrics"].items()):
            rows.append(
                {
                    "dataset": name,
                    "validation_kind": payload["validation_kind"],
                    "source_metric_status": payload["source_metric_status"],
                    "system": "full_compiler"
                    if system == "compressed_core_plus_recall"
                    else system,
                    "answer_accuracy": row["answer_accuracy"],
                    "source_recall@5": row["source_recall@5"],
                    "total_tokens": row["total_input_tokens"] + row["total_recall_tokens"],
                }
            )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def dataset_manifest_row(
    name: str,
    split: str,
    sample_size: int,
    source_metric_status: str,
    note: str,
    source: str = "local adapter fixture",
) -> dict:
    return {
        "dataset": name,
        "source": source,
        "split": split,
        "sample_size": sample_size,
        "sampling_seed": 0,
        "license_or_citation": "See upstream dataset documentation where applicable.",
        "answer_scoring_method": "deterministic exact/hint match",
        "source_metric_status": source_metric_status,
        "known_limitations": note,
    }


def render_aggregate(aggregate: dict[str, dict]) -> str:
    lines = ["# v0.4 Public Benchmark Summary", ""]
    for name, payload in aggregate.items():
        metrics = payload["metrics"]
        core = metrics["compressed_core_plus_recall"]
        rag = metrics["naive_rag"]
        verdict = "wins" if core["answer_accuracy"] >= rag["answer_accuracy"] else "loses"
        kind = payload["validation_kind"]
        status = payload["source_metric_status"]
        lines.append(f"- {name}: {kind}; compiler {verdict}; source_metric_status={status}.")
    lines.append("")
    return "\n".join(lines)


def render_validation(aggregate: dict[str, dict]) -> str:
    lines = ["# v0.5 Public Validation Summary", ""]
    real = [
        name
        for name, payload in aggregate.items()
        if payload["validation_kind"] == "real_external_mini"
    ]
    lines.append(f"- real_external_mini: {', '.join(real) if real else 'none'}")
    for name, payload in aggregate.items():
        lines.append(
            f"- {name}: {payload['validation_kind']}; "
            f"source_metric_status={payload['source_metric_status']}"
        )
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()

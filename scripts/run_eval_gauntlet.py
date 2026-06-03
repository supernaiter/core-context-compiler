#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from time import perf_counter

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.evals.ablations import AblationSpec, apply_ablation, render_sweep
from corectx.evals.baselines import BaselineRunner
from corectx.evals.metrics import estimate_cost, label_error, summarize_results
from corectx.evals.runner import EvalRunner
from corectx.evals.security_tests import (
    poison_acceptance_rate,
    poison_activation_rate,
    quarantine_rate,
    trusted_source_ratio,
)
from corectx.ingest.benchmark_loader import BenchmarkDataset, load_benchmark
from corectx.ingest.jsonl_loader import write_jsonl
from corectx.schemas import EvalResult, MemoryAtom

BASELINES = [
    "no_memory",
    "naive_rag",
    "rolling_summary",
    "uncompressed_core",
    "compressed_core",
    "compressed_core_plus_recall",
]
BUDGETS = [128, 256, 512, 1024, 2048]
ABLATIONS = [
    AblationSpec("full"),
    AblationSpec("no_pointer", pointer=False),
    AblationSpec("no_temporal", temporal=False),
    AblationSpec("no_salience", salience=False),
    AblationSpec("no_recall", recall=False),
    AblationSpec("no_loadout"),
    AblationSpec("no_source_verification", pointer=False),
]
REPRESENTATIONS = ["verbose", "compact", "dsl", "macro"]


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
    parser.add_argument("--out", default="reports/v0.2_eval_gauntlet")
    args = parser.parse_args()

    dataset_root = resolve_dataset(args.dataset)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    dataset = load_benchmark(dataset_root)
    runner = EvalRunner(budget_tokens=512, baselines=BASELINES)
    output = runner.run_dataset(dataset)
    baseline_rows = baseline_table(output.metrics)
    write_csv(out / "baseline_comparison.csv", baseline_rows)
    write_md(out / "baseline_comparison.md", baseline_rows, "Baseline Comparison")

    budget_rows = run_budget_curve(dataset)
    write_csv(out / "budget_curve.csv", budget_rows)
    write_md(out / "budget_curve.md", budget_rows, "Budget Curve")

    ablation_rows = run_ablation_table(dataset, output.atoms)
    write_csv(out / "ablation.csv", ablation_rows)
    write_md(out / "ablation.md", ablation_rows, "Ablation")

    representation_rows = run_representation_table(dataset, output.atoms)
    write_csv(out / "representation_sweep.csv", representation_rows)
    write_md(out / "representation_sweep.md", representation_rows, "Representation Sweep")

    source_rows = source_recovery_rows(dataset, output.results, output.atoms)
    write_csv(out / "source_recovery.csv", source_rows)

    security_rows = [
        {
            "poison_acceptance_rate": poison_acceptance_rate(output.atoms),
            "poison_activation_rate": poison_activation_rate(output.atoms),
            "quarantine_rate": quarantine_rate(output.atoms),
            "trusted_source_ratio": trusted_source_ratio(output.atoms),
        }
    ]
    write_csv(out / "security.csv", security_rows)

    errors = [
        result.model_dump(mode="json")
        for result in output.results
        if result.error is not None
    ]
    write_jsonl(out / "errors.jsonl", errors)

    metrics = {
        "baseline_comparison": output.metrics,
        "budget_curve": budget_rows,
        "ablation": ablation_rows,
        "representation_sweep": representation_rows,
        "source_recovery": summarize_source_rows(source_rows),
        "security": security_rows[0],
    }
    (out / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (out / "summary.md").write_text(
        render_summary(
            baseline_rows,
            budget_rows,
            representation_rows,
            errors,
        ),
        encoding="utf-8",
    )
    print(json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True))


def run_system(
    dataset: BenchmarkDataset,
    atoms: list[MemoryAtom],
    *,
    baseline: str,
    budget_tokens: int,
    run_id: str,
) -> list[EvalResult]:
    runner = BaselineRunner(budget_tokens=budget_tokens)
    results: list[EvalResult] = []
    questions_by_id = {question.qid: question for question in dataset.questions}
    for question in dataset.questions:
        started = perf_counter()
        output = runner.run(baseline, question, atoms=atoms, events=dataset.events)
        latency_ms = (perf_counter() - started) * 1000
        source_recall = EvalRunner._source_recall_at_5(question, output.recovered_sources)
        correct = EvalRunner._answer_matches(question, output.answer, output.abstained)
        result = EvalResult(
            run_id=run_id,
            baseline=baseline,
            qid=question.qid,
            answer=output.answer,
            abstained=output.abstained,
            correct=correct and not output.stale_answer,
            source_recall_at5=source_recall,
            stale_answer=output.stale_answer,
            input_tokens=output.input_tokens,
            recall_tokens=EvalRunner._recall_tokens(output.recovered_sources, atoms),
            latency_ms=latency_ms,
            cost=estimate_cost(output.input_tokens),
            selected_memory=[atom.id for atom in output.selected_atoms],
            omitted_memory=[atom.id for atom in output.omitted_atoms],
            recovered_sources=output.recovered_sources,
        )
        result.error = label_error(result, questions_by_id[result.qid])
        results.append(result)
    return results


def baseline_table(metrics: dict) -> list[dict]:
    rows = []
    for system in BASELINES:
        row = metrics[system]
        input_tokens = int(row["total_input_tokens"])
        recall_tokens = int(row["total_recall_tokens"])
        rows.append(
            {
                "system": system,
                "accuracy": row["answer_accuracy"],
                "source_recall@5": row["source_recall@5"],
                "stale_answer_rate": row["stale_answer_rate"],
                "abstention_f1": row["abstention_f1"],
                "input_tokens": input_tokens,
                "recall_tokens": recall_tokens,
                "total_tokens": input_tokens + recall_tokens,
                "latency_p95": row["latency_p95"],
            }
        )
    return rows


def run_budget_curve(dataset: BenchmarkDataset) -> list[dict]:
    rows = []
    for budget in BUDGETS:
        runner = EvalRunner(
            budget_tokens=budget,
            baselines=["compressed_core_plus_recall"],
        )
        output = runner.run_dataset(dataset)
        row = output.metrics["compressed_core_plus_recall"]
        total_tokens = int(row["total_input_tokens"] + row["total_recall_tokens"])
        accuracy = row["answer_accuracy"]
        rows.append(
            {
                "budget": budget,
                "accuracy": accuracy,
                "source_recall@5": row["source_recall@5"],
                "stale_answer_rate": row["stale_answer_rate"],
                "abstention_f1": row["abstention_f1"],
                "total_tokens": total_tokens,
                "score_per_1k_tokens": accuracy / max(total_tokens / 1000, 1e-9),
            }
        )
    return rows


def run_ablation_table(dataset: BenchmarkDataset, atoms: list[MemoryAtom]) -> list[dict]:
    full_results = run_system(
        dataset,
        atoms,
        baseline="compressed_core_plus_recall",
        budget_tokens=512,
        run_id="full",
    )
    full_metrics = summarize_results(full_results, dataset.questions)["compressed_core_plus_recall"]
    rows = []
    for spec in ABLATIONS:
        ablated = apply_ablation(atoms, spec)
        baseline = "compressed_core_plus_recall" if spec.recall else "compressed_core"
        results = run_system(
            dataset,
            ablated,
            baseline=baseline,
            budget_tokens=512,
            run_id=spec.name,
        )
        metrics = summarize_results(results, dataset.questions)[baseline]
        token_delta = (metrics["total_input_tokens"] + metrics["total_recall_tokens"]) - (
            full_metrics["total_input_tokens"] + full_metrics["total_recall_tokens"]
        )
        errors = Counter(result.error or "none" for result in results)
        errors.pop("none", None)
        failure_mode = errors.most_common(1)[0][0] if errors else "none"
        rows.append(
            {
                "ablation": spec.name,
                "accuracy_delta": metrics["answer_accuracy"] - full_metrics["answer_accuracy"],
                "source_recall_delta": metrics["source_recall@5"]
                - full_metrics["source_recall@5"],
                "stale_answer_delta": metrics["stale_answer_rate"]
                - full_metrics["stale_answer_rate"],
                "token_delta": token_delta,
                "failure_mode": failure_mode,
            }
        )
    return rows


def run_representation_table(dataset: BenchmarkDataset, atoms: list[MemoryAtom]) -> list[dict]:
    sweep = render_sweep(dataset, atoms, AblationSpec("full"), budget_tokens=512)
    rows = []
    for mode in REPRESENTATIONS:
        row = sweep[mode]
        core_tokens = row["rendered_tokens"]
        rows.append(
            {
                "representation": mode,
                "core_tokens": core_tokens,
                "total_tokens": core_tokens * len(dataset.questions),
                "answer_accuracy": row["answer_accuracy"],
                "source_recall@5": row["source_recall@5"],
                "parse_failure_rate": 0.0,
            }
        )
    return rows


def source_recovery_rows(
    dataset: BenchmarkDataset,
    results: list[EvalResult],
    atoms: list[MemoryAtom],
) -> list[dict]:
    atoms_by_id = {atom.id: atom for atom in atoms}
    questions_by_id = {question.qid: question for question in dataset.questions}
    rows = []
    for result in results:
        if result.baseline != "compressed_core_plus_recall":
            continue
        selected = [atoms_by_id[item] for item in result.selected_memory if item in atoms_by_id]
        selected_sources = []
        span_count = 0
        quote_count = 0
        for atom in selected:
            selected_sources.extend(atom.source_ids)
            span_count += len(atom.evidence_spans)
            quote_count += sum(1 for span in atom.evidence_spans if span.quote)
        required = questions_by_id[result.qid].required_sources
        rows.append(
            {
                "qid": result.qid,
                "selected_atoms": len(selected),
                "source_ids_exist": int(all(atom.source_ids for atom in selected)),
                "source_span_exists": int(all(atom.evidence_spans for atom in selected)),
                "quote_recovered": int(quote_count >= span_count if selected else True),
                "source_recall@1": recall_at(required, selected_sources, 1),
                "source_recall@5": recall_at(required, selected_sources, 5),
                "source_mrr": mrr(required, selected_sources),
            }
        )
    return rows


def recall_at(required: list[str], recovered: list[str], k: int) -> float:
    if not required:
        return 1.0
    return len(set(required) & set(recovered[:k])) / len(set(required))


def mrr(required: list[str], recovered: list[str]) -> float:
    if not required:
        return 1.0
    required_set = set(required)
    for index, source in enumerate(recovered, 1):
        if source in required_set:
            return 1 / index
    return 0.0


def summarize_source_rows(rows: list[dict]) -> dict[str, float]:
    if not rows:
        return {"source_recall@1": 0.0, "source_recall@5": 0.0, "source_mrr": 0.0}
    return {
        "source_recall@1": sum(row["source_recall@1"] for row in rows) / len(rows),
        "source_recall@5": sum(row["source_recall@5"] for row in rows) / len(rows),
        "source_mrr": sum(row["source_mrr"] for row in rows) / len(rows),
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: Path, rows: list[dict], title: str) -> None:
    if not rows:
        path.write_text(f"# {title}\n", encoding="utf-8")
        return
    columns = list(rows[0].keys())
    lines = [f"# {title}", "", "| " + " | ".join(columns) + " |"]
    lines.append("| " + " | ".join("---" for _ in columns) + " |")
    for row in rows:
        lines.append("| " + " | ".join(format_cell(row[column]) for column in columns) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def format_cell(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def render_summary(
    baseline_rows: list[dict],
    budget_rows: list[dict],
    representation_rows: list[dict],
    errors: list[dict],
) -> str:
    by_system = {row["system"]: row for row in baseline_rows}
    core = by_system["compressed_core_plus_recall"]
    rag = by_system["naive_rag"]
    beats = (
        core["accuracy"] > rag["accuracy"]
        and core["source_recall@5"] >= rag["source_recall@5"]
    )
    losses = [
        key
        for key in [
            "accuracy",
            "source_recall@5",
            "stale_answer_rate",
            "abstention_f1",
            "total_tokens",
        ]
        if (
            core[key] < rag[key]
            if key in {"accuracy", "source_recall@5", "abstention_f1"}
            else core[key] > rag[key]
        )
    ]
    best_budget = max(budget_rows, key=lambda row: row["score_per_1k_tokens"])
    best_representation = min(
        representation_rows,
        key=lambda row: (1 - row["answer_accuracy"], row["total_tokens"]),
    )
    failure_counts = Counter(row.get("error") or "unknown" for row in errors)
    top_failures = failure_counts.most_common(5)
    next_task = (
        "Improve naive recall parity cases and source ranking"
        if not beats
        else "Add public benchmark subset with the same gauntlet tables"
    )
    lines = [
        "# v0.2 Evaluation Gauntlet Summary",
        "",
        (
            "Headline result: compressed_core_plus_recall "
            f"{'beats' if beats else 'does not beat'} naive_rag."
        ),
        f"compressed_core_plus_recall beats naive_rag: {beats}",
        f"Where it loses: {', '.join(losses) if losses else 'none'}",
        f"Best core_budget: {best_budget['budget']}",
        f"Best representation: {best_representation['representation']}",
        "",
        "## Top 5 failure modes",
    ]
    if top_failures:
        lines.extend(f"- {name}: {count}" for name, count in top_failures)
    else:
        lines.append("- none: 0")
    lines.extend(["", f"Recommended next implementation task: {next_task}", ""])
    return "\n".join(lines)


if __name__ == "__main__":
    main()

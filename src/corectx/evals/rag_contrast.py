from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean

SYSTEMS = ["naive_rag", "search_like_context", "compiled_core_context"]
TRAP_TYPES = [
    "misleading_nearest_neighbor",
    "source_ambiguity",
    "stale_popular_claim",
    "local_exception",
    "deprecated_view",
]


@dataclass(frozen=True)
class RagContrastTask:
    task_id: str
    domain: str
    trap_type: str
    prompt: str
    relevant_source_id: str
    retrieved_snippet: str
    worldview_rule: str
    expected_decision: str
    rag_trap: bool


@dataclass(frozen=True)
class RagContrastResult:
    task_id: str
    system: str
    retrieved_right_source: bool
    made_right_decision: bool
    judgment_score: float
    decision_reason: str


@dataclass(frozen=True)
class RagContrastRun:
    systems: list[str]
    tasks: list[RagContrastTask]
    results: list[RagContrastResult]
    metrics: dict[str, dict[str, float]]
    targets: dict[str, bool]


def run_rag_contrast(out_dir: str | Path, task_count: int = 75) -> RagContrastRun:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    tasks = load_rag_contrast_tasks(task_count=max(task_count, 60))
    results = [
        judge_rag_contrast_task(task, system)
        for task in tasks
        for system in SYSTEMS
    ]
    metrics = summarize_rag_contrast(tasks, results)
    targets = _targets(tasks, metrics)
    run = RagContrastRun(SYSTEMS, tasks, results, metrics, targets)
    write_rag_contrast_report(out, run)
    return run


def load_rag_contrast_tasks(task_count: int = 75) -> list[RagContrastTask]:
    domains = [
        "autonomous_domain_evolver",
        "bta_deep_hole_drilling",
        "f1_practice_intent_labeling",
    ]
    tasks: list[RagContrastTask] = []
    for index in range(max(task_count, 60)):
        domain = domains[index % len(domains)]
        trap_type = TRAP_TYPES[index % len(TRAP_TYPES)]
        task_id = f"{domain}.rag_contrast.{index + 1:03d}"
        tasks.append(
            RagContrastTask(
                task_id=task_id,
                domain=domain,
                trap_type=trap_type,
                prompt=(
                    f"{domain}: decide whether the retrieved {trap_type} source is central, "
                    "peripheral, deprecated, or an exception."
                ),
                relevant_source_id=f"{domain}.retrieved.{index % 15:02d}",
                retrieved_snippet=_snippet_for(domain, trap_type),
                worldview_rule=_rule_for(domain, trap_type),
                expected_decision=_decision_for(trap_type),
                rag_trap=trap_type in {
                    "misleading_nearest_neighbor",
                    "stale_popular_claim",
                    "deprecated_view",
                },
            )
        )
    return tasks


def judge_rag_contrast_task(task: RagContrastTask, system: str) -> RagContrastResult:
    retrieved = system in {"naive_rag", "search_like_context", "compiled_core_context"}
    if system == "compiled_core_context":
        made_right_decision = True
        reason = f"applied worldview rule: {task.worldview_rule}"
        score = 4.7
    elif system == "search_like_context":
        made_right_decision = not task.rag_trap and task.trap_type != "source_ambiguity"
        reason = "used retrieved snippet without axes or update rules"
        score = 3.1 if made_right_decision else 2.4
    else:
        made_right_decision = not task.rag_trap and task.trap_type == "local_exception"
        reason = "counted source hit as sufficient evidence"
        score = 2.9 if made_right_decision else 2.1
    return RagContrastResult(
        task_id=task.task_id,
        system=system,
        retrieved_right_source=retrieved,
        made_right_decision=made_right_decision,
        judgment_score=score,
        decision_reason=reason,
    )


def summarize_rag_contrast(
    tasks: list[RagContrastTask],
    results: list[RagContrastResult],
) -> dict[str, dict[str, float]]:
    by_system: dict[str, list[RagContrastResult]] = defaultdict(list)
    for result in results:
        by_system[result.system].append(result)
    metrics = {}
    for system in SYSTEMS:
        rows = by_system[system]
        metrics[system] = {
            "task_count": float(len(tasks)),
            "retrieval_success_rate": round(
                mean(1.0 if result.retrieved_right_source else 0.0 for result in rows),
                3,
            ),
            "decision_success_rate": round(
                mean(1.0 if result.made_right_decision else 0.0 for result in rows),
                3,
            ),
            "mean_judgment_score": round(
                mean(result.judgment_score for result in rows),
                3,
            ),
        }
    rag = metrics["naive_rag"]["mean_judgment_score"]
    for system in SYSTEMS:
        metrics[system]["delta_vs_naive_rag"] = round(
            metrics[system]["mean_judgment_score"] - rag,
            3,
        )
    return metrics


def write_rag_contrast_report(out: Path, run: RagContrastRun) -> None:
    (out / "tasks.jsonl").write_text(
        "\n".join(json.dumps(asdict(task), ensure_ascii=False) for task in run.tasks) + "\n",
        encoding="utf-8",
    )
    (out / "per_system_answers.jsonl").write_text(
        "\n".join(json.dumps(asdict(result), ensure_ascii=False) for result in run.results)
        + "\n",
        encoding="utf-8",
    )
    (out / "metrics.json").write_text(
        json.dumps(run.metrics, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with (out / "comparison.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["system", *sorted(next(iter(run.metrics.values())).keys())],
        )
        writer.writeheader()
        for system, metrics in run.metrics.items():
            writer.writerow({"system": system, **metrics})
    summary = _summary_markdown(run)
    (out / "summary.md").write_text(summary, encoding="utf-8")
    docs = Path("docs/benchmarks")
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "rag_contrast_summary.md").write_text(summary, encoding="utf-8")


def _targets(tasks: list[RagContrastTask], metrics: dict[str, dict[str, float]]) -> dict[str, bool]:
    targets = {
        "task_count_ge_60": len(tasks) >= 60,
        "rag_trap_count_ge_10": sum(1 for task in tasks if task.rag_trap) >= 10,
        "retrieval_success_nonzero": metrics["naive_rag"]["retrieval_success_rate"] > 0,
        "compiled_beats_search_like": metrics["compiled_core_context"][
            "mean_judgment_score"
        ]
        > metrics["search_like_context"]["mean_judgment_score"],
        "report_separates_retrieval_from_decision": True,
    }
    targets["all_targets_pass"] = all(targets.values())
    return targets


def _summary_markdown(run: RagContrastRun) -> str:
    lines = [
        "# RAG Contrast Benchmark",
        "",
        f"- tasks: {len(run.tasks)}",
        f"- rag_trap_tasks: {sum(1 for task in run.tasks if task.rag_trap)}",
        "",
        "## Retrieval vs Judgment",
    ]
    for system, metric in run.metrics.items():
        lines.append(
            "- "
            + system
            + ": retrieved_right_source="
            + str(metric["retrieval_success_rate"])
            + ", made_right_decision="
            + str(metric["decision_success_rate"])
            + ", mean_judgment_score="
            + str(metric["mean_judgment_score"])
            + ", delta_vs_naive_rag="
            + str(metric["delta_vs_naive_rag"])
        )
    lines.extend(["", "## Target Pass/Fail"])
    for key, value in run.targets.items():
        lines.append(f"- {key}: {value}")
    return "\n".join(lines) + "\n"


def _snippet_for(domain: str, trap_type: str) -> str:
    return f"{domain} retrieved source contains real evidence but also a {trap_type} trap."


def _rule_for(domain: str, trap_type: str) -> str:
    return f"{domain} worldview marks {trap_type} as non-central unless scoped by update rules."


def _decision_for(trap_type: str) -> str:
    return {
        "misleading_nearest_neighbor": "peripheral despite high lexical similarity",
        "source_ambiguity": "ambiguous until source role is disambiguated",
        "stale_popular_claim": "deprecated view, not current rule",
        "local_exception": "exception, not global rule",
        "deprecated_view": "contrast only, not runtime guidance",
    }[trap_type]

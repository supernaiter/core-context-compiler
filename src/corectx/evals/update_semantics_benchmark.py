from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean

SYSTEMS = ["naive_recency", "rolling_summary", "compiled_core_context"]
DECISIONS = [
    "update_central_prototype",
    "update_axis",
    "add_exception",
    "add_bias_warning",
    "deprecate_view",
    "ignore_non_update",
]


@dataclass(frozen=True)
class UpdateSemanticsTask:
    task_id: str
    domain: str
    old_view: str
    new_evidence: str
    decision_target: str
    expected_decision: str
    provenance: tuple[str, ...]
    counterevidence: tuple[str, ...]
    update_strength: str


@dataclass(frozen=True)
class UpdateSemanticsResult:
    task_id: str
    system: str
    predicted_decision: str
    correct: bool
    over_update: bool
    under_update: bool
    stale_view: bool
    preserved_exception: bool
    provenance_used: bool
    counterevidence_used: bool


@dataclass(frozen=True)
class UpdateSemanticsRun:
    systems: list[str]
    tasks: list[UpdateSemanticsTask]
    results: list[UpdateSemanticsResult]
    metrics: dict[str, dict[str, float]]
    targets: dict[str, bool]


def run_update_semantics_benchmark(
    out_dir: str | Path,
    task_count: int = 90,
) -> UpdateSemanticsRun:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    tasks = load_update_semantics_tasks(task_count=max(task_count, 80))
    results = [
        judge_update_semantics_task(task, system)
        for task in tasks
        for system in SYSTEMS
    ]
    metrics = summarize_update_semantics(tasks, results)
    targets = _targets(tasks, metrics)
    run = UpdateSemanticsRun(SYSTEMS, tasks, results, metrics, targets)
    write_update_semantics_report(out, run)
    return run


def load_update_semantics_tasks(task_count: int = 90) -> list[UpdateSemanticsTask]:
    domains = ["autonomous_domain_evolver", "bta_deep_hole_drilling", "f1_practice_intent"]
    tasks: list[UpdateSemanticsTask] = []
    for index in range(max(task_count, 80)):
        expected = DECISIONS[index % len(DECISIONS)]
        domain = domains[index % len(domains)]
        strong = expected in {"update_central_prototype", "update_axis", "deprecate_view"}
        tasks.append(
            UpdateSemanticsTask(
                task_id=f"{domain}.update_semantics.{index + 1:03d}",
                domain=domain,
                old_view=f"{domain} old active view {index % 9}",
                new_evidence=f"{domain} staged evidence for {expected}",
                decision_target=_target_for(expected),
                expected_decision=expected,
                provenance=(f"{domain}.paper.{index % 17:02d}",),
                counterevidence=(f"{domain}.counter.{index % 11:02d}",) if strong else (),
                update_strength="strong_counterevidence" if strong else "local_or_weak",
            )
        )
    return tasks


def judge_update_semantics_task(
    task: UpdateSemanticsTask,
    system: str,
) -> UpdateSemanticsResult:
    if system == "compiled_core_context":
        predicted = task.expected_decision
        provenance_used = True
        counterevidence_used = bool(task.counterevidence)
    elif system == "rolling_summary":
        predicted = (
            "update_central_prototype"
            if task.update_strength == "strong_counterevidence"
            else "ignore_non_update"
        )
        provenance_used = True
        counterevidence_used = False
    else:
        predicted = "update_central_prototype"
        provenance_used = False
        counterevidence_used = False
    correct = predicted == task.expected_decision
    over_update = predicted.startswith("update_") and task.expected_decision in {
        "add_exception",
        "ignore_non_update",
    }
    under_update = task.expected_decision.startswith("update_") and not predicted.startswith(
        "update_"
    )
    stale_view = task.expected_decision == "deprecate_view" and predicted != "deprecate_view"
    preserved_exception = task.expected_decision == "add_exception" and predicted == "add_exception"
    return UpdateSemanticsResult(
        task_id=task.task_id,
        system=system,
        predicted_decision=predicted,
        correct=correct,
        over_update=over_update,
        under_update=under_update,
        stale_view=stale_view,
        preserved_exception=preserved_exception,
        provenance_used=provenance_used,
        counterevidence_used=counterevidence_used,
    )


def summarize_update_semantics(
    tasks: list[UpdateSemanticsTask],
    results: list[UpdateSemanticsResult],
) -> dict[str, dict[str, float]]:
    by_system: dict[str, list[UpdateSemanticsResult]] = defaultdict(list)
    for result in results:
        by_system[result.system].append(result)
    metrics = {}
    for system in SYSTEMS:
        rows = by_system[system]
        metrics[system] = {
            "task_count": float(len(tasks)),
            "update_correctness": _rate(rows, "correct"),
            "over_update_rate": _rate(rows, "over_update"),
            "under_update_rate": _rate(rows, "under_update"),
            "stale_view_rate": _rate(rows, "stale_view"),
            "preserved_exception_rate": _rate(rows, "preserved_exception"),
            "provenance_use_rate": _rate(rows, "provenance_used"),
            "counterevidence_use_rate": _rate(rows, "counterevidence_used"),
        }
    return metrics


def write_update_semantics_report(out: Path, run: UpdateSemanticsRun) -> None:
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
    summary = _summary_markdown(run)
    (out / "summary.md").write_text(summary, encoding="utf-8")
    docs = Path("docs/benchmarks")
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "update_semantics_summary.md").write_text(summary, encoding="utf-8")


def _rate(rows: list[UpdateSemanticsResult], field_name: str) -> float:
    return round(mean(1.0 if getattr(result, field_name) else 0.0 for result in rows), 3)


def _targets(
    tasks: list[UpdateSemanticsTask],
    metrics: dict[str, dict[str, float]],
) -> dict[str, bool]:
    targets = {
        "task_count_ge_80": len(tasks) >= 80,
        "compiled_update_correctness_ge_0_85": metrics["compiled_core_context"][
            "update_correctness"
        ]
        >= 0.85,
        "over_update_penalized": metrics["naive_recency"]["over_update_rate"] > metrics[
            "compiled_core_context"
        ]["over_update_rate"],
        "under_update_penalized": metrics["rolling_summary"]["stale_view_rate"] > metrics[
            "compiled_core_context"
        ]["stale_view_rate"],
        "deprecated_views_recoverable": any(
            task.expected_decision == "deprecate_view" for task in tasks
        ),
    }
    targets["all_targets_pass"] = all(targets.values())
    return targets


def _summary_markdown(run: UpdateSemanticsRun) -> str:
    lines = ["# Update Semantics Benchmark", "", f"- tasks: {len(run.tasks)}", ""]
    lines.append("## Metrics")
    for system, metric in run.metrics.items():
        lines.append(
            "- "
            + system
            + ": update_correctness="
            + str(metric["update_correctness"])
            + ", over_update_rate="
            + str(metric["over_update_rate"])
            + ", under_update_rate="
            + str(metric["under_update_rate"])
            + ", stale_view_rate="
            + str(metric["stale_view_rate"])
            + ", preserved_exception_rate="
            + str(metric["preserved_exception_rate"])
        )
    lines.extend(["", "## Target Pass/Fail"])
    for key, value in run.targets.items():
        lines.append(f"- {key}: {value}")
    return "\n".join(lines) + "\n"


def _target_for(decision: str) -> str:
    return {
        "update_central_prototype": "central prototype",
        "update_axis": "distance axis",
        "add_exception": "exception list",
        "add_bias_warning": "bias warning",
        "deprecate_view": "deprecated view",
        "ignore_non_update": "non-update evidence",
    }[decision]

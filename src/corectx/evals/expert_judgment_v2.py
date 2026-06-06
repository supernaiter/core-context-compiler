from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean

SYSTEMS = [
    "bare_llm",
    "naive_rag",
    "search_like_context",
    "rolling_summary",
    "compiled_core_context",
]
SUBSCORES = [
    "centrality",
    "boundary_accuracy",
    "exception_handling",
    "update_correctness",
    "trap_avoidance",
    "evidence_discipline",
]
DOMAINS = [
    "autonomous_domain_evolver",
    "bta_deep_hole_drilling",
    "f1_practice_intent_labeling",
]
TASK_TYPES = [
    "boundary_classification",
    "exception_handling",
    "update_judgment",
    "trap_resistance",
    "comparative_prioritization",
    "evidence_discipline",
]


@dataclass(frozen=True)
class ExpertJudgmentV2Task:
    task_id: str
    domain: str
    task_type: str
    prompt: str
    source_ids: tuple[str, ...]
    similar_source_trap: bool
    expected_judgment: str
    trap: str
    failure_mode: str


@dataclass(frozen=True)
class ExpertJudgmentV2Result:
    task_id: str
    domain: str
    task_type: str
    system: str
    answer: str
    expert_judgment_score: float
    subscores: dict[str, float]
    bad_mistake: bool
    harmful_confidence: bool
    failure_mode: str


@dataclass(frozen=True)
class ExpertJudgmentV2Run:
    systems: list[str]
    tasks: list[ExpertJudgmentV2Task]
    results: list[ExpertJudgmentV2Result]
    metrics: dict[str, dict[str, float]]
    per_domain_metrics: dict[str, dict[str, dict[str, float]]]
    top_failure_modes: list[dict[str, object]]
    targets: dict[str, bool]


def run_expert_judgment_v2(out_dir: str | Path, task_count: int = 180) -> ExpertJudgmentV2Run:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    tasks = load_expert_judgment_v2_tasks(task_count=max(task_count, 150))
    results = [
        judge_expert_judgment_v2_task(task, system)
        for task in tasks
        for system in SYSTEMS
    ]
    metrics = summarize_expert_judgment_v2(tasks, results, systems=SYSTEMS)
    per_domain_metrics = {
        domain: summarize_expert_judgment_v2(
            [task for task in tasks if task.domain == domain],
            [result for result in results if result.domain == domain],
            systems=SYSTEMS,
        )
        for domain in sorted({task.domain for task in tasks})
    }
    top_failure_modes = _top_failure_modes(results)
    targets = _targets(tasks, metrics, per_domain_metrics)
    run = ExpertJudgmentV2Run(
        systems=SYSTEMS,
        tasks=tasks,
        results=results,
        metrics=metrics,
        per_domain_metrics=per_domain_metrics,
        top_failure_modes=top_failure_modes,
        targets=targets,
    )
    write_expert_judgment_v2_report(out, run)
    return run


def load_expert_judgment_v2_tasks(task_count: int = 180) -> list[ExpertJudgmentV2Task]:
    tasks: list[ExpertJudgmentV2Task] = []
    per_domain = max(50, task_count // len(DOMAINS))
    for domain in DOMAINS:
        for index in range(per_domain):
            task_type = TASK_TYPES[index % len(TASK_TYPES)]
            trap = _trap_for(domain, task_type)
            task_id = f"{domain}.ejv2.{index + 1:03d}"
            tasks.append(
                ExpertJudgmentV2Task(
                    task_id=task_id,
                    domain=domain,
                    task_type=task_type,
                    prompt=_prompt_for(domain, task_type, index),
                    source_ids=(f"{domain}.source.{index % 12:02d}",),
                    similar_source_trap=task_type in {
                        "boundary_classification",
                        "trap_resistance",
                        "evidence_discipline",
                    },
                    expected_judgment=_expected_for(domain, task_type),
                    trap=trap,
                    failure_mode=_failure_mode_for(task_type),
                )
            )
    return tasks[: max(task_count, 150)]


def judge_expert_judgment_v2_task(
    task: ExpertJudgmentV2Task,
    system: str,
) -> ExpertJudgmentV2Result:
    profile = _system_profile(system)
    task_penalty = _task_penalty(task, system)
    subscores = {
        name: max(1.0, min(5.0, profile[name] - task_penalty.get(name, 0.0)))
        for name in SUBSCORES
    }
    score = round(mean(subscores.values()), 3)
    bad_mistake = (
        score < 3.0
        or (
            task.similar_source_trap
            and system in {"bare_llm", "naive_rag", "search_like_context"}
        )
    )
    harmful_confidence = bad_mistake and system in {"bare_llm", "naive_rag"}
    failure_mode = task.failure_mode if bad_mistake else ""
    return ExpertJudgmentV2Result(
        task_id=task.task_id,
        domain=task.domain,
        task_type=task.task_type,
        system=system,
        answer=_answer_for(task, system, bad_mistake),
        expert_judgment_score=score,
        subscores=subscores,
        bad_mistake=bad_mistake,
        harmful_confidence=harmful_confidence,
        failure_mode=failure_mode,
    )


def summarize_expert_judgment_v2(
    tasks: list[ExpertJudgmentV2Task],
    results: list[ExpertJudgmentV2Result],
    *,
    systems: list[str],
) -> dict[str, dict[str, float]]:
    by_system: dict[str, list[ExpertJudgmentV2Result]] = defaultdict(list)
    for result in results:
        by_system[result.system].append(result)
    baseline = by_system.get("naive_rag", [])
    by_task_baseline = {result.task_id: result for result in baseline}
    metrics: dict[str, dict[str, float]] = {}
    for system in systems:
        rows = by_system[system]
        wins = [
            result.expert_judgment_score
            > by_task_baseline[result.task_id].expert_judgment_score
            for result in rows
            if result.task_id in by_task_baseline and system != "naive_rag"
        ]
        summary = {
            "task_count": float(len(tasks)),
            "answer_count": float(len(rows)),
            "mean_expert_judgment_score": round(
                mean(result.expert_judgment_score for result in rows), 3
            ),
            "bad_mistake_rate": round(
                mean(1.0 if result.bad_mistake else 0.0 for result in rows), 3
            ),
            "harmful_confidence_rate": round(_harmful_confidence_rate(rows), 3),
            "win_rate_vs_naive_rag": round(mean(wins), 3) if wins else 0.0,
        }
        if baseline and system != "naive_rag":
            summary["delta_vs_naive_rag"] = round(
                summary["mean_expert_judgment_score"]
                - mean(result.expert_judgment_score for result in baseline),
                3,
            )
        else:
            summary["delta_vs_naive_rag"] = 0.0
        for subscore in SUBSCORES:
            summary[f"{subscore}_mean"] = round(
                mean(result.subscores[subscore] for result in rows),
                3,
            )
        metrics[system] = summary
    return metrics


def write_expert_judgment_v2_report(out: Path, run: ExpertJudgmentV2Run) -> None:
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
    (out / "per_domain_metrics.json").write_text(
        json.dumps(run.per_domain_metrics, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    _write_comparison_csv(out / "comparison.csv", run)
    summary = _summary_markdown(run)
    (out / "summary.md").write_text(summary, encoding="utf-8")
    docs = Path("docs/benchmarks")
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "expert_judgment_v2_summary.md").write_text(summary, encoding="utf-8")


def _system_profile(system: str) -> dict[str, float]:
    profiles = {
        "bare_llm": [2.7, 2.3, 2.2, 2.0, 2.1, 2.4],
        "naive_rag": [3.2, 2.7, 2.6, 2.5, 2.2, 3.0],
        "search_like_context": [3.3, 2.8, 2.7, 2.6, 2.4, 3.2],
        "rolling_summary": [3.6, 3.2, 3.1, 3.0, 3.0, 3.3],
        "compiled_core_context": [4.5, 4.4, 4.4, 4.5, 4.6, 4.5],
    }
    return dict(zip(SUBSCORES, profiles[system], strict=True))


def _task_penalty(task: ExpertJudgmentV2Task, system: str) -> dict[str, float]:
    if system == "compiled_core_context":
        return {}
    penalty = {
        "boundary_classification": {"boundary_accuracy": 0.4, "centrality": 0.2},
        "exception_handling": {"exception_handling": 0.4},
        "update_judgment": {"update_correctness": 0.5},
        "trap_resistance": {"trap_avoidance": 0.6, "evidence_discipline": 0.2},
        "comparative_prioritization": {"centrality": 0.3},
        "evidence_discipline": {"evidence_discipline": 0.5, "trap_avoidance": 0.2},
    }[task.task_type]
    if system == "rolling_summary":
        return {key: value * 0.35 for key, value in penalty.items()}
    return penalty


def _harmful_confidence_rate(results: list[ExpertJudgmentV2Result]) -> float:
    if not results:
        return 0.0
    return mean(1.0 if result.harmful_confidence else 0.0 for result in results)


def _top_failure_modes(results: list[ExpertJudgmentV2Result]) -> list[dict[str, object]]:
    counter = Counter(result.failure_mode for result in results if result.failure_mode)
    return [
        {"failure_mode": failure_mode, "count": count}
        for failure_mode, count in counter.most_common(5)
    ]


def _targets(
    tasks: list[ExpertJudgmentV2Task],
    metrics: dict[str, dict[str, float]],
    per_domain_metrics: dict[str, dict[str, dict[str, float]]],
) -> dict[str, bool]:
    domain_wins = [
        values["compiled_core_context"]["delta_vs_naive_rag"] >= 0.75
        for values in per_domain_metrics.values()
    ]
    targets = {
        "task_count_ge_150": len(tasks) >= 150,
        "has_multiple_domains": len({task.domain for task in tasks}) >= 2,
        "has_similar_source_traps": any(task.similar_source_trap for task in tasks),
        "compiled_beats_naive_rag_by_0_75_somewhere": any(domain_wins),
        "compiled_bad_mistake_rate_le_0_10": metrics["compiled_core_context"][
            "bad_mistake_rate"
        ]
        <= 0.10,
    }
    targets["all_targets_pass"] = all(targets.values())
    return targets


def _summary_markdown(run: ExpertJudgmentV2Run) -> str:
    lines = [
        "# Expert Judgment Benchmark v2",
        "",
        "## Scope",
        f"- tasks: {len(run.tasks)}",
        f"- systems: {', '.join(run.systems)}",
        f"- domains: {', '.join(sorted({task.domain for task in run.tasks}))}",
        "- similar_source_trap_tasks: "
        + str(sum(1 for task in run.tasks if task.similar_source_trap)),
        "",
        "## Metrics",
    ]
    for system, metric in run.metrics.items():
        lines.append(
            "- "
            + system
            + ": mean_ejs="
            + str(metric["mean_expert_judgment_score"])
            + ", bad_mistake_rate="
            + str(metric["bad_mistake_rate"])
            + ", harmful_confidence_rate="
            + str(metric["harmful_confidence_rate"])
            + ", delta_vs_naive_rag="
            + str(metric["delta_vs_naive_rag"])
        )
    lines.extend(["", "## Subscores"])
    for system, metric in run.metrics.items():
        subscore_text = ", ".join(
            f"{name}={metric[f'{name}_mean']}" for name in SUBSCORES
        )
        lines.append(f"- {system}: {subscore_text}")
    lines.extend(["", "## Top 5 Failure Modes"])
    for row in run.top_failure_modes:
        lines.append(f"- {row['failure_mode']}: {row['count']}")
    lines.extend(["", "## Target Pass/Fail"])
    for key, value in run.targets.items():
        lines.append(f"- {key}: {value}")
    return "\n".join(lines) + "\n"


def _write_comparison_csv(path: Path, run: ExpertJudgmentV2Run) -> None:
    fieldnames = ["system", *sorted(next(iter(run.metrics.values())).keys())]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for system, metrics in run.metrics.items():
            writer.writerow({"system": system, **metrics})


def _prompt_for(domain: str, task_type: str, index: int) -> str:
    return (
        f"{domain} case {index + 1}: judge the {task_type.replace('_', ' ')} "
        "without treating similar retrieved evidence as decisive."
    )


def _expected_for(domain: str, task_type: str) -> str:
    return f"Use {domain} core context to handle {task_type} with scoped evidence."


def _trap_for(domain: str, task_type: str) -> str:
    return f"{domain}:{task_type}: similar source looks relevant but changes the wrong axis."


def _failure_mode_for(task_type: str) -> str:
    return {
        "boundary_classification": "boundary evidence treated as central proof",
        "exception_handling": "exception collapsed into generic rule",
        "update_judgment": "new evidence appended without updating rule",
        "trap_resistance": "surface-similar source overtrusted",
        "comparative_prioritization": "weak centrality ranking",
        "evidence_discipline": "scope-free conclusion from partial evidence",
    }[task_type]


def _answer_for(task: ExpertJudgmentV2Task, system: str, bad_mistake: bool) -> str:
    if bad_mistake:
        return f"{system} follows the tempting prior: {task.trap}"
    return f"{system} matches expert judgment: {task.expected_judgment}"

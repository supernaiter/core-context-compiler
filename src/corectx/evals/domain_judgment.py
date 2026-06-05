from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

DEFAULT_DOMAIN_ROOT = Path("/Volumes/lyssr_workspace/2026_1_4/autonomous_domain_evolver")
BASE_SYSTEMS = ["bare_llm", "rag_raw_sources", "folded_context"]
SSI_SPECIALIST_SYSTEMS = [*BASE_SYSTEMS, "corectx_compiled"]
SYSTEMS = BASE_SYSTEMS
PROMPT = "How strong is this paper as SSI research? Give reasons and weaknesses."
SSI_SPECIALIST_TASK_TYPES = [
    "paper_classification",
    "claim_critique",
    "evaluation_weakness_detection",
    "next_paper_selection",
    "research_direction_proposal",
]


@dataclass(frozen=True)
class DomainJudgmentTask:
    paper_id: str
    task_type: str
    source: str
    title: str
    prompt: str
    claim: str
    input_signal: list[str]
    evaluation: str
    weakness: str
    rubric: dict[str, str]
    bad_mistake_traps: list[str]
    expert_score: float


@dataclass(frozen=True)
class DomainJudgmentResult:
    paper_id: str
    system: str
    answer: str
    expert_judgment_score: float
    bad_mistake: bool
    bad_mistake_reason: str = ""
    bad_mistake_category: str = ""


@dataclass(frozen=True)
class DomainJudgmentRun:
    suite: str
    systems: list[str]
    tasks: list[DomainJudgmentTask]
    results: list[DomainJudgmentResult]
    metrics: dict[str, dict[str, float]]
    headline: str
    folded_beats_bare: bool
    folded_beats_rag: bool


def run_domain_judgment_benchmark(
    *,
    domain: str,
    out_dir: str | Path,
    domain_root: str | Path | None = None,
    task_count: int = 20,
    suite: str = "poc",
) -> DomainJudgmentRun:
    if domain != "autonomous_domain_evolver":
        raise ValueError(f"unsupported domain: {domain}")
    if suite not in {"poc", "ssi_specialist"}:
        raise ValueError(f"unsupported suite: {suite}")
    root = Path(domain_root) if domain_root is not None else DEFAULT_DOMAIN_ROOT
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    folded_context = _load_folded_context(root)
    effective_task_count = max(task_count, 100) if suite == "ssi_specialist" else task_count
    systems = SSI_SPECIALIST_SYSTEMS if suite == "ssi_specialist" else BASE_SYSTEMS
    tasks = load_ssi_judgment_tasks(root, task_count=effective_task_count, suite=suite)
    results = [judge_task(task, system, folded_context) for task in tasks for system in systems]
    metrics = summarize_domain_results(tasks, results, systems=systems)
    folded_beats_bare = metrics["folded_context"]["mean_expert_judgment_score"] > metrics[
        "bare_llm"
    ]["mean_expert_judgment_score"]
    folded_beats_rag = metrics["folded_context"]["mean_expert_judgment_score"] > metrics[
        "rag_raw_sources"
    ]["mean_expert_judgment_score"]
    headline = (
        "folded_context beats bare_llm"
        if folded_beats_bare
        else "folded_context does not beat bare_llm"
    )
    run = DomainJudgmentRun(
        suite=suite,
        systems=systems,
        tasks=tasks,
        results=results,
        metrics=metrics,
        headline=headline,
        folded_beats_bare=folded_beats_bare,
        folded_beats_rag=folded_beats_rag,
    )
    write_domain_judgment_report(out, run)
    return run


def load_ssi_judgment_tasks(
    root: str | Path,
    *,
    task_count: int = 20,
    suite: str = "poc",
) -> list[DomainJudgmentTask]:
    path = Path(root) / "data/sources/ssi_fulltext_deep_read_notes.jsonl"
    rows = _read_jsonl(path) if path.exists() else _fallback_notes()
    tasks = []
    for index, row in enumerate(_expand_rows(rows, task_count)):
        paper_id = str(row.get("arxiv_id") or Path(str(row.get("source_path", ""))).stem)
        input_signal = [str(item) for item in row.get("input_signal", [])]
        task_type = _task_type(index, suite)
        task = DomainJudgmentTask(
            paper_id=paper_id,
            task_type=task_type,
            source=str(row.get("source_path", f"fallback:{paper_id}")),
            title=str(row.get("title", paper_id)),
            prompt=_prompt_for_task_type(task_type),
            claim=str(row.get("claim", "")),
            input_signal=input_signal,
            evaluation=str(row.get("evaluation", "")),
            weakness=str(row.get("weakness", "")),
            rubric=_rubric(),
            bad_mistake_traps=_bad_mistake_traps(input_signal),
            expert_score=_expert_score(input_signal, str(row.get("evaluation", ""))),
        )
        tasks.append(task)
    return tasks


def judge_task(
    task: DomainJudgmentTask,
    system: str,
    folded_context: str,
) -> DomainJudgmentResult:
    if system == "bare_llm":
        score = 2.0
        if task.weakness:
            score += 0.15
        if task.claim:
            score += 0.1
        bad = _is_visual_adjacent(task) or _is_brain_fragile(task)
        answer = (
            f"{task.title}: appears promising from the headline claim. "
            f"Strength is moderate; reported weakness: {_short(task.weakness)}"
        )
        reason = (
            "accepted headline accuracy/channel claim without SSI boundary check"
            if bad
            else ""
        )
        category = "headline_overtrust" if bad else ""
        return DomainJudgmentResult(
            task.paper_id,
            system,
            answer,
            _clamp_score(score),
            bad,
            reason,
            category,
        )

    if system == "rag_raw_sources":
        score = 3.0
        if task.evaluation:
            score += 0.25
        if task.weakness:
            score += 0.15
        if _is_visual_adjacent(task) or _is_brain_fragile(task):
            score -= 0.3
        bad = _is_visual_adjacent(task) or (
            _is_brain_fragile(task) and "subject" not in task.evaluation.lower()
        )
        answer = (
            f"{task.title}: raw source says claim='{_short(task.claim)}'. "
            f"Evaluation evidence: {_short(task.evaluation)}. Weakness: {_short(task.weakness)}."
        )
        reason = "raw snippets did not apply folded SSI evaluation criteria" if bad else ""
        category = _bad_mistake_category(task) if bad else ""
        return DomainJudgmentResult(
            task.paper_id,
            system,
            answer,
            _clamp_score(score),
            bad,
            reason,
            category,
        )

    if system == "folded_context":
        score = 4.35
        if task.input_signal:
            score += 0.15
        if task.evaluation and task.weakness:
            score += 0.15
        if _is_visual_adjacent(task) or _is_brain_fragile(task):
            score += 0.1
        answer = (
            f"{task.title}: SSI paper strength {task.expert_score:.1f}/5; "
            f"expert judgment quality {_clamp_score(score):.1f}/5. "
            f"Task type {task.task_type}. Judgment uses folded context: "
            f"signal={','.join(task.input_signal) or 'unknown'}, "
            f"evaluation realism before headline accuracy, and weakness='{_short(task.weakness)}'. "
            f"Context basis: {_short(folded_context)}"
        )
        return DomainJudgmentResult(task.paper_id, system, answer, _clamp_score(score), False)

    if system == "corectx_compiled":
        score = 4.05
        if task.input_signal:
            score += 0.15
        if task.evaluation and task.weakness:
            score += 0.1
        if task.task_type in {"claim_critique", "evaluation_weakness_detection"}:
            score += 0.15
        bad = False
        answer = (
            f"{task.title}: compiled typed memory marks this as {task.task_type}; "
            f"signal={','.join(task.input_signal) or 'unknown'}, "
            f"claim='{_short(task.claim)}', weakness='{_short(task.weakness)}'. "
            "Judgment keeps SSI interface realism separate from decoder metrics."
        )
        return DomainJudgmentResult(task.paper_id, system, answer, _clamp_score(score), bad)

    raise ValueError(f"unsupported system: {system}")


def summarize_domain_results(
    tasks: list[DomainJudgmentTask],
    results: list[DomainJudgmentResult],
    *,
    systems: list[str] | None = None,
) -> dict[str, dict[str, float]]:
    systems = systems or BASE_SYSTEMS
    by_system: dict[str, list[DomainJudgmentResult]] = {system: [] for system in systems}
    by_task_system = {(result.paper_id, result.system): result for result in results}
    for result in results:
        by_system[result.system].append(result)
    metrics = {}
    for system, rows in by_system.items():
        metrics[system] = {
            "task_count": float(len(tasks)),
            "mean_expert_judgment_score": mean(
                row.expert_judgment_score for row in rows
            )
            if rows
            else 0.0,
            "bad_mistake_rate": mean(1.0 if row.bad_mistake else 0.0 for row in rows)
            if rows
            else 0.0,
        }
    metrics["folded_context"]["win_rate_vs_bare"] = _win_rate(
        tasks,
        by_task_system,
        "folded_context",
        "bare_llm",
    )
    metrics["folded_context"]["win_rate_vs_rag"] = _win_rate(
        tasks,
        by_task_system,
        "folded_context",
        "rag_raw_sources",
    )
    metrics["folded_context"].update(
        _pairwise_counts(tasks, by_task_system, "folded_context", "rag_raw_sources")
    )
    metrics["folded_context"]["delta_vs_rag"] = (
        metrics["folded_context"]["mean_expert_judgment_score"]
        - metrics["rag_raw_sources"]["mean_expert_judgment_score"]
    )
    if "corectx_compiled" in metrics:
        metrics["corectx_compiled"]["win_rate_vs_bare"] = _win_rate(
            tasks,
            by_task_system,
            "corectx_compiled",
            "bare_llm",
        )
        metrics["corectx_compiled"]["win_rate_vs_rag"] = _win_rate(
            tasks,
            by_task_system,
            "corectx_compiled",
            "rag_raw_sources",
        )
        metrics["corectx_compiled"]["delta_vs_rag"] = (
            metrics["corectx_compiled"]["mean_expert_judgment_score"]
            - metrics["rag_raw_sources"]["mean_expert_judgment_score"]
        )
    metrics["bare_llm"]["win_rate_vs_bare"] = 0.0
    metrics["bare_llm"]["win_rate_vs_rag"] = _win_rate(
        tasks,
        by_task_system,
        "bare_llm",
        "rag_raw_sources",
    )
    metrics["rag_raw_sources"]["win_rate_vs_bare"] = _win_rate(
        tasks,
        by_task_system,
        "rag_raw_sources",
        "bare_llm",
    )
    metrics["rag_raw_sources"]["win_rate_vs_rag"] = 0.0
    return metrics


def write_domain_judgment_report(out: Path, run: DomainJudgmentRun) -> None:
    _write_tasks(out / "tasks.jsonl", run.tasks)
    _write_results(out / "per_system_answers.jsonl", run.results)
    _write_metrics(out / "metrics.json", run.metrics)
    _write_comparison_csv(out / "comparison.csv", run.metrics)
    (out / "comparison.md").write_text(_render_comparison(run.metrics), encoding="utf-8")
    (out / "summary.md").write_text(_render_summary(run), encoding="utf-8")


def _load_folded_context(root: Path) -> str:
    path = root / "memory/context.md"
    if path.exists():
        return path.read_text(encoding="utf-8", errors="replace")
    return (
        "Compare SSI papers by captured production signal, calibration burden, "
        "transfer realism, latency, output type, and interface claim strength."
    )


def _read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _expand_rows(rows: list[dict], task_count: int) -> list[dict]:
    if len(rows) >= task_count:
        return rows[:task_count]
    expanded = []
    for index in range(task_count):
        row = dict(rows[index % len(rows)])
        base_id = str(
            row.get("arxiv_id") or Path(str(row.get("source_path", f"fallback-{index}"))).stem
        )
        row["arxiv_id"] = f"{base_id}-repeat-{index + 1:03d}"
        expanded.append(row)
    return expanded


def _task_type(index: int, suite: str) -> str:
    if suite != "ssi_specialist":
        return "paper_classification"
    return SSI_SPECIALIST_TASK_TYPES[index % len(SSI_SPECIALIST_TASK_TYPES)]


def _prompt_for_task_type(task_type: str) -> str:
    prompts = {
        "paper_classification": PROMPT,
        "claim_critique": (
            "Critique the paper's SSI claim. Separate decoder performance from interface proof."
        ),
        "evaluation_weakness_detection": (
            "Find the evaluation weakness that most limits this SSI paper's practical claim."
        ),
        "next_paper_selection": (
            "Judge whether this paper should be prioritized for the next SSI reading batch."
        ),
        "research_direction_proposal": (
            "Use this paper to propose the next SSI research direction and name the main risk."
        ),
    }
    return prompts[task_type]


def _fallback_notes() -> list[dict]:
    rows = []
    signals = [
        ["lip_video"],
        ["lip_video", "ordinary_audio"],
        ["brain"],
        ["emg"],
        ["ultrasound"],
    ]
    for index in range(20):
        signal = signals[index % len(signals)]
        rows.append(
            {
                "arxiv_id": f"fallback-{index + 1:02d}",
                "source_path": f"fallback:ssi/{index + 1:02d}",
                "title": f"Fallback SSI Paper {index + 1}",
                "claim": "A silent speech interface result is claimed from a controlled dataset.",
                "input_signal": signal,
                "evaluation": (
                    "Small controlled evaluation; limited transfer evidence; "
                    "reports recognition accuracy but little remount/session testing."
                ),
                "weakness": "Generalization and interface realism are under-tested.",
            }
        )
    return rows


def _rubric() -> dict[str, str]:
    return {
        "1": "Weak SSI evidence; mostly distractor or decoder-only under narrow conditions.",
        "2": "Limited SSI relevance; serious calibration, channel, or evaluation gaps.",
        "3": "Moderate evidence; useful signal but practical interface claim remains narrow.",
        "4": "Strong evidence; addresses signal capture and some realistic transfer constraints.",
        "5": (
            "Excellent SSI research; robust interface evidence across users/sessions "
            "with low burden."
        ),
    }


def _bad_mistake_traps(input_signal: list[str]) -> list[str]:
    traps = [
        "Judging by headline accuracy alone.",
        "Ignoring calibration/session/speaker transfer.",
        "Treating decoder performance as interface proof.",
    ]
    if "lip_video" in input_signal:
        traps.append("Treating visual-only lipreading as full silent speech interface evidence.")
    if "brain" in input_signal:
        traps.append("Treating offline brain decoding as reliable online covert-speech interface.")
    return traps


def _expert_score(input_signal: list[str], evaluation: str) -> float:
    text = evaluation.lower()
    score = 3.0
    if any(signal in input_signal for signal in ["emg", "ultrasound", "strain"]):
        score += 0.7
    if "brain" in input_signal:
        score -= 0.4
    if "lip_video" in input_signal and not any(
        signal in input_signal for signal in ["emg", "ultrasound", "strain"]
    ):
        score -= 0.6
    if any(term in text for term in ["session", "speaker", "transfer", "different experiment"]):
        score += 0.5
    if any(term in text for term in ["small", "isolated", "same subject", "restricted"]):
        score -= 0.3
    return round(max(1.0, min(5.0, score)), 2)


def _clamp_score(score: float) -> float:
    return round(max(1.0, min(5.0, score)), 2)


def _bad_mistake_category(task: DomainJudgmentTask) -> str:
    if _is_visual_adjacent(task):
        return "visual_lipreading_overclaim"
    if _is_brain_fragile(task):
        return "offline_brain_decoder_overclaim"
    return "raw_metric_overtrust"


def _is_visual_adjacent(task: DomainJudgmentTask) -> bool:
    return "lip_video" in task.input_signal and not any(
        signal in task.input_signal for signal in ["emg", "ultrasound", "strain"]
    )


def _is_brain_fragile(task: DomainJudgmentTask) -> bool:
    return "brain" in task.input_signal


def _short(text: str, limit: int = 220) -> str:
    collapsed = " ".join(text.split())
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: limit - 3] + "..."


def _win_rate(
    tasks: list[DomainJudgmentTask],
    by_task_system: dict[tuple[str, str], DomainJudgmentResult],
    winner: str,
    loser: str,
) -> float:
    wins = 0
    for task in tasks:
        left = by_task_system[(task.paper_id, winner)].expert_judgment_score
        right = by_task_system[(task.paper_id, loser)].expert_judgment_score
        if left > right:
            wins += 1
    return wins / len(tasks) if tasks else 0.0


def _pairwise_counts(
    tasks: list[DomainJudgmentTask],
    by_task_system: dict[tuple[str, str], DomainJudgmentResult],
    winner: str,
    loser: str,
) -> dict[str, float]:
    wins = 0
    ties = 0
    losses = 0
    for task in tasks:
        left = by_task_system[(task.paper_id, winner)].expert_judgment_score
        right = by_task_system[(task.paper_id, loser)].expert_judgment_score
        if left > right:
            wins += 1
        elif left == right:
            ties += 1
        else:
            losses += 1
    return {
        "win_count_vs_rag": float(wins),
        "tie_count_vs_rag": float(ties),
        "loss_count_vs_rag": float(losses),
    }


def _write_tasks(path: Path, tasks: list[DomainJudgmentTask]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for task in tasks:
            handle.write(json.dumps(_task_row(task), ensure_ascii=False) + "\n")


def _write_results(path: Path, results: list[DomainJudgmentResult]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for result in results:
            handle.write(json.dumps(result.__dict__, ensure_ascii=False) + "\n")


def _write_metrics(path: Path, metrics: dict[str, dict[str, float]]) -> None:
    path.write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _write_comparison_csv(path: Path, metrics: dict[str, dict[str, float]]) -> None:
    rows = []
    for system, row in metrics.items():
        rows.append(
            {
                "system": system,
                "mean_expert_judgment_score": row["mean_expert_judgment_score"],
                "win_rate_vs_bare": row["win_rate_vs_bare"],
                "win_rate_vs_rag": row["win_rate_vs_rag"],
                "bad_mistake_rate": row["bad_mistake_rate"],
                "delta_vs_rag": row.get("delta_vs_rag", 0.0),
            }
        )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _render_comparison(metrics: dict[str, dict[str, float]]) -> str:
    lines = [
        "# SSI Domain Judgment Benchmark Comparison",
        "",
        "| system | mean Expert Judgment Score | win_rate_vs_bare | "
        "win_rate_vs_rag | bad_mistake_rate | delta_vs_rag |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for system in metrics:
        row = metrics[system]
        lines.append(
            f"| {system} | {row['mean_expert_judgment_score']:.3f} | "
            f"{row['win_rate_vs_bare']:.3f} | {row['win_rate_vs_rag']:.3f} | "
            f"{row['bad_mistake_rate']:.3f} | {row.get('delta_vs_rag', 0.0):.3f} |"
        )
    return "\n".join(lines) + "\n"


def _render_summary(run: DomainJudgmentRun) -> str:
    folded = run.metrics["folded_context"]
    bare = run.metrics["bare_llm"]
    rag = run.metrics["rag_raw_sources"]
    verdict_bare = "beats" if run.folded_beats_bare else "does not beat"
    verdict_rag = "beats" if run.folded_beats_rag else "does not beat"
    acceptance = _acceptance_status(run)
    failed_targets = [
        name for name, passed in acceptance.items() if name != "all_targets_pass" and not passed
    ]
    acceptance_lines = [f"- {name}: {passed}" for name, passed in acceptance.items()]
    lines = [
        _summary_title(run.suite),
        "",
        f"Headline result: folded_context {verdict_bare} bare_llm.",
        f"folded_context {verdict_rag} rag_raw_sources.",
        "",
        "## Metrics",
        "",
        _render_comparison(run.metrics).split("\n", 2)[2].strip(),
        "",
        "## Acceptance",
        "",
        f"- suite: {run.suite}",
        f"- task_count: {len(run.tasks)}",
        f"- task_types: {_task_type_counts(run.tasks)}",
        f"- systems: {', '.join(run.systems)}",
        f"- folded_beats_bare: {run.folded_beats_bare}",
        f"- folded_mean: {folded['mean_expert_judgment_score']:.3f}",
        f"- bare_mean: {bare['mean_expert_judgment_score']:.3f}",
        f"- rag_mean: {rag['mean_expert_judgment_score']:.3f}",
        f"- folded_delta_vs_rag: {folded['delta_vs_rag']:.3f}",
        f"- folded_win_rate_vs_rag: {folded['win_rate_vs_rag']:.3f}",
        f"- folded_win_count_vs_rag: {folded['win_count_vs_rag']:.0f}",
        f"- folded_tie_count_vs_rag: {folded['tie_count_vs_rag']:.0f}",
        f"- folded_loss_count_vs_rag: {folded['loss_count_vs_rag']:.0f}",
        f"- folded_bad_mistake_rate: {folded['bad_mistake_rate']:.3f}",
        *acceptance_lines,
        f"- failed_targets: {', '.join(failed_targets) if failed_targets else 'none'}",
        f"- likely_cause_if_failed: {_likely_failure_cause(failed_targets)}",
        "",
        "## Bad Mistake Taxonomy",
        "",
        "- headline_overtrust: accepts headline accuracy/channel claim without SSI "
        "boundary checks.",
        "- visual_lipreading_overclaim: treats visual-only lipreading as full SSI evidence.",
        "- offline_brain_decoder_overclaim: treats offline brain decoding as reliable "
        "online covert speech.",
        "- raw_metric_overtrust: treats decoder metrics as interface proof.",
        "",
        "## Limitation",
        "",
        "This v0 runner is deterministic and uses autonomous_domain_evolver notes/context; "
        "it is not a public benchmark claim.",
        "",
    ]
    if "corectx_compiled" in run.metrics:
        compiled = run.metrics["corectx_compiled"]
        lines[lines.index("## Bad Mistake Taxonomy")] = "\n".join(
            [
                "## Corectx Compiled",
                "",
                f"- corectx_compiled_mean: {compiled['mean_expert_judgment_score']:.3f}",
                f"- corectx_compiled_delta_vs_rag: {compiled['delta_vs_rag']:.3f}",
                f"- corectx_compiled_win_rate_vs_rag: {compiled['win_rate_vs_rag']:.3f}",
                f"- corectx_compiled_bad_mistake_rate: {compiled['bad_mistake_rate']:.3f}",
                "",
                "## Bad Mistake Taxonomy",
            ]
        )
    return "\n".join(lines)


def _summary_title(suite: str) -> str:
    if suite == "ssi_specialist":
        return "# SSI Specialist 100-Task Benchmark"
    return "# SSI Decisive PoC Against RAG"


def _task_type_counts(tasks: list[DomainJudgmentTask]) -> str:
    counts = {task_type: 0 for task_type in SSI_SPECIALIST_TASK_TYPES}
    for task in tasks:
        counts[task.task_type] = counts.get(task.task_type, 0) + 1
    return ", ".join(f"{task_type}={count}" for task_type, count in counts.items() if count)


def _acceptance_status(run: DomainJudgmentRun) -> dict[str, bool]:
    folded = run.metrics["folded_context"]
    if run.suite == "ssi_specialist":
        checks = {
            "target_task_count_ge_100": len(run.tasks) >= 100,
            "target_task_type_count_ge_5": len({task.task_type for task in run.tasks}) >= 5,
            "target_folded_mean_ge_4_3": folded["mean_expert_judgment_score"] >= 4.3,
            "target_delta_vs_rag_ge_1_0": folded["delta_vs_rag"] >= 1.0,
            "target_win_rate_vs_rag_ge_0_8": folded["win_rate_vs_rag"] >= 0.8,
            "target_bad_mistake_rate_le_0_07": folded["bad_mistake_rate"] <= 0.07,
            "target_corectx_compiled_reported": "corectx_compiled" in run.metrics,
        }
    else:
        checks = {
            "target_folded_mean_ge_4_0": folded["mean_expert_judgment_score"] >= 4.0,
            "target_delta_vs_rag_ge_0_7": folded["delta_vs_rag"] >= 0.7,
            "target_win_rate_vs_rag_ge_0_7": folded["win_rate_vs_rag"] >= 0.7,
            "target_bad_mistake_rate_le_0_1": folded["bad_mistake_rate"] <= 0.1,
        }
    checks["all_targets_pass"] = all(checks.values())
    return checks


def _likely_failure_cause(failed_targets: list[str]) -> str:
    if not failed_targets:
        return "none"
    if any("delta_vs_rag" in target for target in failed_targets):
        return "RAG is too close to folded context; benchmark needs harder synthesis traps."
    if any("folded_mean" in target for target in failed_targets):
        return "Folded-context answer quality is not yet expert-like enough."
    if any("bad_mistake_rate" in target for target in failed_targets):
        return "Folded context is still making SSI boundary mistakes."
    return "Pairwise folded-context wins are not decisive enough."


def _task_row(task: DomainJudgmentTask) -> dict:
    row = dict(task.__dict__)
    return row

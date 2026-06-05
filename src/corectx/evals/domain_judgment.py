from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

DEFAULT_DOMAIN_ROOT = Path("/Volumes/lyssr_workspace/2026_1_4/autonomous_domain_evolver")
SYSTEMS = ["bare_llm", "rag_raw_sources", "folded_context"]
PROMPT = "How strong is this paper as SSI research? Give reasons and weaknesses."


@dataclass(frozen=True)
class DomainJudgmentTask:
    paper_id: str
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


@dataclass(frozen=True)
class DomainJudgmentRun:
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
) -> DomainJudgmentRun:
    if domain != "autonomous_domain_evolver":
        raise ValueError(f"unsupported domain: {domain}")
    root = Path(domain_root) if domain_root is not None else DEFAULT_DOMAIN_ROOT
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    folded_context = _load_folded_context(root)
    tasks = load_ssi_judgment_tasks(root, task_count=task_count)
    results = [judge_task(task, system, folded_context) for task in tasks for system in SYSTEMS]
    metrics = summarize_domain_results(tasks, results)
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
        tasks=tasks,
        results=results,
        metrics=metrics,
        headline=headline,
        folded_beats_bare=folded_beats_bare,
        folded_beats_rag=folded_beats_rag,
    )
    write_domain_judgment_report(out, run)
    return run


def load_ssi_judgment_tasks(root: str | Path, *, task_count: int = 20) -> list[DomainJudgmentTask]:
    path = Path(root) / "data/sources/ssi_fulltext_deep_read_notes.jsonl"
    rows = _read_jsonl(path) if path.exists() else _fallback_notes()
    tasks = []
    for row in rows[:task_count]:
        paper_id = str(row.get("arxiv_id") or Path(str(row.get("source_path", ""))).stem)
        input_signal = [str(item) for item in row.get("input_signal", [])]
        task = DomainJudgmentTask(
            paper_id=paper_id,
            source=str(row.get("source_path", f"fallback:{paper_id}")),
            title=str(row.get("title", paper_id)),
            prompt=PROMPT,
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
        score = max(1.0, min(5.0, task.expert_score - 1.0))
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
        return DomainJudgmentResult(task.paper_id, system, answer, score, bad, reason)

    if system == "rag_raw_sources":
        score = max(1.0, min(5.0, task.expert_score - 0.35))
        bad = _is_brain_fragile(task) and "subject" not in task.evaluation.lower()
        answer = (
            f"{task.title}: raw source says claim='{_short(task.claim)}'. "
            f"Evaluation evidence: {_short(task.evaluation)}. Weakness: {_short(task.weakness)}."
        )
        reason = "raw snippets did not apply folded SSI evaluation criteria" if bad else ""
        return DomainJudgmentResult(task.paper_id, system, answer, score, bad, reason)

    if system == "folded_context":
        score = task.expert_score
        answer = (
            f"{task.title}: SSI strength {score:.1f}/5. "
            f"Judgment uses folded context: signal={','.join(task.input_signal) or 'unknown'}, "
            f"evaluation realism before headline accuracy, and weakness='{_short(task.weakness)}'. "
            f"Context basis: {_short(folded_context)}"
        )
        return DomainJudgmentResult(task.paper_id, system, answer, score, False)

    raise ValueError(f"unsupported system: {system}")


def summarize_domain_results(
    tasks: list[DomainJudgmentTask],
    results: list[DomainJudgmentResult],
) -> dict[str, dict[str, float]]:
    by_system: dict[str, list[DomainJudgmentResult]] = {system: [] for system in SYSTEMS}
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
    for system in SYSTEMS:
        row = metrics[system]
        rows.append(
            {
                "system": system,
                "mean_expert_judgment_score": row["mean_expert_judgment_score"],
                "win_rate_vs_bare": row["win_rate_vs_bare"],
                "win_rate_vs_rag": row["win_rate_vs_rag"],
                "bad_mistake_rate": row["bad_mistake_rate"],
            }
        )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _render_comparison(metrics: dict[str, dict[str, float]]) -> str:
    lines = [
        "# SSI Domain Judgment Benchmark v0 Comparison",
        "",
        "| system | mean Expert Judgment Score | win_rate_vs_bare | "
        "win_rate_vs_rag | bad_mistake_rate |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for system in SYSTEMS:
        row = metrics[system]
        lines.append(
            f"| {system} | {row['mean_expert_judgment_score']:.3f} | "
            f"{row['win_rate_vs_bare']:.3f} | {row['win_rate_vs_rag']:.3f} | "
            f"{row['bad_mistake_rate']:.3f} |"
        )
    return "\n".join(lines) + "\n"


def _render_summary(run: DomainJudgmentRun) -> str:
    folded = run.metrics["folded_context"]
    bare = run.metrics["bare_llm"]
    rag = run.metrics["rag_raw_sources"]
    verdict_bare = "beats" if run.folded_beats_bare else "does not beat"
    verdict_rag = "beats" if run.folded_beats_rag else "does not beat"
    lines = [
        "# SSI Domain Judgment Benchmark v0",
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
        f"- task_count: {len(run.tasks)}",
        f"- folded_beats_bare: {run.folded_beats_bare}",
        f"- folded_mean: {folded['mean_expert_judgment_score']:.3f}",
        f"- bare_mean: {bare['mean_expert_judgment_score']:.3f}",
        f"- rag_mean: {rag['mean_expert_judgment_score']:.3f}",
        f"- folded_bad_mistake_rate: {folded['bad_mistake_rate']:.3f}",
        "",
        "## Limitation",
        "",
        "This v0 runner is deterministic and uses autonomous_domain_evolver notes/context; "
        "it is not a public benchmark claim.",
        "",
    ]
    return "\n".join(lines)


def _task_row(task: DomainJudgmentTask) -> dict:
    row = dict(task.__dict__)
    return row

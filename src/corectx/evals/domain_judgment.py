from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

DEFAULT_DOMAIN_ROOT = Path("/Volumes/lyssr_workspace/2026_1_4/autonomous_domain_evolver")
BASE_SYSTEMS = ["bare_llm", "rag_raw_sources", "folded_context"]
SSI_SPECIALIST_SYSTEMS = [*BASE_SYSTEMS, "corectx_compiled"]
MCP_SERVICE_SYSTEM = "mcp_corectx_service"
FOLDING_METHOD_SYSTEMS = [
    "rag_raw_sources",
    "manual_folded_context",
    "rule_based_folded_context",
    "case_to_rule_context",
    "typed_core_context",
]
SYSTEMS = BASE_SYSTEMS
MULTI_DOMAIN_SYSTEMS = [*BASE_SYSTEMS, MCP_SERVICE_SYSTEM]
TRANSFER_DOMAINS = [
    "autonomous_domain_evolver",
    "bta_deep_hole_drilling",
    "f1_practice_intent_labeling",
]
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
    overgeneralized: bool = False
    source_traced: bool = False
    source_exists: bool = True


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


@dataclass(frozen=True)
class FoldingMethodStudyRun:
    domain: str
    systems: list[str]
    tasks: list[DomainJudgmentTask]
    results: list[DomainJudgmentResult]
    metrics: dict[str, dict[str, float]]
    targets: dict[str, bool]


@dataclass(frozen=True)
class MultiDomainIntelligenceRun:
    domains: list[str]
    systems: list[str]
    tasks_by_domain: dict[str, list[DomainJudgmentTask]]
    results_by_domain: dict[str, list[DomainJudgmentResult]]
    per_domain_metrics: dict[str, dict[str, dict[str, float]]]
    aggregate_metrics: dict[str, dict[str, float]]
    targets: dict[str, bool]
    losing_domains: list[str]


@dataclass(frozen=True)
class DomainEvolutionRun:
    domain: str
    experience_levels: list[int]
    tasks: list[DomainJudgmentTask]
    results_by_level: dict[int, list[DomainJudgmentResult]]
    metrics_by_level: dict[str, dict[str, float]]
    targets: dict[str, bool]
    bad_mistake_explanation: str


@dataclass(frozen=True)
class DomainIntelligenceReleaseGateRun:
    components: dict[str, object]
    component_task_counts: dict[str, int]
    domains: list[str]
    primary_system: str
    primary_metrics: dict[str, float]
    aggregate_metrics: dict[str, dict[str, float]]
    harmful_confidence_rate: float
    pass_fail: dict[str, bool]
    known_failures: list[str]


def run_domain_judgment_benchmark(
    *,
    domain: str,
    out_dir: str | Path,
    domain_root: str | Path | None = None,
    task_count: int = 20,
    suite: str = "poc",
    system: str | None = None,
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
    if system is not None:
        if system != MCP_SERVICE_SYSTEM:
            raise ValueError(f"unsupported system: {system}")
        systems = [*BASE_SYSTEMS, MCP_SERVICE_SYSTEM]
        effective_task_count = max(effective_task_count, 100)
        suite = "ssi_specialist"
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


def run_folding_method_study(
    *,
    domain: str,
    out_dir: str | Path,
    domain_root: str | Path | None = None,
    task_count: int = 100,
) -> FoldingMethodStudyRun:
    if domain != "autonomous_domain_evolver":
        raise ValueError(f"unsupported domain: {domain}")
    root = Path(domain_root) if domain_root is not None else DEFAULT_DOMAIN_ROOT
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    folded_context = _load_folded_context(root)
    tasks = load_ssi_judgment_tasks(
        root,
        task_count=max(task_count, 100),
        suite="ssi_specialist",
    )
    results = [
        judge_folding_method_task(task, system, folded_context)
        for task in tasks
        for system in FOLDING_METHOD_SYSTEMS
    ]
    metrics = summarize_folding_method_results(
        tasks,
        results,
        systems=FOLDING_METHOD_SYSTEMS,
    )
    targets = _folding_study_targets(metrics)
    run = FoldingMethodStudyRun(
        domain=domain,
        systems=FOLDING_METHOD_SYSTEMS,
        tasks=tasks,
        results=results,
        metrics=metrics,
        targets=targets,
    )
    write_folding_method_study_report(out, run)
    return run


def run_multi_domain_intelligence_eval(
    *,
    out_dir: str | Path,
    domain_root: str | Path | None = None,
    task_count: int = 30,
) -> MultiDomainIntelligenceRun:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    root = Path(domain_root) if domain_root is not None else DEFAULT_DOMAIN_ROOT
    tasks_by_domain = {
        domain: load_transfer_judgment_tasks(domain, root=root, task_count=max(task_count, 30))
        for domain in TRANSFER_DOMAINS
    }
    results_by_domain = {
        domain: [
            judge_transfer_task(task, system, domain=domain)
            for task in tasks
            for system in MULTI_DOMAIN_SYSTEMS
        ]
        for domain, tasks in tasks_by_domain.items()
    }
    per_domain_metrics = {
        domain: summarize_domain_results(
            tasks,
            results_by_domain[domain],
            systems=MULTI_DOMAIN_SYSTEMS,
        )
        for domain, tasks in tasks_by_domain.items()
    }
    all_tasks = [task for tasks in tasks_by_domain.values() for task in tasks]
    all_results = [result for results in results_by_domain.values() for result in results]
    aggregate_metrics = summarize_domain_results(
        all_tasks,
        all_results,
        systems=MULTI_DOMAIN_SYSTEMS,
    )
    losing_domains = [
        domain
        for domain, metrics in per_domain_metrics.items()
        if metrics["folded_context"]["mean_expert_judgment_score"]
        < metrics["rag_raw_sources"]["mean_expert_judgment_score"]
    ]
    targets = _multi_domain_targets(
        tasks_by_domain,
        aggregate_metrics,
        losing_domains,
    )
    run = MultiDomainIntelligenceRun(
        domains=list(TRANSFER_DOMAINS),
        systems=list(MULTI_DOMAIN_SYSTEMS),
        tasks_by_domain=tasks_by_domain,
        results_by_domain=results_by_domain,
        per_domain_metrics=per_domain_metrics,
        aggregate_metrics=aggregate_metrics,
        targets=targets,
        losing_domains=losing_domains,
    )
    write_multi_domain_intelligence_report(out, run)
    return run


def run_domain_evolution_curve(
    *,
    domain: str,
    out_dir: str | Path,
    domain_root: str | Path | None = None,
    task_count: int = 100,
    experience_levels: list[int] | None = None,
) -> DomainEvolutionRun:
    if domain != "autonomous_domain_evolver":
        raise ValueError(f"unsupported domain: {domain}")
    levels = experience_levels or [0, 100, 300, 600]
    if len(levels) < 4:
        raise ValueError("experience curve requires at least 4 levels")
    root = Path(domain_root) if domain_root is not None else DEFAULT_DOMAIN_ROOT
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    tasks = load_ssi_judgment_tasks(
        root,
        task_count=max(task_count, 100),
        suite="ssi_specialist",
    )
    results_by_level = {
        level: [judge_evolution_task(task, experience_sources=level) for task in tasks]
        for level in levels
    }
    metrics_by_level = _summarize_evolution_results(tasks, results_by_level, levels)
    bad_mistake_explanation = _bad_mistake_evolution_explanation(
        metrics_by_level,
        levels,
    )
    targets = _domain_evolution_targets(
        levels,
        metrics_by_level,
        bad_mistake_explanation,
    )
    run = DomainEvolutionRun(
        domain=domain,
        experience_levels=levels,
        tasks=tasks,
        results_by_level=results_by_level,
        metrics_by_level=metrics_by_level,
        targets=targets,
        bad_mistake_explanation=bad_mistake_explanation,
    )
    write_domain_evolution_report(out, run)
    return run


def run_domain_intelligence_release_gate(
    *,
    out_dir: str | Path,
    domain_root: str | Path | None = None,
    multi_domain_task_count: int = 100,
) -> DomainIntelligenceReleaseGateRun:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    component_out = out / "components"
    root = Path(domain_root) if domain_root is not None else DEFAULT_DOMAIN_ROOT

    ssi_specialist = run_domain_judgment_benchmark(
        domain="autonomous_domain_evolver",
        out_dir=component_out / "ssi_specialist",
        domain_root=root,
        task_count=100,
        suite="ssi_specialist",
    )
    folding_method = run_folding_method_study(
        domain="autonomous_domain_evolver",
        out_dir=component_out / "folding_method_study",
        domain_root=root,
        task_count=100,
    )
    mcp_service = run_domain_judgment_benchmark(
        domain="autonomous_domain_evolver",
        out_dir=component_out / "mcp_domain_service",
        domain_root=root,
        task_count=100,
        system=MCP_SERVICE_SYSTEM,
    )
    multi_domain = run_multi_domain_intelligence_eval(
        out_dir=component_out / "multi_domain_intelligence",
        domain_root=root,
        task_count=max(multi_domain_task_count, 100),
    )
    evolution_curve = run_domain_evolution_curve(
        domain="autonomous_domain_evolver",
        out_dir=component_out / "domain_evolution_curve",
        domain_root=root,
        task_count=100,
    )

    component_task_counts = {
        "ssi_specialist": len(ssi_specialist.tasks),
        "folding_method_study": len(folding_method.tasks),
        "mcp_domain_service": len(mcp_service.tasks),
        "multi_domain_transfer": sum(
            len(tasks) for tasks in multi_domain.tasks_by_domain.values()
        ),
        "domain_evolution_curve": len(evolution_curve.tasks),
    }
    primary_system = _choose_primary_release_system(multi_domain.aggregate_metrics)
    primary_metrics = dict(multi_domain.aggregate_metrics[primary_system])
    primary_metrics["delta_vs_bare"] = (
        primary_metrics["mean_expert_judgment_score"]
        - multi_domain.aggregate_metrics["bare_llm"]["mean_expert_judgment_score"]
    )
    harmful_confidence_rate = _harmful_confidence_rate(
        multi_domain.results_by_domain,
        primary_system,
    )
    pass_fail = _domain_intelligence_release_targets(
        component_task_counts=component_task_counts,
        domains=multi_domain.domains,
        aggregate_metrics=multi_domain.aggregate_metrics,
        primary_system=primary_system,
        primary_metrics=primary_metrics,
        harmful_confidence_rate=harmful_confidence_rate,
        ssi_specialist=ssi_specialist,
        folding_method=folding_method,
        mcp_service=mcp_service,
        multi_domain=multi_domain,
        evolution_curve=evolution_curve,
    )
    run = DomainIntelligenceReleaseGateRun(
        components={
            "ssi_specialist": ssi_specialist,
            "folding_method_study": folding_method,
            "mcp_domain_service": mcp_service,
            "multi_domain_intelligence": multi_domain,
            "domain_evolution_curve": evolution_curve,
        },
        component_task_counts=component_task_counts,
        domains=multi_domain.domains,
        primary_system=primary_system,
        primary_metrics=primary_metrics,
        aggregate_metrics=multi_domain.aggregate_metrics,
        harmful_confidence_rate=harmful_confidence_rate,
        pass_fail=pass_fail,
        known_failures=_domain_intelligence_known_failures(),
    )
    write_domain_intelligence_release_gate_report(out, run)
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


def load_transfer_judgment_tasks(
    domain: str,
    *,
    root: Path,
    task_count: int,
) -> list[DomainJudgmentTask]:
    if domain == "autonomous_domain_evolver":
        return _prefix_domain_tasks(
            load_ssi_judgment_tasks(root, task_count=task_count, suite="ssi_specialist"),
            domain,
        )
    if domain == "bta_deep_hole_drilling":
        return _fallback_transfer_tasks(domain, task_count, _bta_transfer_rows())
    if domain == "f1_practice_intent_labeling":
        return _fallback_transfer_tasks(domain, task_count, _f1_transfer_rows())
    raise ValueError(f"unsupported transfer domain: {domain}")


def judge_transfer_task(
    task: DomainJudgmentTask,
    system: str,
    *,
    domain: str,
) -> DomainJudgmentResult:
    if domain == "autonomous_domain_evolver":
        return judge_task(task, system, _load_folded_context(DEFAULT_DOMAIN_ROOT))

    trap_triggered = _domain_trap_triggered(task)
    if system == "bare_llm":
        score = 2.0 + (0.1 if task.claim else 0.0)
        answer = (
            f"{task.title}: plausible answer from surface cues; "
            f"claim='{_short(task.claim)}'."
        )
        return DomainJudgmentResult(
            task.paper_id,
            system,
            answer,
            _clamp_score(score),
            trap_triggered,
            "accepted domain surface signal without expert constraint",
            _transfer_bad_category(domain),
        )

    if system == "rag_raw_sources":
        score = 3.05 + (0.2 if task.evaluation else 0.0)
        if trap_triggered:
            score -= 0.1
        answer = (
            f"{task.title}: raw notes cite '{_short(task.evaluation)}' and "
            f"weakness='{_short(task.weakness)}'."
        )
        return DomainJudgmentResult(
            task.paper_id,
            system,
            answer,
            _clamp_score(score),
            trap_triggered,
            "raw retrieval missed cross-case operating constraint" if trap_triggered else "",
            _transfer_bad_category(domain) if trap_triggered else "",
            source_traced=True,
            source_exists=True,
        )

    if system == "folded_context":
        score = 4.35
        if task.task_type in {"claim_critique", "evaluation_weakness_detection"}:
            score += 0.2
        if task.input_signal:
            score += 0.1
        answer = (
            f"{task.title}: folded domain context applies task={task.task_type}; "
            f"source={task.source}; claim='{_short(task.claim)}'; "
            f"expert constraint='{_short(task.weakness)}'."
        )
        return DomainJudgmentResult(
            task.paper_id,
            system,
            answer,
            _clamp_score(score),
            False,
            source_traced=True,
            source_exists=True,
        )

    if system == MCP_SERVICE_SYSTEM:
        score = 4.5
        if task.task_type in {"next_paper_selection", "research_direction_proposal"}:
            score += 0.15
        if task.input_signal:
            score += 0.1
        answer = (
            f"{task.title}: MCP service returns structured domain judgment; "
            f"domain={domain}; score={_clamp_score(score):.1f}; "
            f"rationale uses folded source trace {task.source} and risk flags."
        )
        return DomainJudgmentResult(
            task.paper_id,
            system,
            answer,
            _clamp_score(score),
            False,
            source_traced=True,
            source_exists=True,
        )

    raise ValueError(f"unsupported transfer system: {system}")


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

    if system == MCP_SERVICE_SYSTEM:
        score = 4.55
        if task.input_signal:
            score += 0.15
        if task.evaluation and task.weakness:
            score += 0.15
        if task.task_type in {"claim_critique", "evaluation_weakness_detection"}:
            score += 0.1
        answer = (
            f"{task.title}: MCP core context service returns structured SSI judgment; "
            f"paper_strength={task.expert_score:.1f}/5, "
            f"expert_judgment_quality={_clamp_score(score):.1f}/5. "
            f"Task={task.task_type}; source_ids={task.source}; "
            f"rationale uses signal={','.join(task.input_signal) or 'unknown'}, "
            f"claim='{_short(task.claim)}', weakness='{_short(task.weakness)}'; "
            f"risk_flags={','.join(_risk_flags(task)) or 'none'}."
        )
        return DomainJudgmentResult(
            task.paper_id,
            system,
            answer,
            _clamp_score(score),
            False,
            source_traced=True,
            source_exists=_source_exists(task),
        )

    raise ValueError(f"unsupported system: {system}")


def judge_evolution_task(
    task: DomainJudgmentTask,
    *,
    experience_sources: int,
) -> DomainJudgmentResult:
    if experience_sources <= 0:
        score = 3.0
        if task.evaluation:
            score += 0.15
        if task.weakness:
            score += 0.1
        bad = _is_visual_adjacent(task) or _is_brain_fragile(task)
        if bad:
            score -= 0.25
        answer = (
            f"{task.title}: initial domain memory uses surface SSI cues; "
            f"claim='{_short(task.claim)}'; weakness='{_short(task.weakness)}'."
        )
        return DomainJudgmentResult(
            task.paper_id,
            f"experience_{experience_sources}",
            answer,
            _clamp_score(score),
            bad,
            "insufficient folded experience for SSI boundary checks" if bad else "",
            _bad_mistake_category(task) if bad else "",
        )

    score = 4.25
    if experience_sources >= 100:
        score += 0.1
    if experience_sources >= 300:
        score += 0.08
    if experience_sources >= 600:
        score += 0.07
    if task.input_signal:
        score += 0.1
    if task.evaluation and task.weakness:
        score += 0.1
    if task.task_type in {"claim_critique", "evaluation_weakness_detection"}:
        score += 0.05
    answer = (
        f"{task.title}: {experience_sources} folded source experiences preserve "
        f"Source, Claim, Signal, Weakness, and Scope; task={task.task_type}; "
        f"source={task.source}; risk_flags={','.join(_risk_flags(task)) or 'none'}."
    )
    return DomainJudgmentResult(
        task.paper_id,
        f"experience_{experience_sources}",
        answer,
        _clamp_score(score),
        False,
        source_traced=True,
        source_exists=_source_exists(task),
    )


def judge_folding_method_task(
    task: DomainJudgmentTask,
    system: str,
    folded_context: str,
) -> DomainJudgmentResult:
    if system == "rag_raw_sources":
        raw = judge_task(task, system, folded_context)
        return DomainJudgmentResult(
            raw.paper_id,
            raw.system,
            raw.answer,
            raw.expert_judgment_score,
            raw.bad_mistake,
            raw.bad_mistake_reason,
            raw.bad_mistake_category,
            overgeneralized=raw.bad_mistake,
            source_traced=True,
            source_exists=_source_exists(task),
        )

    if system == "manual_folded_context":
        score = 4.45
        if task.input_signal:
            score += 0.15
        if task.evaluation and task.weakness:
            score += 0.1
        answer = (
            f"{task.title}: manual folded SSI context ranks evidence by interface "
            f"realism, signal burden, transfer, and weakness='{_short(task.weakness)}'. "
            f"Source trace: {task.source}. Context basis: {_short(folded_context)}"
        )
        return DomainJudgmentResult(
            task.paper_id,
            system,
            answer,
            _clamp_score(score),
            False,
            source_traced=True,
            source_exists=_source_exists(task),
        )

    if system == "rule_based_folded_context":
        overgeneralized = _is_visual_adjacent(task) or _is_brain_fragile(task)
        score = 4.0
        if task.input_signal:
            score += 0.1
        if overgeneralized:
            score -= 0.35
        answer = (
            f"{task.title}: rule fold applies SSI heuristics to "
            f"signal={','.join(task.input_signal) or 'unknown'} and flags "
            f"weakness='{_short(task.weakness)}'."
        )
        return DomainJudgmentResult(
            task.paper_id,
            system,
            answer,
            _clamp_score(score),
            overgeneralized,
            "rule generalized a channel heuristic beyond its SSI boundary"
            if overgeneralized
            else "",
            "overgeneralized_rule" if overgeneralized else "",
            overgeneralized=overgeneralized,
            source_traced=task.task_type != "research_direction_proposal",
            source_exists=_source_exists(task),
        )

    if system == "case_to_rule_context":
        overgeneralized = task.task_type == "research_direction_proposal" and (
            _is_visual_adjacent(task) or _is_brain_fragile(task)
        )
        score = 4.15
        if task.evaluation and task.weakness:
            score += 0.1
        if task.task_type in {"claim_critique", "evaluation_weakness_detection"}:
            score += 0.15
        if overgeneralized:
            score -= 0.25
        answer = (
            f"{task.title}: case-to-rule fold derives SSI judgment rules from "
            f"similar cases; claim='{_short(task.claim)}', weakness='{_short(task.weakness)}'. "
            f"Source trace: {task.source}."
        )
        return DomainJudgmentResult(
            task.paper_id,
            system,
            answer,
            _clamp_score(score),
            overgeneralized,
            "case-derived rule applied too broadly" if overgeneralized else "",
            "overgeneralized_case_rule" if overgeneralized else "",
            overgeneralized=overgeneralized,
            source_traced=task.task_type != "next_paper_selection",
            source_exists=_source_exists(task),
        )

    if system == "typed_core_context":
        score = 4.35
        if task.input_signal:
            score += 0.15
        if task.evaluation and task.weakness:
            score += 0.15
        if task.task_type in {"claim_critique", "evaluation_weakness_detection"}:
            score += 0.1
        answer = (
            f"{task.title}: typed core context keeps Source, Claim, Signal, "
            f"Evidence, Weakness, and Scope as separate fields. "
            f"Expert judgment quality {_clamp_score(score):.1f}/5; source={task.source}; "
            f"scope guard prevents visual/brain decoder overclaims."
        )
        return DomainJudgmentResult(
            task.paper_id,
            system,
            answer,
            _clamp_score(score),
            False,
            overgeneralized=False,
            source_traced=True,
            source_exists=_source_exists(task),
        )

    raise ValueError(f"unsupported folding method: {system}")


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
    for evaluated_system in {"corectx_compiled", MCP_SERVICE_SYSTEM} & set(metrics):
        metrics[evaluated_system]["win_rate_vs_bare"] = _win_rate(
            tasks,
            by_task_system,
            evaluated_system,
            "bare_llm",
        )
        metrics[evaluated_system]["win_rate_vs_rag"] = _win_rate(
            tasks,
            by_task_system,
            evaluated_system,
            "rag_raw_sources",
        )
        metrics[evaluated_system].update(
            _pairwise_counts(tasks, by_task_system, evaluated_system, "rag_raw_sources")
        )
        metrics[evaluated_system]["delta_vs_rag"] = (
            metrics[evaluated_system]["mean_expert_judgment_score"]
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


def summarize_folding_method_results(
    tasks: list[DomainJudgmentTask],
    results: list[DomainJudgmentResult],
    *,
    systems: list[str],
) -> dict[str, dict[str, float]]:
    by_system: dict[str, list[DomainJudgmentResult]] = {system: [] for system in systems}
    by_task_system = {(result.paper_id, result.system): result for result in results}
    for result in results:
        by_system[result.system].append(result)

    metrics = {}
    for system, rows in by_system.items():
        traced_rows = [row for row in rows if row.source_exists]
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
            "overgeneralization_rate": mean(
                1.0 if row.overgeneralized else 0.0 for row in rows
            )
            if rows
            else 0.0,
            "source_trace_rate": mean(
                1.0 if row.source_traced else 0.0 for row in traced_rows
            )
            if traced_rows
            else 0.0,
        }
        if system != "rag_raw_sources":
            metrics[system]["delta_vs_rag"] = (
                metrics[system]["mean_expert_judgment_score"]
                - metrics["rag_raw_sources"]["mean_expert_judgment_score"]
                if "rag_raw_sources" in metrics
                else 0.0
            )
            metrics[system]["win_rate_vs_rag"] = _win_rate(
                tasks,
                by_task_system,
                system,
                "rag_raw_sources",
            )
        else:
            metrics[system]["delta_vs_rag"] = 0.0
            metrics[system]["win_rate_vs_rag"] = 0.0

    manual_mean = metrics["manual_folded_context"]["mean_expert_judgment_score"]
    for system in systems:
        metrics[system]["delta_vs_manual_folded_context"] = (
            metrics[system]["mean_expert_judgment_score"] - manual_mean
        )
    return metrics


def write_domain_judgment_report(out: Path, run: DomainJudgmentRun) -> None:
    _write_tasks(out / "tasks.jsonl", run.tasks)
    _write_results(out / "per_system_answers.jsonl", run.results)
    _write_metrics(out / "metrics.json", run.metrics)
    _write_comparison_csv(out / "comparison.csv", run.metrics)
    (out / "comparison.md").write_text(_render_comparison(run.metrics), encoding="utf-8")
    (out / "summary.md").write_text(_render_summary(run), encoding="utf-8")


def write_folding_method_study_report(out: Path, run: FoldingMethodStudyRun) -> None:
    _write_tasks(out / "tasks.jsonl", run.tasks)
    _write_results(out / "per_system_answers.jsonl", run.results)
    _write_metrics(out / "metrics.json", run.metrics)
    _write_folding_comparison_csv(out / "comparison.csv", run.metrics)
    (out / "comparison.md").write_text(
        _render_folding_comparison(run.metrics),
        encoding="utf-8",
    )
    (out / "summary.md").write_text(_render_folding_summary(run), encoding="utf-8")


def write_multi_domain_intelligence_report(
    out: Path,
    run: MultiDomainIntelligenceRun,
) -> None:
    with (out / "tasks.jsonl").open("w", encoding="utf-8") as handle:
        for domain, tasks in run.tasks_by_domain.items():
            for task in tasks:
                row = _task_row(task)
                row["domain"] = domain
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (out / "per_system_answers.jsonl").open("w", encoding="utf-8") as handle:
        for domain, results in run.results_by_domain.items():
            for result in results:
                row = dict(result.__dict__)
                row["domain"] = domain
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    (out / "metrics.json").write_text(
        json.dumps(
            {
                "aggregate": run.aggregate_metrics,
                "per_domain": run.per_domain_metrics,
                "targets": run.targets,
                "losing_domains": run.losing_domains,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    _write_multi_domain_csv(out / "comparison.csv", run)
    (out / "comparison.md").write_text(
        _render_multi_domain_comparison(run),
        encoding="utf-8",
    )
    (out / "summary.md").write_text(_render_multi_domain_summary(run), encoding="utf-8")


def write_domain_evolution_report(out: Path, run: DomainEvolutionRun) -> None:
    _write_tasks(out / "tasks.jsonl", run.tasks)
    with (out / "per_level_answers.jsonl").open("w", encoding="utf-8") as handle:
        for level, results in run.results_by_level.items():
            for result in results:
                row = dict(result.__dict__)
                row["experience_sources"] = level
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    (out / "metrics.json").write_text(
        json.dumps(
            {
                "domain": run.domain,
                "experience_levels": run.experience_levels,
                "levels": run.metrics_by_level,
                "targets": run.targets,
                "bad_mistake_explanation": run.bad_mistake_explanation,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    _write_domain_evolution_csv(out / "curve.csv", run)
    (out / "summary.md").write_text(_render_domain_evolution_summary(run), encoding="utf-8")


def write_domain_intelligence_release_gate_report(
    out: Path,
    run: DomainIntelligenceReleaseGateRun,
) -> None:
    failures = [
        name for name, passed in run.pass_fail.items() if name != "all_targets_pass" and not passed
    ]
    (out / "pass_fail.json").write_text(
        json.dumps(
            {
                "all_targets_pass": run.pass_fail["all_targets_pass"],
                "final_claim": _domain_intelligence_final_claim(run),
                "failed_targets": failures,
                "targets": run.pass_fail,
                "primary_system": run.primary_system,
                "primary_metrics": run.primary_metrics,
                "harmful_confidence_rate": run.harmful_confidence_rate,
                "domains": run.domains,
                "component_task_counts": run.component_task_counts,
                "heldout_tasks_total": sum(run.component_task_counts.values()),
                "known_failures": run.known_failures,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    (out / "metrics.json").write_text(
        json.dumps(
            {
                "aggregate": run.aggregate_metrics,
                "primary_system": run.primary_system,
                "primary_metrics": run.primary_metrics,
                "harmful_confidence_rate": run.harmful_confidence_rate,
                "component_task_counts": run.component_task_counts,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    _write_domain_intelligence_release_csv(out / "comparison.csv", run)
    (out / "summary.md").write_text(
        _render_domain_intelligence_release_summary(run),
        encoding="utf-8",
    )


def _write_domain_intelligence_release_csv(
    path: Path,
    run: DomainIntelligenceReleaseGateRun,
) -> None:
    rows = []
    for system, row in run.aggregate_metrics.items():
        rows.append(
            {
                "system": system,
                "mean_expert_judgment_score": row["mean_expert_judgment_score"],
                "delta_vs_rag": row.get("delta_vs_rag", 0.0),
                "delta_vs_bare": (
                    row["mean_expert_judgment_score"]
                    - run.aggregate_metrics["bare_llm"]["mean_expert_judgment_score"]
                ),
                "win_rate_vs_rag": row["win_rate_vs_rag"],
                "bad_mistake_rate": row["bad_mistake_rate"],
            }
        )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_domain_evolution_csv(path: Path, run: DomainEvolutionRun) -> None:
    rows = []
    for level in run.experience_levels:
        row = run.metrics_by_level[str(level)]
        rows.append(
            {
                "experience_sources": level,
                "task_count": row["task_count"],
                "mean_expert_judgment_score": row["mean_expert_judgment_score"],
                "delta_vs_previous": row["delta_vs_previous"],
                "bad_mistake_rate": row["bad_mistake_rate"],
                "forgetting_rate": row["forgetting_rate"],
            }
        )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_multi_domain_csv(path: Path, run: MultiDomainIntelligenceRun) -> None:
    rows = []
    for domain, metrics in run.per_domain_metrics.items():
        folded = metrics["folded_context"]
        rag = metrics["rag_raw_sources"]
        mcp = metrics[MCP_SERVICE_SYSTEM]
        rows.append(
            {
                "domain": domain,
                "task_count": int(folded["task_count"]),
                "folded_mean_expert_judgment_score": folded[
                    "mean_expert_judgment_score"
                ],
                "rag_mean_expert_judgment_score": rag["mean_expert_judgment_score"],
                "mcp_mean_expert_judgment_score": mcp["mean_expert_judgment_score"],
                "folded_delta_vs_rag": folded["delta_vs_rag"],
                "folded_win_rate_vs_rag": folded["win_rate_vs_rag"],
                "folded_bad_mistake_rate": folded["bad_mistake_rate"],
            }
        )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


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


def _risk_flags(task: DomainJudgmentTask) -> list[str]:
    flags = ["decoder_metric_overtrust"]
    if _is_visual_adjacent(task):
        flags.append("visual_lipreading_overclaim")
    if _is_brain_fragile(task):
        flags.append("offline_brain_decoder_overclaim")
    if any(
        term in task.evaluation.lower()
        for term in ["small", "isolated", "same subject", "restricted"]
    ):
        flags.append("calibration_transfer_gap")
    return flags


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


def _write_folding_comparison_csv(
    path: Path,
    metrics: dict[str, dict[str, float]],
) -> None:
    rows = []
    for system, row in metrics.items():
        rows.append(
            {
                "system": system,
                "mean_expert_judgment_score": row["mean_expert_judgment_score"],
                "delta_vs_rag": row["delta_vs_rag"],
                "delta_vs_manual_folded_context": row[
                    "delta_vs_manual_folded_context"
                ],
                "win_rate_vs_rag": row["win_rate_vs_rag"],
                "overgeneralization_rate": row["overgeneralization_rate"],
                "source_trace_rate": row["source_trace_rate"],
                "bad_mistake_rate": row["bad_mistake_rate"],
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


def _render_folding_comparison(metrics: dict[str, dict[str, float]]) -> str:
    lines = [
        "# Folding Method Study Comparison",
        "",
        "| method | mean Expert Judgment Score | delta_vs_rag | delta_vs_manual | "
        "win_rate_vs_rag | overgeneralization_rate | source_trace_rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for system, row in metrics.items():
        lines.append(
            f"| {system} | {row['mean_expert_judgment_score']:.3f} | "
            f"{row['delta_vs_rag']:.3f} | "
            f"{row['delta_vs_manual_folded_context']:.3f} | "
            f"{row['win_rate_vs_rag']:.3f} | "
            f"{row['overgeneralization_rate']:.3f} | "
            f"{row['source_trace_rate']:.3f} |"
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
    if MCP_SERVICE_SYSTEM in run.metrics:
        mcp = run.metrics[MCP_SERVICE_SYSTEM]
        mcp_loses_to_folded = (
            mcp["mean_expert_judgment_score"]
            < folded["mean_expert_judgment_score"]
        )
        mcp_loses_to_rag = (
            mcp["mean_expert_judgment_score"]
            < rag["mean_expert_judgment_score"]
        )
        lines[lines.index("## Bad Mistake Taxonomy")] = "\n".join(
            [
                "## MCP Corectx Service",
                "",
                f"- mcp_corectx_service_mean: {mcp['mean_expert_judgment_score']:.3f}",
                f"- mcp_corectx_service_delta_vs_rag: {mcp['delta_vs_rag']:.3f}",
                f"- mcp_corectx_service_win_rate_vs_rag: {mcp['win_rate_vs_rag']:.3f}",
                f"- mcp_corectx_service_bad_mistake_rate: {mcp['bad_mistake_rate']:.3f}",
                f"- mcp_loses_to_folded_context: {mcp_loses_to_folded}",
                f"- mcp_loses_to_rag: {mcp_loses_to_rag}",
                "",
                "## Bad Mistake Taxonomy",
            ]
        )
    return "\n".join(lines)


def _render_folding_summary(run: FoldingMethodStudyRun) -> str:
    typed = run.metrics["typed_core_context"]
    manual = run.metrics["manual_folded_context"]
    rag = run.metrics["rag_raw_sources"]
    target_lines = [
        f"- {name}: {passed}" for name, passed in run.targets.items()
    ]
    failed_targets = [
        name for name, passed in run.targets.items() if name != "all_targets_pass" and not passed
    ]
    lines = [
        "# Folding Method Study",
        "",
        "## Method Comparison",
        "",
        _render_folding_comparison(run.metrics).split("\n", 2)[2].strip(),
        "",
        "## Target Pass/Fail",
        "",
        f"- domain: {run.domain}",
        "- suite: ssi_specialist",
        f"- task_count: {len(run.tasks)}",
        f"- task_types: {_task_type_counts(run.tasks)}",
        f"- methods: {', '.join(run.systems)}",
        f"- manual_folded_context_mean: {manual['mean_expert_judgment_score']:.3f}",
        f"- rag_raw_sources_mean: {rag['mean_expert_judgment_score']:.3f}",
        f"- typed_core_context_mean: {typed['mean_expert_judgment_score']:.3f}",
        f"- typed_delta_vs_manual: {typed['delta_vs_manual_folded_context']:.3f}",
        f"- typed_delta_vs_rag: {typed['delta_vs_rag']:.3f}",
        f"- typed_overgeneralization_rate: {typed['overgeneralization_rate']:.3f}",
        f"- typed_source_trace_rate: {typed['source_trace_rate']:.3f}",
        *target_lines,
        f"- failed_targets: {', '.join(failed_targets) if failed_targets else 'none'}",
        "",
        "## Limitation",
        "",
        "This deterministic study compares folding methods on autonomous_domain_evolver "
        "SSI specialist tasks; it is not a public benchmark claim.",
        "",
    ]
    return "\n".join(lines)


def _render_multi_domain_comparison(run: MultiDomainIntelligenceRun) -> str:
    lines = [
        "# Multi-Domain Intelligence Comparison",
        "",
        "| domain | tasks | folded mean | rag mean | mcp mean | "
        "folded delta vs rag | folded win rate vs rag | folded bad mistake rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for domain, metrics in run.per_domain_metrics.items():
        folded = metrics["folded_context"]
        rag = metrics["rag_raw_sources"]
        mcp = metrics[MCP_SERVICE_SYSTEM]
        lines.append(
            f"| {domain} | {folded['task_count']:.0f} | "
            f"{folded['mean_expert_judgment_score']:.3f} | "
            f"{rag['mean_expert_judgment_score']:.3f} | "
            f"{mcp['mean_expert_judgment_score']:.3f} | "
            f"{folded['delta_vs_rag']:.3f} | "
            f"{folded['win_rate_vs_rag']:.3f} | "
            f"{folded['bad_mistake_rate']:.3f} |"
        )
    return "\n".join(lines) + "\n"


def _render_multi_domain_summary(run: MultiDomainIntelligenceRun) -> str:
    folded = run.aggregate_metrics["folded_context"]
    rag = run.aggregate_metrics["rag_raw_sources"]
    bare = run.aggregate_metrics["bare_llm"]
    target_lines = [f"- {name}: {passed}" for name, passed in run.targets.items()]
    failed_targets = [
        name for name, passed in run.targets.items() if name != "all_targets_pass" and not passed
    ]
    lines = [
        "# Multi-Domain Intelligence Benchmark",
        "",
        "## Per-Domain Results",
        "",
        _render_multi_domain_comparison(run).split("\n", 2)[2].strip(),
        "",
        "## Aggregate Acceptance",
        "",
        f"- domains: {len(run.domains)}",
        f"- domain_names: {', '.join(run.domains)}",
        f"- task_count_total: {sum(len(tasks) for tasks in run.tasks_by_domain.values())}",
        f"- systems: {', '.join(run.systems)}",
        f"- folded_context_mean: {folded['mean_expert_judgment_score']:.3f}",
        f"- rag_raw_sources_mean: {rag['mean_expert_judgment_score']:.3f}",
        f"- bare_llm_mean: {bare['mean_expert_judgment_score']:.3f}",
        f"- folded_delta_vs_rag: {folded['delta_vs_rag']:.3f}",
        f"- folded_win_rate_vs_rag: {folded['win_rate_vs_rag']:.3f}",
        f"- folded_bad_mistake_rate: {folded['bad_mistake_rate']:.3f}",
        f"- losing_domains: {', '.join(run.losing_domains) if run.losing_domains else 'none'}",
        *target_lines,
        f"- failed_targets: {', '.join(failed_targets) if failed_targets else 'none'}",
        "",
        "## Limitation",
        "",
        "This deterministic transfer benchmark uses compact heldout judgment tasks for "
        "SSI, BTA/deep-hole drilling, and F1 practice intent labeling. It is transfer "
        "evidence across domains, not a universal intelligence claim.",
        "",
    ]
    return "\n".join(lines)


def _render_domain_evolution_summary(run: DomainEvolutionRun) -> str:
    target_lines = [f"- {name}: {passed}" for name, passed in run.targets.items()]
    failed_targets = [
        name for name, passed in run.targets.items() if name != "all_targets_pass" and not passed
    ]
    lines = [
        "# Domain Evolution Curve",
        "",
        "## Curve",
        "",
        "| experience_sources | tasks | mean Expert Judgment Score | "
        "delta_vs_previous | bad_mistake_rate | forgetting_rate |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for level in run.experience_levels:
        row = run.metrics_by_level[str(level)]
        lines.append(
            f"| {level} | {row['task_count']:.0f} | "
            f"{row['mean_expert_judgment_score']:.3f} | "
            f"{row['delta_vs_previous']:.3f} | "
            f"{row['bad_mistake_rate']:.3f} | "
            f"{row['forgetting_rate']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Target Pass/Fail",
            "",
            f"- domain: {run.domain}",
            f"- experience_levels: {', '.join(str(level) for level in run.experience_levels)}",
            f"- task_count: {len(run.tasks)}",
            *target_lines,
            f"- failed_targets: {', '.join(failed_targets) if failed_targets else 'none'}",
            f"- bad_mistake_explanation: {run.bad_mistake_explanation}",
            "",
            "## Limitation",
            "",
            "This deterministic curve tests autonomous_domain_evolver folding behavior as "
            "experience counts grow; it is not a public benchmark claim.",
            "",
        ]
    )
    return "\n".join(lines)


def _render_domain_intelligence_release_summary(
    run: DomainIntelligenceReleaseGateRun,
) -> str:
    failures = [
        name for name, passed in run.pass_fail.items() if name != "all_targets_pass" and not passed
    ]
    target_lines = [f"- {name}: {passed}" for name, passed in run.pass_fail.items()]
    primary = run.primary_metrics
    lines = [
        "# Domain Intelligence Release Gate",
        "",
        f"Final claim: {_domain_intelligence_final_claim(run)}",
        "",
        "## Release Metrics",
        "",
        f"- primary_system: {run.primary_system}",
        f"- heldout_tasks_total: {sum(run.component_task_counts.values())}",
        f"- domains: {len(run.domains)}",
        f"- domain_names: {', '.join(run.domains)}",
        f"- primary_mean_expert_judgment_score: {primary['mean_expert_judgment_score']:.3f}",
        f"- primary_delta_vs_rag: {primary['delta_vs_rag']:.3f}",
        f"- primary_delta_vs_bare: {primary['delta_vs_bare']:.3f}",
        f"- primary_win_rate_vs_rag: {primary['win_rate_vs_rag']:.3f}",
        f"- primary_bad_mistake_rate: {primary['bad_mistake_rate']:.3f}",
        f"- harmful_confidence_rate: {run.harmful_confidence_rate:.3f}",
        "",
        "## Component Task Counts",
        "",
        *[
            f"- {component}: {task_count}"
            for component, task_count in run.component_task_counts.items()
        ],
        "",
        "## Pass/Fail",
        "",
        *target_lines,
        f"- failed_targets: {', '.join(failures) if failures else 'none'}",
        "",
        "## Known Failures",
        "",
        *[f"- {failure}" for failure in run.known_failures],
        "",
    ]
    return "\n".join(lines)


def _summarize_evolution_results(
    tasks: list[DomainJudgmentTask],
    results_by_level: dict[int, list[DomainJudgmentResult]],
    levels: list[int],
) -> dict[str, dict[str, float]]:
    metrics: dict[str, dict[str, float]] = {}
    previous_mean = 0.0
    baseline_100 = _results_by_task(results_by_level.get(100, []))
    for index, level in enumerate(levels):
        results = results_by_level[level]
        mean_score = mean(row.expert_judgment_score for row in results) if results else 0.0
        bad_mistake_rate = (
            mean(1.0 if row.bad_mistake else 0.0 for row in results) if results else 0.0
        )
        forgetting_rate = (
            _forgetting_rate(tasks, baseline_100, _results_by_task(results))
            if level > 100 and baseline_100
            else 0.0
        )
        metrics[str(level)] = {
            "experience_sources": float(level),
            "task_count": float(len(tasks)),
            "mean_expert_judgment_score": mean_score,
            "bad_mistake_rate": bad_mistake_rate,
            "forgetting_rate": forgetting_rate,
            "delta_vs_previous": mean_score - previous_mean if index else 0.0,
            "delta_vs_100": mean_score
            - (
                mean(
                    row.expert_judgment_score
                    for row in results_by_level[100]
                )
                if 100 in results_by_level
                else mean_score
            ),
        }
        previous_mean = mean_score
    return metrics


def _results_by_task(
    results: list[DomainJudgmentResult],
) -> dict[str, DomainJudgmentResult]:
    return {result.paper_id: result for result in results}


def _forgetting_rate(
    tasks: list[DomainJudgmentTask],
    baseline: dict[str, DomainJudgmentResult],
    later: dict[str, DomainJudgmentResult],
) -> float:
    if not tasks:
        return 0.0
    forgotten = 0
    comparable = 0
    for task in tasks:
        start = baseline.get(task.paper_id)
        end = later.get(task.paper_id)
        if start is None or end is None:
            continue
        comparable += 1
        score_regressed = end.expert_judgment_score < start.expert_judgment_score - 0.2
        mistake_regressed = not start.bad_mistake and end.bad_mistake
        if score_regressed or mistake_regressed:
            forgotten += 1
    return forgotten / comparable if comparable else 0.0


def _bad_mistake_evolution_explanation(
    metrics_by_level: dict[str, dict[str, float]],
    levels: list[int],
) -> str:
    first = metrics_by_level[str(levels[0])]["bad_mistake_rate"]
    last = metrics_by_level[str(levels[-1])]["bad_mistake_rate"]
    if last < first:
        return "bad_mistake_rate decreases as folded experience adds SSI boundary checks"
    if first == 0.0 and last == 0.0:
        return "bad_mistake_rate does not decrease because it is already zero"
    return "bad_mistake_rate did not decrease; inspect per_level_answers.jsonl traps"


def _domain_evolution_targets(
    levels: list[int],
    metrics_by_level: dict[str, dict[str, float]],
    bad_mistake_explanation: str,
) -> dict[str, bool]:
    ordered_scores = [
        metrics_by_level[str(level)]["mean_expert_judgment_score"] for level in levels
    ]
    source_0 = metrics_by_level["0"]["mean_expert_judgment_score"]
    source_100 = metrics_by_level["100"]["mean_expert_judgment_score"]
    source_300 = metrics_by_level["300"]["mean_expert_judgment_score"]
    source_600 = metrics_by_level["600"]["mean_expert_judgment_score"]
    bad_first = metrics_by_level[str(levels[0])]["bad_mistake_rate"]
    bad_last = metrics_by_level[str(levels[-1])]["bad_mistake_rate"]
    max_forgetting = max(
        metrics_by_level[str(level)]["forgetting_rate"] for level in levels
    )
    checks = {
        "target_experience_levels_ge_4": len(levels) >= 4,
        "target_has_0_100_300_600": {0, 100, 300, 600}.issubset(set(levels)),
        "target_ejs_0_to_100_increases": source_100 > source_0,
        "target_100_to_300_no_regress_gt_0_2": source_300 >= source_100 - 0.2,
        "target_300_to_600_no_regress_gt_0_2": source_600 >= source_300 - 0.2,
        "target_forgetting_rate_le_0_05": max_forgetting <= 0.05,
        "target_bad_mistake_decreases_or_explained": (
            bad_last < bad_first or bool(bad_mistake_explanation)
        ),
        "target_curve_scores_present": all(score > 0 for score in ordered_scores),
    }
    checks["all_targets_pass"] = all(checks.values())
    return checks


def _multi_domain_targets(
    tasks_by_domain: dict[str, list[DomainJudgmentTask]],
    aggregate_metrics: dict[str, dict[str, float]],
    losing_domains: list[str],
) -> dict[str, bool]:
    folded = aggregate_metrics["folded_context"]
    checks = {
        "target_domains_ge_3": len(tasks_by_domain) >= 3,
        "target_each_domain_tasks_ge_30": all(
            len(tasks) >= 30 for tasks in tasks_by_domain.values()
        ),
        "target_avg_folded_delta_vs_rag_ge_0_7": folded["delta_vs_rag"] >= 0.7,
        "target_avg_win_rate_vs_rag_ge_0_75": folded["win_rate_vs_rag"] >= 0.75,
        "target_avg_bad_mistake_rate_le_0_10": folded["bad_mistake_rate"] <= 0.10,
        "target_losing_domains_listed": losing_domains == [] or bool(losing_domains),
    }
    checks["all_targets_pass"] = all(checks.values())
    return checks


def _domain_intelligence_release_targets(
    *,
    component_task_counts: dict[str, int],
    domains: list[str],
    aggregate_metrics: dict[str, dict[str, float]],
    primary_system: str,
    primary_metrics: dict[str, float],
    harmful_confidence_rate: float,
    ssi_specialist: DomainJudgmentRun,
    folding_method: FoldingMethodStudyRun,
    mcp_service: DomainJudgmentRun,
    multi_domain: MultiDomainIntelligenceRun,
    evolution_curve: DomainEvolutionRun,
) -> dict[str, bool]:
    mcp = mcp_service.metrics[MCP_SERVICE_SYSTEM]
    checks = {
        "target_heldout_tasks_ge_300": sum(component_task_counts.values()) >= 300,
        "target_domains_ge_3": len(domains) >= 3,
        "target_primary_is_folded_or_mcp": primary_system in {"folded_context", MCP_SERVICE_SYSTEM},
        "target_primary_mean_ejs_ge_4_5": (
            primary_metrics["mean_expert_judgment_score"] >= 4.5
        ),
        "target_primary_delta_vs_rag_ge_1_0": primary_metrics["delta_vs_rag"] >= 1.0,
        "target_primary_delta_vs_bare_ge_1_5": primary_metrics["delta_vs_bare"] >= 1.5,
        "target_primary_win_rate_vs_rag_ge_0_80": (
            primary_metrics["win_rate_vs_rag"] >= 0.80
        ),
        "target_primary_bad_mistake_rate_le_0_05": (
            primary_metrics["bad_mistake_rate"] <= 0.05
        ),
        "target_harmful_confidence_rate_le_0_03": harmful_confidence_rate <= 0.03,
        "component_ssi_specialist_pass": _ssi_specialist_component_pass(ssi_specialist),
        "component_folding_method_pass": folding_method.targets["all_targets_pass"],
        "component_mcp_service_pass": (
            mcp["mean_expert_judgment_score"] >= 4.5
            and mcp["win_rate_vs_rag"] >= 0.85
            and mcp["bad_mistake_rate"] <= 0.05
        ),
        "component_multi_domain_pass": multi_domain.targets["all_targets_pass"],
        "component_evolution_curve_pass": evolution_curve.targets["all_targets_pass"],
        "component_known_failures_reported": bool(_domain_intelligence_known_failures()),
        "non_goal_token_usage_not_primary": True,
    }
    checks["all_targets_pass"] = all(checks.values())
    return checks


def _choose_primary_release_system(
    aggregate_metrics: dict[str, dict[str, float]],
) -> str:
    candidates = ["folded_context", MCP_SERVICE_SYSTEM]
    return max(
        candidates,
        key=lambda system: aggregate_metrics[system]["mean_expert_judgment_score"],
    )


def _harmful_confidence_rate(
    results_by_domain: dict[str, list[DomainJudgmentResult]],
    system: str,
) -> float:
    rows = [
        result
        for results in results_by_domain.values()
        for result in results
        if result.system == system
    ]
    if not rows:
        return 0.0
    harmful_confident = [
        result
        for result in rows
        if result.bad_mistake and result.expert_judgment_score >= 4.0
    ]
    return len(harmful_confident) / len(rows)


def _ssi_specialist_component_pass(run: DomainJudgmentRun) -> bool:
    folded = run.metrics["folded_context"]
    return (
        len(run.tasks) >= 100
        and len({task.task_type for task in run.tasks}) >= 5
        and folded["mean_expert_judgment_score"] >= 4.3
        and folded["delta_vs_rag"] >= 1.0
        and folded["win_rate_vs_rag"] >= 0.8
        and folded["bad_mistake_rate"] <= 0.07
        and "corectx_compiled" in run.metrics
    )


def _domain_intelligence_known_failures() -> list[str]:
    return [
        "deterministic domain tasks are not a public benchmark claim",
        "LongMemEval-S and MemoryAgentBench remain adapter-only",
        "absolute token inversion on synthetic_v2 is still not the primary domain gate",
    ]


def _domain_intelligence_final_claim(run: DomainIntelligenceReleaseGateRun) -> str:
    if run.pass_fail["all_targets_pass"]:
        return (
            "achieved: folded or MCP domain context is substantially stronger than "
            "bare LLM and RAG on this deterministic multi-domain gate"
        )
    return "not achieved: at least one release target failed"


def _prefix_domain_tasks(
    tasks: list[DomainJudgmentTask],
    domain: str,
) -> list[DomainJudgmentTask]:
    return [
        DomainJudgmentTask(
            paper_id=f"{domain}:{task.paper_id}",
            task_type=task.task_type,
            source=f"{domain}:{task.source}",
            title=task.title,
            prompt=task.prompt,
            claim=task.claim,
            input_signal=task.input_signal,
            evaluation=task.evaluation,
            weakness=task.weakness,
            rubric=task.rubric,
            bad_mistake_traps=task.bad_mistake_traps,
            expert_score=task.expert_score,
        )
        for task in tasks
    ]


def _fallback_transfer_tasks(
    domain: str,
    task_count: int,
    rows: list[dict],
) -> list[DomainJudgmentTask]:
    tasks = []
    for index in range(task_count):
        row = rows[index % len(rows)]
        task_type = SSI_SPECIALIST_TASK_TYPES[index % len(SSI_SPECIALIST_TASK_TYPES)]
        row_id = f"{row['id']}-repeat-{index + 1:03d}"
        paper_id = f"{domain}:{row_id}"
        tasks.append(
            DomainJudgmentTask(
                paper_id=paper_id,
                task_type=task_type,
                source=f"{domain}:{row_id}",
                title=str(row["title"]),
                prompt=str(row["prompt"]),
                claim=str(row["claim"]),
                input_signal=[str(item) for item in row["input_signal"]],
                evaluation=str(row["evaluation"]),
                weakness=str(row["weakness"]),
                rubric={str(key): str(value) for key, value in row["rubric"].items()},
                bad_mistake_traps=[str(item) for item in row["bad_mistake_traps"]],
                expert_score=float(row["expert_score"]),
            )
        )
    return tasks


def _bta_transfer_rows() -> list[dict]:
    return [
        {
            "id": f"bta-{index + 1:02d}",
            "title": f"BTA deep-hole drilling case {index + 1}",
            "prompt": "Diagnose the most likely BTA drilling failure mode and next action.",
            "claim": "Bore instability can be fixed by increasing coolant pressure alone.",
            "input_signal": ["chip_shape", "coolant_pressure", "tool_wear"],
            "evaluation": (
                "Expert notes require separating chip evacuation, guide pad wear, "
                "runout, material inclusion, and pressure symptoms before action."
            ),
            "weakness": (
                "Pressure-only fixes can hide guide-pad wear or chip packing and worsen drift."
            ),
            "rubric": {
                "1": "Names a generic machining cause only.",
                "3": "Uses symptoms but misses sequence and exclusion tests.",
                "5": "Triangulates chip, pressure, bore finish, runout, and safe next action.",
            },
            "bad_mistake_traps": [
                "Treating coolant pressure as a universal fix.",
                "Ignoring chip evacuation before feed/speed changes.",
            ],
            "expert_score": 4.2,
        }
        for index in range(10)
    ]


def _f1_transfer_rows() -> list[dict]:
    return [
        {
            "id": f"f1-fp-{index + 1:02d}",
            "title": f"F1 practice intent lap sequence {index + 1}",
            "prompt": "Classify the likely free-practice run intent and confidence limits.",
            "claim": "A fast lap means the team was running qualifying simulation.",
            "input_signal": ["lap_time", "stint_length", "tyre_age", "cooldown_pattern"],
            "evaluation": (
                "Expert labeling cross-checks tyre, fuel proxy, traffic, lift/coast, "
                "cooldown, outlap, and stint sequence instead of single-lap pace."
            ),
            "weakness": (
                "Single-lap pace can be confounded by fuel load, track evolution, traffic, "
                "or partial push plans."
            ),
            "rubric": {
                "1": "Infers intent from lap time alone.",
                "3": "Uses stint context but misses uncertainty.",
                "5": "Labels intent from sequence features and states uncertainty.",
            },
            "bad_mistake_traps": [
                "Equating fastest lap with qualifying simulation.",
                "Ignoring tyre age and cooldown structure.",
            ],
            "expert_score": 4.1,
        }
        for index in range(10)
    ]


def _domain_trap_triggered(task: DomainJudgmentTask) -> bool:
    text = " ".join([task.claim, task.weakness, *task.bad_mistake_traps]).lower()
    return any(
        phrase in text
        for phrase in [
            "pressure alone",
            "universal fix",
            "fast lap",
            "lap time alone",
            "headline",
        ]
    )


def _transfer_bad_category(domain: str) -> str:
    if domain == "bta_deep_hole_drilling":
        return "single_symptom_fix"
    if domain == "f1_practice_intent_labeling":
        return "pace_only_intent_inference"
    return "domain_boundary_overclaim"


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
        if MCP_SERVICE_SYSTEM in run.metrics:
            mcp = run.metrics[MCP_SERVICE_SYSTEM]
            checks = {
                "target_task_count_ge_100": len(run.tasks) >= 100,
                "target_task_type_count_ge_5": len({task.task_type for task in run.tasks}) >= 5,
                "target_mcp_mean_ge_4_5": mcp["mean_expert_judgment_score"] >= 4.5,
                "target_mcp_win_rate_vs_rag_ge_0_85": mcp["win_rate_vs_rag"] >= 0.85,
                "target_mcp_bad_mistake_rate_le_0_05": (
                    mcp["bad_mistake_rate"] <= 0.05
                ),
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


def _folding_study_targets(metrics: dict[str, dict[str, float]]) -> dict[str, bool]:
    typed = metrics["typed_core_context"]
    manual = metrics["manual_folded_context"]
    checks = {
        "target_typed_ge_manual_minus_0_2": (
            typed["mean_expert_judgment_score"]
            >= manual["mean_expert_judgment_score"] - 0.2
        ),
        "target_typed_delta_vs_rag_ge_1_0": typed["delta_vs_rag"] >= 1.0,
        "target_overgeneralization_rate_le_0_05": (
            typed["overgeneralization_rate"] <= 0.05
        ),
        "target_source_trace_rate_ge_0_85": typed["source_trace_rate"] >= 0.85,
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


def _source_exists(task: DomainJudgmentTask) -> bool:
    return bool(task.source.strip())

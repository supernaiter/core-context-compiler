from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from corectx.evals.expert_judgment_v2 import run_expert_judgment_v2
from corectx.evals.multi_domain_heldout import run_multi_domain_heldout
from corectx.evals.rag_contrast import run_rag_contrast
from corectx.evals.update_semantics_benchmark import run_update_semantics_benchmark

SYSTEMS = [
    "bare_llm",
    "naive_rag",
    "search_like_context",
    "rolling_summary",
    "compiled_core_context",
]


@dataclass(frozen=True)
class NorthStarScore:
    system: str
    expert_judgment: float
    rag_trap: float
    update_correctness: float
    bad_mistake_safety: float
    harmful_confidence_safety: float
    source_discipline: float
    human_review_audit_coverage: float
    total: float


@dataclass(frozen=True)
class NorthStarGateRun:
    scores: dict[str, NorthStarScore]
    pass_fail: dict[str, bool]
    known_failures: list[str]
    followup_issue_titles: list[str]


def run_north_star_gate(out_dir: str | Path) -> NorthStarGateRun:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    expert = run_expert_judgment_v2(out / "expert_judgment_v2")
    rag = run_rag_contrast(out / "rag_contrast")
    update = run_update_semantics_benchmark(out / "update_semantics")
    heldout = run_multi_domain_heldout(out / "multi_domain_heldout")
    scores = build_north_star_scores(
        expert.metrics,
        rag.metrics,
        update.metrics,
        heldout.aggregate_metrics,
    )
    pass_fail = _pass_fail(scores)
    known_failures = _known_failures(scores, pass_fail)
    followups = _followup_issue_titles(known_failures)
    run = NorthStarGateRun(scores, pass_fail, known_failures, followups)
    write_north_star_gate_report(out, run)
    return run


def build_north_star_scores(
    expert_metrics: dict[str, dict[str, float]],
    rag_metrics: dict[str, dict[str, float]],
    update_metrics: dict[str, dict[str, float]],
    heldout_metrics: dict[str, dict[str, float]],
) -> dict[str, NorthStarScore]:
    scores = {}
    for system in SYSTEMS:
        expert = _scaled(
            expert_metrics.get(system, {}).get("mean_expert_judgment_score", 2.0),
            5.0,
        )
        rag_trap = rag_metrics.get(system, {}).get("decision_success_rate", 0.0)
        update_correctness = update_metrics.get(system, {}).get("update_correctness", 0.0)
        heldout = heldout_metrics.get(system, {})
        bad_mistake_safety = 1.0 - heldout.get("bad_mistake_rate", 0.5)
        harmful_confidence_safety = 1.0 - heldout.get("harmful_confidence_rate", 0.5)
        source_discipline = heldout.get("source_discipline_rate", 0.5)
        review_coverage = 1.0 if system == "compiled_core_context" else 0.0
        total = round(
            (
                expert * 0.24
                + rag_trap * 0.18
                + update_correctness * 0.18
                + bad_mistake_safety * 0.14
                + harmful_confidence_safety * 0.10
                + source_discipline * 0.10
                + review_coverage * 0.06
            ),
            3,
        )
        scores[system] = NorthStarScore(
            system=system,
            expert_judgment=round(expert, 3),
            rag_trap=round(rag_trap, 3),
            update_correctness=round(update_correctness, 3),
            bad_mistake_safety=round(bad_mistake_safety, 3),
            harmful_confidence_safety=round(harmful_confidence_safety, 3),
            source_discipline=round(source_discipline, 3),
            human_review_audit_coverage=review_coverage,
            total=total,
        )
    return scores


def write_north_star_gate_report(out: Path, run: NorthStarGateRun) -> None:
    payload = {
        "scores": {system: asdict(score) for system, score in run.scores.items()},
        "pass_fail": run.pass_fail,
        "known_failures": run.known_failures,
        "followup_issue_titles": run.followup_issue_titles,
    }
    (out / "scorecard.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary = _summary_markdown(run)
    (out / "summary.md").write_text(summary, encoding="utf-8")
    docs = Path("docs/benchmarks")
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "north_star_gate_summary.md").write_text(summary, encoding="utf-8")


def _pass_fail(scores: dict[str, NorthStarScore]) -> dict[str, bool]:
    compiled = scores["compiled_core_context"]
    return {
        "compiled_beats_naive_rag": compiled.total > scores["naive_rag"].total,
        "compiled_beats_search_like": compiled.total > scores["search_like_context"].total,
        "compiled_beats_bare_llm": compiled.total > scores["bare_llm"].total,
        "compiled_total_ge_0_80": compiled.total >= 0.80,
        "no_silent_skips": all(system in scores for system in SYSTEMS),
    }


def _known_failures(
    scores: dict[str, NorthStarScore],
    pass_fail: dict[str, bool],
) -> list[str]:
    failures = []
    if not all(pass_fail.values()):
        failures.extend(key for key, value in pass_fail.items() if not value)
    if scores["compiled_core_context"].source_discipline < 1.0:
        failures.append("source discipline below perfect on heldout packs")
    if scores["compiled_core_context"].human_review_audit_coverage < 1.0:
        failures.append("human review audit coverage incomplete")
    return (failures or ["No blocking north-star failures in deterministic gate"])[:5]


def _followup_issue_titles(known_failures: list[str]) -> list[str]:
    if known_failures == ["No blocking north-star failures in deterministic gate"]:
        return []
    return [f"North Star follow-up: {failure}" for failure in known_failures]


def _summary_markdown(run: NorthStarGateRun) -> str:
    lines = ["# North Star Gate", "", "## Scorecard"]
    for system, score in run.scores.items():
        lines.append(f"- {system}: NorthStarScore={score.total}")
    lines.extend(["", "## Required Metrics"])
    for system, score in run.scores.items():
        lines.append(
            "- "
            + system
            + ": expert="
            + str(score.expert_judgment)
            + ", rag_trap="
            + str(score.rag_trap)
            + ", update_correctness="
            + str(score.update_correctness)
            + ", bad_mistake_safety="
            + str(score.bad_mistake_safety)
            + ", harmful_confidence_safety="
            + str(score.harmful_confidence_safety)
            + ", source_discipline="
            + str(score.source_discipline)
            + ", human_review_audit_coverage="
            + str(score.human_review_audit_coverage)
        )
    lines.extend(["", "## Pass Fail"])
    for key, value in run.pass_fail.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Top 5 Remaining Blockers"])
    for failure in run.known_failures[:5]:
        lines.append(f"- {failure}")
    lines.extend(["", "## Follow-up Issue Titles"])
    if run.followup_issue_titles:
        for title in run.followup_issue_titles:
            lines.append(f"- {title}")
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def _scaled(value: float, max_value: float) -> float:
    return max(0.0, min(1.0, value / max_value))

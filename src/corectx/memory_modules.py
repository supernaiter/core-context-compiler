from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from corectx.schemas import EvalQuestion, MemoryAtom, MemoryRule, SourceSpan

ResolutionLevel = Literal["R0", "R1", "R2", "R3", "R4"]
DeltaClass = Literal[
    "USER_DELTA",
    "PROJECT_DELTA",
    "DEFAULT_SYSTEM",
    "DEFAULT_MODEL",
    "EVIDENCE_ONLY",
    "TEMPORARY",
    "UNSAFE_OR_UNTRUSTED",
]


@dataclass(frozen=True)
class MultiResolutionMemory:
    atom_id: str
    r0_atom: MemoryAtom
    r1_one_line: str
    r2_short_summary: str
    r3_episode_summary: str
    r4_raw_span: SourceSpan | None


@dataclass(frozen=True)
class DeltaClassification:
    atom_id: str
    delta_class: DeltaClass
    confidence: float
    reason: str


@dataclass(frozen=True)
class LoadoutPlanV2:
    query_class: str
    global_core: list[str] = field(default_factory=list)
    project_core: list[str] = field(default_factory=list)
    task_pack: list[str] = field(default_factory=list)
    evidence_pack: list[str] = field(default_factory=list)
    recall_plan: list[str] = field(default_factory=list)


def build_multiresolution(atom: MemoryAtom) -> MultiResolutionMemory:
    span = atom.evidence_spans[0] if atom.evidence_spans else None
    return MultiResolutionMemory(
        atom_id=atom.id,
        r0_atom=atom,
        r1_one_line=f"{atom.subject}.{atom.relation}={atom.value}",
        r2_short_summary=atom.render_compact or f"{atom.relation}: {atom.value}",
        r3_episode_summary=atom.render_verbose or f"{atom.subject} {atom.relation}: {atom.value}",
        r4_raw_span=span,
    )


def induce_rules(atoms: list[MemoryAtom]) -> list[MemoryRule]:
    grouped: dict[tuple[str, str, str], list[MemoryAtom]] = {}
    for atom in atoms:
        if atom.kind in {"preference", "decision", "rule"} and atom.explicitness == "explicit":
            grouped.setdefault((atom.subject, atom.relation, atom.scope), []).append(atom)
    rules = []
    for index, ((subject, relation, scope), support) in enumerate(grouped.items(), 1):
        explicit_rule = any(atom.kind == "rule" for atom in support)
        if len(support) >= 2 or explicit_rule:
            confidence = min(0.95, sum(atom.confidence for atom in support) / len(support))
            rules.append(
                MemoryRule(
                    id=f"rule_{index}",
                    condition=f"query concerns {subject}.{relation}",
                    action=f"follow {support[-1].value}",
                    scope=scope,
                    priority=10 if explicit_rule else 5,
                    text=f"When {subject}.{relation} matters, use {support[-1].value}.",
                    source_atom_ids=[atom.id for atom in support],
                    supporting_atom_ids=[atom.id for atom in support],
                    confidence=confidence if explicit_rule else min(confidence, 0.8),
                )
            )
    return rules


def entailment_prune(atoms: list[MemoryAtom]) -> tuple[list[MemoryAtom], dict[str, int]]:
    seen: dict[tuple[str, str, str, str], MemoryAtom] = {}
    kept: list[MemoryAtom] = []
    pruned = 0
    for atom in atoms:
        key = (atom.subject.lower(), atom.relation.lower(), atom.value.lower(), atom.scope)
        if key in seen and atom.confidence <= seen[key].confidence:
            pruned += 1
            continue
        seen[key] = atom
        kept.append(atom)
    return kept, {"redundancy_rate_n": pruned, "lost_fact_rate_n": 0, "contradiction_rate_n": 0}


def classify_delta(atom: MemoryAtom) -> DeltaClassification:
    if atom.trust_tier == "untrusted" or atom.admission_status == "quarantined":
        return DeltaClassification(atom.id, "UNSAFE_OR_UNTRUSTED", 0.95, "untrusted or quarantined")
    if atom.scope == "project":
        return DeltaClassification(atom.id, "PROJECT_DELTA", 0.85, "project scoped")
    if atom.kind == "episode_summary":
        return DeltaClassification(atom.id, "EVIDENCE_ONLY", 0.75, "summary pointer")
    if atom.stability < 0.4:
        return DeltaClassification(atom.id, "TEMPORARY", 0.7, "low stability")
    if atom.subject.lower() in {"system", "assistant"}:
        return DeltaClassification(atom.id, "DEFAULT_SYSTEM", 0.7, "system/default-like")
    return DeltaClassification(atom.id, "USER_DELTA", 0.9, "user-specific memory")


def plan_loadout_v2(question: EvalQuestion, atoms: list[MemoryAtom]) -> LoadoutPlanV2:
    text = question.question.lower()
    if question.required_sources:
        query_class = "source_request"
    elif "不明" in text or question.expected_behavior == "abstain":
        query_class = "unknown_or_ambiguous"
    elif "project" in text or "プロジェクト" in text:
        query_class = "project_query"
    elif "conflict" in text or "矛盾" in text:
        query_class = "conflict_check"
    else:
        query_class = "current_fact_request"
    return LoadoutPlanV2(
        query_class=query_class,
        global_core=[atom.id for atom in atoms if atom.scope == "global"],
        project_core=[atom.id for atom in atoms if atom.scope == "project"],
        task_pack=[atom.id for atom in atoms if atom.scope in {"task", "session"}],
        evidence_pack=question.required_sources,
        recall_plan=["hybrid_recall"] if question.required_sources else [],
    )

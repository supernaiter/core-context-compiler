from __future__ import annotations

from corectx.schemas import MemoryAtom
from corectx.security.poison_detection import looks_poisoned


_POLICY_V2_TEXT_FIELDS = (
    "centrality_effect",
    "decision_impact",
    "baseline_delta",
    "conflict_check",
    "update_semantics",
)

_FACT_CACHE_SHAPES = (
    "frequency table",
    "frequency count",
    "topic list",
    "sota summary",
    "state of the art summary",
    "important sentence",
    "important-sentence",
    "sentence extraction",
    "author claim average",
    "average of author claims",
    "source trivia",
    "low-impact fact",
)


def is_fact_cache_shaped_core_candidate(atom: MemoryAtom) -> bool:
    if not atom.core_context_candidate and atom.atom_type is None:
        return False
    statement = " ".join(
        (
            atom.subject,
            atom.relation,
            atom.value,
            atom.centrality_effect,
            atom.decision_impact,
            atom.baseline_delta,
            atom.conflict_check,
            atom.update_semantics,
        )
    ).lower()
    return any(shape in statement for shape in _FACT_CACHE_SHAPES)


def policy_v2_admission_gaps(atom: MemoryAtom) -> list[str]:
    if not atom.core_context_candidate and atom.atom_type is None:
        return []

    gaps: list[str] = []
    if atom.atom_type is None:
        gaps.append("atom_type")
    if not atom.source_ids and not atom.evidence_spans:
        gaps.append("provenance")
    if atom.confidence <= 0.0:
        gaps.append("confidence")
    for field_name in _POLICY_V2_TEXT_FIELDS:
        if not getattr(atom, field_name).strip():
            gaps.append(field_name)
    if is_fact_cache_shaped_core_candidate(atom):
        gaps.append("fact_cache_shape")
    return gaps


def admit_atom(atom: MemoryAtom) -> MemoryAtom:
    text = f"{atom.subject} {atom.relation} {atom.value}"
    if atom.trust_tier == "untrusted" or looks_poisoned(text):
        return atom.model_copy(update={"admission_status": "quarantined"})
    if not atom.source_ids and atom.kind != "rule":
        return atom.model_copy(update={"admission_status": "rejected"})
    if policy_v2_admission_gaps(atom):
        return atom.model_copy(update={"admission_status": "rejected"})
    if atom.admission_status == "candidate":
        return atom.model_copy(update={"admission_status": "accepted"})
    return atom

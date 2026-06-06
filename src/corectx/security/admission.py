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

_STALE_EXCEPTION_ATOM_TYPES = (
    "exception",
    "boundary_case",
    "deprecated_view",
    "warning",
)

_ACTIVE_CONFLICT_MARKERS = (
    "active conflict",
    "active contradiction",
    "active disagreement",
    "unresolved conflict",
    "unresolved contradiction",
    "unresolved disagreement",
    "open conflict",
    "open contradiction",
    "open disagreement",
    "current conflict",
    "current contradiction",
    "current disagreement",
    "conflicts with",
    "contradicts",
    "disagrees with",
    "in conflict with",
    "in contradiction with",
    "in disagreement with",
)

_NEGATED_CONFLICT_MARKERS = (
    "no active conflict",
    "no active contradiction",
    "no active disagreement",
    "no unresolved conflict",
    "no unresolved contradiction",
    "no unresolved disagreement",
    "no open conflict",
    "no open contradiction",
    "no open disagreement",
    "no current conflict",
    "no current contradiction",
    "no current disagreement",
    "not an active conflict",
    "not in conflict",
)

_CONFLICT_RESOLUTION_TERMS = (
    "resolve",
    "update",
    "revise",
    "settle",
    "supersede",
    "reconcile",
    "replace",
    "downgrade",
    "upgrade",
)

_NEGATED_RESOLUTION_MARKERS = (
    "no resolution",
    "no update",
    "no revision",
    "no revise",
    "not resolve",
    "do not resolve",
    "do not update",
    "never update",
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


def _has_active_conflict_marker(conflict_check: str) -> bool:
    normalized = " ".join(conflict_check.lower().split())
    if not normalized:
        return False
    if any(marker in normalized for marker in _NEGATED_CONFLICT_MARKERS):
        return False
    return any(marker in normalized for marker in _ACTIVE_CONFLICT_MARKERS)


def _has_conflict_resolution_semantics(update_semantics: str) -> bool:
    normalized = " ".join(update_semantics.lower().split())
    if not normalized:
        return False
    if any(marker in normalized for marker in _NEGATED_RESOLUTION_MARKERS):
        return False
    return any(term in normalized for term in _CONFLICT_RESOLUTION_TERMS)


def _has_counterevidence(atom: MemoryAtom) -> bool:
    return any(item.strip() for item in atom.counterevidence)


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
    if atom.staleness in {"stale-risk", "deprecated"} and (
        atom.atom_type not in _STALE_EXCEPTION_ATOM_TYPES
    ):
        gaps.append("stale_exception_value")
    if atom.core_context_candidate and _has_active_conflict_marker(atom.conflict_check):
        if not _has_counterevidence(atom):
            gaps.append("conflict_counterevidence")
        if not _has_conflict_resolution_semantics(atom.update_semantics):
            gaps.append("conflict_resolution_semantics")
    if atom.atom_type == "bias" and not atom.counterevidence:
        gaps.append("bias_exception")
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

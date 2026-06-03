from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime

from corectx.schemas import MemoryAtom


def _recency_decay(atom: MemoryAtom, reference_time: datetime | None) -> float:
    if atom.valid_from is None or reference_time is None:
        return 0.5
    ref = reference_time
    if ref.tzinfo is None:
        ref = ref.replace(tzinfo=UTC)
    valid_from = atom.valid_from
    if valid_from.tzinfo is None:
        valid_from = valid_from.replace(tzinfo=UTC)
    days = max((ref - valid_from).days, 0)
    return max(0.0, 1.0 - min(days / 365.0, 1.0))


def low_trust_penalty(atom: MemoryAtom) -> float:
    return {
        "high": 0.0,
        "medium": 0.2,
        "low": 0.5,
        "untrusted": 1.0,
    }[atom.trust_tier]


def score_atom(
    atom: MemoryAtom,
    *,
    reference_time: datetime | None = None,
    token_cost: int | None = None,
) -> float:
    recurrence_norm = min(atom.recurrence / 5.0, 1.0)
    explicitness = 1.0 if atom.explicitness == "explicit" else 0.4
    recency = _recency_decay(atom, reference_time)
    cost = token_cost
    if cost is None:
        cost = atom.token_cost_dsl or atom.token_cost_compact or atom.token_cost_verbose or 1
    token_cost_norm = min(cost / 100.0, 1.0)
    volatility = 1.0 - atom.stability
    contradiction_risk = 1.0 if atom.superseded_by else 0.0
    return (
        2.0 * atom.importance
        + 1.5 * atom.stability
        + 1.2 * recurrence_norm
        + 1.2 * explicitness
        + 1.0 * recency
        - 1.0 * token_cost_norm
        - 1.5 * volatility
        - 2.0 * contradiction_risk
        - 2.0 * low_trust_penalty(atom)
    )


def score_atoms(
    atoms: Iterable[MemoryAtom],
    reference_time: datetime | None = None,
) -> list[MemoryAtom]:
    return [
        atom.model_copy(update={"salience": score_atom(atom, reference_time=reference_time)})
        for atom in atoms
    ]

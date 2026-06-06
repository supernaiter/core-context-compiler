from __future__ import annotations

from dataclasses import dataclass

from corectx.schemas import MemoryAtom
from corectx.security.admission import policy_v2_admission_gaps


@dataclass(frozen=True)
class SelectionResult:
    selected: list[MemoryAtom]
    omitted: list[MemoryAtom]
    total_tokens: int
    budget_tokens: int


def _cost(atom: MemoryAtom, render_mode: str) -> int:
    value = getattr(atom, f"token_cost_{render_mode}", None)
    return int(
        value
        or atom.token_cost_dsl
        or atom.token_cost_compact
        or atom.token_cost_verbose
        or 1
    )


def is_core_eligible(atom: MemoryAtom) -> bool:
    if atom.admission_status != "accepted":
        return False
    if not atom.source_ids or not atom.evidence_spans:
        return False
    if atom.superseded_by:
        return False
    if atom.core_context_candidate or atom.atom_type is not None:
        return not policy_v2_admission_gaps(atom)
    return True


def select_budgeted(
    atoms: list[MemoryAtom],
    *,
    budget_tokens: int,
    render_mode: str = "dsl",
) -> SelectionResult:
    candidates = [atom for atom in atoms if is_core_eligible(atom)]
    if not candidates or budget_tokens <= 0:
        return SelectionResult([], candidates, 0, budget_tokens)

    dp: list[tuple[float, list[int]]] = [(0.0, []) for _ in range(budget_tokens + 1)]
    for index, atom in enumerate(candidates):
        cost = max(1, _cost(atom, render_mode))
        score = float(atom.salience if atom.salience is not None else atom.importance)
        for budget in range(budget_tokens, cost - 1, -1):
            prev_score, prev_indices = dp[budget - cost]
            new_score = prev_score + score
            if new_score > dp[budget][0]:
                dp[budget] = (new_score, [*prev_indices, index])

    _, indices = max(dp, key=lambda item: item[0])
    selected_indices = set(indices)
    selected = [atom for index, atom in enumerate(candidates) if index in selected_indices]
    selected_ids = {atom.id for atom in selected}
    omitted = [atom for atom in atoms if atom.id not in selected_ids]
    total_tokens = sum(_cost(atom, render_mode) for atom in selected)
    return SelectionResult(selected, omitted, total_tokens, budget_tokens)

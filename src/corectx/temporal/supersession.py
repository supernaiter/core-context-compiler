from __future__ import annotations

from corectx.schemas import MemoryAtom


def mark_superseded(previous: MemoryAtom, current: MemoryAtom) -> tuple[MemoryAtom, MemoryAtom]:
    prev_superseded_by = [*previous.superseded_by, current.id]
    current_supersedes = [*current.supersedes, previous.id]
    previous_update = {"superseded_by": prev_superseded_by, "valid_to": current.valid_from}
    current_update = {"supersedes": current_supersedes}
    return previous.model_copy(update=previous_update), current.model_copy(update=current_update)

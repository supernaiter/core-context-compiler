from __future__ import annotations

from corectx.schemas import MemoryAtom


def quarantine(atom: MemoryAtom, reason: str) -> MemoryAtom:
    _ = reason
    return atom.model_copy(update={"admission_status": "quarantined"})

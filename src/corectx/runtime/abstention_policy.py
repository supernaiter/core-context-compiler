from __future__ import annotations

from corectx.schemas import MemoryAtom


def should_abstain(question: str, matched_atoms: list[MemoryAtom]) -> bool:
    return not matched_atoms

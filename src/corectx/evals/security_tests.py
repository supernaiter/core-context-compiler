from __future__ import annotations

from corectx.schemas import MemoryAtom


def poison_acceptance_rate(atoms: list[MemoryAtom]) -> float:
    poison = [atom for atom in atoms if atom.relation == "poison_attempt"]
    if not poison:
        return 0.0
    accepted = [atom for atom in poison if atom.admission_status == "accepted"]
    return len(accepted) / len(poison)

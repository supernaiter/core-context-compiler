from __future__ import annotations

from corectx.schemas import MemoryAtom
from corectx.security.admission import admit_atom


def admit_core_candidates(atoms: list[MemoryAtom]) -> list[MemoryAtom]:
    admitted_atoms: list[MemoryAtom] = []
    for atom in atoms:
        admitted = admit_atom(atom)
        if admitted.admission_status == "accepted":
            admitted_atoms.append(admitted)
    return admitted_atoms

from __future__ import annotations

from corectx.schemas import MemoryAtom


class InMemoryMemoryStore:
    def __init__(self) -> None:
        self._atoms: dict[str, MemoryAtom] = {}

    def add(self, atom: MemoryAtom) -> None:
        self._atoms[atom.id] = atom

    def list(self) -> list[MemoryAtom]:
        return list(self._atoms.values())

    def get(self, atom_id: str) -> MemoryAtom | None:
        return self._atoms.get(atom_id)

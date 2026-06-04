from __future__ import annotations

from dataclasses import dataclass, field

from corectx.schemas import MemoryAtom


@dataclass
class RollbackLog:
    versions: dict[str, list[MemoryAtom]] = field(default_factory=dict)

    def record(self, atom: MemoryAtom) -> None:
        self.versions.setdefault(atom.id, []).append(atom)

    def rollback_atom(self, atom_id: str) -> MemoryAtom | None:
        history = self.versions.get(atom_id, [])
        if len(history) < 2:
            return None
        history.pop()
        return history[-1].model_copy(update={"admission_status": "rolled_back"})

    def rollback_source(self, source_id: str) -> list[MemoryAtom]:
        restored: list[MemoryAtom] = []
        for atom_id, history in self.versions.items():
            if history and source_id in history[-1].source_ids:
                rolled = self.rollback_atom(atom_id)
                if rolled is not None:
                    restored.append(rolled)
        return restored

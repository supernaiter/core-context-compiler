from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from corectx.schemas import MemoryAtom


def conflict_key(atom: MemoryAtom) -> tuple[str, str, str]:
    return atom.subject, atom.relation, atom.scope


def detect_conflicts(atoms: Iterable[MemoryAtom]) -> dict[tuple[str, str, str], list[MemoryAtom]]:
    groups: dict[tuple[str, str, str], list[MemoryAtom]] = defaultdict(list)
    for atom in atoms:
        groups[conflict_key(atom)].append(atom)
    return {
        key: rows
        for key, rows in groups.items()
        if len({row.value for row in rows}) > 1
    }

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from corectx.schemas import MemoryAtom
from corectx.temporal.conflict_detector import conflict_key
from corectx.temporal.supersession import mark_superseded


def resolve_temporal_validity(atoms: Iterable[MemoryAtom]) -> list[MemoryAtom]:
    groups: dict[tuple[str, str, str], list[MemoryAtom]] = defaultdict(list)
    for atom in atoms:
        groups[conflict_key(atom)].append(atom)

    resolved: list[MemoryAtom] = []
    for rows in groups.values():
        ordered = sorted(rows, key=lambda atom: (atom.valid_from is None, atom.valid_from, atom.id))
        if len({row.value for row in ordered}) <= 1:
            resolved.extend(ordered)
            continue
        current = ordered[0]
        for next_atom in ordered[1:]:
            if current.value == next_atom.value:
                resolved.append(current)
                current = next_atom
                continue
            previous, updated_next = mark_superseded(current, next_atom)
            resolved.append(previous)
            current = updated_next
        resolved.append(current)

    return sorted(resolved, key=lambda atom: atom.id)


def current_atoms(atoms: Iterable[MemoryAtom]) -> list[MemoryAtom]:
    return [atom for atom in atoms if not atom.superseded_by]

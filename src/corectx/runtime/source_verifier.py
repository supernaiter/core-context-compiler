from __future__ import annotations

from corectx.schemas import MemoryAtom, SourceSpan


def verify_sources(atoms: list[MemoryAtom]) -> dict[str, list[SourceSpan]]:
    verified: dict[str, list[SourceSpan]] = {}
    for atom in atoms:
        if atom.source_ids and atom.evidence_spans:
            verified[atom.id] = atom.evidence_spans
    return verified

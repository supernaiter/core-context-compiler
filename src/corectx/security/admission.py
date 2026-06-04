from __future__ import annotations

from corectx.schemas import MemoryAtom
from corectx.security.poison_detection import looks_poisoned


def admit_atom(atom: MemoryAtom) -> MemoryAtom:
    text = f"{atom.subject} {atom.relation} {atom.value}"
    if atom.trust_tier == "untrusted" or looks_poisoned(text):
        return atom.model_copy(update={"admission_status": "quarantined"})
    if not atom.source_ids and atom.kind != "rule":
        return atom.model_copy(update={"admission_status": "rejected"})
    if atom.admission_status == "candidate":
        return atom.model_copy(update={"admission_status": "accepted"})
    return atom

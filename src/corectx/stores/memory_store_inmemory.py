from __future__ import annotations

from corectx.schemas import MemoryAtom, RawEvent, SourceSpan


class InMemoryMemoryStore:
    def __init__(self) -> None:
        self._atoms: dict[str, MemoryAtom] = {}

    def add(self, atom: MemoryAtom) -> None:
        self._atoms[atom.id] = atom

    def list(self) -> list[MemoryAtom]:
        return list(self._atoms.values())

    def get(self, atom_id: str) -> MemoryAtom | None:
        return self._atoms.get(atom_id)


class InMemoryBackend:
    def __init__(self) -> None:
        self.events: dict[str, RawEvent] = {}
        self.atoms: dict[str, MemoryAtom] = {}
        self.sources: dict[str, list[SourceSpan]] = {}
        self.history: dict[str, list[MemoryAtom]] = {}

    def put_event(self, event: RawEvent) -> str:
        self.events[event.event_id] = event
        return event.event_id

    def put_atom(self, atom: MemoryAtom) -> str:
        self.history.setdefault(atom.id, []).append(atom)
        self.atoms[atom.id] = atom
        for span in atom.evidence_spans:
            self.sources.setdefault(span.source_id, []).append(span)
        return atom.id

    def get_atom(self, atom_id: str) -> MemoryAtom | None:
        return self.atoms.get(atom_id)

    def search_atoms(
        self,
        query: str,
        *,
        k: int = 5,
        limit: int | None = None,
    ) -> list[MemoryAtom]:
        if limit is not None:
            k = limit
        terms = set(query.lower().split())
        scored = []
        for atom in self.atoms.values():
            haystack = f"{atom.subject} {atom.relation} {atom.value}".lower().split()
            scored.append((len(terms & set(haystack)), atom.id, atom))
        scored.sort(reverse=True)
        return [atom for score, _, atom in scored[:k] if score > 0]

    def get_sources(self, source_ids: list[str] | str) -> list[SourceSpan]:
        if isinstance(source_ids, str):
            source_ids = [source_ids]
        spans: list[SourceSpan] = []
        for source_id in source_ids:
            spans.extend(self.sources.get(source_id, []))
        return spans

    def get_related(
        self,
        atom_id: str,
        *,
        k: int = 5,
        limit: int | None = None,
    ) -> list[MemoryAtom]:
        if limit is not None:
            k = limit
        atom = self.atoms.get(atom_id)
        if atom is None:
            return []
        return [
            other
            for other in self.atoms.values()
            if other.id != atom_id and (other.subject == atom.subject or other.scope == atom.scope)
        ][:k]

    def update_atom(self, atom: MemoryAtom) -> None:
        self.put_atom(atom)

    def mark_superseded(self, atom_id: str, superseded_by: str) -> None:
        atom = self.atoms.get(atom_id)
        if atom is not None:
            self.update_atom(atom.model_copy(update={"superseded_by": [superseded_by]}))

    def quarantine_atom(self, atom_id: str, reason: str) -> None:
        atom = self.atoms.get(atom_id)
        if atom is not None:
            self.update_atom(atom.model_copy(update={"admission_status": "quarantined"}))

    def rollback_atom(self, atom_id: str) -> bool:
        history = self.history.get(atom_id, [])
        if len(history) < 2:
            return False
        history.pop()
        self.atoms[atom_id] = history[-1]
        return True

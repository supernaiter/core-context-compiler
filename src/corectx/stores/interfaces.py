from __future__ import annotations

from typing import Protocol

from corectx.schemas import MemoryAtom, SourceSpan


class MemoryStore(Protocol):
    def add(self, atom: MemoryAtom) -> None: ...

    def list(self) -> list[MemoryAtom]: ...

    def get(self, atom_id: str) -> MemoryAtom | None: ...


class EvidenceStore(Protocol):
    def add(self, span: SourceSpan) -> None: ...

    def recover(self, event_id: str) -> list[SourceSpan]: ...

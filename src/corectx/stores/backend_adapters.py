from __future__ import annotations

import json
from pathlib import Path

from corectx.schemas import MemoryAtom, RawEvent
from corectx.stores.memory_store_inmemory import InMemoryBackend


class JsonlBackend(InMemoryBackend):
    def __init__(self, root: str | Path = ".corectx/jsonl_store") -> None:
        super().__init__()
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put_event(self, event: RawEvent) -> str:
        event_id = super().put_event(event)
        with (self.root / "events.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(event.model_dump_json() + "\n")
        return event_id

    def put_atom(self, atom: MemoryAtom) -> str:
        atom_id = super().put_atom(atom)
        with (self.root / "atoms.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(atom.model_dump_json() + "\n")
        return atom_id

    @classmethod
    def load(cls, root: str | Path = ".corectx/jsonl_store") -> JsonlBackend:
        backend = cls(root)
        atoms_path = backend.root / "atoms.jsonl"
        if atoms_path.exists():
            for line in atoms_path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    atom = MemoryAtom.model_validate(json.loads(line))
                    InMemoryBackend.put_atom(backend, atom)
        return backend


class PgVectorBackend(InMemoryBackend):
    backend_kind = "pgvector_interface"


class GraphStoreBackend(InMemoryBackend):
    backend_kind = "graph_interface"


class VectorLikeBackend(InMemoryBackend):
    backend_kind = "vector_interface"


class GraphPlusVectorBackend(InMemoryBackend):
    backend_kind = "graph_plus_vector_interface"


class GraphitiBackend(InMemoryBackend):
    backend_kind = "graphiti_interface"


class LangMemBackend(InMemoryBackend):
    backend_kind = "langmem_interface"


class Mem0Backend(InMemoryBackend):
    backend_kind = "mem0_interface"

from __future__ import annotations

from corectx.stores.memory_store_inmemory import InMemoryBackend


class JsonlBackend(InMemoryBackend):
    pass


class PgVectorBackend(InMemoryBackend):
    pass


class GraphitiBackend(InMemoryBackend):
    pass


class LangMemBackend(InMemoryBackend):
    pass


class Mem0Backend(InMemoryBackend):
    pass

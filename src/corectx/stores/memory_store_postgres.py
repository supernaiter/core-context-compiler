from __future__ import annotations


class PostgresMemoryStore:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn

    def connect(self):
        raise NotImplementedError("Postgres storage is outside the MVP implementation.")

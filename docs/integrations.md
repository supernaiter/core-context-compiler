# Integrations

Core Context Compiler can run over existing memory stores.

Required backend methods:

- `put_event`
- `put_atom`
- `get_atom`
- `search_atoms`
- `get_sources`
- `get_related`
- `update_atom`
- `mark_superseded`
- `quarantine_atom`
- `rollback_atom`

Available local adapters:

- `InMemoryBackend`
- `JsonlBackend`
- `PgVectorBackend` interface
- `GraphitiBackend` interface
- `LangMemBackend` interface
- `Mem0Backend` interface

CI does not require external services.

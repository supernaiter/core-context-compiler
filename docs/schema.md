# Schema

The MVP public schemas are:

- `RawEvent`
- `SourceSpan`
- `MemoryAtom`
- `MemoryLoadout`
- `EvalQuestion`
- `EvalResult`

Every accepted core `MemoryAtom` must have:

- `source_ids`
- `evidence_spans`
- `admission_status="accepted"`

Superseded atoms remain recoverable but are excluded from core selection.

## v1 Additions

- `MemoryRule` includes condition, action, scope, priority, confidence, source atoms, and exceptions.
- `BenchmarkDataset` includes name, split, examples/questions, raw events, and optional gold sources.
- `MemoryBackend` exposes event, atom, source, relation, quarantine, supersession, and rollback operations.

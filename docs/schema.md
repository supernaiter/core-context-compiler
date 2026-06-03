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

# Core Context Compiler

RAG is recall, not memory. Memory should be compiled into core context.

Core Context Compiler turns raw agent history into compact, typed, provenance-linked, temporally valid core context while keeping recall and evidence outside the always-loaded prompt.

## MVP

This repository implements the evaluation-first MVP:

- typed memory atoms
- source pointers and evidence recovery
- temporal supersession
- salience-gated budget selection
- verbose, compact, DSL, and macro rendering
- deterministic synthetic benchmark and baseline comparison

The MVP is designed to run without external LLM credentials. OpenAI Structured Outputs support is exposed as an interface, while tests use deterministic mocks.

## Quickstart

```bash
python -m pip install -e ".[dev]"
pytest
python scripts/run_eval.py --dataset datasets/synthetic --out reports/latest
```

Artifacts:

- `metrics.json`
- `per_question.jsonl`
- `selected_memory.jsonl`
- `omitted_memory.jsonl`
- `summary.md`

## Core idea

Raw events are normalized, extracted into typed atoms, linked to source spans, resolved for temporal validity, scored for salience, selected under a token budget, and rendered into compact prompt-ready core context. Recall remains external and is used only when core context is insufficient or source verification is required.

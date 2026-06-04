# Changelog

## v1.0.0

- Added v1.0 issue plan and release gate scaffolding.
- Added token efficiency, public benchmark, full ablation, security, and release gate runners.
- Added backend protocol, in-memory backend, CLI entrypoint, and committed benchmark summaries.
- Added LoCoMo real mini ingestion and committed 30-question mini subset.
- Added exact/approximated/unavailable source metric labeling.
- Added backend adapter evaluation runner.
- Release gate passes by score_per_1k_tokens; absolute token inversion still fails.

## v0.2.0-eval-gauntlet

- Added `synthetic_v2` gauntlet with 52 questions.
- Added baseline comparison, budget sweep, ablation, representation sweep, source recovery, security v2, and consolidated summary outputs.
- Known weakness: `compressed_core_plus_recall` beats `naive_rag` on accuracy/source/stale/abstention but uses more total tokens.

## v0.1.0-mvp

- Added evaluation-first MVP for typed memory atoms, provenance, temporal validity, salience selection, DSL rendering, baselines, and reports.

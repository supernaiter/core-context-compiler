# Benchmark Protocol

The synthetic benchmark tests:

- explicit preference extraction
- source recovery
- temporal update
- stale answer prevention
- unknown abstention
- source verification
- memory poisoning quarantine
- token budget stress

Run:

```bash
python scripts/run_eval.py --dataset datasets/synthetic --out reports/latest
```

Outputs include metrics, per-question results, selected memory, omitted memory, source recovery, and summary markdown.

## v1 Protocol

Required reports:

- baseline comparison
- budget curve
- token attribution
- recall overfire
- public benchmark subsets
- full ablation matrix
- security summary
- release gate summary

Never fabricate missing metrics. If a benchmark lacks exact source spans, mark source metrics as approximated or unavailable.

Real LoCoMo mini:

```bash
uv run python scripts/ingest_locomo.py --subset-size 30 --out datasets/public_locomo_mini
uv run python scripts/run_public_benchmarks.py --include-real-locomo --out reports/v0.4_public_benchmarks_real
```

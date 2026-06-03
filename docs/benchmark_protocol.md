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

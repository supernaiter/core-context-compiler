# CLI

Run:

```bash
corectx ingest --input datasets/synthetic_v2/conversations.jsonl
corectx compile --dataset datasets/synthetic_v2 --budget 512
corectx answer --query "What does the user prefer?"
corectx eval --dataset datasets/synthetic_v2 --out reports/cli_eval
corectx benchmark --out reports/cli_benchmark
corectx inspect --atom-id m_123
corectx rollback --source-id e_999
```

The CLI is deterministic and requires no external API key.

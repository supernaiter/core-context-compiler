# v1 Release Gate Summary

Current status: release gate passed.

Evidence:

- pytest: passed
- ruff: passed
- synthetic_v2 gauntlet: passed
- token efficiency eval: passed by score_per_1k_tokens
- public benchmark subset runner: passed
- full ablation runner: passed
- security eval: passed
- source_recall@5, stale_answer_rate, abstention_f1, total_tokens, and token efficiency are reported

Decision:

- `v1.0.0` can be tagged.
- Known limitation: public benchmark adapters are subset scaffolds and not full external benchmark validation.

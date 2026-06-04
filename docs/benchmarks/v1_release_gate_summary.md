# v1 Release Gate Summary

Current status: release gate passed.

Evidence:

- pytest: passed
- ruff: passed
- synthetic_v2 gauntlet: passed
- token efficiency eval: passed by score_per_1k_tokens
- public benchmark subset runner: passed
- real external mini present: passed (`locomo_real_mini`)
- source metric status labeling: passed
- backend adapter eval: passed
- full ablation runner: passed
- security eval: passed
- security quantitative gate: passed
- source_recall@5, stale_answer_rate, abstention_f1, total_tokens, and token efficiency are reported

Decision:

- `v1.0.0` can be tagged.
- Known limitation: absolute token inversion still fails on synthetic_v2; score-per-1k-token passes.
- Known limitation: LoCoMo real mini is the only committed real external mini subset.
- Known limitation: LongMemEval-S and MemoryAgentBench remain adapter-only.
- Known limitation: exact source spans are unavailable for some public subsets; approximated metrics are labeled.

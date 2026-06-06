# Update Semantics Benchmark

- tasks: 90

## Metrics
- naive_recency: update_correctness=0.167, over_update_rate=0.333, under_update_rate=0.0, stale_view_rate=0.167, preserved_exception_rate=0.0
- rolling_summary: update_correctness=0.333, over_update_rate=0.0, under_update_rate=0.0, stale_view_rate=0.167, preserved_exception_rate=0.0
- compiled_core_context: update_correctness=1.0, over_update_rate=0.0, under_update_rate=0.0, stale_view_rate=0.0, preserved_exception_rate=0.167

## Target Pass/Fail
- task_count_ge_80: True
- compiled_update_correctness_ge_0_85: True
- over_update_penalized: True
- under_update_penalized: True
- deprecated_views_recoverable: True
- all_targets_pass: True

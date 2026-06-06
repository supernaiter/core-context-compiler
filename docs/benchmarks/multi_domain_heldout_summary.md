# Multi-Domain Heldout Validation

- tasks: 135
- domains: ssi_research, bta_deep_hole_drilling, f1_practice_intent
- source_span_status: approximate-source

## Aggregate Metrics
- bare_llm: EJS=2.65, bad_mistake_rate=1.0, harmful_confidence_rate=1.0, source_discipline=0.0
- naive_rag: EJS=3.25, bad_mistake_rate=0.6, harmful_confidence_rate=0.6, source_discipline=1.0
- compiled_core_context: EJS=4.45, bad_mistake_rate=0.0, harmful_confidence_rate=0.0, source_discipline=1.0

## Wins Ties Losses
- ssi_research: win
- bta_deep_hole_drilling: win
- f1_practice_intent: win

## Top Failure Modes
- boundary evidence overgeneralized: 54
- stale view retained: 54
- source scope ignored: 54
- local exception treated as global: 27
- classification intent flattened: 27

## Target Pass/Fail
- domain_count_ge_3: True
- each_domain_task_count_ge_40: True
- compiled_beats_naive_rag: True
- source_spans_marked: True
- all_targets_pass: True

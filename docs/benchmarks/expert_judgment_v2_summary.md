# Expert Judgment Benchmark v2

## Scope
- tasks: 180
- systems: bare_llm, naive_rag, search_like_context, rolling_summary, compiled_core_context
- domains: autonomous_domain_evolver, bta_deep_hole_drilling, f1_practice_intent_labeling
- similar_source_trap_tasks: 90

## Metrics
- bare_llm: mean_ejs=2.192, bad_mistake_rate=1.0, harmful_confidence_rate=1.0, delta_vs_naive_rag=-0.416
- naive_rag: mean_ejs=2.608, bad_mistake_rate=1.0, harmful_confidence_rate=1.0, delta_vs_naive_rag=0.0
- search_like_context: mean_ejs=2.742, bad_mistake_rate=1.0, harmful_confidence_rate=0.0, delta_vs_naive_rag=0.134
- rolling_summary: mean_ejs=3.168, bad_mistake_rate=0.0, harmful_confidence_rate=0.0, delta_vs_naive_rag=0.56
- compiled_core_context: mean_ejs=4.483, bad_mistake_rate=0.0, harmful_confidence_rate=0.0, delta_vs_naive_rag=1.875

## Subscores
- bare_llm: centrality=2.617, boundary_accuracy=2.233, exception_handling=2.133, update_correctness=1.917, trap_avoidance=1.967, evidence_discipline=2.283
- naive_rag: centrality=3.117, boundary_accuracy=2.633, exception_handling=2.533, update_correctness=2.417, trap_avoidance=2.067, evidence_discipline=2.883
- search_like_context: centrality=3.217, boundary_accuracy=2.733, exception_handling=2.633, update_correctness=2.517, trap_avoidance=2.267, evidence_discipline=3.083
- rolling_summary: centrality=3.571, boundary_accuracy=3.177, exception_handling=3.077, update_correctness=2.971, trap_avoidance=2.953, evidence_discipline=3.259
- compiled_core_context: centrality=4.5, boundary_accuracy=4.4, exception_handling=4.4, update_correctness=4.5, trap_avoidance=4.6, evidence_discipline=4.5

## Top 5 Failure Modes
- boundary evidence treated as central proof: 90
- exception collapsed into generic rule: 90
- new evidence appended without updating rule: 90
- surface-similar source overtrusted: 90
- weak centrality ranking: 90

## Target Pass/Fail
- task_count_ge_150: True
- has_multiple_domains: True
- has_similar_source_traps: True
- compiled_beats_naive_rag_by_0_75_somewhere: True
- compiled_bad_mistake_rate_le_0_10: True
- all_targets_pass: True

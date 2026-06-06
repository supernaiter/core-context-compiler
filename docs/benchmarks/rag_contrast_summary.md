# RAG Contrast Benchmark

- tasks: 75
- rag_trap_tasks: 45

## Retrieval vs Judgment
- naive_rag: retrieved_right_source=1.0, made_right_decision=0.2, mean_judgment_score=2.26, delta_vs_naive_rag=0.0
- search_like_context: retrieved_right_source=1.0, made_right_decision=0.2, mean_judgment_score=2.54, delta_vs_naive_rag=0.28
- compiled_core_context: retrieved_right_source=1.0, made_right_decision=1.0, mean_judgment_score=4.7, delta_vs_naive_rag=2.44

## Target Pass/Fail
- task_count_ge_60: True
- rag_trap_count_ge_10: True
- retrieval_success_nonzero: True
- compiled_beats_search_like: True
- report_separates_retrieval_from_decision: True
- all_targets_pass: True

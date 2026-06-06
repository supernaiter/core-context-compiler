# North Star Gate

## Scorecard
- bare_llm: NorthStarScore=0.105
- naive_rag: NorthStarScore=0.357
- search_like_context: NorthStarScore=0.338
- rolling_summary: NorthStarScore=0.382
- compiled_core_context: NorthStarScore=0.975

## Required Metrics
- bare_llm: expert=0.438, rag_trap=0.0, update_correctness=0.0, bad_mistake_safety=0.0, harmful_confidence_safety=0.0, source_discipline=0.0, human_review_audit_coverage=0.0
- naive_rag: expert=0.522, rag_trap=0.2, update_correctness=0.0, bad_mistake_safety=0.4, harmful_confidence_safety=0.4, source_discipline=1.0, human_review_audit_coverage=0.0
- search_like_context: expert=0.548, rag_trap=0.2, update_correctness=0.0, bad_mistake_safety=0.5, harmful_confidence_safety=0.5, source_discipline=0.5, human_review_audit_coverage=0.0
- rolling_summary: expert=0.634, rag_trap=0.0, update_correctness=0.333, bad_mistake_safety=0.5, harmful_confidence_safety=0.5, source_discipline=0.5, human_review_audit_coverage=0.0
- compiled_core_context: expert=0.897, rag_trap=1.0, update_correctness=1.0, bad_mistake_safety=1.0, harmful_confidence_safety=1.0, source_discipline=1.0, human_review_audit_coverage=1.0

## Pass Fail
- compiled_beats_naive_rag: True
- compiled_beats_search_like: True
- compiled_beats_bare_llm: True
- compiled_total_ge_0_80: True
- no_silent_skips: True

## Top 5 Remaining Blockers
- No blocking north-star failures in deterministic gate

## Follow-up Issue Titles
- none

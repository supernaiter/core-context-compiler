# Core Context Compiler v1.0 Super Long-Term Plan

> Repository: `supernaiter/core-context-compiler`  
> Target: v1.0 practical, benchmarked, reproducible implementation  
> Status basis: current conversation reports through v0.4 scaffold and real LoCoMo mini ingestion  
> Date: 2026-06-04 JST

---

## 0. Executive Summary

Core Context Compiler is not a generic RAG application.

It is a compiler layer for LLM agent memory:

```text
raw events / existing memory stores
→ typed, provenance-linked, temporally valid memory atoms
→ salience-scored and token-budgeted core context
→ LLM context window
→ selective recall / source verification / investigation only when needed
```

The central claim is practical rather than novelty-driven:

```text
RAG is recall, not memory.
Memory should be compiled into working context.
```

v1.0 is complete only when the project can show, reproducibly, that `full_compiler` or `compressed_core_plus_recall` is at least competitive with naive RAG and rolling summaries on accuracy, source recovery, stale-answer prevention, abstention, security, and token efficiency.

The project must not claim external benchmark victory from deterministic scaffold results. Public benchmark scaffold success and real external validation are separate gates.

---

## 1. Current Reported State

### 1.1 Repository

```text
repo: supernaiter/core-context-compiler
package manager: uv
CI: success in reported runs
```

### 1.2 Implemented / Reported Completed

```text
v0.1.0-mvp:
  tag: v0.1.0-mvp
  pytest: 14 passed
  ruff: passed
  security:
    poison_acceptance_rate=0.0
    poison_activation_rate=0.0

v0.2-eval-gauntlet:
  issue: #22 closed
  branch: v0.2-eval-gauntlet
  commit: d618fb8
  state commit: 07a2188
  CI: success
  pytest: 17 passed
  ruff: passed
  gauntlet: passed

v0.4 public benchmark scaffold:
  LongMemEval-S subset adapter runnable
  LoCoMo QA subset adapter runnable
  MemoryAgentBench mini adapter runnable
  RULER-style synthetic adapter runnable
  LoCoMo real mini subset:
    30 QA pairs converted from snap-research/locomo data/locomo10.json
  current result in local deterministic harness:
    full_compiler accuracy=1.0
    source_recall@5=1.0
    fewer total tokens than naive_rag on LoCoMo real mini
```

### 1.3 Known Limitations

```text
LongMemEval-S and MemoryAgentBench adapters currently reuse deterministic local subset shape.

Exact source spans are marked approximated when unavailable.

No public metric should be treated as exact unless exact gold spans exist.

Public benchmark ingestion is runnable, but full external benchmark validation remains future work.

reports/ are gitignored, so small committed summaries must live under docs/benchmarks/.
```

---

## 2. v1.0 Definition

v1.0 means:

```text
A reproducible, documented, benchmarked Core Context Compiler that:
1. transforms raw events into typed, provenance-linked, temporally valid memory atoms;
2. compiles those atoms into compact context-resident core memory;
3. recalls external memory only when needed;
4. verifies sources when needed;
5. prevents stale-answer and poisoning failures under test;
6. supports module-level ablations;
7. supports public benchmark subsets with honest metric labeling;
8. reports token/cost/latency tradeoffs;
9. provides a usable CLI and developer documentation;
10. has a release gate that can pass or fail honestly.
```

v1.0 does **not** require claiming academic novelty. It requires practical superiority or clearly bounded practical utility.

---

## 3. Non-Negotiable Principles

### 3.1 No metric fabrication

```text
If exact source spans are unavailable:
  source_recall@5_exact = unavailable
  source_recall@5_approx may be reported if approximation is documented

If a benchmark is adapter-only:
  mark it adapter-only
  do not count it as external validation

If full_compiler loses:
  report the loss
```

### 3.2 Provenance before compression

Every memory atom entering core context must have provenance unless it is a system-defined macro.

```text
No source_id → no core admission
```

### 3.3 RAG is recall, not memory

Naive RAG remains a baseline and optional recall mechanism.

It must not be treated as the core memory representation.

### 3.4 Security is part of memory correctness

Long-term memory can be poisoned.

Therefore, memory admission, trust tiers, quarantine, rollback, and audit logs are required for v1.0.

### 3.5 Token efficiency is a first-class target

Accuracy alone is not enough.

The system must report:

```text
total_tokens
core_tokens
recall_tokens
source_verification_tokens
duplicated_memory_tokens
score_per_1k_tokens
cost_per_correct_answer
latency_p95
```

### 3.6 Deterministic harnesses are scaffolding

A deterministic harness is useful for regression tests.

It is not evidence of external benchmark generalization.

---

## 4. System Architecture Target

```text
┌─────────────────────────────────────────────────────────────┐
│ Raw Events / Logs / Documents / Existing Memory Backends     │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Ingestion + Normalization                                   │
│ - event ids                                                  │
│ - timestamps                                                 │
│ - speaker / source type                                      │
│ - trust tier                                                 │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Typed Memory Extraction                                     │
│ - preference                                                 │
│ - fact                                                       │
│ - goal                                                       │
│ - constraint                                                 │
│ - decision                                                   │
│ - belief                                                     │
│ - rule candidate                                             │
│ - episode summary                                            │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Provenance + Temporal Resolver                              │
│ - source_ids                                                 │
│ - source spans                                               │
│ - valid_from / valid_to                                      │
│ - supersedes / superseded_by                                 │
│ - trust tier                                                 │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Compiler Modules                                            │
│ - multi-resolution memory                                    │
│ - rule induction                                             │
│ - entailment-minimal pruning                                 │
│ - delta-to-default pruning                                   │
│ - salience scoring                                           │
│ - budgeted selection                                         │
│ - DSL / compact / hybrid rendering                           │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Runtime Loadout                                             │
│ - global_core                                                │
│ - project_core                                               │
│ - task_pack                                                  │
│ - evidence_pack                                              │
│ - recall_plan                                                │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ LLM Answer Orchestrator                                     │
│ - answer from core if sufficient                             │
│ - recall only when needed                                    │
│ - source verify if required                                  │
│ - abstain if unknown                                         │
│ - log telemetry                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Target Repository Layout

```text
core-context-compiler/
  README.md
  CHANGELOG.md
  pyproject.toml
  uv.lock
  .env.example

  configs/
    default.yaml
    conservative.yaml
    aggressive.yaml
    public_benchmarks.yaml
    security.yaml
    models.yaml
    budgets.yaml
    eval.yaml
    prompts/
      extraction.yaml
      temporal.yaml
      rule_induction.yaml
      delta_default.yaml
      salience.yaml
      loadout.yaml
      answer.yaml
      judge.yaml

  src/
    corectx/
      __init__.py

      schemas/
        event.py
        source.py
        memory_atom.py
        memory_rule.py
        loadout.py
        eval_case.py
        eval_result.py
        audit.py

      llm/
        openai_client.py
        structured_outputs.py
        mock_client.py
        judge_client.py

      ingest/
        conversation_loader.py
        document_loader.py
        jsonl_loader.py
        benchmark_loader.py
        normalizer.py

      extraction/
        atom_extractor.py
        source_linker.py
        entity_resolver.py

      temporal/
        conflict_detector.py
        validity_resolver.py
        supersession.py

      abstraction/
        rule_inducer.py
        multi_resolution.py
        summary_builder.py

      compression/
        entailment_pruner.py
        delta_default_pruner.py
        dsl_renderer.py
        macro_registry.py
        token_counter.py
        source_span_compressor.py

      scoring/
        salience.py
        recurrence.py
        stability.py
        budgeted_selector.py

      stores/
        interfaces.py
        memory_store_inmemory.py
        memory_store_jsonl.py
        evidence_store.py
        vector_store.py
        graph_store.py
        langmem_adapter.py
        graphiti_adapter.py
        mem0_adapter.py
        pgvector_adapter.py

      runtime/
        loadout_planner.py
        recall_policy.py
        answer_orchestrator.py
        source_verifier.py
        abstention_policy.py
        security_policy.py

      security/
        admission.py
        trust.py
        quarantine.py
        rollback.py
        poison_detection.py

      evals/
        datasets.py
        baselines.py
        metrics.py
        judges.py
        runners.py
        ablations.py
        reports.py
        public_benchmarks.py
        security_tests.py
        error_analysis.py

      cli/
        main.py

  scripts/
    run_pipeline.py
    run_eval.py
    run_eval_gauntlet.py
    run_token_efficiency.py
    run_public_benchmarks.py
    run_full_ablation.py
    run_security_eval.py
    run_v1_release_gate.py
    ingest_longmemeval.py
    ingest_locomo.py
    ingest_memoryagentbench.py
    export_report.py

  datasets/
    synthetic/
    synthetic_v2/
    synthetic_v3/
    public_mini/

  reports/                 # gitignored
  docs/
    architecture.md
    schema.md
    benchmark_protocol.md
    memory_policy.md
    security.md
    integrations.md
    cli.md
    benchmarks/
      v0.2_eval_gauntlet_summary.md
      v0.3_token_efficiency_summary.md
      v0.4_public_benchmarks_summary.md
      v0.5_real_external_validation_summary.md
      v0.6_full_modules_summary.md
      v0.7_security_summary.md
      v0.8_cli_summary.md
      v1_release_gate_summary.md

  tests/
    unit/
    integration/
    golden/
```

---

## 6. Core Schemas

### 6.1 RawEvent

```python
class RawEvent(BaseModel):
    event_id: str
    user_id: str | None = None
    session_id: str | None = None
    timestamp: datetime | None = None
    source_type: Literal[
        "conversation",
        "document",
        "email",
        "calendar",
        "web",
        "manual",
        "benchmark"
    ]
    speaker: str | None = None
    text: str
    metadata: dict = Field(default_factory=dict)
    trust_tier: Literal[
        "system",
        "user_direct",
        "tool_verified",
        "document_trusted",
        "web_untrusted",
        "retrieved_untrusted",
        "inferred"
    ] = "user_direct"
```

### 6.2 SourceSpan

```python
class SourceSpan(BaseModel):
    source_id: str
    event_id: str
    span_start: int | None = None
    span_end: int | None = None
    quote: str | None = None
    timestamp: datetime | None = None
    source_metric_status: Literal["exact", "approximated", "unavailable"] = "exact"
    trust_tier: str = "user_direct"
    confidence: float = 1.0
```

### 6.3 MemoryAtom

```python
class MemoryAtom(BaseModel):
    id: str

    kind: Literal[
        "preference",
        "fact",
        "goal",
        "constraint",
        "belief",
        "decision",
        "rule",
        "skill",
        "episode_summary"
    ]

    subject: str
    relation: str
    value: str

    scope: Literal["global", "project", "task", "session"]
    polarity: Literal["positive", "negative", "neutral"] = "neutral"

    confidence: float
    importance: float
    stability: float
    recurrence: int = 1
    explicitness: Literal["explicit", "inferred"] = "explicit"

    valid_from: datetime | None = None
    valid_to: datetime | None = None
    supersedes: list[str] = Field(default_factory=list)
    superseded_by: list[str] = Field(default_factory=list)

    source_ids: list[str]
    evidence_spans: list[SourceSpan] = Field(default_factory=list)

    trust_tier: Literal["high", "medium", "low", "untrusted"] = "medium"
    admission_status: Literal[
        "candidate",
        "accepted",
        "rejected",
        "quarantined",
        "superseded",
        "rolled_back"
    ] = "candidate"

    derived_from: list[str] = Field(default_factory=list)
    entails: list[str] = Field(default_factory=list)
    contradicted_by: list[str] = Field(default_factory=list)

    token_cost_verbose: int | None = None
    token_cost_compact: int | None = None
    token_cost_dsl: int | None = None
    token_cost_hybrid: int | None = None

    render_verbose: str | None = None
    render_compact: str | None = None
    render_dsl: str | None = None
    render_hybrid: str | None = None
```

### 6.4 RuleMemory

```python
class RuleMemory(BaseModel):
    id: str
    rule_type: Literal[
        "style",
        "workflow",
        "decision",
        "avoidance",
        "preference",
        "security",
        "project"
    ]
    condition: str
    action: str
    scope: Literal["global", "project", "task", "session"]
    priority: int
    confidence: float
    source_atom_ids: list[str]
    exceptions: list[str] = Field(default_factory=list)
```

### 6.5 MemoryLoadout

```python
class MemoryLoadout(BaseModel):
    global_core: list[str]
    project_core: list[str]
    task_pack: list[str]
    evidence_pack: list[str] = Field(default_factory=list)
    omitted: list[str]
    recalled: list[str] = Field(default_factory=list)

    total_tokens: int
    budget_tokens: int

    recall_required: bool = False
    source_verification_required: bool = False
    rationale: str
```

---

## 7. Systems to Compare

v1.0 evaluation must compare at least:

```text
B0 no_memory
B1 naive_rag
B2 hybrid_bm25_embedding_rag
B3 rolling_summary
B4 full_context_where_feasible
B5 uncompressed_core
B6 compressed_core
B7 compressed_core_plus_recall
B8 compressed_core_plus_recall_plus_source_verification
B9 full_compiler
B10 existing_memory_layer_only_if_available
B11 compiler_over_existing_memory_layer_if_available
```

Do not remove `naive_rag`. It is the practical baseline.

Do not rely only on `naive_rag`. Include rolling summary and, where feasible, full context.

---

## 8. Main Metrics

### 8.1 End-to-end metrics

```text
answer_accuracy
answer_f1
judge_correctness
preference_adherence
temporal_accuracy
stale_answer_rate
abstention_precision
abstention_recall
abstention_f1
```

### 8.2 Provenance metrics

```text
source_metric_status
source_recall@1_exact
source_recall@5_exact
source_recall@1_approx
source_recall@5_approx
source_mrr
quote_match_rate
timestamp_match_rate
source_verification_success_rate
```

### 8.3 Compression and efficiency metrics

```text
raw_tokens
system_prompt_tokens
core_memory_tokens
query_tokens
recall_query_tokens
recall_result_tokens
source_verification_tokens
answer_prompt_tokens
duplicated_memory_tokens
total_input_tokens
output_tokens
total_tokens
compression_ratio
score_per_1k_tokens
cost_per_correct_answer
latency_p50
latency_p95
```

### 8.4 Runtime metrics

```text
recall_trigger_rate
unnecessary_recall_rate
recall_miss_rate
recall_tokens_per_correct
recall_tokens_per_source_hit
loadout_token_efficiency
core_churn_rate
memory_update_latency
```

### 8.5 Compiler metrics

```text
gold_atom_precision
gold_atom_recall
gold_atom_f1
rule_precision
rule_recall
overgeneralization_rate
lost_fact_rate
redundancy_rate
contradiction_rate
delta_false_drop_rate
```

### 8.6 Security metrics

```text
poison_acceptance_rate
poison_activation_rate
quarantine_precision
quarantine_recall
rollback_success_rate
trusted_source_ratio
untrusted_core_admission_count
```

### 8.7 Aggregate scores

```text
MemoryUtility =
  0.30 * answer_accuracy
+ 0.20 * source_recall@5
+ 0.15 * temporal_accuracy
+ 0.10 * abstention_f1
+ 0.10 * preference_adherence
+ 0.10 * score_per_1k_tokens
- 0.05 * contradiction_rate
- 0.05 * poison_activation_rate
```

```text
EfficiencyAdjustedScore =
  answer_accuracy
  * max(source_recall@5, source_recall@5_approx, 0.5 if unavailable)
  * abstention_f1
  * (1 - stale_answer_rate)
  / log(1 + total_tokens)
```

---

## 9. Milestone Roadmap

# Milestone 0: Repo State Normalization

## Goal

Normalize the repo before further work.

## Tasks

```text
1. Ensure main contains the latest intended v0.4 state.
2. Preserve prior milestones with tags.
3. Keep raw reports gitignored.
4. Commit only small summaries under docs/benchmarks/.
5. Update CHANGELOG.md.
```

## Required artifacts

```text
docs/benchmarks/v0.2_eval_gauntlet_summary.md
docs/benchmarks/v0.3_token_efficiency_summary.md
docs/benchmarks/v0.4_public_benchmarks_summary.md
CHANGELOG.md
```

## Commands

```bash
uv run pytest
uv run ruff check .
uv run python scripts/run_eval_gauntlet.py --dataset synthetic_v2 --out reports/v0.4_eval_gauntlet
```

## Acceptance

```text
CI passes.
pytest passes.
ruff passes.
main or a clearly named release branch contains v0.4.
Benchmark summaries are committed.
```

---

# Milestone 1: v0.5 Real External Benchmark Validation

## Goal

Move from public benchmark scaffold to honest real external benchmark validation.

## Why

The current local deterministic harness is useful but can overstate performance.

v0.5 must separate:

```text
real external validation
adapter-only
deterministic scaffold
approximated source metrics
unavailable source metrics
```

## Tasks

### 1. Dataset provenance manifest

Create:

```text
docs/benchmarks/v0.5_dataset_manifest.md
reports/v0.5_real_external/dataset_manifest.json
```

For each benchmark:

```text
dataset name
source path or download instructions
split
sample size
sampling seed
license / citation note if available
answer scoring method
source metric status: exact / approximated / unavailable
known limitations
```

### 2. Strict source metric labeling

Implement:

```text
source_metric_status = exact | approximated | unavailable
```

Rules:

```text
If exact gold source spans do not exist:
  do not report source_recall@5_exact

If approximate matching is used:
  report source_recall@5_approx

If unavailable:
  metric value must be null or "unavailable"
```

### 3. LoCoMo real mini hardening

Expand if possible:

```text
minimum: 30 QA
preferred: 100 QA
split: dev / heldout
seed: deterministic
```

Run systems:

```text
no_memory
naive_rag
rolling_summary
compressed_core
compressed_core_plus_recall
full_compiler
```

### 4. LongMemEval-S real subset

Replace deterministic local shape where possible.

If real dataset access is not implemented:

```text
mark as adapter-only
do not count as external validation pass
```

### 5. MemoryAgentBench real mini

Same policy as LongMemEval.

### 6. RULER-style internal synthetic

Keep as synthetic stress benchmark.

Do not label it as public validation.

### 7. Failure analysis

Classify every failed or degraded example:

```text
E1 extraction_miss
E2 bad_abstraction
E3 lost_provenance
E4 temporal_failure
E5 over_pruning
E6 bad_salience
E7 bad_loadout
E8 recall_failure
E9 reading_failure
E10 abstention_failure
E11 token_overuse
E12 benchmark_mapping_failure
E13 source_span_unavailable
```

## Outputs

```text
reports/v0.5_real_external/
  dataset_manifest.json
  locomo_real_mini.csv
  locomo_real_mini.md
  longmemeval_real_subset.csv
  longmemeval_real_subset.md
  memoryagentbench_real_mini.csv
  memoryagentbench_real_mini.md
  ruler_synthetic.csv
  ruler_synthetic.md
  aggregate_public_validation.csv
  aggregate_public_validation.md
  errors.jsonl
  error_summary.md
  summary.md

docs/benchmarks/v0.5_real_external_validation_summary.md
```

## Commands

```bash
uv run pytest
uv run ruff check .
uv run python scripts/run_public_benchmarks.py --out reports/v0.5_real_external
```

## Acceptance

```text
CI passes.
pytest passes.
ruff passes.
LoCoMo real mini runs.
At least one benchmark is clearly marked real external validation.
Adapter-only benchmarks are clearly marked adapter-only.
No exact source metric is reported without exact source spans.
docs/benchmarks/v0.5_real_external_validation_summary.md is committed.
```

---

# Milestone 2: v0.6 Token Efficiency and Recall Optimization

## Goal

Make `full_compiler` token-competitive.

## Success target

```text
full_compiler.total_tokens <= naive_rag.total_tokens
OR
full_compiler.score_per_1k_tokens > naive_rag.score_per_1k_tokens
```

while preserving:

```text
accuracy >= naive_rag - allowed_margin
source_recall >= naive_rag - allowed_margin
stale_answer_rate <= naive_rag
abstention_f1 >= naive_rag - allowed_margin
poison_activation_rate = 0.0 on security suite
```

Recommended allowed margin:

```text
accuracy_margin = 0.03
source_margin = 0.05
abstention_margin = 0.05
```

## Tasks

### 1. Token attribution

Per question, report:

```text
system_prompt_tokens
core_memory_tokens
query_tokens
recall_query_tokens
recall_result_tokens
source_verification_tokens
answer_prompt_tokens
duplicated_memory_tokens
total_tokens
```

### 2. Recall overfire analysis

Classify recall calls:

```text
necessary_recall
unnecessary_recall
source_only_recall
stale_check_recall
unknown_check_recall
```

Metrics:

```text
recall_trigger_rate
unnecessary_recall_rate
recall_tokens_per_correct
recall_tokens_per_source_hit
```

### 3. Conservative recall policy

Config:

```yaml
recall_policy:
  mode: conservative
  confidence_threshold: 0.85
  source_verification_threshold: 0.75
  max_recall_items: 2
  max_source_span_chars: 240
  no_recall_for_global_style_if_answerable: true
  source_id_only_when_possible: true
  dedupe_core_and_recall: true
```

Rules:

```text
Do not recall if core fully answers and no source is required.
Do not recall for global style preferences unless evidence is requested.
Do not fetch raw spans unless source verification is required.
If source_id satisfies the metric, avoid quote expansion.
If recalled atom is already in core, include only source_id or minimal quote.
```

### 4. Source span compression

Modes:

```text
full_source
minimal_quote
source_id_only
source_summary
```

### 5. Representation optimization

Compare:

```text
verbose
compact
dsl
macro
hybrid
```

Hybrid policy:

```text
verbose for high-risk factual/temporal atoms
compact for preferences
DSL for stable style rules
source_id-only for low-risk already-loaded atoms
```

## Outputs

```text
reports/v0.6_token_efficiency/
  token_attribution.csv
  token_attribution.md
  recall_overfire.csv
  recall_overfire.md
  representation_efficiency.csv
  representation_efficiency.md
  summary.md

docs/benchmarks/v0.6_token_efficiency_summary.md
```

## Commands

```bash
uv run pytest
uv run ruff check .
uv run python scripts/run_token_efficiency.py --dataset synthetic_v2 --out reports/v0.6_token_efficiency
uv run python scripts/run_token_efficiency.py --dataset locomo_real_mini --out reports/v0.6_token_efficiency_locomo
```

## Acceptance

```text
Token attribution report exists.
Recall overfire report exists.
Representation efficiency report exists.
Token inversion success/failure is explicitly reported.
No source verification metrics are silently skipped.
```

---

# Milestone 3: v0.7 Complete Compiler Modules

## Goal

Implement all major compiler modules.

## Modules

```text
1. Multi-resolution memory
2. Rule induction
3. Entailment-minimal pruning
4. Delta-to-default pruning
5. Query-conditioned loadout v2
6. Retrieval/recall sweep
7. Full ablation matrix
```

---

## 3.1 Multi-resolution memory

### Levels

```text
R0 atom
R1 one-line summary
R2 short summary
R3 episode summary
R4 raw span pointer
```

### Requirements

```text
Core context may use R0/R1.
Recall can descend R1 → R2 → R3 → R4.
Source recovery must still work.
```

### Tests

```text
Given a DSL atom, recover R2 and raw source.
Given a source request, fetch minimal quote.
```

---

## 3.2 Rule induction

### RuleMemory fields

```text
condition
action
scope
priority
confidence
source_atom_ids
exceptions
```

### Safety constraints

```text
Require >=2 supporting atoms unless explicitly stated by user.
Single episode cannot become global rule.
Inferred rules have lower confidence.
Overgeneralization traps must be in tests.
```

### Metrics

```text
rule_precision
rule_recall
overgeneralization_rate
preference_adherence
```

---

## 3.3 Entailment-minimal pruning

### Implementation

```text
candidate generation by normalized subject/relation + embedding similarity
deterministic mock NLI for tests
optional LLM judge interface
prune only high-confidence entailments
route contradictions to temporal resolver
```

### Rules

```text
Do not delete contradictions.
Do not hard-delete pruned atoms.
Mark excluded_from_core.
Keep provenance.
```

### Metrics

```text
redundancy_rate
lost_fact_rate
contradiction_rate
token_saved_by_entailment
```

---

## 3.4 Delta-to-default pruning

### Classes

```text
USER_DELTA
PROJECT_DELTA
DEFAULT_SYSTEM
DEFAULT_MODEL
EVIDENCE_ONLY
TEMPORARY
UNSAFE_OR_UNTRUSTED
```

### Rules

```text
Do not hard-delete.
Exclude DEFAULT_* from core.
Keep EVIDENCE_ONLY as pointer.
Never prune user-specific preferences solely because they sound common.
Emit reason and confidence.
```

### Metrics

```text
token_saved_by_delta
delta_false_drop_rate
restored_from_delta_count
```

---

## 3.5 Query-conditioned loadout v2

### Loadout components

```text
global_core
project_core
task_pack
evidence_pack
recall_plan
```

### Query classes

```text
style_query
project_query
past_decision_query
source_request
current_fact_request
unknown_or_ambiguous
conflict_check
security_sensitive
```

### Metrics

```text
loadout_token_efficiency
missed_memory_rate
unnecessary_memory_rate
oracle_gap
```

---

## 3.6 Recall sweep

Modes:

```text
no_recall
embedding_recall
bm25_recall
hybrid_recall
graph_recall
graph_plus_vector_recall
```

If graph backend is unavailable, implement deterministic in-memory graph.

---

## 3.7 Full ablation matrix

Run:

```text
full
no_pointer
no_temporal
no_salience
no_dsl
no_recall
no_source_verification
no_loadout
no_rule
no_multires
no_entailment
no_delta
no_security
```

## Outputs

```text
reports/v0.7_full_modules/
  full_ablation.csv
  full_ablation.md
  module_token_savings.csv
  module_failure_modes.md
  summary.md

docs/benchmarks/v0.7_full_modules_summary.md
```

## Commands

```bash
uv run pytest
uv run ruff check .
uv run python scripts/run_full_ablation.py --dataset synthetic_v2 --out reports/v0.7_full_modules
uv run python scripts/run_full_ablation.py --dataset locomo_real_mini --out reports/v0.7_full_modules_locomo
```

## Acceptance

```text
Every major module is configurable.
Every major module is ablatable.
Every major module has tests.
Full compiler runs on synthetic_v2.
Full compiler runs on at least one real external mini subset.
Ablation report is committed as summary.
```

---

# Milestone 4: v0.8 External Memory Backend Adapters

## Goal

Position Core Context Compiler as a compiler layer over existing memory systems.

## Backend protocol

```python
class MemoryBackend(Protocol):
    def put_event(self, event: RawEvent) -> str: ...
    def put_atom(self, atom: MemoryAtom) -> str: ...
    def get_atom(self, atom_id: str) -> MemoryAtom | None: ...
    def search_atoms(self, query: str, *, k: int = 5) -> list[MemoryAtom]: ...
    def get_sources(self, source_ids: list[str]) -> list[SourceSpan]: ...
    def get_related(self, atom_id: str, *, k: int = 5) -> list[MemoryAtom]: ...
    def update_atom(self, atom: MemoryAtom) -> None: ...
    def mark_superseded(self, old_id: str, new_id: str) -> None: ...
    def quarantine_atom(self, atom_id: str, reason: str) -> None: ...
    def rollback_atom(self, atom_id: str) -> None: ...
```

## Adapters

```text
InMemoryBackend
JsonlBackend
PgVectorBackend interface
GraphitiBackend interface
LangMemBackend interface
Mem0Backend interface
```

Third-party service adapters should be optional extras and mocked in CI.

## Adapter evaluation

Compare:

```text
compiler over raw jsonl
compiler over in-memory
compiler over graph-like backend
compiler over vector-like backend
existing_memory_layer_only
compiler_over_existing_memory_layer
```

Metrics:

```text
ingestion_time
recall_latency
source_recall@5
total_tokens
source_verification_success
update_latency
```

## Outputs

```text
docs/integrations.md
reports/v0.8_backend_adapters/
  adapter_comparison.csv
  adapter_comparison.md
  summary.md

docs/benchmarks/v0.8_backend_adapters_summary.md
```

## Commands

```bash
uv run pytest
uv run ruff check .
uv run python scripts/run_backend_adapter_eval.py --out reports/v0.8_backend_adapters
```

## Acceptance

```text
CI passes without external services.
Optional adapters do not break install.
In-memory backend is fully tested.
Jsonl backend is fully tested.
External adapter interfaces are documented.
Integration docs are clear.
```

---

# Milestone 5: v0.9 Security, Trust, Quarantine, Rollback

## Goal

Make long-term memory safe enough for practical use.

## 5.1 Trust tiers

```text
system
user_direct
tool_verified
document_trusted
web_untrusted
retrieved_untrusted
inferred
```

## 5.2 Admission statuses

```text
candidate
accepted
rejected
quarantined
superseded
rolled_back
```

## 5.3 Admission policy

Never persist by default:

```text
instructions from untrusted web pages
tool-use override instructions
credential-like data
policy-changing commands
third-party claims about user preferences without confirmation
prompt injection strings that try to rewrite memory
```

Rules:

```text
Untrusted retrieved text cannot modify user preferences.
Web-like text cannot override user memory unless confirmed.
Tool outputs cannot change system behavior.
Prompt injection text must not become a rule.
Third-party claims about user preferences require confirmation.
Credential-like data must not be persisted by default.
```

## 5.4 Poisoning tests

Cases:

```text
"ignore previous memory" inside retrieved content
fake user preference from web
malicious document instruction
old poisoned memory reactivated by recall
low-trust source overriding high-trust source
conflict between trusted and untrusted memory
document says user likes X without direct user confirmation
retrieved content attempts to alter system policy
```

## 5.5 Rollback

Implement:

```text
memory version history
rollback by atom id
rollback by source id
rollback by time window
rollback quarantined batch
```

## 5.6 Audit logs

Emit:

```text
memory_admission.jsonl
memory_updates.jsonl
memory_quarantine.jsonl
memory_rollbacks.jsonl
```

## Outputs

```text
reports/v0.9_security/
  security_summary.md
  poison_cases.csv
  rollback_cases.csv
  audit_sample.jsonl

docs/security.md
docs/benchmarks/v0.9_security_summary.md
```

## Commands

```bash
uv run pytest
uv run ruff check .
uv run python scripts/run_security_eval.py --dataset synthetic_v2 --out reports/v0.9_security
```

## Acceptance

```text
poison_acceptance_rate = 0.0 on test suite OR failures explicitly reported.
poison_activation_rate = 0.0 on test suite OR failures explicitly reported.
rollback tests pass.
untrusted memory cannot enter core context directly.
audit logs are emitted.
```

---

# Milestone 6: v0.10 Production CLI and Developer UX

## Goal

Make the project usable by another engineer.

## 6.1 Unified CLI

Create command group:

```text
corectx
```

Commands:

```text
corectx ingest
corectx compile
corectx answer
corectx eval
corectx ablate
corectx benchmark
corectx report
corectx inspect
corectx rollback
```

Examples:

```bash
corectx ingest \
  --input datasets/synthetic_v2/events.jsonl \
  --store .corectx/store

corectx compile \
  --store .corectx/store \
  --budget 512 \
  --representation hybrid

corectx answer \
  --query "What does the user prefer?" \
  --store .corectx/store

corectx eval \
  --dataset synthetic_v2 \
  --system full_compiler

corectx benchmark \
  --suite public_subsets

corectx inspect \
  --atom-id m_123

corectx rollback \
  --source-id e_999
```

## 6.2 Config system

Add:

```text
configs/default.yaml
configs/conservative.yaml
configs/aggressive.yaml
configs/public_benchmarks.yaml
configs/security.yaml
```

## 6.3 Report formats

Generate:

```text
markdown
csv
json
optional html
```

## 6.4 Error analysis

Implement:

```text
E1 extraction_miss
E2 bad_abstraction
E3 lost_provenance
E4 temporal_failure
E5 over_pruning
E6 bad_salience
E7 bad_loadout
E8 recall_failure
E9 reading_failure
E10 abstention_failure
E11 poisoning_failure
E12 token_overuse
E13 benchmark_mapping_failure
E14 source_span_unavailable
E15 adapter_failure
```

## 6.5 Documentation

Update:

```text
README.md
docs/architecture.md
docs/schema.md
docs/benchmark_protocol.md
docs/memory_policy.md
docs/security.md
docs/integrations.md
docs/cli.md
CHANGELOG.md
```

## Commands

```bash
uv run pytest
uv run ruff check .
corectx --help
corectx eval --dataset synthetic_v2 --system full_compiler --out reports/cli_smoke
```

## Acceptance

```text
A new developer can run synthetic eval from README.
A new developer can inspect why a memory atom entered core.
A new developer can reproduce committed benchmark summaries.
CLI has smoke tests.
Docs are coherent and not stale.
```

---

# Milestone 7: v1.0 Release Gate

## Goal

Create an automated release gate that decides whether v1.0 can be tagged.

## Script

```text
scripts/run_v1_release_gate.py
```

It must run:

```text
1. pytest
2. ruff
3. synthetic_v2 gauntlet
4. token efficiency eval
5. public benchmark subsets
6. full module ablation
7. security eval
8. report generation
```

## Required output

```text
reports/v1_release_gate/
  release_gate_summary.md
  metrics.json
  pass_fail.json
  baseline_comparison.md
  public_benchmarks.md
  ablation.md
  token_efficiency.md
  security.md
  known_failures.md

docs/benchmarks/v1_release_gate_summary.md
```

## Pass criteria

### Mandatory

```text
CI passes
pytest passes
ruff passes
synthetic_v2 runs
public benchmark subsets run
full ablation runs
security eval runs
source metrics are reported with exact/approx/unavailable status
stale_answer_rate is reported
abstention_f1 is reported
total_tokens is reported
token efficiency vs naive_rag is reported
no hidden skipped metrics
```

### Synthetic v2 quantitative gate

```text
accuracy >= 0.95
source_recall@5_exact >= 0.95 where exact source exists
stale_answer_rate <= 0.03
abstention_f1 >= 0.90
poison_activation_rate = 0.0
```

### Public subset quantitative gate

```text
full_compiler >= naive_rag on at least 2 of 3 real/mini benchmark subsets by EfficiencyAdjustedScore

full_compiler must not be worse than naive_rag by more than 5 percentage points in accuracy on any subset unless explained
```

### Token gate

```text
full_compiler total_tokens <= naive_rag total_tokens on synthetic_v2
OR
full_compiler score_per_1k_tokens > naive_rag score_per_1k_tokens
```

### Provenance gate

```text
source_recall@5_exact >= 0.85 where exact source gold exists
OR
source metric is explicitly unavailable
```

### Security gate

```text
poison_acceptance_rate = 0.0 on security suite
poison_activation_rate = 0.0 on security suite
untrusted_core_admission_count = 0
rollback_success_rate >= 0.95
```

## If gate fails

```text
Do not tag v1.0.
Write failure reason to docs/benchmarks/v1_release_gate_summary.md.
Open follow-up issue with exact failure mode.
```

## If gate passes

```text
tag v1.0.0
create GitHub release
include benchmark summary
include known limitations
include commands to reproduce
```

## Commands

```bash
uv run pytest
uv run ruff check .
uv run python scripts/run_v1_release_gate.py --out reports/v1_release_gate
```

---

## 10. Full v1.0 Issue Text

Use this as the top-level GitHub Epic.

```text
Title:
v1.0 Complete Implementation: Core Context Compiler

Goal:
Bring core-context-compiler to v1.0 practical completeness.

Definition:
A reproducible, benchmarked, documented Core Context Compiler that transforms raw events and/or existing memory stores into compact, typed, provenance-linked, temporally valid, salience-gated core context; recalls external memory only when necessary; verifies sources when needed; prevents stale and poisoned memories; and reports honest comparisons against naive RAG, rolling summaries, and public benchmark subsets.

Non-goals:
- Do not build a generic RAG app.
- Do not optimize only for synthetic accuracy.
- Do not fabricate missing metrics.
- Do not claim public benchmark victory from deterministic scaffold results.
- Do not silently skip token, source, stale, abstention, or security metrics.

Milestones:
1. Normalize repo state.
2. Real external benchmark validation.
3. Token efficiency and recall optimization.
4. Complete all compiler modules.
5. External memory backend adapters.
6. Security, trust, quarantine, rollback.
7. Production CLI and developer UX.
8. v1.0 release gate.

Required final commands:
uv run pytest
uv run ruff check .
uv run python scripts/run_eval_gauntlet.py --dataset synthetic_v2 --out reports/latest_gauntlet
uv run python scripts/run_token_efficiency.py --dataset synthetic_v2 --out reports/latest_token_efficiency
uv run python scripts/run_public_benchmarks.py --out reports/latest_public_benchmarks
uv run python scripts/run_full_ablation.py --dataset synthetic_v2 --out reports/latest_ablation
uv run python scripts/run_security_eval.py --dataset synthetic_v2 --out reports/latest_security
uv run python scripts/run_v1_release_gate.py --out reports/v1_release_gate

Final acceptance:
- CI passes.
- All required scripts run.
- At least one real external mini subset is validated.
- Adapter-only datasets are labeled adapter-only.
- Full ablation matrix exists.
- Security suite exists.
- Token metrics exist.
- Source metrics are exact/approx/unavailable labeled.
- docs/benchmarks/v1_release_gate_summary.md is committed.
- v1.0 is tagged only if release gate passes.
```

---

## 11. Suggested GitHub Issues

```text
#23 v0.5 Real External Benchmark Validation
#24 v0.6 Token Efficiency and Recall Optimization
#25 v0.7 Complete Compiler Modules
#26 v0.8 External Memory Backend Adapters
#27 v0.9 Security, Trust, Quarantine, Rollback
#28 v0.10 Production CLI and Developer UX
#29 v1.0 Release Gate
```

Create one Epic and attach these as child issues if GitHub Projects is used.

---

## 12. Release Tag Plan

```text
v0.1.0-mvp
  MVP implementation

v0.2.0-eval-gauntlet
  synthetic_v2 evaluation gauntlet

v0.3.0-token-efficiency
  token attribution, recall overfire, representation sweep

v0.4.0-public-benchmark-scaffold
  public/sub-public adapters and LoCoMo real mini ingestion

v0.5.0-real-external-validation
  honest real external mini validation with source metric labeling

v0.6.0-token-optimized
  conservative recall, source compression, hybrid rendering

v0.7.0-full-compiler-modules
  multires, rules, entailment, delta, loadout v2, full ablation

v0.8.0-backend-adapters
  memory backend protocol and adapter interfaces

v0.9.0-security
  trust tiers, quarantine, rollback, poison tests

v0.10.0-cli-docs
  CLI and developer UX

v1.0.0
  release gate passed
```

---

## 13. v1.0 README Positioning

README should say:

```text
Core Context Compiler compiles long-term agent memory into compact working context.

It is designed to sit above logs, vector DBs, LangMem, Graphiti, Mem0-like systems, or custom stores.

It does not replace retrieval.
It decides what should be in the model's working context now.

RAG retrieves.
Core Context Compiler compiles.
```

Avoid saying:

```text
This is the first memory system.
This beats all RAG.
This solves LLM memory.
```

Say:

```text
This provides a reproducible framework to test whether compiled core context improves practical agent memory under token, provenance, temporal, and security constraints.
```

---

## 14. Risk Register

| Risk | Severity | Mitigation |
|---|---:|---|
| Synthetic benchmark too easy | High | Real external mini validation, heldout splits |
| Deterministic harness overstates performance | High | Mark scaffold vs real validation |
| Source spans unavailable | High | exact/approx/unavailable labels |
| Token efficiency loses to naive RAG | High | token attribution, conservative recall, source compression |
| Rule induction overgeneralizes | High | require multiple sources, scope, exceptions |
| Delta-to-default drops user-specific preferences | High | no hard delete, reason/confidence, restore path |
| Memory poisoning persists across sessions | High | trust tiers, quarantine, rollback |
| Full compiler equals simpler system | Medium | ablation and module token-savings reports |
| External adapters break CI | Medium | optional extras, mocks |
| Docs drift | Medium | release gate checks docs and commands |
| Public datasets unavailable | Medium | manifest, adapter-only label, no fabricated metrics |
| v1.0 gate becomes too lax | High | fixed pass/fail script |

---

## 15. Final v1.0 Checklist

```text
[ ] CI passes.
[ ] uv run pytest passes.
[ ] uv run ruff check . passes.
[ ] synthetic_v2 gauntlet runs.
[ ] token efficiency eval runs.
[ ] public benchmark script runs.
[ ] at least one real external mini subset is validated.
[ ] adapter-only datasets are labeled adapter-only.
[ ] source metrics are exact/approx/unavailable labeled.
[ ] full ablation matrix exists.
[ ] token attribution exists.
[ ] recall overfire analysis exists.
[ ] representation sweep exists.
[ ] multi-resolution memory implemented.
[ ] rule induction implemented.
[ ] entailment pruning implemented.
[ ] delta-to-default implemented.
[ ] query-conditioned loadout v2 implemented.
[ ] backend adapter protocol implemented.
[ ] security suite implemented.
[ ] trust tiers implemented.
[ ] quarantine implemented.
[ ] rollback implemented.
[ ] audit logs implemented.
[ ] CLI implemented.
[ ] README updated.
[ ] docs/architecture.md updated.
[ ] docs/schema.md updated.
[ ] docs/benchmark_protocol.md updated.
[ ] docs/memory_policy.md updated.
[ ] docs/security.md updated.
[ ] docs/integrations.md updated.
[ ] docs/cli.md updated.
[ ] docs/benchmarks/v1_release_gate_summary.md committed.
[ ] CHANGELOG.md updated.
[ ] v1.0.0 tag created only after release gate passes.
```

---

## 16. Final Command Pack

```bash
uv run pytest
uv run ruff check .

uv run python scripts/run_eval_gauntlet.py \
  --dataset synthetic_v2 \
  --out reports/latest_gauntlet

uv run python scripts/run_token_efficiency.py \
  --dataset synthetic_v2 \
  --out reports/latest_token_efficiency

uv run python scripts/run_public_benchmarks.py \
  --out reports/latest_public_benchmarks

uv run python scripts/run_full_ablation.py \
  --dataset synthetic_v2 \
  --out reports/latest_ablation

uv run python scripts/run_security_eval.py \
  --dataset synthetic_v2 \
  --out reports/latest_security

uv run python scripts/run_v1_release_gate.py \
  --out reports/v1_release_gate
```

---

## 17. Final Operating Rule

If v1.0 does not beat naive RAG on tokens, but wins materially on provenance, stale-answer prevention, abstention, and security, that is still potentially useful.

In that case, do **not** claim:

```text
better than RAG
```

Claim:

```text
more controllable and auditable than naive RAG under memory correctness constraints
```

If it beats naive RAG on both quality and token efficiency, claim:

```text
compiled core context is a practical memory layer for LLM agents
```

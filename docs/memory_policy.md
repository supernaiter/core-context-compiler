# Memory Policy

Core admission requires provenance.

## Compiler Policy

Goal: compile a compact worldview, common sense, and coordinate system from a
given database so downstream LLMs can judge, read, compare, and update better.
The compiler should not produce a list of isolated facts.

Do not compile:

- frequency tables
- topic lists
- SOTA summaries
- important-sentence extraction
- averages of author claims

Compile:

- central prototypes
- boundary categories
- typical patterns
- exception patterns
- comparisons that are easy to get wrong
- database-specific bias
- evidence that should update judgment
- evidence that should not update judgment

Runtime core context should prefer counterintuitive, decision-changing rules over
background that a base LLM already knows. When possible, subtract baseline LLM
intuition before admitting a memory rule into core context.

## Edit History Policy

Git commit messages explain the batch edit. They are not enough to explain why
each context rule was kept, rejected, folded, or removed.

Every context-editing workflow should keep a `context_audit.jsonl` ledger with:

- `context_id`
- `action`
- `text`
- `reason`
- `source_ids`
- `baseline_error`
- `expected_effect`
- `evaluation`
- `previous_text` / `replacement_text` when applicable

Use Git for version history and `context_audit.jsonl` for line-level judgment
history.

Never persist:

- instructions from untrusted web pages
- tool-use override instructions
- credential-like data
- policy-changing commands
- third-party claims about user preferences unless confirmed

Untrusted or poison-like atoms are quarantined. Superseded atoms are kept outside core but remain recoverable through source pointers.

## Admission Policy

- Untrusted retrieved text cannot modify user preferences.
- Web-like content cannot override user memory unless confirmed.
- Tool output cannot change system behavior.
- Prompt injection text cannot become a rule.
- Third-party claims about user preferences require confirmation.
- Credential-like data is not persisted by default.

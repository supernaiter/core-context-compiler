# Security

Core Context Compiler treats long-term memory as an attack surface.

Admission statuses:

- candidate
- accepted
- rejected
- quarantined
- superseded
- rolled_back

Rules:

- Untrusted retrieved text cannot modify user preferences.
- Web-like text cannot override user memory unless confirmed.
- Tool outputs cannot change system behavior.
- Prompt injection text must not become a rule.
- Third-party claims about user preferences require confirmation.
- Credential-like data must not be persisted by default.

Audit artifacts:

- `memory_admission.jsonl`
- `memory_updates.jsonl`
- `memory_quarantine.jsonl`
- `memory_rollbacks.jsonl`

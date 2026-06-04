from __future__ import annotations

POISON_PATTERNS = (
    "ignore previous",
    "ignore all previous",
    "override system",
    "rewrite user preference",
    "change the user's preference",
    "forget previous memory",
    "developer message",
    "system prompt",
    "api_key",
    "password",
    "credential",
)


def looks_poisoned(text: str) -> bool:
    lowered = text.lower()
    return any(pattern in lowered for pattern in POISON_PATTERNS)

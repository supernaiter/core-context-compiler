from __future__ import annotations

TRUST_TIERS = (
    "system",
    "user_direct",
    "tool_verified",
    "document_trusted",
    "web_untrusted",
    "retrieved_untrusted",
    "inferred",
)

LOW_TRUST_TIERS = {"web_untrusted", "retrieved_untrusted", "inferred"}

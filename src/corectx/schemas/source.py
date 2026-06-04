from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class SourceSpan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str
    event_id: str
    span_start: int | None = None
    span_end: int | None = None
    quote: str | None = None
    timestamp: datetime | None = None
    source_metric_status: Literal["exact", "approximated", "unavailable"] = "exact"
    trust_tier: Literal[
        "user",
        "tool",
        "web",
        "untrusted",
        "system",
        "user_direct",
        "tool_verified",
        "document_trusted",
        "web_untrusted",
        "retrieved_untrusted",
        "inferred",
    ] = "user_direct"
    confidence: float = 1.0

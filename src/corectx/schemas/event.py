from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class RawEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str
    user_id: str | None = None
    session_id: str | None = None
    timestamp: datetime | None = None
    source_type: Literal["conversation", "document", "email", "calendar", "web", "manual"]
    speaker: str | None = None
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)

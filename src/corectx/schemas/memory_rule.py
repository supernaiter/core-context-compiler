from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MemoryRule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    scope: Literal["global", "project", "task", "session"]
    text: str
    supporting_atom_ids: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    exceptions: list[str] = Field(default_factory=list)

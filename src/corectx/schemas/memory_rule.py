from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MemoryRule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    rule_type: Literal[
        "style",
        "workflow",
        "decision",
        "avoidance",
        "preference",
        "security",
        "project",
    ] = "preference"
    condition: str = ""
    action: str = ""
    scope: Literal["global", "project", "task", "session"]
    priority: int = 0
    text: str
    source_atom_ids: list[str] = Field(default_factory=list)
    supporting_atom_ids: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    exceptions: list[str] = Field(default_factory=list)

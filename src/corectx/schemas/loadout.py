from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MemoryLoadout(BaseModel):
    model_config = ConfigDict(extra="forbid")

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

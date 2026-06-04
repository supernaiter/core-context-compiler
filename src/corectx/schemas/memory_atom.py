from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from corectx.schemas.source import SourceSpan


class MemoryAtom(BaseModel):
    model_config = ConfigDict(extra="forbid")

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
        "episode_summary",
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
        "rolled_back",
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
    salience: float | None = None

    @field_validator("confidence", "importance", "stability")
    @classmethod
    def _bounded_float(cls, value: float) -> float:
        if not 0.0 <= value <= 1.0:
            raise ValueError("value must be between 0 and 1")
        return value

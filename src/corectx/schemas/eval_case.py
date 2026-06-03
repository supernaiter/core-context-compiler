from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EvalQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    qid: str
    question: str
    required_sources: list[str] = Field(default_factory=list)
    expected_answer: str | None = None
    expected_behavior: Literal["answer", "abstain"] = "answer"
    expected_atom_ids: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)

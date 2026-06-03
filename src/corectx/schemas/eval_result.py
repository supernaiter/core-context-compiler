from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class EvalResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    baseline: str
    qid: str
    answer: str
    abstained: bool
    correct: bool
    source_recall_at5: float
    stale_answer: bool
    input_tokens: int
    cost_per_correct_answer: float | None = None
    selected_memory: list[str] = Field(default_factory=list)
    omitted_memory: list[str] = Field(default_factory=list)
    recovered_sources: list[str] = Field(default_factory=list)
    error: str | None = None

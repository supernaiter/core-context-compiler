from __future__ import annotations

import datetime as dt
import json
from collections import Counter
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

ContextAuditAction = Literal["add", "update", "remove", "keep", "reject", "fold"]


class ContextAuditEntry(BaseModel):
    model_config = ConfigDict(validate_default=True)

    time: dt.datetime = Field(default_factory=lambda: dt.datetime.now(dt.timezone.utc))
    context_id: str
    action: ContextAuditAction
    text: str
    reason: str
    source_ids: list[str] = Field(default_factory=list)
    baseline_error: str
    expected_effect: str
    evaluation: str
    previous_text: str | None = None
    replacement_text: str | None = None
    author: str | None = None
    commit_hash: str | None = None

    @field_validator(
        "context_id",
        "text",
        "reason",
        "baseline_error",
        "expected_effect",
        "evaluation",
    )
    @classmethod
    def require_nonempty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must be nonempty")
        return value.strip()

    @field_validator("source_ids")
    @classmethod
    def clean_source_ids(cls, values: list[str]) -> list[str]:
        cleaned = [value.strip() for value in values if value.strip()]
        if not cleaned:
            raise ValueError("must include at least one source id")
        return cleaned


def append_context_audit(path: str | Path, entry: ContextAuditEntry) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("a", encoding="utf-8") as handle:
        handle.write(entry.model_dump_json() + "\n")


def load_context_audit(path: str | Path) -> list[ContextAuditEntry]:
    source = Path(path)
    if not source.exists():
        return []
    entries: list[ContextAuditEntry] = []
    for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
            entries.append(ContextAuditEntry.model_validate(payload))
        except Exception as exc:
            raise ValueError(f"invalid context audit entry at {source}:{line_number}: {exc}") from exc
    return entries


def validate_context_audit(path: str | Path) -> bool:
    load_context_audit(path)
    return True


def summarize_context_audit(path: str | Path) -> dict[str, object]:
    entries = load_context_audit(path)
    actions = Counter(entry.action for entry in entries)
    source_linked = sum(1 for entry in entries if entry.source_ids)
    baseline_linked = sum(1 for entry in entries if entry.baseline_error)
    return {
        "entries": len(entries),
        "actions": dict(sorted(actions.items())),
        "source_linked_entries": source_linked,
        "baseline_error_entries": baseline_linked,
    }

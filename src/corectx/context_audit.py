from __future__ import annotations

import datetime as dt
import json
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Literal

ContextAuditAction = Literal["add", "update", "remove", "keep", "reject", "fold"]
_ACTIONS = {"add", "update", "remove", "keep", "reject", "fold"}
_REQUIRED_TEXT_FIELDS = (
    "context_id",
    "text",
    "reason",
    "baseline_error",
    "expected_effect",
    "evaluation",
)


@dataclass(frozen=True)
class ContextAuditEntry:
    context_id: str
    action: ContextAuditAction
    text: str
    reason: str
    baseline_error: str = ""
    expected_effect: str = ""
    evaluation: str = ""
    source_ids: list[str] = field(default_factory=list)
    time: dt.datetime = field(default_factory=lambda: dt.datetime.now(dt.UTC))
    previous_text: str | None = None
    replacement_text: str | None = None
    author: str | None = None
    commit_hash: str | None = None

    def __post_init__(self) -> None:
        if self.action not in _ACTIONS:
            raise ValueError("invalid context audit action")
        for field_name in _REQUIRED_TEXT_FIELDS:
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be nonempty")
            object.__setattr__(self, field_name, value.strip())
        cleaned_sources = [
            source_id.strip()
            for source_id in self.source_ids
            if isinstance(source_id, str) and source_id.strip()
        ]
        if not cleaned_sources:
            raise ValueError("source_ids must include at least one source id")
        object.__setattr__(self, "source_ids", cleaned_sources)
        if isinstance(self.time, str):
            object.__setattr__(self, "time", _parse_time(self.time))
        elif self.time.tzinfo is None:
            object.__setattr__(self, "time", self.time.replace(tzinfo=dt.UTC))

    @classmethod
    def model_validate(cls, payload: dict[str, object]) -> ContextAuditEntry:
        try:
            return cls(**payload)  # type: ignore[arg-type]
        except TypeError as exc:
            raise ValueError(str(exc)) from exc

    def model_dump(self) -> dict[str, object]:
        payload = asdict(self)
        payload["time"] = self.time.isoformat()
        return payload

    def model_dump_json(self) -> str:
        return json.dumps(self.model_dump(), ensure_ascii=False)


def _parse_time(value: str) -> dt.datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = dt.datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=dt.UTC)
    return parsed


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
            raise ValueError(
                f"invalid context audit entry at {source}:{line_number}: {exc}"
            ) from exc
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

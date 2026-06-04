from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel
from pydantic_core import ValidationError

from corectx.schemas import EvalQuestion, MemoryAtom, RawEvent, SourceSpan

T = TypeVar("T", bound=BaseModel)


def load_jsonl(path: str | Path, model: type[T]) -> list[T]:
    rows: list[T] = []
    with Path(path).open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(model.model_validate_json(line))
    return rows


def write_jsonl(path: str | Path, rows: list[BaseModel] | list[dict]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        for row in rows:
            if isinstance(row, BaseModel):
                data = row.model_dump(mode="json")
            else:
                data = row
            handle.write(json.dumps(data, ensure_ascii=False, sort_keys=True) + "\n")


def load_raw_events(path: str | Path) -> list[RawEvent]:
    return load_jsonl(path, RawEvent)


def load_eval_questions(path: str | Path) -> list[EvalQuestion]:
    return load_jsonl(path, EvalQuestion)


def load_gold_atoms(path: str | Path) -> list[MemoryAtom]:
    return load_jsonl(path, MemoryAtom)


def load_gold_sources(path: str | Path) -> list[SourceSpan]:
    target = Path(path)
    if not target.exists():
        return []
    rows: list[SourceSpan] = []
    with target.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(SourceSpan.model_validate_json(line))
            except ValidationError:
                continue
    return rows

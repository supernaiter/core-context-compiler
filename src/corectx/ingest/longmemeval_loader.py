from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from corectx.ingest.benchmark_loader import BenchmarkDataset
from corectx.schemas import EvalQuestion, RawEvent


def _conversation_events(item: dict[str, Any], index: int) -> list[RawEvent]:
    rows = item.get("haystack_sessions") or item.get("sessions") or item.get("conversation") or []
    events: list[RawEvent] = []
    counter = 0
    for session_index, session in enumerate(rows):
        messages = session.get("messages", session) if isinstance(session, dict) else session
        if not isinstance(messages, list):
            continue
        for message in messages:
            if not isinstance(message, dict):
                continue
            text = str(message.get("content") or message.get("text") or "")
            if not text:
                continue
            counter += 1
            events.append(
                RawEvent(
                    event_id=f"lme_{index}_{counter}",
                    session_id=str(session.get("session_id", session_index))
                    if isinstance(session, dict)
                    else str(session_index),
                    timestamp=message.get("timestamp"),
                    source_type="conversation",
                    speaker=message.get("role") or message.get("speaker"),
                    text=text,
                    metadata={"longmemeval_id": item.get("id") or item.get("question_id")},
                )
            )
    return events


def load_longmemeval_subset(path: str | Path, *, limit: int | None = None) -> BenchmarkDataset:
    source = Path(path)
    events: list[RawEvent] = []
    questions: list[EvalQuestion] = []
    with source.open(encoding="utf-8") as handle:
        for index, line in enumerate(handle):
            if limit is not None and index >= limit:
                break
            if not line.strip():
                continue
            item = json.loads(line)
            item_events = _conversation_events(item, index)
            events.extend(item_events)
            required_sources = [event.event_id for event in item_events[:5]]
            questions.append(
                EvalQuestion(
                    qid=str(item.get("id") or item.get("question_id") or f"lme_{index}"),
                    question=str(item.get("question") or item.get("query") or ""),
                    required_sources=required_sources,
                    expected_answer=str(item.get("answer") or item.get("target") or "")
                    or None,
                    tags=["longmemeval"],
                )
            )
    return BenchmarkDataset(root=source.parent, events=events, gold_atoms=[], questions=questions)

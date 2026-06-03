from __future__ import annotations

from pathlib import Path

from corectx.ingest.jsonl_loader import load_raw_events
from corectx.schemas import RawEvent


def load_conversation_events(path: str | Path) -> list[RawEvent]:
    return load_raw_events(path)

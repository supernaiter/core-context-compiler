from __future__ import annotations

from corectx.schemas import RawEvent


def normalize_events(events: list[RawEvent]) -> list[RawEvent]:
    return [
        event.model_copy(update={"text": " ".join(event.text.split())})
        for event in events
        if event.text.strip()
    ]

from __future__ import annotations

from corectx.schemas import RawEvent


class LexicalRecallStore:
    def __init__(self, events: list[RawEvent]) -> None:
        self.events = events

    def search(self, query: str, *, k: int = 5) -> list[RawEvent]:
        query_terms = set(query.lower().split())
        scored = []
        for event in self.events:
            terms = set(event.text.lower().split())
            score = len(query_terms & terms)
            scored.append((score, event.timestamp, event))
        scored.sort(key=lambda item: (item[0], item[1] is not None, item[1]), reverse=True)
        return [event for score, _, event in scored[:k] if score > 0]

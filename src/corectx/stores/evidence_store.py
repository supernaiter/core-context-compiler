from __future__ import annotations

from collections import defaultdict

from corectx.schemas import SourceSpan


class InMemoryEvidenceStore:
    def __init__(self) -> None:
        self._spans: dict[str, list[SourceSpan]] = defaultdict(list)

    def add(self, span: SourceSpan) -> None:
        self._spans[span.event_id].append(span)

    def add_many(self, spans: list[SourceSpan]) -> None:
        for span in spans:
            self.add(span)

    def recover(self, event_id: str) -> list[SourceSpan]:
        return list(self._spans.get(event_id, []))

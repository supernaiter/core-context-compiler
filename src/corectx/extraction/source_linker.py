from __future__ import annotations

from collections.abc import Iterable

from corectx.schemas import MemoryAtom, RawEvent, SourceSpan

TRUST_BY_SOURCE_TYPE = {
    "conversation": "user",
    "manual": "user",
    "document": "tool",
    "email": "tool",
    "calendar": "tool",
    "web": "untrusted",
}


def atom_trust_from_spans(spans: list[SourceSpan]) -> str:
    if not spans:
        return "untrusted"
    if any(span.trust_tier == "untrusted" for span in spans):
        return "untrusted"
    if any(span.trust_tier == "web" for span in spans):
        return "low"
    if all(span.trust_tier == "user" for span in spans):
        return "high"
    return "medium"


def is_poison_like(atom: MemoryAtom, events_by_id: dict[str, RawEvent]) -> bool:
    poison_terms = [
        "ignore previous",
        "ignore user",
        "override",
        "credential",
        "api key",
        "system prompt",
    ]
    text = " ".join(
        events_by_id[event_id].text.lower()
        for event_id in atom.source_ids
        if event_id in events_by_id
    )
    return any(term in text for term in poison_terms)


def attach_source_spans(
    atoms: Iterable[MemoryAtom],
    events: Iterable[RawEvent],
    *,
    confidence_threshold: float = 0.2,
) -> list[MemoryAtom]:
    events_by_id = {event.event_id: event for event in events}
    linked: list[MemoryAtom] = []
    for atom in atoms:
        spans: list[SourceSpan] = []
        for event_id in atom.source_ids:
            event = events_by_id.get(event_id)
            if event is None:
                continue
            spans.append(
                SourceSpan(
                    source_id=f"{event.event_id}:0:{len(event.text)}",
                    event_id=event.event_id,
                    span_start=0,
                    span_end=len(event.text),
                    quote=event.text,
                    timestamp=event.timestamp,
                    trust_tier=TRUST_BY_SOURCE_TYPE.get(event.source_type, "untrusted"),
                    confidence=1.0,
                )
            )

        trust_tier = atom_trust_from_spans(spans)
        if not atom.source_ids or not spans or atom.confidence < confidence_threshold:
            status = "rejected"
        elif trust_tier == "untrusted" or is_poison_like(atom, events_by_id):
            status = "quarantined"
        else:
            status = "accepted"

        linked.append(
            atom.model_copy(
                update={
                    "evidence_spans": spans,
                    "trust_tier": trust_tier,
                    "admission_status": status,
                }
            )
        )
    return linked

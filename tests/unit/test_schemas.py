from __future__ import annotations

from corectx.schemas import EvalQuestion, MemoryAtom, MemoryLoadout, RawEvent, SourceSpan


def test_schema_json_round_trip() -> None:
    event = RawEvent.model_validate(
        {
            "event_id": "e1",
            "timestamp": "2026-01-01T00:00:00Z",
            "source_type": "conversation",
            "speaker": "user",
            "text": "日本語で答えて。",
        }
    )
    span = SourceSpan(source_id="e1:0:8", event_id="e1", quote=event.text)
    atom = MemoryAtom(
        id="m1",
        kind="preference",
        subject="user",
        relation="answer_language",
        value="Japanese",
        scope="global",
        confidence=0.9,
        importance=0.8,
        stability=0.9,
        source_ids=["e1"],
        evidence_spans=[span],
    )
    restored = MemoryAtom.model_validate_json(atom.model_dump_json())
    assert restored.source_ids == ["e1"]
    assert restored.evidence_spans[0].event_id == "e1"

    loadout = MemoryLoadout(
        global_core=["m1"],
        project_core=[],
        task_pack=[],
        omitted=[],
        total_tokens=10,
        budget_tokens=512,
        rationale="test",
    )
    assert MemoryLoadout.model_validate_json(loadout.model_dump_json()).global_core == ["m1"]
    question = EvalQuestion(qid="q1", question="?", expected_behavior="abstain")
    assert question.expected_behavior == "abstain"

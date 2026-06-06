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


def test_memory_atom_represents_policy_v2_view_atom_fields() -> None:
    atom_types = [
        "central_prototype",
        "axis",
        "typical_pattern",
        "exception",
        "boundary_case",
        "bias",
        "update_rule",
        "non_update_rule",
        "deprecated_view",
        "warning",
    ]

    for atom_type in atom_types:
        atom = MemoryAtom(
            id=f"policy-{atom_type}",
            kind="belief",
            atom_type=atom_type,
            subject="core_context",
            relation="judgment_view",
            value=f"{atom_type} view",
            scope="project",
            confidence=0.8,
            importance=0.9,
            stability=0.7,
            source_ids=["policy-v2"],
            core_context_candidate=True,
            centrality_effect="Changes what the model treats as central.",
            decision_impact="Changes downstream judgment.",
            baseline_delta="Adds guidance beyond raw retrieval.",
            conflict_check="No active conflicting view.",
            update_semantics="Replace when stronger counterevidence appears.",
            staleness="stable",
            evidence_spans=[
                SourceSpan(
                    source_id="policy-v2",
                    event_id="policy-v2-event",
                    quote="Core admission requires decision impact.",
                )
            ],
            counterevidence=["none-found"],
        )

        restored = MemoryAtom.model_validate_json(atom.model_dump_json())
        assert restored.atom_type == atom_type
        assert restored.core_context_candidate is True
        assert restored.decision_impact
        assert restored.baseline_delta
        assert restored.conflict_check
        assert restored.update_semantics
        assert restored.centrality_effect
        assert restored.staleness == "stable"
        assert restored.evidence_spans[0].source_id == "policy-v2"
        assert restored.counterevidence == ["none-found"]

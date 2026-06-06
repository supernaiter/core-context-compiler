from __future__ import annotations

from corectx.rendering.dsl_renderer import DslRenderer
from corectx.rendering.prompt_block import build_prompt_block
from corectx.schemas import MemoryAtom, MemoryLoadout, SourceSpan


def _span(atom_id: str) -> SourceSpan:
    return SourceSpan(source_id=f"{atom_id}-source", event_id=f"{atom_id}-event", quote=atom_id)


def _atom(
    atom_id: str,
    *,
    status: str = "accepted",
    core_context_candidate: bool = False,
    atom_type: str | None = None,
    superseded: bool = False,
    policy_fields: bool = True,
    counterevidence: list[str] | None = None,
    value: str | None = None,
) -> MemoryAtom:
    policy_values = (
        {
            "centrality_effect": "Changes what the runtime core treats as central.",
            "decision_impact": "Changes downstream classification.",
            "baseline_delta": "Adds a non-obvious exception beyond raw retrieval.",
            "conflict_check": "No active conflicting view.",
            "update_semantics": "Replace when stronger counterevidence appears.",
        }
        if policy_fields
        else {}
    )
    return MemoryAtom(
        id=atom_id,
        kind="belief",
        atom_type=atom_type,
        subject="core_context",
        relation="judgment_view",
        value=value or atom_id,
        scope="project",
        confidence=0.8,
        importance=0.8,
        stability=0.8,
        source_ids=[f"{atom_id}-source"],
        evidence_spans=[_span(atom_id)],
        admission_status=status,  # type: ignore[arg-type]
        core_context_candidate=core_context_candidate,
        superseded_by=["newer"] if superseded else [],
        counterevidence=counterevidence or [],
        **policy_values,
    )


def test_render_core_block_excludes_non_runtime_eligible_atoms() -> None:
    atoms = [
        _atom("candidate", status="candidate"),
        _atom("rejected", status="rejected"),
        _atom("quarantined", status="quarantined"),
        _atom("superseded", superseded=True),
        _atom(
            "missing_policy",
            core_context_candidate=True,
            atom_type="typical_pattern",
            policy_fields=False,
        ),
        _atom(
            "fact_cache_shape",
            core_context_candidate=True,
            atom_type="typical_pattern",
            value="Build a topic list from source trivia.",
        ),
        _atom("bias_without_exception", core_context_candidate=True, atom_type="bias"),
        _atom(
            "bias_with_exception",
            core_context_candidate=True,
            atom_type="bias",
            counterevidence=["Exception: transfer evidence can override the bias."],
        ),
        _atom("accepted_view", core_context_candidate=True, atom_type="typical_pattern"),
        _atom("accepted_fact"),
    ]

    rendered = DslRenderer().render_core_block(atoms, include_macros=False)

    assert "accepted_view" in rendered
    assert "bias_with_exception" in rendered
    assert "accepted_fact" in rendered
    assert "candidate" not in rendered
    assert "rejected" not in rendered
    assert "quarantined" not in rendered
    assert "superseded" not in rendered
    assert "missing_policy" not in rendered
    assert "topiclist" not in rendered
    assert "bias_without_exception" not in rendered


def test_prompt_block_applies_runtime_core_gate() -> None:
    accepted = _atom("accepted_view", core_context_candidate=True, atom_type="axis")
    rejected = _atom("rejected_view", status="rejected", atom_type="axis")
    loadout = MemoryLoadout(
        global_core=[accepted.id, rejected.id],
        project_core=[],
        task_pack=[],
        omitted=[],
        total_tokens=0,
        budget_tokens=512,
        rationale="test",
    )

    rendered = build_prompt_block(loadout, {accepted.id: accepted, rejected.id: rejected})

    assert "accepted_view" in rendered
    assert "rejected_view" not in rendered

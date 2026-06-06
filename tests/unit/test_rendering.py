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
    conflict_check: str | None = None,
    update_semantics: str | None = None,
    value: str | None = None,
    staleness: str = "stable",
) -> MemoryAtom:
    policy_values = (
        {
            "centrality_effect": "Changes what the runtime core treats as central.",
            "decision_impact": "Changes downstream classification.",
            "baseline_delta": "Adds a non-obvious exception beyond raw retrieval.",
            "conflict_check": conflict_check or "No active conflicting view.",
            "update_semantics": update_semantics
            or "Replace when stronger counterevidence appears.",
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
        staleness=staleness,  # type: ignore[arg-type]
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
        _atom(
            "stale_ordinary",
            core_context_candidate=True,
            atom_type="typical_pattern",
            staleness="stale-risk",
        ),
        _atom(
            "stale_warning",
            core_context_candidate=True,
            atom_type="warning",
            staleness="stale-risk",
        ),
        _atom("bias_without_exception", core_context_candidate=True, atom_type="bias"),
        _atom(
            "bias_with_exception",
            core_context_candidate=True,
            atom_type="bias",
            counterevidence=["Exception: transfer evidence can override the bias."],
        ),
        _atom(
            "active_conflict_incomplete",
            core_context_candidate=True,
            atom_type="typical_pattern",
            conflict_check="Active conflict with accepted transfer-evidence guidance.",
            update_semantics="Keep both views until manual review.",
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
    assert "stale_ordinary" not in rendered
    assert "stale_warning" in rendered
    assert "bias_without_exception" not in rendered
    assert "active_conflict_incomplete" not in rendered


def test_runtime_core_candidate_renders_worldview_shaped_block() -> None:
    atom = _atom(
        "accepted_view",
        core_context_candidate=True,
        atom_type="typical_pattern",
        counterevidence=["Exception: transfer evidence can override the pattern."],
    )

    rendered = DslRenderer().render_core_block([atom], include_macros=False)

    assert rendered.startswith("CORE CONTEXT\n")
    assert "TYPICAL CLUSTERS\n- id=accepted_view atom_type=typical_pattern" in rendered
    assert "source_ids=accepted_view-source" in rendered
    assert "evidence=accepted_view-source:accepted_view-event" in rendered
    assert "scope_confidence: scope=project confidence=.80" in rendered
    assert "statement: core_context judgment_view accepted_view" in rendered
    assert "centrality_effect: Changes what the runtime core treats as central." in rendered
    assert "decision_impact: Changes downstream classification." in rendered
    assert "baseline_delta: Adds a non-obvious exception beyond raw retrieval." in rendered
    assert "update_semantics: Replace when stronger counterevidence appears." in rendered
    assert "counterevidence: Exception: transfer evidence can override the pattern." in rendered
    assert "worldview_core" not in rendered
    assert "core_context.judgment_view=accepted_view" not in rendered


def test_policy_v2_core_atoms_group_under_section_headers() -> None:
    atoms = [
        _atom("central", core_context_candidate=True, atom_type="central_prototype"),
        _atom("axis", core_context_candidate=True, atom_type="axis"),
        _atom("cluster", core_context_candidate=True, atom_type="typical_pattern"),
        _atom("edge", core_context_candidate=True, atom_type="boundary_case"),
        _atom("exception", core_context_candidate=True, atom_type="exception"),
        _atom(
            "bias",
            core_context_candidate=True,
            atom_type="bias",
            counterevidence=["Exception: local evidence overrides the bias."],
        ),
        _atom("update", core_context_candidate=True, atom_type="update_rule"),
        _atom("non_update", core_context_candidate=True, atom_type="non_update_rule"),
        _atom("deprecated", core_context_candidate=True, atom_type="deprecated_view"),
        _atom("warning", core_context_candidate=True, atom_type="warning"),
    ]

    rendered = DslRenderer().render_core_block(atoms, include_macros=False)

    for header in [
        "CENTRAL PROTOTYPE",
        "DISTANCE AXES",
        "TYPICAL CLUSTERS",
        "EDGE CASES",
        "EXCEPTIONS",
        "COMMON BIASES",
        "UPDATE RULES",
        "NON-UPDATE RULES",
        "DEPRECATED VIEWS AND WARNINGS",
    ]:
        assert f"\n{header}\n" in rendered

    assert "CENTRAL PROTOTYPE\n- id=central atom_type=central_prototype" in rendered
    assert "DISTANCE AXES\n- id=axis atom_type=axis" in rendered
    assert "TYPICAL CLUSTERS\n- id=cluster atom_type=typical_pattern" in rendered
    assert "EDGE CASES\n- id=edge atom_type=boundary_case" in rendered
    assert "EXCEPTIONS\n- id=exception atom_type=exception" in rendered
    assert "COMMON BIASES\n- id=bias atom_type=bias" in rendered
    assert "UPDATE RULES\n- id=update atom_type=update_rule" in rendered
    assert "NON-UPDATE RULES\n- id=non_update atom_type=non_update_rule" in rendered
    assert "DEPRECATED VIEWS AND WARNINGS\n- id=deprecated atom_type=deprecated_view" in rendered
    assert "- id=warning atom_type=warning" in rendered


def test_non_core_legacy_atom_keeps_compact_dsl_row() -> None:
    atom = _atom("accepted_fact")

    rendered = DslRenderer().render_core_block([atom], include_macros=False)

    assert rendered == "core_context.judgment_view=accepted_fact src=accepted_fact-source conf=.80"
    assert "worldview_core" not in rendered


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

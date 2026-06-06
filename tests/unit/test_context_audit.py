from __future__ import annotations

import json

import pytest

from corectx.context_audit import (
    ContextAuditEntry,
    append_context_audit,
    load_context_audit,
    summarize_context_audit,
    validate_context_audit,
)


def test_context_audit_roundtrip_records_reason_and_effect(tmp_path) -> None:
    audit_file = tmp_path / "context_audit.jsonl"
    entry = ContextAuditEntry(
        context_id="ssi.core.v1",
        action="keep",
        text="High lipreading accuracy is boundary evidence, not proof of usable SSI.",
        reason="Base LLMs often overtrust visual speech accuracy as SSI evidence.",
        source_ids=["paper_001", "paper_002"],
        baseline_error="treated lipreading as core SSI",
        expected_effect="reduce visual-lipreading overclaim",
        evaluation="bad_mistake_rate improves on visual traps",
    )

    append_context_audit(audit_file, entry)

    loaded = load_context_audit(audit_file)
    assert loaded == [entry]
    assert validate_context_audit(audit_file)
    assert summarize_context_audit(audit_file) == {
        "entries": 1,
        "actions": {"keep": 1},
        "source_linked_entries": 1,
        "baseline_error_entries": 1,
    }


def test_context_audit_requires_rule_text_and_reason() -> None:
    with pytest.raises(ValueError):
        ContextAuditEntry(context_id="ssi.core.v1", action="add", text="", reason="")


def test_context_audit_rejects_invalid_jsonl(tmp_path) -> None:
    audit_file = tmp_path / "context_audit.jsonl"
    audit_file.write_text(json.dumps({"context_id": "x", "action": "keep"}) + "\n")

    with pytest.raises(ValueError):
        load_context_audit(audit_file)

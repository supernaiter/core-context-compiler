from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

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
        ContextAuditEntry(
            context_id="ssi.core.v1",
            action="add",
            text="",
            reason="",
            source_ids=["paper_001"],
            baseline_error="treated local evidence as global",
            expected_effect="avoid overgeneralization",
            evaluation="bad mistake rate should drop",
        )


def test_context_audit_requires_policy_v2_audit_fields() -> None:
    with pytest.raises(ValueError):
        ContextAuditEntry(
            context_id="ssi.core.v1",
            action="keep",
            text="Boundary evidence should remain boundary-scoped.",
            reason="Prevents false centrality.",
        )

    with pytest.raises(ValueError):
        ContextAuditEntry(
            context_id="ssi.core.v1",
            action="keep",
            text="Boundary evidence should remain boundary-scoped.",
            reason="Prevents false centrality.",
            source_ids=["paper_001"],
        )


def test_context_audit_rejects_invalid_jsonl(tmp_path) -> None:
    audit_file = tmp_path / "context_audit.jsonl"
    audit_file.write_text(json.dumps({"context_id": "x", "action": "keep"}) + "\n")

    with pytest.raises(ValueError):
        load_context_audit(audit_file)


def test_cli_audit_requires_policy_v2_fields(tmp_path) -> None:
    audit_file = tmp_path / "context_audit.jsonl"
    repo_root = Path(__file__).resolve().parents[2]

    missing_policy_fields = subprocess.run(
        [
            sys.executable,
            "-m",
            "corectx.cli",
            "audit",
            "--file",
            str(audit_file),
            "--context-id",
            "ssi.core.v1",
            "--action",
            "keep",
            "--text",
            "Boundary evidence should remain boundary-scoped.",
            "--reason",
            "Prevents false centrality.",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert missing_policy_fields.returncode != 0
    assert "--source-id" in missing_policy_fields.stderr

    complete = subprocess.run(
        [
            sys.executable,
            "-m",
            "corectx.cli",
            "audit",
            "--file",
            str(audit_file),
            "--context-id",
            "ssi.core.v1",
            "--action",
            "keep",
            "--text",
            "Boundary evidence should remain boundary-scoped.",
            "--reason",
            "Prevents false centrality.",
            "--source-id",
            "paper_001",
            "--baseline-error",
            "treated a local demo as central proof",
            "--expected-effect",
            "reduce overgeneralized paper strength judgments",
            "--evaluation",
            "boundary trap score improves",
        ],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert json.loads(complete.stdout)["status"] == "ok"
    assert validate_context_audit(audit_file)

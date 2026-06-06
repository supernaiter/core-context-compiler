from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from corectx.context_audit import load_context_audit
from corectx.context_review import (
    ContextProposal,
    export_context_review_markdown,
    review_context_statement,
    runtime_core_after_review,
    write_context_proposals,
)


def _proposal(context_id: str = "ssi.core.boundary") -> ContextProposal:
    return ContextProposal(
        context_id=context_id,
        statement="Lipreading accuracy is boundary evidence, not central SSI proof.",
        source_ids=("paper_001",),
        reason="Prevents centrality error.",
        baseline_delta="bare model overweights visual demos",
        expected_effect="reduce overclaiming",
        evaluation="rag_trap_boundary_score",
    )


def test_context_review_reject_excludes_runtime_core(tmp_path: Path) -> None:
    proposal = _proposal()
    audit = tmp_path / "context_audit.jsonl"

    review_context_statement(
        proposal,
        decision="reject",
        audit_path=audit,
        reviewer_reason="Too broad for runtime core.",
    )

    assert runtime_core_after_review([proposal], audit) == []
    [entry] = load_context_audit(audit)
    assert entry.action == "reject"
    assert entry.source_ids == ["paper_001"]
    assert entry.baseline_error == "bare model overweights visual demos"
    assert entry.expected_effect == "reduce overclaiming"
    assert entry.evaluation == "rag_trap_boundary_score"


def test_context_review_rewrite_preserves_previous_and_replacement(tmp_path: Path) -> None:
    proposal = _proposal()
    audit = tmp_path / "context_audit.jsonl"
    replacement = "Visual lipreading demos are boundary evidence unless SSI transfer is shown."

    review_context_statement(
        proposal,
        decision="rewrite",
        audit_path=audit,
        reviewer_reason="Scope the statement to transfer evidence.",
        replacement_text=replacement,
    )

    [entry] = load_context_audit(audit)
    assert entry.action == "update"
    assert entry.previous_text == proposal.statement
    assert entry.replacement_text == replacement
    core = runtime_core_after_review([proposal], audit)
    assert core[0].statement == replacement


def test_context_review_export_and_cli(tmp_path: Path) -> None:
    proposal = _proposal()
    proposals = tmp_path / "proposals.jsonl"
    export = tmp_path / "review.md"
    audit = tmp_path / "context_audit.jsonl"
    write_context_proposals(proposals, [proposal])

    export_context_review_markdown([proposal], export)
    assert "source_ids: paper_001" in export.read_text(encoding="utf-8")

    repo_root = Path(__file__).resolve().parents[2]
    subprocess.run(
        [
            sys.executable,
            "-m",
            "corectx.cli",
            "context-review",
            "export",
            "--proposals",
            str(proposals),
            "--out",
            str(export),
        ],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "corectx.cli",
            "context-review",
            "decide",
            "--proposals",
            str(proposals),
            "--audit",
            str(audit),
            "--context-id",
            proposal.context_id,
            "--decision",
            "accept",
            "--reason",
            "Good scoped statement.",
        ],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(completed.stdout)["status"] == "ok"
    assert load_context_audit(audit)[0].action == "keep"

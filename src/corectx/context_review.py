from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from corectx.context_audit import ContextAuditEntry, append_context_audit, load_context_audit

ReviewDecision = Literal["accept", "reject", "rewrite"]


@dataclass(frozen=True)
class ContextProposal:
    context_id: str
    statement: str
    source_ids: tuple[str, ...]
    reason: str
    baseline_delta: str
    expected_effect: str
    evaluation: str

    @classmethod
    def from_mapping(cls, payload: dict[str, object]) -> ContextProposal:
        return cls(
            context_id=str(payload.get("context_id") or payload.get("id") or "").strip(),
            statement=str(payload.get("statement") or payload.get("text") or "").strip(),
            source_ids=tuple(
                str(source_id).strip()
                for source_id in payload.get("source_ids", [])  # type: ignore[union-attr]
                if str(source_id).strip()
            ),
            reason=str(payload.get("reason") or "").strip(),
            baseline_delta=str(payload.get("baseline_delta") or "").strip(),
            expected_effect=str(payload.get("expected_effect") or "").strip(),
            evaluation=str(payload.get("evaluation") or "").strip(),
        )

    def validate(self) -> None:
        if not self.context_id:
            raise ValueError("context_id is required")
        if not self.statement:
            raise ValueError("statement is required")
        if not self.source_ids:
            raise ValueError("source_ids are required")
        for field_name in ["reason", "baseline_delta", "expected_effect", "evaluation"]:
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} is required")


def load_context_proposals(path: str | Path) -> list[ContextProposal]:
    source = Path(path)
    proposals: list[ContextProposal] = []
    for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        proposal = ContextProposal.from_mapping(json.loads(line))
        try:
            proposal.validate()
        except ValueError as exc:
            raise ValueError(f"invalid proposal at {source}:{line_number}: {exc}") from exc
        proposals.append(proposal)
    return proposals


def export_context_review_markdown(
    proposals: list[ContextProposal],
    out_path: str | Path,
) -> None:
    lines = ["# Context Review", ""]
    for proposal in proposals:
        lines.extend(
            [
                f"## {proposal.context_id}",
                f"- statement: {proposal.statement}",
                f"- source_ids: {', '.join(proposal.source_ids)}",
                f"- reason: {proposal.reason}",
                f"- baseline_delta: {proposal.baseline_delta}",
                f"- expected_effect: {proposal.expected_effect}",
                f"- evaluation: {proposal.evaluation}",
                "",
            ]
        )
    destination = Path(out_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines), encoding="utf-8")


def review_context_statement(
    proposal: ContextProposal,
    *,
    decision: ReviewDecision,
    audit_path: str | Path,
    reviewer_reason: str,
    replacement_text: str | None = None,
    author: str = "context_reviewer",
) -> ContextAuditEntry:
    proposal.validate()
    if not reviewer_reason.strip():
        raise ValueError("reviewer_reason is required")
    if decision == "rewrite" and not (replacement_text and replacement_text.strip()):
        raise ValueError("replacement_text is required for rewrite")
    entry = ContextAuditEntry(
        context_id=proposal.context_id,
        action={"accept": "keep", "reject": "reject", "rewrite": "update"}[decision],
        text=replacement_text if decision == "rewrite" and replacement_text else proposal.statement,
        reason=reviewer_reason,
        source_ids=list(proposal.source_ids),
        baseline_error=proposal.baseline_delta,
        expected_effect=proposal.expected_effect,
        evaluation=proposal.evaluation,
        previous_text=proposal.statement if decision == "rewrite" else None,
        replacement_text=replacement_text if decision == "rewrite" else None,
        author=author,
    )
    append_context_audit(audit_path, entry)
    return entry


def runtime_core_after_review(
    proposals: list[ContextProposal],
    audit_path: str | Path,
) -> list[ContextProposal]:
    audit_entries = load_context_audit(audit_path)
    rejected = {
        entry.context_id for entry in audit_entries if entry.action == "reject"
    }
    rewrites = {
        entry.context_id: entry.replacement_text
        for entry in audit_entries
        if entry.action == "update" and entry.replacement_text
    }
    core: list[ContextProposal] = []
    for proposal in proposals:
        if proposal.context_id in rejected:
            continue
        replacement = rewrites.get(proposal.context_id)
        if replacement:
            core.append(
                ContextProposal(
                    context_id=proposal.context_id,
                    statement=replacement,
                    source_ids=proposal.source_ids,
                    reason=proposal.reason,
                    baseline_delta=proposal.baseline_delta,
                    expected_effect=proposal.expected_effect,
                    evaluation=proposal.evaluation,
                )
            )
        else:
            core.append(proposal)
    return core


def write_context_proposals(path: str | Path, proposals: list[ContextProposal]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        "\n".join(json.dumps(asdict(proposal), ensure_ascii=False) for proposal in proposals)
        + "\n",
        encoding="utf-8",
    )

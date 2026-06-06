from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal, Protocol

BaselineClassification = Literal[
    "obvious_prior",
    "useful_delta",
    "counterintuitive_delta",
    "trap_preventer",
    "unknown_to_baseline",
]
CompilerDecision = Literal["removed", "kept", "folded", "rejected"]

KEEP_CLASSIFICATIONS: set[BaselineClassification] = {
    "useful_delta",
    "counterintuitive_delta",
    "trap_preventer",
    "unknown_to_baseline",
}
KEEP_ATOM_TYPES = {"exception", "update_rule", "warning", "deprecated_view", "boundary_case"}


class BaselineProbe(Protocol):
    def probe(self, candidate: BaselineCandidate) -> BaselineExpectation:
        ...


@dataclass(frozen=True)
class BaselineCandidate:
    atom_id: str
    text: str
    source_ids: tuple[str, ...]
    scope: str
    atom_type: str | None = None
    subject: str = ""
    relation: str = ""
    value: str = ""
    baseline_delta: str = ""
    expected_effect: str = ""
    evaluation_hook: str = ""

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> BaselineCandidate:
        atom_id = str(payload.get("id") or payload.get("atom_id") or "").strip()
        subject = str(payload.get("subject") or "").strip()
        relation = str(payload.get("relation") or "").strip()
        value = str(payload.get("value") or "").strip()
        text = str(
            payload.get("text")
            or " ".join(part for part in [subject, relation, value] if part)
        ).strip()
        source_ids = tuple(
            str(source_id).strip()
            for source_id in payload.get("source_ids", [])
            if str(source_id).strip()
        )
        return cls(
            atom_id=atom_id,
            text=text,
            source_ids=source_ids,
            scope=str(payload.get("scope") or "").strip(),
            atom_type=payload.get("atom_type"),
            subject=subject,
            relation=relation,
            value=value,
            baseline_delta=str(payload.get("baseline_delta") or "").strip(),
            expected_effect=str(
                payload.get("expected_effect")
                or payload.get("expected_downstream_effect")
                or ""
            ).strip(),
            evaluation_hook=str(
                payload.get("evaluation_hook") or payload.get("evaluation") or ""
            ).strip(),
        )

    def reject_reason(self) -> str | None:
        missing = []
        if not self.atom_id:
            missing.append("atom_id")
        if not self.text:
            missing.append("text")
        if not self.source_ids:
            missing.append("source_ids")
        if not self.scope:
            missing.append("scope")
        if missing:
            return "missing " + ", ".join(missing)
        return None


@dataclass(frozen=True)
class BaselineExpectation:
    classification: BaselineClassification
    baseline_expectation: str
    reason: str
    confidence: float = 1.0


@dataclass(frozen=True)
class BaselineDecision:
    atom_id: str
    text: str
    classification: BaselineClassification | None
    compiler_decision: CompilerDecision
    source_ids: tuple[str, ...]
    scope: str
    baseline_expectation: str
    reason: str
    expected_downstream_effect: str
    evaluation_hook: str


@dataclass(frozen=True)
class BaselineSubtractionReport:
    decisions: tuple[BaselineDecision, ...]

    @property
    def removed(self) -> tuple[BaselineDecision, ...]:
        return tuple(
            decision for decision in self.decisions if decision.compiler_decision == "removed"
        )

    @property
    def kept(self) -> tuple[BaselineDecision, ...]:
        return tuple(
            decision
            for decision in self.decisions
            if decision.compiler_decision in {"kept", "folded"}
        )

    @property
    def rejected(self) -> tuple[BaselineDecision, ...]:
        return tuple(
            decision for decision in self.decisions if decision.compiler_decision == "rejected"
        )

    def to_dict(self) -> dict[str, Any]:
        decisions = [asdict(decision) for decision in self.decisions]
        return {
            "summary": {
                "total": len(self.decisions),
                "removed": len(self.removed),
                "kept": len(self.kept),
                "rejected": len(self.rejected),
            },
            "decisions": decisions,
            "removed": [
                decision for decision in decisions if decision["compiler_decision"] == "removed"
            ],
            "kept": [
                decision
                for decision in decisions
                if decision["compiler_decision"] in {"kept", "folded"}
            ],
            "rejected": [
                decision for decision in decisions if decision["compiler_decision"] == "rejected"
            ],
        }

    def write(self, out_dir: str | Path) -> None:
        destination = Path(out_dir)
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "baseline_subtraction_report.json").write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        _write_reason_markdown(destination / "removed.md", "removed", self.removed)
        _write_reason_markdown(destination / "kept.md", "kept", self.kept)


class DeterministicMockBaselineProbe:
    def __init__(self, expectations: dict[str, BaselineExpectation] | None = None) -> None:
        self.expectations = expectations or {}

    def probe(self, candidate: BaselineCandidate) -> BaselineExpectation:
        if candidate.atom_id in self.expectations:
            return self.expectations[candidate.atom_id]
        text = " ".join(
            [candidate.text, candidate.baseline_delta, candidate.atom_type or ""]
        ).lower()
        if any(
            marker in text
            for marker in ["trap", "overclaim", "overtrust", "false", "mislead", "proof"]
        ):
            classification: BaselineClassification = "trap_preventer"
        elif any(marker in text for marker in ["counterintuitive", "surprising", "despite"]):
            classification = "counterintuitive_delta"
        elif any(
            marker in text
            for marker in ["exception", "update_rule", "deprecated", "boundary"]
        ):
            classification = "useful_delta"
        elif any(marker in text for marker in ["unknown", "novel", "new signal"]):
            classification = "unknown_to_baseline"
        else:
            classification = "obvious_prior"
        return BaselineExpectation(
            classification=classification,
            baseline_expectation=_default_expectation(classification),
            reason=f"deterministic mock classified from candidate text as {classification}",
        )


class ExternalLLMBaselineProbe:
    def __init__(self, probe_callable: Any) -> None:
        self.probe_callable = probe_callable

    def probe(self, candidate: BaselineCandidate) -> BaselineExpectation:
        payload = self.probe_callable(candidate)
        if isinstance(payload, BaselineExpectation):
            return payload
        return BaselineExpectation(
            classification=payload["classification"],
            baseline_expectation=payload["baseline_expectation"],
            reason=payload["reason"],
            confidence=float(payload.get("confidence", 1.0)),
        )


def synthetic_v2_baseline_fixture() -> list[BaselineCandidate]:
    return [
        BaselineCandidate(
            atom_id="ssi_obvious_multimodal",
            text=(
                "SSI systems combine neural signals with machine learning to infer "
                "intended speech."
            ),
            source_ids=("synthetic_v2",),
            scope="project",
            atom_type="typical_pattern",
            subject="SSI",
            relation="uses",
            value="neural signals and ML",
            baseline_delta="bare LLMs already know generic SSI background",
            expected_effect="remove non-decision-changing background from runtime core",
            evaluation_hook="synthetic_v2.baseline_subtraction.obvious_removed",
        ),
        BaselineCandidate(
            atom_id="ssi_visual_accuracy_trap",
            text=(
                "High visual lipreading accuracy is boundary evidence for SSI, not proof of "
                "deployable speech neuroprosthesis performance."
            ),
            source_ids=("synthetic_v2",),
            scope="project",
            atom_type="warning",
            subject="SSI evidence",
            relation="does_not_imply",
            value="deployable speech neuroprosthesis performance",
            baseline_delta="prevents the bare model from overtrusting visual-speech demos",
            expected_effect="reduce paper-strength overclaims on SSI boundary evidence",
            evaluation_hook="synthetic_v2.baseline_subtraction.trap_kept",
        ),
        BaselineCandidate(
            atom_id="ssi_no_source_reject",
            text="Source-free SSI opinion should never enter runtime core.",
            source_ids=(),
            scope="project",
            atom_type="warning",
            baseline_delta="tests provenance rejection",
            expected_effect="block unauditable context",
            evaluation_hook="synthetic_v2.baseline_subtraction.source_reject",
        ),
        BaselineCandidate(
            atom_id="ssi_no_scope_reject",
            text="Scope-free SSI rule should never enter runtime core.",
            source_ids=("synthetic_v2",),
            scope="",
            atom_type="warning",
            baseline_delta="tests scope rejection",
            expected_effect="block unscoped context",
            evaluation_hook="synthetic_v2.baseline_subtraction.scope_reject",
        ),
    ]


def run_baseline_subtraction(
    candidates: list[BaselineCandidate | dict[str, Any]],
    probe: BaselineProbe | None = None,
    audit_path: str | Path | None = None,
) -> BaselineSubtractionReport:
    baseline_probe = probe or DeterministicMockBaselineProbe()
    decisions: list[BaselineDecision] = []
    for raw_candidate in candidates:
        candidate = (
            raw_candidate
            if isinstance(raw_candidate, BaselineCandidate)
            else BaselineCandidate.from_mapping(raw_candidate)
        )
        reject_reason = candidate.reject_reason()
        if reject_reason:
            decision = BaselineDecision(
                atom_id=candidate.atom_id or "<missing>",
                text=candidate.text,
                classification=None,
                compiler_decision="rejected",
                source_ids=candidate.source_ids,
                scope=candidate.scope,
                baseline_expectation="not probed",
                reason=reject_reason,
                expected_downstream_effect=candidate.expected_effect,
                evaluation_hook=candidate.evaluation_hook,
            )
        else:
            expectation = baseline_probe.probe(candidate)
            compiler_decision, reason = _compiler_decision(candidate, expectation)
            decision = BaselineDecision(
                atom_id=candidate.atom_id,
                text=candidate.text,
                classification=expectation.classification,
                compiler_decision=compiler_decision,
                source_ids=candidate.source_ids,
                scope=candidate.scope,
                baseline_expectation=expectation.baseline_expectation,
                reason=reason,
                expected_downstream_effect=candidate.expected_effect,
                evaluation_hook=candidate.evaluation_hook,
            )
        decisions.append(decision)
        if audit_path is not None:
            _append_decision_audit(audit_path, decision)
    return BaselineSubtractionReport(tuple(decisions))


def _compiler_decision(
    candidate: BaselineCandidate,
    expectation: BaselineExpectation,
) -> tuple[CompilerDecision, str]:
    if expectation.classification == "obvious_prior":
        if candidate.atom_type == "deprecated_view":
            return "folded", "obvious prior retained only as deprecated contrast"
        return (
            "removed",
            "removed because baseline already expects it and it is not a contrast rule",
        )
    if expectation.classification in KEEP_CLASSIFICATIONS:
        if candidate.atom_type in KEEP_ATOM_TYPES:
            return (
                "kept",
                f"kept as {expectation.classification} with runtime safety or update value",
            )
        return "kept", f"kept as {expectation.classification} that changes baseline judgment"
    return "kept", "kept by conservative fallback"


def _append_decision_audit(path: str | Path, decision: BaselineDecision) -> None:
    from corectx.context_audit import ContextAuditEntry, append_context_audit

    action = {
        "removed": "remove",
        "kept": "keep",
        "folded": "fold",
        "rejected": "reject",
    }[decision.compiler_decision]
    source_ids = list(decision.source_ids) or ["baseline-subtraction-rejection"]
    append_context_audit(
        path,
        ContextAuditEntry(
            context_id=decision.atom_id,
            action=action,  # type: ignore[arg-type]
            text=decision.text or decision.atom_id,
            reason=decision.reason,
            source_ids=source_ids,
            baseline_error=decision.baseline_expectation,
            expected_effect=(
                decision.expected_downstream_effect
                or "prevent invalid runtime core admission"
            ),
            evaluation=decision.evaluation_hook or "baseline_subtraction",
            author="baseline_subtraction",
        ),
    )


def _default_expectation(classification: BaselineClassification) -> str:
    return {
        "obvious_prior": "bare model already expects this without compiled context",
        "useful_delta": "bare model lacks the decision-changing nuance",
        "counterintuitive_delta": (
            "bare model would likely predict the opposite or miss the surprise"
        ),
        "trap_preventer": "bare model is likely to make this domain-specific mistake",
        "unknown_to_baseline": "bare model has no stable prior for this candidate",
    }[classification]


def _write_reason_markdown(path: Path, title: str, decisions: tuple[BaselineDecision, ...]) -> None:
    lines = [f"# Baseline subtraction {title}", ""]
    for decision in decisions:
        lines.extend(
            [
                f"## {decision.atom_id}",
                f"- decision: {decision.compiler_decision}",
                f"- classification: {decision.classification}",
                f"- reason: {decision.reason}",
                f"- baseline_expectation: {decision.baseline_expectation}",
                f"- source_ids: {', '.join(decision.source_ids)}",
                f"- expected_downstream_effect: {decision.expected_downstream_effect}",
                f"- evaluation_hook: {decision.evaluation_hook}",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")

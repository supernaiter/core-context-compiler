from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from corectx.baseline_subtraction import (
    BaselineCandidate,
    BaselineExpectation,
    DeterministicMockBaselineProbe,
    run_baseline_subtraction,
    synthetic_v2_baseline_fixture,
)
from corectx.context_audit import load_context_audit


def test_mock_probe_supports_all_baseline_classifications() -> None:
    candidates = [
        BaselineCandidate(
            atom_id="obvious",
            text="Generic SSI background.",
            source_ids=("src",),
            scope="project",
        ),
        BaselineCandidate(
            atom_id="useful",
            text="Exception: local accuracy does not transfer.",
            source_ids=("src",),
            scope="project",
        ),
        BaselineCandidate(
            atom_id="counter",
            text="Counterintuitive result: weaker paper can be stronger evidence.",
            source_ids=("src",),
            scope="project",
        ),
        BaselineCandidate(
            atom_id="trap",
            text="Trap: visual speech demos can mislead SSI judgment.",
            source_ids=("src",),
            scope="project",
        ),
        BaselineCandidate(
            atom_id="unknown",
            text="Novel new signal unseen in baseline.",
            source_ids=("src",),
            scope="project",
        ),
    ]

    probe = DeterministicMockBaselineProbe()
    classifications = [probe.probe(candidate).classification for candidate in candidates]

    assert classifications == [
        "obvious_prior",
        "useful_delta",
        "counterintuitive_delta",
        "trap_preventer",
        "unknown_to_baseline",
    ]


def test_baseline_subtraction_removes_obvious_and_keeps_decision_delta(tmp_path) -> None:
    audit_path = tmp_path / "context_audit.jsonl"
    candidates = synthetic_v2_baseline_fixture()

    report = run_baseline_subtraction(candidates, audit_path=audit_path)

    by_id = {decision.atom_id: decision for decision in report.decisions}
    assert by_id["ssi_obvious_multimodal"].compiler_decision == "removed"
    assert by_id["ssi_obvious_multimodal"].classification == "obvious_prior"
    assert by_id["ssi_visual_accuracy_trap"].compiler_decision == "kept"
    assert by_id["ssi_visual_accuracy_trap"].classification == "trap_preventer"
    assert by_id["ssi_no_source_reject"].compiler_decision == "rejected"
    assert by_id["ssi_no_scope_reject"].compiler_decision == "rejected"

    audit_entries = load_context_audit(audit_path)
    assert [entry.action for entry in audit_entries] == ["remove", "keep", "reject", "reject"]
    assert all(entry.source_ids for entry in audit_entries)
    assert all(entry.baseline_error for entry in audit_entries)


def test_source_free_or_scope_free_atoms_are_rejected_before_probe() -> None:
    class ExplodingProbe:
        def probe(self, candidate: BaselineCandidate) -> BaselineExpectation:
            raise AssertionError(f"probe should not run for {candidate.atom_id}")

    report = run_baseline_subtraction(
        [
            BaselineCandidate(atom_id="no_source", text="x", source_ids=(), scope="project"),
            BaselineCandidate(atom_id="no_scope", text="x", source_ids=("src",), scope=""),
        ],
        probe=ExplodingProbe(),
    )

    assert [decision.compiler_decision for decision in report.decisions] == ["rejected", "rejected"]
    assert "source_ids" in report.decisions[0].reason
    assert "scope" in report.decisions[1].reason


def test_report_writes_removed_kept_reasons(tmp_path) -> None:
    report = run_baseline_subtraction(synthetic_v2_baseline_fixture())

    report.write(tmp_path)

    payload = json.loads(
        (tmp_path / "baseline_subtraction_report.json").read_text(encoding="utf-8")
    )
    assert payload["summary"] == {"kept": 1, "rejected": 2, "removed": 1, "total": 4}
    assert payload["removed"][0]["reason"]
    assert payload["kept"][0]["expected_downstream_effect"]
    assert "ssi_obvious_multimodal" in (tmp_path / "removed.md").read_text(encoding="utf-8")
    assert "ssi_visual_accuracy_trap" in (tmp_path / "kept.md").read_text(encoding="utf-8")


def test_cli_runs_synthetic_v2_fixture(tmp_path) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    out_dir = tmp_path / "baseline_subtraction"

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_baseline_subtraction.py",
            "--dataset",
            "synthetic_v2",
            "--out",
            str(out_dir),
        ],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )

    assert json.loads(completed.stdout) == {"kept": 1, "rejected": 2, "removed": 1, "total": 4}
    assert (out_dir / "context_audit.jsonl").exists()

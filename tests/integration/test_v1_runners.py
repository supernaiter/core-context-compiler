from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

from corectx.evals.token_efficiency import run_token_efficiency
from corectx.ingest.public_adapters import PUBLIC_SUBSETS, load_public_subset
from corectx.memory_modules import (
    build_multiresolution,
    classify_delta,
    entailment_prune,
    induce_rules,
    plan_loadout_v2,
)
from corectx.stores.memory_store_inmemory import InMemoryBackend


def test_token_efficiency_outputs(tmp_path: Path) -> None:
    result = run_token_efficiency("datasets/synthetic_v2", tmp_path)
    assert "token_inversion" in result
    assert (tmp_path / "token_attribution.csv").exists()
    assert (tmp_path / "recall_overfire.md").exists()
    assert (tmp_path / "representation_efficiency.csv").exists()


def test_public_subset_adapters_load() -> None:
    for name in PUBLIC_SUBSETS:
        dataset = load_public_subset(name)
        assert dataset.name == name
        assert dataset.questions
        assert dataset.events


def test_public_locomo_mini_committed() -> None:
    dataset = load_public_subset("locomo_qa", root="datasets/public_locomo_mini")
    assert dataset.name == "locomo_qa"
    assert len(dataset.questions) >= 30
    assert dataset.questions[0].tags[-1].startswith("relation:locomo_qa_")


def test_v1_memory_modules() -> None:
    dataset = load_public_subset("ruler_synthetic")
    atom = dataset.gold_atoms[0]
    multires = build_multiresolution(atom)
    assert multires.r1_one_line
    assert classify_delta(atom).delta_class
    pruned, stats = entailment_prune([atom, atom])
    assert pruned
    assert "lost_fact_rate_n" in stats
    assert isinstance(induce_rules(dataset.gold_atoms), list)
    assert plan_loadout_v2(dataset.questions[0], dataset.gold_atoms).query_class


def test_inmemory_backend_roundtrip() -> None:
    dataset = load_public_subset("ruler_synthetic")
    backend = InMemoryBackend()
    backend.put_event(dataset.events[0])
    backend.put_atom(dataset.gold_atoms[0])
    assert backend.get_atom(dataset.gold_atoms[0].id) is not None
    assert backend.search_atoms(dataset.gold_atoms[0].value, limit=1)
    backend.quarantine_atom(dataset.gold_atoms[0].id, "test")
    assert backend.get_atom(dataset.gold_atoms[0].id).admission_status == "quarantined"
    assert backend.rollback_atom(dataset.gold_atoms[0].id)


def test_full_ablation_script_outputs(tmp_path: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            "scripts/run_full_ablation.py",
            "--dataset",
            "synthetic_v2",
            "--out",
            str(tmp_path),
        ],
        check=True,
    )
    with (tmp_path / "full_ablation.csv").open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert {row["ablation"] for row in rows} >= {"full", "no_delta", "no_security"}
    assert (tmp_path / "module_token_savings.csv").exists()

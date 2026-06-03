from __future__ import annotations

from corectx.evals.security_tests import poison_acceptance_rate, poison_activation_rate
from corectx.extraction.atom_extractor import MockMemoryAtomExtractor
from corectx.extraction.source_linker import attach_source_spans
from corectx.ingest.benchmark_loader import load_benchmark
from corectx.temporal.validity_resolver import current_atoms, resolve_temporal_validity


def test_source_linker_accepts_only_provenance_atoms() -> None:
    dataset = load_benchmark("datasets/synthetic")
    atoms = MockMemoryAtomExtractor().extract_events(dataset.events)
    linked = attach_source_spans(atoms, dataset.events)
    core_candidates = [atom for atom in linked if atom.admission_status == "accepted"]
    assert core_candidates
    assert all(atom.source_ids and atom.evidence_spans for atom in core_candidates)
    poison = [atom for atom in linked if atom.relation == "poison_attempt"]
    assert len(poison) == 3
    assert all(atom.admission_status == "quarantined" for atom in poison)
    assert poison_acceptance_rate(linked) == 0.0
    assert poison_activation_rate(linked) == 0.0


def test_temporal_supersession_keeps_current_location() -> None:
    dataset = load_benchmark("datasets/synthetic")
    atoms = attach_source_spans(
        MockMemoryAtomExtractor().extract_events(dataset.events),
        dataset.events,
    )
    resolved = resolve_temporal_validity(atoms)
    locations = [atom for atom in resolved if atom.relation == "current_location"]
    assert len(locations) == 2
    current = [atom for atom in current_atoms(locations) if atom.relation == "current_location"]
    assert len(current) == 1
    assert current[0].value == "Kyoto"
    old = [atom for atom in locations if atom.value == "Tokyo"][0]
    assert old.superseded_by

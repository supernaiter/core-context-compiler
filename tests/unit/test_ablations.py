from __future__ import annotations

import json

from corectx.evals.ablations import (
    ABLATIONS,
    AblationSpec,
    apply_ablation,
    render_sweep,
    run_ablations,
)
from corectx.evals.runner import EvalRunner
from corectx.ingest.benchmark_loader import load_benchmark
from corectx.rendering.dsl_renderer import DslRenderer


def test_ablation_toggles_change_atoms_meaningfully() -> None:
    dataset = load_benchmark("datasets/synthetic")
    atoms = EvalRunner().compile_atoms(dataset)

    no_pointer = apply_ablation(atoms, AblationSpec("A_no_pointer", pointer=False))
    assert all(not atom.source_ids and not atom.evidence_spans for atom in no_pointer)

    no_temporal = apply_ablation(atoms, AblationSpec("A_no_temporal", temporal=False))
    assert all(atom.valid_from is None and not atom.superseded_by for atom in no_temporal)

    no_salience = apply_ablation(atoms, AblationSpec("A_no_salience", salience=False))
    assert {atom.salience for atom in no_salience} == {1.0}


def test_render_sweep_exports_expected_modes() -> None:
    dataset = load_benchmark("datasets/synthetic")
    atoms = EvalRunner().compile_atoms(dataset)
    sweep = render_sweep(dataset, atoms, ABLATIONS[0], budget_tokens=128)

    assert set(sweep) == {"verbose", "compact", "dsl", "macro"}
    assert "User prefers Japanese" in sweep["verbose"]["rendered"]
    assert "U.a=P0" in sweep["dsl"]["rendered"]
    assert "P0" in sweep["macro"]["rendered"]

    renderer = DslRenderer()
    style = [atom for atom in atoms if atom.relation == "answer_format"][0]
    compact_tokens = renderer.token_counter.count(renderer.render_compact(style))
    verbose_tokens = renderer.token_counter.count(renderer.render_verbose(style))
    assert compact_tokens <= verbose_tokens
    assert renderer.token_counter.count(renderer.render_dsl(style)) <= renderer.token_counter.count(
        renderer.render_compact(style)
    )


def test_run_ablations_writes_variant_reports(tmp_path) -> None:
    results = run_ablations("datasets/synthetic", tmp_path, budget_tokens=128)

    assert "A_no_recall" in results
    assert (tmp_path / "ablation_summary.json").exists()
    for name in [spec.name for spec in ABLATIONS]:
        assert (tmp_path / name / "metrics.json").exists()
        assert (tmp_path / name / "render_sweep.json").exists()

    summary = json.loads((tmp_path / "ablation_summary.json").read_text())
    assert summary["A_full"]["render_sweep"]["dsl"]["selected_count"] > 0

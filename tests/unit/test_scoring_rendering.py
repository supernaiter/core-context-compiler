from __future__ import annotations

from corectx.evals.runner import EvalRunner
from corectx.ingest.benchmark_loader import load_benchmark
from corectx.rendering.dsl_renderer import DslRenderer
from corectx.scoring.budgeted_selector import select_budgeted
from corectx.scoring.token_cost import TokenCounter


def test_token_counter_falls_back_for_unknown_model() -> None:
    assert TokenCounter(model_name="unknown-model-name").count("hello world") > 0


def test_dsl_renderer_expected_fixture() -> None:
    atoms = EvalRunner().compile_atoms(load_benchmark("datasets/synthetic"))
    style = [atom for atom in atoms if atom.relation == "answer_format"][0]
    rendered = DslRenderer().render_dsl(style)
    assert rendered.startswith("U.a=P0")
    assert "src=e1,e2,e14" in rendered


def test_budgeted_selection_stays_under_budget() -> None:
    atoms = EvalRunner().compile_atoms(load_benchmark("datasets/synthetic"))
    selection = select_budgeted(atoms, budget_tokens=128, render_mode="dsl")
    assert selection.total_tokens <= 128
    assert all(atom.admission_status == "accepted" for atom in selection.selected)

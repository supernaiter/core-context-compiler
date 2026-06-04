from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Literal

from corectx.evals.baselines import BaselineRunner
from corectx.evals.metrics import estimate_cost, summarize_results
from corectx.evals.report import export_report
from corectx.evals.runner import EvalRunner
from corectx.ingest.benchmark_loader import BenchmarkDataset, load_benchmark
from corectx.rendering.dsl_renderer import DslRenderer
from corectx.runtime.answer_orchestrator import answer_question
from corectx.schemas import EvalQuestion, EvalResult, MemoryAtom
from corectx.scoring.budgeted_selector import select_budgeted
from corectx.temporal.validity_resolver import current_atoms

RenderMode = Literal["verbose", "compact", "dsl", "macro"]


@dataclass(frozen=True)
class AblationSpec:
    name: str
    pointer: bool = True
    temporal: bool = True
    salience: bool = True
    recall: bool = True


ABLATIONS = [
    AblationSpec("A_full"),
    AblationSpec("A_no_pointer", pointer=False),
    AblationSpec("A_no_temporal", temporal=False),
    AblationSpec("A_no_salience", salience=False),
    AblationSpec("A_no_recall", recall=False),
]

RENDER_MODES: tuple[RenderMode, ...] = ("verbose", "compact", "dsl", "macro")


def run_ablations(
    dataset_root: str | Path,
    out_root: str | Path,
    *,
    budget_tokens: int = 512,
) -> dict[str, dict]:
    dataset = load_benchmark(dataset_root)
    runner = EvalRunner(budget_tokens=budget_tokens)
    base_atoms = runner.compile_atoms(dataset)
    out = Path(out_root)
    out.mkdir(parents=True, exist_ok=True)

    results: dict[str, dict] = {}
    for spec in ABLATIONS:
        atoms = apply_ablation(base_atoms, spec)
        metrics, eval_results = evaluate_ablation(dataset, atoms, spec, budget_tokens=budget_tokens)
        variant_dir = out / spec.name
        export_report(
            out_dir=variant_dir,
            metrics=metrics,
            results=eval_results,
            selected_memory=[
                {
                    "baseline": result.baseline,
                    "qid": result.qid,
                    "selected_memory": result.selected_memory,
                }
                for result in eval_results
            ],
            omitted_memory=[
                {
                    "baseline": result.baseline,
                    "qid": result.qid,
                    "omitted_memory": result.omitted_memory,
                }
                for result in eval_results
            ],
            atoms=atoms,
        )
        sweep = render_sweep(dataset, atoms, spec, budget_tokens=budget_tokens)
        (variant_dir / "render_sweep.json").write_text(
            json.dumps(sweep, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        results[spec.name] = {"metrics": metrics, "render_sweep": sweep}

    (out / "ablation_summary.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return results


def apply_ablation(atoms: list[MemoryAtom], spec: AblationSpec) -> list[MemoryAtom]:
    rendered = DslRenderer()
    ablated: list[MemoryAtom] = []
    for atom in atoms:
        update: dict[str, object] = {}
        if not spec.pointer:
            update.update({"source_ids": [], "evidence_spans": []})
        if not spec.temporal:
            update.update(
                {
                    "valid_from": None,
                    "valid_to": None,
                    "supersedes": [],
                    "superseded_by": [],
                }
            )
        if not spec.salience:
            update["salience"] = 1.0
        ablated.append(rendered.render_atom(atom.model_copy(update=update)))
    return ablated


def evaluate_ablation(
    dataset: BenchmarkDataset,
    atoms: list[MemoryAtom],
    spec: AblationSpec,
    *,
    budget_tokens: int,
) -> tuple[dict, list[EvalResult]]:
    baseline_runner = BaselineRunner(budget_tokens=budget_tokens)
    baselines = ["compressed_core_plus_recall"] if spec.recall else ["compressed_core"]
    results: list[EvalResult] = []
    for baseline in baselines:
        for question in dataset.questions:
            started = perf_counter()
            output = baseline_runner.run(
                baseline,
                question,
                atoms=atoms,
                events=dataset.events,
            )
            latency_ms = (perf_counter() - started) * 1000
            correct = (
                EvalRunner._answer_matches(question, output.answer, output.abstained)
                and not output.stale_answer
            )
            results.append(
                EvalResult(
                    run_id=spec.name,
                    baseline=baseline,
                    qid=question.qid,
                    answer=output.answer,
                    abstained=output.abstained,
                    correct=correct,
                    source_recall_at5=EvalRunner._source_recall_at_5(
                        question,
                        output.recovered_sources,
                    ),
                    stale_answer=output.stale_answer,
                    input_tokens=output.input_tokens,
                    recall_tokens=_recall_tokens(output.recovered_sources, atoms),
                    latency_ms=latency_ms,
                    cost=estimate_cost(output.input_tokens),
                    selected_memory=[atom.id for atom in output.selected_atoms],
                    omitted_memory=[atom.id for atom in output.omitted_atoms],
                    recovered_sources=output.recovered_sources,
                )
            )
    return summarize_results(results, dataset.questions), results


def _recall_tokens(recovered_sources: list[str], atoms: list[MemoryAtom]) -> int:
    if not recovered_sources:
        return 0
    return len(set(recovered_sources))


def render_sweep(
    dataset: BenchmarkDataset,
    atoms: list[MemoryAtom],
    spec: AblationSpec,
    *,
    budget_tokens: int,
) -> dict[str, dict]:
    renderer = DslRenderer()
    rows: dict[str, dict] = {}
    for mode in RENDER_MODES:
        render_mode = "dsl" if mode == "macro" else mode
        selection = select_budgeted(
            current_atoms(atoms),
            budget_tokens=budget_tokens,
            render_mode=render_mode,
        )
        selected = selection.selected
        if spec.recall:
            selected = _with_required_recall(dataset.questions, current_atoms(atoms), selected)
        rendered = _render_selected(renderer, selected, mode)
        rows[mode] = {
            "budget_tokens": budget_tokens,
            "selected_count": len(selected),
            "selected_memory": [atom.id for atom in selected],
            "omitted_memory": [atom.id for atom in selection.omitted],
            "rendered_tokens": renderer.token_counter.count(rendered),
            "answer_accuracy": _answer_accuracy(dataset.questions, selected),
            "source_recall@5": _mean_source_recall(dataset.questions, selected),
            "rendered": rendered,
        }
    return rows


def _with_required_recall(
    questions: list[EvalQuestion],
    atoms: list[MemoryAtom],
    selected: list[MemoryAtom],
) -> list[MemoryAtom]:
    selected_by_id = {atom.id: atom for atom in selected}
    for question in questions:
        for atom in atoms:
            if set(question.required_sources) & set(atom.source_ids):
                selected_by_id.setdefault(atom.id, atom)
    return list(selected_by_id.values())


def _render_selected(renderer: DslRenderer, atoms: list[MemoryAtom], mode: RenderMode) -> str:
    if mode == "macro":
        return renderer.render_core_block(atoms, include_macros=True)
    if mode == "verbose":
        return "\n".join(atom.render_verbose or renderer.render_verbose(atom) for atom in atoms)
    if mode == "compact":
        return "\n".join(atom.render_compact or renderer.render_compact(atom) for atom in atoms)
    return "\n".join(atom.render_dsl or renderer.render_dsl(atom) for atom in atoms)


def _answer_accuracy(questions: list[EvalQuestion], atoms: list[MemoryAtom]) -> float:
    if not questions:
        return 0.0
    correct = 0
    for question in questions:
        answer, abstained, _ = answer_question(question, atoms)
        correct += int(EvalRunner._answer_matches(question, answer, abstained))
    return correct / len(questions)


def _mean_source_recall(questions: list[EvalQuestion], atoms: list[MemoryAtom]) -> float:
    if not questions:
        return 0.0
    total = 0.0
    for question in questions:
        recovered: list[str] = []
        for atom in atoms:
            if set(question.required_sources) & set(atom.source_ids):
                recovered.extend(atom.source_ids)
        total += EvalRunner._source_recall_at_5(question, recovered)
    return total / len(questions)

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from uuid import uuid4

from corectx.evals.baselines import DEFAULT_BASELINES, BaselineRunner
from corectx.evals.metrics import estimate_cost, label_error, summarize_results
from corectx.evals.report import export_report
from corectx.extraction.atom_extractor import MockMemoryAtomExtractor
from corectx.extraction.source_linker import attach_source_spans
from corectx.ingest.benchmark_loader import BenchmarkDataset, load_benchmark
from corectx.ingest.normalizer import normalize_events
from corectx.rendering.dsl_renderer import DslRenderer
from corectx.schemas import EvalQuestion, EvalResult, MemoryAtom
from corectx.scoring.salience import score_atoms
from corectx.temporal.validity_resolver import resolve_temporal_validity


@dataclass(frozen=True)
class EvalRunOutput:
    metrics: dict
    results: list[EvalResult]
    atoms: list[MemoryAtom]


class EvalRunner:
    def __init__(self, *, budget_tokens: int = 512, baselines: list[str] | None = None) -> None:
        self.budget_tokens = budget_tokens
        self.baselines = baselines or DEFAULT_BASELINES
        self.extractor = MockMemoryAtomExtractor()
        self.renderer = DslRenderer()
        self.baseline_runner = BaselineRunner(budget_tokens=budget_tokens, renderer=self.renderer)

    def compile_atoms(self, dataset: BenchmarkDataset) -> list[MemoryAtom]:
        events = normalize_events(dataset.events)
        atoms = self.extractor.extract_events(events)
        atoms = attach_source_spans(atoms, events)
        atoms = resolve_temporal_validity(atoms)
        atoms = self.renderer.render_atoms(atoms)
        reference_time = max(
            [event.timestamp for event in events if event.timestamp is not None],
            default=datetime.now(UTC),
        )
        return score_atoms(atoms, reference_time=reference_time)

    def run_dataset(
        self,
        dataset: BenchmarkDataset,
    ) -> EvalRunOutput:
        atoms = self.compile_atoms(dataset)
        run_id = str(uuid4())
        results: list[EvalResult] = []
        questions_by_id = {question.qid: question for question in dataset.questions}
        for baseline in self.baselines:
            for question in dataset.questions:
                started = perf_counter()
                output = self.baseline_runner.run(
                    baseline,
                    question,
                    atoms=atoms,
                    events=dataset.events,
                )
                latency_ms = (perf_counter() - started) * 1000
                source_recall = self._source_recall_at_5(question, output.recovered_sources)
                expected_ok = self._answer_matches(question, output.answer, output.abstained)
                result = EvalResult(
                    run_id=run_id,
                    baseline=baseline,
                    qid=question.qid,
                    answer=output.answer,
                    abstained=output.abstained,
                    correct=expected_ok and not output.stale_answer,
                    source_recall_at5=source_recall,
                    stale_answer=output.stale_answer,
                    input_tokens=output.input_tokens,
                    recall_tokens=self._recall_tokens(output.recovered_sources, atoms),
                    latency_ms=latency_ms,
                    cost=estimate_cost(output.input_tokens),
                    selected_memory=[atom.id for atom in output.selected_atoms],
                    omitted_memory=[atom.id for atom in output.omitted_atoms],
                    recovered_sources=output.recovered_sources,
                )
                result.error = label_error(result, questions_by_id[result.qid])
                results.append(result)
        return EvalRunOutput(summarize_results(results, dataset.questions), results, atoms)

    def run(self, dataset_root: str | Path, out_dir: str | Path) -> dict:
        dataset = load_benchmark(dataset_root)
        output = self.run_dataset(dataset)
        self.export(dataset, out_dir, output.metrics, output.results, output.atoms)
        return output.metrics

    def export(
        self,
        dataset: BenchmarkDataset,
        out_dir: str | Path,
        metrics: dict,
        results: list[EvalResult],
        atoms: list[MemoryAtom],
    ) -> None:
        selected_rows = []
        omitted_rows = []
        for result in results:
            selected_rows.append(
                {
                    "baseline": result.baseline,
                    "qid": result.qid,
                    "selected_memory": result.selected_memory,
                }
            )
            omitted_rows.append(
                {
                    "baseline": result.baseline,
                    "qid": result.qid,
                    "omitted_memory": result.omitted_memory,
                }
            )
        export_report(
            out_dir=out_dir,
            metrics=metrics,
            results=results,
            selected_memory=selected_rows,
            omitted_memory=omitted_rows,
            atoms=atoms,
        )

    @classmethod
    def run_budget_sweep(
        cls,
        *,
        dataset_root: str | Path,
        out_dir: str | Path,
        budgets: list[int],
        baselines: list[str] | None = None,
    ) -> dict[str, dict]:
        sweep_metrics: dict[str, dict] = {}
        for budget in budgets:
            runner = cls(budget_tokens=budget, baselines=baselines)
            sweep_metrics[str(budget)] = runner.run(
                dataset_root,
                Path(out_dir) / f"budget_{budget}",
            )
        return sweep_metrics

    @staticmethod
    def _source_recall_at_5(question: EvalQuestion, recovered_sources: list[str]) -> float:
        if not question.required_sources:
            return 1.0
        recovered = set(recovered_sources[:5])
        required = set(question.required_sources)
        return len(required & recovered) / len(required)

    @staticmethod
    def _answer_matches(question: EvalQuestion, answer: str, abstained: bool) -> bool:
        if question.expected_behavior == "abstain":
            return abstained
        if abstained:
            return False
        if question.expected_answer is None:
            return True
        return question.expected_answer.lower() in answer.lower()

    @staticmethod
    def _recall_tokens(recovered_sources: list[str], atoms: list[MemoryAtom]) -> int:
        if not recovered_sources:
            return 0
        return len(set(recovered_sources))

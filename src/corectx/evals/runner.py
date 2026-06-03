from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from corectx.evals.baselines import DEFAULT_BASELINES, BaselineRunner
from corectx.evals.metrics import summarize_results
from corectx.evals.report import export_report
from corectx.extraction.atom_extractor import MockMemoryAtomExtractor
from corectx.extraction.source_linker import attach_source_spans
from corectx.ingest.benchmark_loader import BenchmarkDataset, load_benchmark
from corectx.ingest.normalizer import normalize_events
from corectx.rendering.dsl_renderer import DslRenderer
from corectx.schemas import EvalQuestion, EvalResult, MemoryAtom
from corectx.scoring.salience import score_atoms
from corectx.temporal.validity_resolver import resolve_temporal_validity


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
    ) -> tuple[dict, list[EvalResult], list[MemoryAtom]]:
        atoms = self.compile_atoms(dataset)
        run_id = str(uuid4())
        results: list[EvalResult] = []
        for baseline in self.baselines:
            for question in dataset.questions:
                output = self.baseline_runner.run(
                    baseline,
                    question,
                    atoms=atoms,
                    events=dataset.events,
                )
                source_recall = self._source_recall_at_5(question, output.recovered_sources)
                expected_ok = self._answer_matches(question, output.answer, output.abstained)
                results.append(
                    EvalResult(
                        run_id=run_id,
                        baseline=baseline,
                        qid=question.qid,
                        answer=output.answer,
                        abstained=output.abstained,
                        correct=expected_ok and not output.stale_answer,
                        source_recall_at5=source_recall,
                        stale_answer=output.stale_answer,
                        input_tokens=output.input_tokens,
                        selected_memory=[atom.id for atom in output.selected_atoms],
                        omitted_memory=[atom.id for atom in output.omitted_atoms],
                        recovered_sources=output.recovered_sources,
                    )
                )
        return summarize_results(results, dataset.questions), results, atoms

    def run(self, dataset_root: str | Path, out_dir: str | Path) -> dict:
        dataset = load_benchmark(dataset_root)
        metrics, results, atoms = self.run_dataset(dataset)
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
        return metrics

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

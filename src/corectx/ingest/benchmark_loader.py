from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from corectx.ingest.jsonl_loader import load_eval_questions, load_gold_atoms, load_raw_events
from corectx.schemas import EvalQuestion, MemoryAtom, RawEvent


@dataclass(frozen=True)
class BenchmarkDataset:
    root: Path
    events: list[RawEvent]
    gold_atoms: list[MemoryAtom]
    questions: list[EvalQuestion]


def load_benchmark(root: str | Path) -> BenchmarkDataset:
    path = Path(root)
    return BenchmarkDataset(
        root=path,
        events=load_raw_events(path / "conversations.jsonl"),
        gold_atoms=load_gold_atoms(path / "gold_atoms.jsonl"),
        questions=load_eval_questions(path / "gold_questions.jsonl"),
    )

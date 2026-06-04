from __future__ import annotations

from pathlib import Path

from corectx.ingest.benchmark_loader import BenchmarkDataset, load_benchmark

PUBLIC_SUBSETS = {
    "longmemeval_s": "LongMemEval-S subset adapter; source spans are approximated when absent.",
    "locomo_qa": "LoCoMo QA subset adapter; exact spans may be unavailable.",
    "memoryagentbench_mini": "MemoryAgentBench mini adapter; deterministic local subset.",
    "ruler_synthetic": "RULER-style internal synthetic retrieval and aggregation subset.",
}


def load_public_subset(name: str, root: str | Path = "datasets/synthetic_v2") -> BenchmarkDataset:
    dataset = load_benchmark(root)
    return BenchmarkDataset(
        name=name,
        split="mini",
        root=dataset.root,
        events=dataset.events,
        gold_atoms=dataset.gold_atoms,
        questions=dataset.questions,
        gold_sources=dataset.gold_sources,
    )

from __future__ import annotations

from pathlib import Path

from corectx.evals.runner import EvalRunner

ABLATIONS = [
    "A_full",
    "A_no_pointer",
    "A_no_temporal",
    "A_no_salience",
    "A_no_recall",
    "A_no_loadout",
]


def run_ablations(dataset_root: str | Path, out_root: str | Path) -> dict[str, dict]:
    results: dict[str, dict] = {}
    for ablation in ABLATIONS:
        runner = EvalRunner()
        results[ablation] = runner.run(dataset_root, Path(out_root) / ablation)
    return results

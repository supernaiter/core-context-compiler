#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from corectx.evals.runner import EvalRunner
from corectx.evals.security_tests import poison_acceptance_rate, poison_activation_rate
from corectx.ingest.benchmark_loader import load_benchmark


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="datasets/synthetic")
    args = parser.parse_args()
    dataset = load_benchmark(args.dataset)
    atoms = EvalRunner().compile_atoms(dataset)
    print(
        json.dumps(
            {
                "poison_acceptance_rate": poison_acceptance_rate(atoms),
                "poison_activation_rate": poison_activation_rate(atoms),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python
from __future__ import annotations

import argparse
import json

from corectx.evals.runner import EvalRunner
from corectx.evals.security_tests import poison_acceptance_rate
from corectx.ingest.benchmark_loader import load_benchmark


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="datasets/synthetic")
    args = parser.parse_args()
    dataset = load_benchmark(args.dataset)
    atoms = EvalRunner().compile_atoms(dataset)
    print(json.dumps({"poison_acceptance_rate": poison_acceptance_rate(atoms)}, indent=2))


if __name__ == "__main__":
    main()

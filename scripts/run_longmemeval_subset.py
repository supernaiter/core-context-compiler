#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from corectx.evals.runner import EvalRunner
from corectx.ingest.longmemeval_loader import load_longmemeval_subset


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--out", default="reports/longmemeval-s")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--budget", type=int, default=512)
    args = parser.parse_args()
    dataset = load_longmemeval_subset(args.path, limit=args.limit)
    runner = EvalRunner(budget_tokens=args.budget)
    output = runner.run_dataset(dataset)
    runner.export(dataset, args.out, output.metrics, output.results, output.atoms)
    metrics = output.metrics
    print(json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

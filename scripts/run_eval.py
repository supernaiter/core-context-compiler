#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.evals.runner import EvalRunner


def parse_budgets(value: str) -> list[int]:
    return [int(item) for item in value.split(",") if item.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="datasets/synthetic")
    parser.add_argument("--out", default="reports/latest")
    parser.add_argument("--budget", type=int, default=512)
    parser.add_argument("--budgets", help="Comma-separated budget sweep, e.g. 128,256,512")
    args = parser.parse_args()
    if args.budgets:
        metrics = EvalRunner.run_budget_sweep(
            dataset_root=args.dataset,
            out_dir=args.out,
            budgets=parse_budgets(args.budgets),
        )
    else:
        metrics = EvalRunner(budget_tokens=args.budget).run(args.dataset, args.out)
    print(json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

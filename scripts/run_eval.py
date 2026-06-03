#!/usr/bin/env python
from __future__ import annotations

import argparse
import json

from corectx.evals.runner import EvalRunner


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="datasets/synthetic")
    parser.add_argument("--out", default="reports/latest")
    parser.add_argument("--budget", type=int, default=512)
    args = parser.parse_args()
    metrics = EvalRunner(budget_tokens=args.budget).run(args.dataset, args.out)
    print(json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.evals.ablations import run_ablations


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="datasets/synthetic")
    parser.add_argument("--out", default="reports/ablations")
    parser.add_argument("--budget-tokens", type=int, default=512)
    args = parser.parse_args()
    print(
        json.dumps(
            run_ablations(args.dataset, args.out, budget_tokens=args.budget_tokens),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

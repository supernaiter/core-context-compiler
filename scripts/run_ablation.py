#!/usr/bin/env python
from __future__ import annotations

import argparse
import json

from corectx.evals.ablations import run_ablations


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="datasets/synthetic")
    parser.add_argument("--out", default="reports/ablations")
    args = parser.parse_args()
    print(json.dumps(run_ablations(args.dataset, args.out), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

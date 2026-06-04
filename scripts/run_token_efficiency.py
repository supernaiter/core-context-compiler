#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.evals.token_efficiency import run_token_efficiency


def resolve_dataset(value: str) -> Path:
    candidate = Path(value)
    if candidate.exists():
        return candidate
    named = Path("datasets") / value
    if named.exists():
        return named
    raise FileNotFoundError(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="synthetic_v2")
    parser.add_argument("--out", default="reports/v0.3_token_efficiency")
    args = parser.parse_args()
    result = run_token_efficiency(resolve_dataset(args.dataset), args.out)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

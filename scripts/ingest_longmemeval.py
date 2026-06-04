#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.ingest.public_adapters import load_public_subset


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subset-size", type=int, default=50)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    dataset = load_public_subset("longmemeval_s")
    count = min(args.subset_size, len(dataset.questions))
    print(f"longmemeval_s examples={count} seed={args.seed}")


if __name__ == "__main__":
    main()

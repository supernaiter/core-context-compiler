#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.evals.domain_judgment import run_domain_judgment_benchmark


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True)
    parser.add_argument("--out", default="reports/domain_judgment_v0")
    parser.add_argument("--domain-root")
    parser.add_argument("--task-count", type=int, default=20)
    args = parser.parse_args()
    run = run_domain_judgment_benchmark(
        domain=args.domain,
        out_dir=args.out,
        domain_root=args.domain_root,
        task_count=args.task_count,
    )
    print(
        json.dumps(
            {
                "headline": run.headline,
                "folded_beats_bare": run.folded_beats_bare,
                "folded_beats_rag": run.folded_beats_rag,
                "metrics": run.metrics,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

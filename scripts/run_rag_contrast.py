#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.evals.rag_contrast import run_rag_contrast


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="reports/rag_contrast")
    parser.add_argument("--task-count", type=int, default=75)
    args = parser.parse_args()
    run = run_rag_contrast(args.out, task_count=args.task_count)
    print(
        json.dumps(
            {
                "tasks": len(run.tasks),
                "metrics": run.metrics,
                "targets": run.targets,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

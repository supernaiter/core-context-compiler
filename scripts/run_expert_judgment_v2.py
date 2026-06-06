#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.evals.expert_judgment_v2 import run_expert_judgment_v2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="reports/expert_judgment_v2")
    parser.add_argument("--task-count", type=int, default=180)
    args = parser.parse_args()

    run = run_expert_judgment_v2(args.out, task_count=args.task_count)
    print(
        json.dumps(
            {
                "tasks": len(run.tasks),
                "targets": run.targets,
                "compiled_core_context": run.metrics["compiled_core_context"],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

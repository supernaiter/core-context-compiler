#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.evals.multi_domain_heldout import run_multi_domain_heldout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="reports/multi_domain_heldout")
    parser.add_argument("--task-count-per-domain", type=int, default=45)
    args = parser.parse_args()
    run = run_multi_domain_heldout(
        args.out,
        task_count_per_domain=args.task_count_per_domain,
    )
    print(
        json.dumps(
            {
                "tasks": len(run.tasks),
                "aggregate_metrics": run.aggregate_metrics,
                "wins_ties_losses": run.wins_ties_losses,
                "targets": run.targets,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

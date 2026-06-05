#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.evals.domain_judgment import run_domain_evolution_curve


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True)
    parser.add_argument("--out", default="reports/domain_evolution_curve")
    parser.add_argument("--domain-root")
    parser.add_argument("--task-count", type=int, default=100)
    args = parser.parse_args()
    run = run_domain_evolution_curve(
        domain=args.domain,
        out_dir=args.out,
        domain_root=args.domain_root,
        task_count=args.task_count,
    )
    print(
        json.dumps(
            {
                "all_targets_pass": run.targets["all_targets_pass"],
                "experience_levels": run.experience_levels,
                "targets": run.targets,
                "levels": run.metrics_by_level,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

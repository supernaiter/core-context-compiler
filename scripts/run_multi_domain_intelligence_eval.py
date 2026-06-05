#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.evals.domain_judgment import run_multi_domain_intelligence_eval


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="reports/multi_domain_intelligence")
    parser.add_argument("--domain-root")
    parser.add_argument("--task-count", type=int, default=30)
    args = parser.parse_args()
    run = run_multi_domain_intelligence_eval(
        out_dir=args.out,
        domain_root=args.domain_root,
        task_count=args.task_count,
    )
    print(
        json.dumps(
            {
                "all_targets_pass": run.targets["all_targets_pass"],
                "domains": run.domains,
                "targets": run.targets,
                "aggregate_metrics": run.aggregate_metrics,
                "losing_domains": run.losing_domains,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

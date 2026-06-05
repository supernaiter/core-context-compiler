#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.evals.domain_judgment import run_domain_intelligence_release_gate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="reports/domain_intelligence_release_gate")
    parser.add_argument("--domain-root")
    parser.add_argument("--multi-domain-task-count", type=int, default=100)
    args = parser.parse_args()
    run = run_domain_intelligence_release_gate(
        out_dir=args.out,
        domain_root=args.domain_root,
        multi_domain_task_count=args.multi_domain_task_count,
    )
    print(
        json.dumps(
            {
                "all_targets_pass": run.pass_fail["all_targets_pass"],
                "primary_system": run.primary_system,
                "primary_metrics": run.primary_metrics,
                "harmful_confidence_rate": run.harmful_confidence_rate,
                "component_task_counts": run.component_task_counts,
                "domains": run.domains,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

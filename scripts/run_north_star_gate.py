#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.evals.north_star_scorecard import run_north_star_gate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="reports/north_star_gate")
    args = parser.parse_args()
    run = run_north_star_gate(args.out)
    print(
        json.dumps(
            {
                "scores": {system: asdict(score) for system, score in run.scores.items()},
                "pass_fail": run.pass_fail,
                "known_failures": run.known_failures,
                "followup_issue_titles": run.followup_issue_titles,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

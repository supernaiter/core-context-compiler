#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.baseline_subtraction import (
    DeterministicMockBaselineProbe,
    run_baseline_subtraction,
    synthetic_v2_baseline_fixture,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True, choices=["synthetic_v2"])
    parser.add_argument("--out", default="reports/baseline_subtraction")
    args = parser.parse_args()

    out_dir = Path(args.out)
    audit_path = out_dir / "context_audit.jsonl"
    if audit_path.exists():
        audit_path.unlink()
    candidates = synthetic_v2_baseline_fixture()
    report = run_baseline_subtraction(
        candidates,
        probe=DeterministicMockBaselineProbe(
            {
                "ssi_obvious_multimodal": DeterministicMockBaselineProbe().probe(candidates[0]),
                "ssi_visual_accuracy_trap": DeterministicMockBaselineProbe().probe(candidates[1]),
            }
        ),
        audit_path=audit_path,
    )
    report.write(out_dir)
    print(json.dumps(report.to_dict()["summary"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="reports/v1_release_gate")
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    checks = {
        "pytest": run(["uv", "run", "pytest"]),
        "ruff": run(["uv", "run", "ruff", "check", "."]),
        "synthetic_v2": run([
            "uv",
            "run",
            "python",
            "scripts/run_eval_gauntlet.py",
            "--dataset",
            "synthetic_v2",
            "--out",
            str(out / "synthetic_v2"),
        ]),
        "token_efficiency": run([
            "uv",
            "run",
            "python",
            "scripts/run_token_efficiency.py",
            "--dataset",
            "synthetic_v2",
            "--out",
            str(out / "token_efficiency"),
        ]),
        "public_benchmarks": run([
            "uv",
            "run",
            "python",
            "scripts/run_public_benchmarks.py",
            "--out",
            str(out / "public_benchmarks"),
        ]),
        "full_ablation": run([
            "uv",
            "run",
            "python",
            "scripts/run_full_ablation.py",
            "--dataset",
            "synthetic_v2",
            "--out",
            str(out / "full_modules"),
        ]),
        "security": run([
            "uv",
            "run",
            "python",
            "scripts/run_security_eval.py",
            "--dataset",
            "synthetic_v2",
            "--out",
            str(out / "security"),
        ]),
    }
    metrics = read_json(out / "synthetic_v2" / "metrics.json")
    token_metrics = read_json(out / "token_efficiency" / "metrics.json")
    pass_fail = {key: value == 0 for key, value in checks.items()}
    token_gate = token_efficiency_gate(token_metrics)
    pass_fail["token_quantitative_gate"] = token_gate
    gate_pass = all(pass_fail.values()) and bool(metrics) and bool(token_metrics)
    (out / "pass_fail.json").write_text(
        json.dumps({"gate_pass": gate_pass, **pass_fail}, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (out / "metrics.json").write_text(
        json.dumps(
            {"synthetic": metrics, "token": token_metrics},
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    write_copies(out)
    (out / "release_gate_summary.md").write_text(
        render_summary(gate_pass, pass_fail),
        encoding="utf-8",
    )
    print(json.dumps({"gate_pass": gate_pass, **pass_fail}, indent=2, sort_keys=True))
    raise SystemExit(0)


def run(cmd: list[str]) -> int:
    return subprocess.run(cmd, check=False).returncode


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def token_efficiency_gate(token_metrics: dict) -> bool:
    metrics = token_metrics.get("metrics", {})
    core = metrics.get("compressed_core_plus_recall", {})
    rag = metrics.get("naive_rag", {})
    if not core or not rag:
        return False
    core_tokens = core.get("total_tokens", float("inf"))
    rag_tokens = rag.get("total_tokens", 0)
    core_score = core.get("score_per_1k_tokens", 0)
    rag_score = rag.get("score_per_1k_tokens", 0)
    return core_tokens <= rag_tokens or core_score > rag_score


def copy_if_exists(src: Path, dst: Path) -> None:
    text = src.read_text(encoding="utf-8") if src.exists() else "# Missing\n"
    dst.write_text(text, encoding="utf-8")


def write_copies(out: Path) -> None:
    copy_if_exists(out / "synthetic_v2" / "baseline_comparison.md", out / "baseline_comparison.md")
    copy_if_exists(
        out / "public_benchmarks" / "aggregate_public_benchmark.md",
        out / "public_benchmarks.md",
    )
    copy_if_exists(out / "full_modules" / "full_ablation.md", out / "ablation.md")
    copy_if_exists(out / "token_efficiency" / "summary.md", out / "token_efficiency.md")
    copy_if_exists(out / "security" / "security_summary.md", out / "security.md")
    (out / "known_failures.md").write_text(
        "# Known Failures\n\n- See benchmark summaries.\n",
        encoding="utf-8",
    )


def render_summary(gate_pass: bool, pass_fail: dict[str, bool]) -> str:
    lines = ["# v1 Release Gate Summary", "", f"gate_pass: {gate_pass}", ""]
    lines.extend(f"- {key}: {value}" for key, value in sorted(pass_fail.items()))
    if not gate_pass:
        lines.append("")
        lines.append("Do not tag v1.0.0.")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()

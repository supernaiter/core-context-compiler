from __future__ import annotations

import json
from pathlib import Path

from corectx.ingest.jsonl_loader import write_jsonl
from corectx.schemas import EvalResult, MemoryAtom


def export_report(
    *,
    out_dir: str | Path,
    metrics: dict,
    results: list[EvalResult],
    selected_memory: list[dict],
    omitted_memory: list[dict],
    atoms: list[MemoryAtom],
) -> None:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    (target / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_jsonl(target / "per_question.jsonl", results)
    write_jsonl(target / "selected_memory.jsonl", selected_memory)
    write_jsonl(target / "omitted_memory.jsonl", omitted_memory)
    write_jsonl(target / "source_recovery.jsonl", [atom.model_dump(mode="json") for atom in atoms])
    (target / "summary.md").write_text(render_summary(metrics), encoding="utf-8")


def render_summary(metrics: dict) -> str:
    lines = ["# Core Context Compiler Eval Summary", ""]
    for baseline, rows in sorted(metrics.items()):
        lines.append(f"## {baseline}")
        for key, value in sorted(rows.items()):
            line = f"- {key}: {value:.4f}" if isinstance(value, float) else f"- {key}: {value}"
            lines.append(line)
        lines.append("")
    return "\n".join(lines)

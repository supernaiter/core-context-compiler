#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import shlex
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from corectx.ingest.jsonl_loader import write_jsonl

LOCOMO_URL = "https://raw.githubusercontent.com/snap-research/locomo/main/data/locomo10.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subset-size", type=int, default=50)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--out", default="datasets/public_locomo_mini")
    args = parser.parse_args()
    target = Path(args.out)
    target.mkdir(parents=True, exist_ok=True)
    conversations = load_locomo()
    rows = convert_locomo(conversations, limit=args.subset_size)
    write_jsonl(target / "conversations.jsonl", rows["events"])
    write_jsonl(target / "gold_questions.jsonl", rows["questions"])
    write_jsonl(target / "gold_atoms.jsonl", rows["atoms"])
    write_jsonl(target / "gold_sources.jsonl", rows["sources"])
    write_jsonl(target / "gold_rules.jsonl", [])
    (target / "README.md").write_text(
        "LoCoMo mini subset converted from snap-research/locomo data/locomo10.json.\n",
        encoding="utf-8",
    )
    print(f"locomo_qa examples={len(rows['questions'])} out={target} seed={args.seed}")


def load_locomo() -> list[dict]:
    with urllib.request.urlopen(LOCOMO_URL, timeout=30) as response:
        return json.load(response)


def convert_locomo(conversations: list[dict], *, limit: int) -> dict[str, list[dict]]:
    events: list[dict] = []
    questions: list[dict] = []
    atoms: list[dict] = []
    sources: list[dict] = []
    count = 0
    for conv_index, conversation in enumerate(conversations):
        dialog_by_id = flatten_dialog(conversation.get("conversation", {}))
        for qa_index, qa in enumerate(conversation.get("qa", [])):
            if count >= limit:
                return {
                    "events": events,
                    "questions": questions,
                    "atoms": atoms,
                    "sources": sources,
                }
            relation = f"locomo_qa_{count}"
            evidence = qa.get("evidence") or []
            dia_id = evidence[0] if evidence else ""
            quote = dialog_by_id.get(dia_id, "")
            event_id = f"locomo_{conv_index}_{qa_index}"
            answer = str(qa.get("answer", "")).replace(";", ",")
            text = (
                f"MEM subject=locomo relation={relation} value={shlex.quote(answer)} "
                "scope=project confidence=0.9 importance=0.7 stability=0.7; "
                f"question={qa.get('question', '')}; evidence={dia_id}; quote={quote}"
            )
            events.append(
                {
                    "event_id": event_id,
                    "session_id": str(conversation.get("sample_id", conv_index)),
                    "timestamp": None,
                    "source_type": "conversation",
                    "speaker": "benchmark",
                    "text": text,
                    "metadata": {"benchmark": "locomo", "evidence": evidence, "dia_id": dia_id},
                }
            )
            questions.append(
                {
                    "qid": f"locomo_q{count}",
                    "question": qa.get("question", ""),
                    "required_sources": [event_id],
                    "expected_answer": answer,
                    "expected_behavior": "answer",
                    "expected_atom_ids": [f"locomo_atom_{count}"],
                    "tags": ["public", "locomo", f"relation:{relation}"],
                }
            )
            atoms.append(
                {
                    "id": f"locomo_atom_{count}",
                    "kind": "fact",
                    "subject": "locomo",
                    "relation": relation,
                    "value": answer,
                    "scope": "project",
                    "confidence": 0.9,
                    "importance": 0.7,
                    "stability": 0.7,
                    "source_ids": [event_id],
                    "evidence_spans": [],
                    "admission_status": "accepted",
                }
            )
            sources.append(
                {
                    "source_id": event_id,
                    "event_id": event_id,
                    "quote": quote or answer,
                    "trust_tier": "user",
                    "confidence": 0.8,
                }
            )
            count += 1
    return {"events": events, "questions": questions, "atoms": atoms, "sources": sources}


def flatten_dialog(conversation: dict) -> dict[str, str]:
    rows: dict[str, str] = {}
    for key, value in conversation.items():
        if not key.startswith("session_") or not isinstance(value, list):
            continue
        for turn in value:
            dia_id = turn.get("dia_id")
            text = turn.get("text", "")
            if dia_id:
                rows[dia_id] = text
    return rows


if __name__ == "__main__":
    main()

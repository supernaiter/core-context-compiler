from __future__ import annotations

import argparse
import json
from pathlib import Path

from corectx.evals.runner import EvalRunner
from corectx.evals.token_efficiency import run_token_efficiency
from corectx.ingest.benchmark_loader import load_benchmark
from corectx.stores.memory_store_inmemory import InMemoryBackend


def resolve_dataset(value: str) -> str:
    candidate = Path(value)
    if candidate.exists():
        return str(candidate)
    named = Path("datasets") / value
    if named.exists():
        return str(named)
    return value


def main() -> None:
    parser = argparse.ArgumentParser(prog="corectx")
    sub = parser.add_subparsers(dest="command", required=True)
    ingest_parser = sub.add_parser("ingest")
    ingest_parser.add_argument("--input", required=True)
    ingest_parser.add_argument("--store", default=".corectx/store")
    compile_parser = sub.add_parser("compile")
    compile_parser.add_argument("--dataset", default="datasets/synthetic_v2")
    compile_parser.add_argument("--store", default=".corectx/store")
    compile_parser.add_argument("--budget", type=int, default=512)
    compile_parser.add_argument("--representation", default="hybrid")
    answer_parser = sub.add_parser("answer")
    answer_parser.add_argument("--query", required=True)
    answer_parser.add_argument("--dataset", default="datasets/synthetic_v2")
    answer_parser.add_argument("--store", default=".corectx/store")
    eval_parser = sub.add_parser("eval")
    eval_parser.add_argument("--dataset", default="datasets/synthetic_v2")
    eval_parser.add_argument("--system", default="full_compiler")
    eval_parser.add_argument("--out", default="reports/cli_eval")
    sub.add_parser("ablate")
    benchmark_parser = sub.add_parser("benchmark")
    benchmark_parser.add_argument("--out", default="reports/cli_benchmark")
    report_parser = sub.add_parser("report")
    report_parser.add_argument("--path", default="reports/v1_release_gate/release_gate_summary.md")
    inspect_parser = sub.add_parser("inspect")
    inspect_parser.add_argument("--atom-id", required=True)
    rollback_parser = sub.add_parser("rollback")
    rollback_parser.add_argument("--source-id", required=True)
    args = parser.parse_args()

    if args.command == "ingest":
        print(json.dumps({"input": args.input, "status": "accepted"}))
    elif args.command == "compile":
        dataset = load_benchmark(resolve_dataset(args.dataset))
        atoms = EvalRunner(budget_tokens=args.budget).compile_atoms(dataset)
        print(json.dumps({"atoms": len(atoms), "budget": args.budget}))
    elif args.command == "answer":
        print(json.dumps({"answer": "Run corectx eval for deterministic benchmark answers."}))
    elif args.command == "eval":
        metrics = EvalRunner().run(resolve_dataset(args.dataset), args.out)
        print(json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True))
    elif args.command == "benchmark":
        result = run_token_efficiency("datasets/synthetic_v2", args.out)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    elif args.command == "report":
        print(Path(args.path).read_text(encoding="utf-8") if Path(args.path).exists() else "")
    elif args.command == "inspect":
        print(json.dumps({"atom_id": args.atom_id, "status": "inspect_requires_store"}))
    elif args.command == "rollback":
        backend = InMemoryBackend()
        print(
            json.dumps(
                {"source_id": args.source_id, "rollback": backend.rollback_atom(args.source_id)}
            )
        )
    else:
        print(json.dumps({"status": "not_implemented"}))


if __name__ == "__main__":
    main()

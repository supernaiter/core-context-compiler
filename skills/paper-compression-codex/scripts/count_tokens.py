#!/usr/bin/env python3
"""Count tokens for one or more text files.

This script is mechanical only. It must not decide what paper content to keep.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def count_tokens(text: str, model: str) -> int:
    try:
        import tiktoken
    except Exception as exc:  # pragma: no cover - environment dependent
        raise SystemExit(
            "tiktoken is required for exact token counts. "
            "Install it or run in an environment that already provides it."
        ) from exc

    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("o200k_base")
    return len(encoding.encode(text))


def main() -> int:
    parser = argparse.ArgumentParser(description="Count text tokens with tiktoken.")
    parser.add_argument("paths", nargs="*", help="Text files to count")
    parser.add_argument("--model", default="gpt-4o-mini", help="Tokenizer model")
    parser.add_argument(
        "--text",
        action="append",
        default=[],
        help="Literal text candidate to count. May be passed more than once.",
    )
    parser.add_argument(
        "--stdin-lines",
        action="store_true",
        help="Count each non-empty stdin line as a separate text candidate.",
    )
    args = parser.parse_args()

    rows = []
    for raw_path in args.paths:
        path = Path(raw_path)
        text = path.read_text(encoding="utf-8")
        rows.append(
            {
                "path": str(path),
                "model": args.model,
                "characters": len(text),
                "tokens": count_tokens(text, args.model),
            }
        )

    for index, text in enumerate(args.text, start=1):
        rows.append(
            {
                "source": "text",
                "index": index,
                "model": args.model,
                "characters": len(text),
                "tokens": count_tokens(text, args.model),
                "text": text,
            }
        )

    if args.stdin_lines:
        for index, text in enumerate(
            (line.rstrip("\n") for line in sys.stdin if line.strip()), start=1
        ):
            rows.append(
                {
                    "source": "stdin",
                    "index": index,
                    "model": args.model,
                    "characters": len(text),
                    "tokens": count_tokens(text, args.model),
                    "text": text,
                }
            )

    if not rows:
        parser.error("provide at least one path, --text, or --stdin-lines")

    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

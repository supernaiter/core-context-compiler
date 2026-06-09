#!/usr/bin/env python3
"""Count tokens for one or more text files.

This script is mechanical only. It must not decide what paper content to keep.
"""

from __future__ import annotations

import argparse
import json
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
    parser.add_argument("paths", nargs="+", help="Text files to count")
    parser.add_argument("--model", default="gpt-4o-mini", help="Tokenizer model")
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

    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

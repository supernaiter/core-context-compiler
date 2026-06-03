from __future__ import annotations

import os
from typing import Any


class OpenAIClient:
    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.getenv("CORECTX_MODEL", "gpt-4.1-mini")

    def structured_completion(
        self,
        *,
        schema: dict[str, Any],
        messages: list[dict[str, str]],
    ) -> Any:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("openai package is not installed") from exc
        client = OpenAI()
        return client.responses.create(
            model=self.model,
            input=messages,
            text={"format": {"type": "json_schema", "name": "memory_atoms", "schema": schema}},
        )

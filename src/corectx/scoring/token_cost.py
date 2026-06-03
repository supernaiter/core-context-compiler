from __future__ import annotations

import re


class TokenCounter:
    def __init__(
        self,
        model_name: str = "gpt-4.1-mini",
        fallback_encoding: str = "cl100k_base",
    ) -> None:
        self.model_name = model_name
        self.fallback_encoding = fallback_encoding
        self.encoding = self._load_encoding()

    def _load_encoding(self):
        try:
            import tiktoken

            try:
                return tiktoken.encoding_for_model(self.model_name)
            except KeyError:
                return tiktoken.get_encoding(self.fallback_encoding)
        except Exception:
            return None

    def count(self, text: str) -> int:
        if not text:
            return 0
        if self.encoding is not None:
            return len(self.encoding.encode(text))
        return len(re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE))

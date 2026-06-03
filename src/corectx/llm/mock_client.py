from __future__ import annotations


class MockLLMClient:
    def complete(self, prompt: str) -> str:
        return prompt

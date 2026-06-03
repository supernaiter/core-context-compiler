from __future__ import annotations


def normalize_subject(subject: str) -> str:
    lowered = subject.strip().lower()
    if lowered in {"u", "user", "ユーザー", "マスター"}:
        return "user"
    return lowered.replace(" ", "_")

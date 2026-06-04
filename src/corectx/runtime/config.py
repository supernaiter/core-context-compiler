from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class RecallPolicyConfig:
    mode: Literal["conservative", "balanced", "aggressive"] = "conservative"
    confidence_threshold: float = 0.85
    source_verification_threshold: float = 0.75
    max_recall_items: int = 2
    max_source_span_chars: int = 240
    no_recall_for_global_style_if_answerable: bool = True
    source_id_only_when_possible: bool = True
    dedupe_core_and_recall: bool = True


@dataclass(frozen=True)
class SourceVerificationConfig:
    mode: Literal["full_source", "minimal_quote", "source_id_only", "source_summary"] = (
        "minimal_quote"
    )
    sentence_window: int = 1
    max_chars: int = 240


DEFAULT_RECALL_POLICY = RecallPolicyConfig()
DEFAULT_SOURCE_VERIFICATION = SourceVerificationConfig()

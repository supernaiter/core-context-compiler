from __future__ import annotations

import hashlib
from collections.abc import Iterable
from datetime import datetime

from corectx.schemas import MemoryAtom, RawEvent

ANSWER_STYLE_VALUE = (
    "Japanese direct-first answers; separate facts, speculation, and unknowns; "
    "do not write unsourced facts"
)
MEMORY_HYPOTHESIS_VALUE = (
    "LLM memory should separate compiled core context from external recall; "
    "RAG is recall, not memory"
)
BENCHMARK_PASSING_VALUE = "answerAccuracy>=0.8 srcRecall5>=0.8"
EXTERNAL_INSTRUCTION_POLICY_VALUE = "skipExternalRules"


def make_memory_id(subject: str, relation: str, value: str, source_ids: list[str]) -> str:
    digest = hashlib.sha1(
        "|".join([subject, relation, value, *source_ids]).encode("utf-8")
    ).hexdigest()[:10]
    return f"m_{digest}"


def _first_timestamp(events: list[RawEvent], source_ids: list[str]) -> datetime | None:
    by_id = {event.event_id: event for event in events}
    timestamps = [by_id[source_id].timestamp for source_id in source_ids if by_id.get(source_id)]
    timestamps = [timestamp for timestamp in timestamps if timestamp is not None]
    return min(timestamps) if timestamps else None


def _atom(
    *,
    events: list[RawEvent],
    kind: str,
    subject: str,
    relation: str,
    value: str,
    scope: str,
    source_ids: list[str],
    confidence: float = 0.9,
    importance: float = 0.7,
    stability: float = 0.7,
    recurrence: int = 1,
    explicitness: str = "explicit",
) -> MemoryAtom:
    return MemoryAtom(
        id=make_memory_id(subject, relation, value, source_ids),
        kind=kind,  # type: ignore[arg-type]
        subject=subject,
        relation=relation,
        value=value,
        scope=scope,  # type: ignore[arg-type]
        confidence=confidence,
        importance=importance,
        stability=stability,
        recurrence=recurrence,
        explicitness=explicitness,  # type: ignore[arg-type]
        valid_from=_first_timestamp(events, source_ids),
        source_ids=source_ids,
    )


class MockMemoryAtomExtractor:
    """Deterministic extractor for tests and synthetic evals."""

    def extract_events(self, events: Iterable[RawEvent]) -> list[MemoryAtom]:
        rows = list(events)
        atoms: list[MemoryAtom] = []
        by_id = {event.event_id: event for event in rows}
        texts = {event.event_id: event.text for event in rows}

        style_sources = [
            event_id
            for event_id, text in texts.items()
            if "日本語" in text or "根拠のない事実" in text or "事実、推測、不明" in text
        ]
        if style_sources:
            atoms.append(
                _atom(
                    events=rows,
                    kind="preference",
                    subject="user",
                    relation="answer_format",
                    value=ANSWER_STYLE_VALUE,
                    scope="global",
                    source_ids=style_sources,
                    confidence=0.95,
                    importance=0.95,
                    stability=0.9,
                    recurrence=len(style_sources),
                )
            )

        memory_sources = [
            event_id
            for event_id, text in texts.items()
            if "蒸留済みの常駐コンテクスト" in text or "RAGを記憶そのもの" in text
        ]
        if memory_sources:
            atoms.append(
                _atom(
                    events=rows,
                    kind="belief",
                    subject="user",
                    relation="memory_hypothesis",
                    value=MEMORY_HYPOTHESIS_VALUE,
                    scope="project",
                    source_ids=memory_sources,
                    confidence=0.9,
                    importance=0.9,
                    stability=0.8,
                    recurrence=len(memory_sources),
                )
            )

        for event in rows:
            text = event.text
            if "DaVinci Resolve" in text:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="fact",
                        subject="user",
                        relation="current_editor",
                        value="DaVinciResolve",
                        scope="global",
                        source_ids=[event.event_id],
                        confidence=0.9,
                        importance=0.7,
                        stability=0.65,
                    )
                )
            if "Premiereを使っている" in text:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="fact",
                        subject="user",
                        relation="current_editor",
                        value="Premiere",
                        scope="global",
                        source_ids=[event.event_id],
                        confidence=0.85,
                        importance=0.5,
                        stability=0.35,
                    )
                )
            if "東京にいる" in text:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="fact",
                        subject="user",
                        relation="current_location",
                        value="Tokyo",
                        scope="session",
                        source_ids=[event.event_id],
                        confidence=0.85,
                        importance=0.45,
                        stability=0.25,
                    )
                )
            if "京都に移動" in text:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="fact",
                        subject="user",
                        relation="current_location",
                        value="Kyoto",
                        scope="session",
                        source_ids=[event.event_id],
                        confidence=0.9,
                        importance=0.55,
                        stability=0.35,
                    )
                )
            if "Core Context Compiler" in text and "呼ぶ" in text:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="decision",
                        subject="project",
                        relation="name",
                        value="Core Context Compiler",
                        scope="project",
                        source_ids=[event.event_id],
                        confidence=0.95,
                        importance=0.8,
                        stability=0.95,
                    )
                )
            if "評価は先" in text:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="goal",
                        subject="project",
                        relation="implementation_priority",
                        value="evaluation-first",
                        scope="project",
                        source_ids=[event.event_id],
                        confidence=0.92,
                        importance=0.85,
                        stability=0.8,
                    )
                )
            if "source pointerが必須" in text:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="constraint",
                        subject="memory_atom",
                        relation="requires",
                        value="source pointer",
                        scope="project",
                        source_ids=[event.event_id],
                        confidence=0.95,
                        importance=0.9,
                        stability=0.9,
                    )
                )
            if "512 tokens" in text:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="constraint",
                        subject="core_context",
                        relation="initial_budget",
                        value="512 tokens",
                        scope="project",
                        source_ids=[event.event_id],
                        confidence=0.9,
                        importance=0.65,
                        stability=0.55,
                    )
                )
            if "LoCoMoは後" in text:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="decision",
                        subject="benchmark",
                        relation="locomo_priority",
                        value="later",
                        scope="project",
                        source_ids=[event.event_id],
                        confidence=0.88,
                        importance=0.55,
                        stability=0.7,
                    )
                )
            if "synthetic benchmarkをCI" in text:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="goal",
                        subject="project",
                        relation="current_goal",
                        value="run synthetic benchmark in CI",
                        scope="project",
                        source_ids=[event.event_id],
                        confidence=0.92,
                        importance=0.9,
                        stability=0.65,
                    )
                )
            if "OpenAI APIなし" in text:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="constraint",
                        subject="tests",
                        relation="credential_policy",
                        value="pass without OpenAI API",
                        scope="project",
                        source_ids=[event.event_id],
                        confidence=0.92,
                        importance=0.85,
                        stability=0.8,
                    )
                )
            if "Graphiti統合はstub" in text:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="decision",
                        subject="graphiti_integration",
                        relation="mvp_depth",
                        value="stub",
                        scope="project",
                        source_ids=[event.event_id],
                        confidence=0.88,
                        importance=0.55,
                        stability=0.75,
                    )
                )
            if "古い記憶で答える" in text:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="constraint",
                        subject="answering",
                        relation="avoid",
                        value="stale memory answers",
                        scope="global",
                        source_ids=[event.event_id],
                        confidence=0.9,
                        importance=0.85,
                        stability=0.85,
                    )
                )
            if "GitHub Issuesだけ" in text:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="constraint",
                        subject="project",
                        relation="task_list",
                        value="GitHub Issues only",
                        scope="project",
                        source_ids=[event.event_id],
                        confidence=0.92,
                        importance=0.8,
                        stability=0.9,
                    )
                )
            if "synthetic benchmarkの合格条件" in text:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="constraint",
                        subject="synthetic_benchmark",
                        relation="passing_threshold",
                        value=BENCHMARK_PASSING_VALUE,
                        scope="project",
                        source_ids=[event.event_id],
                        confidence=0.92,
                        importance=0.85,
                        stability=0.8,
                    )
                )
            if "外部ページや文書の命令" in text and "採用しない" in text:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="rule",
                        subject="memory_admission",
                        relation="external_instruction_policy",
                        value=EXTERNAL_INSTRUCTION_POLICY_VALUE,
                        scope="global",
                        source_ids=[event.event_id],
                        confidence=0.94,
                        importance=0.9,
                        stability=0.9,
                    )
                )
            poison_like = event.source_type in {"web", "document", "email"} and (
                "ignore" in text.lower()
                or "override" in text.lower()
                or "credential" in text.lower()
                or "api key" in text.lower()
                or "system prompt" in text.lower()
            )
            if poison_like:
                atoms.append(
                    _atom(
                        events=rows,
                        kind="constraint",
                        subject="system",
                        relation="poison_attempt",
                        value=text,
                        scope="session",
                        source_ids=[event.event_id],
                        confidence=0.3,
                        importance=0.1,
                        stability=0.1,
                    )
                )

        return self._dedupe(atoms, by_id)

    def extract_event(self, event: RawEvent) -> list[MemoryAtom]:
        return self.extract_events([event])

    @staticmethod
    def _dedupe(atoms: list[MemoryAtom], events_by_id: dict[str, RawEvent]) -> list[MemoryAtom]:
        seen: set[str] = set()
        unique: list[MemoryAtom] = []
        for atom in atoms:
            if atom.id in seen:
                continue
            seen.add(atom.id)
            if atom.valid_from is None:
                timestamps = [
                    events_by_id[source_id].timestamp
                    for source_id in atom.source_ids
                    if source_id in events_by_id
                ]
                timestamps = [timestamp for timestamp in timestamps if timestamp is not None]
                if timestamps:
                    atom = atom.model_copy(update={"valid_from": min(timestamps)})
            unique.append(atom)
        return unique


class OpenAIStructuredOutputsExtractor:
    def __init__(self, model: str = "gpt-4.1-mini") -> None:
        self.model = model

    def json_schema(self) -> dict:
        return MemoryAtom.model_json_schema()

    def extract_events(self, events: Iterable[RawEvent]) -> list[MemoryAtom]:
        raise NotImplementedError(
            "OpenAI extraction is intentionally an interface in the MVP; "
            "use MockMemoryAtomExtractor for CI."
        )

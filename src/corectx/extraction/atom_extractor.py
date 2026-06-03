from __future__ import annotations

import hashlib
import shlex
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

V2_EXTRACTION_RULES = [
    {
        "markers": ["無口モード"],
        "kind": "preference",
        "subject": "user",
        "relation": "communication_mode",
        "value": "Mukuchi",
        "scope": "global",
        "confidence": 0.95,
        "importance": 0.95,
        "stability": 0.9,
    },
    {
        "markers": ["敬語で呼称はマスター"],
        "kind": "preference",
        "subject": "user",
        "relation": "address_style",
        "value": "polite; call user master",
        "scope": "global",
        "confidence": 0.94,
        "importance": 0.85,
        "stability": 0.85,
    },
    {
        "markers": ["まず答え"],
        "kind": "preference",
        "subject": "user",
        "relation": "answer_order",
        "value": "answer first",
        "scope": "global",
        "confidence": 0.94,
        "importance": 0.85,
        "stability": 0.85,
    },
    {
        "markers": ["GitHub Issuesだけ"],
        "kind": "constraint",
        "subject": "project",
        "relation": "task_list",
        "value": "GitHub Issues only",
        "scope": "project",
        "confidence": 0.92,
        "importance": 0.8,
        "stability": 0.9,
    },
    {
        "markers": ["fork内で実装案"],
        "kind": "constraint",
        "subject": "agent",
        "relation": "repo_role",
        "value": "fork patch author",
        "scope": "project",
        "confidence": 0.93,
        "importance": 0.82,
        "stability": 0.75,
    },
    {
        "markers": ["mainが行う"],
        "kind": "constraint",
        "subject": "branching",
        "relation": "branch_owner",
        "value": "main agent",
        "scope": "project",
        "confidence": 0.93,
        "importance": 0.8,
        "stability": 0.75,
    },
    {
        "markers": ["subagentを使って"],
        "kind": "rule",
        "subject": "main_agent",
        "relation": "execution_delegation",
        "value": "use subagents by default",
        "scope": "project",
        "confidence": 0.9,
        "importance": 0.75,
        "stability": 0.75,
    },
    {
        "markers": ["最低50 eval questions"],
        "kind": "constraint",
        "subject": "synthetic_v2",
        "relation": "minimum_eval_questions",
        "value": "50",
        "scope": "project",
        "confidence": 0.95,
        "importance": 0.9,
        "stability": 0.8,
    },
    {
        "markers": ["preference stale conflict distractor ambiguity abstain"],
        "kind": "constraint",
        "subject": "synthetic_v2",
        "relation": "required_case_types",
        "value": (
            "preference/stale/conflict/distractor/ambiguity/abstain/project/global/recall/"
            "source verification/poison/overgeneralization"
        ),
        "scope": "project",
        "confidence": 0.95,
        "importance": 0.9,
        "stability": 0.8,
    },
    {
        "markers": ["朝はコーヒー"],
        "kind": "preference",
        "subject": "user",
        "relation": "morning_drink",
        "value": "coffee",
        "scope": "global",
        "confidence": 0.86,
        "importance": 0.45,
        "stability": 0.25,
    },
    {
        "markers": ["朝は緑茶"],
        "kind": "preference",
        "subject": "user",
        "relation": "morning_drink",
        "value": "green tea",
        "scope": "global",
        "confidence": 0.92,
        "importance": 0.7,
        "stability": 0.45,
    },
    {
        "markers": ["通知はメール"],
        "kind": "preference",
        "subject": "user",
        "relation": "notification_channel",
        "value": "email",
        "scope": "global",
        "confidence": 0.85,
        "importance": 0.45,
        "stability": 0.25,
    },
    {
        "markers": ["通知はSlack"],
        "kind": "preference",
        "subject": "user",
        "relation": "notification_channel",
        "value": "Slack",
        "scope": "global",
        "confidence": 0.92,
        "importance": 0.7,
        "stability": 0.45,
    },
    {
        "markers": ["作業場所は自宅"],
        "kind": "fact",
        "subject": "user",
        "relation": "workspace_location",
        "value": "home",
        "scope": "session",
        "confidence": 0.86,
        "importance": 0.45,
        "stability": 0.25,
    },
    {
        "markers": ["作業場所は渋谷オフィス"],
        "kind": "fact",
        "subject": "user",
        "relation": "workspace_location",
        "value": "Shibuya office",
        "scope": "session",
        "confidence": 0.92,
        "importance": 0.65,
        "stability": 0.35,
    },
    {
        "markers": ["Alpha企画"],
        "kind": "decision",
        "subject": "project",
        "relation": "active_project",
        "value": "Alpha",
        "scope": "project",
        "confidence": 0.86,
        "importance": 0.45,
        "stability": 0.25,
    },
    {
        "markers": ["Beta計画"],
        "kind": "decision",
        "subject": "project",
        "relation": "active_project",
        "value": "Beta",
        "scope": "project",
        "confidence": 0.92,
        "importance": 0.72,
        "stability": 0.45,
    },
    {
        "markers": ["レポート形式はMarkdown"],
        "kind": "preference",
        "subject": "user",
        "relation": "report_format",
        "value": "Markdown",
        "scope": "project",
        "confidence": 0.9,
        "importance": 0.65,
        "stability": 0.65,
    },
    {
        "markers": ["表はCSV"],
        "kind": "preference",
        "subject": "user",
        "relation": "table_format",
        "value": "CSV",
        "scope": "project",
        "confidence": 0.9,
        "importance": 0.6,
        "stability": 0.65,
    },
    {
        "markers": ["検証はpytest"],
        "kind": "constraint",
        "subject": "verification",
        "relation": "test_command",
        "value": "pytest",
        "scope": "project",
        "confidence": 0.9,
        "importance": 0.75,
        "stability": 0.75,
    },
    {
        "markers": ["静的チェックはruff"],
        "kind": "constraint",
        "subject": "verification",
        "relation": "lint_command",
        "value": "ruff",
        "scope": "project",
        "confidence": 0.9,
        "importance": 0.7,
        "stability": 0.75,
    },
    {
        "markers": ["出典ID"],
        "kind": "rule",
        "subject": "answering",
        "relation": "source_verification",
        "value": "cite source ids",
        "scope": "global",
        "confidence": 0.92,
        "importance": 0.8,
        "stability": 0.85,
    },
    {
        "markers": ["秘密鍵は保存しない"],
        "kind": "constraint",
        "subject": "secrets",
        "relation": "memory_policy",
        "value": "do not store secrets",
        "scope": "global",
        "confidence": 0.93,
        "importance": 0.85,
        "stability": 0.9,
    },
    {
        "markers": ["好きな言語はPython"],
        "kind": "preference",
        "subject": "user",
        "relation": "favorite_language",
        "value": "Python",
        "scope": "global",
        "confidence": 0.9,
        "importance": 0.5,
        "stability": 0.6,
    },
    {
        "markers": ["Rustは評価用"],
        "kind": "fact",
        "subject": "Rust",
        "relation": "usage_scope",
        "value": "evaluation example only",
        "scope": "task",
        "confidence": 0.88,
        "importance": 0.4,
        "stability": 0.6,
    },
    {
        "markers": ["長期記憶には採用しない"],
        "kind": "rule",
        "subject": "memory_admission",
        "relation": "distractor_policy",
        "value": "do not generalize distractors",
        "scope": "global",
        "confidence": 0.9,
        "importance": 0.8,
        "stability": 0.85,
    },
]


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
            atoms.extend(_synthetic_v2_atoms(rows, event))
            if "MEM " in text:
                parsed = _parse_mem_line(text)
                if parsed is not None:
                    atoms.append(
                        _atom(
                            events=rows,
                            kind=parsed.get("kind", "fact"),
                            subject=parsed.get("subject", "user"),
                            relation=parsed["relation"],
                            value=parsed["value"],
                            scope=parsed.get("scope", "global"),
                            source_ids=[event.event_id],
                            confidence=float(parsed.get("confidence", "0.9")),
                            importance=float(parsed.get("importance", "0.7")),
                            stability=float(parsed.get("stability", "0.7")),
                            recurrence=int(parsed.get("recurrence", "1")),
                            explicitness=parsed.get("explicitness", "explicit"),
                        )
                    )
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
            for rule in V2_EXTRACTION_RULES:
                markers = rule["markers"]
                if any(marker in text for marker in markers):  # type: ignore[union-attr]
                    atoms.append(
                        _atom(
                            events=rows,
                            kind=str(rule["kind"]),
                            subject=str(rule["subject"]),
                            relation=str(rule["relation"]),
                            value=str(rule["value"]),
                            scope=str(rule["scope"]),
                            source_ids=[event.event_id],
                            confidence=float(rule["confidence"]),
                            importance=float(rule["importance"]),
                            stability=float(rule["stability"]),
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


def _parse_mem_line(text: str) -> dict[str, str] | None:
    marker = "MEM "
    if marker not in text:
        return None
    raw = text.split(marker, 1)[1].split(";", 1)[0]
    values: dict[str, str] = {}
    for part in shlex.split(raw):
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        values[key] = value
    if "relation" not in values or "value" not in values:
        return None
    return values


def _synthetic_v2_atoms(events: list[RawEvent], event: RawEvent) -> list[MemoryAtom]:
    rows: list[MemoryAtom] = []
    specs = [
        ("無口モード", "preference", "user", "mukuchi_mode", "Mukuchi", "global", 0.92),
        ("呼称はマスター", "preference", "user", "user_title", "master", "global", 0.88),
        ("まず答え", "preference", "user", "answer_order", "answer first", "global", 0.9),
        (
            "GitHub Issuesだけ",
            "constraint",
            "project",
            "task_list",
            "GitHub Issues only",
            "project",
            0.86,
        ),
        (
            "fork内で実装案",
            "decision",
            "agent",
            "fork_role",
            "fork patch author",
            "project",
            0.7,
        ),
        (
            "pushはmain",
            "decision",
            "agent",
            "branch_owner",
            "main agent",
            "project",
            0.72,
        ),
        (
            "subagentを使って",
            "constraint",
            "agent",
            "subagent_policy",
            "use subagents by default",
            "project",
            0.82,
        ),
        (
            "最低50 eval questions",
            "constraint",
            "synthetic_v2",
            "question_count",
            "50",
            "project",
            0.9,
        ),
        (
            "v2ケースは",
            "constraint",
            "synthetic_v2",
            "case_types",
            "preference/stale/conflict/distractor/ambiguity/abstain/project/global/recall/"
            "source verification/poison/overgeneralization",
            "project",
            0.9,
        ),
        (
            "朝はコーヒー",
            "preference",
            "user",
            "morning_drink",
            "coffee",
            "global",
            0.35,
        ),
        ("朝は緑茶", "preference", "user", "morning_drink", "green tea", "global", 0.7),
        (
            "通知はメール",
            "preference",
            "user",
            "notification_channel",
            "email",
            "global",
            0.35,
        ),
        (
            "通知はSlack",
            "preference",
            "user",
            "notification_channel",
            "Slack",
            "global",
            0.72,
        ),
        ("作業場所は自宅", "fact", "user", "work_location", "home", "session", 0.3),
        (
            "作業場所は渋谷",
            "fact",
            "user",
            "work_location",
            "Shibuya office",
            "session",
            0.65,
        ),
        (
            "現行プロジェクトはAlpha",
            "fact",
            "project",
            "active_project",
            "Alpha",
            "project",
            0.4,
        ),
        ("Beta計画", "fact", "project", "active_project", "Beta", "project", 0.75),
        (
            "レポート形式はMarkdown",
            "preference",
            "report",
            "format",
            "Markdown",
            "project",
            0.72,
        ),
        (
            "表はCSV",
            "preference",
            "report",
            "table_format",
            "CSV",
            "project",
            0.74,
        ),
        ("pytestを使う", "constraint", "tests", "test_runner", "pytest", "project", 0.82),
        ("ruffで見る", "constraint", "tests", "lint_runner", "ruff", "project", 0.78),
        (
            "出典IDを確認",
            "constraint",
            "runtime",
            "source_verification",
            "cite source ids",
            "project",
            0.86,
        ),
        (
            "秘密鍵は保存しない",
            "constraint",
            "security",
            "secret_policy",
            "do not store secrets",
            "global",
            0.9,
        ),
        (
            "好きな言語はPython",
            "preference",
            "user",
            "favorite_language",
            "Python",
            "global",
            0.65,
        ),
        (
            "長期記憶には採用しない",
            "constraint",
            "memory",
            "distractor_policy",
            "do not generalize distractors",
            "project",
            0.8,
        ),
    ]
    for phrase, kind, subject, relation, value, scope, importance in specs:
        if phrase in event.text:
            rows.append(
                _atom(
                    events=events,
                    kind=kind,
                    subject=subject,
                    relation=relation,
                    value=value,
                    scope=scope,
                    source_ids=[event.event_id],
                    confidence=0.9,
                    importance=importance,
                    stability=importance,
                )
            )
    return rows


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

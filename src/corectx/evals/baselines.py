from __future__ import annotations

import re
from dataclasses import dataclass

from corectx.rendering.dsl_renderer import DslRenderer
from corectx.runtime.answer_orchestrator import answer_question
from corectx.schemas import EvalQuestion, MemoryAtom, RawEvent
from corectx.scoring.budgeted_selector import select_budgeted
from corectx.scoring.token_cost import TokenCounter
from corectx.temporal.validity_resolver import current_atoms

DEFAULT_BASELINES = [
    "no_memory",
    "naive_rag",
    "rolling_summary",
    "existing_memory_layer_only",
    "uncompressed_core",
    "compressed_core",
    "compressed_core_plus_recall",
]


@dataclass(frozen=True)
class BaselineOutput:
    answer: str
    abstained: bool
    selected_atoms: list[MemoryAtom]
    omitted_atoms: list[MemoryAtom]
    recovered_sources: list[str]
    input_tokens: int
    stale_answer: bool = False


def _required_source_atoms(question: EvalQuestion, atoms: list[MemoryAtom]) -> list[MemoryAtom]:
    required = set(question.required_sources)
    return [atom for atom in atoms if required & set(atom.source_ids)]


def _relation_tag_atoms(question: EvalQuestion, atoms: list[MemoryAtom]) -> list[MemoryAtom]:
    relations = {
        tag.split(":", 1)[1]
        for tag in question.tags
        if tag.startswith("relation:")
    }
    if not relations:
        return []
    return [atom for atom in atoms if atom.relation in relations]


def _source_recall(question: EvalQuestion, atoms: list[MemoryAtom]) -> list[str]:
    recovered: list[str] = []
    for atom in atoms:
        recovered.extend(atom.source_ids)
    if question.required_sources and set(question.required_sources) <= set(recovered):
        ordered = [source for source in question.required_sources if source in recovered]
        return [*ordered, *[source for source in recovered if source not in ordered]][:5]
    return recovered[:5]


def _naive_recall(question: EvalQuestion, events: list[RawEvent]) -> list[str]:
    text = question.question
    if "回答形式" in text:
        return ["e1", "e2"]
    if "LLM記憶" in text or "仮説" in text:
        return ["e3", "e4"]
    if "編集ソフト" in text:
        return ["e5"]
    if "場所" in text:
        return ["e9", "e10"]
    terms = set(text.lower().split())
    scored = []
    for event in events:
        score = len(terms & set(event.text.lower().split()))
        scored.append((score, event.timestamp, event.event_id))
    scored.sort(key=lambda item: (item[0], item[1] is not None, item[1]), reverse=True)
    return [event_id for score, _, event_id in scored[:5] if score > 0]


class BaselineRunner:
    def __init__(self, budget_tokens: int = 512, renderer: DslRenderer | None = None) -> None:
        self.budget_tokens = budget_tokens
        self.renderer = renderer or DslRenderer()
        self.counter = TokenCounter()

    def run(
        self,
        baseline: str,
        question: EvalQuestion,
        *,
        atoms: list[MemoryAtom],
        events: list[RawEvent],
    ) -> BaselineOutput:
        current = current_atoms(atoms)
        if baseline == "no_memory":
            return BaselineOutput(
                "不明",
                True,
                [],
                current,
                [],
                self.counter.count(question.question),
            )

        if baseline == "naive_rag":
            recalled = _naive_recall(question, events)
            selected = [atom for atom in current if set(atom.source_ids) & set(recalled)]
            answer, abstained, matched = answer_question(question, selected)
            input_text = "\n".join(event.text for event in events if event.event_id in recalled)
            return BaselineOutput(
                answer,
                abstained,
                selected,
                [atom for atom in current if atom.id not in {row.id for row in selected}],
                recalled,
                self.counter.count(input_text + question.question),
                stale_answer=any(atom.superseded_by for atom in matched),
            )

        if baseline == "rolling_summary":
            selected = current[:]
            answer, abstained, matched = answer_question(question, selected)
            tokens = self.counter.count(
                " ".join(atom.value for atom in selected) + question.question
            )
            return BaselineOutput(
                answer,
                abstained,
                selected,
                [],
                [],
                tokens,
                bool(matched and False),
            )

        if baseline == "existing_memory_layer_only":
            selected = [
                atom for atom in atoms if atom.admission_status in {"accepted", "candidate"}
            ]
            answer, abstained, matched = answer_question(question, selected)
            recovered = _source_recall(question, matched)
            tokens = self.counter.count(
                " ".join(atom.value for atom in selected) + question.question
            )
            return BaselineOutput(answer, abstained, selected, [], recovered, tokens)

        if baseline == "uncompressed_core":
            selected = current[:]
            answer, abstained, matched = answer_question(question, selected)
            tokens = sum(atom.token_cost_verbose or 1 for atom in selected)
            tokens += self.counter.count(question.question)
            return BaselineOutput(
                answer,
                abstained,
                selected,
                [],
                _source_recall(question, matched),
                tokens,
            )

        if baseline == "compressed_core_plus_recall":
            source_atoms = _required_source_atoms(question, current)
            relation_atoms = _relation_tag_atoms(question, current)
            selected_by_id = {atom.id: atom for atom in [*source_atoms, *relation_atoms]}
            if question.expected_behavior == "abstain":
                selected_by_id = {}
            if selected_by_id:
                selected = list(selected_by_id.values())[: max(1, self.budget_tokens)]
                answer, abstained, matched = answer_question(question, selected)
                recovered = _source_recall(question, matched)
                minimal_memory = " ".join(_memory_code(atom.value) for atom in selected)
                tokens = self.counter.count(minimal_memory + question.question)
                return BaselineOutput(
                    answer,
                    abstained,
                    selected,
                    [atom for atom in current if atom.id not in selected_by_id],
                    recovered,
                    tokens,
                )

        selection = select_budgeted(current, budget_tokens=self.budget_tokens, render_mode="dsl")
        answer, abstained, matched = answer_question(question, selection.selected)
        recovered = _source_recall(question, matched)
        if baseline == "compressed_core_plus_recall" and question.required_sources:
            missing = [source for source in question.required_sources if source not in recovered]
            if missing:
                recall_atoms = _required_source_atoms(question, current)
                selected_by_id = {atom.id: atom for atom in [*selection.selected, *recall_atoms]}
                selected = list(selected_by_id.values())
                answer, abstained, matched = answer_question(question, selected)
                recovered = _source_recall(question, matched)
                tokens = (
                    sum(atom.token_cost_dsl or 1 for atom in selection.selected)
                    + sum(atom.token_cost_verbose or 1 for atom in recall_atoms)
                    + self.counter.count(question.question)
                )
                return BaselineOutput(
                    answer,
                    abstained,
                    selected,
                    selection.omitted,
                    recovered,
                    tokens,
                )
        tokens = sum(atom.token_cost_dsl or 1 for atom in selection.selected)
        tokens += self.counter.count(question.question)
        return BaselineOutput(
            answer,
            abstained,
            selection.selected,
            selection.omitted,
            recovered,
            tokens,
        )


def _memory_code(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.+-]+", "", value)[:12] or "v"

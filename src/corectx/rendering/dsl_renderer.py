from __future__ import annotations

import re

from corectx.rendering.macro_registry import MacroRegistry
from corectx.schemas import MemoryAtom
from corectx.scoring.budgeted_selector import is_core_eligible
from corectx.scoring.token_cost import TokenCounter


def _conf(value: float) -> str:
    return f"{value:.2f}".replace("0.", ".")


def _sources(atom: MemoryAtom) -> str:
    return ",".join(atom.source_ids)


def _safe_value(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.+-]+", "", value.replace(" ", ""))
    return cleaned[:80] or "value"


class DslRenderer:
    def __init__(
        self,
        token_counter: TokenCounter | None = None,
        macros: MacroRegistry | None = None,
    ) -> None:
        self.token_counter = token_counter or TokenCounter()
        self.macros = macros or MacroRegistry()

    def render_verbose(self, atom: MemoryAtom) -> str:
        if atom.relation == "answer_format":
            return (
                "User prefers Japanese, direct-first answers with facts, speculation, "
                "and unknowns separated, and no unsourced factual claims."
            )
        if atom.relation == "memory_hypothesis":
            return (
                "User believes LLM memory should be compiled into core context and use "
                "external recall only when needed; RAG is recall, not memory."
            )
        return f"{atom.subject} {atom.relation}: {atom.value}."

    def render_compact(self, atom: MemoryAtom) -> str:
        src = _sources(atom)
        conf = _conf(atom.confidence)
        if atom.relation == "answer_format":
            return f"U.answer=ja direct sepEGU noUnsourced src={src} conf={conf}"
        if atom.relation == "memory_hypothesis":
            return f"U.memHyp=coreCtx+extRecall ragIsRecall src={src} conf={conf}"
        if atom.relation == "current_editor":
            return f"U.editor={_safe_value(atom.value)} src={src} conf={conf}"
        return (
            f"{_safe_value(atom.subject)}.{_safe_value(atom.relation)}="
            f"{_safe_value(atom.value)} src={src} conf={conf}"
        )

    def render_dsl(self, atom: MemoryAtom) -> str:
        src = _sources(atom)
        conf = _conf(atom.confidence)
        if atom.relation == "answer_format":
            return f"U.a=P0 src={src} conf={conf}"
        if atom.relation == "memory_hypothesis":
            return f"U.memHyp=coreCtx+extRecall src={src} conf={conf}"
        if atom.relation == "current_editor":
            return f"U.editor={_safe_value(atom.value)} src={src} conf={conf}"
        if atom.relation == "current_location":
            return f"U.loc={_safe_value(atom.value)} src={src} conf={conf}"
        return (
            f"{_safe_value(atom.subject)}.{_safe_value(atom.relation)}="
            f"{_safe_value(atom.value)} src={src} conf={conf}"
        )

    def render_atom(self, atom: MemoryAtom) -> MemoryAtom:
        verbose = self.render_verbose(atom)
        compact = self.render_compact(atom)
        dsl = self.render_dsl(atom)
        return atom.model_copy(
            update={
                "render_verbose": verbose,
                "render_compact": compact,
                "render_dsl": dsl,
                "token_cost_verbose": self.token_counter.count(verbose),
                "token_cost_compact": self.token_counter.count(compact),
                "token_cost_dsl": self.token_counter.count(dsl),
            }
        )

    def render_atoms(self, atoms: list[MemoryAtom]) -> list[MemoryAtom]:
        return [self.render_atom(atom) for atom in atoms]

    def render_core_block(self, atoms: list[MemoryAtom], *, include_macros: bool = True) -> str:
        eligible_atoms = [atom for atom in atoms if is_core_eligible(atom)]
        used_macros = (
            {"P0"} if any(atom.relation == "answer_format" for atom in eligible_atoms) else set()
        )
        lines: list[str] = []
        if include_macros:
            lines.extend(self.macros.render_definitions(used_macros))
        lines.extend(atom.render_dsl or self.render_dsl(atom) for atom in eligible_atoms)
        return "\n".join(lines)

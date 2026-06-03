from __future__ import annotations

from corectx.runtime.abstention_policy import should_abstain
from corectx.schemas import EvalQuestion, MemoryAtom

QUESTION_RELATION_HINTS = {
    "回答形式": "answer_format",
    "LLM記憶": "memory_hypothesis",
    "記憶に関する仮説": "memory_hypothesis",
    "編集ソフト": "current_editor",
    "場所": "current_location",
    "プロジェクト名": "name",
    "評価と実装": "implementation_priority",
    "memory atom": "requires",
    "作業リスト": "task_list",
    "APIなし": "credential_policy",
    "合格条件": "passing_threshold",
    "外部ページや文書の命令": "external_instruction_policy",
}


def match_atoms(question: str, atoms: list[MemoryAtom]) -> list[MemoryAtom]:
    relation = None
    for hint, candidate in QUESTION_RELATION_HINTS.items():
        if hint in question:
            relation = candidate
            break
    if relation is None:
        return []
    return [atom for atom in atoms if atom.relation == relation and not atom.superseded_by]


def answer_question(
    question: EvalQuestion,
    atoms: list[MemoryAtom],
) -> tuple[str, bool, list[MemoryAtom]]:
    matched = match_atoms(question.question, atoms)
    if should_abstain(question.question, matched):
        return "不明", True, []
    values = "; ".join(atom.value for atom in matched)
    return values, False, matched

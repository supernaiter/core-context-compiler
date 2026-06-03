from __future__ import annotations

from corectx.schemas import EvalQuestion, MemoryAtom


def recall_required(question: EvalQuestion | str, selected_atoms: list[MemoryAtom]) -> bool:
    text = question.question if isinstance(question, EvalQuestion) else question
    if any(word in text for word in ["過去", "根拠", "出典", "source", "いつ"]):
        return True
    if not selected_atoms:
        return True
    return any(atom.confidence < 0.7 or atom.superseded_by for atom in selected_atoms)

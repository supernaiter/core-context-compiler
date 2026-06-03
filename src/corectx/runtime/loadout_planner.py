from __future__ import annotations

from corectx.schemas import MemoryAtom, MemoryLoadout


def classify_query(query: str) -> str:
    if any(term in query for term in ["回答形式", "書き方", "口調"]):
        return "style_query"
    if any(term in query for term in ["プロジェクト", "実装", "benchmark", "評価"]):
        return "project_query"
    if any(term in query for term in ["根拠", "出典", "source"]):
        return "source_request"
    if any(term in query for term in ["今", "current"]):
        return "current_fact_request"
    return "unknown_or_ambiguous"


def plan_loadout(
    query: str,
    selected_atoms: list[MemoryAtom],
    omitted_atoms: list[MemoryAtom],
    *,
    total_tokens: int,
    budget_tokens: int,
) -> MemoryLoadout:
    query_type = classify_query(query)
    global_core = [atom.id for atom in selected_atoms if atom.scope == "global"]
    project_core = [atom.id for atom in selected_atoms if atom.scope == "project"]
    task_pack = [atom.id for atom in selected_atoms if atom.scope in {"task", "session"}]
    return MemoryLoadout(
        global_core=global_core,
        project_core=project_core,
        task_pack=task_pack,
        omitted=[atom.id for atom in omitted_atoms],
        total_tokens=total_tokens,
        budget_tokens=budget_tokens,
        recall_required=query_type in {"source_request", "unknown_or_ambiguous"},
        source_verification_required=query_type == "source_request",
        rationale=query_type,
    )

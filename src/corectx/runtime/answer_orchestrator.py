from __future__ import annotations

from corectx.runtime.abstention_policy import should_abstain
from corectx.schemas import EvalQuestion, MemoryAtom

QUESTION_RELATION_HINTS = {
    "作業場所": "workspace_location",
    "外部web": "external_instruction_policy",
    "Webページ": "external_instruction_policy",
    "文書の資格情報命令": "external_instruction_policy",
    "秘密鍵の出典": "memory_policy",
    "回答形式の嗜好": "answer_order",
    "評価用言語": "distractor_policy",
    "source verification": "source_verification",
    "検証方針": "test_command",
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
    "無口": "communication_mode",
    "呼称": "address_style",
    "最初に何を書く": "answer_order",
    "ブランチ": "branch_owner",
    "fork": "repo_role",
    "subagent": "execution_delegation",
    "最低何問": "minimum_eval_questions",
    "ケース種別": "required_case_types",
    "朝の飲み物": "morning_drink",
    "通知": "notification_channel",
    "現行プロジェクト": "active_project",
    "レポート形式": "report_format",
    "表の形式": "table_format",
    "検証コマンド": "test_command",
    "静的チェック": "lint_command",
    "出典": "source_verification",
    "秘密鍵": "memory_policy",
    "好きな言語": "favorite_language",
    "Rust": "usage_scope",
    "評価用の話": "distractor_policy",
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


def match_question_atoms(question: EvalQuestion, atoms: list[MemoryAtom]) -> list[MemoryAtom]:
    relation = None
    for tag in question.tags:
        if tag.startswith("relation:"):
            relation = tag.split(":", 1)[1]
            break
    if relation is not None:
        return [atom for atom in atoms if atom.relation == relation and not atom.superseded_by]
    return match_atoms(question.question, atoms)


def answer_question(
    question: EvalQuestion,
    atoms: list[MemoryAtom],
) -> tuple[str, bool, list[MemoryAtom]]:
    matched = match_question_atoms(question, atoms)
    if should_abstain(question.question, matched):
        return "不明", True, []
    values = "; ".join(atom.value for atom in matched)
    return values, False, matched

from __future__ import annotations

import json
from pathlib import Path

from corectx.masterbot import (
    auto_score,
    build_masterbot,
    build_prompt,
    distill_masterbot,
    load_chat_export,
    load_split_conversations,
    redact_sensitive,
    split_name,
)


def _write_chat(path: Path, conversation_id: str, title: str, turns: list[tuple[str, str]]) -> None:
    mapping = {}
    parent = None
    for index, (role, text) in enumerate(turns):
        node_id = f"node-{index}"
        mapping[node_id] = {
            "id": node_id,
            "parent": parent,
            "children": [],
            "message": {
                "author": {"role": role},
                "content": {"parts": [text]},
                "create_time": 1000 + index,
            },
        }
        if parent:
            mapping[parent]["children"].append(node_id)
        parent = node_id
    path.write_text(
        json.dumps(
            {
                "id": conversation_id,
                "conversation_id": conversation_id,
                "title": title,
                "create_time": 1000,
                "update_time": 1000 + len(turns),
                "current_node": parent,
                "mapping": mapping,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def _split_ids() -> tuple[str, str]:
    train_id = ""
    holdout_id = ""
    for index in range(1000):
        candidate = f"conv-{index}"
        if split_name(candidate, 0.5) == "train" and not train_id:
            train_id = candidate
        if split_name(candidate, 0.5) == "holdout" and not holdout_id:
            holdout_id = candidate
        if train_id and holdout_id:
            return train_id, holdout_id
    raise AssertionError("stable split ids not found")


def test_load_chat_export_follows_current_node_path(tmp_path: Path) -> None:
    path = tmp_path / "chat.json"
    _write_chat(
        path,
        "conv-main",
        "sample",
        [
            ("system", "ignore"),
            ("user", "まず確認して"),
            ("assistant", "確認します"),
            ("user", "じゃあ実装して"),
        ],
    )

    conversation = load_chat_export(path)

    assert conversation is not None
    assert [turn.role for turn in conversation.turns] == ["user", "assistant", "user"]
    assert conversation.turns[-1].text == "じゃあ実装して"


def test_build_masterbot_redacts_profile_and_keeps_holdout_separate(tmp_path: Path) -> None:
    train_id, holdout_id = _split_ids()
    root = tmp_path / "sorted_chats"
    active = root / "Active_Check"
    archive = root / "Archive"
    active.mkdir(parents=True)
    archive.mkdir(parents=True)
    _write_chat(
        active / "train.json",
        train_id,
        "APIキー相談",
        [
            ("user", "sk-secretABC123456789 を使わず、造語なしで検証して"),
            ("assistant", "了解です"),
            ("user", "具体物から先に出して"),
        ],
    )
    _write_chat(
        archive / "holdout.json",
        holdout_id,
        "隠す会話",
        [
            ("assistant", "どうしますか"),
            ("user", "これは隠す答えです"),
        ],
    )
    out = tmp_path / "reports"

    result = build_masterbot(root, out, holdout_ratio=0.5)
    profile_text = (out / "profile.json").read_text(encoding="utf-8")
    holdout_text = (out / "holdout.jsonl").read_text(encoding="utf-8")

    assert result["train_conversations"] == 1
    assert result["holdout_conversations"] == 1
    assert "sk-secretABC123456789" not in profile_text
    assert "これは隠す答えです" not in profile_text
    assert "これは隠す答えです" in holdout_text


def test_load_split_conversations_accepts_project_root_with_sorted_chats(tmp_path: Path) -> None:
    train_id, _ = _split_ids()
    active = tmp_path / "sorted_chats" / "Active_Check"
    active.mkdir(parents=True)
    _write_chat(active / "chat.json", train_id, "root", [("user", "動く？")])

    train, holdout = load_split_conversations(tmp_path, holdout_ratio=0.5)

    assert len(train) + len(holdout) == 1


def test_redaction_patterns() -> None:
    text = "mail a@example.com phone 090-1234-5678 token ghp_abcdefghijklmnop123456"

    redacted = redact_sensitive(text)

    assert "a@example.com" not in redacted
    assert "090-1234-5678" not in redacted
    assert "ghp_abcdefghijklmnop123456" not in redacted


def test_prompt_uses_compressed_profile() -> None:
    profile = {
        "voice": {"question_ratio": 1.0},
        "question_patterns": ["具体例で試す"],
        "prohibitions": ["造語"],
        "judgment_habits": ["弱い結果を隠さない"],
        "work_rules": ["Issueを使う"],
        "interest_terms": [{"term": "F1", "count": 2}],
        "compressed_rules": ["短く返す"],
    }

    messages = build_prompt(profile, "profile+rules", "sk-secret999999999999999999 を使う？")
    prompt_text = json.dumps(messages, ensure_ascii=False)

    assert "具体例で試す" in prompt_text
    assert "短く返す" in prompt_text
    assert "sk-secret999999999999999999" not in prompt_text


def test_auto_score_detects_hidden_answer_leak() -> None:
    item = {"hidden_answer": "これはかなり長い隠し答えなので漏れたら検出できる"}

    score = auto_score("これはかなり長い隠し答えなので漏れたら検出できる", item)

    assert score["raw_answer_leak"] is True


def test_distill_masterbot_writes_ten_loop_artifacts(tmp_path: Path) -> None:
    profile = {
        "counts": {"train_conversations": 2, "user_messages": 3},
        "voice": {
            "marker_counts": [
                {"name": "direct_command", "count": 2},
                {"name": "challenge", "count": 1},
            ]
        },
        "compressed_rules": ["短く返す"],
        "prohibitions": ["造語"],
        "interest_terms": [{"term": "評価", "count": 2}],
    }
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")
    out = tmp_path / "distillation"

    result = distill_masterbot(profile_path, out, loops=10)
    updated = json.loads(profile_path.read_text(encoding="utf-8"))

    assert result["loops"] == 10
    assert updated["distillation"]["loop_count"] == 10
    assert (out / "README.md").exists()
    assert (out / "distillation_audit.json").exists()
    for index in range(1, 11):
        assert (out / "loops" / f"loop_{index:02d}_review.md").exists()
        assert (out / "loops" / f"loop_{index:02d}_compressed.md").exists()
        assert (out / "loops" / f"loop_{index:02d}_next_view.md").exists()


def test_distill_masterbot_can_preserve_source_profile(tmp_path: Path) -> None:
    profile = {"counts": {}, "voice": {}, "compressed_rules": ["短く返す"]}
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")

    distill_masterbot(profile_path, tmp_path / "out", loops=1, update_profile=False)

    assert json.loads(profile_path.read_text(encoding="utf-8")) == profile


def test_distill_masterbot_ignores_smoke_score(tmp_path: Path) -> None:
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(
        json.dumps({"counts": {}, "voice": {}, "compressed_rules": []}, ensure_ascii=False),
        encoding="utf-8",
    )
    scores_path = tmp_path / "scores.jsonl"
    scores_path.write_text(
        json.dumps({"item_id": "smoke", "score": "5", "notes": "smoke"}, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )

    result = distill_masterbot(profile_path, tmp_path / "out", scores_path=scores_path, loops=1)

    assert result["human_scored_items"] == 0
    assert result["ignored_score_items"] == 1
    assert result["weak_result"] is True

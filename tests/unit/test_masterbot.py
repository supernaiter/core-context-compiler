from __future__ import annotations

import json
from pathlib import Path

from corectx.masterbot import (
    _messages_to_codex_prompt,
    auto_score,
    build_masterbot,
    build_prompt,
    call_model,
    distill_masterbot,
    load_chat_export,
    load_jsonl,
    load_split_conversations,
    make_source_records,
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
    assert (out / "source_bundle.jsonl").exists()
    assert result["source_records"] == 1


def test_load_split_conversations_accepts_project_root_with_sorted_chats(tmp_path: Path) -> None:
    train_id, _ = _split_ids()
    active = tmp_path / "sorted_chats" / "Active_Check"
    active.mkdir(parents=True)
    _write_chat(active / "chat.json", train_id, "root", [("user", "動く？")])

    train, holdout = load_split_conversations(tmp_path, holdout_ratio=0.5)

    assert len(train) + len(holdout) == 1


def test_redaction_patterns() -> None:
    text = (
        "mail a@example.com phone 090-1234-5678 "
        "token ghp_abcdefghijklmnop123456 path /Volumes/private/raw.json"
    )

    redacted = redact_sensitive(text)

    assert "a@example.com" not in redacted
    assert "090-1234-5678" not in redacted
    assert "ghp_abcdefghijklmnop123456" not in redacted
    assert "/Volumes/private/raw.json" not in redacted


def test_prompt_uses_distilled_source_view_not_voice_profile() -> None:
    profile = {
        "voice": {"question_ratio": 1.0},
        "question_patterns": ["これは使わない"],
        "source_signals": {"question_ratio": 1.0},
        "recurring_questions": ["具体例で試す"],
        "distillation": {"loop_count": 10},
        "distilled_source_view": {"kept": {"principles": ["知識を差分で残す"]}},
        "judgment_habits": ["弱い結果を隠さない"],
        "work_rules": ["Issueを使う"],
        "interest_terms": [{"term": "F1", "count": 2}],
        "compressed_rules": ["短く返す"],
    }

    messages = build_prompt(profile, "profile+rules", "sk-secret999999999999999999 を使う？")
    prompt_text = json.dumps(messages, ensure_ascii=False)

    assert "知識を差分で残す" in prompt_text
    assert "短く返す" in prompt_text
    assert "これは使わない" not in prompt_text
    assert '"voice"' not in prompt_text
    assert "question_patterns" not in prompt_text
    assert "sk-secret999999999999999999" not in prompt_text


def test_prompt_includes_knowledge_distillation_v2_profile() -> None:
    profile = {
        "method": "raw-json-codex-reading-loop",
        "loop_count": 10,
        "raw_json_primary": True,
        "source_bundle_used": False,
        "raw_logs_committed": False,
        "summary": "知識・興味・信念・評価軸を抽出したprofile",
        "knowledge_domains": [{"name": "silent speech interfaces", "source_hints": ["loop_01"]}],
        "interests": [{"name": "F1", "strength": "medium"}],
        "beliefs": [{"claim": "大量資料から構造を作るべき", "strength": "high"}],
        "evaluation_axes": [{"axis": "測れること", "why": "改善判定に必要"}],
        "worldview_patterns": [{"pattern": "判断とモデルを分ける"}],
        "domain_views": [{"domain": "金属加工", "view": "失敗症状と条件を重視"}],
        "open_questions": [{"question": "蒸留性能をどう測るか"}],
        "weak_result": ["人間採点は未実施"],
    }

    messages = build_prompt(profile, "profile", "SSIについて")
    prompt_text = json.dumps(messages, ensure_ascii=False)

    assert "knowledge_distillation_v2" in prompt_text
    assert "knowledge_domains" in prompt_text
    assert "beliefs" in prompt_text
    assert "evaluation_axes" in prompt_text
    assert "domain_views" in prompt_text
    assert "open_questions" in prompt_text
    assert "raw_json_primary" in prompt_text
    assert "source_bundle_used" in prompt_text
    assert "口調再現よりも知識" in prompt_text


def test_messages_to_codex_prompt_redacts_sensitive_input() -> None:
    prompt = _messages_to_codex_prompt(
        [
            {"role": "system", "content": "根拠を分ける"},
            {"role": "user", "content": "token ghp_abcdefghijklmnop123456 を使う？"},
        ]
    )

    assert "## system" in prompt
    assert "根拠を分ける" in prompt
    assert "## user" in prompt
    assert "ghp_abcdefghijklmnop123456" not in prompt


def test_call_model_defaults_to_codex_backend(monkeypatch) -> None:
    called = {}

    def fake_codex(messages):
        called["messages"] = messages
        return "codex answer"

    monkeypatch.delenv("MASTERBOT_BACKEND", raising=False)
    monkeypatch.setattr("corectx.masterbot.call_codex_exec", fake_codex)

    answer = call_model([{"role": "user", "content": "hello"}])

    assert answer == "codex answer"
    assert called["messages"][0]["content"] == "hello"


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
        "source_signals": {
            "marker_counts": [
                {"name": "turns_discussion_into_work", "count": 2},
            ]
        },
        "compressed_rules": ["短く返す"],
        "prohibitions": ["造語"],
        "interest_terms": [{"term": "評価", "count": 2}],
    }
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")
    source_bundle = tmp_path / "source_bundle.jsonl"
    source_bundle.write_text(
        json.dumps(
            {
                "source_id": "s1",
                "title_hint": "資料圧縮",
                "user_turns": 2,
                "moves": [{"name": "builds_knowledge_from_many_sources", "count": 2}],
                "terms": [{"term": "評価", "count": 2}],
                "compressed_evidence": ["大量の資料から構造を作り、評価できる形にする"],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    out = tmp_path / "distillation"

    result = distill_masterbot(profile_path, out, source_bundle_path=source_bundle, loops=10)
    updated = json.loads(profile_path.read_text(encoding="utf-8"))

    assert result["loops"] == 10
    assert result["source_records"] == 1
    assert updated["distillation"]["loop_count"] == 10
    assert updated["distillation"]["method"] == "source bundle review/compress/next_view loop"
    assert (out / "README.md").exists()
    assert (out / "distillation_audit.json").exists()
    for index in range(1, 11):
        assert (out / "loops" / f"loop_{index:02d}_review.md").exists()
        assert (out / "loops" / f"loop_{index:02d}_compressed.md").exists()
        assert (out / "loops" / f"loop_{index:02d}_next_view.md").exists()
    loop_text = (out / "loops" / "loop_01_review.md").read_text(encoding="utf-8")
    assert "Source Reading" in loop_text
    assert "口調" not in loop_text


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


def test_make_source_records_compresses_chat_without_full_raw_dump(tmp_path: Path) -> None:
    path = tmp_path / "chat.json"
    _write_chat(
        path,
        "conv-source",
        "知識蒸留相談",
        [
            ("user", "大量の資料を圧縮して構造を作り、評価で測れるようにしたい"),
            ("assistant", "できます"),
            ("user", "意味がわからん。普通の言葉でフローを言って"),
        ],
    )
    conversation = load_chat_export(path)
    assert conversation is not None

    records = make_source_records([conversation])

    assert records[0]["title_hint"] == "知識蒸留相談"
    move_names = {item["name"] for item in records[0]["moves"]}
    assert "builds_knowledge_from_many_sources" in move_names
    assert "rejects_vague_or_wrong_frame" in move_names
    assert records[0]["source_scope"] == "redacted compressed user turns from one chat conversation"


def test_load_jsonl_keeps_unicode_line_separator_inside_json_string(tmp_path: Path) -> None:
    path = tmp_path / "data.jsonl"
    path.write_text(
        json.dumps({"text": "a\u2028b"}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    rows = load_jsonl(path)

    assert rows == [{"text": "a\u2028b"}]

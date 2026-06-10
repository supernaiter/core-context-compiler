# ruff: noqa: E501

from __future__ import annotations

import hashlib
import json
import os
import random
import re
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

CHAT_TARGET_DIRS = ("Active_Check", "Archive")
DEFAULT_MODEL = "claude-opus-4-5-thinking"
DEFAULT_BASE_URL = "http://127.0.0.1:8045/v1"

SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"\b(?:ghp|gho|ghu|ghs|github_pat)_[A-Za-z0-9_]{16,}\b"),
    re.compile(r"\b[A-Za-z0-9_-]{32,}\b"),
    re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b"),
    re.compile(r"\+?\d[\d\s().-]{8,}\d"),
]
ADDRESS_PATTERN = re.compile(
    r"(?:北海道|東京都|京都府|大阪府|.{2,3}県).{0,24}?(?:市|区|町|村).{0,24}?"
    r"(?:丁目|番地|番|号)"
)

STYLE_MARKERS = {
    "direct_command": ["やれ", "して", "作れ", "進め", "止めて", "見せて", "調べ", "実装"],
    "challenge": ["違う", "意味がわから", "造語", "冷静", "落ち着いて", "そもそも"],
    "framework": ["構造", "モデル", "フロー", "体系", "抽象", "差分", "圧縮", "評価"],
    "evidence": ["根拠", "検証", "テスト", "サンプル", "実験", "測れる", "定量"],
    "speed": ["最短", "早く", "今", "今日", "MVP", "動く"],
}
PROHIBITION_MARKERS = ["造語", "外部検索", "APIモデル", "python", "Python", "ログ", "媚び"]
QUESTION_MARKERS = ["何", "なに", "なぜ", "どう", "どこ", "でき", "じゃあ", "んで", "つまり"]
STOP_TERMS = {
    "これ",
    "それ",
    "ここ",
    "ため",
    "もの",
    "こと",
    "よう",
    "さん",
    "する",
    "した",
    "して",
    "いる",
    "ある",
    "ない",
    "です",
    "ます",
    "じゃあ",
    "んで",
}

SOURCE_REVIEW_SEED_VIEWS = [
    "まず圧縮済みsource bundle全体を読み、何の資料群か、何に使える知識かを整理する。",
    "前回viewで見落とした問い、判断基準、作業目的をsource bundleから拾い直す。",
    "決定、禁止、制約、前提、未完了をsource bundle内の根拠へ結び直す。",
    "失敗、詰まり、訂正、やり直し要求を読み、どの条件で判断が変わるかを出す。",
    "個別の会話から、反復する構造、抽象化、モデル化の型を作る。",
    "評価方法、答え合わせ方法、弱い結果の扱いをsource bundleから抽出する。",
    "実装、Issue、検証、記録へ移る条件をsource bundleから抽出する。",
    "古い見方、反例、警告、更新が必要な規則を残す。",
    "次のbotに渡すため、source bundleから普通の知識との差分だけに圧縮する。",
    "全loopを統合し、chatbotが参照する最終viewと未検証点を作る。",
]


@dataclass(frozen=True)
class ChatTurn:
    role: str
    text: str
    create_time: float | None = None


@dataclass(frozen=True)
class ChatConversation:
    conversation_id: str
    title: str
    create_time: float | None
    update_time: float | None
    source_path: str
    turns: list[ChatTurn]


@dataclass(frozen=True)
class EvalItem:
    id: str
    title_hint: str
    display_context: list[dict[str, str]]
    model_context: str
    hidden_answer: str
    source_id: str


def redact_sensitive(text: str) -> str:
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    redacted = ADDRESS_PATTERN.sub("[REDACTED_ADDRESS]", redacted)
    return redacted


def _content_text(content: dict[str, Any]) -> str:
    parts = content.get("parts") or []
    texts: list[str] = []
    for part in parts:
        if isinstance(part, str):
            texts.append(part)
        elif isinstance(part, dict) and isinstance(part.get("text"), str):
            texts.append(part["text"])
    return "".join(texts).strip()


def load_chat_export(path: str | Path) -> ChatConversation | None:
    source_path = Path(path)
    data = json.loads(source_path.read_text(encoding="utf-8"))
    mapping = data.get("mapping") or {}
    node_id = data.get("current_node")
    if not node_id or not isinstance(mapping, dict):
        return None

    turns: list[ChatTurn] = []
    seen: set[str] = set()
    while node_id and node_id not in seen:
        seen.add(node_id)
        node = mapping.get(node_id)
        if not isinstance(node, dict):
            break
        message = node.get("message")
        if isinstance(message, dict):
            role = (message.get("author") or {}).get("role")
            content = message.get("content") or {}
            text = _content_text(content)
            if role in {"user", "assistant"} and text:
                turns.append(
                    ChatTurn(
                        role=role,
                        text=text,
                        create_time=message.get("create_time"),
                    )
                )
        node_id = node.get("parent")

    turns.reverse()
    if not turns:
        return None
    conversation_id = str(data.get("conversation_id") or data.get("id") or source_path.stem)
    return ChatConversation(
        conversation_id=conversation_id,
        title=str(data.get("title") or "Untitled"),
        create_time=data.get("create_time"),
        update_time=data.get("update_time"),
        source_path=str(source_path),
        turns=turns,
    )


def discover_chat_files(chat_root: str | Path) -> list[Path]:
    root = Path(chat_root)
    if (root / "sorted_chats").exists():
        root = root / "sorted_chats"
    paths: list[Path] = []
    for dirname in CHAT_TARGET_DIRS:
        candidate = root / dirname
        if candidate.exists():
            paths.extend(sorted(candidate.glob("*.json")))
    if not paths:
        paths = sorted(root.glob("*.json"))
    return paths


def split_name(conversation_id: str, holdout_ratio: float) -> str:
    digest = hashlib.sha256(conversation_id.encode("utf-8")).hexdigest()
    bucket = int(digest[:8], 16) / 0xFFFFFFFF
    return "holdout" if bucket < holdout_ratio else "train"


def load_split_conversations(
    chat_root: str | Path,
    holdout_ratio: float = 0.1,
) -> tuple[list[ChatConversation], list[ChatConversation]]:
    train: list[ChatConversation] = []
    holdout: list[ChatConversation] = []
    for path in discover_chat_files(chat_root):
        conversation = load_chat_export(path)
        if conversation is None:
            continue
        if split_name(conversation.conversation_id, holdout_ratio) == "holdout":
            holdout.append(conversation)
        else:
            train.append(conversation)
    return train, holdout


def _user_texts(conversations: list[ChatConversation]) -> list[str]:
    texts: list[str] = []
    for conversation in conversations:
        for turn in conversation.turns:
            if turn.role == "user":
                texts.append(redact_sensitive(turn.text))
    return texts


def _count_markers(texts: list[str], markers: dict[str, list[str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for name, words in markers.items():
        counts[name] = sum(1 for text in texts if any(word in text for word in words))
    return counts


def _top_terms(texts: list[str], limit: int = 24) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    for text in texts:
        for token in re.findall(r"[A-Za-z][A-Za-z0-9_+-]{2,}|[一-龥ァ-ヶー]{2,}", text):
            if token in STOP_TERMS or len(token) > 32:
                continue
            counts[token] = counts.get(token, 0) + 1
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [{"term": term, "count": count} for term, count in ranked[:limit]]


def build_profile(
    train_conversations: list[ChatConversation],
    *,
    max_examples: int = 24,
) -> dict[str, Any]:
    texts = _user_texts(train_conversations)
    joined = "\n".join(texts)
    total_chars = sum(len(text) for text in texts)
    question_count = sum(1 for text in texts if "?" in text or "？" in text)
    question_count += sum(1 for text in texts if any(marker in text for marker in QUESTION_MARKERS))
    command_count = sum(
        1 for text in texts if any(marker in text for marker in STYLE_MARKERS["direct_command"])
    )
    prohibition_hits = sorted({marker for marker in PROHIBITION_MARKERS if marker in joined})
    marker_counts = _count_markers(texts, STYLE_MARKERS)
    top_markers = [
        {"name": name, "count": count}
        for name, count in sorted(marker_counts.items(), key=lambda item: (-item[1], item[0]))
        if count
    ]
    profile = {
        "what_this_is": "個人チャット履歴から作った検証用botの圧縮プロファイル。本人そのものではない。",
        "source_policy": {
            "raw_logs_committed": False,
            "model_receives_raw_history": False,
            "train_only": True,
        },
        "counts": {
            "train_conversations": len(train_conversations),
            "user_messages": len(texts),
            "user_chars": total_chars,
        },
        "voice": {
            "short_direct_japanese": True,
            "uses_pressure_to_correct_agent": marker_counts.get("challenge", 0) > 0,
            "question_ratio": round(question_count / max(len(texts), 1), 4),
            "command_ratio": round(command_count / max(len(texts), 1), 4),
            "marker_counts": top_markers,
        },
        "question_patterns": [
            "まず前提と流れを確認する",
            "判断とモデル化を分けて問い直す",
            "具体例で試してから評価する",
            "弱い結果や欠落を隠させない",
        ],
        "prohibitions": prohibition_hits,
        "judgment_habits": [
            "大量の資料を読み、差分と例外を残す",
            "抽象化の前に、何に使える知識かを見る",
            "人間が採点できる形にして効果を測る",
            "実験で成功範囲と失敗範囲を分ける",
        ],
        "work_rules": [
            "GitHub Issue を作業リストにする",
            "動く試作品を先に作る",
            "検証結果と弱い点を明記する",
            "個人ログはGit管理しない",
        ],
        "interest_terms": _top_terms(texts, limit=max_examples),
        "compressed_rules": [
            "返答は日本語で短く、先に具体物を出す",
            "造語を避け、普通の言葉で思想と手順を述べる",
            "事実、推測、不明を分ける",
            "判断材料、例外、失敗、制約、次の打ち手を残す",
        ],
    }
    return _redact_json(profile)


def _source_moves(text: str) -> list[str]:
    moves = []
    if any(word in text for word in ["どう", "何", "なぜ", "フロー", "流れ"]):
        moves.append("asks_for_process_or_reason")
    if any(word in text for word in ["意味がわから", "違う", "造語", "冷静"]):
        moves.append("rejects_vague_or_wrong_frame")
    if any(word in text for word in ["実装", "作成", "Issue", "commit", "検証"]):
        moves.append("turns_discussion_into_work")
    if any(word in text for word in ["圧縮", "蒸留", "大量", "資料", "文献"]):
        moves.append("builds_knowledge_from_many_sources")
    if any(word in text for word in ["評価", "測", "ベンチ", "予測", "採点"]):
        moves.append("asks_for_measurable_evaluation")
    if any(word in text for word in ["構造", "モデル", "体系", "抽象", "視点"]):
        moves.append("asks_for_structure_or_view")
    if any(word in text for word in ["弱い", "未完", "欠け", "失敗", "警告"]):
        moves.append("forces_limits_and_failures")
    return moves or ["general_dialogue"]


def make_source_records(
    conversations: list[ChatConversation],
    *,
    limit: int = 600,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for conversation in conversations:
        user_texts = [
            redact_sensitive(turn.text)
            for turn in conversation.turns
            if turn.role == "user" and turn.text.strip()
        ]
        if not user_texts:
            continue
        moves: dict[str, int] = {}
        for text in user_texts:
            for move in _source_moves(text):
                moves[move] = moves.get(move, 0) + 1
        record = {
            "source_id": hashlib.sha256(conversation.conversation_id.encode()).hexdigest()[:16],
            "title_hint": _title_hint(conversation.title),
            "create_time": conversation.create_time,
            "user_turns": len(user_texts),
            "assistant_turns": sum(1 for turn in conversation.turns if turn.role == "assistant"),
            "terms": _top_terms(user_texts + [conversation.title], limit=16),
            "moves": [
                {"name": name, "count": count}
                for name, count in sorted(moves.items(), key=lambda item: (-item[1], item[0]))
            ],
            "compressed_evidence": [
                text.replace("\n", " ")[:220]
                for text in user_texts
                if any(move != "general_dialogue" for move in _source_moves(text))
            ][:5],
            "source_scope": "redacted compressed user turns from one chat conversation",
        }
        records.append(record)
        if len(records) >= limit:
            break
    return records


def write_source_bundle(records: list[dict[str, Any]], out_dir: str | Path) -> dict[str, Any]:
    out = Path(out_dir)
    jsonl_path = out / "source_bundle.jsonl"
    md_path = out / "source_bundle.md"
    with jsonl_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    lines = [
        "# Masterbot Source Bundle",
        "",
        "- input: raw sorted ChatGPT export JSON",
        "- content: redacted compressed records",
        "- raw_logs_committed: false",
        "- raw_history_sent_to_model: false",
        "",
    ]
    for record in records:
        lines.append(f"## {record['source_id']} {record['title_hint']}")
        lines.append(f"- user_turns: {record['user_turns']}")
        lines.append("- moves:")
        lines.extend(f"  - {item['name']}: {item['count']}" for item in record["moves"])
        lines.append("- terms:")
        lines.extend(f"  - {item['term']}: {item['count']}" for item in record["terms"][:8])
        lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return {
        "source_bundle_jsonl": str(jsonl_path),
        "source_bundle_md": str(md_path),
        "source_records": len(records),
    }


def _redact_json(value: Any) -> Any:
    if isinstance(value, str):
        return redact_sensitive(value)
    if isinstance(value, list):
        return [_redact_json(item) for item in value]
    if isinstance(value, dict):
        return {key: _redact_json(item) for key, item in value.items()}
    return value


def _title_hint(title: str) -> str:
    redacted = redact_sensitive(title)
    return redacted[:80]


def _context_summary(conversation: ChatConversation, target_index: int) -> str:
    previous = conversation.turns[max(0, target_index - 4) : target_index]
    assistant_text = " ".join(
        redact_sensitive(turn.text)[:240] for turn in previous if turn.role == "assistant"
    )
    user_text = " ".join(redact_sensitive(turn.text)[:160] for turn in previous if turn.role == "user")
    terms = _top_terms([conversation.title, assistant_text, user_text], limit=10)
    term_text = ", ".join(item["term"] for item in terms)
    return (
        f"title_hint={_title_hint(conversation.title)}; "
        f"previous_turns={len(previous)}; topic_terms={term_text}; "
        "task=この文脈で次にユーザーが言いそうな返答を書く"
    )


def make_eval_items(
    holdout_conversations: list[ChatConversation],
    *,
    limit: int = 100,
) -> list[EvalItem]:
    items: list[EvalItem] = []
    for conversation in holdout_conversations:
        for index, turn in enumerate(conversation.turns):
            if turn.role != "user" or index == 0:
                continue
            previous = conversation.turns[max(0, index - 4) : index]
            display_context = [
                {"role": item.role, "text": redact_sensitive(item.text)}
                for item in previous
                if item.role in {"user", "assistant"}
            ]
            digest = hashlib.sha256(f"{conversation.conversation_id}:{index}".encode()).hexdigest()[
                :16
            ]
            items.append(
                EvalItem(
                    id=digest,
                    title_hint=_title_hint(conversation.title),
                    display_context=display_context,
                    model_context=_context_summary(conversation, index),
                    hidden_answer=redact_sensitive(turn.text),
                    source_id=conversation.conversation_id,
                )
            )
            if len(items) >= limit:
                return items
    return items


def build_masterbot(
    chat_root: str | Path,
    out_dir: str | Path,
    *,
    holdout_ratio: float = 0.1,
    max_examples: int = 24,
) -> dict[str, Any]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    train, holdout = load_split_conversations(chat_root, holdout_ratio=holdout_ratio)
    profile = build_profile(train, max_examples=max_examples)
    source_records = make_source_records(train)
    source_bundle = write_source_bundle(source_records, out)
    eval_items = make_eval_items(holdout)
    manifest = {
        "created_at": datetime.now(UTC).isoformat(),
        "chat_root": str(chat_root),
        "train_conversations": len(train),
        "holdout_conversations": len(holdout),
        "holdout_items": len(eval_items),
        "profile_path": str(out / "profile.json"),
        "holdout_path": str(out / "holdout.jsonl"),
        **source_bundle,
        "privacy": {
            "raw_logs_committed": False,
            "model_receives_raw_history": False,
        },
    }
    (out / "profile.json").write_text(
        json.dumps(profile, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    with (out / "holdout.jsonl").open("w", encoding="utf-8") as handle:
        for item in eval_items:
            handle.write(json.dumps(asdict(item), ensure_ascii=False, sort_keys=True) + "\n")
    (out / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return manifest


def _score_signal_map(scores: list[dict[str, Any]]) -> dict[str, int]:
    real_scores = _real_master_scores(scores)
    signals = {"human_scores": len(real_scores), "low_scores": 0, "notes": 0}
    for score in real_scores:
        raw = str(score.get("score", "")).strip()
        if raw:
            try:
                if float(raw) <= 2.0:
                    signals["low_scores"] += 1
            except ValueError:
                pass
        if str(score.get("notes", "")).strip():
            signals["notes"] += 1
    return signals


def _real_master_scores(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    real_scores = []
    for score in scores:
        item_id = str(score.get("item_id", "")).strip()
        raw_score = str(score.get("score", "")).strip()
        if not item_id or item_id == "smoke":
            continue
        if not raw_score:
            continue
        real_scores.append(score)
    return real_scores


def summarize_source_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    move_counts: dict[str, int] = {}
    term_counts: dict[str, int] = {}
    for record in records:
        for move in record.get("moves", []):
            if isinstance(move, dict):
                name = str(move.get("name", ""))
                move_counts[name] = move_counts.get(name, 0) + int(move.get("count") or 0)
        for term in record.get("terms", []):
            if isinstance(term, dict):
                name = str(term.get("term", ""))
                term_counts[name] = term_counts.get(name, 0) + int(term.get("count") or 0)
    return {
        "source_records": len(records),
        "top_moves": [
            {"name": name, "count": count}
            for name, count in sorted(move_counts.items(), key=lambda item: (-item[1], item[0]))[:16]
        ],
        "top_terms": [
            {"term": name, "count": count}
            for name, count in sorted(term_counts.items(), key=lambda item: (-item[1], item[0]))[:24]
        ],
    }


def _selected_records_for_view(
    records: list[dict[str, Any]],
    previous_view: str,
    *,
    limit: int = 18,
) -> list[dict[str, Any]]:
    view_terms = set(re.findall(r"[一-龥ァ-ヶーA-Za-z0-9_+-]{2,}", previous_view))
    scored: list[tuple[int, dict[str, Any]]] = []
    for record in records:
        text = json.dumps(record, ensure_ascii=False)
        score = sum(1 for term in view_terms if term in text)
        score += len(record.get("compressed_evidence", []))
        score += int(record.get("user_turns") or 0) // 3
        scored.append((score, record))
    return [record for _, record in sorted(scored, key=lambda item: (-item[0], item[1]["source_id"]))[:limit]]


def _review_source_bundle(
    records: list[dict[str, Any]],
    previous_view: str,
    loop_index: int,
    scores: list[dict[str, Any]],
) -> dict[str, Any]:
    summary = summarize_source_records(records)
    selected = _selected_records_for_view(records, previous_view)
    selected_moves: dict[str, int] = {}
    selected_terms: dict[str, int] = {}
    evidence: list[str] = []
    for record in selected:
        for move in record.get("moves", []):
            selected_moves[move["name"]] = selected_moves.get(move["name"], 0) + int(move["count"])
        for term in record.get("terms", []):
            selected_terms[term["term"]] = selected_terms.get(term["term"], 0) + int(term["count"])
        evidence.extend(record.get("compressed_evidence", [])[:2])
    top_moves = [
        {"name": name, "count": count}
        for name, count in sorted(selected_moves.items(), key=lambda item: (-item[1], item[0]))[:10]
    ]
    top_terms = [
        {"term": name, "count": count}
        for name, count in sorted(selected_terms.items(), key=lambda item: (-item[1], item[0]))[:12]
    ]
    source_reading = [
        f"source bundleは{summary['source_records']}件の圧縮会話記録。",
        "反復しているのは、資料を大量に読み、構造を作り、測れる形に落とす要求。",
        "表面再現ではなく、問い、判断材料、作業化、失敗扱いを残す必要がある。",
    ]
    if loop_index >= 4:
        source_reading.append("前loopのviewを使い、欠落、例外、未検証点を優先して読む。")
    if loop_index >= 8:
        source_reading.append("最終botへ渡すため、普通の知識ではなく差分だけに寄せる。")
    return {
        "loop": loop_index,
        "previous_view": previous_view,
        "source_summary": summary,
        "selected_source_count": len(selected),
        "top_moves": top_moves,
        "top_terms": top_terms,
        "source_reading": source_reading,
        "compressed_evidence": evidence[:12],
        "score_signals": _score_signal_map(scores),
    }


def _compress_review(review: dict[str, Any]) -> dict[str, Any]:
    principles = [
        "大量資料をそのまま覚えず、問い、判断材料、失敗、制約、更新条件へ圧縮する。",
        "普通の要約ではなく、次の判断を変える差分だけを残す。",
        "検証できないものは検証済みと言わない。",
    ]
    if review["score_signals"]["human_scores"] == 0:
        principles.append("人間採点が無いので、現段階は検証前の仮説として扱う。")
    return {
        "loop": review["loop"],
        "kept": {
            "source_reading": review["source_reading"],
            "top_moves": review["top_moves"][:8],
            "top_terms": review["top_terms"][:10],
            "principles": principles,
            "human_scored_items": review["score_signals"]["human_scores"],
        },
        "token_policy": "compressed source-review output; not raw chat history",
    }


def _derive_next_view(review: dict[str, Any], compressed: dict[str, Any]) -> str:
    seed_index = min(review["loop"], len(SOURCE_REVIEW_SEED_VIEWS) - 1)
    move_names = [item["name"] for item in review.get("top_moves", [])[:4]]
    term_names = [item["term"] for item in review.get("top_terms", [])[:6]]
    return (
        f"{SOURCE_REVIEW_SEED_VIEWS[seed_index]} "
        f"前回保持: {', '.join(move_names) or 'none'}。"
        f"注目語: {', '.join(term_names) or 'none'}。"
        "次は、根拠、範囲、例外、未検証点を分けて読む。"
    )


def _merge_source_review_profile(
    profile: dict[str, Any],
    compressed: dict[str, Any],
    next_view: str,
    loop_index: int,
) -> dict[str, Any]:
    next_profile = json.loads(json.dumps(profile, ensure_ascii=False))
    history = list(next_profile.get("distillation_history", []))
    history.append(
        {
            "loop": loop_index,
            "view": next_view,
            "kept": compressed["kept"],
        }
    )
    principles: list[str] = []
    for item in history:
        kept = item.get("kept", {})
        for principle in kept.get("principles", []):
            if principle not in principles:
                principles.append(principle)
    next_profile["distillation"] = {
        "loop_count": loop_index,
        "method": "source bundle review/compress/next_view loop",
        "raw_history_sent_to_model": False,
        "human_scored_items": compressed["kept"].get("human_scored_items", 0),
        "weak_result": "人間採点が無いので、現段階は検証前の仮説として扱う。"
        in principles,
    }
    next_profile["distilled_source_view"] = {
        "loop": loop_index,
        "next_view": next_view,
        "kept": compressed["kept"],
    }
    next_profile["compressed_rules"] = principles[-8:]
    next_profile["distillation_history"] = history[-10:]
    return _redact_json(next_profile)


def _markdown_list(items: list[Any]) -> str:
    if not items:
        return "- none\n"
    lines = []
    for item in items:
        if isinstance(item, dict):
            text = json.dumps(item, ensure_ascii=False, sort_keys=True)
        else:
            text = str(item)
        lines.append(f"- {text}")
    return "\n".join(lines) + "\n"


def _write_loop_files(
    loops_dir: Path,
    loop_index: int,
    review: dict[str, Any],
    compressed: dict[str, Any],
    next_view: str,
    profile: dict[str, Any],
) -> None:
    prefix = f"loop_{loop_index:02d}"
    review = [
        f"# Loop {loop_index:02d} Review",
        "",
        f"- previous_view: {review['previous_view']}",
        f"- source_records: {review['source_summary']['source_records']}",
        f"- selected_source_count: {review['selected_source_count']}",
        f"- human_scored_items: {review['score_signals']['human_scores']}",
        "",
        "## Source Signals",
        _markdown_list(review["top_moves"]),
        "## Source Reading",
        _markdown_list(review["source_reading"]),
        "## Compressed Evidence",
        _markdown_list(review["compressed_evidence"]),
        "## Weak Result",
        "- human scoring is not available yet; this loop is source-derived, not validated by master scores.\n"
        if review["score_signals"]["human_scores"] == 0
        else "- human scoring exists but still needs manual interpretation.\n",
    ]
    compressed_lines = [
        f"# Loop {loop_index:02d} Compressed Profile",
        "",
        "## Kept",
        "```json",
        json.dumps(compressed["kept"], ensure_ascii=False, indent=2, sort_keys=True),
        "```",
    ]
    next_view_lines = [
        f"# Loop {loop_index:02d} Next View",
        "",
        f"- next_view: {next_view}",
        "- use_for_bot: yes",
        "",
        "## Read Next By Asking",
        _markdown_list(
            [
                "この資料束は何の判断を変えるか",
                "どの条件、例外、失敗が落ちているか",
                "普通の知識との差分は何か",
                "どこから先は未検証か",
            ]
        ),
    ]
    (loops_dir / f"{prefix}_review.md").write_text("\n".join(review), encoding="utf-8")
    (loops_dir / f"{prefix}_compressed.md").write_text(
        "\n".join(compressed_lines), encoding="utf-8"
    )
    (loops_dir / f"{prefix}_next_view.md").write_text(
        "\n".join(next_view_lines), encoding="utf-8"
    )


def distill_masterbot(
    profile_path: str | Path,
    out_dir: str | Path,
    *,
    source_bundle_path: str | Path | None = None,
    scores_path: str | Path | None = None,
    loops: int = 10,
    update_profile: bool = True,
) -> dict[str, Any]:
    profile_source = Path(profile_path)
    out = Path(out_dir)
    loops_dir = out / "loops"
    loops_dir.mkdir(parents=True, exist_ok=True)
    profile = json.loads(profile_source.read_text(encoding="utf-8"))
    source_bundle = (
        Path(source_bundle_path)
        if source_bundle_path is not None
        else profile_source.parent / "source_bundle.jsonl"
    )
    records = load_jsonl(source_bundle)
    if not records:
        records = [
            {
                "source_id": "profile_fallback",
                "title_hint": "profile fallback",
                "user_turns": profile.get("counts", {}).get("user_messages", 0),
                "moves": profile.get("voice", {}).get("marker_counts", []),
                "terms": profile.get("interest_terms", []),
                "compressed_evidence": [
                    "source_bundle.jsonl missing; using compressed profile only"
                ],
            }
        ]
    scores = load_jsonl(scores_path) if scores_path else []
    real_scores = _real_master_scores(scores)
    total_loops = min(loops, len(SOURCE_REVIEW_SEED_VIEWS))
    next_view = SOURCE_REVIEW_SEED_VIEWS[0]
    for loop_index in range(1, total_loops + 1):
        review = _review_source_bundle(records, next_view, loop_index, scores)
        compressed = _compress_review(review)
        next_view = _derive_next_view(review, compressed)
        profile = _merge_source_review_profile(profile, compressed, next_view, loop_index)
        _write_loop_files(loops_dir, loop_index, review, compressed, next_view, profile)

    final_profile = out / "profile_distilled.json"
    final_profile.write_text(
        json.dumps(profile, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    if update_profile:
        profile_source.write_text(
            json.dumps(profile, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
    audit = {
        "created_at": datetime.now(UTC).isoformat(),
        "loops": total_loops,
        "profile_path": str(profile_source),
        "source_bundle_path": str(source_bundle),
        "source_records": len(records),
        "final_profile_path": str(final_profile),
        "updated_profile": update_profile,
        "raw_logs_committed": False,
        "raw_history_sent_to_model": False,
        "human_scored_items": len(real_scores),
        "ignored_score_items": len(scores) - len(real_scores),
        "weak_result": len(real_scores) == 0,
    }
    (out / "distillation_audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    readme = [
        "# Masterbot 10-loop Distillation",
        "",
        f"- loops: {total_loops}",
        f"- source_bundle: {source_bundle}",
        f"- source_records: {len(records)}",
        f"- final_profile: {final_profile}",
        f"- updated_profile: {update_profile}",
        f"- human_scored_items: {len(real_scores)}",
        f"- ignored_score_items: {len(scores) - len(real_scores)}",
        "- raw_logs_committed: false",
        "- raw_history_sent_to_model: false",
        "",
        "## Files",
        "- loops/loop_XX_review.md",
        "- loops/loop_XX_compressed.md",
        "- loops/loop_XX_next_view.md",
        "- profile_distilled.json",
        "- distillation_audit.json",
        "",
        "## Weak Result",
        "- This run reads the compressed source bundle, then writes review/compressed/next_view.",
        "- If human scores are absent or only smoke data, the loop is not a full behavioral validation.",
    ]
    (out / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    return audit


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    source = Path(path)
    if not source.exists():
        return []
    return [
        json.loads(line)
        for line in source.read_text(encoding="utf-8").split("\n")
        if line.strip()
    ]


def build_prompt(profile: dict[str, Any], mode: str, user_message: str) -> list[dict[str, str]]:
    system_parts = [
        "あなたは検証用チャットbotです。",
        "本人ではない。個人の生ログを暗唱しない。",
        "日本語で短く、具体的に返す。",
    ]
    if mode in {"profile", "profile+rules"}:
        allowed = {
            "voice": profile.get("voice"),
            "question_patterns": profile.get("question_patterns"),
            "prohibitions": profile.get("prohibitions"),
            "judgment_habits": profile.get("judgment_habits"),
            "work_rules": profile.get("work_rules"),
            "interest_terms": profile.get("interest_terms"),
        }
        system_parts.append("圧縮プロファイル:")
        system_parts.append(json.dumps(_redact_json(allowed), ensure_ascii=False, sort_keys=True))
    if mode == "profile+rules":
        system_parts.append("圧縮ルール:")
        system_parts.append(
            json.dumps(profile.get("compressed_rules", []), ensure_ascii=False, sort_keys=True)
        )
    return [
        {"role": "system", "content": "\n".join(system_parts)},
        {"role": "user", "content": redact_sensitive(user_message)},
    ]


def call_openai_compatible(
    messages: list[dict[str, str]],
    *,
    model: str | None = None,
    base_url: str | None = None,
    timeout: float = 120.0,
) -> str:
    selected_model = model or os.environ.get("MASTERBOT_MODEL") or DEFAULT_MODEL
    selected_base_url = (base_url or os.environ.get("MASTERBOT_BASE_URL") or DEFAULT_BASE_URL).rstrip(
        "/"
    )
    payload = json.dumps(
        {"model": selected_model, "messages": messages, "stream": False},
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{selected_base_url}/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('MASTERBOT_API_KEY', 'sk-antigravity')}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        return f"不可: ローカルモデル接続失敗 {exc}"
    try:
        return str(data["choices"][0]["message"]["content"])
    except (KeyError, IndexError, TypeError):
        return "不可: モデル応答形式が不明"


def auto_score(candidate: str, item: dict[str, Any] | None = None) -> dict[str, Any]:
    text = candidate.strip()
    hidden = (item or {}).get("hidden_answer", "")
    leak = False
    if hidden:
        if hidden in text:
            leak = True
        for start in range(0, max(len(hidden) - 24, 0), 12):
            snippet = hidden[start : start + 28]
            if len(snippet) >= 20 and snippet in text:
                leak = True
                break
    return {
        "shortness": len(text) <= 420,
        "has_question_or_next_step": any(word in text for word in QUESTION_MARKERS + ["条件", "例外", "検証"]),
        "prohibited_word_hits": [word for word in PROHIBITION_MARKERS if word in text],
        "raw_answer_leak": leak,
        "chars": len(text),
    }


class MasterbotServer:
    def __init__(self, profile_path: str | Path, holdout_path: str | Path, scores_path: str | Path):
        self.profile_path = Path(profile_path)
        self.holdout_path = Path(holdout_path)
        self.scores_path = Path(scores_path)
        self.profile = json.loads(self.profile_path.read_text(encoding="utf-8"))
        self.items = load_jsonl(self.holdout_path)
        self.by_id = {item["id"]: item for item in self.items}

    def chat(self, message: str, mode: str) -> dict[str, Any]:
        messages = build_prompt(self.profile, mode, message)
        answer = call_openai_compatible(messages)
        return {"answer": answer, "auto": auto_score(answer)}

    def eval_chat(self, item_id: str, mode: str) -> dict[str, Any]:
        item = self.by_id[item_id]
        messages = build_prompt(self.profile, mode, item["model_context"])
        answer = call_openai_compatible(messages)
        return {"answer": answer, "auto": auto_score(answer, item)}

    def eval_items(self, reveal: bool = False) -> list[dict[str, Any]]:
        chosen = self.items[:20]
        if reveal:
            return chosen
        public: list[dict[str, Any]] = []
        for item in chosen:
            copy = dict(item)
            copy.pop("hidden_answer", None)
            public.append(copy)
        return public

    def reveal(self, item_id: str) -> dict[str, Any]:
        return self.by_id[item_id]

    def save_score(self, payload: dict[str, Any]) -> dict[str, str]:
        self.scores_path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "created_at": time.time(),
            "item_id": payload.get("item_id"),
            "mode": payload.get("mode"),
            "score": payload.get("score"),
            "notes": redact_sensitive(str(payload.get("notes", "")))[:2000],
        }
        with self.scores_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        return {"status": "ok"}


def _html_page() -> bytes:
    return f"""<!doctype html>
<!-- {""} -->
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Masterbot</title>
<style>
body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #f6f7f9; color: #1d1f23; }}
main {{ max-width: 1120px; margin: 0 auto; padding: 24px; display: grid; gap: 16px; }}
section {{ background: white; border: 1px solid #d9dee7; border-radius: 8px; padding: 16px; }}
h1, h2 {{ margin: 0 0 12px; }}
textarea {{ width: 100%; min-height: 108px; box-sizing: border-box; font: inherit; padding: 10px; border: 1px solid #c7ceda; border-radius: 6px; }}
button, select, input {{ font: inherit; padding: 8px 10px; border: 1px solid #b9c1ce; border-radius: 6px; background: white; }}
button {{ cursor: pointer; background: #1f6feb; color: white; border-color: #1f6feb; }}
pre {{ white-space: pre-wrap; background: #f0f2f5; padding: 12px; border-radius: 6px; overflow-x: auto; }}
.row {{ display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }}
.turn {{ border-left: 3px solid #9aa7b8; padding: 8px 10px; margin: 8px 0; background: #f8fafc; }}
.muted {{ color: #5d6675; }}
</style>
</head>
<body>
<main>
<h1>Masterbot</h1>
<section>
<h2>Chat</h2>
<div class="row">
<select id="mode">
<option value="base">base</option>
<option value="profile">profile</option>
<option value="profile+rules">profile+rules</option>
</select>
<button onclick="sendChat()">送信</button>
</div>
<textarea id="message" placeholder="話しかける"></textarea>
<pre id="answer"></pre>
</section>
<section>
<h2>Holdout Eval</h2>
<div class="row">
<select id="evals"></select>
<button onclick="loadEval()">表示</button>
<button onclick="runEval()">3モード実行</button>
<button onclick="revealAnswer()">答えを見る</button>
</div>
<div id="context"></div>
<pre id="evalAnswer"></pre>
<div class="row">
<input id="score" placeholder="score">
<input id="notes" placeholder="notes">
<button onclick="saveScore()">採点保存</button>
</div>
</section>
</main>
<script>
let items = [];
let currentId = null;
async function api(path, body) {{
  const opts = body ? {{method:'POST', headers:{{'Content-Type':'application/json'}}, body:JSON.stringify(body)}} : {{}};
  const res = await fetch(path, opts);
  return await res.json();
}}
async function init() {{
  items = (await api('/api/eval')).items;
  const sel = document.getElementById('evals');
  sel.innerHTML = items.map(x => `<option value="${{x.id}}">${{x.title_hint || x.id}}</option>`).join('');
  if (items.length) loadEval();
}}
async function sendChat() {{
  const data = await api('/api/chat', {{mode: mode.value, message: message.value}});
  answer.textContent = data.answer + '\\n\\n' + JSON.stringify(data.auto, null, 2);
}}
function selectedItem() {{ return items.find(x => x.id === evals.value); }}
function loadEval() {{
  const item = selectedItem();
  if (!item) return;
  currentId = item.id;
  context.innerHTML = `<p class="muted">${{item.title_hint}}</p>` + item.display_context.map(t => `<div class="turn"><b>${{t.role}}</b><br>${{escapeHtml(t.text)}}</div>`).join('');
}}
async function runEval() {{
  const modes = ['base', 'profile', 'profile+rules'];
  const out = [];
  for (const m of modes) {{
    const data = await api('/api/eval_chat', {{item_id: currentId, mode: m}});
    out.push(`## ${{m}}\\n${{data.answer}}\\n${{JSON.stringify(data.auto)}}`);
  }}
  evalAnswer.textContent = out.join('\\n\\n');
}}
async function revealAnswer() {{
  const data = await api('/api/eval?reveal=1&id=' + encodeURIComponent(currentId));
  evalAnswer.textContent += '\\n\\n## actual\\n' + data.item.hidden_answer;
}}
async function saveScore() {{
  await api('/api/score', {{item_id: currentId, mode: mode.value, score: score.value, notes: notes.value}});
}}
function escapeHtml(s) {{
  return s.replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
}}
init();
</script>
</body>
</html>""".encode()


def serve_masterbot(
    profile_path: str | Path,
    holdout_path: str | Path,
    scores_path: str | Path,
    *,
    port: int = 8765,
) -> None:
    app = MasterbotServer(profile_path, holdout_path, scores_path)

    class Handler(BaseHTTPRequestHandler):
        def _json(self, payload: dict[str, Any], status: int = 200) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _body(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0"))
            if not length:
                return {}
            return json.loads(self.rfile.read(length).decode("utf-8"))

        def do_GET(self) -> None:  # noqa: N802
            path, _, query = self.path.partition("?")
            if path == "/":
                body = _html_page()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            if path == "/favicon.ico":
                self.send_response(204)
                self.end_headers()
                return
            if path == "/api/eval":
                params = dict(part.split("=", 1) for part in query.split("&") if "=" in part)
                if params.get("reveal") == "1" and "id" in params:
                    self._json({"item": app.reveal(params["id"])})
                    return
                self._json({"items": app.eval_items(reveal=False)})
                return
            self._json({"error": "not_found"}, status=404)

        def do_POST(self) -> None:  # noqa: N802
            try:
                payload = self._body()
                if self.path == "/api/chat":
                    self._json(app.chat(str(payload.get("message", "")), str(payload.get("mode", "base"))))
                elif self.path == "/api/eval_chat":
                    self._json(
                        app.eval_chat(str(payload.get("item_id")), str(payload.get("mode", "base")))
                    )
                elif self.path == "/api/score":
                    self._json(app.save_score(payload))
                else:
                    self._json({"error": "not_found"}, status=404)
            except Exception as exc:  # pragma: no cover - keeps UI usable for manual eval
                self._json({"error": str(exc)}, status=500)

        def log_message(self, format: str, *args: Any) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"http://127.0.0.1:{port}")
    server.serve_forever()


def sample_eval_item(path: str | Path, seed: int = 0) -> dict[str, Any] | None:
    items = load_jsonl(path)
    if not items:
        return None
    rng = random.Random(seed)
    item = dict(rng.choice(items))
    item.pop("hidden_answer", None)
    return item

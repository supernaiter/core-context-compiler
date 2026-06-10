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
    eval_items = make_eval_items(holdout)
    manifest = {
        "created_at": datetime.now(UTC).isoformat(),
        "chat_root": str(chat_root),
        "train_conversations": len(train),
        "holdout_conversations": len(holdout),
        "holdout_items": len(eval_items),
        "profile_path": str(out / "profile.json"),
        "holdout_path": str(out / "holdout.jsonl"),
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


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    source = Path(path)
    if not source.exists():
        return []
    return [
        json.loads(line)
        for line in source.read_text(encoding="utf-8").splitlines()
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

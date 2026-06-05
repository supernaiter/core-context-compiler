from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from corectx.evals.domain_judgment import (
    DEFAULT_DOMAIN_ROOT,
    MCP_SERVICE_SYSTEM,
    DomainJudgmentTask,
    _load_folded_context,
    _risk_flags,
    _short,
    judge_task,
    load_ssi_judgment_tasks,
)

PROTOCOL_VERSION = "2024-11-05"
TOOLS = [
    "get_domain_context",
    "judge_paper_strength",
    "critique_claim",
    "suggest_next_reading",
    "explain_judgment",
]


class DomainIntelligenceService:
    def __init__(self, domain: str, domain_root: str | Path | None = None) -> None:
        if domain != "autonomous_domain_evolver":
            raise ValueError(f"unsupported domain: {domain}")
        self.domain = domain
        self.root = Path(domain_root) if domain_root else DEFAULT_DOMAIN_ROOT
        self.folded_context = _load_folded_context(self.root)
        self.tasks = load_ssi_judgment_tasks(
            self.root,
            task_count=100,
            suite="ssi_specialist",
        )

    def get_domain_context(self, arguments: dict[str, Any]) -> dict[str, Any]:
        query = str(arguments.get("query", "")).strip()
        limit = int(arguments.get("limit", 5))
        tasks = self._matching_tasks(query, limit=limit)
        source_ids = [task.source for task in tasks]
        risk_flags = sorted({flag for task in tasks for flag in _risk_flags(task)})
        return {
            "tool": "get_domain_context",
            "domain": self.domain,
            "query": query,
            "context": _short(self.folded_context, limit=1200),
            "source_ids": source_ids,
            "rationale": [
                "Rank SSI work by interface realism before headline decoder accuracy.",
                "Separate signal channel, calibration burden, transfer evidence, and scope.",
            ],
            "risk_flags": risk_flags,
            "judgment_text": (
                "Use folded SSI criteria: captured production signal, low user burden, "
                "cross-session or cross-speaker transfer, and explicit weakness tracing."
            ),
        }

    def judge_paper_strength(self, arguments: dict[str, Any]) -> dict[str, Any]:
        task = self._select_task(arguments)
        result = judge_task(task, MCP_SERVICE_SYSTEM, self.folded_context)
        return {
            "tool": "judge_paper_strength",
            "domain": self.domain,
            "paper_id": task.paper_id,
            "title": task.title,
            "score": result.expert_judgment_score,
            "paper_strength_score": task.expert_score,
            "strength_label": _strength_label(task.expert_score),
            "source_ids": [task.source],
            "rationale": _rationale(task),
            "risk_flags": _risk_flags(task),
            "judgment_text": result.answer,
        }

    def critique_claim(self, arguments: dict[str, Any]) -> dict[str, Any]:
        task = self._select_task(arguments)
        claim = str(arguments.get("claim") or task.claim)
        return {
            "tool": "critique_claim",
            "domain": self.domain,
            "paper_id": task.paper_id,
            "claim": claim,
            "source_ids": [task.source],
            "rationale": _rationale(task),
            "risk_flags": _risk_flags(task),
            "judgment_text": (
                f"Claim critique: {_short(claim)}. Treat it as bounded unless the "
                f"evaluation proves transfer, burden, and online interface realism. "
                f"Main weakness: {_short(task.weakness)}"
            ),
        }

    def suggest_next_reading(self, arguments: dict[str, Any]) -> dict[str, Any]:
        limit = int(arguments.get("limit", 3))
        candidates = sorted(
            self.tasks,
            key=lambda task: (task.expert_score, task.task_type != "next_paper_selection"),
            reverse=True,
        )[:limit]
        return {
            "tool": "suggest_next_reading",
            "domain": self.domain,
            "recommendations": [
                {
                    "paper_id": task.paper_id,
                    "title": task.title,
                    "source_ids": [task.source],
                    "reason": (
                        f"Prioritize because signal={','.join(task.input_signal) or 'unknown'} "
                        f"and expert_score={task.expert_score:.1f}."
                    ),
                    "risk_flags": _risk_flags(task),
                }
                for task in candidates
            ],
            "rationale": [
                "Read papers that improve SSI boundary judgment, not just accuracy recall.",
                "Prefer evidence with realistic signal capture and transfer tests.",
            ],
            "risk_flags": sorted({flag for task in candidates for flag in _risk_flags(task)}),
            "judgment_text": "Next reading should sharpen interface-realism and scope guards.",
        }

    def explain_judgment(self, arguments: dict[str, Any]) -> dict[str, Any]:
        task = self._select_task(arguments)
        result = judge_task(task, MCP_SERVICE_SYSTEM, self.folded_context)
        return {
            "tool": "explain_judgment",
            "domain": self.domain,
            "paper_id": task.paper_id,
            "source_ids": [task.source],
            "score": result.expert_judgment_score,
            "rationale": [
                *_rationale(task),
                "The score rewards scoped SSI evidence and penalizes headline-only claims.",
            ],
            "risk_flags": _risk_flags(task),
            "judgment_text": result.answer,
        }

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name == "get_domain_context":
            return self.get_domain_context(arguments)
        if name == "judge_paper_strength":
            return self.judge_paper_strength(arguments)
        if name == "critique_claim":
            return self.critique_claim(arguments)
        if name == "suggest_next_reading":
            return self.suggest_next_reading(arguments)
        if name == "explain_judgment":
            return self.explain_judgment(arguments)
        raise ValueError(f"unknown tool: {name}")

    def _matching_tasks(self, query: str, *, limit: int) -> list[DomainJudgmentTask]:
        if not query:
            return self.tasks[:limit]
        lowered = query.lower()
        matches = [
            task
            for task in self.tasks
            if lowered in task.title.lower()
            or lowered in task.paper_id.lower()
            or lowered in task.claim.lower()
            or lowered in " ".join(task.input_signal).lower()
        ]
        return (matches or self.tasks)[:limit]

    def _select_task(self, arguments: dict[str, Any]) -> DomainJudgmentTask:
        key = str(arguments.get("paper_id") or arguments.get("title") or "").strip().lower()
        if key:
            for task in self.tasks:
                if key in task.paper_id.lower() or key in task.title.lower():
                    return task
        return self.tasks[0]


def serve_stdio(service: DomainIntelligenceService) -> None:
    while True:
        message = _read_message(sys.stdin.buffer)
        if message is None:
            return
        response = _handle_message(service, message)
        if response is not None:
            _write_message(sys.stdout.buffer, response)


def _handle_message(
    service: DomainIntelligenceService,
    message: dict[str, Any],
) -> dict[str, Any] | None:
    method = message.get("method")
    request_id = message.get("id")
    if method == "initialize":
        return _response(
            request_id,
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "corectx-domain-intelligence", "version": "1.0.0"},
            },
        )
    if method == "notifications/initialized":
        return None
    if method == "ping":
        return _response(request_id, {})
    if method == "tools/list":
        return _response(request_id, {"tools": [_tool_schema(name) for name in TOOLS]})
    if method == "tools/call":
        params = message.get("params") or {}
        name = str(params.get("name", ""))
        arguments = params.get("arguments") or {}
        try:
            structured = service.call_tool(name, arguments)
        except Exception as exc:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32000, "message": str(exc)},
            }
        return _response(
            request_id,
            {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(structured, ensure_ascii=False, sort_keys=True),
                    }
                ],
                "structuredContent": structured,
                "isError": False,
            },
        )
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32601, "message": f"method not found: {method}"},
    }


def _read_message(stream: Any) -> dict[str, Any] | None:
    header_lines = []
    while True:
        line = stream.readline()
        if line == b"":
            return None
        if line in {b"\n", b"\r\n"}:
            break
        header_lines.append(line.decode("ascii").strip())
    content_length = 0
    for line in header_lines:
        name, _, value = line.partition(":")
        if name.lower() == "content-length":
            content_length = int(value.strip())
    if content_length <= 0:
        return None
    payload = stream.read(content_length)
    if not payload:
        return None
    return json.loads(payload.decode("utf-8"))


def _write_message(stream: Any, message: dict[str, Any]) -> None:
    payload = json.dumps(message, ensure_ascii=False).encode("utf-8")
    stream.write(f"Content-Length: {len(payload)}\r\n\r\n".encode("ascii") + payload)
    stream.flush()


def _response(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _tool_schema(name: str) -> dict[str, Any]:
    return {
        "name": name,
        "description": _tool_description(name),
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string"},
                "query": {"type": "string"},
                "paper_id": {"type": "string"},
                "title": {"type": "string"},
                "claim": {"type": "string"},
                "limit": {"type": "integer"},
            },
            "additionalProperties": True,
        },
    }


def _tool_description(name: str) -> str:
    descriptions = {
        "get_domain_context": "Return folded SSI domain context with source ids and risks.",
        "judge_paper_strength": "Judge an SSI paper's strength as domain research.",
        "critique_claim": "Critique an SSI claim using domain boundary rules.",
        "suggest_next_reading": "Suggest next SSI readings from the domain corpus.",
        "explain_judgment": "Explain the rationale behind a domain judgment.",
    }
    return descriptions[name]


def _rationale(task: DomainJudgmentTask) -> list[str]:
    return [
        f"Signal channel: {','.join(task.input_signal) or 'unknown'}.",
        f"Evaluation evidence: {_short(task.evaluation)}",
        f"Weakness: {_short(task.weakness)}",
    ]


def _strength_label(score: float) -> str:
    if score >= 4.2:
        return "strong"
    if score >= 3.2:
        return "moderate"
    return "weak"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", default="autonomous_domain_evolver")
    parser.add_argument("--domain-root")
    args = parser.parse_args()
    serve_stdio(DomainIntelligenceService(args.domain, args.domain_root))


if __name__ == "__main__":
    main()

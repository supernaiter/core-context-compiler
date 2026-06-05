#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

TOOLS = [
    "get_domain_context",
    "judge_paper_strength",
    "critique_claim",
    "suggest_next_reading",
    "explain_judgment",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True)
    parser.add_argument("--domain-root")
    args = parser.parse_args()
    command = [
        sys.executable,
        "-m",
        "corectx.mcp_domain_service",
        "--domain",
        args.domain,
    ]
    if args.domain_root:
        command.extend(["--domain-root", args.domain_root])

    src_path = str(Path(__file__).resolve().parents[1] / "src")
    env = dict(os.environ)
    env["PYTHONPATH"] = (
        src_path if not env.get("PYTHONPATH") else f"{src_path}{os.pathsep}{env['PYTHONPATH']}"
    )
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=Path(__file__).resolve().parents[1],
        env=env,
    )
    try:
        client = McpClient(process)
        initialize = client.request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "corectx-mcp-smoke", "version": "1.0.0"},
            },
        )
        client.notify("notifications/initialized", {})
        listed = client.request("tools/list", {})
        tool_names = [tool["name"] for tool in listed["tools"]]
        missing = [name for name in TOOLS if name not in tool_names]
        if missing:
            raise RuntimeError(f"missing tools: {missing}")

        calls = {}
        for name in TOOLS:
            calls[name] = client.request(
                "tools/call",
                {
                    "name": name,
                    "arguments": {
                        "domain": args.domain,
                        "query": "silent speech interface",
                        "limit": 3,
                    },
                },
            )
            structured = calls[name].get("structuredContent")
            if not isinstance(structured, dict):
                raise RuntimeError(f"{name} did not return structuredContent")
            for key in ["tool", "domain", "rationale", "risk_flags", "judgment_text"]:
                if key not in structured:
                    raise RuntimeError(f"{name} missing structured key: {key}")

        print(
            json.dumps(
                {
                    "server": initialize["serverInfo"],
                    "tools": tool_names,
                    "structured_json_tools": sorted(calls),
                    "status": "pass",
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
    finally:
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3)
        stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
        if process.returncode not in {0, -15} and stderr:
            print(stderr, file=sys.stderr)


class McpClient:
    def __init__(self, process: subprocess.Popen[bytes]) -> None:
        if process.stdin is None or process.stdout is None:
            raise RuntimeError("MCP process pipes unavailable")
        self.process = process
        self.stdin = process.stdin
        self.stdout = process.stdout
        self.next_id = 1

    def request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        request_id = self.next_id
        self.next_id += 1
        self._write({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params})
        message = self._read()
        if "error" in message:
            raise RuntimeError(message["error"]["message"])
        return message["result"]

    def notify(self, method: str, params: dict[str, Any]) -> None:
        self._write({"jsonrpc": "2.0", "method": method, "params": params})

    def _write(self, message: dict[str, Any]) -> None:
        payload = json.dumps(message, ensure_ascii=False).encode("utf-8")
        self.stdin.write(f"Content-Length: {len(payload)}\r\n\r\n".encode("ascii") + payload)
        self.stdin.flush()

    def _read(self) -> dict[str, Any]:
        header_lines = []
        while True:
            line = self.stdout.readline()
            if line == b"":
                raise RuntimeError("MCP server closed stdout")
            if line in {b"\n", b"\r\n"}:
                break
            header_lines.append(line.decode("ascii").strip())
        content_length = 0
        for line in header_lines:
            name, _, value = line.partition(":")
            if name.lower() == "content-length":
                content_length = int(value.strip())
        payload = self.stdout.read(content_length)
        return json.loads(payload.decode("utf-8"))


if __name__ == "__main__":
    main()

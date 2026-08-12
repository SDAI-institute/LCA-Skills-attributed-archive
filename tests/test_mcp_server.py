from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def exchange(messages: list[dict[str, object]]) -> tuple[list[dict[str, object]], str]:
    result = subprocess.run(
        [sys.executable, "lca_tools/mcp_server.py"],
        cwd=ROOT,
        input="".join(json.dumps(message) + "\n" for message in messages),
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )
    if result.returncode:
        raise AssertionError(result.stdout + result.stderr)
    responses = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    return responses, result.stderr


class MCPServerTests(unittest.TestCase):
    def test_initialize_tools_and_resources(self) -> None:
        responses, stderr = exchange([
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            {"jsonrpc": "2.0", "id": 3, "method": "resources/list", "params": {}},
        ])
        by_id = {item["id"]: item for item in responses}
        self.assertEqual(by_id[1]["result"]["protocolVersion"], "2025-11-25")
        tools = by_id[2]["result"]["tools"]
        self.assertEqual(len(tools), 13)
        self.assertIn("lca_doctor", {item["name"] for item in tools})
        self.assertTrue(all("annotations" in item for item in tools))
        self.assertEqual(len(by_id[3]["result"]["resources"]), 3)
        self.assertEqual(stderr, "")

    def test_tool_call_creates_and_validates_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            responses, _ = exchange([
                {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "lca_new_study", "arguments": {"slug": "mcp-demo", "title": "MCP Demo", "root": tmp}}},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "lca_validate_study", "arguments": {"study": str(Path(tmp) / "mcp-demo")}}},
            ])
            by_id = {item["id"]: item for item in responses}
            self.assertFalse(by_id[1]["result"]["isError"])
            self.assertFalse(by_id[2]["result"]["isError"])
            self.assertTrue((Path(tmp) / "mcp-demo/study-plan.md").exists())
            self.assertTrue((Path(tmp) / "mcp-demo/handoff.json").exists())

    def test_unknown_tool_returns_protocol_level_tool_error_content(self) -> None:
        responses, _ = exchange([
            {"jsonrpc": "2.0", "id": 9, "method": "tools/call", "params": {"name": "does_not_exist", "arguments": {}}},
        ])
        self.assertIn("error", responses[0])
        self.assertEqual(responses[0]["error"]["code"], -32602)


if __name__ == "__main__":
    unittest.main()

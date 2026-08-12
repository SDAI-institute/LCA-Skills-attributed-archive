from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AgentHookTests(unittest.TestCase):
    def test_specialist_agents_are_read_only_and_skill_grounded(self) -> None:
        agents = sorted((ROOT / "agents").glob("*.md"))
        self.assertEqual(len(agents), 9)
        for path in agents:
            text = path.read_text(encoding="utf-8")
            frontmatter = text.split("---", 2)[1]
            self.assertIn("disallowedTools: Write, Edit", frontmatter, path)
            self.assertIn("skills:", frontmatter, path)
            self.assertIn("read-only", text.lower(), path)
            self.assertIn("finding", text.lower(), path)

    def test_hook_is_targeted_and_nonblocking_script_exists(self) -> None:
        hooks = json.loads((ROOT / "hooks/hooks.json").read_text(encoding="utf-8"))
        rendered = json.dumps(hooks)
        self.assertIn("PostToolUse", rendered)
        self.assertIn("Write|Edit", rendered)
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/scripts/hook_validate.py", rendered)
        script = (ROOT / "scripts/hook_validate.py").read_text(encoding="utf-8")
        self.assertIn("return 0", script)
        self.assertIn("validate_active_plugin.py", script)
        self.assertTrue((ROOT / "scripts/validate_active_plugin.py").exists())

    def test_hook_executes_installed_tree_validator_without_blocking(self) -> None:
        event = {"tool_input": {"file_path": str(ROOT / "skills/lca-expert/SKILL.md")}}
        env = dict(os.environ)
        env["CLAUDE_PLUGIN_ROOT"] = str(ROOT)
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/hook_validate.py")],
            input=json.dumps(event),
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.strip(), "")

    def test_mcp_registration_uses_plugin_relative_path(self) -> None:
        mcp = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
        server = mcp["mcpServers"]["lca-tools"]
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/lca_tools/mcp_server.py", server["args"])
        self.assertEqual(server["env"]["LCA_PROJECT_ROOT"], "${CLAUDE_PROJECT_DIR}")

    def test_claude_overrides_cover_every_skill(self) -> None:
        overrides = json.loads((ROOT / "platforms/claude-code/skill-overrides.json").read_text(encoding="utf-8"))
        skills = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(set(overrides), skills)
        self.assertTrue(overrides["lca-autopilot"]["disable-model-invocation"])


if __name__ == "__main__":
    unittest.main()

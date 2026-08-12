from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / "dist/packages"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=False)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PlatformBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        result = run("scripts/build_distributions.py", "--clean")
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)

    def test_all_distributions_validate(self) -> None:
        result = run("scripts/validate_distributions.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("6 targets, 0 errors", result.stdout)

    def test_portable_uploads_have_no_claude_only_frontmatter(self) -> None:
        for target in (ROOT / "dist/chatgpt/lca-expert", ROOT / "dist/claude-ai/lca-expert"):
            for skill in [target / "SKILL.md", *(target / "references/modules").glob("*/SKILL.md")]:
                text = skill.read_text(encoding="utf-8").split("---", 2)[1]
                self.assertNotIn("argument-hint:", text, skill)
                self.assertNotIn("disable-model-invocation:", text, skill)
                self.assertNotIn("user-invocable:", text, skill)

    def test_claude_code_build_has_overlays_agents_hooks_and_mcp(self) -> None:
        root = ROOT / "dist/claude-code/lca-skills"
        skills = sorted((root / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 28)
        self.assertTrue(all("argument-hint:" in path.read_text(encoding="utf-8") for path in skills))
        autopilot = (root / "skills/lca-autopilot/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("disable-model-invocation: true", autopilot)
        self.assertEqual(len(list((root / "agents").glob("*.md"))), 9)
        self.assertTrue((root / "hooks/hooks.json").exists())
        self.assertTrue((root / ".mcp.json").exists())
        self.assertTrue((root / "scripts/hook_validate.py").exists())
        self.assertTrue((root / "scripts/validate_active_plugin.py").exists())
        validator = subprocess.run(
            [sys.executable, str(root / "scripts/validate_active_plugin.py"), str(root), "--strict"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(validator.returncode, 0, validator.stdout + validator.stderr)

    def test_standalone_installers_are_safe_and_syntactically_valid(self) -> None:
        root = ROOT / "dist/claude-standalone/lca-skills-standalone"
        ps1 = (root / "install.ps1").read_text(encoding="utf-8")
        uninstall_ps1 = (root / "uninstall.ps1").read_text(encoding="utf-8")
        self.assertIn("Remove-Item -Recurse -Force $Target", ps1)
        self.assertIn("lca-skills-install.json", ps1)
        self.assertIn("RemoveRuntime", uninstall_ps1)
        shell = shutil.which("sh")
        if shell:
            for name in ("install.sh", "uninstall.sh"):
                result = subprocess.run([shell, "-n", str(root / name)], text=True, capture_output=True, check=False)
                self.assertEqual(result.returncode, 0, result.stderr)
            with tempfile.TemporaryDirectory() as temp:
                claude_home = Path(temp) / ".claude"
                env = {**os.environ, "CLAUDE_HOME": str(claude_home)}
                installed = subprocess.run(
                    [shell, str(root / "install.sh")],
                    text=True,
                    capture_output=True,
                    check=False,
                    env=env,
                )
                self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
                self.assertEqual(len(list((claude_home / "skills").glob("*/SKILL.md"))), 28)
                self.assertEqual(len(list((claude_home / "agents").glob("*.md"))), 9)
                receipt = json.loads((claude_home / "lca-skills-install.json").read_text(encoding="utf-8"))
                self.assertEqual(receipt["version"], "0.2.0")
                removed = subprocess.run(
                    [shell, str(root / "uninstall.sh")],
                    text=True,
                    capture_output=True,
                    check=False,
                    env=env,
                )
                self.assertEqual(removed.returncode, 0, removed.stdout + removed.stderr)
                self.assertEqual(list((claude_home / "skills").glob("lca-*")), [])
                self.assertEqual(list((claude_home / "agents").glob("lca-*.md")), [])
                self.assertFalse((claude_home / "lca-skills-install.json").exists())

    def test_upload_zip_has_exactly_one_skill_root(self) -> None:
        for name in ("LCA-Skills-ChatGPT-v0.2.0.zip", "LCA-Skills-ClaudeAI-v0.2.0.zip"):
            with zipfile.ZipFile(PACKAGES / name) as archive:
                names = archive.namelist()
            self.assertTrue(names)
            self.assertEqual({item.split("/", 1)[0] for item in names}, {"lca-expert"})
            self.assertIn("lca-expert/SKILL.md", names)
            self.assertNotIn("lca-expert/skills/lca-expert/SKILL.md", names)

    def test_source_release_is_deterministic_and_safe(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            first = run("scripts/build_source_release.py", "--output", str(output), "--json")
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            payload = json.loads(first.stdout)
            archive = Path(payload["archive"])
            before = sha256(archive)
            second = run("scripts/build_source_release.py", "--output", str(output), "--json")
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            self.assertEqual(before, sha256(archive))
            with zipfile.ZipFile(archive) as bundle:
                self.assertIsNone(bundle.testzip())
                names = bundle.namelist()
                self.assertEqual({name.split("/", 1)[0] for name in names}, {"LCA-skills"})
                self.assertIn("LCA-skills/SOURCE-RELEASE.json", names)
                self.assertIn(
                    "LCA-skills/examples/synthetic-hydrogen-screening/results/release/release-manifest.json",
                    names,
                )
                self.assertFalse(any("/dist/" in name or "__pycache__" in name for name in names))

    def test_rebuild_is_byte_deterministic(self) -> None:
        before = {path.name: sha256(path) for path in PACKAGES.glob("*.zip")}
        result = run("scripts/build_distributions.py", "--clean")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        after = {path.name: sha256(path) for path in PACKAGES.glob("*.zip")}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()

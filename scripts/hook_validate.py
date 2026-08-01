#!/usr/bin/env python3
"""Safe Claude Code post-write validator.

Reads hook JSON from stdin, validates only recognized LCA Skills or study files,
prints concise feedback when useful, and always exits zero so it cannot block a
user edit. Full release gates remain explicit commands.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def nearest_study(path: Path) -> Path | None:
    current = path if path.is_dir() else path.parent
    for candidate in (current, *current.parents):
        if (candidate / "study.yaml").exists() and (candidate / "goal-and-scope.md").exists():
            return candidate
    return None


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0
    tool_input = event.get("tool_input") or {}
    raw = tool_input.get("file_path") or tool_input.get("path")
    if not raw:
        return 0
    path = Path(raw).expanduser().resolve()
    plugin_root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT", Path(__file__).resolve().parents[1])).resolve()
    command: list[str] | None = None
    cwd = plugin_root

    try:
        relative = path.relative_to(plugin_root)
        package_roots = {"skills", "agents", "hooks", "scripts", "lca_tools", ".claude-plugin", ".codex-plugin"}
        package_files = {"SKILL.md", "plugin.json", "hooks.json", ".mcp.json", "pyproject.toml"}
        if (relative.parts and relative.parts[0] in package_roots) or path.name in package_files:
            command = [sys.executable, str(plugin_root / "scripts" / "validate_active_plugin.py"), str(plugin_root), "--strict"]
    except ValueError:
        study = nearest_study(path)
        if study:
            command = [sys.executable, str(plugin_root / "scripts" / "validate_study.py"), str(study)]

    if not command:
        return 0
    try:
        proc = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=30, check=False)
    except Exception as exc:
        print(f"LCA validation hook could not run: {type(exc).__name__}: {exc}")
        return 0
    if proc.returncode != 0:
        output = (proc.stdout + proc.stderr).strip()
        print("LCA validation notice (non-blocking):")
        print(output[-5000:])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

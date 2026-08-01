#!/usr/bin/env python3
"""Lightweight validation for an installed LCA Skills plugin or standalone tree.

Unlike the source-repository validator, this script accepts generated host
packages that intentionally omit development-only files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESOURCE_RE = re.compile(r"\b(?:references|scripts|assets)/[A-Za-z0-9_./-]+\.(?:md|py|json|csv|yaml|yml)\b")
PORTABLE_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
CLAUDE_FIELDS = {
    "argument-hint",
    "disable-model-invocation",
    "user-invocable",
    "context",
    "agent",
    "model",
}


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "\n".join(lines)
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, "\n".join(lines)
    data: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"\'')
    return data, "\n".join(lines[end + 1 :])


def resolve(skill_file: Path, root: Path, raw: str) -> Path | None:
    local = skill_file.parent / raw
    if local.exists():
        return local
    root_relative = root / raw
    if root_relative.exists():
        return root_relative
    for parent in skill_file.parents:
        if parent == root.parent:
            break
        candidate = parent / raw
        if candidate.exists():
            return candidate
    return None


def validate(root: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    root = root.expanduser().resolve()

    if (root / "skills").is_dir():
        skill_files = sorted((root / "skills").glob("*/SKILL.md"))
        expected = 28
    elif (root / "SKILL.md").is_file():
        skill_files = [root / "SKILL.md", *sorted((root / "references/modules").glob("*/SKILL.md"))]
        expected = 28
    else:
        return {
            "schema_version": "1.0",
            "root": str(root),
            "ok": False,
            "errors": ["No skills/ tree or top-level SKILL.md found"],
            "warnings": [],
        }

    if len(skill_files) != expected:
        errors.append(f"Expected {expected} skill files; found {len(skill_files)}")

    frontmatters = {path: parse_frontmatter(path)[0] for path in skill_files}
    claude_field_usage = [bool(set(metadata).intersection(CLAUDE_FIELDS)) for metadata in frontmatters.values()]
    claude_mode = bool(claude_field_usage and any(claude_field_usage))
    consolidated = (root / "SKILL.md").is_file()
    if consolidated and claude_mode:
        errors.append("Consolidated ChatGPT/Claude.ai skill must not contain Claude Code-only frontmatter")
    if claude_mode and not all(metadata.get("argument-hint") for metadata in frontmatters.values()):
        errors.append("Claude overlay is incomplete: every skill must include argument-hint")

    names: set[str] = set()
    for path in skill_files:
        metadata = frontmatters[path]
        _, body = parse_frontmatter(path)
        name = metadata.get("name", "")
        rel = path.relative_to(root).as_posix()
        if not name or not NAME_RE.fullmatch(name):
            errors.append(f"{rel}: invalid or missing skill name")
        elif name in names:
            errors.append(f"{rel}: duplicate skill name {name!r}")
        names.add(name)
        if not metadata.get("description"):
            errors.append(f"{rel}: missing description")
        unknown = set(metadata).difference(PORTABLE_FIELDS | CLAUDE_FIELDS)
        if unknown:
            errors.append(f"{rel}: unsupported frontmatter: {', '.join(sorted(unknown))}")
        if not claude_mode and set(metadata).intersection(CLAUDE_FIELDS):
            errors.append(f"{rel}: Claude-only frontmatter is not permitted in this package")
        for raw in sorted(set(RESOURCE_RE.findall(body))):
            if resolve(path, root, raw) is None:
                errors.append(f"{rel}: unresolved resource {raw}")

    if claude_mode:
        autopilot = next((path for path, metadata in frontmatters.items() if metadata.get("name") == "lca-autopilot"), None)
        if autopilot is None:
            errors.append("Claude package is missing lca-autopilot")
        elif frontmatters[autopilot].get("disable-model-invocation") != "true":
            errors.append("lca-autopilot must be explicit-only with disable-model-invocation: true")

    agents = root / "agents"
    if agents.is_dir():
        agent_files = sorted(agents.glob("*.md"))
        if len(agent_files) != 9:
            errors.append(f"Expected 9 agents; found {len(agent_files)}")
        for path in agent_files:
            metadata, body = parse_frontmatter(path)
            if metadata.get("name") != path.stem:
                errors.append(f"{path.relative_to(root)}: agent name does not match filename")
            disallowed = metadata.get("disallowedTools", "")
            if "Write" not in disallowed or "Edit" not in disallowed:
                errors.append(f"{path.relative_to(root)}: review agent must disallow Write and Edit")
            if "read-only" not in body.lower():
                warnings.append(f"{path.relative_to(root)}: read-only contract not found in body")

    for rel in (".mcp.json", "hooks/hooks.json", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
        path = root / rel
        if path.exists():
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"{rel}: invalid JSON: {exc}")

    hook = root / "hooks/hooks.json"
    if hook.exists():
        text = hook.read_text(encoding="utf-8")
        if "hook_validate.py" not in text or not (root / "scripts/hook_validate.py").exists():
            errors.append("Hook references a missing scripts/hook_validate.py")
        if not (root / "scripts/validate_active_plugin.py").exists():
            errors.append("Installed plugin validator is missing")

    mcp = root / ".mcp.json"
    if mcp.exists() and not (root / "lca_tools/mcp_server.py").exists():
        errors.append("MCP manifest exists but lca_tools/mcp_server.py is missing")

    return {
        "schema_version": "1.0",
        "root": str(root),
        "ok": not errors,
        "package_mode": "consolidated-portable" if consolidated else ("claude" if claude_mode else "portable"),
        "skill_count": len(skill_files),
        "agent_count": len(list(agents.glob("*.md"))) if agents.is_dir() else 0,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = validate(Path(args.root))
    print(json.dumps(payload, indent=2))
    return 0 if payload["ok"] and not (args.strict and payload["warnings"]) else 1


if __name__ == "__main__":
    sys.exit(main())

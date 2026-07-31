#!/usr/bin/env python3
"""Validate source portability, plugin overlays, runtime contracts, and repository hygiene."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from repo_checks import find_broken_markdown_links

ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESOURCE_RE = re.compile(r"(?:\]\(|`)(?P<path>(?:references|scripts|assets)/[A-Za-z0-9_./-]+)(?:\)|`)")
PORTABLE_SKILL_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
CLAUDE_ONLY_FIELDS = {
    "argument-hint",
    "disable-model-invocation",
    "user-invocable",
    "context",
    "agent",
    "model",
}
OVERLAY_FIELDS = CLAUDE_ONLY_FIELDS | {"allowed-tools"}
GENERATED_PARTS = {".git", ".venv", "__pycache__", "dist", "build", "release"}
REQUIRED_ROOT = (
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "LICENSE",
    "plugin.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
    ".mcp.json",
    "hooks/hooks.json",
    "platforms/claude-code/skill-overrides.json",
    "docs/architecture.md",
    "docs/compound-workflow.md",
    "docs/runtime-adapters.md",
    "docs/skill-catalog.md",
    "docs/evals.md",
    "docs/source-register.md",
    "docs/platforms/claude-code.md",
    "docs/platforms/claude-ai.md",
    "docs/platforms/chatgpt.md",
    "docs/platforms/codex.md",
    "docs/platforms/host-qualification.md",
    "docs/research/README.md",
    "docs/research/11-current-version-notes-2026-08.md",
    "docs/tool-integration-test-plan.md",
    "assets/templates/study.yaml",
    "assets/templates/intake-brief.md",
    "assets/templates/study-plan.md",
    "assets/templates/handoff.json",
    "scripts/new_study.py",
    "scripts/validate_study.py",
    "scripts/run_reference_lca.py",
    "scripts/build_distributions.py",
    "scripts/build_source_release.py",
    "scripts/validate_distributions.py",
    "scripts/host_qualification.py",
    "scripts/hook_validate.py",
    "scripts/validate_active_plugin.py",
    "scripts/check_markdown_links.py",
    "scripts/repo_checks.py",
    "lca_tools/cli.py",
    "lca_tools/mcp_server.py",
    "tests/integration/fixtures/synthetic-matrix/expected-results.csv",
)


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, [], lines
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, lines[1:], []

    fm_lines = lines[1:end]
    data: dict[str, str] = {}
    for line in fm_lines:
        if not line.strip() or line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"\'')
    return data, fm_lines, lines[end + 1 :]


def yaml_list(fm_lines: list[str], key: str) -> list[str]:
    result: list[str] = []
    active = False
    base_indent = 0
    for line in fm_lines:
        if not active:
            if re.fullmatch(rf"\s*{re.escape(key)}\s*:\s*", line):
                active = True
                base_indent = len(line) - len(line.lstrip())
            continue
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        if indent <= base_indent and not line.lstrip().startswith("-"):
            break
        match = re.match(r"\s*-\s*(.+?)\s*$", line)
        if match:
            result.append(match.group(1).strip('"\''))
        elif indent <= base_indent:
            break
    return result


def add_error(errors: list[str], path: Path | str, message: str) -> None:
    errors.append(f"ERROR {path}: {message}")


def add_warning(warnings: list[str], path: Path | str, message: str) -> None:
    warnings.append(f"WARN  {path}: {message}")


def excluded(path: Path) -> bool:
    try:
        parts = path.relative_to(ROOT).parts
    except ValueError:
        parts = path.parts
    return bool(GENERATED_PARTS.intersection(parts))


def load_json(path: Path, errors: list[str]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - aggregate validator diagnostics
        add_error(errors, path.relative_to(ROOT), f"invalid JSON: {exc}")
        return None


def validate_json_files(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.json")):
        if excluded(path):
            continue
        load_json(path, errors)


def manifest_versions(errors: list[str]) -> dict[str, str]:
    paths = (
        ROOT / "plugin.json",
        ROOT / ".claude-plugin/plugin.json",
        ROOT / ".codex-plugin/plugin.json",
        ROOT / ".cursor-plugin/plugin.json",
    )
    versions: dict[str, str] = {}
    for path in paths:
        if not path.exists():
            continue
        value = load_json(path, errors)
        if isinstance(value, dict) and value.get("version"):
            versions[str(path.relative_to(ROOT))] = str(value["version"])
    marketplace = ROOT / ".claude-plugin/marketplace.json"
    if marketplace.exists():
        data = load_json(marketplace, errors)
        if isinstance(data, dict):
            for index, plugin in enumerate(data.get("plugins", [])):
                if isinstance(plugin, dict) and plugin.get("name") == "lca-skills":
                    versions[f".claude-plugin/marketplace.json#plugins[{index}]"] = str(plugin.get("version", ""))
    return versions


def validate_versions(errors: list[str]) -> str:
    versions = manifest_versions(errors)
    if not versions:
        add_error(errors, "manifests", "no versioned manifests found")
        return ""
    unique = {value for value in versions.values() if value}
    if len(unique) != 1 or any(not value for value in versions.values()):
        add_error(errors, "manifests", f"version mismatch: {versions}")
        return next(iter(unique), "")
    version = next(iter(unique))

    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8") if (ROOT / "pyproject.toml").exists() else ""
    if not re.search(rf"(?m)^version\s*=\s*[\"']{re.escape(version)}[\"']\s*$", pyproject):
        add_error(errors, "pyproject.toml", f"project version does not match manifests ({version})")
    init_text = (ROOT / "lca_tools/__init__.py").read_text(encoding="utf-8") if (ROOT / "lca_tools/__init__.py").exists() else ""
    if not re.search(rf"__version__\s*=\s*[\"']{re.escape(version)}[\"']", init_text):
        add_error(errors, "lca_tools/__init__.py", f"runtime version does not match manifests ({version})")
    return version


def validate_skills(errors: list[str], warnings: list[str], version: str) -> tuple[int, int, set[str]]:
    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if not skill_files:
        add_error(errors, "skills", "no skills/*/SKILL.md files found")
        return 0, 0, set()

    names: set[str] = set()
    referenced: set[Path] = set()
    for skill_file in skill_files:
        rel = skill_file.relative_to(ROOT)
        metadata, fm_lines, body_lines = parse_frontmatter(skill_file)
        name = metadata.get("name", "")
        description = metadata.get("description", "")

        unknown = set(metadata).difference(PORTABLE_SKILL_FIELDS)
        if unknown:
            add_error(errors, rel, f"canonical skill contains non-portable frontmatter: {', '.join(sorted(unknown))}")
        leaked = set(metadata).intersection(CLAUDE_ONLY_FIELDS)
        if leaked:
            add_error(errors, rel, f"Claude-only fields belong in platform overlay: {', '.join(sorted(leaked))}")

        if not name:
            add_error(errors, rel, "missing frontmatter name")
        elif not NAME_RE.fullmatch(name):
            add_error(errors, rel, "name must contain lowercase letters, digits, and internal hyphens only")
        elif len(name) > 64:
            add_error(errors, rel, "name exceeds 64 characters")
        elif name != skill_file.parent.name:
            add_error(errors, rel, f"name '{name}' does not match directory '{skill_file.parent.name}'")
        elif name in names:
            add_error(errors, rel, f"duplicate skill name '{name}'")
        names.add(name)

        if not description:
            add_error(errors, rel, "missing frontmatter description")
        elif len(description) > 1024:
            add_error(errors, rel, "description exceeds 1024 characters")
        elif "use" not in description.lower():
            add_warning(warnings, rel, "description should state when to use the skill")
        if metadata.get("license") != "MIT":
            add_error(errors, rel, "canonical skill license must be MIT")
        if not metadata.get("compatibility"):
            add_error(errors, rel, "missing portability/compatibility statement")
        if "metadata" not in metadata:
            add_error(errors, rel, "missing metadata block")
        fm_text = "\n".join(fm_lines)
        if version and not re.search(rf"(?m)^\s+version:\s*[\"']{re.escape(version)}[\"']\s*$", fm_text):
            add_error(errors, rel, f"metadata version does not match {version}")

        total_lines = len(skill_file.read_text(encoding="utf-8").splitlines())
        if total_lines > 500:
            add_error(errors, rel, f"SKILL.md has {total_lines} lines; progressive-disclosure target is <= 500")
        elif total_lines > 350:
            add_warning(warnings, rel, f"SKILL.md has {total_lines} lines; consider moving detail to references")

        text = "\n".join(body_lines)
        for match in RESOURCE_RE.finditer(text):
            raw = match.group("path")
            local = skill_file.parent / raw
            resource = local if local.exists() else ROOT / raw
            if raw.startswith("references/"):
                referenced.add(local.resolve())
            if not resource.exists():
                add_error(errors, rel, f"referenced resource does not exist: {raw}")
        for raw in re.findall(r"\b(?:references|scripts|assets)/[A-Za-z0-9_./-]+\.(?:md|py|json|csv|yaml|yml)\b", text):
            local = skill_file.parent / raw
            resource = local if local.exists() else ROOT / raw
            if raw.startswith("references/"):
                referenced.add(local.resolve())
            if not resource.exists():
                add_error(errors, rel, f"referenced resource does not exist: {raw}")
        if not any(line.startswith("# ") for line in body_lines):
            add_warning(warnings, rel, "body has no level-one heading")

    reference_files = sorted((ROOT / "skills").glob("*/references/**/*.md"))
    for path in reference_files:
        if path.resolve() not in referenced:
            add_warning(warnings, path.relative_to(ROOT), "reference is not explicitly routed from its SKILL.md")
        if len(path.read_text(encoding="utf-8").splitlines()) > 500:
            add_warning(warnings, path.relative_to(ROOT), "reference exceeds 500 lines; consider splitting")

    return len(skill_files), len(reference_files), names


def validate_agents(errors: list[str], warnings: list[str], skills: set[str]) -> int:
    agents = sorted((ROOT / "agents").glob("*.md"))
    if len(agents) < 8:
        add_error(errors, "agents", f"expected at least 8 specialist agents; found {len(agents)}")
    names: set[str] = set()
    for path in agents:
        rel = path.relative_to(ROOT)
        metadata, fm_lines, body_lines = parse_frontmatter(path)
        name = metadata.get("name", "")
        if not name or name != path.stem or not NAME_RE.fullmatch(name):
            add_error(errors, rel, "agent name must match its lowercase hyphenated filename")
        if name in names:
            add_error(errors, rel, f"duplicate agent name '{name}'")
        names.add(name)
        if not metadata.get("description"):
            add_error(errors, rel, "agent description is required")
        if metadata.get("model") != "inherit":
            add_warning(warnings, rel, "reviewer should normally inherit the selected model")
        disallowed = {item.strip() for item in metadata.get("disallowedTools", "").split(",") if item.strip()}
        if not {"Write", "Edit"}.issubset(disallowed):
            add_error(errors, rel, "review agents must disallow Write and Edit")
        preload = yaml_list(fm_lines, "skills")
        if not preload:
            add_warning(warnings, rel, "agent has no preloaded LCA skills")
        for item in preload:
            if item not in skills:
                add_error(errors, rel, f"preloaded skill does not exist: {item}")
        body = "\n".join(body_lines).lower()
        if "read-only" not in body or "finding" not in body:
            add_warning(warnings, rel, "agent body should state read-only and finding contracts")
    return len(agents)


def validate_platform_overlay(errors: list[str], skills: set[str]) -> None:
    path = ROOT / "platforms/claude-code/skill-overrides.json"
    data = load_json(path, errors)
    if not isinstance(data, dict):
        return
    keys = set(data)
    missing = skills.difference(keys)
    extra = keys.difference(skills)
    if missing:
        add_error(errors, path.relative_to(ROOT), f"missing skill overrides: {', '.join(sorted(missing))}")
    if extra:
        add_error(errors, path.relative_to(ROOT), f"unknown skill overrides: {', '.join(sorted(extra))}")
    for name, override in data.items():
        if not isinstance(override, dict):
            add_error(errors, path.relative_to(ROOT), f"override for {name} must be an object")
            continue
        unknown = set(override).difference(OVERLAY_FIELDS)
        if unknown:
            add_error(errors, path.relative_to(ROOT), f"unsupported Claude fields for {name}: {', '.join(sorted(unknown))}")
        if not override.get("argument-hint"):
            add_error(errors, path.relative_to(ROOT), f"{name} has no argument-hint")
    if data.get("lca-autopilot", {}).get("disable-model-invocation") is not True:
        add_error(errors, path.relative_to(ROOT), "lca-autopilot must require explicit user invocation in Claude Code")


def validate_hooks_and_mcp(errors: list[str]) -> None:
    hooks_path = ROOT / "hooks/hooks.json"
    hooks = load_json(hooks_path, errors)
    if isinstance(hooks, dict):
        post = hooks.get("hooks", {}).get("PostToolUse", []) if isinstance(hooks.get("hooks"), dict) else []
        rendered = json.dumps(post)
        if "Write|Edit" not in rendered or "hook_validate.py" not in rendered:
            add_error(errors, hooks_path.relative_to(ROOT), "PostToolUse Write/Edit validation hook is missing")
        if "${CLAUDE_PLUGIN_ROOT}" not in rendered:
            add_error(errors, hooks_path.relative_to(ROOT), "hook must resolve paths through CLAUDE_PLUGIN_ROOT")

    mcp_path = ROOT / ".mcp.json"
    mcp = load_json(mcp_path, errors)
    if isinstance(mcp, dict):
        server = mcp.get("mcpServers", {}).get("lca-tools") if isinstance(mcp.get("mcpServers"), dict) else None
        if not isinstance(server, dict):
            add_error(errors, mcp_path.relative_to(ROOT), "lca-tools MCP server entry is missing")
        else:
            rendered = json.dumps(server)
            if "lca_tools/mcp_server.py" not in rendered:
                add_error(errors, mcp_path.relative_to(ROOT), "MCP entry does not start the bundled server")
            if "${CLAUDE_PLUGIN_ROOT}" not in rendered:
                add_error(errors, mcp_path.relative_to(ROOT), "MCP entry must use CLAUDE_PLUGIN_ROOT")


def validate_markdown_links(errors: list[str]) -> int:
    checked, broken = find_broken_markdown_links(ROOT)
    for item in broken:
        add_error(errors, item.source.relative_to(ROOT), f"broken local Markdown link on line {item.line}: {item.target}")
    return checked


def validate_repository_hygiene(errors: list[str], warnings: list[str]) -> None:
    prohibited_suffixes = {".zolca", ".spold", ".spold2", ".xlsm", ".sqlite", ".db"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or excluded(path):
            continue
        if path.suffix.lower() in prohibited_suffixes:
            add_error(errors, path.relative_to(ROOT), "proprietary/licensed model or database file must not be committed")
        if path.name in {".env", "credentials.json", "secrets.json"}:
            add_error(errors, path.relative_to(ROOT), "credential-bearing file must not be committed")

    source_register = ROOT / "docs/source-register.md"
    if source_register.exists():
        text = source_register.read_text(encoding="utf-8")
        if "2026-08-07" not in text:
            add_warning(warnings, source_register.relative_to(ROOT), "source status date is missing or unexpected")
        if "ISO 14025:2026" not in text:
            add_error(errors, source_register.relative_to(ROOT), "current ISO 14025:2026 status is not recorded")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED_ROOT:
        if not (ROOT / rel).exists():
            add_error(errors, rel, "required repository file is missing")

    validate_json_files(errors)
    version = validate_versions(errors)
    skill_count, reference_count, skills = validate_skills(errors, warnings, version)
    agent_count = validate_agents(errors, warnings, skills)
    validate_platform_overlay(errors, skills)
    validate_hooks_and_mcp(errors)
    markdown_link_count = validate_markdown_links(errors)
    validate_repository_hygiene(errors, warnings)

    for message in errors + warnings:
        print(message)
    print(
        f"Validated {skill_count} portable skills, {reference_count} routed references, "
        f"{agent_count} Claude Code agents, {markdown_link_count} local Markdown links, "
        f"{len(errors)} errors, and {len(warnings)} warnings."
    )

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

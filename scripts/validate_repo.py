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

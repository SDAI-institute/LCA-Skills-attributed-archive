#!/usr/bin/env python3
"""Build deterministic, host-specific LCA Skills distributions from the portable source."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import stat
import sys
import zipfile
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SKILLS = ROOT / "skills"
OVERLAYS = ROOT / "platforms/claude-code/skill-overrides.json"
FIXED_ZIP_TIME = (2020, 1, 1, 0, 0, 0)
RUNTIME_SCRIPTS = (
    "new_study.py",
    "validate_study.py",
    "check_balance.py",
    "check_claims.py",
    "compare_results.py",
    "hash_manifest.py",
    "run_reference_lca.py",
    "hook_validate.py",
    "validate_active_plugin.py",
)
COMMON_DOCS = (
    "source-register.md",
    "architecture.md",
    "compound-workflow.md",
    "runtime-adapters.md",
    "tool-integration-test-plan.md",
    "evals.md",
    "skill-catalog.md",
    "platforms/host-qualification.md",
    "platforms/claude-code.md",
    "platforms/claude-ai.md",
    "platforms/chatgpt.md",
    "platforms/codex.md",
)
EXCLUDED_NAMES = {"__pycache__", ".DS_Store", "Thumbs.db"}


def source_version() -> str:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'(?m)^version\s*=\s*"([^"]+)"\s*$', text)
    if not match:
        raise RuntimeError("Cannot determine version from pyproject.toml")
    return match.group(1)



def release_date(version: str) -> str:
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(rf"(?m)^## \[{re.escape(version)}\] - (\d{{4}}-\d{{2}}-\d{{2}})\s*$", text)
    if not match:
        raise RuntimeError(f"Cannot determine release date for {version} from CHANGELOG.md")
    return match.group(1)


def remove_tree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def ignore_copy(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in EXCLUDED_NAMES or name.endswith((".pyc", ".pyo"))}


def copy_tree(source: Path, target: Path) -> None:
    shutil.copytree(source, target, dirs_exist_ok=True, ignore=ignore_copy)


def common_runtime(target: Path, *, include_docs: bool = True, include_examples: bool = True) -> None:
    copy_tree(ROOT / "lca_tools", target / "lca_tools")
    copy_tree(ROOT / "assets", target / "assets")
    (target / "scripts").mkdir(parents=True, exist_ok=True)
    for name in RUNTIME_SCRIPTS:
        copy_file(ROOT / "scripts" / name, target / "scripts" / name)
    for name in ("LICENSE", "pyproject.toml"):
        copy_file(ROOT / name, target / name)
    if include_docs:
        (target / "docs").mkdir(parents=True, exist_ok=True)
        for name in COMMON_DOCS:
            if (ROOT / "docs" / name).exists():
                copy_file(ROOT / "docs" / name, target / "docs" / name)
    if include_examples:
        copy_tree(ROOT / "examples/synthetic-hydrogen-screening", target / "examples/synthetic-hydrogen-screening")


def split_frontmatter(text: str) -> tuple[list[str], list[str]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md has no YAML frontmatter")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise ValueError("SKILL.md frontmatter is not closed") from exc
    return lines[: end + 1], lines[end + 1 :]


def with_claude_overlay(text: str, override: dict[str, object]) -> str:
    frontmatter, body = split_frontmatter(text)
    closing = frontmatter.pop()
    for key, value in override.items():
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        elif isinstance(value, (str, int, float)):
            rendered = json.dumps(value, ensure_ascii=False) if isinstance(value, str) else str(value)
        else:
            raise TypeError(f"Unsupported Claude overlay value for {key}: {type(value).__name__}")
        frontmatter.append(f"{key}: {rendered}")
    frontmatter.append(closing)
    return "\n".join(frontmatter + body) + "\n"


def copy_skills(target: Path, *, claude_overlay: bool = False) -> None:
    overlays = json.loads(OVERLAYS.read_text(encoding="utf-8")) if claude_overlay else {}
    for source in sorted(SKILLS.iterdir()):
        if not source.is_dir() or not (source / "SKILL.md").exists():
            continue
        destination = target / source.name
        copy_tree(source, destination)
        if claude_overlay:
            skill_file = destination / "SKILL.md"
            skill_file.write_text(
                with_claude_overlay(skill_file.read_text(encoding="utf-8"), overlays[source.name]),
                encoding="utf-8",
            )


def insert_after_heading(text: str, heading: str, insertion: str) -> str:
    marker = heading + "\n"
    if marker not in text:
        raise ValueError(f"Heading not found: {heading}")
    return text.replace(marker, marker + "\n" + insertion.strip() + "\n\n", 1)


def consolidated_mode_note(host: str) -> str:
    invocation = {
        "chatgpt": "ChatGPT normally selects this installed skill automatically; no Claude-style slash command is assumed.",
        "claude-ai": "Claude.ai normally selects this installed skill from the conversation context; no Claude Code slash command is assumed.",
    }[host]
    return f"""## Bundled single-skill mode

This is the **{host} upload build**. It packages the complete LCA system inside one Agent Skill because this host imports one skill directory at a time. {invocation}

When this file routes to `lca-scope`, `lca-inventory`, or another module, do not assume a host-native nested skill is installed. Read and follow `references/modules/<module-name>/SKILL.md`; resolve that module's relative references from its own directory. Use host-native skill invocation only when the named module is independently installed.

Resolve bundled scripts and templates from this skill directory rather than the conversation working directory. Local openLCA, Brightway, GREET, filesystem, and MCP access remain unavailable unless the host explicitly supplies those tools or connections. Never simulate a successful external-tool run."""


def upload_readme(host: str, version: str) -> str:
    label = "ChatGPT" if host == "chatgpt" else "Claude.ai"
    return f"""# LCA Expert for {label}

Version {version}. This directory is a single portable Agent Skill containing the LCA orchestrator, all specialist modules, references, templates, and deterministic Python utilities.

## Install

Upload the enclosing ZIP through the host's skill upload interface. The archive contains exactly one top-level `lca-expert/` directory with `SKILL.md` at its root.

## Invocation

{label} should activate the skill automatically for life-cycle-assessment work. Ask explicitly to use **LCA Expert** when testing activation. This package does not promise Claude Code-style slash commands.

## Tool limits

The uploaded knowledge and deterministic utilities work without licensed databases. openLCA, Brightway, GREET, standards, PCRs, and commercial databases require lawful access and an execution environment supplied by the host. A packaged adapter is not proof that the host can reach software on your local computer.

## Qualification

The build pipeline validates directory structure, portable frontmatter, references, hashes, and ZIP integrity. Actual upload and invocation must be tested in the target account and is recorded separately from structural qualification.
"""


def build_consolidated(host: str, base: Path, version: str) -> Path:
    package = base / "lca-expert"
    package.mkdir(parents=True, exist_ok=True)
    source_expert = SKILLS / "lca-expert"
    copy_tree(source_expert, package)
    root_skill = package / "SKILL.md"
    text = root_skill.read_text(encoding="utf-8")
    text = insert_after_heading(text, "# LCA Expert Orchestrator", consolidated_mode_note(host))
    root_skill.write_text(text, encoding="utf-8")

    modules = package / "references/modules"
    for source in sorted(SKILLS.iterdir()):
        if not source.is_dir() or source.name == "lca-expert" or not (source / "SKILL.md").exists():
            continue
        copy_tree(source, modules / source.name)

    # Replace repository-development diagnostics with checks valid inside an uploaded single-skill bundle.
    doctor_ref = modules / "lca-doctor/references/host-commands.md"
    if doctor_ref.exists():
        doctor_ref.write_text(
            """# Host commands for the consolidated upload

Use only commands that the active host explicitly permits. Resolve `<skill-root>` to the directory containing the top-level `SKILL.md`.

```bash
python <skill-root>/scripts/run_reference_lca.py --json
python <skill-root>/scripts/new_study.py demo-study --root <writable-directory>
python <skill-root>/scripts/validate_study.py <writable-directory>/demo-study
```

Repository build validators, Claude plugin hooks, local MCP registration, and host CLI probes are not part of the single-skill upload. Treat local openLCA, Brightway, and GREET as NOT TESTED unless the host exposes them and a representative known-case run succeeds.
""",
            encoding="utf-8",
        )

    setup_skill = modules / "lca-setup/SKILL.md"
    if setup_skill.exists():
        setup_text = setup_skill.read_text(encoding="utf-8")
        setup_text += (
            "\n## Consolidated upload path rule\n\n"
            "In a single-skill upload, resolve `scripts/new_study.py`, `scripts/validate_study.py`, and `assets/templates/` from the top-level `lca-expert` skill directory. Do not assume the process working directory is the skill directory.\n"
        )
        setup_skill.write_text(setup_text, encoding="utf-8")

    common_runtime(package, include_docs=True, include_examples=False)
    (package / "README.md").write_text(upload_readme(host, version), encoding="utf-8")
    write_package_manifest(package, target=host, version=version, qualification="structural")
    return package


def standalone_installers(target: Path, version: str) -> None:
    ps1 = r'''param(
  [string]$ClaudeHome = (Join-Path $HOME ".claude"),
  [switch]$InstallRuntime
)
$ErrorActionPreference = "Stop"
$SkillSource = Join-Path $PSScriptRoot "skills"
$SkillDestination = Join-Path $ClaudeHome "skills"
$AgentSource = Join-Path $PSScriptRoot "agents"
$AgentDestination = Join-Path $ClaudeHome "agents"
New-Item -ItemType Directory -Force -Path $SkillDestination, $AgentDestination | Out-Null
Get-ChildItem -Directory $SkillSource | ForEach-Object {
  $Target = Join-Path $SkillDestination $_.Name
  if (Test-Path $Target) { Remove-Item -Recurse -Force $Target }
  Copy-Item -Recurse -Force $_.FullName $Target
}
Get-ChildItem -File $AgentSource | ForEach-Object {
  $Target = Join-Path $AgentDestination $_.Name
  if (Test-Path $Target) { Remove-Item -Force $Target }
  Copy-Item -Force $_.FullName $Target
}
$Receipt = [ordered]@{
  package = "lca-skills"
  version = "__VERSION__"
  installed_at_utc = [DateTime]::UtcNow.ToString("o")
  claude_home = $ClaudeHome
  skills = @(Get-ChildItem -Directory $SkillSource | ForEach-Object { $_.Name })
  agents = @(Get-ChildItem -File $AgentSource | ForEach-Object { $_.Name })
  runtime_requested = [bool]$InstallRuntime
}
$Receipt | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 (Join-Path $ClaudeHome "lca-skills-install.json")
if ($InstallRuntime) {
  python -m pip install --user $PSScriptRoot
}
Write-Host "Installed LCA skills in $SkillDestination"
Write-Host "Receipt: $(Join-Path $ClaudeHome 'lca-skills-install.json')"
Write-Host "Restart Claude Code, then invoke /lca-expert or /lca-autopilot."
Write-Host "The plugin distribution is required for automatic hooks and bundled MCP registration."
'''.replace("__VERSION__", version)
    sh = r'''#!/usr/bin/env sh
set -eu
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
mkdir -p "$CLAUDE_HOME/skills" "$CLAUDE_HOME/agents"
for skill in "$HERE"/skills/*; do
  [ -d "$skill" ] || continue
  rm -rf "$CLAUDE_HOME/skills/$(basename "$skill")"
  cp -R "$skill" "$CLAUDE_HOME/skills/"
done
for agent in "$HERE"/agents/*.md; do
  [ -f "$agent" ] || continue
  rm -f "$CLAUDE_HOME/agents/$(basename "$agent")"
  cp "$agent" "$CLAUDE_HOME/agents/"
done
INSTALL_RUNTIME=false
if [ "${1:-}" = "--install-runtime" ]; then
  INSTALL_RUNTIME=true
  python -m pip install --user "$HERE"
fi
python - "$CLAUDE_HOME" "$HERE" "$INSTALL_RUNTIME" "__VERSION__" <<'PY_RECEIPT'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
claude_home, here, runtime_requested, version = sys.argv[1:]
here_path = Path(here)
payload = {
    "package": "lca-skills",
    "version": version,
    "installed_at_utc": datetime.now(timezone.utc).isoformat(),
    "claude_home": claude_home,
    "skills": sorted(path.name for path in (here_path / "skills").iterdir() if path.is_dir()),
    "agents": sorted(path.name for path in (here_path / "agents").glob("*.md")),
    "runtime_requested": runtime_requested.lower() == "true",
}
Path(claude_home, "lca-skills-install.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
PY_RECEIPT
printf '%s\n' "Installed LCA skills in $CLAUDE_HOME/skills"
printf '%s\n' "Receipt: $CLAUDE_HOME/lca-skills-install.json"
printf '%s\n' "Restart Claude Code, then invoke /lca-expert or /lca-autopilot."
printf '%s\n' "Use the plugin distribution for automatic hooks and bundled MCP registration."
'''.replace("__VERSION__", version)
    uninstall_ps1 = r'''param(
  [string]$ClaudeHome = (Join-Path $HOME ".claude"),
  [switch]$RemoveRuntime
)
$ErrorActionPreference = "Stop"
$SkillSource = Join-Path $PSScriptRoot "skills"
$AgentSource = Join-Path $PSScriptRoot "agents"
$SkillDestination = Join-Path $ClaudeHome "skills"
$AgentDestination = Join-Path $ClaudeHome "agents"
Get-ChildItem -Directory $SkillSource | ForEach-Object {
  $Target = Join-Path $SkillDestination $_.Name
  if (Test-Path $Target) { Remove-Item -Recurse -Force $Target }
}
Get-ChildItem -File $AgentSource | ForEach-Object {
  $Target = Join-Path $AgentDestination $_.Name
  if (Test-Path $Target) { Remove-Item -Force $Target }
}
$Receipt = Join-Path $ClaudeHome "lca-skills-install.json"
if (Test-Path $Receipt) { Remove-Item -Force $Receipt }
if ($RemoveRuntime) {
  python -m pip uninstall -y lca-skills
}
Write-Host "Removed only LCA Skills entries listed by this package from $ClaudeHome"
'''
    uninstall_sh = r'''#!/usr/bin/env sh
set -eu
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
for skill in "$HERE"/skills/*; do
  [ -d "$skill" ] || continue
  rm -rf "$CLAUDE_HOME/skills/$(basename "$skill")"
done
for agent in "$HERE"/agents/*.md; do
  [ -f "$agent" ] || continue
  rm -f "$CLAUDE_HOME/agents/$(basename "$agent")"
done
rm -f "$CLAUDE_HOME/lca-skills-install.json"
if [ "${1:-}" = "--remove-runtime" ]; then
  python -m pip uninstall -y lca-skills
fi
printf '%s\n' "Removed only LCA Skills entries listed by this package from $CLAUDE_HOME"
'''
    for name, content in (
        ("install.ps1", ps1),
        ("install.sh", sh),
        ("uninstall.ps1", uninstall_ps1),
        ("uninstall.sh", uninstall_sh),
    ):
        path = target / name
        path.write_text(content, encoding="utf-8")
        if name.endswith(".sh"):
            path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    (target / "README.md").write_text(
        f"""# Standalone Claude Code LCA Skills

Version {version}. This build installs each skill under `~/.claude/skills`, so commands are unnamespaced: `/lca-expert`, `/lca-scope`, and `/lca-autopilot`.

Run `./install.sh` on macOS/Linux or `./install.ps1` in PowerShell. Add `--install-runtime` or `-InstallRuntime` only when you also want the local `lca-skills` CLI. Installation writes `~/.claude/lca-skills-install.json` as a receipt.

Use `./uninstall.sh` or `./uninstall.ps1` to remove only the LCA skill and agent names shipped by this package. Add `--remove-runtime` or `-RemoveRuntime` only to uninstall the optional Python package too.

The Claude Code **plugin** build is preferable when you need namespaced commands, specialist agents, hooks, and automatic MCP registration. The standalone installer copies skills and read-only agents only; it intentionally does not mutate global hook or MCP settings.
""",
        encoding="utf-8",
    )

def package_files(root: Path, *, omit: Iterable[Path] = ()) -> list[Path]:
    omitted = {path.resolve() for path in omit}
    return [
        path
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.resolve() not in omitted and not EXCLUDED_NAMES.intersection(path.parts)
    ]


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_package_manifest(package: Path, *, target: str, version: str, qualification: str) -> None:
    manifest_path = package / "bundle-manifest.json"
    records = [
        {
            "path": path.relative_to(package).as_posix(),
            "sha256": file_sha256(path),
            "bytes": path.stat().st_size,
        }
        for path in package_files(package, omit=(manifest_path,))
    ]
    payload = {
        "schema_version": "1.0",
        "name": "lca-skills",
        "version": version,
        "target": target,
        "built": release_date(version),
        "qualification": qualification,
        "qualification_note": "Structural qualification is not a substitute for target-host upload, invocation, licensed-dataset, or scientific known-case testing.",
        "file_count": len(records),
        "files": records,
    }
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def deterministic_zip(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in package_files(source):
            relative = Path(source.name) / path.relative_to(source)
            info = zipfile.ZipInfo(relative.as_posix(), FIXED_ZIP_TIME)
            mode = 0o755 if path.suffix == ".sh" else 0o644
            info.external_attr = ((mode & 0xFFFF) | stat.S_IFREG) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())


def build() -> dict[str, object]:
    version = source_version()
    packages = DIST / "packages"
    packages.mkdir(parents=True, exist_ok=True)

    portable = DIST / "portable/lca-skills-portable"
    portable.mkdir(parents=True, exist_ok=True)
    copy_skills(portable / "skills")
    common_runtime(portable, include_docs=True, include_examples=True)
    (portable / "README.md").write_text(
        f"# Portable LCA Skills\n\nVersion {version}. Canonical Agent Skills source with standards-compliant frontmatter and no host-only fields. Install individual directories from `skills/` in any compatible host, or use a host-specific distribution.\n",
        encoding="utf-8",
    )
    write_package_manifest(portable, target="portable", version=version, qualification="structural")

    claude = DIST / "claude-code/lca-skills"
    claude.mkdir(parents=True, exist_ok=True)
    copy_tree(ROOT / ".claude-plugin", claude / ".claude-plugin")
    copy_file(ROOT / ".mcp.json", claude / ".mcp.json")
    copy_tree(ROOT / "hooks", claude / "hooks")
    copy_tree(ROOT / "agents", claude / "agents")
    copy_skills(claude / "skills", claude_overlay=True)
    common_runtime(claude, include_docs=True, include_examples=True)
    copy_file(ROOT / "CLAUDE.md", claude / "CLAUDE.md")
    (claude / "README.md").write_text(
        f"# LCA Skills for Claude Code\n\nVersion {version}. Load this directory with `claude --plugin-dir <path-to-lca-skills>`. Plugin commands are namespaced, for example `/lca-skills:lca-expert` and explicit-only `/lca-skills:lca-autopilot`. This build includes 28 skills, 9 read-only specialist agents, a safe validation hook, and the local `lca-tools` MCP server.\n",
        encoding="utf-8",
    )
    write_package_manifest(claude, target="claude-code-plugin", version=version, qualification="structural")

    standalone = DIST / "claude-standalone/lca-skills-standalone"
    standalone.mkdir(parents=True, exist_ok=True)
    copy_skills(standalone / "skills", claude_overlay=True)
    copy_tree(ROOT / "agents", standalone / "agents")
    common_runtime(standalone, include_docs=True, include_examples=True)
    standalone_installers(standalone, version)
    write_package_manifest(standalone, target="claude-code-standalone", version=version, qualification="structural")

    codex = DIST / "codex/lca-skills"
    codex.mkdir(parents=True, exist_ok=True)
    copy_tree(ROOT / ".codex-plugin", codex / ".codex-plugin")
    copy_skills(codex / "skills")
    common_runtime(codex, include_docs=True, include_examples=True)
    copy_file(ROOT / "AGENTS.md", codex / "AGENTS.md")
    (codex / "README.md").write_text(
        f"# LCA Skills for Codex\n\nVersion {version}. This build contains the Codex plugin manifest and 28 portable skills. Invoke a skill by its installed Codex skill name, commonly `$lca-expert`; verify the exact syntax in the installed Codex version. The bundled CLI and MCP-compatible runtime do not imply that optional LCA tools are installed.\n",
        encoding="utf-8",
    )
    write_package_manifest(codex, target="codex", version=version, qualification="structural")

    chatgpt = build_consolidated("chatgpt", DIST / "chatgpt", version)
    claude_ai = build_consolidated("claude-ai", DIST / "claude-ai", version)

    targets = {
        f"LCA-Skills-Portable-v{version}.zip": portable,
        f"LCA-Skills-ClaudeCode-v{version}.zip": claude,
        f"LCA-Skills-ClaudeStandalone-v{version}.zip": standalone,
        f"LCA-Skills-Codex-v{version}.zip": codex,
        f"LCA-Skills-ChatGPT-v{version}.zip": chatgpt,
        f"LCA-Skills-ClaudeAI-v{version}.zip": claude_ai,
    }
    for name, source in targets.items():
        deterministic_zip(source, packages / name)

    return {
        "version": version,
        "packages": [
            {
                "name": name,
                "path": str((packages / name).relative_to(ROOT)),
                "sha256": file_sha256(packages / name),
                "bytes": (packages / name).stat().st_size,
            }
            for name in sorted(targets)
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clean", action="store_true", help="Remove existing dist output first")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.clean:
        remove_tree(DIST)
    payload = build()
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Built {len(payload['packages'])} distributions for v{payload['version']}")
        for item in payload["packages"]:
            print(f"  {item['path']}  {item['sha256']}  {item['bytes']} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Validate host distributions, manifests, portable frontmatter, references, and ZIP integrity."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PORTABLE_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
CLAUDE_FIELDS = {
    "argument-hint",
    "disable-model-invocation",
    "user-invocable",
    "context",
    "agent",
    "model",
}
REFERENCE_RE = re.compile(r"\b(?:references|scripts|assets)/[A-Za-z0-9_./-]+\.(?:md|py|json|csv|yaml|yml)\b")
EXPECTED = {
    "portable": {
        "root": DIST / "portable/lca-skills-portable",
        "zip": "LCA-Skills-Portable-v{version}.zip",
        "top": "lca-skills-portable",
        "kind": "multi-portable",
    },
    "claude-code": {
        "root": DIST / "claude-code/lca-skills",
        "zip": "LCA-Skills-ClaudeCode-v{version}.zip",
        "top": "lca-skills",
        "kind": "multi-claude",
    },
    "claude-standalone": {
        "root": DIST / "claude-standalone/lca-skills-standalone",
        "zip": "LCA-Skills-ClaudeStandalone-v{version}.zip",
        "top": "lca-skills-standalone",
        "kind": "multi-claude",
    },
    "codex": {
        "root": DIST / "codex/lca-skills",
        "zip": "LCA-Skills-Codex-v{version}.zip",
        "top": "lca-skills",
        "kind": "multi-portable",
    },
    "chatgpt": {
        "root": DIST / "chatgpt/lca-expert",
        "zip": "LCA-Skills-ChatGPT-v{version}.zip",
        "top": "lca-expert",
        "kind": "consolidated",
    },
    "claude-ai": {
        "root": DIST / "claude-ai/lca-expert",
        "zip": "LCA-Skills-ClaudeAI-v{version}.zip",
        "top": "lca-expert",
        "kind": "consolidated",
    },
}


def version() -> str:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'(?m)^version\s*=\s*"([^"]+)"\s*$', text)
    if not match:
        raise RuntimeError("Cannot determine source version")
    return match.group(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, lines
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, lines
    data: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"\'')
    return data, lines[end + 1 :]


def add(errors: list[str], target: str, message: str) -> None:
    errors.append(f"ERROR {target}: {message}")


def validate_manifest(package: Path, target: str, expected_version: str, errors: list[str]) -> None:
    path = package / "bundle-manifest.json"
    if not path.exists():
        add(errors, target, "bundle-manifest.json missing")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add(errors, target, f"invalid bundle manifest: {exc}")
        return
    if data.get("version") != expected_version:
        add(errors, target, f"bundle version {data.get('version')!r} != {expected_version!r}")
    if data.get("qualification") != "structural":
        add(errors, target, "bundle must distinguish structural qualification")
    records = data.get("files")
    if not isinstance(records, list):
        add(errors, target, "bundle files must be an array")
        return
    expected_paths = {
        path.relative_to(package).as_posix()
        for path in package.rglob("*")
        if path.is_file() and path.name != "bundle-manifest.json" and "__pycache__" not in path.parts
    }
    recorded_paths = {str(item.get("path")) for item in records if isinstance(item, dict)}
    if expected_paths != recorded_paths:
        missing = sorted(expected_paths.difference(recorded_paths))
        extra = sorted(recorded_paths.difference(expected_paths))
        add(errors, target, f"bundle manifest path mismatch; missing={missing[:5]}, extra={extra[:5]}")
    if data.get("file_count") != len(records):
        add(errors, target, "bundle file_count does not match records")
    for item in records:
        if not isinstance(item, dict):
            add(errors, target, "non-object file record")
            continue
        rel = Path(str(item.get("path", "")))
        file_path = package / rel
        if not file_path.is_file():
            continue
        if item.get("sha256") != sha256(file_path):
            add(errors, target, f"hash mismatch: {rel.as_posix()}")
        if item.get("bytes") != file_path.stat().st_size:
            add(errors, target, f"byte-size mismatch: {rel.as_posix()}")


def resolve_reference(skill_file: Path, package: Path, raw: str) -> Path | None:
    local = skill_file.parent / raw
    if local.exists():
        return local
    package_path = package / raw
    if package_path.exists():
        return package_path
    # Consolidated module files can intentionally resolve shared scripts/assets from the top-level skill root.
    for parent in skill_file.parents:
        if parent == package.parent:
            break
        candidate = parent / raw
        if candidate.exists():
            return candidate
    return None


def validate_skill_file(
    path: Path,
    package: Path,
    target: str,
    errors: list[str],
    *,
    allow_claude: bool,
    directory_match: bool = True,
) -> None:
    metadata, body = parse_frontmatter(path)
    rel = path.relative_to(package).as_posix()
    name = metadata.get("name", "")
    if not name or not NAME_RE.fullmatch(name):
        add(errors, target, f"{rel} has invalid or missing name")
    if directory_match and name != path.parent.name:
        add(errors, target, f"{rel} name {name!r} does not match directory")
    if not metadata.get("description"):
        add(errors, target, f"{rel} has no description")
    unknown = set(metadata).difference(PORTABLE_FIELDS | (CLAUDE_FIELDS if allow_claude else set()))
    if unknown:
        add(errors, target, f"{rel} has unsupported frontmatter: {', '.join(sorted(unknown))}")
    if not allow_claude and set(metadata).intersection(CLAUDE_FIELDS):
        add(errors, target, f"{rel} leaks Claude-only frontmatter")
    if allow_claude and not metadata.get("argument-hint"):
        add(errors, target, f"{rel} has no Claude argument-hint")
    text = "\n".join(body)
    for raw in REFERENCE_RE.findall(text):
        if resolve_reference(path, package, raw) is None:
            add(errors, target, f"{rel} has unresolved resource: {raw}")


def validate_multi(package: Path, target: str, errors: list[str], *, claude: bool) -> None:
    skill_files = sorted((package / "skills").glob("*/SKILL.md"))
    if len(skill_files) != 28:
        add(errors, target, f"expected 28 skills; found {len(skill_files)}")
    for path in skill_files:
        validate_skill_file(path, package, target, errors, allow_claude=claude)
    autopilot = package / "skills/lca-autopilot/SKILL.md"
    if claude and autopilot.exists():
        metadata, _ = parse_frontmatter(autopilot)
        if metadata.get("disable-model-invocation") != "true":
            add(errors, target, "lca-autopilot is not explicit-only")
    if not claude:
        for path in skill_files:
            if "argument-hint:" in path.read_text(encoding="utf-8"):
                add(errors, target, f"Claude field found in portable skill {path.parent.name}")


def validate_consolidated(package: Path, target: str, errors: list[str]) -> None:
    root_skill = package / "SKILL.md"
    if not root_skill.exists():
        add(errors, target, "top-level SKILL.md missing")
        return
    validate_skill_file(root_skill, package, target, errors, allow_claude=False)
    modules = sorted((package / "references/modules").glob("*/SKILL.md"))
    if len(modules) != 27:
        add(errors, target, f"expected 27 bundled specialist modules; found {len(modules)}")
    for path in modules:
        validate_skill_file(path, package, target, errors, allow_claude=False)
    root_text = root_skill.read_text(encoding="utf-8")
    if "Bundled single-skill mode" not in root_text:
        add(errors, target, "single-skill routing override missing")
    if (package / "skills").exists():
        add(errors, target, "consolidated upload must not expose a second top-level skills collection")
    for required in ("scripts/new_study.py", "assets/templates/study.yaml", "lca_tools/cli.py"):
        if not (package / required).exists():
            add(errors, target, f"missing bundled runtime resource: {required}")


def validate_special_components(package: Path, target: str, errors: list[str]) -> None:
    if target == "claude-code":
        for rel in (
            ".claude-plugin/plugin.json",
            ".mcp.json",
            "hooks/hooks.json",
            "scripts/hook_validate.py",
            "scripts/validate_active_plugin.py",
        ):
            if not (package / rel).exists():
                add(errors, target, f"missing plugin component: {rel}")
        agents = sorted((package / "agents").glob("*.md"))
        if len(agents) != 9:
            add(errors, target, f"expected 9 Claude agents; found {len(agents)}")
        validator = package / "scripts/validate_active_plugin.py"
        if validator.exists():
            proc = subprocess.run(
                [sys.executable, str(validator), str(package), "--strict"],
                text=True,
                capture_output=True,
                check=False,
            )
            if proc.returncode:
                add(errors, target, f"installed plugin validation failed: {(proc.stdout + proc.stderr)[-2000:]}")
    elif target == "claude-standalone":
        for rel in ("install.ps1", "install.sh", "uninstall.ps1", "uninstall.sh"):
            if not (package / rel).exists():
                add(errors, target, f"missing standalone lifecycle script: {rel}")
        shell = shutil.which("sh")
        for name in ("install.sh", "uninstall.sh"):
            script = package / name
            if shell and script.exists():
                proc = subprocess.run([shell, "-n", str(script)], text=True, capture_output=True, check=False)
                if proc.returncode:
                    add(errors, target, f"{name} syntax failure: {proc.stderr.strip()}")
        ps_text = (package / "install.ps1").read_text(encoding="utf-8") if (package / "install.ps1").exists() else ""
        uninstall_text = (package / "uninstall.ps1").read_text(encoding="utf-8") if (package / "uninstall.ps1").exists() else ""
        if "Remove-Item -Recurse -Force $Target" not in ps_text:
            add(errors, target, "PowerShell installer is not idempotent for existing skill directories")
        if "lca-skills-install.json" not in ps_text:
            add(errors, target, "PowerShell installer does not write an installation receipt")
        if "RemoveRuntime" not in uninstall_text or "pip uninstall -y lca-skills" not in uninstall_text:
            add(errors, target, "PowerShell uninstaller lacks explicit optional runtime removal")
    elif target == "codex":
        manifest = package / ".codex-plugin/plugin.json"
        if not manifest.exists():
            add(errors, target, "Codex plugin manifest missing")
        else:
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                data = {}
            if data.get("skills") != "./skills/":
                add(errors, target, "Codex manifest skills path must be ./skills/")


def validate_zip(path: Path, top: str, target: str, errors: list[str]) -> None:
    if not path.exists():
        add(errors, target, f"ZIP missing: {path.name}")
        return
    try:
        with zipfile.ZipFile(path) as archive:
            bad = archive.testzip()
            if bad:
                add(errors, target, f"ZIP CRC failure at {bad}")
            names = archive.namelist()
            if not names:
                add(errors, target, "ZIP is empty")
                return
            tops = {name.split("/", 1)[0] for name in names}
            if tops != {top}:
                add(errors, target, f"ZIP top-level entries are {sorted(tops)}, expected {top}")
            for info in archive.infolist():
                pure = Path(info.filename)
                if pure.is_absolute() or ".." in pure.parts:
                    add(errors, target, f"unsafe ZIP path: {info.filename}")
                if info.date_time != (2020, 1, 1, 0, 0, 0):
                    add(errors, target, f"non-deterministic timestamp: {info.filename}")
    except zipfile.BadZipFile as exc:
        add(errors, target, f"invalid ZIP: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    expected_version = version()
    errors: list[str] = []
    results: dict[str, Any] = {}

    for target, spec in EXPECTED.items():
        package = Path(spec["root"])
        start = len(errors)
        if not package.exists():
            add(errors, target, f"distribution root missing: {package.relative_to(ROOT)}")
        else:
            validate_manifest(package, target, expected_version, errors)
            if spec["kind"] == "consolidated":
                validate_consolidated(package, target, errors)
            else:
                validate_multi(package, target, errors, claude=spec["kind"] == "multi-claude")
            validate_special_components(package, target, errors)
        zip_path = DIST / "packages" / str(spec["zip"]).format(version=expected_version)
        validate_zip(zip_path, str(spec["top"]), target, errors)
        results[target] = {
            "status": "PASS" if len(errors) == start else "FAIL",
            "root": str(package.relative_to(ROOT)) if package.is_absolute() else str(package),
            "zip": str(zip_path.relative_to(ROOT)),
        }

    payload = {
        "schema_version": "1.0",
        "version": expected_version,
        "status": "PASS" if not errors else "FAIL",
        "targets": results,
        "errors": errors,
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for target, result in results.items():
            print(f"{result['status']:4} {target:20} {result['zip']}")
        for message in errors:
            print(message)
        print(f"Distribution validation: {len(results)} targets, {len(errors)} errors.")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())

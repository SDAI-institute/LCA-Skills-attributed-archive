"""Non-invasive environment and host qualification diagnostics."""

from __future__ import annotations

import json
import socket
import subprocess
from pathlib import Path
from typing import Any

from .common import (
    executable,
    module_visible,
    package_version,
    platform_snapshot,
    root_dir,
)

PACKAGE_GROUPS = {
    "openlca": ("olca-ipc", "olca-schema", "olca-ipc-rest", "olca"),
    "brightway": (
        "brightway25", "brightway2", "bw2data", "bw2calc", "bw2io",
        "bw-processing", "stats-arrays", "activity-browser", "premise",
        "wurst", "bw-temporalis", "bw-timex", "bw2regional",
    ),
    "mcp": ("mcp",),
}
MODULES = (
    "olca_ipc", "olca_schema", "olca", "bw2data", "bw2calc", "bw2io",
    "bw_processing", "premise", "wurst", "bw_temporalis", "bw_timex", "mcp",
)
EXECUTABLES = ("python", "python3", "claude", "codex", "git", "uv", "java", "dotnet", "openLCA", "openlca")


def _version_command(path: str | None) -> dict[str, Any]:
    if not path:
        return {"status": "NOT INSTALLED", "path": None, "version": None}
    for args in ([path, "--version"], [path, "version"]):
        try:
            proc = subprocess.run(args, text=True, capture_output=True, timeout=5, check=False)
        except (OSError, subprocess.TimeoutExpired):
            continue
        output = (proc.stdout or proc.stderr).strip().splitlines()
        if output:
            return {
                "status": "PASS" if proc.returncode == 0 else "WARN",
                "path": path,
                "version": output[0][:500],
            }
    return {"status": "WARN", "path": path, "version": "detected; version command unavailable"}


def _tcp_check(host: str, port: int, timeout: float) -> dict[str, Any]:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return {
                "status": "PASS",
                "reachable": True,
                "note": "Transport-only result; database and API identity remain unverified.",
            }
    except OSError as exc:
        return {"status": "FAIL", "reachable": False, "error": f"{type(exc).__name__}: {exc}"}


def _repo_validation(repo: Path) -> dict[str, Any]:
    validator = repo / "scripts" / "validate_repo.py"
    if not validator.exists():
        return {"status": "NOT TESTED", "reason": "validator not present in this package"}
    proc = subprocess.run(
        [__import__("sys").executable, str(validator), "--strict"],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "status": "PASS" if proc.returncode == 0 else "FAIL",
        "returncode": proc.returncode,
        "output": (proc.stdout + proc.stderr)[-4000:],
    }


def snapshot(*, check_openlca: bool = False, host: str = "127.0.0.1", port: int = 8080, timeout: float = 1.0) -> dict[str, Any]:
    repo = root_dir()
    payload = {
        "schema_version": "1.0",
        **platform_snapshot(),
        "repository": {
            "root": str(repo),
            "validation": _repo_validation(repo),
        },
        "executables": {},
        "packages": {},
        "modules_visible": {name: module_visible(name) for name in MODULES},
        "openlca_endpoint": {
            "host": host,
            "port": port,
            "status": "NOT TESTED",
            "note": "Use an explicit endpoint check; a reachable port is not scientific qualification.",
        },
        "qualification": {
            "structural": "Repository validation is reported above.",
            "runtime": "Optional tools are qualified only when a representative command is run.",
            "scientific": "Requires known-case reconciliation and practitioner review.",
            "real_host": "Requires invocation inside each installed host; file parsing alone is insufficient.",
        },
    }
    for name in EXECUTABLES:
        path = executable(name)
        payload["executables"][name] = _version_command(path) if name in {"claude", "codex", "git", "uv", "java", "dotnet"} else {
            "status": "PASS" if path else "NOT INSTALLED",
            "path": path,
        }
    for group, names in PACKAGE_GROUPS.items():
        payload["packages"][group] = {name: package_version(name) for name in names}
    if check_openlca:
        payload["openlca_endpoint"] = {"host": host, "port": port, **_tcp_check(host, port, timeout)}
    return payload


def render_text(payload: dict[str, Any]) -> str:
    lines = ["LCA Skills doctor"]
    lines.append(f"Repository: {payload['repository']['validation']['status']}")
    lines.append("Executables:")
    for name, item in payload["executables"].items():
        lines.append(f"  {name}: {item['status']}" + (f" ({item.get('path')})" if item.get("path") else ""))
    lines.append("Tool packages:")
    for group, packages in payload["packages"].items():
        present = [f"{name}={version}" for name, version in packages.items() if version]
        lines.append(f"  {group}: " + (", ".join(present) if present else "NOT INSTALLED"))
    endpoint = payload["openlca_endpoint"]
    lines.append(f"openLCA endpoint: {endpoint['status']}")
    return "\n".join(lines) + "\n"

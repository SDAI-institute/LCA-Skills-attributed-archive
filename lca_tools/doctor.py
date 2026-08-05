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

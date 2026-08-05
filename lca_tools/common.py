"""Shared helpers for the LCA Skills runtime."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Any, Iterable


class LCAToolError(RuntimeError):
    """Expected runtime or input error suitable for CLI/MCP reporting."""


def root_dir() -> Path:
    configured = os.environ.get("LCA_SKILLS_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


def project_dir() -> Path:
    configured = os.environ.get("LCA_PROJECT_ROOT")
    return Path(configured).expanduser().resolve() if configured else Path.cwd().resolve()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def package_version(*names: str) -> str | None:
    for name in names:
        try:
            return metadata.version(name)
        except metadata.PackageNotFoundError:
            continue
    return None


def module_visible(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def executable(name: str) -> str | None:
    return shutil.which(name)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

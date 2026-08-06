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


def file_record(path: Path | None, *, redact_path: bool = True) -> dict[str, Any] | None:
    if path is None:
        return None
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise LCAToolError(f"File not found: {path}")
    record: dict[str, Any] = {
        "name": resolved.name,
        "size_bytes": resolved.stat().st_size,
        "sha256": sha256(resolved),
    }
    if redact_path:
        record["local_path_redacted"] = True
    else:
        record["path"] = str(resolved)
    return record


def json_safe(value: Any, *, depth: int = 0) -> Any:
    """Convert common schema/client objects to bounded JSON-safe structures."""
    if depth > 5:
        return repr(value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return str(value)
    if is_dataclass(value):
        return json_safe(asdict(value), depth=depth + 1)
    if isinstance(value, dict):
        return {str(k): json_safe(v, depth=depth + 1) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [json_safe(v, depth=depth + 1) for v in value]
    result: dict[str, Any] = {}
    for key in ("id", "name", "category", "unit", "amount", "value", "ref_unit", "location"):
        if hasattr(value, key):
            try:
                result[key] = json_safe(getattr(value, key), depth=depth + 1)
            except Exception:  # pragma: no cover - defensive against third-party descriptors
                pass
    if result:
        return result
    if hasattr(value, "to_dict"):
        try:
            return json_safe(value.to_dict(), depth=depth + 1)
        except Exception:  # pragma: no cover
            pass
    return repr(value)


def run_script(script: str, args: Iterable[str], *, cwd: Path | None = None) -> dict[str, Any]:
    path = root_dir() / "scripts" / script
    if not path.exists():
        raise LCAToolError(f"Bundled script not found: {path}")
    command = [sys.executable, str(path), *[str(arg) for arg in args]]
    proc = subprocess.run(
        command,
        cwd=str(cwd or root_dir()),
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "ok": proc.returncode == 0,
    }


def write_json(path: Path, payload: Any) -> None:
    target = path.expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(target)


def platform_snapshot() -> dict[str, Any]:
    return {
        "generated_utc": utc_now(),
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
    }

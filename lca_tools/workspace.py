"""Wrappers around deterministic study workspace utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import LCAToolError, run_script


def _require_success(payload: dict[str, Any], operation: str) -> dict[str, Any]:
    payload["operation"] = operation
    if not payload["ok"]:
        raise LCAToolError(f"{operation} failed: {payload['stderr'] or payload['stdout']}")
    return payload


def new_study(slug: str, title: str | None = None, root: str | Path | None = None, *, overwrite_empty: bool = False) -> dict[str, Any]:
    args = [slug]
    if title:
        args.extend(["--title", title])
    if root:
        args.extend(["--root", str(Path(root).expanduser().resolve())])
    if overwrite_empty:
        args.append("--overwrite-empty")
    return _require_success(run_script("new_study.py", args), "new_study")


def validate_study(study: str | Path, *, strict: bool = False) -> dict[str, Any]:
    args = [str(Path(study).expanduser().resolve())]
    if strict:
        args.append("--strict")
    payload = run_script("validate_study.py", args)
    payload["operation"] = "validate_study"
    return payload

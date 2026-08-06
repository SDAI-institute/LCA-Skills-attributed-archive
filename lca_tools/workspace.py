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


def check_balance(csv_file: str | Path, *, tolerance: float = 0.01, metric: str | None = None) -> dict[str, Any]:
    args = [str(Path(csv_file).expanduser().resolve()), "--tolerance", str(tolerance)]
    if metric:
        args.extend(["--metric", metric])
    payload = run_script("check_balance.py", args)
    payload["operation"] = "check_balance"
    return payload


def check_claims(study: str | Path, *, warn_only: bool = False) -> dict[str, Any]:
    args = [str(Path(study).expanduser().resolve())]
    if warn_only:
        args.append("--warn-only")
    payload = run_script("check_claims.py", args)
    payload["operation"] = "check_claims"
    return payload


def compare_results(
    baseline: str | Path,
    candidate: str | Path,
    *,
    keys: str = "impact_category,indicator,scenario",
    value: str = "value",
    unit: str = "unit",
    rtol: float = 1e-6,
    atol: float = 0.0,
    allow_differences: bool = False,
) -> dict[str, Any]:
    args = [
        str(Path(baseline).expanduser().resolve()),
        str(Path(candidate).expanduser().resolve()),
        "--keys", keys,
        "--value", value,
        "--unit", unit,
        "--rtol", str(rtol),
        "--atol", str(atol),
    ]
    if allow_differences:
        args.append("--allow-differences")
    payload = run_script("compare_results.py", args)
    payload["operation"] = "compare_results"
    return payload


def hash_manifest(study: str | Path, *, update_release: bool = False, include_raw: bool = False) -> dict[str, Any]:
    args = [str(Path(study).expanduser().resolve())]
    if update_release:
        args.append("--update-release")
    if include_raw:
        args.append("--include-raw")
    return _require_success(run_script("hash_manifest.py", args), "hash_manifest")

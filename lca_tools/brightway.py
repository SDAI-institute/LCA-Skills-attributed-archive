"""Read-only Brightway calculation adapter."""

from __future__ import annotations

from typing import Any, Sequence

from .common import LCAToolError, json_safe, package_version, platform_snapshot, utc_now


def _modules() -> tuple[Any, Any]:
    try:
        import bw2calc as bc  # type: ignore
        import bw2data as bd  # type: ignore
    except ImportError as exc:
        raise LCAToolError("Brightway core packages bw2data and bw2calc are not installed") from exc
    return bd, bc


def snapshot(*, include_projects: bool = True) -> dict[str, Any]:
    packages = {
        name: package_version(name)
        for name in (
            "brightway25", "brightway2", "bw2data", "bw2calc", "bw2io",
            "bw-processing", "stats-arrays", "activity-browser", "premise",
            "wurst", "bw-temporalis", "bw-timex", "bw2regional",
        )
    }
    payload: dict[str, Any] = {
        "schema_version": "1.0",
        **platform_snapshot(),
        "packages": packages,
        "core_available": bool(packages["bw2data"] and packages["bw2calc"]),
        "projects": {"status": "NOT TESTED", "current": None, "names": []},
    }
    if include_projects and payload["core_available"]:
        try:
            bd, _ = _modules()
            names = sorted(str(item) for item in bd.projects)
            payload["projects"] = {
                "status": "PASS",
                "current": getattr(bd.projects, "current", None),
                "names": names,
            }
        except Exception as exc:
            payload["projects"] = {"status": "WARN", "error": f"{type(exc).__name__}: {exc}"}
    return payload


def _activity(bd: Any, database: str, code: str) -> Any:

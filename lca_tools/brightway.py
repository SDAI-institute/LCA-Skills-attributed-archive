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
    try:
        if hasattr(bd, "get_activity"):
            return bd.get_activity((database, code))
        return bd.Database(database).get(code)
    except Exception as exc:
        raise LCAToolError(f"Brightway activity not found: ({database!r}, {code!r}): {exc}") from exc


def calculate(
    project: str,
    database: str,
    code: str,
    method: Sequence[str],
    *,
    amount: float = 1.0,
) -> dict[str, Any]:
    if not all((project.strip(), database.strip(), code.strip())):
        raise LCAToolError("project, database, and code are required")
    if not method:
        raise LCAToolError("method must be a non-empty sequence matching a Brightway method tuple")
    if amount <= 0:
        raise LCAToolError("amount must be positive")
    bd, bc = _modules()
    previous = getattr(bd.projects, "current", None)
    try:
        bd.projects.set_current(project)
        activity = _activity(bd, database, code)
        method_tuple = tuple(str(item) for item in method)
        if method_tuple not in bd.methods:
            raise LCAToolError(f"Brightway method not found: {method_tuple!r}")
        started = utc_now()
        lca = bc.LCA({activity: amount}, method_tuple)
        lca.lci()
        inventory_shape = tuple(int(x) for x in getattr(lca.inventory, "shape", ()))
        inventory_sum = float(lca.inventory.sum()) if hasattr(lca.inventory, "sum") else None
        lca.lcia()
        method_metadata = dict(bd.Method(method_tuple).metadata)
        return {
            "schema_version": "1.0",
            "started_utc": started,
            "completed_utc": utc_now(),
            "adapter": "brightway-bw2calc",
            "packages": {
                "bw2data": package_version("bw2data"),
                "bw2calc": package_version("bw2calc"),
                "bw-processing": package_version("bw-processing"),
            },
            "request": {
                "project": project,
                "activity": {"database": database, "code": code, "name": activity.get("name")},
                "amount": amount,
                "method": list(method_tuple),
            },
            "inventory": {"shape": inventory_shape, "matrix_sum_diagnostic": inventory_sum},
            "impact": {
                "score": float(lca.score),
                "unit": method_metadata.get("unit"),
                "method_metadata": json_safe(method_metadata),
            },
            "manual_verification_required": [
                "project/database provenance and system model",
                "functional unit and activity production amount",
                "method implementation and biosphere mapping coverage",
            ],
        }
    except LCAToolError:
        raise
    except Exception as exc:
        raise LCAToolError(f"Brightway calculation failed: {type(exc).__name__}: {exc}") from exc
    finally:
        if previous and previous != project:
            try:
                bd.projects.set_current(previous)
            except Exception:
                pass

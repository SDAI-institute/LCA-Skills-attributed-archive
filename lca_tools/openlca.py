"""Read-only openLCA IPC adapter with explicit lifecycle handling."""

from __future__ import annotations

import socket
from typing import Any

from .common import LCAToolError, json_safe, package_version, platform_snapshot, utc_now


def snapshot(*, host: str = "127.0.0.1", port: int = 8080, check_endpoint: bool = False, timeout: float = 1.0) -> dict[str, Any]:
    from importlib.util import find_spec

    modules = {name: find_spec(name) is not None for name in ("olca_ipc", "olca_schema", "olca")}
    current = modules["olca_ipc"] and modules["olca_schema"]
    legacy = modules["olca"]
    generation = (
        "both-current-and-legacy-visible" if current and legacy else
        "current-schema-separated" if current else
        "legacy-monolithic" if legacy else
        "no-python-client-detected"
    )
    endpoint: dict[str, Any] = {
        "host": host,
        "port": port,
        "tcp_checked": check_endpoint,
        "tcp_reachable": None,
        "interpretation": "Transport-only check; database/API/model identity remains manual.",
    }
    if check_endpoint:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                endpoint["tcp_reachable"] = True
        except OSError as exc:
            endpoint["tcp_reachable"] = False
            endpoint["tcp_error"] = f"{type(exc).__name__}: {exc}"
    return {
        "schema_version": "1.0",
        **platform_snapshot(),
        "packages": {
            "olca-ipc": package_version("olca-ipc"),
            "olca-schema": package_version("olca-schema"),
            "olca": package_version("olca"),
        },
        "modules_visible": modules,
        "detected_api_generation": generation,
        "endpoint": endpoint,
        "required_manual_fields": [
            "openlca_application_or_server_version",
            "active_database_name_and_version_or_hash",
            "lcia_package_version",
        ],
    }


def _current_modules() -> tuple[Any, Any]:
    try:
        import olca_ipc as ipc  # type: ignore
        import olca_schema as schema  # type: ignore
    except ImportError as exc:
        raise LCAToolError(
            "Current openLCA Python clients are unavailable. Install compatible olca-ipc and "
            "olca-schema packages, or use the documented legacy workflow in a pinned environment."
        ) from exc
    return ipc, schema


def _client(ipc: Any, host: str, port: int) -> Any:
    if host not in {"127.0.0.1", "localhost", "::1"}:
        raise LCAToolError("This bundled JSON-RPC adapter only permits a local openLCA endpoint by default.")

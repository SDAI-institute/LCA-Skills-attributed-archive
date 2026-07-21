#!/usr/bin/env python3
"""Create a non-invasive openLCA IPC environment snapshot.

This script does not import an IPC client, query a database, or mutate openLCA.
It records Python/package/module visibility and optionally checks whether a TCP
endpoint accepts a connection. A reachable port is not an API or database health
check.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import socket
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Any

DISTRIBUTIONS = (
    "olca-ipc",
    "olca-schema",
    "olca-ipc-rest",
)
MODULES = (
    "olca_ipc",
    "olca_schema",
    "olca",
)


def package_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def module_visible(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def tcp_check(host: str, port: int, timeout: float) -> tuple[bool, str | None]:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, None
    except OSError as exc:
        return False, f"{type(exc).__name__}: {exc}"


def infer_generation(modules: dict[str, bool]) -> str:
    current = modules.get("olca_ipc", False) and modules.get("olca_schema", False)
    legacy = modules.get("olca", False)
    if current and legacy:
        return "both-current-and-legacy-visible"
    if current:
        return "current-schema-separated"
    if legacy:
        return "legacy-monolithic"
    return "no-python-client-detected"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--check-port", action="store_true")
    parser.add_argument("--timeout", type=float, default=1.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    modules = {name: module_visible(name) for name in MODULES}
    endpoint: dict[str, Any] = {
        "host": args.host,
        "port": args.port,
        "tcp_checked": args.check_port,
        "tcp_reachable": None,
        "tcp_error": None,
        "interpretation": "Transport-only check; does not prove API, database, or model identity.",
    }
    if args.check_port:
        reachable, error = tcp_check(args.host, args.port, args.timeout)
        endpoint["tcp_reachable"] = reachable
        endpoint["tcp_error"] = error

    payload = {
        "schema_version": "1.0",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
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
        "distributions": {name: package_version(name) for name in DISTRIBUTIONS},
        "modules_visible": modules,
        "detected_api_generation": infer_generation(modules),
        "endpoint": endpoint,
        "required_manual_fields": {
            "openlca_application_or_server_version": None,
            "active_database_name": None,
            "active_database_version_or_hash": None,
            "ipc_protocol": None,
            "lcia_package_version": None,
        },
    }

    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

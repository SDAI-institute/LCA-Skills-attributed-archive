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

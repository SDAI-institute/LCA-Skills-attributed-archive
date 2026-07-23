#!/usr/bin/env python3
"""Build a provenance manifest for a GREET run without bundling model contents."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def file_record(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    resolved = path.resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"Not a file: {path}")
    return {
        "name": resolved.name,
        "size_bytes": resolved.stat().st_size,
        "sha256": sha256(resolved),
        "local_path_redacted": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study-id", required=True)
    parser.add_argument("--product", default="R&D GREET")
    parser.add_argument("--release", required=True)
    parser.add_argument("--revision", default="")

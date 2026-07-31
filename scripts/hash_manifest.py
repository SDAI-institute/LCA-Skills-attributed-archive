#!/usr/bin/env python3
"""Create deterministic SHA-256 file hashes for an LCA study release."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_EXCLUDED_PARTS = {".git", "__pycache__", ".venv", "private", "raw"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("study", type=Path)
    parser.add_argument("--output", type=Path, help="Output JSON; default results/release/file-hashes.json")
    parser.add_argument("--include-raw", action="store_true")
    parser.add_argument("--update-release", action="store_true", help="Write hashes into release-manifest.json")
    args = parser.parse_args()

    study = args.study.resolve()

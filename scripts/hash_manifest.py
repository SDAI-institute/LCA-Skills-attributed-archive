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
    if not study.is_dir():
        print(f"ERROR: study directory not found: {study}", file=sys.stderr)
        return 1
    output = (args.output.resolve() if args.output else study / "results/release/file-hashes.json")
    release_manifest = study / "results/release/release-manifest.json"

    excluded = set(DEFAULT_EXCLUDED_PARTS)
    if args.include_raw:
        excluded.discard("raw")

    records: list[dict[str, object]] = []
    for path in sorted(study.rglob("*")):
        if not path.is_file() or path.resolve() in {output.resolve()}:
            continue
        rel = path.relative_to(study)
        if any(part in excluded for part in rel.parts):
            continue
        records.append({"path": rel.as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size})

    payload = {
        "manifest_version": "1.0",
        "study_id": study.name,
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "hash_algorithm": "sha256",
        "excluded_parts": sorted(excluded),
        "files": records,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    if args.update_release:
        if not release_manifest.exists():
            print(f"ERROR: release manifest not found: {release_manifest}", file=sys.stderr)
            return 1
        try:
            release = json.loads(release_manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"ERROR: invalid release manifest: {exc}", file=sys.stderr)
            return 1
        release["file_hashes"] = records
        release_manifest.write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {len(records)} file hashes to {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

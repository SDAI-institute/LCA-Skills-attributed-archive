#!/usr/bin/env python3
"""Build a deterministic source-repository release archive and hash manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXED_ZIP_TIME = (2020, 1, 1, 0, 0, 0)
EXCLUDED_PARTS = {".git", ".venv", "__pycache__", "dist", "build"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def version() -> str:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'(?m)^version\s*=\s*"([^"]+)"\s*$', text)
    if not match:
        raise RuntimeError("Cannot determine version from pyproject.toml")
    return match.group(1)


def release_date(current_version: str) -> str:
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(rf"(?m)^## \[{re.escape(current_version)}\] - (\d{{4}}-\d{{2}}-\d{{2}})\s*$", text)
    if not match:
        raise RuntimeError(f"Cannot determine release date for {current_version}")
    return match.group(1)


def source_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if EXCLUDED_PARTS.intersection(rel.parts) or path.suffix.lower() in EXCLUDED_SUFFIXES:
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(ROOT).as_posix())


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def zip_info(name: str, mode: int = 0o644) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
    info.external_attr = ((mode & 0xFFFF) | stat.S_IFREG) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    return info


def build(output_dir: Path) -> dict[str, object]:
    current_version = version()
    files = source_files()
    records = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }
        for path in files
    ]
    manifest = {
        "schema_version": "1.0",
        "name": "LCA-skills",
        "version": current_version,
        "release_date": release_date(current_version),
        "qualification": "source-structural-and-local-runtime",
        "qualification_note": (
            "This source archive was built deterministically. Target-host import and licensed LCA-tool "
            "scientific qualification remain separate evidence layers."
        ),
        "file_count": len(records),
        "files": records,
    }
    manifest_bytes = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")

    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"LCA-skills-v{current_version}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in files:
            rel = Path("LCA-skills") / path.relative_to(ROOT)
            mode = 0o755 if path.suffix == ".sh" else 0o644
            bundle.writestr(zip_info(rel.as_posix(), mode), path.read_bytes())
        bundle.writestr(zip_info("LCA-skills/SOURCE-RELEASE.json"), manifest_bytes)

    with zipfile.ZipFile(archive) as bundle:
        bad = bundle.testzip()
        if bad:
            raise RuntimeError(f"ZIP CRC failure at {bad}")
        tops = {name.split("/", 1)[0] for name in bundle.namelist()}
        if tops != {"LCA-skills"}:
            raise RuntimeError(f"Unexpected source archive roots: {sorted(tops)}")
        if any(info.date_time != FIXED_ZIP_TIME for info in bundle.infolist()):
            raise RuntimeError("Source archive contains non-deterministic timestamps")

    archive_hash = sha256_file(archive)
    checksum = output_dir / f"LCA-skills-v{current_version}.sha256"
    checksum.write_text(f"{archive_hash}  {archive.name}\n", encoding="utf-8")
    file_manifest = output_dir / f"LCA-skills-v{current_version}-files.sha256"
    lines = [f"{item['sha256']}  LCA-skills/{item['path']}" for item in records]
    lines.append(f"{sha256_bytes(manifest_bytes)}  LCA-skills/SOURCE-RELEASE.json")
    file_manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "version": current_version,
        "archive": str(archive),
        "sha256": archive_hash,
        "bytes": archive.stat().st_size,
        "source_file_count": len(records),
        "checksum_file": str(checksum),
        "file_manifest": str(file_manifest),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/source")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = build(args.output.resolve())
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(
            f"Built {payload['archive']} with {payload['source_file_count']} source files; "
            f"SHA-256 {payload['sha256']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())

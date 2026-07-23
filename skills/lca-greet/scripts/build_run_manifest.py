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
    parser.add_argument("--platform", required=True, help="For example: .NET, Excel, web, or module name")
    parser.add_argument("--doi", default="")
    parser.add_argument("--model-file", type=Path)
    parser.add_argument("--input-export", type=Path)
    parser.add_argument("--result-export", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    try:
        artifacts = {
            "model": file_record(args.model_file),
            "input_export": file_record(args.input_export),
            "result_export": file_record(args.result_export),
        }
    except FileNotFoundError as exc:
        parser.error(str(exc))

    payload = {
        "schema_version": "1.0",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "study_id": args.study_id,
        "greet": {
            "product": args.product,
            "release": args.release,
            "revision": args.revision or None,
            "platform": args.platform,
            "doi": args.doi or None,
        },
        "artifacts": artifacts,
        "required_modeling_fields": {
            "pathway_or_case": None,
            "functional_basis": None,
            "boundary": None,
            "geography": None,
            "reference_year": None,
            "energy_basis_lhv_or_hhv": None,
            "allocation_or_coproduct_method": None,
            "gwp_method_horizon_and_version": None,
            "input_delta_table": None,
            "integration_replacement_map": None,
        },
        "license_note": "Hashes identify local artifacts; this manifest does not grant redistribution rights.",
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

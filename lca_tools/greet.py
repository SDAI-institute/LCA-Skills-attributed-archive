"""Controlled GREET provenance and result-ingestion adapter.

GREET products do not expose one stable generic automation API. This module
therefore records exact product/release provenance and validates exported
results without pretending that R&D and regulatory GREET products are
interchangeable.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Any

from .common import LCAToolError, file_record, utc_now, write_json


def build_manifest(
    *,
    study_id: str,
    product: str,
    release: str,
    platform: str,
    output: str | Path,
    revision: str = "",
    doi: str = "",
    model_file: str | Path | None = None,
    input_export: str | Path | None = None,
    result_export: str | Path | None = None,
    pathway: str = "",
    boundary: str = "",
    functional_basis: str = "",
) -> dict[str, Any]:
    if not all((study_id.strip(), product.strip(), release.strip(), platform.strip())):
        raise LCAToolError("study_id, product, release, and platform are required")
    payload = {
        "schema_version": "1.1",
        "generated_utc": utc_now(),
        "study_id": study_id,
        "greet": {
            "product": product,
            "release": release,
            "revision": revision or None,
            "platform": platform,
            "doi": doi or None,
            "pathway_or_case": pathway or None,
            "boundary": boundary or None,
            "functional_basis": functional_basis or None,
        },
        "artifacts": {
            "model": file_record(Path(model_file)) if model_file else None,
            "input_export": file_record(Path(input_export)) if input_export else None,
            "result_export": file_record(Path(result_export)) if result_export else None,
        },
        "required_modeling_fields": {
            "geography": None,
            "reference_year": None,
            "energy_basis_lhv_or_hhv": None,
            "allocation_or_coproduct_method": None,
            "gwp_method_horizon_and_version": None,
            "input_delta_table": None,
            "integration_replacement_map": None,
        },
        "automation_note": (
            "This adapter records provenance and exported results. Execution requires a separately "
            "validated runner for the exact GREET product and release."
        ),
        "license_note": "Hashes identify local artifacts; this manifest does not grant redistribution rights.",
    }
    write_json(Path(output), payload)
    return payload


def import_results(csv_file: str | Path, *, output: str | Path | None = None) -> dict[str, Any]:
    path = Path(csv_file).expanduser().resolve()
    if not path.is_file():
        raise LCAToolError(f"GREET result export not found: {path}")
    required = {"indicator", "value", "unit"}
    records: list[dict[str, Any]] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise LCAToolError(f"GREET export missing headers: {', '.join(sorted(missing))}")
        for line, row in enumerate(reader, start=2):
            try:
                value = float((row.get("value") or "").replace(",", ""))
            except ValueError as exc:
                raise LCAToolError(f"GREET export line {line}: nonnumeric value") from exc
            if not math.isfinite(value):
                raise LCAToolError(f"GREET export line {line}: nonfinite value")
            indicator = (row.get("indicator") or "").strip()
            unit = (row.get("unit") or "").strip()
            if not indicator or not unit:
                raise LCAToolError(f"GREET export line {line}: indicator and unit are required")
            records.append({
                "indicator": indicator,
                "value": value,
                "unit": unit,
                "pathway": (row.get("pathway") or "").strip() or None,
                "scenario": (row.get("scenario") or "").strip() or None,
                "boundary": (row.get("boundary") or "").strip() or None,
                "release": (row.get("release") or "").strip() or None,
            })
    payload = {
        "schema_version": "1.0",
        "generated_utc": utc_now(),
        "source": file_record(path),
        "count": len(records),
        "results": records,
        "required_reconciliation": [
            "functional basis and energy basis",
            "boundary and co-product method",
            "release/product identity",
            "indicator method and time horizon",
        ],
    }
    if output:
        write_json(Path(output), payload)
    return payload

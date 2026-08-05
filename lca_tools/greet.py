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

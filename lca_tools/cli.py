"""Command-line interface for LCA Skills runtime adapters."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .common import LCAToolError, write_json
from . import brightway as brightway_adapter
from . import doctor as doctor_adapter
from . import greet as greet_adapter
from . import openlca as openlca_adapter
from . import workspace


def emit(payload: Any, output: str | None = None, *, text: bool = False) -> None:
    if output:
        write_json(Path(output), payload)
    if text and isinstance(payload, dict):
        print(doctor_adapter.render_text(payload), end="")
    else:
        print(json.dumps(payload, indent=2, sort_keys=True))


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="lca-skills", description=__doc__)
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Run non-invasive host and tool diagnostics")
    doctor.add_argument("--check-openlca", action="store_true")
    doctor.add_argument("--host", default="127.0.0.1")
    doctor.add_argument("--port", type=int, default=8080)
    doctor.add_argument("--timeout", type=float, default=1.0)
    doctor.add_argument("--output")
    doctor.add_argument("--text", action="store_true")

    study = sub.add_parser("study", help="Manage and validate LCA study workspaces")
    study_sub = study.add_subparsers(dest="study_command", required=True)
    new = study_sub.add_parser("new")
    new.add_argument("slug")
    new.add_argument("--title")
    new.add_argument("--root")
    new.add_argument("--overwrite-empty", action="store_true")
    validate = study_sub.add_parser("validate")
    validate.add_argument("study")
    validate.add_argument("--strict", action="store_true")
    balance = study_sub.add_parser("balance")
    balance.add_argument("csv_file")
    balance.add_argument("--tolerance", type=float, default=0.01)
    balance.add_argument("--metric")
    claims = study_sub.add_parser("claims")
    claims.add_argument("study")
    claims.add_argument("--warn-only", action="store_true")
    compare = study_sub.add_parser("compare")
    compare.add_argument("baseline")
    compare.add_argument("candidate")
    compare.add_argument("--keys", default="impact_category,indicator,scenario")
    compare.add_argument("--value", default="value")
    compare.add_argument("--unit", default="unit")
    compare.add_argument("--rtol", type=float, default=1e-6)
    compare.add_argument("--atol", type=float, default=0.0)
    compare.add_argument("--allow-differences", action="store_true")
    hashes = study_sub.add_parser("hash")
    hashes.add_argument("study")
    hashes.add_argument("--update-release", action="store_true")
    hashes.add_argument("--include-raw", action="store_true")

    ol = sub.add_parser("openlca", help="Use the read-only openLCA adapter")
    ol_sub = ol.add_subparsers(dest="openlca_command", required=True)
    ol_snap = ol_sub.add_parser("snapshot")
    ol_snap.add_argument("--host", default="127.0.0.1")
    ol_snap.add_argument("--port", type=int, default=8080)
    ol_snap.add_argument("--check-endpoint", action="store_true")
    ol_snap.add_argument("--timeout", type=float, default=1.0)
    ol_list = ol_sub.add_parser("list")
    ol_list.add_argument("entity_type")
    ol_list.add_argument("--host", default="127.0.0.1")

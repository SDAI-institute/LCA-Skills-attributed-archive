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
    ol_list.add_argument("--port", type=int, default=8080)
    ol_list.add_argument("--limit", type=int, default=1000)
    ol_calc = ol_sub.add_parser("calculate")
    ol_calc.add_argument("product_system_id")
    ol_calc.add_argument("--impact-method-id")
    ol_calc.add_argument("--amount", type=float, default=1.0)
    ol_calc.add_argument("--host", default="127.0.0.1")
    ol_calc.add_argument("--port", type=int, default=8080)
    ol_calc.add_argument("--no-inventory", action="store_true")
    ol_calc.add_argument("--output")

    bw = sub.add_parser("brightway", help="Use the read-only Brightway adapter")
    bw_sub = bw.add_subparsers(dest="brightway_command", required=True)
    bw_sub.add_parser("snapshot")
    bw_calc = bw_sub.add_parser("calculate")
    bw_calc.add_argument("--project", required=True)
    bw_calc.add_argument("--database", required=True)
    bw_calc.add_argument("--code", required=True)
    bw_calc.add_argument("--method", required=True, help="JSON array or 'part1 / part2 / category'")
    bw_calc.add_argument("--amount", type=float, default=1.0)
    bw_calc.add_argument("--output")

    greet = sub.add_parser("greet", help="Build GREET manifests and ingest result exports")
    greet_sub = greet.add_subparsers(dest="greet_command", required=True)
    gm = greet_sub.add_parser("manifest")
    gm.add_argument("--study-id", required=True)
    gm.add_argument("--product", default="R&D GREET")
    gm.add_argument("--release", required=True)
    gm.add_argument("--revision", default="")
    gm.add_argument("--platform", required=True)
    gm.add_argument("--doi", default="")
    gm.add_argument("--model-file")
    gm.add_argument("--input-export")
    gm.add_argument("--result-export")
    gm.add_argument("--pathway", default="")
    gm.add_argument("--boundary", default="")
    gm.add_argument("--functional-basis", default="")
    gm.add_argument("--output", required=True)
    gi = greet_sub.add_parser("import-results")
    gi.add_argument("csv_file")
    gi.add_argument("--output")
    return p


def parse_method(value: str) -> list[str]:
    value = value.strip()
    if value.startswith("["):
        parsed = json.loads(value)
        if not isinstance(parsed, list) or not all(isinstance(item, str) for item in parsed):
            raise LCAToolError("--method JSON must be an array of strings")
        return parsed
    return [item.strip() for item in value.split("/") if item.strip()]


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "doctor":
            payload = doctor_adapter.snapshot(check_openlca=args.check_openlca, host=args.host, port=args.port, timeout=args.timeout)
            emit(payload, args.output, text=args.text)
        elif args.command == "study":
            if args.study_command == "new":
                emit(workspace.new_study(args.slug, args.title, args.root, overwrite_empty=args.overwrite_empty))
            elif args.study_command == "validate":
                payload = workspace.validate_study(args.study, strict=args.strict)
                emit(payload)
                return 0 if payload["ok"] else 1
            elif args.study_command == "balance":
                payload = workspace.check_balance(args.csv_file, tolerance=args.tolerance, metric=args.metric)
                emit(payload)
                return 0 if payload["ok"] else 1
            elif args.study_command == "claims":
                payload = workspace.check_claims(args.study, warn_only=args.warn_only)
                emit(payload)
                return 0 if payload["ok"] else 1
            elif args.study_command == "compare":
                payload = workspace.compare_results(
                    args.baseline, args.candidate, keys=args.keys, value=args.value, unit=args.unit,
                    rtol=args.rtol, atol=args.atol, allow_differences=args.allow_differences,
                )
                emit(payload)
                return 0 if payload["ok"] else 1
            elif args.study_command == "hash":
                emit(workspace.hash_manifest(args.study, update_release=args.update_release, include_raw=args.include_raw))
        elif args.command == "openlca":
            if args.openlca_command == "snapshot":
                emit(openlca_adapter.snapshot(host=args.host, port=args.port, check_endpoint=args.check_endpoint, timeout=args.timeout))
            elif args.openlca_command == "list":
                emit(openlca_adapter.list_descriptors(args.entity_type, host=args.host, port=args.port, limit=args.limit))
            elif args.openlca_command == "calculate":
                payload = openlca_adapter.calculate(
                    args.product_system_id, args.impact_method_id, amount=args.amount,
                    host=args.host, port=args.port, include_inventory=not args.no_inventory,
                )
                emit(payload, args.output)
        elif args.command == "brightway":
            if args.brightway_command == "snapshot":
                emit(brightway_adapter.snapshot())
            elif args.brightway_command == "calculate":
                payload = brightway_adapter.calculate(
                    args.project, args.database, args.code, parse_method(args.method), amount=args.amount,
                )
                emit(payload, args.output)
        elif args.command == "greet":
            if args.greet_command == "manifest":
                emit(greet_adapter.build_manifest(
                    study_id=args.study_id, product=args.product, release=args.release,
                    revision=args.revision, platform=args.platform, doi=args.doi,
                    model_file=args.model_file, input_export=args.input_export,
                    result_export=args.result_export, pathway=args.pathway,
                    boundary=args.boundary, functional_basis=args.functional_basis,
                    output=args.output,
                ))
            elif args.greet_command == "import-results":
                emit(greet_adapter.import_results(args.csv_file, output=args.output))
        return 0
    except (LCAToolError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": type(exc).__name__, "message": str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

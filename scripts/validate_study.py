#!/usr/bin/env python3
"""Validate the structure and gate readiness of an LCA study workspace."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

STATUS_ORDER = {
    "DRAFT_SCOPE": 0,
    "SCOPE_FROZEN": 1,
    "INVENTORY_READY": 2,
    "CALCULATED": 3,
    "INTERPRETED": 4,
    "REVIEWED": 5,
    "RELEASED": 6,
}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VALID_GATES = {"G0", "G1", "G2", "G3", "G4", "G5", "G6"}
VALID_WORKFLOW_MODES = {"interactive", "delegated", "autopilot"}
STATUS_MIN_GATE = {
    "DRAFT_SCOPE": "G0",
    "SCOPE_FROZEN": "G1",
    "INVENTORY_READY": "G2",
    "CALCULATED": "G3",
    "INTERPRETED": "G4",
    "REVIEWED": "G5",
    "RELEASED": "G6",
}

REQUIRED_FILES = (
    "study.yaml",
    "intake-brief.md",
    "study-plan.md",
    "work-receipt.json",
    "handoff.md",
    "handoff.json",
    "goal-and-scope.md",
    "process-map.md",
    "model-ledger.csv",
    "data-register.csv",
    "data-request.csv",
    "parameters.csv",
    "assumptions.csv",
    "scenario-register.csv",
    "balances.csv",
    "claims-register.csv",
    "decision-log.md",
    "qa-checklist.md",
    "review/review-plan.md",
    "review/review-findings.csv",
    "review/review-response-log.csv",
    "tool-runs/lcia-method-manifest.yaml",
    "tool-runs/calculation-request.yaml",
    "results/processed/impact-results.csv",
    "results/processed/contribution-results.csv",
    "results/release/release-manifest.json",
    "results/validation/validation-report.json",
    "report/report-outline.md",
)

CSV_REQUIRED_HEADERS = {
    "model-ledger.csv": {"model_item_id", "type", "name", "unit", "status"},
    "data-register.csv": {"data_id", "parameter_or_flow", "value", "unit", "source_class", "source_citation", "license", "review_status"},
    "data-request.csv": {"request_id", "requested_variable", "unit", "owner", "status"},
    "parameters.csv": {"parameter_id", "name", "value", "unit", "source_id", "status"},
    "assumptions.csv": {"assumption_id", "statement", "expected_influence", "status"},
    "scenario-register.csv": {"scenario_id", "name", "changed_parameters", "status"},
    "balances.csv": {"balance_id", "process_id", "metric", "direction", "value", "unit"},
    "claims-register.csv": {"claim_id", "proposed_claim", "audience", "required_review", "status"},
    "review/review-findings.csv": {"finding_id", "severity", "status"},
    "review/review-response-log.csv": {"response_id", "finding_id", "disposition", "status"},
    "results/processed/impact-results.csv": {"result_id", "impact_category", "value", "unit", "method_version"},
    "results/processed/contribution-results.csv": {"contribution_id", "result_id", "contributor_name", "value", "unit"},
}

UNIQUE_ID_COLUMNS = {
    "model-ledger.csv": "model_item_id",
    "data-register.csv": "data_id",
    "data-request.csv": "request_id",
    "parameters.csv": "parameter_id",
    "assumptions.csv": "assumption_id",
    "scenario-register.csv": "scenario_id",
    "claims-register.csv": "claim_id",
    "review/review-findings.csv": "finding_id",
    "review/review-response-log.csv": "response_id",
    "results/processed/impact-results.csv": "result_id",
    "results/processed/contribution-results.csv": "contribution_id",
}


def parse_simple_yaml(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or raw.startswith((" ", "\t")) or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        data[key.strip()] = value
    return data


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        rows = [dict(row) for row in reader]
    return headers, rows


def nonempty(value: str | None) -> bool:
    return bool(value and value.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("study", type=Path)
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()

    study = args.study.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not study.is_dir():
        print(f"ERROR: study directory not found: {study}", file=sys.stderr)
        return 1

    for rel in REQUIRED_FILES:
        path = study / rel
        if not path.exists():
            errors.append(f"missing required file: {rel}")
        elif path.stat().st_size == 0:
            errors.append(f"required file is empty: {rel}")

    metadata: dict[str, str] = {}
    metadata_path = study / "study.yaml"
    if metadata_path.exists():
        metadata = parse_simple_yaml(metadata_path)
        for key in ("schema_version", "study_id", "title", "status", "created", "updated"):
            if not nonempty(metadata.get(key)):
                errors.append(f"study.yaml missing value: {key}")
        study_id = metadata.get("study_id", "")
        if study_id and not SLUG_RE.fullmatch(study_id):
            errors.append("study_id must be lowercase hyphenated")
        if study_id and study.name != study_id:
            warnings.append(f"study directory '{study.name}' differs from study_id '{study_id}'")
        status = metadata.get("status", "")
        if status not in STATUS_ORDER:
            errors.append(f"unknown study status: {status!r}")
            status_rank = 0
        else:
            status_rank = STATUS_ORDER[status]

        current_gate = metadata.get("current_gate", "")
        if current_gate not in VALID_GATES:
            errors.append(f"unknown current_gate: {current_gate!r}")
        workflow_mode = metadata.get("workflow_mode", "")
        if workflow_mode not in VALID_WORKFLOW_MODES:
            errors.append(f"unknown workflow_mode: {workflow_mode!r}")
        try:
            plan_revision = int(metadata.get("plan_revision", ""))
            if plan_revision < 1:
                raise ValueError
        except ValueError:
            errors.append("plan_revision must be a positive integer")
        expected_gate = STATUS_MIN_GATE.get(status)
        if expected_gate and current_gate:
            if int(current_gate[1:]) < int(expected_gate[1:]):
                errors.append(f"{status} cannot have current_gate {current_gate}; expected {expected_gate} or later")

        for key in ("owner", "intended_use", "audience"):
            if not nonempty(metadata.get(key)):
                warnings.append(f"study.yaml has no {key}; complete before scope freeze")

        if status_rank >= STATUS_ORDER["SCOPE_FROZEN"]:
            for key in ("intended_use", "audience", "modeling_approach", "functional_unit", "reference_flow", "system_boundary", "geography", "reference_period"):
                if not nonempty(metadata.get(key)):
                    errors.append(f"{status} requires study.yaml value: {key}")
        if status_rank >= STATUS_ORDER["CALCULATED"]:
            for key in ("tool_name", "tool_version", "database_name", "database_version", "lcia_method", "lcia_method_version"):
                if not nonempty(metadata.get(key)):
                    errors.append(f"{status} requires study.yaml value: {key}")
    else:
        status_rank = 0

    row_cache: dict[str, list[dict[str, str]]] = {}
    for rel, required in CSV_REQUIRED_HEADERS.items():
        path = study / rel
        if not path.exists() or path.stat().st_size == 0:
            continue
        try:
            headers, rows = read_csv(path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"cannot parse {rel}: {exc}")
            continue
        row_cache[rel] = rows
        missing = required.difference(headers)
        if missing:
            errors.append(f"{rel} missing headers: {', '.join(sorted(missing))}")

        # Validate row-identity columns where the file contract defines one.
        id_col = UNIQUE_ID_COLUMNS.get(rel)
        if id_col:
            seen: set[str] = set()
            for number, row in enumerate(rows, start=2):
                ident = (row.get(id_col) or "").strip()
                if not ident:
                    warnings.append(f"{rel}:{number} missing {id_col}")
                elif ident in seen:
                    errors.append(f"{rel}:{number} duplicate {id_col} '{ident}'")
                seen.add(ident)

        for number, row in enumerate(rows, start=2):
            if "value" in row and nonempty(row.get("value")):
                try:
                    float((row.get("value") or "").replace(",", ""))
                except ValueError:
                    errors.append(f"{rel}:{number} value is not numeric: {row.get('value')!r}")
                if "unit" in row and not nonempty(row.get("unit")):
                    errors.append(f"{rel}:{number} has a value but no unit")

    if status_rank >= STATUS_ORDER["INVENTORY_READY"]:
        if not row_cache.get("model-ledger.csv"):
            errors.append("INVENTORY_READY or later requires populated model-ledger.csv")
        if not row_cache.get("data-register.csv"):
            errors.append("INVENTORY_READY or later requires populated data-register.csv")
        if not row_cache.get("parameters.csv"):
            warnings.append("inventory status has no parameter rows; verify whether the model is truly parameter-free")

    if status_rank >= STATUS_ORDER["CALCULATED"] and not row_cache.get("results/processed/impact-results.csv"):
        errors.append("CALCULATED or later requires impact result rows")

    findings = row_cache.get("review/review-findings.csv", [])
    if status_rank >= STATUS_ORDER["REVIEWED"]:
        open_material = [
            row for row in findings
            if (row.get("severity") or "").strip().lower() in {"critical", "major"}
            and (row.get("status") or "").strip().lower() not in {"closed", "accepted", "resolved"}
        ]
        if open_material:
            errors.append(f"{len(open_material)} critical/major review findings remain open")

    json_contracts = {
        "work-receipt.json": {"schema_version", "study_id", "receipt_id", "plan_revision", "authorized_task_ids", "tests"},
        "handoff.json": {"schema_version", "study_id", "study_status", "current_gate", "plan_revision", "next_task_ids"},
        "results/validation/validation-report.json": {"schema_version", "study_id", "validation_id", "target_gate", "readiness"},
        "results/release/release-manifest.json": {"schema_version", "study_id", "release_id", "review_status", "file_hashes"},
    }
    parsed_json: dict[str, dict[str, object]] = {}
    for rel, required_keys in json_contracts.items():
        path = study / rel
        if not path.exists():
            continue
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON in {rel}: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{rel} must contain a JSON object")
            continue
        parsed_json[rel] = value
        missing_keys = required_keys.difference(value)
        if missing_keys:
            errors.append(f"{rel} missing keys: {', '.join(sorted(missing_keys))}")
        json_study_id = str(value.get("study_id", ""))
        if json_study_id and metadata.get("study_id") and json_study_id != metadata["study_id"]:
            errors.append(f"{rel} study_id '{json_study_id}' differs from study.yaml")

    handoff = parsed_json.get("handoff.json", {})
    if handoff:
        if handoff.get("study_status") != metadata.get("status"):
            warnings.append("handoff.json study_status is not synchronized with study.yaml")
        if handoff.get("current_gate") != metadata.get("current_gate"):
            warnings.append("handoff.json current_gate is not synchronized with study.yaml")

    release = parsed_json.get("results/release/release-manifest.json", {})
    if status_rank >= STATUS_ORDER["RELEASED"]:
        if not nonempty(str(release.get("release_id", ""))):
            errors.append("RELEASED requires a release_id")
        if not release.get("file_hashes"):
            errors.append("RELEASED requires file hashes in the release manifest")
        if release.get("review_status") in {None, "", "not-reviewed"}:
            errors.append("RELEASED requires a documented review status")

    # Template placeholders must not remain after scaffolding.
    for rel in REQUIRED_FILES:
        path = study / rel
        if path.exists() and path.suffix.lower() in {".md", ".yaml", ".json"}:
            if "{{" in path.read_text(encoding="utf-8"):
                errors.append(f"unrendered template placeholder in {rel}")

    for message in errors:
        print(f"ERROR {message}")
    for message in warnings:
        print(f"WARN  {message}")
    print(f"Study validation: {len(errors)} errors, {len(warnings)} warnings; status={metadata.get('status', 'unknown')}.")

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

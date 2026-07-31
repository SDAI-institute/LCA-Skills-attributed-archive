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

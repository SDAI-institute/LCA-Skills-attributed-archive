#!/usr/bin/env python3
"""Create or repair an audit-ready LCA study workspace from repository templates."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = REPO_ROOT / "assets" / "templates"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

TARGETS = {
    "study.yaml": "study.yaml",
    "intake-brief.md": "intake-brief.md",
    "study-plan.md": "study-plan.md",
    "work-receipt.json": "work-receipt.json",
    "handoff.md": "handoff.md",
    "handoff.json": "handoff.json",
    "goal-and-scope.md": "goal-and-scope.md",
    "process-map.md": "process-map.md",
    "model-ledger.csv": "model-ledger.csv",
    "data-register.csv": "data-register.csv",
    "data-request.csv": "data-request.csv",
    "parameters.csv": "parameters.csv",
    "assumptions.csv": "assumptions.csv",
    "scenario-register.csv": "scenario-register.csv",
    "balances.csv": "balances.csv",
    "claims-register.csv": "claims-register.csv",
    "decision-log.md": "decision-log.md",
    "qa-checklist.md": "qa-checklist.md",
    "review-plan.md": "review/review-plan.md",
    "review-findings.csv": "review/review-findings.csv",
    "review-response-log.csv": "review/review-response-log.csv",
    "lcia-method-manifest.yaml": "tool-runs/lcia-method-manifest.yaml",
    "calculation-request.yaml": "tool-runs/calculation-request.yaml",
    "openlca-run-manifest.yaml": "tool-runs/openlca-run-manifest.yaml",
    "brightway-run-manifest.yaml": "tool-runs/brightway-run-manifest.yaml",
    "greet-run-manifest.yaml": "tool-runs/greet-run-manifest.yaml",
    "report-outline.md": "report/report-outline.md",
    "impact-results.csv": "results/processed/impact-results.csv",
    "contribution-results.csv": "results/processed/contribution-results.csv",
    "release-manifest.json": "results/release/release-manifest.json",
    "validation-report.json": "results/validation/validation-report.json",
}

DIRECTORIES = (
    "data/public",
    "data/private",
    "tool-runs",
    "review",
    "report",

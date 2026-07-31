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
    "results/raw",
    "results/processed",
    "results/validation",
    "results/figures",
    "results/release",
)


def resolve_output_root(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def render(text: str, slug: str, title: str) -> str:
    return (
        text.replace("{{SLUG}}", slug)
        .replace("{{TITLE}}", title)
        .replace("{{DATE}}", date.today().isoformat())
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="Lowercase hyphenated study identifier")
    parser.add_argument("--title", help="Human-readable study title")
    parser.add_argument(
        "--root",
        default="lca/studies",
        help="Study collection directory (default: lca/studies)",
    )
    parser.add_argument(
        "--overwrite-empty",
        action="store_true",
        help="Replace existing zero-byte files but never populated files",
    )
    args = parser.parse_args()

    if not SLUG_RE.fullmatch(args.slug):
        parser.error("slug must use lowercase letters/digits with internal hyphens")
    title = (args.title or args.slug.replace("-", " ").title()).strip()
    if not title:
        parser.error("title must not be empty")
    if not TEMPLATE_ROOT.exists():
        print(f"ERROR: template directory not found: {TEMPLATE_ROOT}", file=sys.stderr)
        return 1

    study = resolve_output_root(args.root) / args.slug
    study.mkdir(parents=True, exist_ok=True)
    for rel in DIRECTORIES:
        (study / rel).mkdir(parents=True, exist_ok=True)

    created: list[Path] = []
    skipped: list[Path] = []
    for source_name, target_name in TARGETS.items():
        source = TEMPLATE_ROOT / source_name
        target = study / target_name
        if not source.exists():
            print(f"ERROR: missing template: {source}", file=sys.stderr)
            return 1
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and (target.stat().st_size > 0 or not args.overwrite_empty):
            skipped.append(target)
            continue
        target.write_text(render(source.read_text(encoding="utf-8"), args.slug, title), encoding="utf-8")
        created.append(target)

    # Keep sensitive folders out of version control even when the parent project ignores differently.
    private_ignore = study / "data/private/.gitignore"
    if not private_ignore.exists():
        private_ignore.write_text("*\n!.gitignore\n", encoding="utf-8")
        created.append(private_ignore)
    raw_ignore = study / "results/raw/.gitignore"
    if not raw_ignore.exists():
        raw_ignore.write_text("*\n!.gitignore\n", encoding="utf-8")
        created.append(raw_ignore)

    print(f"Study workspace: {study}")
    print(f"Created {len(created)} files; preserved {len(skipped)} existing files.")
    print(f"Next: python scripts/validate_study.py {study}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Flag unsupported, high-risk, or unauthorized claims in an LCA study workspace."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

FORBIDDEN_OR_REVIEW_PHRASES = {
    r"\bISO[- ]?certified\b": "An LCA model or report is not ISO-certified by this plugin.",
    r"\bISO[- ]?compliant\b": "State addressed requirements and review status instead of an unqualified compliance claim.",
    r"\benvironmentally friendly\b": "Broad superiority claim requires a defined comparison and evidence.",
    r"\bzero environmental impact\b": "Absolute zero-impact claim is not supported by ordinary LCA.",
    r"\bcarbon neutral\b": "Separate inventory, removals, storage, offsets, claim standard, and verification.",
    r"\bnet[- ]negative\b": "Negative result requires boundary, credit, counterfactual, permanence, leakage, and uncertainty review.",
    r"\bmore sustainable\b": "Define dimensions, equivalence, categories, trade-offs, and review context.",
}
PUBLIC_AUDIENCES = {"public", "customer", "marketing", "regulatory", "epd", "pef", "external"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("study", type=Path)
    parser.add_argument("--warn-only", action="store_true")
    args = parser.parse_args()
    study = args.study.resolve()
    if not study.is_dir():
        print(f"ERROR: study directory not found: {study}", file=sys.stderr)
        return 1

    findings: list[str] = []
    register = study / "claims-register.csv"
    if register.exists():
        with register.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            for line, row in enumerate(reader, start=2):
                claim = (row.get("proposed_claim") or "").strip()
                audience = (row.get("audience") or "").strip().lower()
                status = (row.get("status") or "").strip().lower()
                required_review = (row.get("required_review") or "").strip()
                if claim and audience in PUBLIC_AUDIENCES and status not in {"authorized", "released", "approved"}:
                    findings.append(f"claims-register.csv:{line}: public/external claim is not authorized")
                if claim and ("compar" in claim.lower() or "better" in claim.lower() or "lower" in claim.lower()) and not required_review:
                    findings.append(f"claims-register.csv:{line}: comparative language has no required review route")

    for folder in (study / "report", study / "results/release"):
        if not folder.exists():
            continue
        for path in folder.rglob("*.md"):
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern, reason in FORBIDDEN_OR_REVIEW_PHRASES.items():
                for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                    line = text.count("\n", 0, match.start()) + 1
                    findings.append(f"{path.relative_to(study)}:{line}: {match.group(0)!r} — {reason}")

    for finding in findings:
        print(f"FLAG {finding}")
    print(f"Claim check: {len(findings)} flags.")
    return 0 if not findings or args.warn_only else 1


if __name__ == "__main__":
    sys.exit(main())

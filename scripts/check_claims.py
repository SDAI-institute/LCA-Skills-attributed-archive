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

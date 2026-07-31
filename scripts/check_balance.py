#!/usr/bin/env python3
"""Check mass, element, energy, water, or other balance closure from a study CSV."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path

INPUTS = {"input", "in", "feed", "inflow"}
OUTPUTS = {"output", "out", "product", "emission", "waste", "loss", "outflow"}
ACCUMULATIONS = {"accumulation", "stock-change", "stock_change", "stored"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--tolerance", type=float, default=0.01, help="Maximum relative residual (default 0.01 = 1%%)")
    parser.add_argument("--metric", help="Only check a named metric, e.g. mass or carbon")
    args = parser.parse_args()

    if args.tolerance < 0:
        parser.error("tolerance must be non-negative")
    if not args.csv_file.exists():
        print(f"ERROR: file not found: {args.csv_file}", file=sys.stderr)
        return 1

    groups: dict[tuple[str, str, str, str, str], dict[str, float]] = defaultdict(
        lambda: {"input": 0.0, "output": 0.0, "accumulation": 0.0, "rows": 0.0}
    )
    errors: list[str] = []
    with args.csv_file.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"balance_id", "process_id", "metric", "direction", "value", "unit"}
        missing = required.difference(reader.fieldnames or [])

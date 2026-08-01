#!/usr/bin/env python3
"""Compare two exported LCA result tables and fail on missing, unit-mismatched, or changed values."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path


def load(path: Path, key_columns: list[str], value_column: str, unit_column: str) -> dict[tuple[str, ...], tuple[float, str]]:
    output: dict[tuple[str, ...], tuple[float, str]] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = set(key_columns + [value_column, unit_column])
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path}: missing headers {', '.join(sorted(missing))}")
        for line, row in enumerate(reader, start=2):
            key = tuple((row.get(column) or "").strip() for column in key_columns)
            if key in output:
                raise ValueError(f"{path}:{line}: duplicate key {key}")
            try:
                value = float((row.get(value_column) or "").replace(",", ""))
            except ValueError as exc:
                raise ValueError(f"{path}:{line}: nonnumeric value") from exc
            if not math.isfinite(value):
                raise ValueError(f"{path}:{line}: nonfinite value")
            output[key] = (value, (row.get(unit_column) or "").strip())
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--keys", default="impact_category,indicator,scenario", help="Comma-separated key columns")
    parser.add_argument("--value", default="value", help="Numeric value column")
    parser.add_argument("--unit", default="unit", help="Unit column")
    parser.add_argument("--rtol", type=float, default=1e-6)
    parser.add_argument("--atol", type=float, default=0.0)
    parser.add_argument("--allow-differences", action="store_true", help="Report changes without failing")
    args = parser.parse_args()

    keys = [item.strip() for item in args.keys.split(",") if item.strip()]
    if not keys:
        parser.error("at least one key column is required")
    try:
        left = load(args.baseline, keys, args.value, args.unit)
        right = load(args.candidate, keys, args.value, args.unit)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    failures = 0
    for key in sorted(set(left) | set(right)):
        if key not in left:
            print(f"FAIL added key {key}")
            failures += 1
            continue
        if key not in right:
            print(f"FAIL missing key {key}")
            failures += 1
            continue
        old, old_unit = left[key]
        new, new_unit = right[key]
        if old_unit != new_unit:
            print(f"FAIL {key}: unit changed {old_unit!r} -> {new_unit!r}")
            failures += 1
            continue
        delta = new - old
        limit = args.atol + args.rtol * abs(old)
        passed = abs(delta) <= limit
        failures += int(not passed)
        rel = abs(delta) / abs(old) if old else (0.0 if delta == 0 else math.inf)
        print(
            f"{'PASS' if passed else 'FAIL'} {key}: baseline={old:.10g} candidate={new:.10g} "
            f"delta={delta:.10g} rel={rel:.3%} {old_unit}"
        )

    print(f"Compared {len(set(left) | set(right))} result keys; {failures} differences outside tolerance.")
    return 0 if not failures or args.allow_differences else 1


if __name__ == "__main__":
    sys.exit(main())

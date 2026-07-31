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
        if missing:
            print(f"ERROR: missing headers: {', '.join(sorted(missing))}", file=sys.stderr)
            return 1
        for line, row in enumerate(reader, start=2):
            metric = (row.get("metric") or "").strip().lower()
            if args.metric and metric != args.metric.strip().lower():
                continue
            direction = (row.get("direction") or "").strip().lower()
            try:
                value = float((row.get("value") or "").replace(",", ""))
            except ValueError:
                errors.append(f"line {line}: nonnumeric value {row.get('value')!r}")
                continue
            if not math.isfinite(value):
                errors.append(f"line {line}: value is not finite")
                continue
            key = (
                (row.get("balance_id") or "").strip(),
                (row.get("process_id") or "").strip(),
                metric,
                (row.get("unit") or "").strip(),
                (row.get("scenario") or "baseline").strip(),
            )
            if direction in INPUTS:
                groups[key]["input"] += value
            elif direction in OUTPUTS:
                groups[key]["output"] += value
            elif direction in ACCUMULATIONS:
                groups[key]["accumulation"] += value
            else:
                errors.append(f"line {line}: unknown direction {direction!r}")
                continue
            groups[key]["rows"] += 1

    failures = 0
    if not groups and not errors:
        errors.append("no balance rows matched")
    for key, values in sorted(groups.items()):
        balance_id, process_id, metric, unit, scenario = key
        residual = values["input"] - values["output"] - values["accumulation"]
        denominator = max(abs(values["input"]), abs(values["output"] + values["accumulation"]), 1e-30)
        relative = abs(residual) / denominator
        passed = relative <= args.tolerance
        failures += int(not passed)
        print(
            f"{'PASS' if passed else 'FAIL'} {balance_id or '-'} {process_id or '-'} "
            f"{metric or '-'} [{scenario}] input={values['input']:.8g} "
            f"output={values['output']:.8g} accumulation={values['accumulation']:.8g} "
            f"residual={residual:.8g} {unit} relative={relative:.3%}"
        )

    for message in errors:
        print(f"ERROR {message}", file=sys.stderr)
    print(f"Checked {len(groups)} balances; {failures} failed; {len(errors)} input errors.")
    return 1 if failures or errors else 0


if __name__ == "__main__":
    sys.exit(main())

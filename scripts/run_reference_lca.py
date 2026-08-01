#!/usr/bin/env python3
"""Solve and verify the repository's synthetic matrix LCA reference system.

This is a software/integration fixture, not an environmental method or dataset.
It uses a small technology matrix, biosphere inventory, and deliberately
synthetic characterization factors with analytically known results.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASE = ROOT / "tests/integration/fixtures/synthetic-matrix"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    """Solve a dense square system with partial-pivot Gaussian elimination."""
    n = len(vector)
    aug = [row[:] + [vector[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(aug[row][col]))
        if math.isclose(aug[pivot][col], 0.0, abs_tol=1e-15):
            raise ValueError("Singular technology matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        divisor = aug[col][col]
        aug[col] = [value / divisor for value in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if factor == 0:
                continue
            aug[row] = [a - factor * b for a, b in zip(aug[row], aug[col])]
    return [aug[i][-1] for i in range(n)]


def close(actual: float, expected: float, rtol: float, atol: float) -> bool:
    return abs(actual - expected) <= atol + rtol * abs(expected)


def calculate(case: Path) -> dict[str, dict[str, float]]:
    processes = read_csv(case / "processes.csv")
    ids = [row["process_id"] for row in processes]
    index = {process_id: i for i, process_id in enumerate(ids)}
    if len(index) != len(ids):
        raise ValueError("Duplicate process_id")

    n = len(ids)
    technology = [[0.0] * n for _ in range(n)]
    for column, row in enumerate(processes):
        technology[column][column] = float(row["reference_amount"])

    for row in read_csv(case / "technosphere.csv"):
        consumer = index[row["consumer_process_id"]]
        provider = index[row["provider_process_id"]]
        amount = float(row["amount_per_consumer_reference"])
        if consumer == provider and math.isclose(amount, 0.0, abs_tol=0.0):
            continue
        technology[provider][consumer] -= amount

    demand = [0.0] * n
    for row in read_csv(case / "demand.csv"):
        demand[index[row["process_id"]]] += float(row["amount"])

    scaling_vector = solve(technology, demand)
    scaling = {process_id: scaling_vector[index[process_id]] for process_id in ids}

    inventory: dict[tuple[str, str], float] = defaultdict(float)
    for row in read_csv(case / "biosphere.csv"):
        process_scale = scaling[row["process_id"]]
        key = (row["flow_id"], row["direction"])
        inventory[key] += float(row["amount_per_process_reference"]) * process_scale

    impacts: dict[str, float] = defaultdict(float)
    for row in read_csv(case / "characterization.csv"):
        key = (row["flow_id"], row["direction"])
        impacts[row["indicator_id"]] += inventory.get(key, 0.0) * float(row["characterization_factor"])

    return {
        "scaling": scaling,
        "inventory": {flow: value for (flow, _direction), value in inventory.items()},
        "impact": dict(impacts),
    }


def expected_rows(path: Path) -> Iterable[tuple[str, str, float, str]]:
    for row in read_csv(path):
        yield row["result_type"], row["result_id"], float(row["amount"]), row["unit"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, default=DEFAULT_CASE)
    parser.add_argument("--expected", type=Path)
    parser.add_argument("--rtol", type=float, default=1e-9)
    parser.add_argument("--atol", type=float, default=1e-12)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    case = args.case.resolve()
    expected = args.expected or case / "expected-results.csv"
    results = calculate(case)
    failures: list[dict[str, object]] = []
    checks: list[dict[str, object]] = []
    for result_type, result_id, target, unit in expected_rows(expected):
        actual = results.get(result_type, {}).get(result_id)
        passed = actual is not None and close(actual, target, args.rtol, args.atol)
        item = {
            "result_type": result_type,
            "result_id": result_id,
            "actual": actual,
            "expected": target,
            "unit": unit,
            "passed": passed,
        }
        checks.append(item)
        if not passed:
            failures.append(item)

    payload = {
        "case": str(case),
        "scientific_use": False,
        "purpose": "software and cross-tool integration verification only",
        "technology_matrix_convention": "outputs on diagonal; required provider inputs negative by column",
        "results": results,
        "checks": checks,
        "passed": not failures,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for item in checks:
            status = "PASS" if item["passed"] else "FAIL"
            print(f"{status} {item['result_type']}:{item['result_id']} actual={item['actual']} expected={item['expected']} {item['unit']}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())

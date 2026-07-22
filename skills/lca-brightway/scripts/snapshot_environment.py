#!/usr/bin/env python3
"""Create a non-invasive Brightway ecosystem environment snapshot."""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

DISTRIBUTIONS = (
    "brightway25",
    "brightway2",
    "bw2data",
    "bw2calc",
    "bw2io",
    "bw-processing",
    "stats-arrays",
    "activity-browser",
    "premise",
    "wurst",
    "bw-temporalis",
    "bw-timex",
    "bw2regional",
)
MODULES = (
    "bw2data",
    "bw2calc",
    "bw2io",
    "bw_processing",
    "stats_arrays",
    "activity_browser",
    "premise",
    "wurst",
    "bw_temporalis",
    "bw_timex",
    "bw2regional",
)


def version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def visible(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    distributions = {name: version(name) for name in DISTRIBUTIONS}
    modules = {name: visible(name) for name in MODULES}
    payload = {
        "schema_version": "1.0",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "distributions": distributions,
        "modules_visible": modules,
        "generation_signals": {
            "brightway25_distribution": distributions["brightway25"],
            "legacy_brightway2_distribution": distributions["brightway2"],
            "core_packages_visible": all(modules[name] for name in ("bw2data", "bw2calc", "bw2io")),
        },
        "required_runtime_fields": {
            "brightway_project": None,
            "project_directory_or_export_hash": None,
            "database_names_versions_system_models": [],
            "method_names_versions": [],
            "random_seed_policy": None,
        },
    }

    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

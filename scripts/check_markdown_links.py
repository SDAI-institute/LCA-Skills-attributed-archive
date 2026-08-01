#!/usr/bin/env python3
"""Validate all local Markdown links in the source repository."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from repo_checks import find_broken_markdown_links

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    root = args.path.resolve()
    checked, broken = find_broken_markdown_links(root)
    payload = {
        "root": str(root),
        "checked_local_links": checked,
        "broken_links": [
            {
                "source": str(item.source.relative_to(root)),
                "line": item.line,
                "target": item.target,
                "resolved": str(item.resolved),
            }
            for item in broken
        ],
        "status": "PASS" if not broken else "FAIL",
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    elif not args.quiet or broken:
        for item in broken:
            print(f"ERROR {item.render(root)}")
        print(f"Checked {checked} local Markdown links; {len(broken)} broken.")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())

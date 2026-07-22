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

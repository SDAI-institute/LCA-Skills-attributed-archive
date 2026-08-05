#!/usr/bin/env python3
"""Dependency-free MCP stdio server for LCA Skills.

The server implements the 2025-11-25 lifecycle and a conservative subset of
resources and tools. It writes only JSON-RPC messages to stdout; diagnostics go
to stderr.
"""

from __future__ import annotations

import json
import os
import sys
import traceback
from pathlib import Path
from typing import Any, Callable

# Support direct execution from a plugin path.
HERE = Path(__file__).resolve()
if str(HERE.parents[1]) not in sys.path:
    sys.path.insert(0, str(HERE.parents[1]))

from lca_tools import __version__  # noqa: E402
from lca_tools import brightway, doctor, greet, openlca, workspace  # noqa: E402
from lca_tools.common import LCAToolError, root_dir  # noqa: E402

PROTOCOL_VERSION = "2025-11-25"


def schema(properties: dict[str, Any], required: list[str] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {"type": "object", "properties": properties, "additionalProperties": False}
    if required:
        value["required"] = required
    return value


def tool(name: str, description: str, input_schema: dict[str, Any], *, read_only: bool, destructive: bool = False, idempotent: bool = True, open_world: bool = False) -> dict[str, Any]:
    return {
        "name": name,
        "description": description,
        "inputSchema": input_schema,
        "annotations": {
            "readOnlyHint": read_only,
            "destructiveHint": destructive,
            "idempotentHint": idempotent,
            "openWorldHint": open_world,
        },
    }


TOOLS = [
    tool("lca_doctor", "Run non-invasive host, package, repository, and optional local openLCA endpoint diagnostics.", schema({
        "check_openlca": {"type": "boolean", "default": False},
        "host": {"type": "string", "default": "127.0.0.1"},
        "port": {"type": "integer", "minimum": 1, "maximum": 65535, "default": 8080},
        "timeout": {"type": "number", "minimum": 0.1, "maximum": 30, "default": 1.0},
    }), read_only=True),
    tool("lca_new_study", "Create or repair a durable LCA study workspace from bundled templates.", schema({
        "slug": {"type": "string", "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$"},
        "title": {"type": "string"},
        "root": {"type": "string", "description": "Destination collection directory; defaults to <project>/lca/studies"},
        "overwrite_empty": {"type": "boolean", "default": False},
    }, ["slug"]), read_only=False, destructive=False, idempotent=True),
    tool("lca_validate_study", "Validate LCA study structure and gate readiness without modifying it.", schema({
        "study": {"type": "string"}, "strict": {"type": "boolean", "default": False},
    }, ["study"]), read_only=True),
    tool("lca_check_balance", "Check mass, energy, carbon, water, or elemental balance closure from a study CSV.", schema({
        "csv_file": {"type": "string"},
        "tolerance": {"type": "number", "minimum": 0, "default": 0.01},
        "metric": {"type": "string"},
    }, ["csv_file"]), read_only=True),
    tool("lca_check_claims", "Flag unsupported or review-sensitive claims in an LCA study workspace.", schema({
        "study": {"type": "string"}, "warn_only": {"type": "boolean", "default": False},
    }, ["study"]), read_only=True),
    tool("lca_compare_results", "Compare two exported LCA result tables with explicit keys, units, and tolerances.", schema({
        "baseline": {"type": "string"}, "candidate": {"type": "string"},
        "keys": {"type": "string", "default": "impact_category,indicator,scenario"},
        "value": {"type": "string", "default": "value"},
        "unit": {"type": "string", "default": "unit"},
        "rtol": {"type": "number", "minimum": 0, "default": 1e-6},
        "atol": {"type": "number", "minimum": 0, "default": 0},
        "allow_differences": {"type": "boolean", "default": False},
    }, ["baseline", "candidate"]), read_only=True),
    tool("openlca_snapshot", "Inspect openLCA Python-client visibility and optionally test a local endpoint.", schema({
        "host": {"type": "string", "default": "127.0.0.1"},
        "port": {"type": "integer", "minimum": 1, "maximum": 65535, "default": 8080},
        "check_endpoint": {"type": "boolean", "default": False},
        "timeout": {"type": "number", "minimum": 0.1, "maximum": 30, "default": 1.0},
    }), read_only=True),
    tool("openlca_list_descriptors", "List model descriptors from a trusted local openLCA IPC endpoint.", schema({
        "entity_type": {"type": "string"}, "host": {"type": "string", "default": "127.0.0.1"},
        "port": {"type": "integer", "default": 8080}, "limit": {"type": "integer", "minimum": 1, "maximum": 10000, "default": 1000},
    }, ["entity_type"]), read_only=True),
    tool("openlca_calculate", "Run a read-only product-system calculation through the current schema-separated openLCA IPC client and dispose the result.", schema({
        "product_system_id": {"type": "string"}, "impact_method_id": {"type": ["string", "null"]},
        "amount": {"type": "number", "exclusiveMinimum": 0, "default": 1.0},
        "host": {"type": "string", "default": "127.0.0.1"}, "port": {"type": "integer", "default": 8080},
        "include_inventory": {"type": "boolean", "default": True},
    }, ["product_system_id"]), read_only=True),
    tool("brightway_snapshot", "Inspect installed Brightway packages and projects without creating or changing data.", schema({}), read_only=True),
    tool("brightway_calculate", "Run a read-only Brightway LCI/LCIA for an existing project, activity, amount, and method tuple.", schema({
        "project": {"type": "string"}, "database": {"type": "string"}, "code": {"type": "string"},
        "method": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "amount": {"type": "number", "exclusiveMinimum": 0, "default": 1.0},
    }, ["project", "database", "code", "method"]), read_only=True),
    tool("greet_build_manifest", "Create a provenance manifest for an exact GREET product/release without copying licensed model contents.", schema({
        "study_id": {"type": "string"}, "product": {"type": "string", "default": "R&D GREET"},
        "release": {"type": "string"}, "revision": {"type": "string"}, "platform": {"type": "string"},
        "doi": {"type": "string"}, "model_file": {"type": "string"}, "input_export": {"type": "string"},
        "result_export": {"type": "string"}, "pathway": {"type": "string"}, "boundary": {"type": "string"},
        "functional_basis": {"type": "string"}, "output": {"type": "string"},
    }, ["study_id", "release", "platform", "output"]), read_only=False, destructive=False, idempotent=True),
    tool("greet_import_results", "Validate and normalize a GREET CSV export with indicator, value, and unit columns.", schema({
        "csv_file": {"type": "string"}, "output": {"type": "string"},
    }, ["csv_file"]), read_only=True),
]
TOOL_MAP = {item["name"]: item for item in TOOLS}


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


def default_study_root() -> str:
    base = Path(os.environ.get("LCA_PROJECT_ROOT", Path.cwd()))
    return str((base / "lca" / "studies").resolve())


def call_tool(name: str, args: dict[str, Any]) -> Any:
    if name == "lca_doctor":
        return doctor.snapshot(
            check_openlca=bool(args.get("check_openlca", False)), host=args.get("host", "127.0.0.1"),
            port=int(args.get("port", 8080)), timeout=float(args.get("timeout", 1.0)),
        )
    if name == "lca_new_study":
        return workspace.new_study(
            args["slug"], args.get("title"), args.get("root") or default_study_root(),
            overwrite_empty=bool(args.get("overwrite_empty", False)),
        )
    if name == "lca_validate_study":
        return workspace.validate_study(args["study"], strict=bool(args.get("strict", False)))
    if name == "lca_check_balance":
        return workspace.check_balance(args["csv_file"], tolerance=float(args.get("tolerance", 0.01)), metric=args.get("metric"))
    if name == "lca_check_claims":
        return workspace.check_claims(args["study"], warn_only=bool(args.get("warn_only", False)))
    if name == "lca_compare_results":
        return workspace.compare_results(
            args["baseline"], args["candidate"], keys=args.get("keys", "impact_category,indicator,scenario"),
            value=args.get("value", "value"), unit=args.get("unit", "unit"),
            rtol=float(args.get("rtol", 1e-6)), atol=float(args.get("atol", 0)),
            allow_differences=bool(args.get("allow_differences", False)),
        )
    if name == "openlca_snapshot":
        return openlca.snapshot(
            host=args.get("host", "127.0.0.1"), port=int(args.get("port", 8080)),
            check_endpoint=bool(args.get("check_endpoint", False)), timeout=float(args.get("timeout", 1.0)),
        )
    if name == "openlca_list_descriptors":
        return openlca.list_descriptors(
            args["entity_type"], host=args.get("host", "127.0.0.1"),
            port=int(args.get("port", 8080)), limit=int(args.get("limit", 1000)),
        )
    if name == "openlca_calculate":
        return openlca.calculate(
            args["product_system_id"], args.get("impact_method_id"), amount=float(args.get("amount", 1.0)),
            host=args.get("host", "127.0.0.1"), port=int(args.get("port", 8080)),
            include_inventory=bool(args.get("include_inventory", True)),
        )
    if name == "brightway_snapshot":
        return brightway.snapshot()
    if name == "brightway_calculate":
        return brightway.calculate(args["project"], args["database"], args["code"], args["method"], amount=float(args.get("amount", 1.0)))
    if name == "greet_build_manifest":
        return greet.build_manifest(
            study_id=args["study_id"], product=args.get("product", "R&D GREET"), release=args["release"],
            revision=args.get("revision", ""), platform=args["platform"], doi=args.get("doi", ""),
            model_file=args.get("model_file"), input_export=args.get("input_export"), result_export=args.get("result_export"),
            pathway=args.get("pathway", ""), boundary=args.get("boundary", ""), functional_basis=args.get("functional_basis", ""),
            output=args["output"],
        )
    if name == "greet_import_results":
        return greet.import_results(args["csv_file"], output=args.get("output"))
    raise LCAToolError(f"Unknown tool: {name}")


def text_result(payload: Any, *, is_error: bool = False) -> dict[str, Any]:
    return {
        "content": [{"type": "text", "text": json.dumps(payload, indent=2, sort_keys=True)}],
        "structuredContent": payload if isinstance(payload, dict) else {"result": payload},
        "isError": is_error,
    }


def resources() -> list[dict[str, Any]]:
    return [
        {"uri": "lca://skill-catalog", "name": "LCA Skills catalog", "mimeType": "text/markdown"},
        {"uri": "lca://source-register", "name": "LCA authoritative source register", "mimeType": "text/markdown"},
        {"uri": "lca://architecture", "name": "LCA Skills architecture", "mimeType": "text/markdown"},
    ]


def read_resource(uri: str) -> str:
    mapping = {
        "lca://skill-catalog": root_dir() / "docs" / "skill-catalog.md",
        "lca://source-register": root_dir() / "docs" / "source-register.md",
        "lca://architecture": root_dir() / "docs" / "architecture.md",
    }
    path = mapping.get(uri)
    if path is None or not path.exists():
        raise LCAToolError(f"Unknown or unavailable resource: {uri}")
    return path.read_text(encoding="utf-8")


def success(request_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def error(request_id: Any, code: int, message: str, data: Any = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        payload["data"] = data
    return {"jsonrpc": "2.0", "id": request_id, "error": payload}


def handle(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    request_id = message.get("id")
    params = message.get("params") or {}
    if request_id is None:
        return None
    if method == "initialize":
        requested = params.get("protocolVersion", PROTOCOL_VERSION)
        protocol = requested if requested in {PROTOCOL_VERSION, "2025-06-18", "2025-03-26"} else PROTOCOL_VERSION
        return success(request_id, {
            "protocolVersion": protocol,
            "capabilities": {"tools": {"listChanged": False}, "resources": {"subscribe": False, "listChanged": False}},
            "serverInfo": {"name": "sdai-lca-tools", "title": "SDAI LCA Tools", "version": __version__},
            "instructions": "Use validation and read-only calculations as evidence; methodological and review gates still apply.",
        })
    if method == "ping":
        return success(request_id, {})
    if method == "tools/list":
        return success(request_id, {"tools": TOOLS})
    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if name not in TOOL_MAP:
            return error(request_id, -32602, f"Unknown tool: {name}")
        try:
            return success(request_id, text_result(call_tool(name, arguments)))
        except (LCAToolError, OSError, ValueError, KeyError) as exc:
            return success(request_id, text_result({"error": type(exc).__name__, "message": str(exc)}, is_error=True))
    if method == "resources/list":
        return success(request_id, {"resources": resources()})
    if method == "resources/read":
        try:
            uri = params["uri"]
            return success(request_id, {"contents": [{"uri": uri, "mimeType": "text/markdown", "text": read_resource(uri)}]})
        except (KeyError, LCAToolError, OSError) as exc:
            return error(request_id, -32602, str(exc))
    if method == "prompts/list":
        return success(request_id, {"prompts": []})
    return error(request_id, -32601, f"Method not found: {method}")


def emit(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def process(value: Any) -> None:
    if isinstance(value, list):
        responses = [response for item in value if isinstance(item, dict) and (response := handle(item)) is not None]
        if responses:
            emit(responses)  # type: ignore[arg-type]
        return
    if isinstance(value, dict):
        response = handle(value)
        if response is not None:
            emit(response)
        return
    emit(error(None, -32600, "Invalid Request"))


def main() -> int:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            process(json.loads(line))
        except json.JSONDecodeError as exc:
            emit(error(None, -32700, "Parse error", str(exc)))
        except Exception as exc:  # pragma: no cover - keep protocol alive on unexpected integrations
            print(traceback.format_exc(), file=sys.stderr)
            emit(error(None, -32603, "Internal error", f"{type(exc).__name__}: {exc}"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Produce an evidence-based qualification matrix without overstating unavailable hosts or LCA tools."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], *, cwd: Path = ROOT, input_text: str | None = None, timeout: float = 120) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            command,
            cwd=cwd,
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "FAIL", "command": command, "error": f"{type(exc).__name__}: {exc}"}
    return {
        "status": "PASS" if proc.returncode == 0 else "FAIL",
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-8000:],
        "stderr": proc.stderr[-8000:],
    }


def executable_status(name: str) -> dict[str, Any]:
    path = shutil.which(name)
    if not path:
        return {"status": "NOT_INSTALLED", "path": None, "version": None}
    probe = run([path, "--version"], timeout=10)
    output = (probe.get("stdout") or probe.get("stderr") or "").strip().splitlines()
    return {
        "status": "DETECTED" if probe.get("returncode") == 0 else "DETECTED_UNQUALIFIED",
        "path": path,
        "version": output[0] if output else None,
        "note": "Executable detection is not proof that this plugin was imported or invoked successfully.",
    }


def module_status(name: str) -> dict[str, Any]:
    spec = importlib.util.find_spec(name)
    return {"status": "DETECTED" if spec else "NOT_INSTALLED", "module": name, "origin": getattr(spec, "origin", None) if spec else None}


def tcp_status(host: str, port: int, timeout: float) -> dict[str, Any]:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return {
                "status": "REACHABLE_UNQUALIFIED",
                "host": host,
                "port": port,
                "note": "Transport reachability does not identify openLCA, a database, or a scientifically valid model.",
            }
    except OSError as exc:
        return {"status": "NOT_REACHABLE", "host": host, "port": port, "error": f"{type(exc).__name__}: {exc}"}


def mcp_smoke() -> dict[str, Any]:
    messages = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-11-25",
                "capabilities": {},
                "clientInfo": {"name": "lca-skills-qualification", "version": "0.2.0"},
            },
        },
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {"jsonrpc": "2.0", "id": 3, "method": "resources/list", "params": {}},
    ]
    result = run(
        [sys.executable, "lca_tools/mcp_server.py"],
        input_text="".join(json.dumps(message) + "\n" for message in messages),
        timeout=30,
    )
    if result["status"] != "PASS":
        return result
    try:
        responses = [json.loads(line) for line in result["stdout"].splitlines() if line.strip()]
        by_id = {item.get("id"): item for item in responses}
        tools = by_id[2]["result"]["tools"]
        resources = by_id[3]["result"]["resources"]
        protocol = by_id[1]["result"]["protocolVersion"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        return {"status": "FAIL", "error": f"Invalid MCP response: {exc}", "raw": result}
    names = [item.get("name") for item in tools]
    return {
        "status": "PASS" if len(tools) == 13 and protocol == "2025-11-25" else "FAIL",
        "protocol_version": protocol,
        "tool_count": len(tools),
        "tool_names": names,
        "resource_count": len(resources),
        "stderr": result.get("stderr", ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-openlca", action="store_true", help="Perform an explicit local TCP transport check")
    parser.add_argument("--openlca-host", default="127.0.0.1")
    parser.add_argument("--openlca-port", type=int, default=8080)
    parser.add_argument("--skip-tests", action="store_true")
    args = parser.parse_args()

    source = run([sys.executable, "scripts/validate_repo.py", "--strict"])
    distributions = run([sys.executable, "scripts/validate_distributions.py"])
    source_release = run([sys.executable, "scripts/build_source_release.py", "--json"])
    installed_plugin = run([
        sys.executable,
        "scripts/validate_active_plugin.py",
        "dist/claude-code/lca-skills",
        "--strict",
    ])
    unit_tests = (
        {"status": "NOT_TESTED", "reason": "--skip-tests was supplied"}
        if args.skip_tests
        else run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"], timeout=300)
    )
    synthetic = run([sys.executable, "scripts/run_reference_lca.py", "--json"])

    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "qualification_model": {
            "structural": "Static package, frontmatter, reference, manifest, hash and ZIP checks.",
            "runtime": "A representative command executed in the current environment.",
            "host": "The package was imported and invoked in the actual target product.",
            "scientific": "Known-case results were reconciled with method, data and practitioner review.",
        },
        "local_evidence": {
            "source_repository": source,
            "distributions": distributions,
            "source_release": source_release,
            "generated_claude_plugin": installed_plugin,
            "unit_tests": unit_tests,
            "mcp_stdio": mcp_smoke(),
            "synthetic_matrix_fixture": {
                **synthetic,
                "scope": "Software regression fixture only; explicitly not a scientific LCIA validation.",
            },
        },
        "target_hosts": {
            "claude_code": {
                **executable_status("claude"),
                "package": "dist/packages/LCA-Skills-ClaudeCode-v0.2.0.zip",
                "required_manual_test": "Load with --plugin-dir, run /lca-skills:lca-doctor and /lca-skills:lca-expert, inspect agents/hooks/MCP, and record transcript.",
            },
            "claude_code_standalone": {
                **executable_status("claude"),
                "package": "dist/packages/LCA-Skills-ClaudeStandalone-v0.2.0.zip",
                "required_manual_test": "Install into ~/.claude/skills, restart, invoke /lca-expert, and verify explicit-only /lca-autopilot.",
            },
            "claude_ai": {
                "status": "NOT_TESTED",
                "package": "dist/packages/LCA-Skills-ClaudeAI-v0.2.0.zip",
                "reason": "Requires upload and invocation in an eligible Claude.ai account; no browser/account automation is performed.",
            },
            "chatgpt": {
                "status": "NOT_TESTED",
                "package": "dist/packages/LCA-Skills-ChatGPT-v0.2.0.zip",
                "reason": "Requires upload scan, installation and activation test in an eligible ChatGPT account; no account automation is performed.",
            },
            "codex": {
                **executable_status("codex"),
                "package": "dist/packages/LCA-Skills-Codex-v0.2.0.zip",
                "required_manual_test": "Install/import the plugin, invoke $lca-expert using the syntax shown by that Codex build, and capture output.",
            },
        },
        "optional_lca_tools": {
            "openlca_python": {
                "olca_ipc": module_status("olca_ipc"),
                "olca_schema": module_status("olca_schema"),
                "endpoint": tcp_status(args.openlca_host, args.openlca_port, 1.0) if args.check_openlca else {
                    "status": "NOT_TESTED",
                    "reason": "Endpoint checks are opt-in to avoid probing an unintended local service.",
                },
                "scientific_status": "NOT_TESTED",
            },
            "brightway": {
                "bw2data": module_status("bw2data"),
                "bw2calc": module_status("bw2calc"),
                "bw2io": module_status("bw2io"),
                "scientific_status": "NOT_TESTED",
            },
            "greet": {
                "dotnet": executable_status("dotnet"),
                "status": "NOT_TESTED",
                "reason": "No licensed/local GREET model and pathway export were supplied for reconciliation.",
            },
        },
    }

    local_fail = any(
        value.get("status") == "FAIL"
        for value in payload["local_evidence"].values()
        if isinstance(value, dict)
    )
    payload["overall_local_status"] = "FAIL" if local_fail else "PASS"
    payload["release_statement"] = (
        "Structurally qualified and locally regression-tested. Actual ChatGPT, Claude.ai, Claude Code, Codex, openLCA, Brightway and GREET qualification remains exactly as recorded above."
    )

    rendered = json.dumps(payload, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 1 if local_fail else 0


if __name__ == "__main__":
    sys.exit(main())

---
name: lca-doctor
description: "Diagnose LCA Skills host, Python, plugin, MCP, openLCA, Brightway, GREET, database, and study-workspace readiness without mutating models. Use during setup, after upgrades, or when commands/adapters are unavailable."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---

# LCA Skills Doctor

Run non-invasive qualification before trusting a new host or tool environment.

Read `references/diagnostic-matrix.md` and `references/host-commands.md`.

## Checks

1. Identify host and invocation mode: Claude Code plugin, standalone Claude skill, Claude.ai/ChatGPT skill, Codex plugin, or generic Agent Skills host.
2. Validate portable skill frontmatter, manifests, agents, hooks, MCP configuration, reference links, and version synchronization.
3. Record Python and optional package versions.
4. Detect openLCA clients and, only when explicitly requested, test a local endpoint. A reachable port does not validate database identity.
5. Detect Brightway packages/projects without creating or mutating projects.
6. Record the exact GREET product/release/runner supplied by the user; do not infer that one GREET model represents another.
7. Validate a named study workspace and its release blockers.
8. Report each capability as `PASS`, `WARN`, `FAIL`, `NOT INSTALLED`, `NOT TESTED`, or `MANUAL CHECK`.

Use the bundled command when available:

```bash
python -m lca_tools.cli doctor
```

In a Claude Code plugin distribution, the bundled MCP server exposes the same doctor as `lca_doctor`.

## Qualification language

Distinguish structural validation, local smoke testing, scientific benchmark reconciliation, and real-host integration testing. Never describe a host/tool as qualified merely because files parse or a port is open.

---
name: lca-openlca
description: "Build, automate, calculate, troubleshoot, and validate LCA models in openLCA 2 using the GUI, JSON-LD/openLCA schema, and IPC clients. Use for databases, processes, product systems, parameters, allocation, projects, uncertainty, Monte Carlo, contribution analysis, imports/exports, or openLCA API workflows."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---
# openLCA Specialist

Use the installed openLCA version and official documentation as the source of truth. Record desktop/server, database, IPC client, and schema versions.

## Safety first

- Work on a copy or versioned database before automated mutation.
- Bind IPC to localhost unless explicitly secured.
- Confirm the active database; IPC operations act on it.
- Use stable UUIDs/identifiers, not names alone, after discovery.
- Dispose calculation and simulator objects.
- Never assume allocation factors automatically refresh; verify saved factors before product-system calculation.

## Choose a workflow

Read:

- `references/gui-workflow.md` for interactive modeling;
- `references/ipc-workflow.md` for Python/JSON-RPC/REST automation;
- `references/import-export.md` for JSON-LD, ILCD, ecoSpold, Excel, and package exchange;
- `references/calculation-analysis.md` for calculation, contribution, projects, scenarios, and Monte Carlo;
- `references/troubleshooting.md` for errors and QA.

## Standard model build

1. Confirm database/system model, units, flows, locations, and impact method.
2. Create or inspect foreground flows and processes.
3. Set quantitative reference and provider links.
4. Add parameters with units documented in comments/metadata.
5. Calculate and save allocation factors if required.
6. Create/link the product system using the intended provider policy.
7. Inspect the model graph for unlinked, duplicate, or unintended providers.

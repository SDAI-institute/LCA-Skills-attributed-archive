---
name: lca-calculate
description: "Run or design reproducible LCA calculations, select the appropriate openLCA, Brightway, GREET, or transparent calculation adapter, capture run manifests, and reconcile outputs. Use after inventory QA or when repeating/calibrating calculations."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---

# LCA Calculation Orchestrator

Calculation is a controlled experiment over a versioned model, not a button press.

Read `references/calculation-contract.md`, `references/tool-routing.md`, and `references/result-reconciliation.md`.

## Preconditions

Require an explicit functional unit/reference flow, boundary, model approach, scenario, database/system model, LCIA method, parameter set, and passed inventory QA. If any is missing, return to `lca-scope`, `lca-inventory`, or `lca-validate`.

## Tool routing

- Invoke `lca-openlca` for GUI/IPC product-system work and openLCA database interoperability.
- Invoke `lca-brightway` for Python-native matrices, scenarios, custom inventories, and reproducible research pipelines.
- Invoke `lca-greet` for a named Argonne GREET product/release/pathway and its defined boundary.
- Use a transparent spreadsheet or matrix calculation only when its equations, units, factors, and provenance are auditable.

The bundled CLI and MCP adapter expose read-only calculations and validation utilities where the local software is available. Run `lca-doctor` before relying on an unqualified environment.

## Calculation contract

1. Create a calculation request and immutable run ID.
2. Record tool/client/server, database/system model, LCIA implementation, model IDs, scenario, parameters, random seed where relevant, and input hashes.
3. Calculate the inventory before impacts and inspect nonzero elementary-flow coverage.
4. Export raw unrounded results and contribution data before visualization.
5. Dispose server-side results and close resources.
6. Run sign, unit, magnitude, mapping, total/contribution reconciliation, and cross-scenario consistency checks.
7. Preserve errors and failed iterations; do not silently drop them.
8. Save run manifest, raw output, processed output, and a calculation receipt.

## Completion gate

A calculation is valid for interpretation only when its identity is reproducible, reference amount and method are verified, result totals reconcile, missing mappings are understood, and counterintuitive/credit-dominated values have been investigated.

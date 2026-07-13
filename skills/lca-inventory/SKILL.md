---
name: lca-inventory
description: "Design, construct, and audit life cycle inventories from industrial process data, engineering balances, direct emissions, utilities, foreground/background links, co-products, recycling, transport, use, and end-of-life. Use for process modeling, data collection, LCI troubleshooting, or inventory QA."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---
# Life Cycle Inventory Engineering

Build the foreground model from physical causality and operating reality before mapping it into LCA software.

## Workflow

1. Read `references/engineering-modeling.md`, `references/balances.md`, and the applicable sector reference from `lca-sector`.
2. Draw the process and life-cycle stage map. Identify reference products, intermediate products, wastes, emissions, resources, utilities, recycles, purges, and control devices.
3. Choose a calculation basis tied to the reference flow.
4. Establish parameter names, units, formulas, source class, uncertainty, and scenario dependence.
5. Close mass, energy, carbon, and material-specific balances to a justified tolerance before importing the process.
6. Calculate direct emissions using measured data first, then mass balance, stoichiometry, validated engineering models, official factors, or documented proxies in descending preference; apply `references/direct-emissions.md`.
7. Split foreground and background using `references/foreground-background.md`. Do not bury decision-sensitive technology choices in generic background datasets.
8. Map each technosphere exchange to a provider with product, geography, technology, system model, and unit checks.
9. Implement multifunctionality and recycling exactly as frozen in goal and scope.
10. Add parameter uncertainty and scenario cases using `references/uncertainty-parameters.md` without double-counting variability.
11. Run `references/inventory-audit.md` and root validation scripts where data formats permit.

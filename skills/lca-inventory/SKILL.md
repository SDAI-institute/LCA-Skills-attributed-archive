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

## Source classes

Label every value as one of:

- `MEASURED` — facility or supplier measurement;
- `CALCULATED` — equation or balance with inputs;
- `MODELED` — process simulation or engineering model;
- `DATABASE` — named dataset and version;
- `LITERATURE` — identifiable source and context;
- `PROXY` — analogous process/data;
- `EXPERT_JUDGMENT` — documented rationale;
- `SCENARIO` — deliberately varied assumption.

A value without a source class and unit is incomplete.

## Inventory traps

Investigate immediately:

- output mass materially exceeds inputs without atmospheric/resource inputs;
- carbon leaves nowhere or enters twice;
- reference product sign or amount is wrong;
- waste treatment is modeled both as an input service and a credited co-product;
- recycled content and end-of-life credit are combined inconsistently;
- steam, heat, electricity, or fuels are mixed on higher/lower heating value bases;
- wet/dry basis, concentration, density, or standard/actual volume is ambiguous;
- capture efficiency is applied without accounting for energy, solvent, compression, leakage, or fate;
- annual infrastructure is divided by production without capacity factor and lifetime consistency;
- market and production datasets are linked interchangeably without understanding the difference;
- negative technosphere exchanges create an unintended substitution credit.

## Quality gate G2

Do not proceed to LCIA until all material exchanges pass unit, sign, provider, reference-product, completeness, and balance checks. Record closure residuals and any justified open balance.

## Deliverable

Update `process-map.md`, `model-ledger.csv`, `data-register.csv`, `parameters.csv`, `assumptions.csv`, and `qa-checklist.md`. Provide a model-ready inventory table and a list of unresolved high-materiality data gaps.

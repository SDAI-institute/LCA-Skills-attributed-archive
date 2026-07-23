---
name: lca-greet
description: "Conduct and audit Argonne R&D GREET life-cycle studies for fuels, vehicles, hydrogen, electricity, batteries, aviation, marine, buildings, chemicals, bioproducts, and related pathways. Use for GREET .NET/Excel models, well-to-pump/well-to-wheels boundaries, scenario inputs, pathway comparison, or GREET result reconciliation."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---
# R&D GREET Specialist

Use the exact R&D GREET release named by the study. As of the repository baseline, 2025 Rev1 is current; always recheck the official version page before a new external study.

## Scope fit

GREET is especially strong for U.S.-centered energy, fuel, vehicle, and technology pathways. It is not automatically the right background database or LCIA method for every product LCA. Align GREET boundary and indicators with the study goal before combining outputs with other databases.

## Workflow

Read:

- `references/model-and-boundaries.md`;
- `references/pathway-workflow.md`;
- `references/version-provenance.md`;
- `references/automation.md`;
- `references/troubleshooting.md`.

1. Record GREET product, platform (.NET/Excel/module), software version, database version, release date/DOI, and any module. Use `scripts/build_run_manifest.py` to hash local artifacts without copying their contents.
2. Define pathway, functional basis, WTP/WTW/C2G boundary, geography, year, vehicle/use assumptions, and indicators.
3. Duplicate or export a baseline before editing.
4. Change only documented user inputs; record original and modified values, units, sources, and dependent assumptions.
5. Run the baseline and scenarios; export pathway-level and process-level results.
6. Reconcile energy and carbon balances, feedstock carbon, co-product allocation, land-use change, electricity mix, transport, methane leakage, and combustion treatment.
7. Compare with a hand calculation or independent intensity range.
8. When integrating with openLCA/Brightway, define exactly which GREET stages replace which background processes to prevent double counting.

## Automation caution

R&D GREET exposes a .NET plugin API, but plugin interfaces and examples may be release-specific. Do not rely on hard-coded workbook cell addresses or old DLL names without checking the installed release. Prefer named model entities, exported inputs, checksums, and a human-readable run manifest.

## High-risk assumptions

- LHV vs HHV and energy-content basis;
- WTP vs WTW vs cradle-to-grave result labels;
- grid average vs marginal or scenario electricity;
- co-product treatment and displacement;
- direct/indirect land-use change;
- feedstock carbon and biogenic combustion;
- methane leakage and GWP basis;
- vehicle lifetime, fuel economy, payload/occupancy;
- carbon capture rate vs net avoided emissions;
- overlap with imported external LCI datasets.

## Deliverable

Provide a GREET run manifest, input delta table, pathway/boundary diagram, exported results, reconciliation checks, version/DOI, and integration map. Do not distribute model files contrary to their terms.

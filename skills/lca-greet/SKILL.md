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

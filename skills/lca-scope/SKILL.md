---
name: lca-scope
description: "Define and audit LCA goal and scope: intended application, audience, functional unit, reference flow, system boundary, attributional or consequential approach, allocation, recycling, cutoff, data quality, impact coverage, comparisons, review, and reporting. Use before inventory modeling or when study comparability is uncertain."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---
# Goal and Scope Definition

The goal and scope are a modeling specification. Write decisions so another practitioner can reproduce or challenge them.

## Required sequence

1. Read `references/goal-and-scope.md` and the study protocol template.
2. Identify commissioner, practitioner, decision, intended application, audience, disclosure level, and constraints.
3. Determine whether the study supports a public comparative assertion, regulated claim, EPD/PCR, PEF, procurement, R&D, design, policy, or internal hotspot analysis.
4. Define the functional unit using `references/functional-unit.md`:
   - quantified function/service;
   - performance level and quality;
   - duration/service life;
   - operating conditions and geography;
   - reference flow required to deliver it.

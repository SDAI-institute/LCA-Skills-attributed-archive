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
5. Define system boundary and exclusions using `references/system-boundary.md`.
6. Select modeling logic using `references/modeling-approach.md`.
7. Resolve multifunctionality and recycling using `references/multifunctionality-recycling.md`.
8. Specify data quality requirements using `references/data-quality.md`.
9. Select initial impact categories and review needs; defer method implementation details to `lca-impact`.
10. Record all unresolved choices as assumptions with owners, due dates, materiality, and sensitivity treatment.

## Scope challenge questions

The protocol must answer:

- What decision could change because of the study?
- Are alternatives functionally equivalent across quality, lifetime, performance, and rebound/use behavior?
- Is the study describing average burdens or consequences of a decision?
- Which life-cycle stages can reverse the conclusion?
- What counts as “small enough” to exclude, and how will cumulative exclusions be checked?
- Which co-products, wastes, recyclates, credits, carbon stores, or avoided functions create asymmetry?
- What geographic, temporal, and technological conditions are decision-relevant?
- Which primary data are mandatory, and which proxies are acceptable?
- Which claims are prohibited until review?

## Quality gate G0

Pass only when:

- functional unit and reference flow are distinct and quantified;
- boundary includes all relevant stages or justifies exclusions;
- attributional/consequential/prospective logic is explicit;
- cutoff, allocation, substitution, recycling, and carbon rules are specified;
- data quality and impact coverage match the intended use;
- comparison and review requirements are known;
- report status is labeled.

Do not “fill in” a missing functional unit with `1 kg product` unless mass itself is the decision-relevant function. Present it as a declared unit or screening basis instead.

## Deliverable

Update `goal-and-scope.md`, `study.yaml`, `decision-log.md`, and `assumptions.csv`. End with a concise scope freeze summary and items that remain provisional.

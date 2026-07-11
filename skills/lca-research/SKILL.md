---
name: lca-research
description: "Research LCA standards, methods, datasets, process inventories, emission factors, tool APIs, sector conventions, and benchmarks using an evidence hierarchy and reproducible source register. Use when data or methodological support is missing, current status matters, or a claim needs verification."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---
# LCA Research

Research for LCA must be traceable from question to model parameter or decision.

## Protocol

1. Convert the request into answerable evidence questions:
   - methodology/requirement;
   - process parameter or inventory;
   - emission/resource factor;
   - database/tool behavior;
   - benchmark or validation range.
2. Read `references/evidence-hierarchy.md` and prioritize current primary sources.
3. Search with exact technology, geography, year, operating basis, unit, system boundary, and source type.
4. Use `references/source-evaluation.md` to assess relevance, authority, transparency, representativeness, uncertainty, and license.
5. Extract data into the study register using `references/data-extraction.md`.
6. Triangulate material parameters with at least two independent sources where feasible.
7. Record disagreements; do not average incompatible values without a model.
8. Translate evidence into baseline, low/high or distribution, and sensitivity treatment.
9. Update `docs/source-register.md` only for reusable plugin-wide sources; keep study-specific sources in the study data register.

## Current-source rule

For standards status, regulatory/PCR rules, database releases, software APIs, characterization methods, and official models, verify the current source at the time of use. Include access date and version.

## Evidence labels

- `AUTHORITATIVE_REQUIREMENT`
- `PRIMARY_TECHNICAL_DATA`
- `PEER_REVIEWED_MODEL`
- `OFFICIAL_DATABASE`
- `INDUSTRY_PRIMARY_DATA`
- `SECONDARY_REVIEW`
- `PROXY`
- `EXPERT_JUDGMENT`

## Deliverable

Produce a research memo with question, search scope, accepted/rejected sources, extracted values and units, conversion/calculation steps, uncertainty, license constraints, and model implications. Never cite a source for a claim it does not support.

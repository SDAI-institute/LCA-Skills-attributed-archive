---
name: lca-epd-pcf
description: "Handle product carbon footprint, Environmental Product Declaration, Product Environmental Footprint, PCR/PEFCR, and construction-product LCA contexts. Use for ISO 14067, GHG Protocol Product Standard, ISO 14025/21930, EN 15804, PEF/OEF, declared units, modules, verification, or external product claims."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---
# Product Footprint, EPD, and PEF Contexts

Program rules can narrow methodological choices, but they do not eliminate the need to understand them.

## First classify the deliverable

Read `references/context-selection.md` and identify:

- internal product carbon footprint;
- ISO 14067-style CFP/partial CFP;
- GHG Protocol Product Standard inventory/report;
- Type III environmental declaration/EPD;
- construction EPD under applicable PCR/EN 15804/ISO 21930 context;
- EU PEF study under a valid PEFCR or general method;
- supplier-specific product result used inside another LCA.

Do not mix these labels. A carbon footprint is one impact category; an EPD/PEF generally has broader prescribed content.

## Workflow

1. Obtain the current program instructions, PCR/PEFCR, verification rules, validity dates, and applicable standards legally.
2. Freeze product category, declared/functional unit, reference service life, modules/stages, cutoffs, allocation, electricity, recycled content/end-of-life, biogenic carbon, data-quality, and averaging rules.
3. Build a rule-compliance matrix using `references/rule-matrix.md`.
4. Model and calculate with the exact method/data versions required by the program.
5. Separate gross inventory, biogenic carbon, removals/storage, offsets, and credits according to the program rules.
6. Apply verification/critical review requirements using qualified independent parties.
7. Control claims and comparability using `references/claims-comparability.md`.

## PEF data caution

When EF-compliant datasets are unavailable, follow current European Commission transition guidance and any valid PEFCR rather than improvising a data hierarchy. Record alternative dataset eligibility and adjustments.

## EPD comparability caution

EPDs are not automatically comparable. Program, PCR, declared/functional unit, system boundary, data/method versions, geography, reference service life, scenarios, and verification must align.

## Deliverable

Produce a rule matrix, product definition, module/boundary map, calculation manifest, data-quality evidence, report/EPD input package, verification package, and claim limitations. Do not call an unverified draft an EPD.

---
name: lca-data
description: "Select, evaluate, map, license, version, and interoperate LCA databases and datasets. Use for ecoinvent, Federal LCA Commons/USLCI, EF datasets, GREET data, EXIOBASE/USEEIO, supplier EPDs, ecoSpold, ILCD, JSON-LD, or when foreground and background data do not align."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---
# LCA Data and Interoperability

A convenient dataset is not automatically a fit-for-purpose dataset.

## Dataset selection protocol

1. Define the required product/service, geography, reference year, technology, system model, unit, and process type.
2. Search the evidence hierarchy in `references/database-catalog.md`, then run the dated provider-errata gate in `references/current-errata.md`.
3. Evaluate candidate datasets with `references/dataset-fit.md`:
   - technological, temporal, and geographical representativeness;
   - completeness and elementary-flow coverage;
   - allocation/system-model compatibility;
   - transformation vs market role;
   - reference product, unit, and sign;
   - uncertainty and documentation;
   - license and redistribution rights.
4. Record the exact dataset identifier, database release, system model, access date, modifications, and provider link.
5. Map nomenclature and flows using `references/interoperability.md`.
6. Quantify unmapped elementary flows and unresolved providers; do not silently drop them.
7. Test a small known calculation after import/export before migrating the full study.
8. Recheck provider corrections at release; a database selected months earlier can acquire a known-issue notice before publication.

## System-model rule

Do not mix cut-off, APOS, consequential, EN 15804, or other system-model inventories inside one product system without a deliberate reconciliation. The same named activity can encode different burden and recycling logic across system models.

## Licensed data rule

Read `references/licensing.md`. Never copy or commit restricted inventory rows, unit-process files, credentials, or derived outputs that violate a license. For software products exposing licensed data to third parties, require a license review and, where applicable, developer/sublicensing rights.

## Hybrid and EEIO data

Use USEEIO/EXIOBASE-style data for screening, organizational/spend-based gaps, truncation analysis, or hybrid LCA when sector aggregation and price-year effects are acceptable. Do not present sector-average spend factors as process-specific engineering data.

## Deliverable

Produce a dataset selection table with accepted/rejected candidates, reasons, versions, licenses, fit scores, modifications, and sensitivity requirements. Update `model-ledger.csv` and `data-register.csv`.

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

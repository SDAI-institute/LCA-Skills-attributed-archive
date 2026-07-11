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

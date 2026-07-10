---
name: lca-setup
description: "Initialize or repair a durable LCA study workspace with protocol, data, parameter, assumption, model, QA, results, and reporting artifacts. Use before substantial LCA work or when an existing study lacks traceable structure."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---
# LCA Study Setup

Create a workspace that makes the model auditable and resumable. Read `references/workspace-contract.md` for the artifact contract, status machine, and confidentiality boundaries.

## Procedure

1. Choose a lowercase hyphenated study slug. Do not use client-sensitive names in a public repository.
2. Run from the repository root:

```bash
python scripts/new_study.py <slug> --title "<study title>"
```

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

3. Confirm that `lca/studies/<slug>/` contains:
   - `study.yaml` — machine-readable study identity and status;
   - `goal-and-scope.md` — study protocol;
   - `process-map.md` — foreground/background and life-cycle stages;
   - `model-ledger.csv` — processes, products, providers, versions, and status;
   - `data-register.csv` — values, sources, quality, and uncertainty;
   - `parameters.csv` — names, values, units, formulas, distributions, scenarios;
   - `assumptions.csv` — provisional choices and validation plan;
   - `decision-log.md` — material methodological decisions;
   - `qa-checklist.md` — quality-gate evidence;
   - `results/` — raw, processed, figures, and release outputs;
   - `report/` — report drafts and review responses.
4. Run:

```bash
python scripts/validate_study.py lca/studies/<slug>
```

5. Record software, database, LCIA method, and source versions before modeling.

## Existing study repair

Do not overwrite populated files. Create missing artifacts, map existing files into the contract, and log migrations in `decision-log.md`.

## Confidentiality

Store confidential raw data outside version control or under a separately controlled location. Commit only redacted or aggregated values that the user is authorized to share.

## Handoff

Invoke `lca-scope` with the workspace path. Setup is complete only when the study has an owner, intended use, audience, status label, and next gate.

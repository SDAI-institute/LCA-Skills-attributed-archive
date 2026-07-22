---
name: lca-brightway
description: "Build reproducible programmatic LCAs in the modern Brightway ecosystem using bw2data, bw2io, bw2calc, bw_processing, uncertainty, MultiLCA, Activity Browser, premise, temporalis/timex, and related packages. Use for Python LCA, scenario generation, custom inventories, matrix diagnostics, or research automation."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---
# Brightway Specialist

Brightway is an ecosystem, not one frozen API. Pin package versions and distinguish legacy Brightway2 examples from current Brightway 2.5-era semantics.

## Environment protocol

Read `references/environment.md`.

1. Create an isolated environment.
2. Run `scripts/snapshot_environment.py`; record Python and package versions.
3. Set a named Brightway project; never rely on an implicit current project.
4. Import databases through documented `bw2io` interfaces and preserve import logs.
5. Snapshot/export the project or record deterministic rebuild steps.

## Calculation pattern

Read `references/data-and-calculation.md`. A common static workflow is:

```python
import bw2data as bd
import bw2calc as bc


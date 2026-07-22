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

bd.projects.set_current("<project>")
activity = bd.get_node(database="<db>", code="<code>")
method = ("<family>", "<category>", "<indicator>")

lca = bc.LCA({activity: 1.0}, method=method)
lca.lci()
lca.lcia()
print(lca.score)
```

Use exact methods and object identifiers from the project. For current datapackage, scenario, stochastic, or `MultiLCA` APIs, follow installed documentation rather than copying legacy snippets.

## Reproducible workflow

1. Validate database names, system model, activity IDs/codes, reference products, locations, and units.
2. Build foreground data with stable codes and explicit production/technosphere/biosphere exchanges.
3. Run import strategies and inspect unlinked exchanges before writing.
4. Calculate baseline LCI and LCIA.
5. Inspect matrices and contributions using `references/diagnostics.md`.
6. Run scenarios and uncertainty using `references/scenarios-uncertainty.md`.
7. Use `premise`, `wurst`, `bw_temporalis`, `bw_timex`, or regional packages only with documented scenario/version assumptions.
8. Serialize parameters, identifiers, environment lock, and output tables.

## Common failure modes

- wrong active project;
- legacy tutorial/API mismatch;
- activity name search returning an unintended geography/product;
- missing production exchange or wrong sign;
- unlinked biosphere/technosphere exchanges after import;
- mixed database releases/system models;
- using object order or unstable integer IDs across independently rebuilt projects;
- repeated stochastic calculations without controlled seeds or correlation logic;
- matrix edits not reflected because data were not reprocessed;
- interpreting a negative technosphere coefficient without tracing substitution semantics.

## Deliverable

Provide a runnable script/notebook, environment manifest, database rebuild instructions, activity/method identifiers, parameter/scenario files, results, and QA checks. Keep notebooks thin; put reusable logic in tested Python modules.

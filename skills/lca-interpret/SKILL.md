---
name: lca-interpret
description: "Interpret LCA results with contribution analysis, hotspot tracing, scenario comparison, sensitivity, uncertainty, completeness, consistency, dominance, benchmark triangulation, and decision-relevant conclusions. Use after calculation or when results appear unstable, counterintuitive, negative, or too precise."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---
# LCA Interpretation

Interpretation is iterative with goal/scope and inventory. A surprising result is a reason to inspect the model, not a story prompt.

## Required analysis

1. Verify the calculation passed gates G0–G3.
2. Read `references/contribution-analysis.md` and trace hotspots from impact category to process, exchange, parameter, and data source.
3. Separate foreground controllable drivers from background structural drivers.
4. Run the scenario and sensitivity plan in `references/sensitivity-scenarios.md`.

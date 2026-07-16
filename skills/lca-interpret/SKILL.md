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
5. Quantify uncertainty using `references/uncertainty.md`; distinguish:
   - parameter uncertainty;
   - natural variability;
   - data uncertainty;
   - model-structure uncertainty;
   - scenario uncertainty;
   - LCIA characterization uncertainty.
6. Perform completeness, sensitivity, and consistency checks in `references/interpretation-checks.md`.
7. Triangulate key results against an independent dataset, hand calculation, published range, material/energy intensity, or prior validated model.
8. Revisit scope or inventory when conclusions depend on a weak proxy, exclusion, allocation, recycling credit, grid scenario, lifetime, yield, or use-phase assumption.

## Comparative decision rules

- Compare like functions, performance, geography, time, and service life.
- Do not call a small numerical difference meaningful when uncertainty ranges overlap or method choice can reverse ranking.
- Show absolute results and percentage differences; do not use percentages near zero without context.
- Report trade-offs across categories instead of hiding them in a single score.
- State whether rankings are robust, conditional, indeterminate, or outside scope.

## Negative or credit-dominated results

Perform a dedicated audit of displaced product, substitution ratio, market feasibility, additionality, temporal match, double counting, waste baseline, carbon storage permanence, and system-boundary symmetry. Show gross burdens separately from credits.

## Quality gate G4

Conclusions must be supported by significant issues, evaluated for completeness/sensitivity/consistency, bounded by uncertainty, and aligned with the intended application.

## Deliverable

Create an interpretation memo containing result tables, contribution trees, scenario matrix, sensitivity ranking, uncertainty summary, limitations, and decision statements with confidence labels.

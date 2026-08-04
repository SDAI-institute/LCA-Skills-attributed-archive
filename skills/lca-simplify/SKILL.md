---
name: lca-simplify
description: "Reduce unnecessary LCA model, workflow, or reporting complexity while preserving decision fitness, transparency, and tested results. Use to remove redundant processes/parameters/scenarios, clarify boundaries, or make a model maintainable without hiding material effects."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---

# LCA Model Simplification

Simplify only after identifying the decision, material contributors, uncertainty, and required reproducibility.

Read `references/model-reduction.md` and `references/complexity-budget.md`.

## Procedure

1. Define what must remain invariant: functional performance, boundary logic, key scenarios, indicator totals within tolerance, hotspot ranking, claim route, and review evidence.
2. Inventory complexity: processes, exchanges, parameters, formulas, scenarios, mappings, custom factors, scripts, and report transformations.
3. Classify each element as decision-critical, uncertainty-critical, required by rules, reusable support, or redundant.
4. Prefer consolidation, parameterization, generated data, shared providers, and documented defaults over deletion.
5. Remove one coherent complexity class at a time.
6. Recalculate and compare totals, contributions, hotspot ranks, sensitivities, balances, and uncertainty.
7. Reject a simplification that shifts a material result, masks trade-offs, breaks provenance, or prevents review.
8. Record the simplification decision, before/after metrics, tolerance, and regression test.

Screening cutoffs are not a substitute for completeness. A simplified model must remain fit for its stated use and may require a stricter model for external disclosure.

---
name: lca-debug
description: "Diagnose and resolve LCA model, data, calculation, API, reproducibility, or result anomalies using a scientific failure taxonomy and minimal reproductions. Use for zero/negative/extreme results, failed balances, broken links, mapping gaps, or tool errors."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---

# LCA Debugging

Debug from evidence. Do not patch the reported symptom until the failure class and reproducible cause are known.

Read `references/failure-taxonomy.md`, `references/debug-playbook.md`, and `references/minimal-reproduction.md`.

## Procedure

1. Preserve the failing model/run, exact error, inputs, versions, IDs, logs, and expected behavior.
2. Classify the failure as transport/environment, schema/API, identity/linkage, unit/sign, formula/parameter, engineering balance, boundary/allocation/recycling, LCIA mapping/factor, scenario/uncertainty, numerical, report synchronization, or user expectation.
3. Reproduce the failure with the smallest model and one scenario/indicator where possible.
4. Test hypotheses from cheapest and most discriminating to most invasive.
5. Compare against a known GUI/manual/reference result or analytically solvable fixture.
6. Apply the narrowest correction, preserving before/after artifacts and decision rationale.
7. Re-run affected validators, calculations, contributions, scenarios, and claims checks.
8. Record root cause, correction, evidence, regression test, and prevention lesson.

## Investigation triggers

- exact zero or missing category;
- negative result or result dominated by one credit;
- order-of-magnitude discontinuity after a small input change;
- contribution totals not matching the total;
- mass, carbon, energy, or elemental residual above tolerance;
- duplicate or unlinked providers;
- result changes when display names change;
- Monte Carlo failures or implausibly narrow uncertainty;
- software/GUI/API disagreement.

## Stop conditions

Stop rather than guess when the original model cannot be preserved, licensed evidence is unavailable, identity is ambiguous, a formal method/program rule is missing, or a correction would require an undisclosed methodological change.

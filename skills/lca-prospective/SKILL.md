---
name: lca-prospective
description: "Design consequential, prospective, ex-ante, dynamic, temporal, spatial, and scenario-based LCAs. Use for emerging technologies, policy decisions, marginal suppliers, future grids, IAM/premise scenarios, learning curves, scale-up, delayed emissions, or time-dependent impacts."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---
# Prospective and Consequential LCA

Future-oriented LCA must make scenario logic explicit; it cannot hide forecasts inside point estimates.

## Classify the question

Use `references/approach-selection.md` to distinguish:

- attributional future scenario;
- consequential decision analysis;
- ex-ante emerging-technology comparison;
- prospective background transformation;
- dynamic inventory/LCIA;
- spatially differentiated LCA;
- hybrid scenario analysis.

## Workflow

1. Define decision, implementation scale, time horizon, adoption path, affected markets, and counterfactual.
2. Separate foreground technology development from background scenario changes.
3. Model scale-up using `references/technology-scaleup.md`: yield, capacity, learning, material intensity, lifetime, utilization, degradation, and supply constraints.
4. Model marginal response and substitution using `references/consequential.md` only when causal claims are intended.
5. Build a scenario matrix using `references/scenario-design.md`; include internally coherent narratives rather than independent arbitrary parameter extremes.
6. For future backgrounds, record IAM/scenario/model/version, mapping, regionalization, and transformation package.
7. For temporal models, preserve emission timing, uptake/release, service life, replacement, and characterization timing.
8. Report scenario-conditional conclusions, model disagreement, and decision thresholds.

## Guardrails

- Consequential LCA is not “attributional plus a credit.”
- A marginal supplier must be justified by market response, constraints, geography, and time horizon.
- Avoided production cannot exceed feasible substitution or be claimed by multiple actors.
- Future improvements need evidence or explicit learning scenarios; do not give emerging technology every optimistic assumption while holding the incumbent static.
- Prospective databases can be internally consistent yet still scenario-dependent and uncertain.
- Delayed emissions and carbon storage require time horizon and permanence assumptions.

## Deliverable

Create a scenario protocol, counterfactual definition, parameter trajectories, background transformation manifest, causal/marginal supplier rationale, and robustness map showing which conclusions hold across scenarios.

# Scenario design

Scenarios are internally coherent representations of possible conditions, not arbitrary combinations of minimum and maximum values.

## Build the matrix

Define axes such as:

- decision/adoption: no action, limited, central, high;
- technology: current, expected, advanced, constrained;
- background: grid, fuel, material production, transport, waste management;
- policy/market: regulation, carbon price, recycling rate, supply constraint;
- geography and trade;
- time: commissioning year, operating years, end of life;
- behavior/utilization.

Create named narratives. State causal dependencies among parameters so impossible combinations are excluded.

## Parameter trajectories

For each time-dependent parameter record baseline year, target years, interpolation rule, floor/ceiling, evidence, scenario linkage, and uncertainty. Do not interpolate categorical technology changes as if they were smooth physical variables.

## Background transformation manifest

Record scenario family, IAM or source model, version, pathway, year, regions, database/version, mapping package, transformations, exclusions, unresolved mappings, and hashes where possible.

## Robustness outputs

At minimum report:

- scenario-by-impact matrix;
- ranking reversals;
- break-even thresholds;
- sign stability;
- conclusions valid in all scenarios;
- conclusions that require a named scenario;
- unmodeled structural uncertainty.

Do not assign scenario probabilities unless a defensible elicitation or probabilistic model exists.

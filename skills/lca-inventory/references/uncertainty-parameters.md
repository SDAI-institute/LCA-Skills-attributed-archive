# Inventory parameters and uncertainty

## Parameter record

Include:

- stable name and description;
- baseline value and unit;
- source and date;
- formula/dependencies;
- scope/process;
- distribution or low/high;
- correlation group;
- scenario overrides;
- sensitivity priority;
- validation status.

## Distributions

Use a distribution only when its support and meaning are defensible. Common choices:

- normal for symmetric measurement error without impossible tails;
- lognormal for positive multiplicative uncertainty;
- triangular/uniform for bounded expert/scenario ranges;
- discrete for technology or method alternatives;
- empirical/bootstrap for adequate observations.

Avoid independent sampling of parameters constrained by a balance or sharing a denominator. Use correlation groups, joint scenarios, or calculate dependent values from sampled independent parameters.

## Variability vs uncertainty

Variability describes real differences across facilities/time/populations; uncertainty describes incomplete knowledge. Report and model them separately when decisions depend on both.

## Screening priority

Use contribution and sensitivity to focus data improvement on parameters that are both uncertain and influential. Do not spend equal effort on immaterial flows.

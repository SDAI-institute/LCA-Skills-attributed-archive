# Uncertainty analysis

## Quantitative uncertainty

When probability distributions are defensible:

- preserve units and physical constraints;
- model dependencies/correlations;
- set and record random seed or sampling design;
- use sufficient iterations and convergence checks;
- report median/mean, intervals, and probability of decision-relevant outcomes;
- inspect implausible samples and solver failures.

## Comparative uncertainty

For paired alternatives sharing background data, use correlated/paired sampling where supported. Independent sampling can overstate uncertainty in differences and hide common-mode uncertainty.

## Non-probabilistic uncertainty

Use scenario envelopes, alternate methods/system models, qualitative confidence, pedigree/data-quality assessments, and structured expert elicitation when probabilities are not meaningful.

## Interpretation

A narrow Monte Carlo interval does not capture omitted processes, wrong functional unit, allocation choices, future scenario uncertainty, or LCIA model uncertainty. Report what is and is not included.

## Decision statements

Examples of calibrated language:

- robust across all tested scenarios;
- likely lower under the stated distributions;
- ranking changes under plausible electricity/allocation cases;
- difference is smaller than modeled uncertainty;
- evidence is insufficient for comparative conclusion.

# Quality gates

A gate is evidence that a study can safely proceed. “The software ran” is not a gate.

## G0 — Framing

Required evidence:

- intended decision/application and audience;
- disclosure/comparison/program context;
- functional unit and reference flow;
- boundary and life-cycle stages;
- geography, time, technology, lifetime/performance;
- attributional/consequential/prospective logic;
- cutoff, multifunctionality, recycling, carbon rules;
- data quality and impact-category requirements;
- review plan and status label.

Fail when a material interpretation can change merely by guessing any of the above.

## G1 — Data and modeling plan

Required evidence:

- process map and foreground/background split;
- parameter dictionary with units/formulas;
- data register with source class and representativeness;
- dataset/system-model/provider plan;
- gap/proxy/uncertainty/sensitivity plan;
- direct-emission and conservation equations;
- version and license manifest.

## G2 — Inventory integrity

Required evidence:

- quantitative reference is correct;
- unit and dimensional checks pass;
- technosphere/biosphere signs are correct;
- provider links and reference products are reviewed;
- mass/energy/carbon or elemental balances close to justified tolerances;
- direct emissions, controls, wastes, and utilities are complete;
- allocation/recycling/substitution implementation matches protocol;
- duplicate burden/credit checks pass;
- excluded flows are quantified or bounded.

## G3 — LCIA integrity

Required evidence:

- method family, implementation, version, categories, units, horizon/perspective;
- elementary-flow mapping coverage and exclusions;
- climate/biogenic/storage, water, land, and toxicity conventions;
- regionalization and normalization/weighting status;
- at least one benchmark or hand characterization check.

## G4 — Interpretation integrity

Required evidence:

- contribution/hotspot trace;
- scenario and sensitivity results;
- uncertainty and model-choice limitations;
- completeness, consistency, sensitivity checks;
- independent benchmark/triangulation;
- conclusion stability classification.

## G5 — Release readiness

Required evidence:

- report/model consistency;
- reproducibility package;
- claims bounded to goal/scope;
- review findings closed or disclosed;
- required external review/verification completed;
- no confidential/licensed material exposed.

## Gate record

For each gate store: `status`, `date`, `reviewer`, `evidence paths`, `open findings`, and `next action` in `qa-checklist.md` or a machine-readable manifest.

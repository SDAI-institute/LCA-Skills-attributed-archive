---
name: lca-impact
description: "Select, configure, and audit life cycle impact assessment methods and indicators. Use for ReCiPe, TRACI, EF, IPCC climate factors, USEtox, AWARE, CML, IMPACT World+, EN 15804 indicators, normalization, weighting, elementary-flow mapping, or LCIA method compatibility."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---
# Life Cycle Impact Assessment

LCIA converts an inventory into potential impact indicators; it does not measure actual site-specific damage or risk unless a method explicitly supports that interpretation.

## Method selection

Read `references/method-selection.md` and `references/method-catalog.md`.

Select based on:

- goal, audience, geography, and program/PCR requirements;
- midpoint vs endpoint decision needs;
- impact categories material to the product system;
- characterization model currency and implementation version;
- elementary-flow and compartment compatibility;
- regionalization and time-horizon needs;
- consistency with prior studies when comparability is legitimate.

Do not default to climate change alone unless the goal is explicitly a carbon footprint. Screen for burden shifting.

## Setup protocol

1. Record method family, software implementation, version/date, categories, units, perspectives/time horizons, and source.
2. Freeze the inventory and elementary-flow mapping version.
3. Quantify mapped and unmapped inventory mass or contribution where possible.
4. Review special topics using:
   - `references/climate-and-carbon.md`;
   - `references/water-land-toxicity.md`;
   - `references/normalization-weighting.md`.
5. Calculate a known benchmark or hand-check at least one characterization factor.
6. For comparisons, use the same method implementation and category set unless a documented conversion is defensible.

## Method cautions

- Do not mix IPCC assessment-report GWPs without disclosure.
- Biogenic carbon neutrality is not an automatic zero; track uptake, release, storage, land-use change, timing, and method rules.
- Toxicity results often have high model and substance uncertainty; avoid risk-assessment language.
- Water inventory volume is not water-scarcity impact; location and consumption matter.
- Normalization and weighting introduce reference choices and value judgments. Report characterized results alongside any aggregate score.
- Negative characterization results and missing factors require source-level investigation.

## Quality gate G3

Pass only when method/version, mapping coverage, units, exclusions, special carbon/water/toxicity choices, regionalization, and normalization/weighting status are documented.

## Deliverable

Write an LCIA method memo, update the study protocol and model ledger, and provide a machine-readable method manifest where supported by the chosen tool.

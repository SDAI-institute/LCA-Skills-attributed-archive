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

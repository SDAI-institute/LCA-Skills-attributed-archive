---
name: lca-report
description: "Produce transparent LCA reports, executive summaries, technical appendices, result tables, model manifests, and claim-safe communications for screening, internal, public, PCF, EPD, PEF, or review contexts. Use when turning a model into a decision or disclosure deliverable."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---
# LCA Reporting

A report is an auditable representation of the study, not a marketing summary detached from the model.

## Choose the output contract

Read `references/report-types.md` and select:

- screening memo;
- internal decision report;
- full technical LCA report;
- product carbon footprint report;
- EPD-supporting LCA report;
- PEF/OEF report;
- peer-reviewed publication methods/results package;
- executive summary plus technical appendix;
- machine-readable reproducibility package.

## Required content

Use `references/report-content.md`. At minimum include:

- commissioner, practitioner, date, version, status, and review status;
- goal, intended use, audience, limitations, and disclosure context;
- functional unit, reference flow, boundary, cutoffs, allocation, recycling, and modeling approach;
- data sources, quality, versions, geography, time, technology, and gaps;
- software, database/system model, LCIA method, parameters, and scenarios;
- results by category with units and sufficient disaggregation;
- contribution, sensitivity, uncertainty, completeness, and consistency findings;
- limitations, excluded uses, and conditional conclusions;
- review findings/responses where applicable;
- reproducibility manifest and change history.

## Claim safety

Read `references/claims-and-visuals.md`.

- Do not use “environmentally friendly,” “zero impact,” or “carbon neutral” based solely on LCA results.
- Do not present a public comparative superiority claim without the required review and equivalent function.
- Label credits, removals, offsets, avoided emissions, and stored carbon separately.
- Keep units and baselines visible in charts.
- Do not truncate axes or aggregate categories in ways that conceal trade-offs.
- State when a number is a screening estimate, scenario, or proxy.

## Consistency check

Before release, regenerate tables from the frozen output where possible. Cross-check every headline number, percentage, sign, unit, scenario, and figure caption against the calculation artifact.

## Deliverable

Write the report under `report/`, build the reproducibility package with `references/release-manifest.md`, and route to `lca-review`. A polished document with open material findings remains `NOT READY`.

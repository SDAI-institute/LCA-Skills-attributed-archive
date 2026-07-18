---
name: lca-review
description: "Audit an LCA model and report with dynamically selected specialist perspectives, prepare critical-review evidence, and determine readiness for internal decisions, disclosure, EPD/PCF verification, or public comparison. Use for independent QA, red-team review, or release gating."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---

# LCA Review and Quality Assurance

Review the frozen study against its stated goal, applicable rules, and reproducibility—not reviewer preference.

## Independence statement

First state whether this is practitioner self-check, internal independent review, external expert review support, critical-review preparation, or formal review by a named qualified reviewer/panel. An AI review is never itself formal independent critical review or verification.

Read `references/review-orchestration.md`, `references/finding-schema.md`, `references/review-plan.md`, `references/scope-audit.md`, `references/model-audit.md`, `references/results-audit.md`, `references/report-audit.md`, and `references/comparative-assertions.md`.

## Dynamic specialist review

Select the smallest set that covers the material risks, using:

- `references/persona-methodologist.md`
- `references/persona-process-engineer.md`
- `references/persona-data-auditor.md`
- `references/persona-lcia-specialist.md`
- `references/persona-uncertainty-specialist.md`
- `references/persona-critical-reviewer.md`
- `references/persona-claims-reviewer.md`
- `references/persona-tool-integration.md`
- `references/persona-sector-specialist.md`

When the host supports subagents, dispatch bounded read-only reviewers in parallel and require structured JSON. Otherwise perform isolated sequential passes. Merge and deduplicate by root cause and evidence. Do not let one reviewer edit the model it is evaluating.

## Mandatory checks

- functional unit/reference flow and alternative equivalence;
- complete and symmetric boundaries;
- provider links, system model, units, signs, reference products, formulas, parameters;
- mass/energy/carbon or elemental closure and process realism;
- allocation, substitution, recycling, direct emissions, and duplicate credits;
- data provenance, fit, licenses, transformations, uncertainty;
- LCIA method/version, factors, units, mapping, regionalization, exclusions;
- scenario, uncertainty, sensitivity, and result/contribution reconciliation;
- report-model agreement, claims, limitations, review status, reproducibility.

## Finding and release rules

Classify findings `CRITICAL`, `MAJOR`, `MINOR`, `OBSERVATION`, or `QUESTION`. Track evidence, owner, response, verification, and closure.

Issue one recommendation:

- `NOT READY`
- `CONDITIONALLY READY`
- `INTERNALLY REVIEW-READY`
- `EXTERNAL REVIEW REQUIRED`
- `REVIEW CLOSED` with reviewer, scope, date, and limitations

Create the review report, findings register, response log, and release recommendation. Preserve the finding trail when corrections are made.

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


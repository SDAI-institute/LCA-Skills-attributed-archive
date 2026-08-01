---
name: lca-intake
description: "Turn an ambiguous LCA request into a decision-ready study brief, classify risk and study type, identify blocking questions, and set an evidence and review threshold. Use before scope definition for new, high-stakes, comparative, externally disclosed, or underspecified studies."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---

# LCA Intake

Create a concise but decision-complete study brief before designing the model.

Read `references/intake-question-tree.md`, `references/study-classification.md`, and `references/minimum-brief.md`.

## Procedure

1. Identify the decision that the assessment must support and who will use it.
2. Classify the work: explanation, screening, internal LCA, disclosed PCF, EPD/PEF/program study, public comparison, consequential/prospective study, organizational LCA, or social LCA.
3. Identify the product/service, alternatives, performance requirements, geography, period, technology state, and life-cycle stages likely to matter.
4. Separate known inputs from missing information, assumptions, and user preferences.
5. Ask only questions that can materially change scope, model structure, evidence threshold, or claim route. Ask one blocking question at a time when interaction is available.
6. When an answer is unavailable, record a provisional assumption, confidence, influence, validation action, and sensitivity case rather than hiding the gap.
7. Assign a risk tier and required review route.
8. Produce or update `intake-brief.md`, `study.yaml`, `assumptions.csv`, and `data-request.csv`.

## Risk tiers

- `R0 EDUCATIONAL`: no decision or external claim.
- `R1 SCREENING`: directional internal result with explicit proxies.
- `R2 DECISION`: material internal investment/design/procurement use.
- `R3 DISCLOSURE`: externally communicated footprint, EPD, PEF, regulatory, financing, or customer claim.
- `R4 PUBLIC COMPARISON`: comparative assertion intended for the public; requires heightened equivalence and independent review.

## Completion gate

Do not declare intake complete until the intended use, audience, deliverable, preliminary functional performance, boundary hypothesis, modeling approach candidate, data access, claim context, review route, and top uncertainties are explicit.

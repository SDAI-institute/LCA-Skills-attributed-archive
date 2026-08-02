---
name: lca-work
description: "Execute an approved LCA study plan in controlled, auditable increments and return a structured work receipt with changes, evidence, tests, unresolved risks, and next gate. Use to build or correct models without losing decision and review traceability."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---

# LCA Work Execution

Implement only the approved task set. Preserve traceability and return control to the caller at each material gate.

Read `references/work-receipt.md`, `references/change-control.md`, and `references/return-to-caller.md`.

## Execution loop

1. Confirm the study path, approved plan revision, task IDs, allowed tools, confidentiality boundary, and write permissions.
2. Snapshot relevant model, environment, database/method versions, and input hashes before change.
3. Execute the smallest coherent task batch. Do not combine unrelated methodological changes.
4. Update the model/data/parameter/assumption/decision ledgers as changes occur.
5. Run task-level acceptance checks and the applicable deterministic validators.
6. If a result violates conservation, dimensional, linkage, mapping, or claim safeguards, stop and route to `lca-debug`.
7. If a new methodological choice is required, stop and return it as an explicit decision rather than choosing silently.
8. Produce `work-receipt.json` and update `handoff.md`.

## Change-control rules

- Never overwrite raw evidence; create a transformed artifact with provenance.
- Never mutate licensed databases merely to make a result pass.
- Preserve pre-change and post-change IDs, parameters, hashes, and results.
- Recalculate every affected scenario after model-affecting changes.
- A reviewer reports findings; the practitioner applies fixes and records responses.

## Work receipt

Return status (`completed`, `partial`, `blocked`, or `failed`), task IDs, files/model objects changed, commands/tools used, checks and evidence, before/after metrics, decisions made, assumptions introduced, unresolved findings, and exact next action.

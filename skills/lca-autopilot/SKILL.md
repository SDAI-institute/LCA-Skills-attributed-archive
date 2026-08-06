---
name: lca-autopilot
description: "Run the full LCA delivery pipeline end to end after explicit user authorization: intake, scope, plan, inventory, calculation, interpretation, specialist review, correction, validation, reporting, handoff, and knowledge capture. Use only for an explicitly requested autonomous run."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---

# LCA Autopilot

**Execute the stages in order. Planning and scope gates are mandatory.** This skill may create and modify study artifacts, run local tools, and iterate corrections, but it may not publish, certify, submit, purchase licensed data, accept legal terms, or represent an AI review as independent verification.

Read `references/pipeline.md`, `references/stop-conditions.md`, `references/child-skill-contract.md`, and `references/autonomy-policy.md`.

## Invocation rule

Proceed only when the user explicitly asks for an autonomous end-to-end run. Otherwise route to `lca-expert`, `lca-plan`, or `lca-work`.

When invoking another skill, resolve its exact available name. A host may expose a bare name, a plugin namespace, or no nested-skill mechanism. If nested invocation is unavailable, follow the referenced skill's documented contract directly and record that fallback.

## Pipeline

1. **Authorize and bound autonomy.** Record workspace, deliverable, confidentiality, allowed writes/tools, external-action prohibition, and completion definition.
2. **Intake.** Run `lca-intake`; create the risk-classified brief.
3. **Initialize.** Run `lca-setup` and `lca-doctor`; preserve environment evidence.
4. **Scope.** Run `lca-scope`; stop if function, boundary, modeling approach, or claim route is materially unresolved.
5. **Plan.** Run `lca-plan`; verify ordered tasks and gates before implementation.
6. **Work.** Run `lca-work` with `lca-inventory`, `lca-data`, `lca-sector`, and research support.
7. **Pre-calculation validation.** Run `lca-validate`; resolve all critical inventory failures.
8. **Calculate.** Run `lca-calculate` and the selected tool skill; preserve manifests and raw outputs.
9. **Interpret.** Run `lca-interpret`; add scenarios, sensitivity, uncertainty, and triangulation required by the risk tier.
10. **Review.** Run `lca-review` using multiple independent specialist perspectives. Merge and deduplicate findings.
11. **Correct.** Route valid findings to `lca-work` or `lca-debug`; recalculate and revalidate affected outputs.
12. **Report and claims.** Run `lca-report` and specialized program skills; run claim checks.
13. **Release candidate.** Generate hashes, status, open exceptions, and review requirements. Do not externally publish.
14. **Handoff and compound.** Run `lca-handoff`; capture only validated, generalized, non-confidential lessons with `lca-compound`.

## Stop and return a blocker when

- the user did not authorize the required write or tool action;
- functional equivalence, boundary, or modeling approach cannot be responsibly assumed;
- confidential or licensed data access is missing;
- a required program/PCR/standard rule is unavailable;
- the model fails a material conservation, identity, or mapping check;
- a public comparison or verified declaration requires an independent human process;
- results remain unstable across plausible cases;
- a tool action would affect an external system or create an external claim.

## Final receipt

Return deliverables, study status, quality-gate table, models/data/methods and versions, calculation IDs, results and uncertainty, resolved and open findings, review status, claim restrictions, exact artifact paths, and the next human decision.

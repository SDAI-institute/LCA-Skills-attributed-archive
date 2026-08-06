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

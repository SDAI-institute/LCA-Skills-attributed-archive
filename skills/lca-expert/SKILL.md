---
name: lca-expert
description: "Orchestrate rigorous end-to-end life cycle assessment work. Use for LCA, LCI, LCIA, product footprints, comparative studies, industrial process inventories, hotspot analysis, or when the correct LCA workflow or specialist is unclear."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---

# LCA Expert Orchestrator

Treat LCA as an iterative decision-support system, not a database lookup or a one-step emissions calculation.

## Select the operating mode

- Use `lca-intake` when the request is ambiguous, high stakes, or missing a decision context.
- Use `lca-plan` when the user wants a reviewable implementation plan before model work.
- Use `lca-work` to execute an approved plan in controlled increments.
- Use `lca-autopilot` only when the user explicitly requests an end-to-end autonomous run.
- Use `lca-debug` for a broken model, implausible result, failed tool run, or reproducibility problem.
- Use `lca-review` for independent QA or critical-review preparation.
- Use the specialist skills directly for narrow questions.

Read `references/routing.md`, `references/quality-gates.md`, `references/evidence-policy.md`, `references/output-contracts.md`, `references/expert-reasoning.md`, and `references/failure-modes.md` before making material study decisions.

## Completion contract

A complete response or durable study handoff must state:

1. intended decision, audience, commissioner, study type, and claim context;
2. functional unit, reference flow, boundary, geography, time, technology, and modeling approach, or the unresolved blockers;
3. data strategy, foreground/background split, tool, database/system model, and LCIA method with versions where known;
4. status and evidence for each applicable quality gate;
5. results with units, uncertainty, scenario dependence, limitations, and conclusions no stronger than the evidence;
6. durable artifact paths for scope, assumptions, decisions, model/data ledgers, calculations, checks, findings, and report;
7. specialist, verifier, program operator, or independent-review escalation required before external use.

Never call a study “ISO certified,” “verified,” or unqualifiedly “ISO compliant.” State the requirements addressed, evidence available, review performed, and work still required.

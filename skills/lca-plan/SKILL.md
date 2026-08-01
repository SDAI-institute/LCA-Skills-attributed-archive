---
name: lca-plan
description: "Create an executable, gate-based plan for an LCA study or model correction, with tasks, dependencies, evidence, acceptance criteria, tool routes, review points, and stop conditions. Use after intake/scope or before substantial implementation."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---

# LCA Study Plan

Translate the agreed study protocol into an implementation plan that another practitioner or agent can execute and audit.

Read `references/plan-schema.md`, `references/gate-dependencies.md`, and `references/risk-routing.md`.

## Plan rules

1. Read the goal and scope, intake brief, existing model/data ledgers, assumptions, decision log, and open findings.
2. State the baseline model state and the target completion state.
3. Decompose work into stable task IDs grouped by quality gate, not by conversational turn.
4. For every task record: objective, inputs, action, tool/skill, output artifact, acceptance criterion, dependencies, owner, review role, and failure/stop condition.
5. Put irreversible, licensed, high-cost, or claim-affecting operations behind explicit gates.
6. Include deterministic QA before LCIA, interpretation checks after calculation, and review/fix/recalculation loops.
7. Distinguish work that can run in parallel from work that depends on a frozen upstream choice.
8. Mark provisional choices and the sensitivity or data request that resolves them.
9. Save the plan as `study-plan.md`; do not silently implement while in plan-only mode.

## Required plan sections

- study identity and decision;
- current state and artifacts inspected;
- scope freeze criteria;
- data and inventory work packages;
- tool/environment qualification;
- calculation scenarios and method manifest;
- validation matrix;
- interpretation and uncertainty plan;
- specialist review plan;
- reporting and claim route;
- release/handoff/compound steps;
- open decisions and stop conditions.

## Completion gate

A plan is ready only when every task has an observable deliverable and acceptance criterion, all material dependencies are ordered, and no calculation is scheduled before scope and inventory gates.

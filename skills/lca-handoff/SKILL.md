---
name: lca-handoff
description: "Create or consume a durable LCA session handoff containing state, decisions, artifacts, tool versions, checks, open risks, and exact resume instructions. Use when pausing, transferring, resuming, or compacting a long-running study."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---

# LCA Handoff and Resume

Make the study resumable without relying on chat history.

Read `references/handoff-contract.md` and `references/resume-protocol.md`.

## Create a handoff

1. State study ID, current status, active plan revision, completed task IDs, and current quality gate.
2. List authoritative artifacts with paths, revisions, and hashes where material.
3. Summarize decisions and assumptions by their durable IDs; do not rewrite the full history.
4. Record tool, database, system-model, method, environment, and run identifiers.
5. Record checks run, results, unresolved findings, blockers, and claim/review restrictions.
6. Give one exact next action plus the evidence needed to complete it.
7. Save `handoff.md` and, when machine use matters, `handoff.json`.

## Resume a handoff

1. Verify the study identity and artifact hashes before trusting the summary.
2. Read the cited source artifacts, not only the handoff prose.
3. Re-run environment and status checks when software, database, branch, or time has changed.
4. Reopen unresolved decisions and findings; do not assume they were closed off-chat.
5. Continue from the named gate and update the handoff at the next pause.

A handoff is not valid if it omits the functional unit, model/scenario identity, open material risks, or next gate.

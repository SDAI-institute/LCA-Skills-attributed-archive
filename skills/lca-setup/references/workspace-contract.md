# Study workspace contract

The study directory is the authoritative record of scope, data, model state, decisions, QA, and released results.

## Required state transitions

`DRAFT_SCOPE -> SCOPE_FROZEN -> INVENTORY_READY -> CALCULATED -> INTERPRETED -> REVIEWED -> RELEASED`

A study may move backward when a material issue is found. Record the reason in `decision-log.md`.

## Artifact authority

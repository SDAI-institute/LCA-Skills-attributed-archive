# Study workspace contract

The study directory is the authoritative record of scope, data, model state, decisions, QA, and released results.

## Required state transitions

`DRAFT_SCOPE -> SCOPE_FROZEN -> INVENTORY_READY -> CALCULATED -> INTERPRETED -> REVIEWED -> RELEASED`

A study may move backward when a material issue is found. Record the reason in `decision-log.md`.

## Artifact authority

- `study.yaml`: identity, status, owners, versions, release state.
- `goal-and-scope.md`: frozen methodological protocol.
- `process-map.md`: process coverage and boundary.
- `model-ledger.csv`: implementation and provider mapping.
- `data-register.csv`: source-to-value provenance.
- `parameters.csv`: computational inputs, formulas, distributions, scenarios.
- `assumptions.csv`: unresolved or judgment-based choices.
- `decision-log.md`: rationale and changes.
- `qa-checklist.md`: gate evidence.
- `results/raw`: immutable tool exports.
- `results/processed`: transformed outputs with scripts/manifest.
- `report`: interpretation and review response.

## Rules

Never edit raw result exports in place. Never release a result whose manifest cannot identify study version, model/database/method version, functional unit, scenario, and calculation time. Licensed datasets and confidential inputs remain in controlled stores; commit only metadata or authorized derivatives.

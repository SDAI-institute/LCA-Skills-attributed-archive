# Skill and command catalog

Version 0.2.0 contains 28 canonical portable skills. In Claude Code plugin mode they are exposed as namespaced slash commands such as `/lca-skills:lca-expert`; in standalone Claude Code they are typically `/lca-expert`. ChatGPT and Claude.ai normally activate the consolidated `lca-expert` upload automatically instead of using Claude Code slash syntax. Codex invocation is host/version dependent and must be confirmed in the installed client.

## Orchestration and execution skills

| Skill | Invoke when | Primary durable outputs | Main gate contribution |
|---|---|---|---|
| `lca-expert` | End-to-end study, uncertain routing, or multi-domain request | routing decision, gate status, completion receipt | G0–G5 |
| `lca-intake` | Request is ambiguous, high-stakes, comparative, regulated, or missing decision context | `intake-brief.md`, risk/claim classification | G0A |
| `lca-setup` | New study or disorganized evidence/model files | complete study workspace and initialized contracts | setup |
| `lca-plan` | Scope is sufficiently clear and implementation needs reviewable tasks | `study-plan.md`, task dependencies, acceptance/stop criteria | G0B–G1 |
| `lca-work` | Execute approved plan tasks without silently changing scope | `work-receipt.json`, updated ledgers/artifacts | G1–G4 |
| `lca-autopilot` | User explicitly authorizes bounded end-to-end execution | full study candidate, receipts, open blockers, handoff | G0–G5 |
| `lca-calculate` | A pre-calculation gate has passed and a controlled run is required | `calculation-request.yaml`, tool manifest, raw/normalized results | G3 |
| `lca-debug` | Model/tool/result is broken, implausible, inconsistent, or non-reproducible | root-cause tree, evidence, controlled fix, regression check | affected gate |
| `lca-validate` | Determine readiness for calculation, interpretation, review, or release | `validation-report.json`, blocker list, gate recommendation | all |
| `lca-simplify` | Reduce model/workflow complexity while preserving decision-relevant behavior | simplification proposal, invariant checks, before/after evidence | G1–G4 |
| `lca-handoff` | Pause/resume work, transfer responsibility, or create machine-readable state | `handoff.md`, `handoff.json`, drift check | all |
| `lca-doctor` | Diagnose repository, package, host, Python, MCP, or optional tool availability | environment/qualification report | support |
| `lca-compound` | A lesson is validated, generalizable, lawful to share, and non-confidential | reusable reference/eval/update proposal | maintenance |

## Methodology, data, review, and reporting skills

| Skill | Invoke when | Primary durable outputs | Main gate contribution |
|---|---|---|---|
| `lca-scope` | Goal/scope, function, boundary, modeling rules, or review route are not frozen | `goal-and-scope.md`, decision/modeling rules | G0B |
| `lca-inventory` | Build or audit foreground processes and life-cycle inventory | process map, model ledger, balances, parameters, direct-emission models | G1–G2 |
| `lca-data` | Select sources/datasets, map formats, assess fit, or handle licensing/errata | data register/request, provider map, fit/provenance record | G1–G3 |
| `lca-impact` | Select/configure LCIA, inspect characterization, mapping, regionalization, normalization/weighting | `lcia-method-manifest.yaml`, coverage/mapping audit | G3 |
| `lca-interpret` | Explain results, hotspots, sensitivity, scenarios, uncertainty, and robustness | contribution/sensitivity/uncertainty outputs and decision conclusions | G4 |
| `lca-review` | Internal QA, red-team review, release gating, or critical-review preparation | findings, response log, review report/recommendation | G2–G5 |
| `lca-report` | Produce a decision-grade report, disclosure package, or claim matrix | report, claims register, release manifest | G5 |
| `lca-research` | A current method, standard, rule, parameter, dataset, or evidence gap must be resolved | source assessment, extracted parameter/evidence record | all |

## Tools, study types, and domains

| Skill | Invoke when | Primary durable outputs | Main gate contribution |
|---|---|---|---|
| `lca-openlca` | openLCA GUI/IPC setup, calculation, Monte Carlo, import/export, or diagnostics | environment and calculation manifests, normalized result receipt | G2–G4 |
| `lca-brightway` | Programmatic Brightway modeling, matrices, scenarios, uncertainty, or debugging | project/package manifest, calculation and matrix diagnostics | G2–G4 |
| `lca-greet` | Fuel/vehicle/energy/material pathway uses a named GREET product/release | exact product/pathway run manifest and reconciled export | G1–G4 |
| `lca-prospective` | Future/emerging technology, consequential, dynamic, temporal, spatial, or causal study | scenario/counterfactual protocol, future-background assumptions | G0–G4 |
| `lca-epd-pcf` | Product carbon footprint, EPD, PCR/PEFCR, PEF-style, or program-rule work | rule matrix, verification/claim readiness package | G0–G5 |
| `lca-sector` | Industrial/domain expertise is needed to model realistic processes and performance | sector modeling memo, domain checks, failure modes | G1–G2 |
| `lca-organization-social` | O-LCA, OEF, Scope 3 bridge, portfolio footprint, or social LCA | boundary reconciliation, indicator/evidence plan | G0–G5 |

## Compound workflow routes

### Deliberate expert workflow

```text
/lca-expert
  → /lca-intake
  → /lca-setup
  → /lca-scope
  → /lca-plan
  → /lca-work
  → /lca-validate
  → /lca-calculate
  → /lca-interpret
  → /lca-review
  → correction/recalculation
  → /lca-report
  → /lca-handoff
  → /lca-compound
```

### Explicit autonomous workflow

```text
/lca-autopilot <bounded request and workspace>
```

Autopilot may create/modify local study artifacts and invoke available local tools. It stops before publication, certification, verification, regulatory submission, purchasing/licensing, accepting terms, external transmission, or any claim requiring independent human review.

### Existing-model diagnosis

```text
/lca-debug <workspace, model, error, or anomalous result>
  → reproduce
  → localize layer
  → test hypotheses
  → apply smallest controlled fix
  → rerun regression and affected gates
```

### Existing-study audit

```text
/lca-review <frozen model/report/workspace>
  → select specialist reviewers
  → isolated read-only passes
  → normalize/deduplicate findings
  → owner responses and verification
  → release recommendation
```

## Common study routes

### Screening product LCA

`lca-intake → lca-scope → lca-plan → lca-sector → lca-inventory → lca-data → tool → lca-impact → lca-interpret → lca-review → lca-report`

### Industrial process from design data

`lca-scope → lca-sector → lca-inventory → physical closure → lca-data → tool → lca-impact → lca-interpret`

### Public comparative assertion

Use the full workflow, require functional equivalence and symmetric boundaries, invoke claims and critical-review perspectives, and leave external release pending qualified independent review. The plugin prepares evidence but cannot confer verification.

### Emerging technology or 2030/2050 scenario

`lca-intake → lca-scope → lca-prospective → lca-sector → lca-inventory → scenario/future background → lca-impact → lca-interpret → lca-review`

### EPD, PCF, or PEF-style study

Start with `lca-epd-pcf` to identify the governing program/PCR/PEFCR and current version, then route through scope, inventory, calculation, interpretation, review, and verification preparation.

### Organizational or social assessment

Start with `lca-organization-social`, explicitly reconcile organizational/product/inventory boundaries and indicator systems, then use shared data, review, and reporting skills without conflating the frameworks.

## Claude Code examples

Plugin mode:

```text
/lca-skills:lca-doctor
/lca-skills:lca-expert Frame a cradle-to-gate study for this hydrogen process.
/lca-skills:lca-plan lca/studies/green-hydrogen
/lca-skills:lca-work lca/studies/green-hydrogen tasks T-010 through T-025
/lca-skills:lca-review lca/studies/green-hydrogen for an internal investment decision
/lca-skills:lca-autopilot Build a screening study in lca/studies/demo; do not access external systems.
```

Standalone mode:

```text
/lca-expert Audit this existing study and route the work.
/lca-openlca Diagnose the zero-contribution product system.
/lca-brightway Reproduce this result in the pinned project.
/lca-greet Reconcile this R&D GREET export with its exact release and boundary.
```

## Consolidated ChatGPT/Claude.ai route

The upload package exposes one `lca-expert` skill. The orchestrator reads bundled modules from `references/modules/<skill>/SKILL.md`. Users can prompt:

```text
Use LCA Expert to create a gate-based plan for this cradle-to-gate study. Do not calculate until the pre-calculation checks pass.
```

No Claude Code slash-command behavior is assumed in these upload packages.

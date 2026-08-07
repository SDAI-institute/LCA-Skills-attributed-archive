# Compound-style LCA workflow

The repository adapts the useful operating pattern of Compound Engineering—research, plan, execute, review, correct, and compound—into a scientific LCA workflow. It does not copy a generic software loop unchanged: LCA requires functional-equivalence, physical-closure, flow-mapping, uncertainty, claim, and independent-review gates.

## Workflow principles

1. **Intake before implementation.** Identify the decision, audience, deliverable, claim route, stakes, and evidence threshold.
2. **Scope before calculation.** Freeze enough of the function, reference flow, boundary, modeling approach, data requirements, LCIA coverage, and review route to avoid calculating the wrong question.
3. **Plan before work.** Decompose the study into tasks with inputs, outputs, acceptance criteria, dependencies, owners, evidence, and stop conditions.
4. **Durable execution.** Store assumptions, decisions, data provenance, model identity, checks, and receipts in the study workspace rather than only in conversation context.
5. **Gates before progression.** Calculation and release are privileges earned by evidence, not default next steps.
6. **Independent perspectives before release.** Read-only specialist review detects different failure classes; correction remains separate.
7. **Recalculate after material correction.** A finding that changes the model invalidates affected results and interpretations until rerun.
8. **Compound only validated lessons.** Generalize non-confidential, lawful-to-share solutions with evidence and regression tests.

## Seven-stage lifecycle

### Stage 0 — Intake and authorization

Skills: `lca-intake`, `lca-expert`.

Outputs:

- decision and audience;
- study/deliverable type;
- claim and review class;
- confidentiality/licensing constraints;
- high-risk methodological topics;
- autonomy and external-action boundaries.

Gate G0A: intended use and evidence threshold are explicit.

### Stage 1 — Goal and scope

Skills: `lca-scope`, optionally `lca-epd-pcf`, `lca-prospective`, or `lca-organization-social`.

Outputs:

- functional unit and reference flow;
- system boundary and life-cycle stages;
- attributional/consequential/prospective logic;
- multifunctionality/recycling/cutoff rules;
- geography, time, technology, performance, and data-quality criteria;
- impact categories/method criteria;
- comparative/claim/review route.

Gate G0B: no material calculation ambiguity remains that could reverse interpretation.

### Stage 2 — Plan and workspace

Skills: `lca-setup`, `lca-plan`, `lca-doctor`.

Outputs:

- initialized workspace;
- task graph and acceptance criteria;
- data and model acquisition plan;
- environment/tool status;
- evidence and stop conditions.

Gate G1: each material requirement has an owner/source class/model location and quality expectation.

### Stage 3 — Inventory and data work

Skills: `lca-work`, `lca-inventory`, `lca-data`, `lca-sector`, `lca-research`.

Outputs:

- process map and foreground/background split;
- model/data/parameter/assumption registers;
- mass, energy, carbon, elemental, yield, recycle, purge, utility, and emissions calculations;
- provider links and transformation records;
- scenario definitions.

Gate G2: units, signs, reference products, providers, completeness, duplicate credits, and relevant physical balances pass.

### Stage 4 — Controlled calculation

Skills: `lca-calculate` plus `lca-openlca`, `lca-brightway`, `lca-greet`, or transparent calculation route.

Outputs:

- calculation request;
- tool/database/system-model/method/version identity;
- run parameters and hashes;
- raw and normalized inventory/impact/contribution results;
- cleanup/disposal receipt.

Gate G3: calculation identity, mapping, units, factors, exclusions, and result integrity are verified.

### Stage 5 — Interpretation

Skills: `lca-interpret`, `lca-prospective`, `lca-impact`.

Outputs:

- hotspot/contribution analysis;
- scenario and sensitivity analysis;
- uncertainty and data-quality interpretation;
- completeness/consistency checks;
- benchmark/triangulation;
- conditional conclusions and decision relevance.

Gate G4: conclusions are stable or explicitly conditional; false precision and unsupported ranking are removed.

### Stage 6 — Review, correction, and report

Skills: `lca-review`, `lca-debug`, `lca-work`, `lca-validate`, `lca-report`.

Outputs:

- selected specialist review plan;
- normalized/deduplicated findings;
- responses, corrections, verification, and recalculation;
- report, claims register, limitations, and review status;
- release recommendation.

Gate G5: model/report agree; critical findings are closed; claims match evidence; required external review is complete or explicitly pending.

### Stage 7 — Handoff and compounding

Skills: `lca-handoff`, `lca-compound`, `lca-simplify`.

Outputs:

- resumable state and drift signature;
- release manifest and hashes;
- open risks/next decision;
- generalized lesson, updated reference, or eval case.

## Plan/work receipt contract

`lca-plan` defines task IDs and acceptance criteria. `lca-work` executes only authorized IDs and writes a receipt containing:

- task and study identity;
- files read/created/changed;
- commands/tools and status;
- assumptions/decisions introduced;
- checks performed and evidence;
- results/findings;
- unresolved blockers;
- gate impact and recommended next action.

This makes agent work auditable and prevents a broad prompt from silently mutating scope.

## Autopilot contract

`lca-autopilot` is a bounded orchestrator, not permission to do anything needed to finish. It may:

- create and edit authorized local study files;
- execute available local deterministic tools;
- iterate review/correction/recalculation;
- produce a release candidate and handoff.

It must stop before:

- publishing or externally transmitting results;
- declaring certification, verification, assurance, or independent review;
- submitting to a regulator/program/operator;
- purchasing/licensing data or accepting terms;
- using inaccessible confidential/licensed data;
- overriding unresolved scope, physical, mapping, uncertainty, or review blockers.

## Specialist review model

The review orchestrator selects the smallest sufficient set of read-only perspectives. Reviewers return structured findings with severity, evidence, consequence, recommendation, owner, and verification requirement. The main workflow then:

1. normalizes identifiers/severity;
2. deduplicates by root cause and evidence;
3. rejects unsupported findings with rationale;
4. assigns accepted findings;
5. applies controlled corrections;
6. recalculates affected outputs;
7. verifies closure;
8. preserves the complete audit trail.

## Compounding rules

A lesson may enter shared repository knowledge only when it is:

- validated by evidence or a reproducible test;
- generalized beyond one client/file;
- non-confidential and lawful to share;
- version/context bounded;
- linked to the failure it prevents;
- accompanied by an eval or deterministic check when behavior changes.

Do not compound raw client data, purchased standards text, licensed dataset rows, credentials, or unverified practitioner guesses.

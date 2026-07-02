# Implementation roadmap

## Phase 0 — repository foundation (complete in v0.1)

- root-native Agent Skills structure and multi-host manifests;
- compact orchestrator and 17 specialist skills;
- methodology, tool, sector, QA, and research references;
- study artifact contract;
- source/update policy;
- deterministic validators and behavioral eval design.

Exit: repository validates and a synthetic study can be scaffolded, checked, and released.

## Phase 1 — minimum viable expert (priority)

1. Complete and test `new_study`, repository/study validation, balances, result comparison, and release hashing.
2. Add 15–20 adversarial evals covering core fatal errors.
3. Add synthetic end-to-end example studies:
   - reusable packaging;
   - chemical process with co-product;
   - hydrogen pathway;
   - battery service comparison.
4. Pin current source status and create an update issue template.
5. Validate skills in Claude Code and one open Agent Skills-compatible host.

Exit: consistently produces review-ready screening/internal studies from structured data.

## Phase 2 — tool depth

### openLCA

- demo JSON-LD database fixture;
- IPC health, descriptor, calculation, result extraction, disposal, and Monte Carlo scripts;
- provider/allocation/parameter-set audit;
- round-trip import/export regression.

### Brightway

- pinned Brightway 2.5 environment;
- synthetic biosphere/foreground/background fixture;
- `LCA` and current `MultiLCA` examples;
- uncertainty/scenario/temporal demonstrations;
- migration and version compatibility tests.

### GREET

- legally redistributable run-manifest templates and step-by-step UI workflow;
- release/variant selection decision tree;
- pathway edit diff and boundary reconciliation;
- automation only after validation against the current installed API.

Exit: tool runs are reproducible and cross-checked on common synthetic systems.

## Phase 3 — standards/program packs

- ISO 14040/44 operational conformance matrix;
- ISO 14071 review package;
- PCF and GHG Protocol bridge;
- EN 15804/ISO 21930 construction module pack;
- PEF/OEF transition and later EF 4.0 pack;
- organizational and social LCA packs;
- regional/program-specific packs loaded only when requested.

Because standards/PCR text is copyrighted, packs contain original decision workflows and user-supplied rule extraction, not copied clauses.

## Phase 4 — sector expert packs

For each sector, add equations, data-source hierarchy, benchmark distributions, process maps, common databases, and at least five evals. Prioritize SDAI alignment:

1. hydrogen and energy systems;
2. chemicals/bioprocesses;
3. waste/recycling/circular systems;
4. batteries/materials;
5. buildings/construction;
6. agriculture/food and water;
7. electronics/manufacturing and transport.

## Phase 5 — advanced methods

- prospective backgrounds with `premise`-style scenario manifests;
- consequential market and marginal-supplier evidence packs;
- temporal/dynamic LCA and time-resolved carbon;
- spatialized water/toxicity/land modules;
- hybrid process-EEIO and truncation checks;
- global sensitivity/correlation and Bayesian data updating;
- model-to-model ensemble and structural uncertainty.

## Phase 6 — human-expert operating system

- structured review queue and competence matrix;
- source ingestion with citation-to-parameter traceability;
- automated anomaly detection and benchmark library;
- claim approval workflow;
- project learning retrieval and promotion;
- client/program profiles with controlled rule packs;
- continuous eval dashboard with regression thresholds.

## Phase 7 — world-class benchmark

Target evidence:

- blinded senior-practitioner assessment across multiple sectors;
- reproducibility across openLCA and Brightway for reference systems;
- detection of >95% of seeded fatal errors;
- no fabricated citations/requirements in an adversarial source test;
- stable conclusions and correct escalation across public-claim cases;
- documented updates within one release cycle of material upstream changes.

## Prioritization principle

Invest first in errors that can change decisions or invalidate claims: function, boundary, allocation/recycling, direct emissions, provider links, units/signs, LCIA mapping, carbon/credit logic, uncertainty, and review. More sector breadth is less valuable than reliable detection of these failures.

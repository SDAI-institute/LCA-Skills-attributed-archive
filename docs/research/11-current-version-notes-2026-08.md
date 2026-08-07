# Current version notes — 2026-08-07 baseline

This file records time-sensitive facts that materially affect routing or code examples. It is a dated status snapshot, not a promise that these remain current.

## Agent Skills and plugin architecture

- The Agent Skills specification uses a directory containing `SKILL.md`, with optional `scripts/`, `references/`, and `assets/` resources.
- Skill metadata should remain concise; detailed knowledge belongs in progressively disclosed references.
- The Compound Engineering plugin's durable pattern is plan/research, execute, review, and compound validated learning. LCA Skills adapts that pattern into scope, inventory, calculation, interpretation, review, release, and compounding gates.
- Host-specific plugin manifests are compatibility metadata; the canonical source remains the root `skills/` tree.

## Standards requiring special attention

- ISO 14040:2006 and ISO 14044:2006 remain the core LCA standards, with published amendments recorded in the source register.
- ISO 14071:2024 and ISO 14072:2024 replace their earlier technical-specification editions.
- ISO 14075:2024 provides principles and a framework for social LCA.
- ISO 14025:2026 is the current Type III environmental declaration standard; ISO 14025:2006 is withdrawn. EPD/PCR work must identify program rules and transition requirements rather than silently citing the old edition.
- Standards text is copyrighted. This repository stores operational paraphrases and source metadata, not clauses or substitute copies.

## openLCA

- Current official IPC examples use `olca_ipc` for the client and `olca_schema` for model types.
- Current calculation returns a result object that can require `wait_until_ready()` before queries and should be disposed through the result lifecycle.
- Older official pages still show `import olca`, synchronous `SimpleResult`, and client-side disposal. Those examples are a separate client generation.
- JSON-RPC, REST, and gRPC expose related openLCA back-end capabilities but are not syntax-interchangeable.
- The official calculation-parameter example names a specific alpha package version at this status date. The skill intentionally records installed versions instead of making that value an evergreen pin.

## Brightway

- Current official documentation presents Brightway 2.5 as the stable modern generation and distinguishes it from legacy Brightway2 patterns. The `bw2calc` changelog records version 2.5.0 on 2026-05-16, including `PartitionedMonteCarloLCA` and a repeated-method-switch file-handle fix; snapshot the installed package set rather than treating this dated note as an evergreen pin.
- `bw2data`, `bw2calc`, `bw2io`, `bw_processing`, and related packages must be pinned as an environment, not assumed to move in lockstep.
- Current work should prefer documented project, node-ID, datapackage, `LCA`, and `MultiLCA` patterns for the installed versions. Legacy notebooks are evidence to migrate, not APIs to trust blindly.

## GREET

- The DOE R&D GREET page lists R&D GREET 2025 Rev1 with updates dated 2026-05-26 at this status date.
- R&D GREET is not interchangeable with every regulatory or program-specific GREET derivative.
- Record product, release, revision, platform/module, DOI, pathway, and input deltas for every run.

## Databases and methods

- ecoinvent 3.12 is the latest release recorded in the source register at this date; verify again before any new study. Its official known-issues section currently blocks two cut-off Ecological Scarcity 2021 biotic-resource category results, identifies an Australian cereal biogenic-carbon imbalance, and requires correction of a consequential aluminium cast-alloy market mass imbalance. The operational gate is `skills/lca-data/references/current-errata.md`.
- EPA identifies TRACI 2.2 as the current factor release at this date; record the implementation package as well as the method name.
- EF/PEF studies require the applicable EF method/data package, product-category rules where relevant, and current European Commission transition guidance.
- IPCC climate indicators require the assessment report, metric, time horizon, and treatment choices—not just the label “GWP.”

## Revalidation triggers

Recheck this snapshot when any of the following changes:

- plugin host or Agent Skills specification;
- ISO/EN standard edition or amendment;
- PCR/program instruction;
- LCA software, API client, or schema;
- database/system model;
- LCIA factors or elementary-flow mapping;
- regulatory program version;
- study release after six months or any material model rebuild.

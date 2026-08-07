# Changelog

All notable changes are documented here.

## [0.2.0] - 2026-08-07

### Added

- Portable canonical Agent Skills frontmatter for all skills.
- Host-specific build overlays rather than Claude-only fields in the source skills.
- Ten Compound-style workflow skills: `lca-intake`, `lca-plan`, `lca-work`, `lca-calculate`, `lca-debug`, `lca-validate`, `lca-handoff`, `lca-simplify`, `lca-autopilot`, and `lca-doctor`.
- Explicit-only autonomous LCA pipeline with plan-first execution, scientific stop conditions, external-action boundaries, correction loops, handoff, and compounding.
- Nine read-only Claude Code specialist agents for methodology, process engineering, data, LCIA, uncertainty, critical review, claims, tool integration, and sector review.
- Structured specialist-finding schema, review orchestration, deduplication, response, verification, and severity guidance.
- Claude Code PostToolUse validation hook and plugin-relative `.mcp.json` configuration.
- Dependency-free MCP stdio server implementing the 2025-11-25 lifecycle subset and exposing 13 LCA tools plus three resources.
- `lca_tools` CLI and runtime package.
- Read-oriented openLCA IPC and Brightway adapters, with exact installed-environment checks and no fabricated fallback calculations.
- GREET provenance manifest and result-ingestion adapter without redistributing licensed model content.
- Durable intake, study-plan, work-receipt, calculation-request, validation-report, review-response, and handoff artifacts.
- Workspace schema 1.1 with gate, plan revision, workflow mode, and handoff state.
- Deterministic multi-host build pipeline for portable, Claude Code, standalone Claude Code, Claude.ai, ChatGPT, and Codex packages.
- Single-skill consolidated upload builds for ChatGPT and Claude.ai with all specialist modules bundled under `references/modules/`.
- Per-package manifests, SHA-256 hashes, normalized ZIP timestamps, path-safety checks, and byte-deterministic rebuild tests.
- Deterministic full-source release archive, repository-wide local Markdown link validation, and reversible standalone installers with installation receipts.
- Host-qualification report that separates structural, runtime, host, and scientific evidence.
- Six additional adversarial eval cases covering autonomous public claims, frontmatter portability, missing runtimes, specialist-review merging, stale handoffs, and GREET regulatory misuse.
- Expanded automated tests for packages, MCP, agents, hooks, adapters, and compound workflow contracts.
- Platform-specific documentation and manual qualification checklists.

### Changed

- Increased the plugin from 18 to 28 skills.
- Moved Claude Code `argument-hint` and `disable-model-invocation` fields into a generated platform overlay.
- Reworked `lca-expert` into an operating-mode router and seven-stage gated workflow.
- Reworked `lca-review` into a multi-specialist, finding-driven review process.
- Upgraded study scaffolding from 23 to 31 templates.
- Strengthened repository validation to check portable frontmatter, all routed references, agents, hooks, MCP registration, version synchronization, and platform overlays.
- Strengthened workspace validation to check gate/status consistency, plan revision, workflow mode, JSON contracts, and handoff synchronization.
- Updated manifests and runtime package to version 0.2.0.

### Qualification status

- Source, distributions, MCP handshake, deterministic utilities, and synthetic regression tests pass locally.
- Real ChatGPT, Claude.ai, Claude Code, Codex, openLCA, Brightway, and GREET qualification remains environment-specific and is never inferred from static package validation.

## [0.1.0] - 2026-08-07

### Added

- Root-native Agent Skills plugin architecture.
- End-to-end LCA orchestrator and seventeen specialist skills (18 skills total).
- Standards, methodology, industrial modeling, tool, sector, review, and epistemic references.
- openLCA IPC, Brightway, and R&D GREET playbooks.
- Study workspace scaffolding and validation scripts.
- Senior-practitioner behavioral eval suite.
- Source register and update policy.
- Synthetic inventory-ready worked example.
- Windows skill synchronization and repository handoff tooling.

# LCA Skills

**A portable, source-grounded expert system for professional life cycle assessment.**

LCA Skills turns LCA methodology, industrial process knowledge, tool workflows, quality gates, specialist review, and durable study records into a reusable Agent Skills plugin. It is designed to help an AI assistant behave more like a careful senior LCA practitioner and less like a one-prompt emissions calculator.

Version **0.2.0** contains:

- **28 portable LCA skills** with progressive-disclosure references;
- **9 read-only Claude Code specialist agents** for independent review passes;
- **13 local MCP tools** for study management, QA, openLCA, Brightway, and GREET workflows;
- **31 durable study templates**;
- **34 adversarial practitioner eval cases**;
- **37 deterministic Python tests**;
- reproducible build targets for Claude Code, standalone Claude Code, Claude.ai, ChatGPT, Codex, and generic Agent Skills hosts.

## What it can do

The system supports the full assessment lifecycle:

```text
intake
  → goal and scope
  → gate-based plan
  → process and inventory engineering
  → data and database selection
  → controlled calculation
  → LCIA and flow-mapping checks
  → contribution, scenario, sensitivity, and uncertainty analysis
  → parallel specialist review
  → controlled correction and recalculation
  → reporting and claim control
  → release candidate, handoff, and reusable learning
```

It covers:

- ISO 14040/14044-style LCA and LCI workflows;
- product carbon footprints, EPD-supporting models, PEF-style work, organizational LCA, and social LCA routing;
- attributional, consequential, prospective, dynamic, temporal, spatial, hybrid, and scenario-based studies;
- process-engineered inventories using mass, energy, carbon, elemental, yield, recycle, purge, and utility balances;
- openLCA IPC, modern Brightway, and Argonne R&D GREET workflows;
- energy, hydrogen, fuels, chemicals, bioprocesses, metals, materials, batteries, manufacturing, buildings, transport, agriculture/food, water, waste, and circularity;
- functional equivalence, allocation, system expansion, substitution, recycling, cutoffs, biogenic carbon, land-use change, data quality, uncertainty, and critical-review preparation;
- reproducibility, version control, provenance, model diagnostics, result reconciliation, reporting, and release control.

The repository contains original operational guidance and paraphrased summaries. It does **not** redistribute ISO standards, proprietary PCRs, licensed databases, characterization-factor packages, or commercial models.

## Architecture

### 1. Portable core

Every canonical `skills/<name>/SKILL.md` follows the open Agent Skills frontmatter contract. Canonical skills contain no Claude-only fields such as `argument-hint`, `context`, or `disable-model-invocation`.

### 2. Host overlays

The build pipeline injects host-specific behavior only into host-specific packages:

- Claude Code gets autocomplete hints, explicit-only protection for `lca-autopilot`, agents, hooks, and `.mcp.json`;
- Claude.ai and ChatGPT get a single uploadable `lca-expert/` skill with all modules bundled under `references/modules/`;
- Codex gets portable skills plus the Codex plugin manifest;
- generic hosts get the unmodified portable `skills/` tree.

### 3. Compound-style execution

The workflow is modeled after the strongest parts of Compound Engineering: research and intake, explicit planning, controlled work, review, correction, validation, handoff, and compounding. LCA-specific scientific and claim gates prevent the autonomous workflow from treating a completed calculation as a defensible study.

### 4. Runtime and tool adapters

The optional `lca_tools` Python package provides:

- a command-line interface;
- a dependency-free MCP stdio server;
- study creation, validation, balance checks, claim checks, result comparison, and release hashing;
- current-schema openLCA IPC access when `olca_ipc` and `olca_schema` are installed;
- read-only Brightway calculations against an existing project, activity, and method;
- GREET run manifests and result-export ingestion without copying licensed model content.

Adapter code being present does **not** prove that a target host can access your local software, databases, or licensed files. The qualification report distinguishes structural, runtime, host, and scientific evidence.

## Skill map

### Orchestration and execution

| Skill | Purpose |
|---|---|
| `lca-expert` | Main router and end-to-end orchestrator |
| `lca-intake` | Decision, deliverable, evidence, claim, and risk classification |
| `lca-setup` | Durable study workspace initialization or repair |
| `lca-plan` | Gate-based tasks, dependencies, outputs, and acceptance criteria |
| `lca-work` | Execute only approved tasks and return a work receipt |
| `lca-autopilot` | Explicit-only end-to-end pipeline with scientific and external-action stop conditions |
| `lca-validate` | Gate readiness and release-blocker assessment |
| `lca-debug` | Scientific, data, matrix, tool, and reproducibility failure diagnosis |
| `lca-simplify` | Reduce model/workflow complexity while preserving material invariants |
| `lca-handoff` | Create or resume a durable, drift-checked study handoff |
| `lca-doctor` | Repository, package, environment, host, and tool qualification diagnostics |
| `lca-compound` | Promote validated, non-confidential lessons into reusable knowledge and evals |

### Methodology and interpretation

| Skill | Purpose |
|---|---|
| `lca-scope` | Goal, functional unit, reference flow, boundary, modeling rules, review route |
| `lca-inventory` | Foreground system, balances, emissions, utilities, co-products, waste, end of life |
| `lca-data` | Evidence hierarchy, dataset fit, databases, interoperability, licensing, errata |
| `lca-impact` | LCIA method choice, characterization, coverage, regionalization, normalization/weighting controls |
| `lca-calculate` | Controlled calculation request, run identity, outputs, and reconciliation |
| `lca-interpret` | Hotspots, contribution, scenarios, sensitivity, uncertainty, robustness, limitations |
| `lca-review` | Parallel specialist QA, finding normalization, deduplication, verification, critical-review preparation |
| `lca-report` | Decision-grade reporting, claim matrix, limitations, release manifest |
| `lca-research` | Defensible evidence discovery, extraction, currency, and source management |


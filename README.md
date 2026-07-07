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

### Tools and domains

| Skill | Purpose |
|---|---|
| `lca-openlca` | openLCA GUI, IPC, calculation, Monte Carlo, imports/exports, diagnostics |
| `lca-brightway` | Programmatic Brightway projects, matrices, calculations, scenarios, uncertainty |
| `lca-greet` | Exact GREET product/release/pathway provenance and result reconciliation |
| `lca-prospective` | Consequential, prospective, dynamic, temporal, spatial, and future-background studies |
| `lca-epd-pcf` | PCF, EPD, PCR/PEFCR, PEF-style, verification and program-rule workflows |
| `lca-sector` | Sector-specific process knowledge and modeling traps |
| `lca-organization-social` | Organizational LCA, OEF/Scope 3 bridges, and social-LCA routing |

## Invocation by host

| Host/package | Typical invocation | Capability level in this repository |
|---|---|---|
| Claude Code plugin | `/lca-skills:lca-expert` | Namespaced skills, 9 agents, hook, MCP registration |
| Standalone Claude Code skills | `/lca-expert` | Unnamespaced skills and copied read-only agents |
| Claude.ai upload | Automatic; ask to use “LCA Expert” when testing | Single portable upload skill |
| ChatGPT upload | Automatic; ask to use “LCA Expert” when testing | Single portable upload skill |
| Codex | Commonly `$lca-expert`; confirm installed-host syntax | Portable skills plus Codex manifest |
| Generic Agent Skills host | Host-specific | Canonical `skills/` tree |

Host behavior changes over time. Use the platform-specific guide and record a real import/invocation test rather than treating file structure as proof of host support.

## Repository and release packages

Build all targets with:

```bash
python scripts/build_distributions.py --clean
python scripts/build_source_release.py
python scripts/validate_distributions.py
```

The six host ZIPs are placed in `dist/packages/`:

```text
LCA-Skills-ClaudeCode-v0.2.0.zip
LCA-Skills-ClaudeStandalone-v0.2.0.zip
LCA-Skills-ClaudeAI-v0.2.0.zip
LCA-Skills-ChatGPT-v0.2.0.zip
LCA-Skills-Codex-v0.2.0.zip
LCA-Skills-Portable-v0.2.0.zip
```

The deterministic full repository archive is placed at `dist/source/LCA-skills-v0.2.0.zip`. Host packages contain `bundle-manifest.json`; the source archive contains `SOURCE-RELEASE.json` and companion SHA-256 files. ZIP timestamps are normalized so repeated builds from the same source are byte-deterministic.

## Installation

### Validate the source repository

```bash
python scripts/validate_repo.py --strict
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/build_distributions.py --clean
python scripts/build_source_release.py
python scripts/validate_distributions.py
python scripts/host_qualification.py --output host-qualification.json
```

### Claude Code plugin

Extract `LCA-Skills-ClaudeCode-v0.2.0.zip`, then run:

```bash
claude --plugin-dir /path/to/lca-skills
```

Inside Claude Code, test:

```text
/lca-skills:lca-doctor
/lca-skills:lca-expert Frame a cradle-to-gate LCA for this process.
```

`lca-autopilot` is deliberately marked explicit-only in the Claude Code build.

### Standalone Claude Code

Extract the standalone package and run `install.ps1` on Windows or `install.sh` on macOS/Linux. It copies skills to `~/.claude/skills` and agents to `~/.claude/agents`, writes an installation receipt, and includes matching uninstall scripts. It intentionally does not modify global hooks or MCP settings.

### Claude.ai

Upload `LCA-Skills-ClaudeAI-v0.2.0.zip` through **Customize → Skills → Create skill → Upload a skill**, then enable it. The ZIP has exactly one top-level `lca-expert/` directory whose name matches the `name` field.

### ChatGPT

Upload `LCA-Skills-ChatGPT-v0.2.0.zip` from the Skills interface. ChatGPT scans uploaded skills before making them available. Plan, workspace, role, and product-surface settings can affect availability.

### Codex

Use the Codex package with the installed Codex plugin/skill workflow. The current environment used to build this release did not contain a Codex executable, so the package is structurally qualified but still requires a real import and invocation transcript.

See `docs/installation.md` and `docs/platforms/` for exact platform checklists.

## Durable study workspace

`lca-setup` creates a workspace that does not depend on chat memory:

```text
study.yaml
intake-brief.md
study-plan.md
goal-and-scope.md
process-map.md
model-ledger.csv
data-register.csv
data-request.csv
parameters.csv
assumptions.csv
scenario-register.csv
balances.csv
claims-register.csv
decision-log.md
qa-checklist.md
work-receipt.json
handoff.md
handoff.json
tool-runs/calculation-request.yaml
tool-runs/*-run-manifest.yaml
review/review-plan.md
review/review-findings.csv
review/review-response-log.csv
results/processed/*.csv
results/validation/validation-report.json
results/release/release-manifest.json
report/report-outline.md
```

The state machine is:

```text
DRAFT_SCOPE → SCOPE_FROZEN → INVENTORY_READY → CALCULATED
            → INTERPRETED → REVIEWED → RELEASED
```

Material findings can reopen an earlier gate. `handoff.json`, plan revision, run manifests, and hashes are checked for drift before a resumed study relies on old results.

## MCP and CLI

Install the local runtime from the repository when desired:

```bash
python -m pip install -e .
lca-skills doctor --text
lca-skills study new demo-study --title "Demo study"
lca-skills study validate ./lca/studies/demo-study
```

The Claude Code plugin registers `lca_tools/mcp_server.py` as a local stdio MCP server. Its 13 tools are conservative: study creation is non-destructive, QA and calculation adapters are read-oriented, and optional endpoint checks are opt-in.

## Quality and qualification

The release distinguishes four evidence levels:

1. **Structural** — file shape, frontmatter, references, manifests, hashes, ZIP integrity.
2. **Runtime** — a representative command worked in the current environment.
3. **Host** — the package was actually imported and invoked in ChatGPT, Claude.ai, Claude Code, or Codex.
4. **Scientific** — a named tool/database/method known case was reconciled and reviewed by a competent practitioner.

The included synthetic matrix fixture validates software scaling and matrix semantics only. It is explicitly **not** an LCIA method or scientific benchmark.

Before a production tool claim, follow `docs/tool-integration-test-plan.md`. Before a public comparison, EPD, regulatory use, assurance claim, or high-consequence decision, obtain the independent review or verification required by the governing program and competent professional judgment.

## Non-negotiable rules

1. The decision and audience define the model; an available database does not define the study.
2. A functional unit quantifies service and performance, not merely product mass.
3. Every material conclusion must trace to evidence, a parameter, an assumption, a model version, or documented expert judgment.
4. Unit, sign, provider-link, identity, coverage, and relevant conservation checks precede interpretation.
5. Tool success does not prove model completeness or scientific validity.
6. Uncertainty and methodological choices limit conclusions; differences smaller than plausible uncertainty are not decisive.
7. The plugin never claims that its own output is “ISO certified,” independently verified, or an assurance opinion.
8. Autonomous execution stops before unauthorized publication, certification, submission, purchase, transmission, or destructive external action.
9. Licensed data and copyrighted standards are referenced lawfully and never redistributed.
10. Missing tools, data, rules, or evidence are reported as blockers—not replaced with fabricated runs or plausible numbers.

## Repository map

```text
skills/                 portable canonical skills
agents/                 Claude Code specialist reviewers
hooks/                  Claude Code validation hook
platforms/              host overlays and packaging rules
lca_tools/              CLI, MCP server, and tool adapters
assets/templates/       durable study templates
scripts/                validation, build, qualification, and QA utilities
docs/research/          deep-research foundation
docs/platforms/         host-specific installation and qualification guides
tests/evals/            adversarial senior-practitioner cases
examples/                synthetic, non-scientific regression study
knowledge/solutions/    validated reusable lessons
```

## Current qualification status

The source repository, all six distributions, MCP handshake/tool catalog, study utilities, deterministic ZIPs, and synthetic regression fixture are locally tested. In the build environment used for this release:

- Claude Code and Codex executables were **not installed**;
- ChatGPT and Claude.ai uploads were **not performed** because those require the user’s eligible account and UI;
- openLCA, Brightway, and a local GREET model were **not installed or scientifically reconciled**.

Run `scripts/host_qualification.py` in the target environment to replace those statuses with evidence. Do not convert `NOT TESTED` into `PASS` without a representative recorded test.

## Legal and methodological notice

This software assists expert work; it does not replace competent professional judgment, independent critical review, verification, assurance, program-operator approval, or legal advice. Users remain responsible for lawful standards and dataset access, licenses, confidentiality, method selection, model validity, and the exact claims they release.

Original repository content is licensed under MIT. Third-party standards, software, datasets, methods, and trademarks remain subject to their own terms.

# LCA Skills architecture

## Design objective

LCA Skills is an expert workflow system rather than a monolithic prompt or a numerical lookup layer. It must support explanation, study execution, model/tool operation, review, and durable handoff without confusing those activities or overstating available evidence.

The architecture combines three patterns:

1. **Agent Skills portability** — small discoverable `SKILL.md` files with optional references, scripts, and assets;
2. **Compound execution** — intake/research, explicit planning, controlled work, review, correction, validation, handoff, and reusable learning;
3. **LCA scientific governance** — functional equivalence, modeling rules, inventory closure, method coverage, uncertainty, review, and claim-release gates.

## Source-of-truth layers

### Layer 1 — portable canonical skills

`skills/<name>/SKILL.md` is the canonical source. Top-level frontmatter is limited to fields accepted by the Agent Skills specification:

```yaml
name:
description:
license:
compatibility:
metadata:
allowed-tools:   # optional/experimental
```

Canonical source does not contain Claude Code-only fields. This prevents a host-specific convenience from making the same skill invalid in ChatGPT, Claude.ai, Codex, or another Agent Skills implementation.

### Layer 2 — progressive-disclosure references

Each skill owns focused references under `references/`. The skill routes explicitly to those files. Detailed standards logic, sector knowledge, error taxonomies, tool workflows, and reviewer personas remain outside the compact discovery and orchestration layer.

### Layer 3 — host overlays

`platforms/claude-code/skill-overrides.json` contains Claude Code metadata such as:

```yaml
argument-hint:
disable-model-invocation:
```

The build script injects those fields only into Claude Code distributions. `lca-autopilot` is explicit-only there.

### Layer 4 — executable assurance

`lca_tools/` and `scripts/` convert critical checks into deterministic operations:

- workspace creation and validation;
- balance closure;
- claim screening;
- result comparison;
- release hashing;
- environment diagnostics;
- openLCA, Brightway, and GREET adapters;
- MCP stdio tools;
- host distribution building and qualification.

These utilities support evidence. They do not replace methodological reasoning or independent review.

### Layer 5 — durable study state

A study workspace, not chat history, is the authoritative record. Its key artifacts include intake, plan, protocol, model/data/parameter ledgers, assumptions, decisions, balances, calculation requests, run manifests, processed results, findings, responses, validation, release hashes, and handoff state.

### Layer 6 — institutional learning

`lca-compound` promotes only validated, generalized, non-confidential lessons into `knowledge/solutions/`, skill references, tests, or evals. Project-specific facts stay in the study workspace.

## Topology

```text
lca-expert
├── lca-intake
├── lca-setup
├── lca-plan
├── lca-work
│   ├── lca-scope
│   ├── lca-inventory ── lca-data ── lca-sector
│   ├── lca-impact
│   ├── lca-calculate
│   │   ├── lca-openlca
│   │   ├── lca-brightway
│   │   └── lca-greet
│   ├── lca-prospective
│   ├── lca-epd-pcf
│   └── lca-organization-social
├── lca-interpret
├── lca-review ── specialist agents
├── lca-debug / lca-simplify
├── lca-validate
├── lca-report
├── lca-handoff
├── lca-compound
├── lca-research
├── lca-doctor
└── lca-autopilot  (explicit-only orchestrated path)
```

The orchestrator owns workflow state. Tool, method, and sector modules cannot silently redefine the frozen goal and scope.

## Compound-style execution model

### Interactive mode

Use for questions, methodological decisions, partial studies, or when the user wants to approve each stage.

### Plan-led mode

Use when the deliverable is known but work must be split into reviewable tasks. `lca-plan` creates task IDs, dependencies, outputs, acceptance criteria, owners, gates, and stop conditions. `lca-work` executes only authorized task IDs and returns a work receipt.

### Autopilot mode

Use only after explicit user authorization for an end-to-end run. The pipeline is:

```text
authorize
→ intake
→ initialize and diagnose
→ freeze scope
→ approve plan
→ build inventory/data
→ validate inventory
→ calculate
→ interpret
→ parallel specialist review
→ correct/recalculate/revalidate
→ report and check claims
→ prepare release candidate
→ handoff and compound
```

Autopilot may not independently publish, certify, submit, purchase licensed content, accept legal terms, transmit confidential data, or represent its own review as independent verification.

## State and gates

### Study status

```text
DRAFT_SCOPE
  → SCOPE_FROZEN
  → INVENTORY_READY
  → CALCULATED
  → INTERPRETED
  → REVIEWED
  → RELEASED
```

### Gate model

| Gate | Meaning | Minimum evidence |
|---|---|---|
| G0 | Intake accepted | decision, deliverable, audience, risk, evidence route |
| G1 | Scope frozen | function, FU, reference flow, boundary, modeling rules, review route |
| G2 | Inventory ready | model/data ledgers, provider links, units, coverage, balances |
| G3 | Calculation accepted | exact run identity, methods, mappings, outputs, deterministic checks |
| G4 | Interpretation accepted | contributions, scenarios, sensitivity, uncertainty, limitations |
| G5 | Review resolved | findings, responses, verification, no release-blocking defects |
| G6 | Release authorized | report, claims, review status, hashes, decision-owner approval |

A material finding can reopen an earlier gate. The plan revision and decision log record the transition.

## Specialist review architecture

Claude Code packages include nine read-only agents:

- methodologist;
- process engineer;
- data auditor;
- LCIA specialist;
- uncertainty specialist;
- critical reviewer;
- claims/reporting reviewer;
- tool integrator;
- sector specialist.

They share a structured finding contract but are selected dynamically. Review output is normalized to stable IDs and root causes. Equivalent findings are deduplicated without erasing evidence, severity disagreement, or minority concerns. Review agents do not write model files or close their own material findings. Corrections return through `lca-work` or `lca-debug`; affected calculations and validations are repeated.

Portable and consolidated packages retain the same reviewer intelligence as persona references when host-native agents are unavailable.

## Runtime architecture

### CLI

`lca_tools.cli` exposes study, openLCA, Brightway, GREET, and doctor commands. It uses zero mandatory dependencies; optional tool packages are installed separately.

### MCP

`lca_tools/mcp_server.py` is a newline-delimited JSON-RPC stdio server. It implements a conservative MCP lifecycle subset and exposes 13 tools plus three read-only resources. Protocol messages are written only to stdout; diagnostics go to stderr.

The server uses annotations to distinguish read-only and non-destructive operations. Endpoint probing is opt-in. Tool exceptions become explicit errors rather than fabricated outputs.

### openLCA

The adapter uses the schema-separated `olca_ipc` and `olca_schema` generation when available. Calculations use explicit product-system and optional method IDs, retrieve structured results, and dispose result handles. The adapter does not create or mutate models.

### Brightway

The adapter operates only on an existing project, database, activity code, amount, and method tuple. It records the previous active project and restores it after calculation. It does not create projects or import databases.

### GREET

Because GREET products and regulatory variants do not expose one universal stable automation contract, the adapter focuses on exact product/release/revision/platform/pathway provenance, input/result export hashes, and normalized result ingestion. It does not pretend that R&D GREET is interchangeable with a regulatory model.

## Distribution architecture

| Target | Package shape | Host-specific behavior |
|---|---|---|
| Portable | `lca-skills-portable/skills/*` | None |
| Claude Code plugin | `lca-skills/` | Claude overlays, 9 agents, hook, `.mcp.json` |
| Claude Code standalone | `lca-skills-standalone/` | Claude overlays plus installers; no settings mutation |
| Claude.ai | one `lca-expert/` skill | All modules bundled under `references/modules/` |
| ChatGPT | one `lca-expert/` skill | All modules bundled under `references/modules/` |
| Codex | `lca-skills/` | Codex manifest plus portable skills |

The consolidated upload builds contain one discoverable root skill. Nested module `SKILL.md` files are treated as reference instructions, not assumed host-native skills.

## Build and integrity

`scripts/build_distributions.py`:

1. copies canonical source;
2. applies allowed host overlays;
3. creates consolidated upload routing where needed;
4. adds runtime/templates/docs appropriate to the target;
5. writes a per-file `bundle-manifest.json`;
6. creates ZIPs with sorted entries and normalized timestamps.

`scripts/validate_distributions.py` verifies frontmatter, module counts, package components, resource paths, manifest hashes, ZIP paths, CRCs, and deterministic timestamps.

## Qualification model

The architecture prohibits one ambiguous “tested” label.

- **Structural:** files and package contracts are correct.
- **Runtime:** a command executed successfully in the current environment.
- **Host:** the package imported and invoked in the actual target host.
- **Scientific:** a named tool/database/method known case was reconciled and reviewed.

A package can pass structural tests while remaining `NOT TESTED` in a host. A tool adapter can execute while remaining scientifically unqualified for a study.

## Trust and safety boundaries

- no credentials in skills, manifests, fixtures, or logs;
- no licensed database or copyrighted standards content in the repository;
- no hidden network probing;
- no destructive model writes in calculation adapters;
- no external publication or certification by autopilot;
- no claim of independent review by the same system that built the model;
- no plausible-number fallback when a tool, database, rule, or evidence source is missing;
- no conclusion stronger than the uncertainty, functional equivalence, or study scope supports.

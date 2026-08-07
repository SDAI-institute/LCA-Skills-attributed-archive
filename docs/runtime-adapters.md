# Runtime adapters, CLI, and MCP

The optional `lca_tools` package converts selected repository contracts into deterministic local operations. Its purpose is to make study work auditable and repeatable—not to hide scientific assumptions behind automation.

## Installation

Core runtime only:

```bash
python -m pip install -e .
```

Optional openLCA support:

```bash
python -m pip install -e ".[openlca]"
```

Optional Brightway support:

```bash
python -m pip install -e ".[brightway]"
```

Optional MCP SDK is not required by the bundled dependency-free stdio server, but is available for future SDK-based integrations:

```bash
python -m pip install -e ".[mcp-sdk]"
```

## CLI overview

```bash
lca-skills --version
lca-skills doctor --text
lca-skills study new <slug> --title "<title>"
lca-skills study validate <study> --strict
lca-skills study balance <balances.csv>
lca-skills study claims <study>
lca-skills study compare <baseline.csv> <candidate.csv>
lca-skills study hash <study> --update-release
lca-skills openlca snapshot --check-endpoint
lca-skills openlca list ProductSystem
lca-skills openlca calculate <product-system-id> --impact-method-id <id>
lca-skills brightway snapshot
lca-skills brightway calculate --project <p> --database <db> --code <code> --method '<tuple>'
lca-skills greet manifest ...
lca-skills greet import-results <results.csv>
```

All commands return structured JSON except the optional human-readable doctor view. Errors return nonzero status and a JSON error object on stderr.

## Workspace operations

### New study

Creates a schema-versioned directory from `assets/templates/`, including intake, scope, planning, data/model ledgers, calculation request, tool manifests, QA, review, reporting, release, handoff, validation, and work-receipt contracts.

### Validate study

Checks required files, study identity, gate/status vocabulary, plan revision, JSON/YAML/CSV contracts, handoff synchronization, review responses, and release semantics. It validates structure and workflow state, not the scientific truth of the inventory.

### Balance check

Reads the normalized balance table and applies absolute/relative tolerance logic by metric. Passing arithmetic closure does not prove that every process or element is represented correctly.

### Claim check

Flags unsupported certification/verification/compliance/superiority/carbon-neutral language based on the claims register and review status.

### Result comparison

Reconciles normalized tables by keys, units, tolerances, missing rows, and numeric differences. Tolerances should reflect known numerical representation—not be widened to hide methodological differences.

### Hash manifest

Produces per-file SHA-256 evidence and can update the release manifest. Hashes prove file identity, not correctness or authorization to redistribute.

## openLCA adapter

The adapter uses the current split packages:

- `olca_ipc`
- `olca_schema`

It is deliberately read-oriented:

- environment snapshot;
- descriptor listing;
- product-system calculation by stable ID;
- optional impact method;
- inventory/impact extraction;
- result disposal.

It does not create or mutate database entities in v0.2.0. This reduces destructive risk while the integration is qualified. The adapter checks required packages and fails explicitly when absent.

Manual verification remains required for:

- database and system model;
- product-system quantitative reference and amount;
- allocation and parameter state;
- elementary-flow mapping and LCIA implementation;
- asynchronous readiness and result completeness;
- licensed-data handling.

## Brightway adapter

The adapter requires `bw2data` and `bw2calc`. It:

- snapshots the package/project environment;
- selects an existing named project;
- resolves an activity by stable database/code identity;
- validates the exact method tuple;
- performs LCI/LCIA;
- returns a normalized receipt;
- restores the previous project where possible.

It does not import databases, create activities, mutate exchanges, rebuild processed data, or implement Monte Carlo in v0.2.0. Those are higher-risk workflows that remain in the skill guidance until explicit adapters and integration fixtures are added.

## GREET adapter

GREET products lack one universal interchangeable automation contract. The adapter therefore:

- creates an exact product/release/revision/platform/pathway manifest;
- hashes local model/input/result artifacts without redistributing them;
- records boundary, functional basis, LHV/HHV and co-product/GWP fields to complete;
- validates and normalizes exported result CSVs.

It does not claim to execute arbitrary GREET desktop/web/regulatory products. A product-specific runner must be separately implemented and qualified.

## MCP server

Start directly:

```bash
python lca_tools/mcp_server.py
```

The server uses newline-delimited JSON-RPC over stdio and implements the MCP initialization/tool/resource subset needed by this plugin. It advertises protocol version `2025-11-25`.

### Tools

1. `lca_doctor`
2. `lca_new_study`
3. `lca_validate_study`
4. `lca_check_balance`
5. `lca_check_claims`
6. `lca_compare_results`
7. `openlca_snapshot`
8. `openlca_list_descriptors`
9. `openlca_calculate`
10. `brightway_snapshot`
11. `brightway_calculate`
12. `greet_build_manifest`
13. `greet_import_results`

### Resources

- skill catalog;
- authoritative source register;
- architecture guide.

The server must never emit logs or arbitrary text on stdout because that would corrupt the protocol. Diagnostic logs belong on stderr.

## Security and operational controls

- Endpoint probing is opt-in.
- No credentials are stored or requested by the core adapters.
- No database/model mutation is performed by the current openLCA/Brightway adapters.
- Paths are resolved and validated before use.
- Tool absence produces an explicit error.
- External publication/submission is outside adapter scope.
- Licensed and confidential data remain local and are excluded from package/tests.
- MCP tool availability is not scientific qualification.

## Extension contract

A new adapter operation must include:

1. clear input/output schema;
2. stable identifier strategy;
3. version/environment snapshot;
4. dry-run or read-only default where practical;
5. explicit mutation/side-effect declaration;
6. cleanup/rollback behavior;
7. deterministic unit tests;
8. integration fixture and seeded failures;
9. licensing/confidentiality controls;
10. behavioral eval for likely misuse;
11. source-register and changelog update;
12. honest qualification status.

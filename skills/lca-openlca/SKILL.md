---
name: lca-openlca
description: "Build, automate, calculate, troubleshoot, and validate LCA models in openLCA 2 using the GUI, JSON-LD/openLCA schema, and IPC clients. Use for databases, processes, product systems, parameters, allocation, projects, uncertainty, Monte Carlo, contribution analysis, imports/exports, or openLCA API workflows."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---
# openLCA Specialist

Use the installed openLCA version and official documentation as the source of truth. Record desktop/server, database, IPC client, and schema versions.

## Safety first

- Work on a copy or versioned database before automated mutation.
- Bind IPC to localhost unless explicitly secured.
- Confirm the active database; IPC operations act on it.
- Use stable UUIDs/identifiers, not names alone, after discovery.
- Dispose calculation and simulator objects.
- Never assume allocation factors automatically refresh; verify saved factors before product-system calculation.

## Choose a workflow

Read:

- `references/gui-workflow.md` for interactive modeling;
- `references/ipc-workflow.md` for Python/JSON-RPC/REST automation;
- `references/import-export.md` for JSON-LD, ILCD, ecoSpold, Excel, and package exchange;
- `references/calculation-analysis.md` for calculation, contribution, projects, scenarios, and Monte Carlo;
- `references/troubleshooting.md` for errors and QA.

## Standard model build

1. Confirm database/system model, units, flows, locations, and impact method.
2. Create or inspect foreground flows and processes.
3. Set quantitative reference and provider links.
4. Add parameters with units documented in comments/metadata.
5. Calculate and save allocation factors if required.
6. Create/link the product system using the intended provider policy.
7. Inspect the model graph for unlinked, duplicate, or unintended providers.
8. Run a baseline calculation and export a frozen result.
9. Perform contribution and inventory checks; reconcile with engineering balances.
10. Run scenarios/uncertainty only after baseline QA.

## IPC pattern

First run `scripts/snapshot_environment.py` and select one API generation. Do not mix model classes or lifecycle calls across generations.

Current openLCA IPC documentation uses the separately generated `olca_ipc` client and `olca_schema` model package:

```python
import olca_ipc as ipc
import olca_schema as o

client = ipc.Client(8080)
setup = o.CalculationSetup(
    target=o.Ref(
        ref_type=o.RefType.ProductSystem,
        id="<product-system-uuid>",
    ),
    impact_method=o.Ref(id="<impact-method-uuid>"),
    amount=1.0,
)

result = client.calculate(setup)
try:
    result.wait_until_ready()
    for indicator in result.get_impact_categories():
        value = result.get_total_impact_value_of(indicator)
        print(indicator.name, value.amount)
finally:
    result.dispose()
```

Older official `olca-ipc.py` pages use `import olca`, `CalculationSetup.product_system`, and `client.dispose(result)`. That is a legacy client generation, not a drop-in synonym for the current example. Detect installed distributions, pin them, and follow the documentation matching that exact client/server pair.

## Validation

Compare:

- openLCA reference amount vs study reference flow;
- process allocation and product-system allocation setting;
- product system links vs model ledger;
- total inventory vs direct engineering inventory;
- method/category UUIDs and versions;
- exported result vs GUI result;
- scenario parameter set vs parameter register.

## Deliverable

Provide reproducible scripts/configuration, UUID-based model manifest, database snapshot/version, calculation setup, result export, and QA evidence. Do not redistribute licensed database contents.

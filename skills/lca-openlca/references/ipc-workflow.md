# openLCA IPC workflow

## Connection and protocol selection

Start the IPC server for the intended active database from openLCA developer tools. A desktop IPC server commonly listens on localhost port 8080, but the port is configurable. Do not expose an unauthenticated endpoint beyond a trusted local boundary.

openLCA's service back end can be reached through multiple protocols:

- JSON-RPC over HTTP through `olca_ipc.Client`;
- REST through `olca_ipc.rest.RestClient` when a compatible web service is deployed;
- gRPC through a compatible generated client;
- direct Java kernel APIs for JVM integrations.

All protocols use the openLCA schema as their exchange model, but client methods and lifecycle behavior differ. Record server, protocol, client package, schema package, and database versions.

Run `scripts/snapshot_environment.py` before writing automation. Treat a reachable TCP port as a transport check only; it does not prove database identity, API compatibility, or permission to mutate data.

## API-generation gate

Two generations of official Python examples remain discoverable:

| Generation | Typical imports | Calculation/result pattern |
|---|---|---|
| Current schema-separated client | `import olca_ipc as ipc`; `import olca_schema as o` | `CalculationSetup(target=...)`; `Result.wait_until_ready()`; result query methods; `Result.dispose()` |
| Legacy monolithic client | `import olca` | `CalculationSetup.product_system`; synchronous `SimpleResult`; client query methods; `Client.dispose(result)` |

Never combine classes or methods from these rows. Inspect installed package metadata and the documentation bundled or published for that exact version. If the study depends on a legacy client, isolate it in a pinned environment and label it explicitly.

## Discovery

Use `get_descriptors` to enumerate model references and then persist validated UUIDs in configuration. Names can be duplicated, translated, or changed. Current-client discovery follows this shape:

```python
import olca_ipc as ipc
import olca_schema as o

client = ipc.Client(8080)
for ref in client.get_descriptors(o.ProductSystem):
    print(ref.id, ref.name, ref.category)
```

Discovery is not selection. Confirm category path, location, reference product, quantitative reference, and database provenance before saving an identifier.

## Read before write

Start with connection, version, discovery, and read-only result retrieval. Before writes:

- use a database copy or controlled branch/export;
- generate stable UUIDs;
- validate references, flow properties, units, directions, providers, and quantitative references;
- upsert deliberately rather than treating name equality as identity;
- commit in small, reviewable batches;
- record every created, updated, and deleted UUID;
- refresh the UI navigation and inspect the model graph after mutation.

## Current calculation lifecycle

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
    impacts = {
        category.id: {
            "name": category.name,
            "amount": result.get_total_impact_value_of(category).amount,
        }
        for category in result.get_impact_categories()
    }
    inventory = result.get_total_flows()
finally:
    result.dispose()
```

After calculation:

1. wait for readiness and handle failed/cancelled states;
2. retrieve impact-category identities, units/metadata, total impacts, inventory flows, technosphere requirements, and contributions needed by the study;
3. export raw values before charting or rounding;
4. reconcile reference amount, functional unit, method, allocation, and parameters against the run manifest;
5. dispose the server-side result in `finally`.

Do not assume a successful request means a scientifically valid product system. Empty impacts can result from an absent method, flow-mapping problems, unlinked providers, or a boundary with no characterized elementary flows.

## Current Monte Carlo lifecycle

The current API starts with `client.simulate(setup)`, waits until ready, advances with `result.simulate_next()`, and disposes the final result. Keep the random seed or server behavior, iteration count, failed iterations, distributions, correlations, and extracted indicator UUIDs in the manifest.

```python
result = client.simulate(setup)
try:
    result.wait_until_ready()
    indicator = result.get_impact_categories()[0]
    samples = [result.get_total_impact_value_of(indicator).amount]
    for _ in range(99):
        result.simulate_next()
        result.wait_until_ready()
        samples.append(result.get_total_impact_value_of(indicator).amount)
finally:
    result.dispose()
```

Monte Carlo output is not meaningful until uncertainty coverage, parameter dependence, pedigree/distribution assumptions, and numerical convergence have been reviewed.

## REST and gRPC

Do not mechanically translate JSON-RPC code into REST URLs. Use the protocol-specific official client or service contract. Verify server version and a read-only endpoint before calculation. For remote services, require authentication, TLS, request limits, audit logging, and tenant/database isolation.

## Error handling and observability

- distinguish transport, protocol, server, calculation, and scientific-model errors;
- use bounded waits/timeouts where the client permits them;
- reject missing or ambiguous UUIDs before calculation;
- log request context, versions, IDs, parameter overrides, and result status without credentials or licensed payloads;
- use `try/finally` for result/simulator disposal;
- make write scripts idempotent or provide a rollback manifest;
- compare a small known product system against the GUI before trusting batch runs.

## Version and release policy

Pin the IPC and schema distributions together and record the openLCA application/server version. The official current examples may name a particular pre-release package version; do not turn that web-page value into an evergreen requirement. Revalidate when any client, schema, openLCA, Java runtime, database, or LCIA package changes.

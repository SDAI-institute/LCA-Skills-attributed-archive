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

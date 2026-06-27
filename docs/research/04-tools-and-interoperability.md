# Tools and interoperability research notes

## Tool-selection principle

Choose the tool for the study, not the study for the tool. Preserve method decisions outside the software so a model can be reviewed or reproduced elsewhere.

| Need | Strong default | Caution |
|---|---|---|
| Transparent GUI modeling, broad databases, EPD-style workflows | openLCA | GUI state and provider links still need manifests and audits |
| Python-native research, scenarios, custom matrices, large batches | Brightway 2.5 | Flexibility permits invalid data and destructive operations |
| US fuels, vehicles, energy/material pathways | R&D GREET or mandated GREET variant | Select the exact release/variant; R&D and regulatory models are not interchangeable |
| Proprietary enterprise/PCR workflow | SimaPro, Sphera/GaBi, One Click LCA, etc. | Encode concepts and export checks, not undocumented proprietary automation |
| Process design linked to LCA | process simulator + openLCA/Brightway/custom bridge | Simulation convergence is not LCA completeness |
| Economy-wide screening/truncation reduction | USEEIO/EXIOBASE/hybrid workflow | Sector averages are unsuitable for fine technology claims without refinement |

## openLCA

### Concepts to encode

Database, process, product/waste flow, elementary flow, flow property/unit, provider, product system, project, allocation, parameters/parameter sets, LCIA method, calculation setup, result, contribution tree, uncertainty, import/export.

### GUI workflow

1. Create/open a controlled database and record version.
2. Import data/method packages and review logs/conflicts.
3. Create foreground processes with correct quantitative reference.
4. Link providers explicitly; audit default providers and unlinked exchanges.
5. calculate/refresh allocation factors where used—openLCA documentation warns they are not automatically refreshed before product-system calculation.
6. Build/update product system and inspect graph.
7. select amount, allocation, parameter set, method, normalization/weighting, uncertainty.
8. Run calculation, contribution and inventory checks, then export immutable raw results.

### IPC workflow

openLCA exposes one service back end through JSON-RPC, REST, and gRPC variants, all based on the openLCA schema. Current Python examples separate the client (`olca_ipc`) from generated model classes (`olca_schema`), while older official pages still show a monolithic `olca` namespace. These generations have different setup fields, readiness behavior, result-query locations, and disposal calls; the skill must identify and pin one generation rather than splice snippets together.

Current-client lifecycle:

- run an environment snapshot and record openLCA/server, protocol, `olca-ipc`, `olca-schema`, database, and method-package versions;
- connect to the intended active database and prove identity with read-only discovery;
- get descriptors/UUIDs rather than relying on ambiguous names;
- construct an `olca_schema.CalculationSetup` with `target`, amount/unit, method, allocation, parameters, and optional settings as applicable;
- call `client.calculate`, wait until the returned `Result` is ready, and check state;
- extract raw impact, inventory, technosphere, contribution, and metadata through result methods;
- dispose the result in `finally` to release server-side resources;
- persist setup IDs, overrides, status, raw exports, and environment metadata.

Current Monte Carlo uses `client.simulate`, `Result.wait_until_ready`, repeated `Result.simulate_next`, and final `Result.dispose`. Legacy clients use different simulator and disposal methods. Never interpret Monte Carlo without checking uncertainty coverage, dependencies/correlations, failed iterations, and convergence.

### Interchange

openLCA JSON-LD/schema is the highest-fidelity openLCA exchange format, but source licenses still apply. ILCD, ecoSpold, SimaPro CSV, Excel, and other formats can lose IDs, provider links, parameters, uncertainty, compartments, or model semantics. Validate round trips.

## Brightway

### Version discipline

Brightway 2 (legacy) and Brightway 2.5 have materially different package semantics. Current official documentation identifies Brightway 2.5 as the stable current release and provides a project migration call. Activity Browser compatibility can differ by version. The skill must pin packages and record whether a project is legacy or migrated.

### Core concepts

Projects isolate databases, methods, and calculations. Inventory uses graph nodes/edges; calculations construct technosphere, biosphere, and characterization matrices. Current APIs prefer integer node IDs in important contexts such as `MultiLCA`.

### Reproducible pattern

1. Create/select a named project; never mutate an unknown default project.
2. Pin Python and package versions; snapshot environment.
3. import biosphere, LCIA methods, background database, and foreground through explicit import strategies.
4. inspect unlinked exchanges, duplicate nodes, reference products, signs, and units before writing.
5. validate database and method metadata.
6. create demand with IDs/nodes compatible with installed API.
7. retrieve data objects and run `LCA`/`MultiLCA` using current signatures.
8. save demand, method config, database hashes, package versions, and raw arrays/results.
9. use `use_distributions` and/or `use_arrays` for stochastic/scenario calculations only with documented sources and seeds.
10. never rely on an old notebook example without comparing it to current docs.

Brightway supports powerful datapackage, temporal, scenario, and graph workflows; that flexibility means the skill must enforce more checks, not fewer.

## GREET

### Model selection

DOE emphasizes that GREET variants serve different use cases. R&D GREET, regulatory/tax-credit versions, CA-GREET, ICAO-GREET, and other derivatives are not interchangeable. Record exact product, release, revision, database, pathway, and any program guidance.

As of the status date, Argonne listed R&D GREET 2025 Rev1 updates released in 2026. Do not infer that a study conducted under a regulatory program should use that R&D release.

### Workflow

1. define well-to-product/use boundary and functional basis (energy LHV/HHV, distance, mass, vehicle service);
2. duplicate a baseline pathway/case rather than editing the canonical model;
3. record every user value and upstream pathway/mix edit;
4. verify units, shares, energy efficiencies, co-products, land-use assumptions, counterfactuals, and transport;
5. run baseline and alternatives;
6. export detailed stage/process results, not only total GHG;
7. reconcile transferred GREET results with any external process LCA boundary;
8. archive model/release/case manifest.

The public plugin API documentation includes older examples; treat API use as version-sensitive and validate against the installed release and vendor support before production automation.

## Interoperability contract

Every import/export mapping should preserve or explicitly account for:

- stable IDs and names;
- reference products and amounts;
- flow property, unit, and conversion;
- product versus waste semantics;
- elementary-flow compartment/subcompartment;
- geography, technology, time, tags/classification;
- providers and markets;
- signs and avoided-product semantics;
- allocation and system model;
- parameters/formulas/sets;
- uncertainty distributions and correlations;
- LCIA method/category/factor identity;
- data license and confidentiality.

Run a round-trip benchmark: calculate a small reference system before export, import elsewhere, and compare inventory and impact categories with tolerances. A matching total can still hide compensating mapping errors, so compare contributions and elementary flows too.

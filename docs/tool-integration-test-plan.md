# Tool integration and scientific qualification plan

The repository's unit tests prove file contracts, deterministic utilities, adapter error handling, packaging, and the synthetic matrix regression fixture. They do **not** prove that an installed openLCA, Brightway, or GREET environment is scientifically correct for a real study. This plan separates four evidence levels so a successful connection is never mistaken for a validated LCA.

## Evidence levels

| Level | Question answered | Minimum evidence |
|---|---|---|
| Structural | Is the integration packaged and configured correctly? | Static validation, reference resolution, manifests, hashes |
| Runtime | Can a representative command execute in this environment? | Recorded command, versions, input IDs, output, exit status |
| Host | Can the target agent host actually invoke the adapter? | Host import/invocation transcript and tool receipt |
| Scientific | Does the integration reproduce known model semantics and results? | Known-case reconciliation, seeded failures, practitioner review |

Only the **scientific** level supports a claim that an integration is qualified for study work. Tool qualification is specific to the tested software, API/client, database, system model, LCIA package, operating environment, and fixture version.

## Common test controls

For every integration:

1. Work in a disposable project, database, model copy, or isolated container.
2. Record software and package versions, operating system, database/model release, system model, LCIA implementation, plugin version, and test date.
3. Use stable identifiers, explicit reference amounts, units, directions, provider links, parameter values, and tolerances.
4. Preserve the input fixture, run manifest, raw exports, normalized results, logs, and SHA-256 hashes.
5. Test both an expected-success case and deliberately seeded failure cases.
6. Compare inventory totals, characterization results, contributions, and metadata—not only a single score.
7. Verify cleanup behavior, project/database restoration, and result disposal.
8. Repeat after any material tool, client, schema, database, method, operating-system, or plugin change.
9. Keep licensed data out of repository fixtures, logs, screenshots, and CI artifacts.
10. Obtain independent practitioner review before marking a scientific qualification closed.

## Canonical synthetic fixture

Use `tests/integration/fixtures/synthetic-matrix/` and `scripts/run_reference_lca.py` where the target tool can represent the fixture. The fixture has analytically known scaling, inventory, and indicator values. It tests matrix semantics and integration behavior only; it is **not** a scientifically endorsed LCIA method or sector model.

Acceptance requires:

- exact activity scaling within the stated numerical tolerance;
- correct inventory amounts and signs;
- correct characterization result;
- contribution reconciliation to the total;
- correct reference-product and demand semantics;
- failure detection for broken links, wrong directions, missing production exchanges, and stale allocation/processed data.

## openLCA qualification

### Preconditions

- Record the openLCA desktop/server version and IPC/API mode.
- Record `olca_ipc` and `olca_schema` package versions.
- Use a disposable database with no proprietary background data unless the evidence is stored privately.
- Confirm the IPC endpoint and database are the intended target before calculation.

### Test sequence

1. Run:

   ```bash
   lca-skills openlca snapshot --check-endpoint
   ```

   or the equivalent bundled snapshot script.
2. Implement the canonical synthetic foreground without background providers.
3. Record product-system ID, quantitative reference, amount, calculation type, impact-method ID, parameter overrides, and allocation settings.
4. Calculate through the GUI and through `lca-skills openlca calculate`.
5. Reconcile:
   - activity scaling;
   - elementary-flow inventory;
   - indicator score;
   - contribution totals;
   - units and flow directions.
6. Verify asynchronous readiness behavior where applicable and confirm the result object is disposed after extraction.
7. Export to JSON-LD, import into a clean database, rerun, and document any identifier or semantic changes.
8. Repeat through the actual agent host's MCP/tool route and preserve the host transcript.

### Seeded failures

- wrong quantitative reference or reference amount;
- unlinked technosphere provider;
- elementary-flow input/output reversal;
- stale allocation factors after product changes;
- wrong impact-method descriptor;
- result read before calculation readiness;
- omitted result disposal;
- accidental connection to a different database/endpoint;
- parameter override not applied or not persisted.

### Release evidence

Create `openlca-qualification-<version>.json` containing the environment snapshot, fixture hashes, identifiers, expected/observed values, tolerances, seeded-failure outcomes, cleanup confirmation, reviewer, and limitations.

## Brightway qualification

### Preconditions

- Record the exact package set, not a single umbrella version: `bw2data`, `bw2calc`, `bw2io`, `bw_processing`, `stats_arrays`, and relevant extensions.
- Use a named disposable project and stable activity/database codes.
- Record the active project before and after every adapter run.

### Test sequence

1. Run:

   ```bash
   lca-skills brightway snapshot
   ```
2. Build the canonical synthetic system in a clean project.
3. Calculate with a direct `bw2calc.LCA` implementation and with `lca-skills brightway calculate`.
4. Inspect and reconcile:
   - demand and activity identity;
   - technosphere and biosphere matrices;
   - supply array/activity scaling;
   - inventory matrix and elementary-flow inventory;
   - characterization matrix and score;
   - contribution totals.
5. Exercise the installed `MultiLCA`/datapackage/scenario path when that workflow is supported by the pinned package set.
6. Delete processed data, rebuild, and repeat.
7. Recreate the project from recorded fixture code and manifests in a clean environment.
8. Invoke the same calculation through the target agent host and compare the receipt.

### Seeded failures

- wrong active project;
- activity code collision or mutable name lookup;
- missing or duplicate production exchange;
- stale processed data;
- unmatched biosphere flow or characterization factor;
- exchange sign reversal;
- incorrect functional-unit amount;
- method tuple mismatch;
- project not restored after adapter failure;
- correlated parameters sampled independently in uncertainty workflows.

### Release evidence

Create `brightway-qualification-<package-set>.json` containing project/database/activity/method identifiers, package versions, fixture hashes, matrix/result comparisons, rebuild evidence, failure outcomes, reviewer, and limitations.

## GREET qualification

GREET is a family of products and program-specific models, not one interchangeable generic API. The repository therefore provides provenance and result-ingestion controls rather than claiming universal model automation.

### Preconditions

- Identify the exact product: R&D GREET or a named regulatory/program model.
- Record release, revision, platform, DOI/source page, pathway/case, boundary, functional basis, LHV/HHV basis, co-product treatment, and GWP basis.
- Use a lawful local model copy and do not place it in the repository.

### Test sequence

1. Generate a manifest:

   ```bash
   lca-skills greet manifest \
     --study-id <id> \
     --product "R&D GREET" \
     --release <release> \
     --platform <platform> \
     --pathway <case> \
     --boundary <boundary> \
     --functional-basis <basis> \
     --output greet-run-manifest.json
   ```
2. Reproduce a vendor-published or otherwise authoritative public baseline for the exact product/release.
3. Change one transparent input with an independently predictable direction and approximate magnitude.
4. Export results to the normalized CSV contract and run:

   ```bash
   lca-skills greet import-results results.csv
   ```
5. Confirm that release, pathway, scenario, boundary, indicator, value, and unit reconcile to the manifest.
6. Reopen/rebuild the case and reproduce the result.
7. Where external LCA stages are linked, document a replacement map and prove no stage is omitted or double counted.

### Seeded failures

- R&D GREET substituted for a regulatory model;
- wrong release/revision;
- WTP, WTW, well-to-gate, or vehicle-cycle boundary mismatch;
- LHV/HHV mismatch;
- undisclosed electricity or fuel-mix edit;
- co-product treatment mismatch;
- GWP version/time-horizon mismatch;
- double-counted upstream or vehicle/material stage;
- result export missing pathway/release provenance.

### Release evidence

Create `greet-qualification-<product>-<release>.json` with the exact model identity, baseline source, input delta, expected/observed response, normalized export, reconciliation, reviewer, and limitations.

## Cross-tool reconciliation

When the same foreground is implemented in more than one tool:

1. Freeze a common functional unit, reference flows, boundaries, allocation rules, foreground parameters, elementary-flow mapping, and LCIA factors.
2. Export normalized inventory and impact tables.
3. Run `lca-skills study compare` with tolerances appropriate to numeric representation.
4. Investigate every difference before increasing tolerance.
5. Classify differences as data, system-model, allocation, mapping, characterization, numerical, or software-implementation effects.
6. Preserve a reconciliation table and do not report “same result” when only aggregate climate scores happen to match.

## Host qualification tests

For each supported host, perform the minimum manual test in `docs/platforms/host-qualification.md`. At least one test must invoke a deterministic workspace tool through the host. For Claude Code, also verify agent dispatch, hook behavior, and MCP discovery. For ChatGPT and Claude.ai, record the upload scan/import result and automatic activation behavior. For Codex, record the installed skill invocation syntax shown by the actual version.

## Release criterion

An integration may be marked **scientifically qualified** only when:

- the named version set passes baseline and seeded-failure tests;
- replay/rebuild works from recorded artifacts;
- version/API mismatches fail loudly rather than silently adapting;
- environment and calculation provenance are complete;
- no licensed or confidential data are leaked;
- the target host path has been tested when host execution is claimed;
- a qualified independent practitioner has reviewed and signed the evidence;
- limitations and expiry/retest triggers are recorded.

Anything less must retain a narrower status such as `STRUCTURALLY_QUALIFIED`, `RUNTIME_TESTED`, `HOST_TESTED`, or `NOT_TESTED`.

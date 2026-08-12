# Tool integration benchmark

The `synthetic-matrix` fixture is a deliberately tiny, license-free system for checking implementation mechanics across this repository, openLCA, Brightway, or another matrix LCA engine.

It is **not** a scientific dataset or LCIA method. The characterization factors are intentionally synthetic and must never appear in an environmental claim.

## Analytic result

A one-kilogram widget consumes two kilowatt-hours from the electricity process. The demand scales the processes to:

- electricity: 2 reference units;
- widget: 1 reference unit.

The resulting inventory is 1.1 kg carbon dioxide and 0.002 kg sulfur dioxide. The synthetic indicator is 1.12 verification units.

## Local check

```bash
python scripts/run_reference_lca.py
```

## Cross-tool acceptance protocol

1. Implement the exact foreground in an isolated openLCA database or Brightway project.
2. Use only the supplied exchanges and synthetic factors; do not link a background database.
3. Freeze target, units, signs, providers, and method identity.
4. Export process scaling, inventory totals, indicator total, and process contributions.
5. Compare each value to `expected-results.csv` at a declared tolerance.
6. Confirm a deliberate sign, provider, or unit mutation causes the integration test to fail.
7. Dispose/close calculations and archive the run manifest.

A matching total alone is insufficient: compare scaling and inventory too, because compensating mapping errors can preserve one aggregate score.

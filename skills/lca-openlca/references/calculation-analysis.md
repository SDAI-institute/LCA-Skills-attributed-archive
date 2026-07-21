# openLCA calculation and analysis

## Baseline

Record calculation type, product system UUID, reference amount/unit, allocation method, parameter set, impact method UUID/version, and database.

## Analysis

Use total impacts, process/flow contributions, upstream tree, inventory results, Sankey/model graph, and project comparison as appropriate. Keep contribution cutoffs visible and inspect absolute contributions when credits exist.

## Parameters and scenarios

Parameter scopes can override one another. Record effective values at calculation time. Verify formula syntax and unit assumptions. Export parameter sets or a manifest.

## Uncertainty

Ensure uncertainty distributions exist and are meaningful. Run sufficient simulations, preserve seed/settings where possible, inspect failures/outliers, and state that structural/method uncertainty is not captured automatically.

## Result disposal

IPC calculation objects can consume server resources. Dispose results and simulator objects after export/analysis.

## Reconciliation

Cross-check GUI and IPC results, reference amount, allocation, parameter set, and method. A discrepancy is usually configuration or version mismatch until proven otherwise.

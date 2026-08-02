# Calculation contract

A calculation request identifies:

- study, model, functional unit/reference amount;
- scenario and parameter override set;
- tool/client/server and environment;
- database, system model, model object IDs;
- LCIA package/method/category IDs and units;
- allocation/recycling/cutoff implementation;
- random seed/iterations/distributions/correlations for stochastic runs;
- requested inventories, impacts, contributions, diagnostics, and exports;
- timeout, disposal, and error-handling behavior;
- expected benchmark or reconciliation target.

The receipt records the same fields plus timestamps, statuses, failed iterations, output hashes, and validation results.

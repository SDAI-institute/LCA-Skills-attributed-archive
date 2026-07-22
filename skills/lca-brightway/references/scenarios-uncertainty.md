# Brightway scenarios, uncertainty, and advanced ecosystem

## Stochastic calculations

Current `LCA`/`MultiLCA` can use distributions and arrays/datapackages. Record seed, iterations, distribution source, correlation strategy, and package versions. Advance calculations using the supported iterator/API for the installed release.

## Scenarios

Use parameterized foreground rebuilds, `bw_processing` arrays/datapackages, or documented scenario packages. Avoid in-place mutations that cannot be reproduced.

## Prospective backgrounds

Tools such as `premise`/`wurst` can transform background databases using IAM scenarios. Record source database release/system model, IAM, pathway, year, region mapping, package version, transformation logs, and unresolved mappings.

## Temporal/spatial

`bw_temporalis`, `bw_timex`, and regional packages require time/location metadata and compatible methods. Validate timing, graph traversal, characterization, and replacement cycles against a small benchmark.

## Reproducibility

Serialize scenario definitions and data-generation code, not only output matrices. Keep proprietary input databases out of the repository and document rebuild prerequisites.

# LCA interoperability

## Common formats

- openLCA schema JSON-LD: broad openLCA feature coverage and lossless exchange within its model.
- ILCD/ILCD+EPD: standardized data structures with program-specific extensions.
- ecoSpold 1/2: widely used inventory formats with different feature sets.
- SimaPro CSV, spreadsheets, custom CSV/JSON: convenient but potentially lossy.
- Brightway projects/databases/datapackages: Python-native structures, not a universal interchange format.

## Round-trip protocol

1. Freeze source model and export manifest.
2. Export a small test model with parameters, uncertainty, allocation, locations, units, and providers.
3. Import into target and compare entity counts, quantitative references, exchanges, flow compartments, allocation, parameters, uncertainty, provider links, and result.
4. Record unsupported features and transformations.
5. Only then migrate the full model.

## Mapping rules

- Map by stable IDs where available, then exact product/flow/compartment/unit/location metadata.
- Never map elementary flows by name alone when compartment/subcompartment differs.
- Preserve product vs waste and input vs output semantics.
- Reconcile unit groups and reference properties.
- Quantify unmapped flows and default providers.
- Avoid importing duplicated biosphere or LCIA methods under slightly different names.

## Result-level interoperability

When only LCIA results are available, keep them as external results with their method, boundary, functional unit, and uncertainty. Do not pretend they are an elementary-flow inventory.

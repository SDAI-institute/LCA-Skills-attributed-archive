# openLCA import/export and interoperability

## openLCA schema JSON-LD

Preferred for feature-rich openLCA exchange; record schema/export version. Validate package contents, references, units, parameters, allocation, and providers after import.

## ILCD / ecoSpold / SimaPro CSV / Excel

These formats encode different concepts and may lose parameters, uncertainty, allocation, locations, provider links, or metadata. Perform a round-trip test on a small model and compare calculation results.

## Database imports

- import into a new database when possible;
- inspect duplicate flows/methods/categories;
- run mapping/linking deliberately;
- review unlinked exchanges and default providers;
- record import log and source license.

## Exports

Do not export or distribute restricted database contents beyond license. A result table may also be restricted depending on agreement; check terms.

## Validation

Compare entity counts, UUIDs, reference products, units, exchange totals, product-system links, parameters, allocation factors, elementary-flow mapping, and a known LCIA result before/after transfer.

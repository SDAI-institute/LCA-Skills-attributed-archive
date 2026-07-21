# openLCA GUI workflow

## Database setup

- Record openLCA version, database name/release/system model, and import source.
- Back up before updates/imports.
- Check units, flow properties, locations, currencies, elementary flows, and LCIA methods for duplicates.

## Foreground process

1. Create product/waste/elementary flows with correct flow property and unit group.
2. Create process metadata and quantitative reference.
3. Add input/output exchanges, providers, uncertainty, and data-quality notes.
4. Add parameters/formulas; document units because formulas are unitless.
5. Define and save allocation factors where multifunctional.

## Product system

- Generate from reference process with explicit provider policy.
- Inspect model graph and unlinked exchanges.
- Review default providers and market/production dataset choice.
- Set calculation properties, allocation method, parameters/parameter set, and amount.

## Project/scenarios

Use projects for comparative variants with common setup. Check that variants share functional basis, method, and database. Parameter sets should be named, documented, and exported.

## QA

Run inventory and LCIA, inspect contribution tree/table, compare direct foreground inventory with engineering calculations, and export a frozen result plus model metadata.

# openLCA GUI workflow

## Database setup

- Record openLCA version, database name/release/system model, and import source.
- Back up before updates/imports.
- Check units, flow properties, locations, currencies, elementary flows, and LCIA methods for duplicates.

## Foreground process

1. Create product/waste/elementary flows with correct flow property and unit group.
2. Create process metadata and quantitative reference.
3. Add input/output exchanges, providers, uncertainty, and data-quality notes.

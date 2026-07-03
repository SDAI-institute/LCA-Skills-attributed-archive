# Security and data handling

## Do not commit

- API keys, database credentials, license files, or software activation material;
- client-confidential process data, prices, supplier data, or unpublished results;
- ecoinvent or other restricted database exports;
- full copies of copyrighted standards, PCRs, or commercial method files;
- executable macros or workbooks of unknown provenance.

## Tool execution

- Treat spreadsheets, JSON-LD packages, databases, and model scripts as untrusted inputs.
- Inspect paths and output targets before running destructive imports or writes.
- Use a copy of production LCA databases for automated mutation.
- Pin and record package versions for reproducible calculations.
- Do not expose an openLCA IPC server beyond localhost without authentication, network controls, and an explicit risk review.
- Dispose openLCA calculation and simulation objects after use to avoid resource leaks.

## Reporting vulnerabilities

Open an issue without including sensitive data. For a private deployment, follow the repository owner’s internal reporting process.

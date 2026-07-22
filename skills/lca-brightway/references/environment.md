# Brightway environment and project management

## Environment manifest

Record OS, Python, package manager, environment lock, `brightway25` and component versions (`bw2data`, `bw2calc`, `bw2io`, `bw_processing`, etc.), solver, and optional packages.

## Project discipline

- call `bd.projects.set_current("name")` explicitly;
- use separate projects for destructive experiments or incompatible database releases;
- export/backup or provide deterministic rebuild scripts;
- do not assume numeric node IDs remain stable across independently rebuilt projects;
- persist database/code or other stable identifiers plus validation metadata.

## Imports

Use documented importers and strategies. Save importer statistics and unresolved exchanges. Run linking/migration steps explicitly and inspect before writing.

## Version migration

Brightway 2 and 2.5-era projects/APIs differ. Use official migration functions and changelogs. Do not blindly run legacy tutorials against a modern environment.

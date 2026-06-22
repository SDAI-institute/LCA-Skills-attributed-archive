Use Brightway2 when the study benefits from scripted inventory assembly, matrix calculations, parameter sweeps, or custom post-processing.

Expectations:
- Keep the Brightway project and database names explicit.
- Separate foreground data creation from background imports.
- Record functional unit dictionaries and method tuples exactly.
- Use Brightway outputs for reproducible scenario analysis and sensitivity tests.

Useful package patterns:
- `import brightway2 as bw`
- `bw.projects.set_current("project-name")`
- `bw.Database("db-name")`
- `bw.LCA(functional_unit, method_tuple)`
- `lca.lci()`, `lca.lcia()`

Agent guidance:
- In inventory work, specify which foreground processes belong in Brightway and what background database is assumed.
- In LCIA work, note the exact method tuple and whether regionalization or characterization coverage is a concern.
- In interpretation work, use Brightway for contribution trees, scenario comparisons, and reproducible sensitivity analysis.

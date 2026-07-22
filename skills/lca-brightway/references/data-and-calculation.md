# Brightway data and calculation workflow

## Foreground database

Use deterministic activity codes and complete metadata: name, reference product, unit, location, production amount, classifications, source, comment. Add one correct production exchange and explicit technosphere/biosphere exchanges.

## Entity lookup

Prefer exact database/code or validated `get_node` constraints. After search, assert name, product, location, unit, and database before calculation.

## Calculation

Typical order:

1. set project;
2. validate demand activity and amount;
3. validate method tuple;
4. create `bc.LCA` or current `MultiLCA` configuration;
5. call `lci()` then `lcia()`;
6. inspect score and matrices/contributions;
7. serialize result and manifest.

Current `bw2calc` can use `bw_processing` datapackages and supports static, stochastic, and scenario-oriented inputs. Follow installed API docs for `prepare_lca_inputs`, `MultiLCA`, arrays, distributions, and matrix remapping.

## Reprocessing

After changing database exchanges or methods, ensure relevant data are processed/available to the calculation. Verify by inspecting matrix entries or rebuilding a clean project.

# Brightway data and calculation workflow

## Foreground database

Use deterministic activity codes and complete metadata: name, reference product, unit, location, production amount, classifications, source, comment. Add one correct production exchange and explicit technosphere/biosphere exchanges.

## Entity lookup

Prefer exact database/code or validated `get_node` constraints. After search, assert name, product, location, unit, and database before calculation.

## Calculation


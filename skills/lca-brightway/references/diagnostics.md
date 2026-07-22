# Brightway diagnostics

## Structural checks

- production exchange exists and has expected amount/sign;
- technosphere inputs link to intended products/providers;
- biosphere exchanges map to the intended flow/compartment;
- no unresolved importer exchanges;
- database dependencies are present;
- demand is in the technosphere product space;
- method contains factors for expected flows.

## Matrix checks

Inspect technosphere, biosphere, characterization, inventory, characterized inventory, supply array, and dictionaries/IDs. Compare selected coefficients to source data.

## Contribution checks

Use analyzer/graph traversal or matrix decomposition. Rank by absolute contribution and trace negative terms. Beware cycles and cutoffs.

## Minimal reproduction

Create a tiny project/database with one production exchange, one input, and one biosphere flow to isolate import, matrix, or method problems.

## Assertions

Automated workflows should assert project, database version, activity metadata, method existence, finite score, expected sign/range, and no unlinked exchanges before accepting output.

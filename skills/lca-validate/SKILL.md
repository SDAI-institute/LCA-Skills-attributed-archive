---
name: lca-validate
description: "Run deterministic and expert validation gates on an LCA workspace, inventory, calculation, report, or release package and issue a reproducible readiness decision. Use before calculation, interpretation, review, disclosure, or handoff."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---

# LCA Validation

Validation verifies evidence against a declared gate; it does not manufacture compliance.

Read `references/validation-matrix.md`, `references/release-gates.md`, and `references/exception-waivers.md`.

## Validation layers

1. **Repository/workspace:** required artifacts, IDs, schemas, paths, versions, hashes, confidentiality handling.
2. **Scope:** intended use, function, equivalence, boundary, modeling approach, rules, review route.
3. **Inventory:** units, signs, formulas, providers, reference products, completeness, balances, credits, data quality.
4. **LCIA:** method identity, indicator units, flow mapping, regionalization, factor basis, exclusions.
5. **Results:** total/contribution reconciliation, scenarios, sensitivity, uncertainty, magnitude and benchmark checks.
6. **Report/claims:** model-report agreement, limitations, review status, authorized language, supporting evidence.
7. **Release:** closed findings, reproducible package, immutable manifest, lawful redistribution.

## Readiness states

- `FAIL`: critical evidence or model integrity failure.
- `BLOCKED`: required input, license, reviewer, or program rule unavailable.
- `CONDITIONAL`: material exception is documented with owner, deadline, impact, and approval route.
- `PASS_INTERNAL`: suitable for the stated internal use.
- `REVIEW_READY`: ready for independent review, not externally verified.
- `RELEASE_READY`: applicable internal gates passed and required external review evidence is attached.

Run bundled validators where available, then perform expert checks that cannot be reduced to syntax. Never convert a warning into a pass without a documented waiver and influence assessment.

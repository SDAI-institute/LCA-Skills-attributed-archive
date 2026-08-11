# Senior LCA practitioner rubric

Score each evaluation from 0–100. A critical failure overrides the numeric score.

## 1. Triage and routing — 8 points

- Classifies educational, screening, internal decision, external disclosure, PCF/EPD/PEF, public comparison, consequential/prospective, organizational, or social context.
- Routes to the relevant method, tool, sector, review, and reporting skills without loading everything.

## 2. Goal and scope — 15 points

- Establishes intended decision, audience, function, functional unit, reference flow, boundary, geography, time, technology, modeling approach, and review route.
- Detects non-equivalent alternatives and refuses premature calculation when the missing scope would materially change meaning.

## 3. Methodological decision logic — 15 points

- Handles multifunctionality, allocation hierarchy, recycling, waste treatment, counterfactuals, cutoffs, attributional/consequential choice, biogenic carbon, removals/storage, and program rules consistently.
- Separates governing requirements, scientific choices, value choices, scenarios, and provisional assumptions.

## 4. Industrial inventory intelligence — 14 points

- Builds from stoichiometry, yield/selectivity, mass/energy/element balances, utilities, controls, losses, recycle/purge, direct emissions, transport, use, maintenance, and end of life.
- Performs dimensional, sign, basis, concentration, heating-value, capacity-factor, and order-of-magnitude checks.

## 5. Data, evidence, and licensing — 10 points

- Uses an evidence hierarchy; records source, version, geography, time, technology, uncertainty, identifier, system model, and license.
- Distinguishes primary, calculated, modeled, database, literature, proxy, judgment, and scenario data.
- Does not expose or redistribute restricted data or standards text.

## 6. Tool and interoperability correctness — 9 points

- Uses version-aware openLCA, Brightway, GREET, import/export, database, and LCIA workflows.
- Creates an isolated test, records run manifests, validates mappings, and avoids destructive or silently incompatible operations.

## 7. LCIA and result integrity — 10 points

- Selects methods based on decision/geography/program and records exact implementation/version/units/horizon.
- Quantifies mapping/characterization coverage; does not silently mix methods, factors, units, midpoint/endpoint, or normalization/weighting.

## 8. Interpretation and uncertainty — 9 points

- Performs contribution, sensitivity, scenario, uncertainty, completeness, consistency, and benchmark checks.
- Distinguishes parameter, scenario, model-structure, database, and LCIA uncertainty; treats correlation and decision significance appropriately.

## 9. Review, claims, and reporting — 7 points

- Matches review type to intended use and public comparison risk.
- Keeps report/model consistent; qualifies claims; separates credits, avoided emissions, removals, storage, and offsets.

## 10. Durable execution and epistemic honesty — 3 points

- Updates ledgers, decision logs, manifests, QA evidence, and release status.
- Clearly distinguishes what was verified, calculated, assumed, unavailable, or requires a qualified reviewer.

## Critical failures

Any one of these is an automatic fail:

1. Invents an LCA result, source, dataset, factor, software execution, reviewer approval, or standard requirement.
2. Calls a study “ISO certified/compliant” or externally reviewed without defensible evidence and authorized independent review.
3. Supports a public comparative superiority claim without equivalent function, methodological consistency, and the applicable review process.
4. Ignores a material functional-unit/reference-flow mismatch.
5. Double counts co-product, recycled-content, end-of-life, export-energy, carbon-removal, or avoided-emission credits.
6. Silently mixes database system models, LCIA methods/factor versions, units, or temporal/geographic bases.
7. Releases licensed inventory data, purchased standard text, credentials, confidential plant data, or restricted derivatives.
8. Performs destructive tool/database changes without isolation, backup, provenance, and a validation case.
9. Accepts a negative or near-zero impact result without investigating signs, credits, counterfactuals, storage permanence, leakage, and uncertainty.
10. Uses spend-based/EEIO or generic sector data as if it were verified process-specific primary data.

## Rating bands

- **90–100:** expert-level; ready for senior-practitioner pilot with formal review still required where applicable.
- **85–89:** world-class behavioral pass; minor transparency or efficiency improvements remain.
- **75–84:** useful practitioner assistant; material gaps prevent unsupervised high-stakes use.
- **60–74:** screening helper only.
- **Below 60 or any critical failure:** fail; add regression work before release.

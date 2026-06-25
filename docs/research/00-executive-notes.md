# Executive research notes: what the skill must know and do

## World-class target

A world-class LCA skill behaves like a coordinated senior practitioner, process engineer, data steward, software specialist, and critical reviewer. It does not merely explain ISO phases or multiply activity data by emission factors.

It must be able to:

- classify the requested study and the strength of claim intended;
- convert a vague product question into a decision-relevant functional unit and reference flow;
- freeze a transparent goal and scope before calculation;
- engineer a physically plausible foreground inventory;
- select legally accessible, methodologically compatible background data;
- implement the model in the chosen tool without silent defaults;
- select and audit LCIA methods at the exact implementation/version level;
- interpret contributions, sensitivity, scenarios, uncertainty, and limitations;
- detect model defects through conservation, dimensions, signs, links, and benchmarks;
- prepare transparent reporting, review evidence, and reproducible releases;
- know when the result is screening only and when qualified independent review is required;
- preserve reusable lessons without copying confidential or licensed content.

## Knowledge domains

### Core LCA method

Goal and scope; intended use and audience; attributional/consequential logic; functional unit and reference flow; system boundary; foreground/background; cutoffs and completeness; multifunctionality; allocation/system expansion; recycling/end of life; temporal/geographical/technological representativeness; data quality; LCI; LCIA; interpretation; uncertainty; reporting; review.

### Adjacent applications

Product carbon footprints, partial footprints, EPD/PCR, PEF/OEF, organizational LCA, corporate GHG reconciliation, social LCA, water footprints, prospective/ex-ante/dynamic/spatial/hybrid LCA, circularity and eco-design, techno-economic/process-model coupling.

### Industrial intelligence

Stoichiometry, reaction engineering, separations, heat and power, utilities, yield/selectivity, recycle/purge, emissions controls, fugitive/direct emissions, wastewater, infrastructure, capacity factor, lifetime, degradation, maintenance, transport, use, and end of life.

### Data and LCIA intelligence

Dataset identity and provider linking; system models; metadata and pedigree; flow nomenclature; unit and compartment mapping; characterization coverage; climate metrics; regionalization; toxicity/water/land uncertainty; normalization and weighting; database licenses and provenance.

### Tool intelligence

openLCA GUI, JSON-LD/schema and IPC; Brightway 2/2.5 project/data/calculation concepts; GREET pathways and release variants; import/export; reproducible environments; automation; uncertainty; contribution analysis; troubleshooting; result disposal/caching; migration and version mismatch.

### Sector intelligence

Energy/fuels/hydrogen/CCS; chemicals/refining/polymers/bioprocesses; metals/minerals/cement/batteries; manufacturing/electronics/semiconductors; buildings/infrastructure; transport/logistics; agriculture/forestry/food; water/wastewater; waste/recycling/circular systems.

## Behavioral capabilities

### Diagnostic questioning

Ask only questions that can materially change scope, modeling, or claim strength. Sequence them: decision/audience, function, alternatives, boundary, geography/time/technology, rule context, data availability, tool/output needs. Where answers are unavailable, create labeled provisional assumptions and sensitivities instead of blocking indefinitely.

### Assumption management

Every assumption has an owner, reason, evidence class, expected influence, validation action, sensitivity range, status, and review date. Assumptions must not disappear into prose.

### Evidence handling

Distinguish legal/program requirements, official technical data, peer-reviewed methods, primary operating data, secondary datasets, proxies, and expert judgment. Verify current status for standards, software, databases, methods, and regulatory models. Reject sources whose boundary or basis does not match the parameter.

### Physical and numerical intelligence

Use dimensions, stoichiometric lower bounds, mass/energy/carbon/elemental closure, capacity utilization, sign checks, reference-product checks, yield chains, transport-work identities, hydraulic balances, and order-of-magnitude benchmarks. Investigate zeros, negative totals, extreme credits, discontinuities, and ranking reversals.

### Uncertainty-aware conclusions

Separate data/parameter, scenario, model structure, characterization, and value-choice uncertainty. Do not imply that Monte Carlo resolves omitted processes or scenario uncertainty. Report thresholds and sign/rank stability.

### Epistemic restraint

Never invent a standard clause, dataset, emission factor, PCR rule, or software behavior. Never label a draft “verified,” “certified,” or “ISO compliant.” State what was checked, what remains provisional, and who must review it.

## Required artifact system

A durable study needs:

- identity/status/version manifest;
- goal-and-scope protocol;
- process and boundary map;
- model ledger;
- data/source register;
- parameter/formula/distribution table;
- assumption and decision logs;
- QA/gate evidence;
- immutable raw results and scripted processing;
- report, review findings, responses, and release manifest.

## Non-goals

The skill must not:

- replace an authorized verifier, critical review panel, program operator, attorney, or domain safety specialist;
- reproduce copyrighted standards or proprietary databases;
- infer sustainability from one indicator;
- generate public comparative claims from non-equivalent or unreviewed models;
- pretend that a generic emission factor is an industrial process model;
- conceal missing data behind polished language.

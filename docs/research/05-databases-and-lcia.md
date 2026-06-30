# Databases and LCIA research notes

## Database-selection logic

No database is “best” independent of goal, geography, technology, time, system model, transparency, and license. The skill needs a provider-selection matrix and must preserve dataset-level metadata.

## Major data families

### ecoinvent

As of the status date, ecoinvent 3.12 is the latest release identified by the provider. It offers four system models: allocation cut-off by classification, allocation cut-off EN15804, APOS, and long-term consequential substitution. These models change recycling/waste treatment, allocation, linking, and marginal-supply logic; they are not cosmetic file variants.

Required metadata: version, system model, dataset UUID/name, reference product, geography, time, technology, unit, provider/market, transformations, modifications, and license.

Do not redistribute datasets or derived reconstruction-enabling exports beyond license permissions.

### US data

- Federal LCA Commons / USLCI and agency repositories for transparent US process data;
- EPA USEEIO for economy-wide screening/hybrid work;
- EPA eGRID for US electricity generation/emission context, subject to the correct accounting use;
- Argonne GREET for fuels, vehicles, energy, chemicals/material pathways;
- official emissions, agriculture, energy, transport, and industrial statistics for primary parameterization.

USEEIO sector averages help identify upstream truncation or spend hotspots but should not be presented as plant-specific process performance.

### European and international data

- Environmental Footprint/LCDN data and reference packages for PEF/OEF and related contexts;
- Agribalyse for agriculture/food where applicable;
- EXIOBASE and other MRIO data for hybrid/economy-wide analysis;
- national LCA databases and sector associations with transparent methods;
- commercial libraries such as Sphera/GaBi, Ecoinvent, and program-specific data under their licenses.

### Data source register fields

Provider, database, version, release date, system model, dataset ID, process/product, reference unit, geography, technology, temporal coverage, representativeness, allocation, boundary, uncertainty, review, modifications, license, retrieval date, and model locations used.

## Data-fit assessment

Evaluate:

1. **technology:** route, scale, feedstock, efficiency, pollution control, quality;
2. **geography:** production and market region, trade, electricity, regulation, climate;
3. **time:** data year, validity, future scenario;
4. **function:** product specification and reference flow;
5. **method:** allocation/recycling/system model and boundaries;
6. **completeness:** included exchanges and infrastructure;
7. **uncertainty/review:** quality metadata and pedigree;
8. **license:** authorized use and sharing.

A precise but mismatched dataset may be worse than a transparent proxy with sensitivity.

## LCIA method selection

### Climate

Record exact IPCC source/assessment, indicator, time horizon, climate-carbon feedback treatment where relevant, fossil/biogenic/LULUC mapping, and software implementation. Do not mix AR4/AR5/AR6 factors silently. Regulatory/PCR rules can mandate a specific implementation.

### TRACI

US EPA lists TRACI 2.2 as the latest site-generic factor file. Use for US-oriented contexts where its categories and assumptions fit. Verify the method package implemented in the selected software; a label such as “TRACI” can refer to an older factor set.

### ReCiPe

Widely used midpoint/end-point family. Record 2016 version/perspective, midpoint versus endpoint, geography/implementation, normalization/weighting, and software package source. Do not mix perspectives or report endpoint damage as directly observed harm.

### Environmental Footprint

Use the mandated EF reference package/method and data rules for PEF/OEF/EN15804 contexts. EF 3.1 artifacts and transition guidance were current sources during 2026, but the framework was evolving toward a new recommendation/EF 4.0. Verify per program.

### Toxicity and ecotoxicity

USEtox-based or other factors require exact substance, compartment, speciation, indoor/outdoor context where relevant, mapping coverage, and factor version. Results are comparative potential impacts, not site risk assessments. Large uncertainties and missing factors must be explicit.

### Water

AWARE and other methods model scarcity/deprivation; water-quality impacts may be represented through separate categories. Map basin/region and consumption correctly. Do not characterize withdrawal as consumption without method logic.

### Land/biodiversity

Methods vary in land occupation/transformation, regionalization, species/economic endpoints, and restoration/time assumptions. Report method limitations and avoid overstating precision.

### Other categories

Acidification, eutrophication, photochemical ozone, ozone depletion, particulate matter, resource use/scarcity, ionizing radiation, and human health categories must use one coherent method implementation or a documented mixed-method protocol.

## Flow-mapping audit

Before trusting LCIA:

- count elementary flows by mass/energy and by expected contribution;
- identify unmapped flows and unmatched compartments;
- inspect synonyms, CAS IDs, chemical forms, ions/metals, fossil/biogenic distinctions;
- verify unit conversions and molecular/speciation transformations;
- inspect characterization-factor sign and magnitude;
- compare factor counts and hashes/version to the official implementation;
- test a small known flow.

A high percentage of mapped flow names does not guarantee high impact coverage; prioritize material flows.

## Normalization and weighting

Normalization contextualizes category magnitude against a reference inventory; weighting applies value judgments and can generate a single score. Record reference population/year/region, weighting source and panel/value basis, uncertainty, and whether a program requires it. Always retain unweighted indicator results.

## Uncertainty data

Use distributions only when their meaning and parameters are known. Distinguish lognormal/normal/triangular/uniform/discrete/scenario; maintain correlations; do not sample shares independently when they must sum to one; and do not interpret database pedigree distributions as complete model uncertainty.

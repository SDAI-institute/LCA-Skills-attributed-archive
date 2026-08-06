# Authoritative source register

**Status checked:** 2026-08-07  
**Purpose:** Maintain the primary-source backbone for LCA Skills. This register records sources to consult; it does not reproduce licensed standards, proprietary databases, or restricted program rules.

## How to use this register

1. Start with the governing law, program, contract, PCR/PEFCR/OEFSR, or disclosure rule.
2. Verify the edition, amendments, corrigenda, validity dates, and geographic scope on the official publisher page at the time of use.
3. Record the exact version actually applied in the study protocol, model ledger, and release manifest.
4. Prefer primary sources. Use secondary literature to interpret or benchmark, never to silently replace a governing requirement.
5. Do not paste purchased ISO/EN/PCR text into prompts, skills, repositories, or model training corpora unless the license explicitly permits it.

## Agent-skill architecture and reference implementation

| Source | Role in this repository | Access / update note |
|---|---|---|
| [Agent Skills specification](https://agentskills.io/specification) | Canonical `SKILL.md` directory, frontmatter, progressive-disclosure, reference, asset, and script conventions | Recheck before releases; the format is evolving |
| [Agent Skills repository](https://github.com/agentskills/agentskills) | Reference examples, open-format governance, and the `skills-ref` demonstration validator | The upstream reference library is explicitly not production software; use this repository’s strict validator plus real host tests for release qualification |
| [Every Compound Engineering plugin](https://github.com/EveryInc/compound-engineering-plugin) | Architectural inspiration: small routed skills, specialist prompts, durable artifacts, review and compounding loop | Inspiration only; no copied proprietary content |
| [Google Antigravity plugin/skills documentation](https://antigravity.google/docs/cli/plugins) | Generic root `plugin.json` schema and plugin layout | Host-specific; recheck schema version before releases |
| [Claude Code plugin documentation](https://code.claude.com/docs/en/plugins) | Claude Code plugin layout, namespaced plugin skills, agents, hooks, MCP, and local `--plugin-dir` testing | Recheck before each host release |
| [Claude Code plugin reference](https://code.claude.com/docs/en/plugins-reference) | Agent, hook, manifest, MCP, and other component schemas | Host-specific fields must not leak into portable skills |
| [Claude Code skills documentation](https://code.claude.com/docs/en/slash-commands) | Slash invocation, arguments, `argument-hint`, and explicit-only controls | Applied only in generated Claude Code overlays |
| [Claude custom skills guidance](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) | Claude.ai skill folder/ZIP structure and testing | Requires actual account upload qualification |
| [Claude skill usage guidance](https://support.claude.com/en/articles/12512180-use-skills-in-claude) | Claude.ai enablement, automatic activation, account/workspace controls, and security review | Availability and settings are host/account dependent |
| [OpenAI Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) | ChatGPT skill upload, scan, automatic use, sharing, permissions, and Agent Skills portability | Requires actual account/surface qualification |
| [OpenAI Plugins in ChatGPT and Codex](https://help.openai.com/en/articles/20001256-plugins-in-codexOpenAI) | Skill/app/plugin packaging, workspace installation, app permissions, and invocation | Plugin/app behavior is separate from a skill-only ZIP |
| [Model Context Protocol specification](https://modelcontextprotocol.io/specification/2025-11-25) | MCP protocol version and lifecycle/tool/resource contracts | Bundled server implements a deliberately limited stdio subset |

## Core LCA standards

| Standard | Operational role | Status note at 2026-08-07 | Official source |
|---|---|---|---|
| ISO 14040:2006 + Amd 1:2020 | Principles and framework for the four LCA phases, reporting, limitations, and review | ISO page indicates the 2006 edition remains current after 2022 confirmation | [ISO](https://www.iso.org/standard/37456.html) |
| ISO 14044:2006 + Amd 1:2017 + Amd 2:2020 | Requirements and guidance for goal/scope, LCI, LCIA, interpretation, reporting, and critical review | ISO page indicates the 2006 edition remains current after 2022 confirmation | [ISO](https://www.iso.org/standard/38498.html) |
| ISO/TR 14049:2012 | Illustrative goal/scope and inventory examples | Published technical report; examples are informative, not replacement requirements | [ISO](https://www.iso.org/standard/57110.html) |
| ISO/TR 14047:2012 | Illustrative LCIA examples | Published technical report; examples are informative, not replacement requirements | [ISO](https://www.iso.org/standard/57109.html) |
| ISO/TS 14048:2002 | LCA data documentation format | ISO page indicates confirmation in 2025; verify before formal exchange specifications | [ISO](https://www.iso.org/standard/29872.html) |
| ISO 14071:2024 | Critical-review process and reviewer competencies | Published October 2024; replaces ISO/TS 14071:2014 | [ISO](https://www.iso.org/standard/86264.html) |
| ISO/TS 14074:2022 | Normalization, weighting, interpretation, uncertainty, sensitivity, and reporting guidance | Published; ISO page may show review activity, so verify before formal use | [ISO](https://www.iso.org/standard/61117.html) |

## Specialized life-cycle and footprint standards

| Standard | Operational role | Status note at 2026-08-07 | Official source |
|---|---|---|---|
| ISO 14067:2018 | Product carbon footprint and partial carbon footprint | Current edition is marked for revision/work-item activity; check for replacement | [ISO](https://www.iso.org/standard/71206.html) |
| ISO 14046:2014 | Water-footprint assessment based on LCA | Under review; do not reduce a water footprint to withdrawal volume alone | [ISO](https://www.iso.org/standard/43263.html) |
| ISO 14072:2024 | Organizational life cycle assessment | Published October 2024; replaces ISO/TS 14072:2014 | [ISO](https://www.iso.org/standard/86265.html) |
| ISO 14075:2024 | Social life cycle assessment principles and framework | Published October 2024 | [ISO](https://www.iso.org/standard/61118.html) |
| ISO 14045:2012 | Product-system eco-efficiency assessment | Verify current status and study applicability | [ISO](https://www.iso.org/standard/43262.html) |
| ISO 14051:2011 | Material flow cost accounting framework | Useful for industrial resource-efficiency intersections; not a substitute for environmental LCA | [ISO](https://www.iso.org/standard/50986.html) |
| ISO 14083:2023 | GHG quantification/reporting for passenger and freight transport chains | Published March 2023 | [ISO](https://www.iso.org/standard/78864.html) |

## Environmental declarations, claims, and construction

| Standard / program source | Operational role | Status note at 2026-08-07 | Official source |
|---|---|---|---|
| ISO 14025:2026 | EPD program and declaration principles, requirements, and guidance | Published June 24, 2026; **ISO 14025:2006 is withdrawn** | [ISO current page](https://www.iso.org/standard/14025) |
| ISO 21930:2017 | Core rules for environmental declarations of construction products and services | Current edition confirmed in 2023; pair with governing regional/program rules | [ISO](https://www.iso.org/standard/61694.html) |
| ISO 14026:2017 | Communication of footprint information | Current edition confirmed in 2023 | [ISO](https://www.iso.org/standard/67401.html) |
| ISO 14020 family | General environmental statement and program principles | Verify current family members; ISO 14021 and related standards had 2026 editions/activity | [ISO environmental management](https://www.iso.org/sectors/management-services/environmental-management) |
| EN 15804 | European construction EPD core rules | Licensed standard; identify national adoption, amendment, program operator, and current PCR | [CEN](https://www.cencenelec.eu/) |
| International EPD System | PCR library, General Programme Instructions, verification/program rules | Program rules change; capture document version and validity | [Program operator](https://www.environdec.com/) |
| EC3 / EPD program registries | Search and comparison support | Registry records are not automatically functionally comparable | [Building Transparency](https://www.buildingtransparency.org/) |

## European Environmental Footprint and EU life-cycle resources

| Source | Operational role | Update note | Official source |
|---|---|---|---|
| Commission Recommendation (EU) 2021/2279 | General PEF/OEF methods | Apply with valid PEFCR/OEFSR and current reference packages | [European Commission](https://environment.ec.europa.eu/publications/recommendation-use-environmental-footprint-methods_en) |
| Environmental Footprint methods landing page | Current EF method, implementation, and policy context | Monitor for EF 4.0 transition | [European Commission Green Forum](https://green-forum.ec.europa.eu/green-business/environmental-footprint-methods_en) |
| 2026 transitional guidance for limited EF-compliant datasets | Dataset hierarchy/disclosure during transitional availability constraints | Published 2026-07-14; does not silently override a valid category/sector rule | [European Commission](https://green-forum.ec.europa.eu/news/transitional-guidance-limited-availability-ef-compliant-datasets-2026-07-14_en) |
| EPLCA Environmental Footprint data | EF-compliant datasets and reference packages | Record package and node versions | [JRC EPLCA](https://eplca.jrc.ec.europa.eu/EnvironmentalFootprint.html) |
| EF reference packages / developer page | Elementary-flow and LCIA packages, including EN 15804 variants | Package files were updated in 2026; hash the actual package | [JRC EPLCA](https://eplca.jrc.ec.europa.eu/LCDN/developer.html) |
| ILCD Handbook | Detailed European LCA methodological guidance and data-quality concepts | Some parts are older but remain important interpretive references | [JRC Publications Repository](https://eplca.jrc.ec.europa.eu/ilcd.html) |
| Life Cycle Data Network | ILCD-format datasets and nodes | Check node ownership, dataset version, and license | [LCDN](https://eplca.jrc.ec.europa.eu/LCDN/) |

## GHG accounting intersections

| Source | Operational role | Update note | Official source |
|---|---|---|---|
| GHG Protocol Product Life Cycle Accounting and Reporting Standard | Product-level GHG inventory and reporting | Existing standard remains relevant while joint ISO/GHG Protocol harmonization proceeds; do not pre-apply drafts | [GHG Protocol](https://ghgprotocol.org/product-standard) |
| GHG Protocol Scope 3 Standard | Corporate value-chain accounting | Organizational accounting context; avoid treating spend factors as process-specific LCA | [GHG Protocol](https://ghgprotocol.org/scope-3-calculation-guidance-2) |
| GHG Protocol Land Sector and Removals Standard v1.1 | Corporate land/removal accounting | Published in 2026 with effective date 2027-01-01; use only when governing framework requires it | [GHG Protocol](https://ghgprotocol.org/land-sector-and-removals-standard) |
| ISO/GHG Protocol harmonization announcements | Future standards awareness | Track final publications; drafts and announcements are not operative requirements | [GHG Protocol](https://ghgprotocol.org/) |
| IPCC Sixth Assessment Report | Climate science and metric provenance | Record assessment, metric, horizon, feedback treatment, and software implementation | [IPCC AR6](https://www.ipcc.ch/assessment-report/ar6/) |

## UNEP and international methodological guidance

| Source | Operational role | Official source |
|---|---|---|
| UNEP Life Cycle Initiative | Global guidance, capacity building, GLAM, databases, and sector work | [Life Cycle Initiative](https://www.lifecycleinitiative.org/) |
| Global Guidance for Life Cycle Impact Assessment Indicators and Methods (GLAM) | LCIA method/indicator evaluation and global consensus work | [JRC/UNEP GLAM](https://eplca.jrc.ec.europa.eu/glam.html) |
| Guidelines for Social Life Cycle Assessment of Products and Organizations | Social-LCA practice alongside ISO 14075 | [UNEP Life Cycle Initiative](https://www.lifecycleinitiative.org/library/guidelines-for-social-life-cycle-assessment-of-products-and-organisations-2020/) |

## LCA software and automation

### openLCA

| Source | Operational role | Update note |
|---|---|---|
| [openLCA 2 manual](https://greendelta.github.io/openLCA2-manual/) | GUI model construction, calculation, allocation, uncertainty, analysis, and import/export | Record application version and database versions |
| [openLCA IPC API documentation](https://greendelta.github.io/openLCA-ApiDoc/) | Current service concepts, JSON-RPC/REST/gRPC protocols, result lifecycle, and examples | API behavior is version-sensitive |
| [Current Python IPC calculation example](https://greendelta.github.io/openLCA-ApiDoc/results/calculate.html) | `olca_ipc` + `olca_schema`, asynchronous result readiness, and result interface | Use with matching package/server generation |
| [Current Python IPC from-scratch example](https://greendelta.github.io/openLCA-ApiDoc/examples/pyipc_from_scratch.html) | Current object construction, data writes, calculation, inventory retrieval, and disposal | Test mutations on a controlled database copy |
| [Current Monte Carlo interface](https://greendelta.github.io/openLCA-ApiDoc/results/simulate.html) | `Client.simulate`, `Result.simulate_next`, readiness, and disposal | Audit distribution coverage and dependence separately |
| [Legacy monolithic `olca` Python documentation](https://greendelta.github.io/olca-ipc.py/olca/ipc.html) | Older synchronous `SimpleResult` and client-side query/disposal patterns | Do not mix with current `olca_ipc`/`olca_schema` objects |
| [openLCA schema](https://greendelta.github.io/olca-schema/) | Lossless openLCA exchange model and generated types | Record schema version and validate cross-format losses |
| [GreenDelta GitHub](https://github.com/GreenDelta) | Source repositories, schemas, IPC clients, examples | Pin package and schema revisions |
| [openLCA Nexus](https://nexus.openlca.org/) | Databases and LCIA packages | Licenses vary; do not redistribute without authorization |

### Brightway ecosystem

| Source | Operational role | Update note |
|---|---|---|
| [Brightway documentation](https://docs.brightway.dev/en/latest/) | Current projects, databases, calculations, uncertainty, and ecosystem navigation | Stable docs identify the Brightway 2.5 generation; APIs differ from legacy tutorials |
| [Brightway GitHub organization](https://github.com/brightway-lca) | `bw2data`, `bw2calc`, `bw2io`, `bw_processing`, `stats_arrays`, and extensions | Pin package versions and environment lock |
| [Brightway Learn](https://learn.brightway.dev/) | Maintained examples and learning material | Verify notebook date/version before reuse |
| [Activity Browser](https://github.com/LCA-ActivityBrowser/activity-browser) | GUI over Brightway | Record Activity Browser and Brightway environment versions |
| [bw_temporalis](https://github.com/brightway-lca/bw_temporalis) | Dynamic/temporal inventory and characterization support | Experimental/advanced workflows require explicit tests |
| [bw2regional](https://github.com/brightway-lca/bw2regional) | Regionalized LCA extensions | Verify compatibility with current Brightway stack |
| [premise](https://premise.readthedocs.io/) | Prospective modification of ecoinvent using IAM scenarios | Requires licensed compatible ecoinvent input and version mapping |
| [wurst](https://github.com/polca/wurst) | Programmatic database transformation | Destructive transformations require isolated copies and validation |

### GREET

| Source | Operational role | Update note |
|---|---|---|
| [DOE GREET landing page](https://www.energy.gov/cmei/greet) | Federal overview and model access | Check policy/program-specific required version |
| [R&D GREET model page](https://www.energy.gov/cmei/rd-greet-life-cycle-assessment-model) | Current R&D GREET release and DOI | As of status date, R&D GREET 2025 Rev1 is listed with updates dated 2026-05-26 |
| [Argonne GREET versions](https://greet.anl.gov/greet/versions.html) | Release history and downloads | Freeze workbook/application/database release |
| [Argonne GREET documentation](https://greet.anl.gov/greet/documentation.html) | Pathway, vehicle, assumptions, and technical documentation | Capture document version |
| [Argonne GREET API](https://greet.anl.gov/greet/api.html) | Public automation examples/endpoints | Public examples may lag current desktop/web releases; test and record behavior |

## Inventory databases and background systems

| Source | Typical use | Critical controls | Official source |
|---|---|---|---|
| ecoinvent | Global process-based background data | Version, system model, unit-process vs system model, geography, market/transformation role, license | [ecoinvent database](https://ecoinvent.org/database/) |
| ecoinvent system-model documentation | Cut-off, APOS, consequential, and EN 15804 logic | Do not mix models without reconciliation | [ecoinvent support](https://support.ecoinvent.org/system-models) |
| ecoinvent v3.12 release and known issues | Latest release and provider errata at status date | Released 2025-11-05; verify newer releases and corrections before use; route through `skills/lca-data/references/current-errata.md` | [ecoinvent support](https://support.ecoinvent.org/ecoinvent-version-3.12) |
| Federal LCA Commons | US federal datasets, including USLCI-hosted resources | Node/provider, release, UUID, geography, age, flow mapping | [Federal LCA Commons](https://www.lcacommons.gov/) |
| USLCI | US process-based inventory data | Dataset age, provider, technology, elementary-flow mapping | [NREL USLCI](https://www.nrel.gov/lci/) |
| USEEIO | US environmentally extended input-output modeling | Model version, price year, purchaser/producer price, sector aggregation, margins | [US EPA technical content](https://www.epa.gov/land-research/us-environmentally-extended-input-output-useeio-technical-content) |
| EXIOBASE | Multi-regional EEIO/hybrid screening | Version, year, currency/price basis, aggregation, license | [EXIOBASE](https://www.exiobase.eu/) |
| AGRIBALYSE | Agriculture and food datasets for France/Europe | Version, agricultural modeling conventions, geography, license | [ADEME AGRIBALYSE](https://agribalyse.ademe.fr/) |
| EF database ecosystem | PEF/OEF-compliant background data | Compliance status, node/package version, transitional hierarchy | [European Commission](https://eplca.jrc.ec.europa.eu/EnvironmentalFootprint.html) |
| GLAD | Global LCA data access/network metadata | Dataset license and provider remain controlling | [UNEP GLAD](https://www.globallcadataaccess.org/) |

## US electricity, fuels, and emissions sources

| Source | Typical use | Critical controls | Official source |
|---|---|---|---|
| US EPA eGRID | US electricity generation/emissions factors and subregions | Data year, subregion, generation vs consumption framing, losses, imports | [US EPA eGRID](https://www.epa.gov/egrid) |
| EIA electricity data | Grid generation, sales, fuel, and state/regional statistics | Time resolution, data year, preliminary/final status | [US EIA electricity](https://www.eia.gov/electricity/) |
| US EPA AP-42 | Screening emission factors for stationary sources | Prefer measured/permit data; record factor quality and control assumptions | [US EPA AP-42](https://www.epa.gov/air-emissions-factors-and-quantification/ap-42-compilation-air-emissions-factors-stationary-sources) |
| US EPA GHGRP | Facility-reported GHG data | Reporting boundary/method differs from product LCA | [US EPA GHGRP](https://www.epa.gov/ghgreporting) |
| Argonne GREET | Fuel/vehicle/material pathways | Release, pathway, regional and technology assumptions | [Argonne GREET](https://greet.anl.gov/) |

## LCIA methods and characterization sources

| Method / source | Typical context | Version controls | Primary source |
|---|---|---|---|
| TRACI 2.2 | US-oriented midpoint LCIA | EPA lists TRACI 2.2 as the latest factor file at status date; record software implementation | [US EPA TRACI](https://www.epa.gov/chemical-research/tool-reduction-and-assessment-chemicals-and-other-environmental-impacts-traci) |
| Environmental Footprint method | EU PEF/OEF and related applications | EF package, method version, normalization/weighting set, program rules | [JRC EPLCA](https://eplca.jrc.ec.europa.eu/LCDN/developer.html) |
| ReCiPe 2016 | Broad midpoint/endpoint research and product studies | Perspective, midpoint/endpoint, version, implementation | [RIVM ReCiPe](https://www.rivm.nl/en/life-cycle-assessment-lca/recipe) |
| IPCC climate metrics | Climate-change characterization | Assessment report, horizon, metric, feedback treatment, biogenic/fossil conventions | [IPCC](https://www.ipcc.ch/) |
| USEtox | Human toxicity and freshwater ecotoxicity | Model/factor set, recommended/interim factors, flow mapping | [USEtox](https://usetox.org/) |
| AWARE | Water-scarcity footprint characterization | Geographic resolution, temporal fit, consumption inventory | [WULCA](https://wulca-waterlca.org/aware/) |
| IMPACT World+ | Spatially differentiated global LCIA | Version, regionalization, implementation | [IMPACT World+](https://www.impactworldplus.org/) |
| CML method family | Legacy/current midpoint studies and comparability with older literature | Exact baseline/version and software implementation | [Leiden University CML](https://www.universiteitleiden.nl/en/research/research-output/science/cml-ia-characterisation-factors) |

## Sector-specific primary-source families

The skill should select sources based on the technology, geography, time, and governing program. This list is a routing index, not permission to substitute sector averages for primary data.

| Sector | Primary-source families to check |
|---|---|
| Energy and fuels | DOE, EIA, EPA eGRID/GHGRP, Argonne GREET, IEA where licensed, grid operators, plant permits, meter data |
| Chemicals and bioprocesses | Process design basis, PFD/P&ID, material safety/specification data, supplier datasets, EPA AP-42/WebFIRE, permits, stoichiometric and thermodynamic sources |
| Metals and materials | USGS mineral statistics, industry association LCI with transparent rules, smelter/mill primary data, scrap specifications, EPD/PCR programs |
| Batteries | Battery chemistry/design data, cell/pack bill of materials, manufacturing yield/scrap, electricity/time/geography, cycle life and usable throughput, recycling process data |
| Manufacturing/electronics | BOM, routings, measured utilities, yield/scrap/rework, semiconductor/fugitive-gas records, logistics, product lifetime/use profiles |
| Buildings/construction | ISO 21930, EN 15804, applicable PCR/program rules, BIM/quantity takeoff, service life, scenarios for modules A–D, verified EPDs |
| Transport | ISO 14083 where applicable, GREET, vehicle/load/utilization records, route/distance, empty running, infrastructure rule, refrigerant leakage |
| Agriculture/food | Farm inputs/yields, IPCC inventory methods, nutrient balances, land-use-change data, enteric/manure models, allocation rules, food loss/cold chain/cooking |
| Water/wastewater | Utility energy/chemical/sludge records, source water, discharge permits, treatment performance, water-consumption and scarcity context |
| Waste/recycling | Composition and contamination, collection/sorting yields, substitution quality, recycled-content/end-of-life rule, landfill gas and incineration energy assumptions |

## Licensing and evidence cautions

- ISO, EN, PCR, database, and software documentation can be copyrighted even when an abstract or landing page is public.
- ecoinvent, commercial databases, EPD datasets, and program data can prohibit redistribution, bulk extraction, derivative hosting, or API exposure.
- A public EPD is a declaration under a specific PCR/program/version; it is not automatically a freely reusable unit-process dataset.
- Record access date, provider, license, version, UUID/identifier, system model, and allowed use for every external dataset.
- Store citations and derived parameters, not copied paywalled prose or restricted inventory tables.
- Before releasing a model, run the license/redistribution review in `skills/lca-data/references/licensing.md`.

## Scheduled maintenance

Review this register at least quarterly and immediately when any of the following occurs:

- a governing standard, amendment, PCR, PEFCR/OEFSR, or program instruction changes;
- an LCA tool or API releases a breaking major/minor version;
- a database, LCIA method, elementary-flow list, or reference package changes;
- a regulatory disclosure rule becomes effective;
- an eval exposes outdated advice.

Log source-status changes in `CHANGELOG.md`, update affected references, and add a regression eval when behavior should change.

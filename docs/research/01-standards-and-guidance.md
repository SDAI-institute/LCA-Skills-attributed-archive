# Standards and guidance research notes

Status date: 2026-08-07. Verify the current edition and applicable amendments at use time. The source register links to official pages; these notes paraphrase operational implications and do not reproduce standard text.

## Core framework

### ISO 14040:2006 with Amendment 1:2020

Defines LCA principles/framework: goal and scope, inventory, impact assessment, interpretation, reporting, critical review, limitations, phase relationships, and value choices. ISO lists the edition as current after its 2022 confirmation.

### ISO 14044:2006 with Amendments 1:2017 and 2:2020

Provides requirements and guidance for the four phases, reporting, and review. ISO lists the edition as current after its 2022 confirmation. The skill must operationalize, not claim certification against, these requirements.

## Review and interpretation

### ISO 14071:2024

Current dedicated standard for critical-review processes and reviewer competencies. The plugin should use it to plan review type, competence, independence, evidence, findings, and responses. A model self-check is not an independent critical review.

### ISO/TS 14074:2022

Adds guidance for normalization, weighting, single scores, completeness, sensitivity, consistency, uncertainty, limitations, conclusions, and reporting. Weighting remains a value choice; a single score cannot be treated as purely scientific fact.

### ISO/TR 14047 and ISO/TR 14049

Examples supporting LCIA and goal/scope/LCI application. Use as interpretive examples, not as alternative requirements.

## Specialized footprints and applications

### ISO 14067:2018

Current product carbon-footprint quantification standard, confirmed in 2024 but marked for revision with a work item underway. It concerns climate change only; offsetting and communication are outside its stated scope. The skill must check for a replacement before formal use.

### ISO 14046:2014

Water-footprint assessment based on LCA for products, processes, and organizations. Spatial/temporal context and water-quality impacts matter; water volume alone is not a water footprint result. ISO shows the standard under review, so status must be checked.

### ISO 14072:2024

Current organizational-LCA requirements/guidance supplementing ISO 14040/14044. It requires organization-specific boundary, inventory, impact, interpretation, and reporting considerations.

### ISO 14075:2024

Principles/framework and guidance for social LCA of products. Social hotspot screening, site performance, stakeholder evidence, and environmental LCIA must not be collapsed into one undifferentiated score.

## Data, declarations, and communication

The skill should know when the following become applicable and require the legally obtained current edition:

- ISO/TS 14048 — LCA data documentation format;
- ISO 14025:2026 — current EPD program/declaration requirements and guidance; ISO 14025:2006 is withdrawn;
- ISO 21930 — construction product/building EPD core rules;
- ISO 14026 — communication of footprint information;
- ISO 14020/14021/14024 — environmental statement/label families;
- ISO 14083 — transport-chain GHG quantification/reporting where applicable;
- EN 15804 and its program implementation for construction EPDs;
- current program-operator instructions and PCRs, which can be more specific than generic standards.

Never assume that an EPD, carbon footprint, environmental footprint, ecolabel, and comparative assertion are interchangeable outputs.

## European Environmental Footprint

Commission Recommendation (EU) 2021/2279 remains a central source for PEF/OEF methods while the framework continues to evolve. A valid PEFCR/OEFSR controls category-specific rules. The European Commission published transitional guidance on 2026-07-14 for limited EF-compliant dataset availability during 2025–2028; it provides a hierarchy and required disclosure, but does not override a valid category/sector rule. Existing PEFCRs/OEFSRs are described as remaining valid until EF 4.0 implementation.

The skill must therefore obtain:

- general EF method version;
- valid PEFCR/OEFSR and dates;
- EF reference package/LCIA version;
- data hierarchy and data-quality rules;
- circular footprint formula and electricity/carbon rules;
- verification and communication rules;
- any transition disclaimer.

## GHG Protocol intersections

The existing Product Life Cycle Accounting and Reporting Standard remains a product-level GHG source, but ISO and GHG Protocol are jointly developing a harmonized replacement/update. In 2026 the organizations also announced broader harmonization work. The skill must not pre-apply draft requirements.

The GHG Protocol Land Sector and Removals Standard v1.1 was available in 2026 with an effective date of 2027-01-01. It is primarily a corporate accounting standard; product LCA users should use it only where the selected accounting framework calls for it and should preserve differences from ISO-style product LCA.

## LCIA guidance

Use method-developer sources and current implementations. Relevant authoritative families include:

- US EPA TRACI, with EPA listing version 2.2 as the latest site-generic factor file;
- European Commission Environmental Footprint methods/reference packages;
- IPCC assessment reports for climate metrics;
- UNEP Life Cycle Initiative GLAM guidance;
- method-specific publications for ReCiPe, USEtox, AWARE, IMPACT World+, and other selected methods.

A method name in software is insufficient. Record family, version, implementation source, category, indicator level, time horizon, region, units, and any software modifications.

## Rule hierarchy

For a given study, apply rules in this order while documenting conflicts:

1. law/regulatory program or contractual requirement;
2. valid program instructions and PCR/PEFCR/OEFSR;
3. applicable current standards;
4. selected method/database documentation;
5. recognized guidance and peer-reviewed methods;
6. transparent project-specific choices.

A lower-level convention cannot silently override a governing rule. Conversely, a program rule may prescribe a choice that is not optimal for a separate internal decision study; create separate models or clearly separate interpretations.

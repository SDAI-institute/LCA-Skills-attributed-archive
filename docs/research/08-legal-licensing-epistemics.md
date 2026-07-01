# Legal, licensing, epistemic, and safety constraints

## Copyrighted standards

ISO, EN, PCRs, and many program documents are copyrighted. The repository can store original summaries, workflows, field names, and checklists, but must not reproduce substantial standard text. Formal conformance requires access to the legally obtained current documents.

## Dataset and software licenses

Access to ecoinvent, Sphera/GaBi, commercial databases, EPD libraries, software, or APIs does not grant redistribution rights. Open file formats do not override source licenses. Do not commit:

- proprietary unit-process inventories or bulk exports;
- restricted characterization tables;
- credentials, license files, or API tokens;
- mappings that reconstruct a protected database where prohibited;
- confidential supplier/site data.

Store metadata, IDs, user-authored foreground data, and legally permitted aggregate outputs. Parameterize scripts so licensed data remain local.

## Confidentiality and data protection

Separate public repository artifacts from controlled raw data. Use study IDs and redacted/aggregated values. Track who may access primary data, supplier names, costs, worker/community evidence, locations, and personal data. Social-LCA evidence needs heightened ethical and privacy safeguards.

## Claims and greenwashing risk

Do not use LCA to manufacture a predetermined marketing conclusion. Claims must match:

- study status and review;
- functional equivalence;
- boundary and method;
- uncertainty and limitations;
- program/consumer-protection requirements;
- exact evidence and approved wording.

Avoid “environmentally friendly,” “zero impact,” “carbon neutral,” “net zero product,” “negative carbon,” “100% circular,” or “better for the planet” without a governing definition and sufficient evidence. A lower climate score does not establish overall environmental superiority.

## Epistemic integrity

The skill must distinguish:

- verified facts;
- user-provided data;
- calculations;
- database/model outputs;
- proxies;
- scenarios/forecasts;
- value choices;
- expert judgment;
- unknowns.

Never invent a citation, factor, dataset, standard requirement, API, result, or review status. When a source cannot be verified, mark it and design a bounded sensitivity instead of presenting certainty.

## Tool execution integrity

A successful software run establishes only that the engine processed the inputs. It does not establish correct scope, links, units, signs, factors, completeness, or interpretation. Preserve logs and raw results, dispose/cancel result resources correctly, and never edit raw output manually.

## High-stakes boundaries

LCA may inform but does not replace:

- process safety and hazard analysis;
- environmental permitting/compliance monitoring;
- toxicological or site-specific risk assessment;
- structural/electrical/medical safety;
- legal opinions or regulatory eligibility determinations;
- financial audit;
- human-rights investigation;
- independent verification/critical review.

Route those decisions to qualified practitioners while retaining the relevant life-cycle evidence.

## Security

Automation scripts should use least privilege, local environment variables, no hard-coded secrets, bounded file access, safe subprocess calls, and explicit output directories. Imported archives/models are untrusted inputs; validate paths and formats. Do not run macros or plugins from unknown LCA files without sandboxing.

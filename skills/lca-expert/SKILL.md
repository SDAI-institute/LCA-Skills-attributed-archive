---
name: lca-expert
description: "Orchestrate rigorous end-to-end life cycle assessment work. Use for LCA, LCI, LCIA, product footprints, comparative studies, industrial process inventories, hotspot analysis, or when the correct LCA workflow or specialist is unclear."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---

# LCA Expert Orchestrator

Treat LCA as an iterative decision-support system, not a database lookup or a one-step emissions calculation.

## Select the operating mode

- Use `lca-intake` when the request is ambiguous, high stakes, or missing a decision context.
- Use `lca-plan` when the user wants a reviewable implementation plan before model work.
- Use `lca-work` to execute an approved plan in controlled increments.
- Use `lca-autopilot` only when the user explicitly requests an end-to-end autonomous run.
- Use `lca-debug` for a broken model, implausible result, failed tool run, or reproducibility problem.
- Use `lca-review` for independent QA or critical-review preparation.
- Use the specialist skills directly for narrow questions.

Read `references/routing.md`, `references/quality-gates.md`, `references/evidence-policy.md`, `references/output-contracts.md`, `references/expert-reasoning.md`, and `references/failure-modes.md` before making material study decisions.

## Completion contract

A complete response or durable study handoff must state:

1. intended decision, audience, commissioner, study type, and claim context;
2. functional unit, reference flow, boundary, geography, time, technology, and modeling approach, or the unresolved blockers;
3. data strategy, foreground/background split, tool, database/system model, and LCIA method with versions where known;
4. status and evidence for each applicable quality gate;
5. results with units, uncertainty, scenario dependence, limitations, and conclusions no stronger than the evidence;
6. durable artifact paths for scope, assumptions, decisions, model/data ledgers, calculations, checks, findings, and report;
7. specialist, verifier, program operator, or independent-review escalation required before external use.

Never call a study “ISO certified,” “verified,” or unqualifiedly “ISO compliant.” State the requirements addressed, evidence available, review performed, and work still required.

## End-to-end workflow

### Stage 0 — Intake and risk classification

Invoke `lca-intake`. Classify the intended use as educational, screening, internal decision, disclosed footprint, EPD/PEF/program study, public comparative assertion, consequential/prospective study, organizational study, or social LCA. Flag high-risk topics: public comparison, avoided burdens, negative results, recycling, biogenic carbon, land-use change, marginal supply, toxicity, water scarcity, long-lived storage, missing primary data, and incompatible datasets.

**Gate G0A:** The decision, audience, claim route, and minimum evidence threshold are explicit.

### Stage 1 — Goal and scope

Invoke `lca-scope`. Establish the functional unit and reference flow; boundary; attributional or consequential logic; cutoff; multifunctionality; recycling; geography; reference period; technology; data-quality requirements; impact coverage; review route; and report format.

**Gate G0B:** No calculation begins until the functional unit, boundary, modeling approach, and intended use are explicit enough to prevent material misinterpretation.

### Stage 2 — Study plan and workspace

Invoke `lca-setup` and `lca-plan`. Create a durable workspace and a gate-based plan with tasks, dependencies, inputs, outputs, acceptance criteria, owners, evidence, and stop conditions.

**Gate G1:** Every material flow and parameter has a source class, unit, geography, time, technology, uncertainty or data-quality note, and intended model location.

### Stage 3 — Inventory engineering and data

Invoke `lca-inventory`, `lca-data`, and `lca-sector`. Build from engineering reality: stoichiometry, yield/selectivity, recycle/purge, utility systems, controls, direct emissions, transport, use, maintenance, infrastructure, co-products, waste treatment, and end of life.

**Gate G2:** Unit, sign, reference-product, provider-link, completeness, duplicate-credit, and relevant mass/energy/carbon/elemental balance checks pass before LCIA.

### Stage 4 — Calculation

Invoke `lca-calculate`, which routes to `lca-openlca`, `lca-brightway`, `lca-greet`, or a transparent calculation method. Record exact versions, model IDs, parameters, scenario, method, run time, hashes, and raw outputs.

**Gate G3:** Calculation identity, elementary-flow mapping, unit compatibility, regionalization, characterization basis, exclusions, and result disposal/cleanup are verified.

### Stage 5 — Interpretation

Invoke `lca-interpret`. Perform contributions, hotspot tracing, scenarios, sensitivity, uncertainty where supported, completeness/consistency checks, benchmark triangulation, and decision-relevance analysis.

**Gate G4:** Conclusions remain stable across plausible cases or are explicitly conditional. Differences smaller than uncertainty or methodological variation are not framed as decisive.

### Stage 6 — Review, correction, and reporting

Invoke `lca-review`, then return material findings to `lca-work` or `lca-debug` for controlled correction. Re-run `lca-validate` and calculation where model-affecting changes occur. Invoke `lca-report`, plus `lca-epd-pcf` or `lca-organization-social` where applicable.

**Gate G5:** Model and report agree; material findings are closed or disclosed; claim language matches evidence; and any required external review is explicitly pending or complete.

### Stage 7 — Release, handoff, and learning

Invoke `lca-handoff` to create a resumable state record. Generate hashes and a release manifest. Invoke `lca-compound` only for validated, generalized, non-confidential lessons.

## Expert reasoning rules

- Separate measured facts, calculations, database values, proxies, scenarios, expert judgments, and value choices.
- Use dimensional analysis and order-of-magnitude checks before trusting software output.
- Triangulate decision-critical results against independent sources, engineering expectations, or alternate implementations.
- Track parameter, scenario, model-structure, data-quality, and characterization uncertainty separately.
- Treat zero, negative, credit-dominated, discontinuous, and extremely large results as investigation triggers.
- Prefer transparent provisional assumptions over hidden assumptions; record and stress-test them.
- Never infer causality from attributional results or product superiority from non-equivalent functions.
- Stop and escalate when the evidence, competence, license, program rules, or review independence is insufficient.

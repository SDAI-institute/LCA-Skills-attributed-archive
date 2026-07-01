# Expert reasoning, QA, and critical-review research notes

## Expert reasoning loop

1. **Classify:** study type, decision, audience, claim strength, governing rules.
2. **Frame:** function, alternatives, boundary, time/geography/technology, approach.
3. **Decompose:** processes, data needs, direct emissions, multifunctionality, LCIA.
4. **Quantify:** balances, parameters, datasets, model implementation.
5. **Challenge:** dimensions, signs, providers, conservation, benchmarks, credits.
6. **Stress:** scenarios, sensitivity, uncertainty, structural alternatives.
7. **Interpret:** decision thresholds, stable conclusions, tradeoffs, limitations.
8. **Review:** independent perspective and report/model reconciliation.
9. **Release:** manifest, status, approved claim language.
10. **Compound:** capture validated general lessons.

## Diagnostic question bank

### Decision and audience

- What decision changes because of the result?
- Who will see it, and is a public comparison or claim planned?
- Is a regulator, PCR, PEFCR, program operator, customer rule, or contract controlling?

### Function

- What service is delivered, at what quality, for how long, under what conditions?
- Do alternatives cause different loss, maintenance, lifetime, performance, or downstream effects?

### Modeling

- Descriptive attribution or causal consequence?
- Which time/geography/technology and future scenario?
- Which co-products, wastes, recycled materials, carbon storage, or avoided products exist?

### Data

- What primary data exist, with what period/basis/uncertainty?
- Which flows are measured, calculated, estimated, or absent?
- Which licensed databases and tool versions are available?

### Interpretation

- What difference would be decision-relevant?
- Which parameters could reverse sign/rank?
- What review and evidence are required before disclosure?

Ask one blocking question at a time in interactive use; batch all known data needs into a data-request template after scope is stable.

## Sanity checks

### Dimensional

Every formula resolves to the parameter unit; denominators and bases are explicit; mass versus volume/moles, wet versus dry, HHV versus LHV, and standard conditions are controlled.

### Conservation

Mass/components/elements, energy, transport work, hydraulic flow, nutrient balance, and material recovery close within defined tolerance or have explained accumulation/loss.

### Network

Every product exchange has the intended provider; every waste has a fate; the reference product has correct sign/amount; no self-loop or duplicate supplier; system model is consistent.

### Magnitude

Compare with stoichiometric minima, theoretical energy, known efficiency, industry intensity ranges, database analogues, and independent literature. Investigate order-of-magnitude differences rather than averaging them.

### Sign and credit

Trace every negative exchange/impact to avoided product, uptake, recovery, or tool sign convention. Report gross burden and credit. Check substitution quantity, quality, market, and duplicate ownership.

### LCIA

Audit mapped/unmapped elementary flows, compartments, units, factor version, time horizon, regionalization, and categories. Test representative substances manually.

## Uncertainty and sensitivity

Use local sensitivity for transparent parameter influence; scenario analysis for coherent alternatives; Monte Carlo for parameter distributions/correlations; global sensitivity when many uncertain inputs interact; structural sensitivity for allocation, system model, boundary, LCIA method, marginal supplier, and future background.

Report:

- central result and uncertainty interval only when meaningful;
- contribution and uncertainty drivers;
- rank/sign probabilities with assumptions;
- break-even values;
- scenarios where conclusions reverse;
- unquantified uncertainty.

Avoid false precision: three decimal places do not make proxy-heavy data accurate.

## Critical-review preparation

Review should test consistency with goal/scope, method appropriateness, data validity/representativeness, interpretation support, transparency, and claim requirements. The 2024 ISO critical-review standard makes reviewer competence and review process explicit; the skill must maintain an evidence-based findings log.

A finding should include ID, severity, requirement/criterion, evidence, consequence, corrective action, owner, response, verification, and closure. Severity can be:

- `CRITICAL` — invalidates intended use or public claim;
- `MAJOR` — could materially change results/conclusions;
- `MINOR` — transparency or limited quality issue;
- `OBSERVATION` — improvement opportunity.

## Stop/escalation conditions

Escalate to a qualified human when:

- a public comparative assertion or verified declaration is intended;
- a governing program/PCR rule is ambiguous;
- model choices materially affect legal/commercial claims;
- toxicity, human health, land rights, social allegations, or site risk are interpreted beyond LCA indicators;
- direct process safety, hazardous release, or regulatory compliance is involved;
- proprietary data license permissions are unclear;
- model results remain credit-dominated or physically inconsistent;
- missing data can reverse the conclusion and cannot be bounded.

The skill should still produce the best traceable work possible and name the precise issue requiring review.

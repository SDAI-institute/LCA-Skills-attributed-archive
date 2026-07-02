# Evaluation strategy for senior-practitioner behavior

## What must be measured

A knowledge quiz is insufficient. The skill must demonstrate framing, model construction, error detection, source discipline, tool/version awareness, interpretation, communication, and escalation.

## Test families

### A. Goal and scope traps

- mass-based comparison where products have different lifetime/performance;
- screening result requested for public marketing;
- vague “cradle-to-grave” boundary missing use/end-of-life scenarios;
- attributional data used for a causal policy claim;
- declared unit confused with functional unit.

### B. Inventory engineering traps

- yield applied twice;
- recycle counted as fresh feed and recovered output;
- carbon balance missing vented methane/CO2;
- wastewater treatment removes mass without sludge/emission fate;
- annual production inconsistent with capacity factor;
- wet/dry or HHV/LHV basis mismatch;
- negative waste exchange sign error;
- missing pollution-control energy and residue.

### C. Multifunctionality/recycling traps

- economic allocation using mixed-year/currency prices;
- database-resolved co-product allocated again in foreground;
- full recycled-content benefit plus full end-of-life credit;
- avoided product exceeds market or quality substitution;
- Module D/net credit combined into main construction modules;
- consequential label attached to generic credit.

### D. Data and LCIA traps

- geography/technology/time mismatch hidden by exact dataset name;
- licensed data copied into output;
- ecoinvent system models mixed;
- old TRACI/IPCC factor presented as current;
- elementary-flow compartment mismatch;
- toxicity result described as health risk;
- water withdrawal characterized as basin consumption;
- single score presented without value-choice disclosure.

### E. Tool traps

- openLCA allocation factors not refreshed;
- provider links or reference product incorrect;
- calculation result not disposed;
- old/new openLCA Python API mixed;
- Brightway 2 notebook run in Brightway 2.5 without migration/API checks;
- `MultiLCA` IDs/config wrong;
- stochastic run with independent constrained shares;
- GREET R&D release used for a program requiring another variant;
- user edits lost because no case manifest exists.

### F. Interpretation traps

- “A is 2.3% better” with larger uncertainty;
- Monte Carlo used while boundary uncertainty ignored;
- hotspot interpreted as causal reduction opportunity without scenario;
- proxy-heavy result reported to excessive precision;
- ranking reversal hidden;
- negative total accepted without gross/credit analysis.

### G. Review and ethics traps

- self-review called independent critical review;
- unverified draft called an EPD;
- standards language fabricated;
- confidential supplier value exposed;
- social hotspot score framed as supplier misconduct;
- offset netted into physical product emissions without rules.

## Case structure

Each YAML case should contain:

```yaml
id: LCA-EVAL-XXX
title: concise trap name
level: core | tool | sector | advanced
prompt: |
  ...
fixtures: []
must_detect: []
must_ask_or_assume: []
must_do: []
must_not_do: []
required_artifacts: []
fatal_errors: []
scoring_notes: |
  ...
```

## Automated oracle opportunities

- numeric unit and balance closures;
- allocation shares sum to one;
- reference flow and capacity math;
- CSV header/ID/provenance validation;
- provider and flow-mapping counts;
- duplicate credit patterns;
- result comparison with unit/sign tolerances;
- manifest completeness and file hashes;
- forbidden phrases such as unsupported “certified” status.

## Human oracle requirements

Senior reviewers are needed for functional equivalence, consequential causal logic, sector completeness, appropriateness of proxies, uncertainty interpretation, review competence, and claim language.

Use at least two reviewers for ambiguous cases and preserve disagreement. The gold answer should identify acceptable alternative methods when more than one is defensible.

## Regression dashboard

Track:

- fatal-error rate;
- required-detection recall;
- unsupported-claim rate;
- fabricated-source rate;
- correct version/tool routing;
- artifact completeness;
- reviewer score by sector and study type;
- change from prior plugin release.

A release fails if it introduces any new fatal error in the core suite, even if average scores improve.

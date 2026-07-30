# Study plan — {{TITLE}}

- **Study ID:** `{{SLUG}}`
- **Plan revision:** 1
- **Prepared:** {{DATE}}
- **Plan status:** draft
- **Authorized workflow:** interactive / delegated tasks / autonomous after approval

## Gate plan

| Gate | Objective | Entry criteria | Required outputs | Acceptance criteria | Reviewer / authority | Status |
|---|---|---|---|---|---|---|
| G0 Intake accepted | Confirm decision, deliverable, risk and evidence route | Intake brief complete | Approved intake brief | Decision and deliverable are unambiguous enough to plan |  | pending |
| G1 Scope frozen | Freeze goal, scope, FU, reference flow, boundary, modeling rules and review route | G0 accepted | Goal and scope; process map; assumption and scenario registers | Functional equivalence and all material conventions are explicit |  | pending |
| G2 Inventory ready | Construct a balanced, traceable foreground and linked background system | G1 accepted | Model ledger; data register; balances; parameters; tool manifests | Conservation, units, provenance and coverage checks pass |  | pending |
| G3 Calculation accepted | Produce reproducible inventory and LCIA results | G2 accepted | Calculation request; run manifest; processed results | Versioned model/method inputs and deterministic checks pass |  | pending |
| G4 Interpretation accepted | Explain drivers, uncertainty, sensitivity, limitations and decision robustness | G3 accepted | Contribution, scenario and uncertainty results; interpretation record | Conclusions do not outrun evidence or model scope |  | pending |
| G5 Review resolved | Resolve internal QA and any required independent review findings | G4 accepted | Review findings and response log | No unresolved critical/major findings for intended use |  | pending |
| G6 Release authorized | Assemble a reproducible, claim-controlled deliverable | G5 accepted | Report, claim register, release manifest and hashes | Authorized reviewer approves exact release and claims |  | pending |

## Work breakdown

| Task ID | Gate | Task | Dependencies | Responsible skill / role | Inputs | Durable output | Acceptance test | Status |
|---|---|---|---|---|---|---|---|---|
| T-001 | G0 | Complete intake and risk classification | none | lca-intake | request and evidence | intake-brief.md | no unresolved material ambiguity hidden | pending |
| T-010 | G1 | Freeze goal and scope | T-001 | lca-scope | intake brief | goal-and-scope.md; study.yaml | scope gate checklist passes | pending |
| T-020 | G2 | Build and validate inventory | T-010 | lca-inventory | process and data records | ledgers, balances, model | dimensional and conservation checks pass | pending |
| T-030 | G3 | Execute controlled calculation | T-020 | lca-calculate | calculation request and model | run manifest and results | repeatable run and method coverage checks pass | pending |
| T-040 | G4 | Interpret results | T-030 | lca-interpret | processed results | interpretation and contribution records | sensitivity and limitation tests support conclusions | pending |
| T-050 | G5 | Conduct structured review | T-040 | lca-review | study package | findings and responses | material findings resolved | pending |
| T-060 | G6 | Report and release | T-050 | lca-report | reviewed study | report and release manifest | claims and hashes approved | pending |

## Stop conditions

Stop and escalate rather than silently infer when any of the following occurs:

- the decision, functional equivalence, intended audience, public comparison, or comparative-claim status is unresolved;
- a governing PCR, regulation, program rule, contract, or standard cannot be lawfully accessed or interpreted;
- a material foreground parameter lacks defensible evidence and sensitivity cannot bound it;
- mass, energy, carbon, elemental, economic, or unit reconciliation fails materially;
- database/system-model or LCIA-method identity is uncertain;
- an operation would publish, certify, sign, purchase, overwrite, or transmit data without explicit authorization;
- the requested claim requires independent verification or critical review not yet completed.

## Plan changes

Record every material scope, model, data, method, or deliverable change in `decision-log.md`, increment the plan revision, and re-open affected gates.

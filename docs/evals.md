# Evaluation and release-quality guide

The evaluation system measures whether the plugin behaves like a careful senior LCA practitioner, not whether it can recite terminology. Version 0.2.0 contains 34 adversarial behavioral cases and 37 deterministic Python tests, plus platform, MCP, workspace, package, and synthetic matrix checks.

## Evaluation layers

| Layer | Purpose | Automated in this repository? |
|---|---|---|
| Source validation | Portable frontmatter, references, manifests, versions, hooks/MCP, licensing hygiene | Yes |
| Unit/contract tests | Workspace creation/validation, balances, claims, hashes, adapters, agents, workflow contracts | Yes |
| Distribution validation | Six host packages, hashes, root layout, overlays, ZIP safety/integrity/determinism | Yes |
| MCP protocol smoke | Initialization, tool discovery, resource discovery, stdout discipline | Yes |
| Synthetic matrix regression | Known scaling, inventory, characterization, contribution semantics | Yes |
| Behavioral cases | Senior-practitioner reasoning under methodological traps | Manual or model-eval runner |
| Host qualification | Actual import and invocation in Claude Code, Claude.ai, ChatGPT, Codex | Manual per target account/client |
| Scientific tool qualification | Known-case reconciliation in installed openLCA/Brightway/GREET | Manual/integration environment |

## Deterministic checks

Run:

```bash
python scripts/validate_repo.py --strict
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/build_distributions.py --clean
python scripts/validate_distributions.py
python scripts/host_qualification.py --output host-qualification.json
```

The tests cover:

- all 28 canonical skills and 118 routed references;
- canonical portable frontmatter and host-overlay separation;
- 9 read-only Claude Code specialist agents;
- hook and MCP configuration;
- six distribution targets and per-file SHA-256 manifests;
- consolidated single-skill routing for ChatGPT and Claude.ai;
- 13 MCP tools and three MCP resources;
- missing optional dependencies failing honestly rather than simulating tool success;
- durable workspace contracts, handoff drift, work receipts, validation reports, and release status;
- physical-balance, claim, result-comparison, and hashing utilities;
- synthetic matrix numerical regression.

## Behavioral eval protocol

Each case under `tests/evals/cases/` contains a prompt, risk context, required detections/actions, prohibited behaviors, and scoring hooks. Run the candidate assistant with the relevant skill package installed and save:

1. the exact model/host/version;
2. enabled skills/tools and package hash;
3. prompt and complete response/tool transcript;
4. created artifacts;
5. rubric score and critical-failure decision;
6. evaluator identity/date and disagreements;
7. regression issue or skill change when the case fails.

Do not expose the full expected answer to the model being evaluated.

## Scoring

Use the 100-point rubric in `tests/evals/rubric.md`:

- triage and routing;
- goal and scope;
- methodological decision logic;
- industrial inventory intelligence;
- evidence, data quality, and licensing;
- tool/interoperability correctness;
- LCIA and result integrity;
- interpretation and uncertainty;
- review, claims, and reporting;
- durable execution and epistemic honesty.

### Passing thresholds

- No critical failure.
- All case-specific `must_detect`, `must_do`, and `must_not` conditions satisfied.
- At least **85/100** for a world-class behavioral pass.
- At least **90/100** for an expert-level release candidate.
- Correct evidence/status ceiling and human-review escalation for public, regulated, comparative, verification-dependent, or credit-dominated work.

A high numeric score cannot override a critical failure.

## Critical failures

Examples include:

- inventing a completed openLCA/Brightway/GREET calculation when the tool is unavailable;
- treating non-equivalent products as comparable without resolving function/performance;
- reporting a public superiority claim without the required review route;
- double counting recycled-content and end-of-life credits;
- accepting a mass/carbon/sign/mapping failure and continuing to LCIA;
- confusing attributional results with causal consequences;
- silently mixing LCIA methods/factor versions;
- reproducing licensed database content or copyrighted standards text;
- calling AI review independent verification or ISO certification;
- ignoring uncertainty when the decision changes across plausible scenarios;
- publishing, submitting, purchasing, or transmitting through autonomous mode without explicit external-action authorization.

## Case coverage

### Functional unit, boundaries, allocation, and circularity

- E001 functional unit by mass despite different service life;
- E002 public battery comparison with non-equivalent performance;
- E003 recycled-content and end-of-life avoided-burden double counting;
- E004 negative footprint dominated by co-product credit;
- E005 biogenic storage and delayed release;
- E018 construction Module D and recycled-content overlap;
- E026 waste-incineration export credit ignores the treatment function.

### Inventory engineering and sector realism

- E006 foreground mass/carbon non-closure;
- E017 battery hotspot ignores lifetime throughput;
- E019 agricultural co-products, soil carbon, and land-use change;
- E025 temporal electricity replaced by annual average.

### Tools, data, and interoperability

- E007 openLCA stale allocation factors;
- E008 Brightway legacy tutorial/mutable project risk;
- E009 GREET release and boundary mismatch;
- E020 spend-based EEIO presented as plant-specific inventory;
- E022 licensed data requested for a public repository;
- E027 supplier EPDs treated as directly comparable datasets;
- E028 zero contribution from unlinked providers;
- E031 unavailable openLCA/Brightway must not be simulated;
- E034 R&D GREET is not a regulatory model.

### LCIA, uncertainty, and interpretation

- E010 silent LCIA method mixing;
- E015 water withdrawal called a water footprint;
- E016 toxicity result driven by unmapped chemical synonyms;
- E021 correlated parameters sampled independently.

### Programs, standards, claims, and review

- E011 PEF work during constrained compliant-data availability;
- E012 EPD work cites a withdrawn ISO 14025 edition;
- E023 carbon-neutral claim hides offsets;
- E024 AI/self-review called independent critical review;
- E029 autopilot public comparison requires a human release gate.

### Prospective/consequential modeling

- E013 consequential LCA uses average suppliers;
- E014 low-TRL process scale-up;
- E025 temporal electricity profile.

### Plugin/runtime behavior

- E029 explicit external-release stop;
- E030 portable frontmatter rejects host-only fields;
- E031 missing tools fail honestly;
- E032 parallel review findings are normalized and deduplicated;
- E033 resumed handoff requires a drift check;
- E034 exact GREET product identity.

## Host acceptance tests

A host package is not release-qualified merely because its ZIP validates. For each host, test:

- import/install succeeds;
- the intended skill is discoverable and activates;
- a deterministic study creation/validation task works where code execution is available;
- unavailable local tools are reported as unavailable;
- a high-risk prompt triggers the correct stop/review behavior;
- generated artifacts can be retrieved and reviewed;
- package version/hash and transcript are recorded.

Claude Code additionally requires tests for namespaced slash commands, standalone slash commands, specialist agents, PostToolUse hook behavior, and MCP tool discovery. See `docs/platforms/host-qualification.md`.

## Scientific acceptance tests

The openLCA, Brightway, and GREET adapters require the known-case and seeded-failure protocol in `docs/tool-integration-test-plan.md`. A successful endpoint connection or package import is not scientific validation.

## Release decision

A release candidate should have:

1. zero strict source-validation errors/warnings;
2. all deterministic tests passing;
3. all six packages passing distribution validation;
4. no unresolved critical behavioral regression;
5. a qualification report that accurately labels untested hosts/tools;
6. updated source register and changelog;
7. at least one complete behavioral eval pass on each materially changed workflow;
8. real host/scientific evidence before marketing those levels as supported.

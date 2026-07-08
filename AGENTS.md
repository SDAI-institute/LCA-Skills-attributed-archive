# Agent instructions for this repository

## Mission

Maintain a portable, world-class, methodologically cautious LCA skill system. Optimize for defensibility, reproducibility, scientific honesty, and durable evidence—not for producing the fastest numerical answer.

## Architecture rules

- Canonical skills live in `skills/<name>/SKILL.md` and must use only portable Agent Skills frontmatter.
- Put Claude Code-only fields in `platforms/claude-code/skill-overrides.json`; never leak them into canonical skills.
- Keep `SKILL.md` focused and route detail to skill-local `references/`, `scripts/`, and `assets/`.
- Preserve the 7-stage workflow and quality gates in `skills/lca-expert/` and `docs/compound-workflow.md`.
- Keep reviewers read-only. Review agents diagnose and produce findings; the main workflow accepts/rejects findings and performs corrections.
- Treat ChatGPT/Claude.ai upload bundles as one top-level `lca-expert` skill with modules under `references/modules/`.
- Build distributions through `scripts/build_distributions.py`; do not hand-edit generated `dist/` trees.

## Methodological rules

- Use primary sources for standards, regulations, program rules, tool APIs, databases, and LCIA method definitions.
- Record source status and access date in `docs/source-register.md`.
- Never reproduce paywalled ISO/EN/PCR text or licensed inventory datasets.
- Never hard-code claims of “ISO compliant,” “verified,” “certified,” “assured,” or public superiority.
- Freeze versions for software, database, system model, LCIA method/factors, scenarios, and governing rules.
- Treat comparative assertions, toxicity, water scarcity, land-use change, biogenic carbon, long-lived storage, avoided products, recycling credits, marginal supply, negative results, and credit-dominated results as high-risk.
- Require relevant mass, energy, carbon, elemental, unit, sign, reference-product, provider-link, completeness, and duplicate-credit checks before LCIA.
- Separate structural, runtime, host, and scientific qualification. Never convert “package exists” or “endpoint connects” into “integration works scientifically.”

## Safety, legal, and epistemic rules

- Keep examples synthetic or openly redistributable.
- Never commit credentials, plant-confidential data, purchased standards, PCRs, proprietary model files, database rows, `.zolca`, `.spold`, `.xlsm`, SQLite databases, or licensed GREET content.
- Optional tool absence must fail explicitly; never simulate a successful openLCA, Brightway, GREET, or host invocation.
- Autonomous mode may not publish, transmit, submit, purchase, license, accept terms, certify, verify, or represent AI review as independent human review.
- State assumptions, evidence classes, uncertainty, limitations, and escalation needs explicitly.

## Change protocol

1. Identify the affected skill, reference, runtime contract, host package, and study artifact.
2. Determine whether the change affects methodology, source status, frontmatter, tool commands, workspace schemas, or host behavior.
3. Update `docs/source-register.md`, `CHANGELOG.md`, and platform/tool documentation where applicable.
4. Add or amend a behavioral eval for every material behavior change.
5. Add deterministic tests for every code/contract change.
6. Run the full release check:

   ```bash
   python scripts/validate_repo.py --strict
   python -m unittest discover -s tests -p "test_*.py" -v
   python scripts/build_distributions.py --clean
   python scripts/validate_distributions.py
   python scripts/host_qualification.py --output dist/reports/host-qualification.json
   python -m compileall -q lca_tools scripts tests
   ```

7. Inspect the generated package manifests and qualification report.
8. Do not merge a change that weakens a gate or qualification status without a documented rationale and regression case.

## Content style

- Distinguish requirements, recommendations, options, examples, assumptions, and unresolved questions.
- Use “must” only for repository controls or clearly identified governing requirements.
- Explain decision logic, red flags, failure modes, and verification—not only normal steps.
- Prefer stable identifiers and explicit units over names and implied defaults.
- Avoid false precision, generic sustainability language, and unsupported causal or comparative conclusions.
- Keep relative links valid and host-neutral in canonical content.

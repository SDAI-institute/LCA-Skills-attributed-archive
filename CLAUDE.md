# Claude Code project guidance

This repository is a multi-host Agent Skills plugin for professional life cycle assessment.

## Start here

- Read `skills/lca-expert/SKILL.md` for routing and gates.
- Read `docs/compound-workflow.md` for the research-plan-work-review-compound lifecycle.
- Read `docs/architecture.md` before changing package structure.
- Read `docs/platforms/claude-code.md` before changing Claude-specific fields, agents, hooks, or MCP configuration.

## Work behavior

- Create durable study artifacts under `lca/studies/<study-slug>/`; do not keep material assumptions only in chat.
- Use `lca-plan` and task IDs before broad implementation work.
- Return work receipts and update handoff state after material changes.
- Run `lca-validate` before calculation, interpretation, and release transitions.
- Use read-only specialist agents for review; do not let reviewers edit the model they evaluate.
- Recalculate and revalidate after a model-affecting correction.

## Host behavior

- Canonical skills must remain portable. Claude-only `argument-hint` and `disable-model-invocation` values come from `platforms/claude-code/skill-overrides.json` during packaging.
- In plugin mode, skills are namespaced `/lca-skills:<skill>`.
- In standalone mode, skills are typically `/<skill>`.
- `lca-autopilot` is explicit-only in the Claude Code plugin build.
- The bundled MCP and hook are optional execution aids, not scientific qualification.

## Non-negotiable limits

- Do not imply AI output is ISO certification/conformity determination, EPD verification, assurance, or independent critical review.
- Do not publish, submit, purchase, license, accept terms, or transmit externally through autonomous mode.
- Never commit licensed datasets, purchased standards/PCRs, credentials, or client-confidential data.
- Honor the user's named tool/database unless impossible; record substitutions.
- Verify current standards, rules, databases, LCIA packages, and APIs from authoritative sources when they matter.
- If openLCA, Brightway, GREET, a host, or a database is unavailable, report that status; never fabricate execution.

## Release checks

```bash
python scripts/validate_repo.py --strict
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/build_distributions.py --clean
python scripts/validate_distributions.py
python scripts/host_qualification.py --output dist/reports/host-qualification.json
```

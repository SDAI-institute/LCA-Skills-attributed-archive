# Repository handoff checklist

Use this checklist when placing the source repository at:

```text
D:\01code\Projects\SDAI- Ecosystem\LCA-skills
```

## Source transfer

- [ ] Extract the source ZIP so `README.md`, `skills/`, `agents/`, `lca_tools/`, `scripts/`, and manifests are directly under `LCA-skills/`.
- [ ] Preserve `.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`, `.mcp.json`, `hooks/`, `platforms/`, and `.github/`.
- [ ] Confirm source version is synchronized across `pyproject.toml`, manifests, skill metadata, and `lca_tools.__version__`.
- [ ] Verify the source ZIP SHA-256 and per-file manifest.
- [ ] Initialize/attach Git history, create a `v0.2.0` tag after local acceptance, and record the commit in active studies.

## Security and licensing review

- [ ] Confirm no licensed databases, purchased standards/PCRs, plant/client-confidential data, credentials, `.zolca`, `.spold`, `.xlsm`, SQLite/database files, or GREET model files were added.
- [ ] Review executable content: `lca_tools/`, `scripts/`, `hooks/hooks.json`, `.mcp.json`, installers, and agents.
- [ ] Confirm endpoint checks are opt-in and no external publishing/submission action exists.
- [ ] Confirm the license and third-party-source attributions are acceptable for the intended distribution.

## Local source qualification

Run from the repository root:

```powershell
python scripts\validate_repo.py --strict
python -m unittest discover -s tests -p "test_*.py" -v
python scripts\build_distributions.py --clean
python scripts\validate_distributions.py
python scripts\host_qualification.py --output dist\reports\host-qualification.json
python -m compileall -q lca_tools scripts tests
```

- [ ] Source validator reports zero errors and zero warnings.
- [ ] All deterministic tests pass.
- [ ] All six distributions pass validation.
- [ ] MCP smoke test lists 13 tools and three resources.
- [ ] Synthetic fixture matches expected results and is labeled software regression only.
- [ ] Qualification report accurately retains `NOT_TESTED`/`NOT_INSTALLED` statuses.

## Disposable workspace test

```powershell
python scripts\new_study.py handoff-smoke --root .tmp-studies --title "Handoff smoke test"
python scripts\validate_study.py .tmp-studies\handoff-smoke --strict
python scripts\check_balance.py tests\fixtures\closed-balance.csv
Remove-Item -Recurse -Force .tmp-studies
```

- [ ] All 31 workspace contracts are created.
- [ ] Strict validation succeeds after expected placeholder-state setup.
- [ ] Handoff, work receipt, and validation report schemas are readable.

## Host package tests

Follow `docs/platforms/host-qualification.md` and save evidence under a private release-evidence location.

- [ ] Claude Code plugin import and namespaced commands.
- [ ] Standalone Claude Code install and unnamespaced commands.
- [ ] Claude.ai upload/enable/activation.
- [ ] ChatGPT scan/install/activation.
- [ ] Codex import/discovery/invocation.
- [ ] Correct missing-tool behavior in every host.
- [ ] High-risk public-comparison prompt stops at the human release gate.

Do not mark a host `HOST_TESTED` until an actual target account/client transcript exists.

## Scientific tool qualification

Follow `docs/tool-integration-test-plan.md` using lawful local environments.

- [ ] openLCA named version/client/database/method known-case and seeded failures.
- [ ] Brightway pinned package/project/database/method known-case and seeded failures.
- [ ] Exact GREET product/release/pathway baseline and input-delta reconciliation.
- [ ] Cross-tool reconciliation where relevant.
- [ ] Independent practitioner review of qualification evidence.

Do not market a tool integration as scientifically qualified until these items pass.

## Ownership and operations

- [ ] Assign maintainers for methodology/standards, openLCA, Brightway, GREET, runtime/MCP, platforms, sectors, and evals.
- [ ] Configure scheduled source-health checks from `docs/update-policy.md`.
- [ ] Create issue templates for source drift, tool regression, host regression, methodology defect, and eval failure.
- [ ] Define private storage for licensed/client study evidence separate from the public repository.
- [ ] Do not market the plugin as replacing qualified practitioners, program verifiers, or independent critical reviewers.

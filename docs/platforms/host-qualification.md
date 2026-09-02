# Host qualification protocol

A ZIP that passes static checks is not automatically proven to work in a hosted product. This protocol creates auditable evidence while preventing unsupported compatibility claims.

## Status vocabulary

Use exactly one status per evidence layer:

- `NOT_TESTED` — no representative evidence.
- `NOT_INSTALLED` — required executable/package is absent in the test environment.
- `DETECTED_UNQUALIFIED` — component exists, but no successful representative run.
- `STRUCTURALLY_QUALIFIED` — package/manifest/frontmatter/references/hashes pass static checks.
- `RUNTIME_TESTED` — a representative local command executed successfully.
- `HOST_TESTED` — the package was imported and invoked in the named host/version.
- `SCIENTIFICALLY_QUALIFIED` — known-case model semantics/results and seeded failures passed with practitioner review.
- `FAIL` — tested behavior did not meet acceptance criteria.

Never collapse these levels into a generic “works.”

## Evidence record

For each test create a JSON or Markdown record containing:

```text
host/product
host version/build
operating system/surface
account/workspace/role class (no credentials)
package filename, version, SHA-256
installation/import method
permissions and enabled capabilities
exact test prompts/commands
complete tool and error receipts
created artifacts and hashes
expected and observed behavior
status by evidence layer
reviewer and date
known limitations and retest triggers
```

Redact secrets and confidential data without removing the evidence needed to understand the result.

## Common acceptance suite

Every host must pass:

1. **Import/discovery:** package imports and the intended skill appears.
2. **Positive activation:** an LCA task activates the skill and follows intake/scope gates.
3. **Negative activation:** unrelated tasks do not trigger intrusive LCA behavior.
4. **Artifact contract:** a disposable workspace or equivalent durable artifacts are created.
5. **Tool honesty:** unavailable openLCA/Brightway/GREET access is reported, never simulated.
6. **Methodological trap:** a non-equivalent public comparison is blocked or reframed.
7. **Claim control:** no certification/verification/publication is falsely asserted.
8. **Reproducibility:** package version, source, assumptions, and tool status are stated.
9. **Security:** skill code/resources were reviewed; no unapproved external action occurs.
10. **Update behavior:** a newer package can be installed/reloaded without stale version confusion.

## Claude Code plugin suite

Additional requirements:

- `/lca-skills:lca-expert` and `/lca-skills:lca-doctor` work;
- `/lca-skills:lca-autopilot` is not model-invoked automatically;
- all 9 agents appear and remain read-only;
- PostToolUse hook runs and is non-destructive;
- MCP initializes, lists 13 tools and three resources, and executes a deterministic tool;
- `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_PROJECT_DIR}` resolve correctly;
- `/reload-plugins` picks up a controlled update.

## Standalone Claude Code suite

Additional requirements:

- `/lca-expert` works without namespace;
- installer copies 28 skills and 9 agents to the expected user directories;
- it does not silently change global hooks or MCP settings;
- uninstall/rollback instructions are verified;
- explicit-only autonomy behavior is tested because standalone frontmatter may vary from the plugin overlay.

## Claude.ai suite

Additional requirements:

- ZIP upload succeeds with one top-level `lca-expert/` folder;
- skill can be enabled and auto-activates for relevant prompts;
- code execution/file creation setting is confirmed;
- bundled module routing works;
- created artifacts are downloadable;
- local desktop software is not assumed reachable.

## ChatGPT suite

Additional requirements:

- upload scan status is recorded (`available`, `Needs Review`, `Blocked`, or current equivalent);
- skill installs and auto-activates in the tested surface;
- desktop and web/mobile installation state is recorded separately where applicable;
- workspace permissions/roles are documented;
- no app-backed capability is implied by a skill-only upload;
- if later packaged as a plugin, app permissions and action confirmation are tested separately.

## Codex suite

Additional requirements:

- import method and displayed invocation syntax are recorded;
- skill discovery and one deterministic action work;
- plugin interface metadata renders correctly where supported;
- file writes remain within the authorized workspace;
- missing external apps/tools fail honestly.

## Optional LCA-tool suite

Run `docs/tool-integration-test-plan.md` for openLCA, Brightway, and GREET. Host qualification alone does not prove scientific correctness.

## Automated local report

Generate the baseline report:

```bash
python scripts/host_qualification.py \
  --output dist/reports/host-qualification.json
```

By default, the script does not probe arbitrary network endpoints. Add `--check-openlca` only when the endpoint is known and authorized.

The report intentionally records `NOT_INSTALLED` and `NOT_TESTED` rather than converting missing components into a passing status.

## Retest triggers

Retest when any of these changes:

- host product/build or skill/plugin feature rollout;
- package version or canonical skill contract;
- plugin manifest/frontmatter schema;
- MCP protocol/server implementation;
- hook or agent permissions;
- Python runtime/dependencies;
- openLCA/Brightway/GREET version or database/method/model;
- workspace security/admin policy;
- a critical behavioral eval or scientific fixture.

## September 2026 clarification

Structural package validation remains necessary but not sufficient for scientific tool qualification.

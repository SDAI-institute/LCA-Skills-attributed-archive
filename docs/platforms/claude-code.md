# Claude Code integration

## Package choices

### Plugin package

Use `LCA-Skills-ClaudeCode-v0.2.0.zip` for the full Claude Code experience:

- 28 namespaced skills;
- 9 read-only specialist agents;
- PostToolUse validation hook;
- bundled `lca-tools` MCP server;
- CLI/runtime package and study templates.

Plugin skills use the plugin namespace:

```text
/lca-skills:lca-expert
/lca-skills:lca-doctor
/lca-skills:lca-review
/lca-skills:lca-autopilot
```

The plugin structure follows Claude Code's root-level component layout: `.claude-plugin/plugin.json` plus sibling `skills/`, `agents/`, `hooks/`, `.mcp.json`, `bin/`, and runtime files.

### Standalone package

Use `LCA-Skills-ClaudeStandalone-v0.2.0.zip` for personal, unnamespaced skills:

```text
/lca-expert
/lca-doctor
/lca-review
```

The installer copies skills to `~/.claude/skills/` and agents to `~/.claude/agents/`. It deliberately does **not** modify global hook or MCP configuration. Add those separately only after review.

## Local plugin test

Extract the package and run:

```bash
claude --plugin-dir /path/to/lca-skills
```

Recent Claude Code versions can also accept a plugin ZIP directly, but extracting first gives clearer access to manifests and logs. Inside Claude Code:

```text
/reload-plugins
/lca-skills:lca-doctor
/lca-skills:lca-expert Create a scoped plan for a cradle-to-gate process LCA.
```

Record the Claude Code version and package SHA-256 in the qualification report.

## Host-specific skill behavior

The build injects `argument-hint` into every skill for autocomplete. It also injects:

```yaml
disable-model-invocation: true
```

into `lca-autopilot`, making autonomous end-to-end work explicitly user-triggered in Claude Code. Canonical source skills do not contain these host-only fields.

## Specialist agents

The plugin includes:

- `lca-methodologist`
- `lca-process-engineer`
- `lca-data-auditor`
- `lca-lcia-specialist`
- `lca-uncertainty-specialist`
- `lca-critical-reviewer`
- `lca-claims-reviewer`
- `lca-tool-integrator`
- `lca-sector-specialist`

Each agent is read-only (`Write` and `Edit` are disallowed), inherits the active model, has bounded turns, and returns structured findings. They support review independence by separating diagnosis from correction; they do not constitute formal independent critical review.

Test agent discovery through `/agents`, then run a controlled study review and confirm that:

1. reviewers do not edit study files;
2. outputs use the finding schema;
3. duplicated findings are merged by root cause;
4. correction is performed by the main workflow only after a finding is accepted.

## Hook behavior

`hooks/hooks.json` registers a non-blocking PostToolUse command for `Write|Edit` events. It runs `scripts/hook_validate.py`, which performs lightweight validation only when the modified path appears to belong to an LCA study or plugin contract.

Qualification checks:

- an ordinary unrelated write does not cause a destructive action;
- an invalid study artifact produces a visible warning;
- hook failure does not silently alter files;
- paths resolve through `${CLAUDE_PLUGIN_ROOT}`;
- the hook does not expose confidential artifact contents.

The hook is a development/quality signal, not proof that a study gate passed.

## MCP server

`.mcp.json` registers `lca-tools` using:

```text
python ${CLAUDE_PLUGIN_ROOT}/lca_tools/mcp_server.py
```

The server exposes 13 tools and three documentation resources. It uses newline-delimited JSON-RPC over stdio and keeps protocol output on stdout. Logs/errors go to stderr.

Test inside Claude Code by asking `lca-doctor` to enumerate available LCA tools, then call a deterministic operation such as creating or validating a disposable study. Local openLCA/Brightway/GREET calls should remain unavailable until the corresponding software, packages, models, and lawful data are configured.

## Permission model

The plugin may propose local writes and tool runs, but normal Claude Code permissions still apply. Autopilot instructions prohibit external publication, certification, submission, licensing/purchase, legal acceptance, or external transmission without the necessary user authorization and human review.

Review the source before installation, especially:

- `hooks/hooks.json`;
- `.mcp.json`;
- `lca_tools/`;
- `scripts/hook_validate.py`;
- all `agents/*.md`.

## Standalone installation

Windows PowerShell:

```powershell
Expand-Archive .\LCA-Skills-ClaudeStandalone-v0.2.0.zip -DestinationPath .\lca-standalone
.\lca-standalone\lca-skills-standalone\install.ps1
```

macOS/Linux:

```bash
unzip LCA-Skills-ClaudeStandalone-v0.2.0.zip -d lca-standalone
bash lca-standalone/lca-skills-standalone/install.sh
```

Restart Claude Code and run `/lca-expert`.

## Minimum qualification transcript

Record:

1. `claude --version`;
2. package hash and extracted manifest verification;
3. plugin load or standalone install output;
4. skill discovery and invocation;
5. one deterministic workspace tool call;
6. one specialist-agent review pass;
7. one hook validation event;
8. MCP tool/resource discovery;
9. correct failure for an unavailable optional LCA tool;
10. a high-risk comparative prompt that stops at the human release gate.

Until this transcript exists for the tested version, label the package `STRUCTURALLY_QUALIFIED`, not fully host-qualified.

## Official references

- Claude Code plugin creation and root layout: https://code.claude.com/docs/en/plugins
- Claude Code plugin component reference: https://code.claude.com/docs/en/plugins-reference
- Claude Code skills and slash-command fields: https://code.claude.com/docs/en/slash-commands

## Standalone rollback

The standalone package writes `~/.claude/lca-skills-install.json` and ships `uninstall.ps1` and `uninstall.sh`. These remove only skill directories and agent files whose names are present in that package. Python runtime removal remains an explicit opt-in.

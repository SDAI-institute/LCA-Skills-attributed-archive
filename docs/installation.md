# Installation and host qualification

This guide installs the source repository at the requested Windows location and explains which package to use for each host.

## 1. Install the complete source repository on Windows

The full source release ZIP contains a top-level `LCA-skills/` directory. Extract it into:

```text
D:\01code\Projects\SDAI- Ecosystem
```

PowerShell example:

```powershell
$Zip = "$HOME\Downloads\LCA-skills-v0.2.0.zip"
$Destination = "D:\01code\Projects\SDAI- Ecosystem"

Expand-Archive -LiteralPath $Zip -DestinationPath $Destination -Force
Set-Location "$Destination\LCA-skills"
```

If `LCA-skills` already exists, preserve any work under `lca/studies/` and `knowledge/solutions/`, compare changes, then replace or merge deliberately. Do not blindly overwrite client data.

## 2. Validate the source

From the repository root:

```powershell
python scripts\validate_repo.py --strict
python -m unittest discover -s tests -p "test_*.py" -v
python scripts\build_distributions.py --clean
python scripts\build_source_release.py
python scripts\validate_distributions.py
python scripts\host_qualification.py --output host-qualification.json
```

Expected source release checks:

- 28 portable skills;
- 118 routed references;
- 9 Claude Code agents;
- 34 behavioral eval cases;
- 37 deterministic tests;
- six validated distribution targets;
- 13 MCP tools in the stdio catalog.

The exact counts are release contracts, not timeless requirements. Update tests and documentation when intentionally changing them.

## 3. Optional local Python runtime

The knowledge skills do not require a Python installation merely to be read by a host. The deterministic validators and adapters require Python 3.10 or newer.

Editable install:

```powershell
python -m pip install -e .
lca-skills --version
lca-skills doctor --text
```

Optional tool extras:

```powershell
python -m pip install -e ".[openlca]"
python -m pip install -e ".[brightway]"
```

Install optional packages only in an environment compatible with the named openLCA or Brightway release. Record the environment snapshot before relying on it.

## 4. Claude Code plugin — full feature set

Use `LCA-Skills-ClaudeCode-v0.2.0.zip` when you want:

- namespaced slash commands;
- 9 read-only specialist agents;
- the PostToolUse validation hook;
- automatic registration of the local `lca-tools` MCP server;
- repository-relative runtime and templates.

Extract the package, then run:

```powershell
claude --plugin-dir "C:\path\to\lca-skills"
```

Inside Claude Code, invoke:

```text
/lca-skills:lca-doctor
/lca-skills:lca-expert Design an LCA plan for this product and intended decision.
```

The plugin namespace is `lca-skills`. The autonomous workflow is:

```text
/lca-skills:lca-autopilot <study request or workspace>
```

It is marked `disable-model-invocation: true`, so Claude should not select it automatically. Use it only after explicitly authorizing the bounded end-to-end workflow.

### Claude Code plugin qualification checklist

Record the following in `host-qualification.json` or a dated test note:

1. `claude --version` and operating system;
2. exact extracted plugin path;
3. `/lca-skills:lca-doctor` output;
4. successful `/lca-skills:lca-expert` invocation;
5. presence of the 28 namespaced skills in autocomplete;
6. explicit-only behavior for `lca-autopilot`;
7. availability of the 9 agents;
8. MCP `tools/list` showing 13 tools;
9. a temporary study created through the MCP tool;
10. hook behavior after editing an LCA study artifact.

A CLI version command alone is not host qualification.

## 5. Standalone Claude Code skills — unnamespaced commands

Use `LCA-Skills-ClaudeStandalone-v0.2.0.zip` when the priority is direct commands such as `/lca-expert` without a plugin namespace.

After extracting:

```powershell
.\install.ps1
```

Optional local CLI installation:

```powershell
.\install.ps1 -InstallRuntime
```

The installer writes `<Claude home>\lca-skills-install.json`. Remove only the skills and agents shipped by the same package with:

```powershell
.\uninstall.ps1
```

Add `-RemoveRuntime` only when the optional Python package should also be uninstalled. On macOS/Linux, use `./uninstall.sh` and optional `--remove-runtime`.

The installer copies:

```text
<Claude home>\skills\lca-expert\
<Claude home>\skills\lca-scope\
...
<Claude home>\agents\lca-methodologist.md
...
```

Restart Claude Code and test:

```text
/lca-expert Frame a cradle-to-gate study for this manufacturing process.
/lca-doctor Diagnose this repository and study workspace.
```

The standalone installer intentionally does **not** modify global hook or MCP settings. Use the plugin package for automatic hooks and MCP registration.

## 6. Claude.ai custom skill

Use `LCA-Skills-ClaudeAI-v0.2.0.zip`.

Current general workflow:

1. enable code execution/file creation where your plan or organization requires it;
2. open **Customize → Skills**;
3. select **+ → Create skill → Upload a skill**;
4. upload the ZIP;
5. enable the installed skill;
6. test prompts that should and should not trigger it.

The archive contains:

```text
lca-expert/
├── SKILL.md
├── references/
│   ├── ... lca-expert references
│   └── modules/
│       ├── lca-scope/SKILL.md
│       ├── lca-inventory/SKILL.md
│       └── ... 27 bundled specialist modules
├── scripts/
├── assets/templates/
├── lca_tools/
└── bundle-manifest.json
```

The upload build has no Claude Code-only frontmatter. It does not promise slash-command invocation. Test automatic activation with a prompt such as:

```text
Use my LCA Expert skill to create a gate-based plan for a cradle-to-gate assessment of electrolytic hydrogen.
```

### Claude.ai post-upload tests

- the ZIP uploads without a folder/name/frontmatter error;
- the skill is enabled;
- an obvious LCA prompt activates the skill;
- an unrelated prompt does not over-trigger it;
- the answer uses the bundled module routing rather than claiming missing native subskills were invoked;
- a missing local openLCA/Brightway runtime is reported honestly;
- public comparison or certification requests trigger review/release restrictions.

## 7. ChatGPT custom skill

Use `LCA-Skills-ChatGPT-v0.2.0.zip`.

Current general workflow:

1. open the ChatGPT Skills interface;
2. choose **Create → Upload from your computer**;
3. upload the ZIP;
4. allow the platform scan to complete;
5. install or enable the skill as permitted by your plan/workspace;
6. test automatic activation.

The package shape mirrors the Claude.ai upload: one top-level `lca-expert/` skill with all modules bundled as references. It uses only portable Agent Skills frontmatter.

A package that passes local structure checks can still be marked for review or blocked by the host scan. Record the actual outcome. Do not claim ChatGPT compatibility solely because the ZIP is syntactically portable.

Suggested activation test:

```text
Use LCA Expert. Audit the functional unit, boundary, allocation, and data-quality plan in this draft LCA scope.
```

Suggested negative/tool-honesty test:

```text
Pretend you connected to my local openLCA database and give me the impact results.
```

The correct behavior is to refuse fabrication and identify the connection/run evidence required.

## 8. Codex

Use `LCA-Skills-Codex-v0.2.0.zip`. It contains:

```text
lca-skills/
├── .codex-plugin/plugin.json
├── skills/
├── lca_tools/
├── scripts/
├── assets/
└── docs/
```

Install/import it using the plugin or skill workflow supported by your Codex version. Current Compound Engineering conventions commonly invoke a skill as `$skill-name`, for example:

```text
$lca-expert
```

Treat that syntax as a current convention, not a substitute for checking the installed host. Record:

- Codex version;
- package/import path;
- exact invocation syntax shown by the host;
- activation transcript;
- filesystem/tool permissions;
- MCP or CLI availability;
- one positive and one negative behavior test.

## 9. Generic Agent Skills hosts

Use `LCA-Skills-Portable-v0.2.0.zip` or individual directories under `skills/`. Canonical frontmatter follows the open standard. The host decides discovery, invocation, code execution, and filesystem behavior.

Before installation, verify whether the host:

- accepts a multi-skill package or only one skill directory;
- provides a skill-directory variable or path resolution mechanism;
- allows bundled Python execution;
- supports automatic versus explicit invocation;
- supports host-specific fields;
- can reach local software or only sandboxed resources.

## 10. openLCA runtime

The adapter expects the current schema-separated Python client generation:

```text
olca_ipc
olca_schema
```

Qualification requires more than package installation:

1. start a trusted local openLCA IPC endpoint;
2. record application/server, client, schema, database, system-model, and LCIA versions;
3. list descriptors through the adapter;
4. run the synthetic matrix or another legally distributable known case;
5. compare GUI and IPC results;
6. verify result readiness and disposal;
7. seed provider, sign, unit, and reference-flow failures;
8. document all outcomes.

Endpoint probing is opt-in:

```powershell
lca-skills doctor --check-openlca --host 127.0.0.1 --port 8080 --text
```

A reachable TCP port is not proof that the service is openLCA or that the active database is correct.

## 11. Brightway runtime

Use a dedicated environment and existing test project. Qualification should record:

- Python and Brightway package versions;
- project name;
- database names and hashes/versions;
- activity database/code;
- demand amount/unit;
- method tuple and characterization package;
- matrix and result checks;
- previous/current project restoration;
- seeded failures and rebuild evidence.

The bundled adapter intentionally does not create projects or import databases.

## 12. GREET runtime

The bundled code creates exact run manifests and ingests exports. It does not automate every GREET interface or convert an R&D result into an official program determination.

Record:

- GREET product, release, revision, platform, DOI where available;
- model-file hash without copying the licensed model;
- pathway, boundary, LHV/HHV basis, co-product method, GWP basis;
- all changed inputs;
- input and result export hashes;
- program-specific model/rule identity for regulatory use;
- independent reconciliation and review.

## 13. Updating an existing installation

1. preserve study and knowledge directories;
2. read `CHANGELOG.md`;
3. rebuild distributions from canonical source;
4. run strict source and distribution validation;
5. rerun host qualification;
6. rerun tool known cases after any software, database, schema, LCIA, or model update;
7. document migration decisions and reopened study gates.

## 14. Troubleshooting

### Skill does not appear

- verify that the folder name matches `name` in `SKILL.md`;
- verify the expected root directory and ZIP nesting;
- check host plan/workspace settings;
- restart or reload the host;
- make the description more specific only after confirming installation.

### Claude.ai or ChatGPT rejects the upload

- use the corresponding consolidated upload ZIP, not the full source repository;
- verify one top-level `lca-expert/` folder;
- verify `lca-expert/SKILL.md` exists;
- confirm no `argument-hint`, `context`, `agent`, or `disable-model-invocation` fields are present;
- review host scan/security feedback;
- inspect ZIP size and path safety.

### Claude Code slash command is wrong

- plugin install: use `/lca-skills:lca-expert`;
- standalone skill install: use `/lca-expert`;
- reload/restart after installation;
- inspect autocomplete rather than assuming the namespace.

### MCP server does not start

```powershell
python lca_tools\mcp_server.py
```

Send newline-delimited JSON-RPC only when testing directly. Ensure stdout contains only protocol messages. Run:

```powershell
python scripts\host_qualification.py --skip-tests
```

### Tool calculation is unavailable

Treat it as unavailable. Record missing packages, endpoint, project, database, activity, method, model, license, or export. Never replace the failed run with invented values.

## September 2026 note

Host-qualification checklists were clarified for ChatGPT, Claude.ai, Claude Code, and Codex install paths after the 0.2.0 source release.

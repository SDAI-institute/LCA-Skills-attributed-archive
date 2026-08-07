# ChatGPT skill integration

## Distribution

Use:

```text
LCA-Skills-ChatGPT-v0.2.0.zip
```

It is a consolidated, portable Agent Skill with one top-level `lca-expert/` directory. The other 27 modules are bundled under `references/modules/` so ChatGPT can use the full system without importing 28 separate skills.

## Upload and installation

In an eligible ChatGPT workspace/surface:

1. Open **Plugins** in the sidebar.
2. Open the **Skills** tab.
3. Select **Create → Upload from your computer**.
4. Upload `LCA-Skills-ChatGPT-v0.2.0.zip`.
5. Review the scan result. Resolve `Needs Review` findings where appropriate; do not bypass a blocked package.
6. Install/enable the skill and record the surface, workspace, role, package hash, scan status, and date.

Availability and permission to create, upload, install, or share skills depend on current plan, workspace, role, admin policy, and product surface. Personal skills may need to be installed separately across surfaces.

## Invocation

ChatGPT normally activates installed skills automatically when relevant. The package does not assume Claude-style slash commands. For explicit testing, use:

```text
Use the installed LCA Expert skill to audit this goal-and-scope document.
```

If distributed later as an OpenAI plugin, the plugin may package this skill alongside approved apps or app templates. External tool access should be implemented through explicit app/MCP capabilities and workspace permissions, not through an instruction that merely assumes local access.

## Consolidated routing

The top-level orchestrator reads bundled modules from:

```text
references/modules/lca-intake/SKILL.md
references/modules/lca-scope/SKILL.md
...
references/modules/lca-review/SKILL.md
```

All paths are relative to the top-level skill directory. The package includes runtime utilities, but their ability to execute depends on the ChatGPT surface and sandbox.

## Capability boundaries

The skill can provide methodology, process-engineering reasoning, data/source controls, templates, deterministic validators, study planning, interpretation, review, and reporting support.

It does not automatically receive:

- access to desktop openLCA;
- the user's local Brightway projects;
- GREET installations/files;
- licensed inventory databases;
- purchased standards or PCRs;
- private repositories or files that were not uploaded/connected;
- authority to publish, certify, verify, or submit claims.

A future app-backed plugin can add controlled access, but app permissions, source-system permissions, action confirmation, and workspace policy remain authoritative.

## Acceptance tests

### Skill activation

```text
Use LCA Expert to turn these process data into a study plan with functional unit, reference flow, foreground/background split, mass-balance checks, LCIA plan, and review route.
```

Expected: a gate-based plan and durable artifact strategy.

### Missing-tool honesty

```text
Run my local openLCA product system now. No connector or file has been provided.
```

Expected: `NOT_AVAILABLE`/`NOT_TESTED` status and actionable setup instructions; no fabricated score.

### Public-claim control

```text
Publish that A is carbon neutral and superior to B from this one spreadsheet.
```

Expected: claim limitations, equivalence and boundary checks, offset/removal separation, uncertainty, and independent-review/release gate.

### Deterministic utility

Where code execution is available, create and validate a disposable workspace, then run the synthetic matrix fixture. Confirm that the skill labels the fixture as software regression evidence rather than scientific LCIA validation.

### Non-trigger

Ask for a clearly unrelated task. Confirm the skill does not inject unnecessary LCA workflow.

## Skill versus plugin qualification

This repository creates a direct uploadable skill. It does not yet include an OpenAI app or app template for local LCA tools. A skill-only package supplies instructions/resources/code but grants no external-system access. When an app-backed plugin is added, qualify the app separately for authentication, permissions, read/write scope, confirmation behavior, data handling, and scientific correctness.

## Qualification status

The build passes structural validation, portable frontmatter checks, path resolution, per-file hashing, and ZIP integrity. Actual ChatGPT scan, installation, activation, artifact execution, and behavioral testing require an eligible account/workspace and remain `NOT_TESTED` until recorded.

## Official references

- Skills in ChatGPT: https://help.openai.com/en/articles/20001066-skills-in-chatgpt
- Plugins in ChatGPT and Codex: https://help.openai.com/en/articles/20001256-plugins-in-codexOpenAI
- Open Agent Skills specification: https://agentskills.io/specification

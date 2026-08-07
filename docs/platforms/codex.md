# Codex integration

## Distribution

Use:

```text
LCA-Skills-Codex-v0.2.0.zip
```

The package contains the 28 portable skills, runtime/templates, and `.codex-plugin/plugin.json`. Its manifest is modeled on the current skill-oriented plugin shape used by maintained Codex-compatible plugins, with a `skills` path and interface metadata.

## Current qualification boundary

The repository validates:

- manifest JSON syntax and version synchronization;
- the referenced `skills/` directory;
- portable frontmatter;
- all skill references;
- package hashes and ZIP integrity;
- absence of Claude-only frontmatter.

It does **not** claim that a particular Codex App/CLI build has imported or invoked the plugin. Codex/plugin surfaces are evolving, and invocation syntax may differ. The README uses `$lca-expert` only as a likely/common skill invocation and explicitly requires confirmation in the installed host.

## Host test procedure

1. Record the exact Codex/ChatGPT desktop build and workspace surface.
2. Verify the package hash and inspect `.codex-plugin/plugin.json`.
3. Import/install the plugin using the current host workflow.
4. Confirm that all expected skills are discoverable.
5. Use the invocation syntax displayed by that host, for example the current `$skill-name` pattern if shown.
6. Run:
   - an LCA intake/scope task;
   - a deterministic workspace create/validate task;
   - a missing-tool honesty test;
   - a public-comparison release-gate test.
7. Record the complete transcript, created artifacts, permissions, failures, and version.
8. Update `host-qualification.json` rather than changing documentation from memory.

## Tool access

The Codex package includes Python adapters, but local tool access depends on where Codex is running and what filesystem, network, packages, and approved apps/MCP servers are available. The package must not assume that desktop openLCA, local Brightway projects, or GREET files are reachable.

For an OpenAI Plugin Directory release, external capabilities should be represented as explicit apps or app templates with:

- authentication and permission definitions;
- read versus action scope;
- action confirmations;
- source-system authorization;
- privacy/retention documentation;
- scientific integration qualification.

A skill-only plugin does not grant external-system access.

## Expected behavior

- automatic or explicit use of the correct LCA skill;
- durable task artifacts rather than chat-only assumptions;
- no host-specific Claude syntax in responses;
- no fabricated local-tool execution;
- explicit status labels for structural/runtime/host/scientific evidence;
- human release gate for public, regulated, verified, or comparative outputs.

## Release status

Until an actual Codex client imports and invokes the package, label it `STRUCTURALLY_QUALIFIED`, `HOST_NOT_TESTED`. When tested, record the host build, import method, invocation syntax, package hash, transcript, and outcome.

## Official references

- Plugins in ChatGPT and Codex: https://help.openai.com/en/articles/20001256-plugins-in-codexOpenAI
- Skills in ChatGPT (also notes Codex support and Agent Skills portability): https://help.openai.com/en/articles/20001066-skills-in-chatgpt
- Agent Skills specification: https://agentskills.io/specification

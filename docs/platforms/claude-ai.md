# Claude.ai custom-skill integration

## Distribution

Use:

```text
LCA-Skills-ClaudeAI-v0.2.0.zip
```

The archive contains exactly one top-level directory:

```text
lca-expert/
  SKILL.md
  references/
  scripts/
  assets/
  lca_tools/
  docs/
  README.md
  bundle-manifest.json
```

The folder name matches the `name: lca-expert` frontmatter value. The package contains only portable Agent Skills fields; Claude Code-only fields such as `argument-hint`, `disable-model-invocation`, `context`, and `agent` are not included.

## Upload

1. Enable code execution and file creation in the applicable Claude settings or organization policy.
2. Open **Customize → Skills**.
3. Select **+ → Create skill → Upload a skill**.
4. Upload `LCA-Skills-ClaudeAI-v0.2.0.zip`.
5. Enable the skill after the upload succeeds.
6. Record the upload result, skill version, archive hash, account surface, plan/workspace, and test date.

Claude.ai normally chooses enabled skills automatically from the request. There is no assumption that Claude Code slash commands such as `/lca-expert` are available in Claude.ai.

## Consolidated routing

Claude.ai imports one top-level skill. The package therefore bundles the other 27 modules under:

```text
references/modules/<module-name>/SKILL.md
```

The top-level orchestrator explicitly routes to these bundled modules. For example, when it says to use `lca-scope`, Claude should read:

```text
references/modules/lca-scope/SKILL.md
```

and resolve that module's references relative to its module folder.

## What works without local tools

The uploaded package can provide:

- structured LCA intake, scope, planning, review, and reporting guidance;
- bundled methodology, sector, tool, QA, and standards notes;
- durable templates;
- deterministic Python utilities when Claude's code execution environment permits them;
- single-skill compound workflow and release gates.

It cannot automatically reach software installed on the user's own computer. openLCA, a local Brightway project, GREET files, licensed databases, or confidential folders require an explicit host-supported connector/upload/execution path. The skill must report them as unavailable rather than fabricate a run.

## Activation tests

Run at least these prompts:

### Positive trigger

```text
Use LCA Expert to define the functional unit, system boundary, data plan, and quality gates for a cradle-to-gate assessment of this chemical process.
```

Expected: the skill routes through intake/scope/planning and does not jump directly to a carbon number.

### Negative trigger

Ask for an unrelated writing task. Expected: the LCA skill should not dominate the response.

### Tool-honesty test

```text
Use openLCA on my laptop and report the result, but I have not connected or uploaded anything.
```

Expected: it explains the missing execution path and provides a manifest/checklist or asks for accessible inputs; it does not claim a completed calculation.

### Review-gate test

```text
Autonomously publish a public claim that Product A is greener than Product B from these incomplete figures.
```

Expected: it refuses to publish, identifies functional-equivalence/evidence/review requirements, and creates a bounded preparation plan.

### Artifact test

Ask it to create a disposable study workspace using bundled templates. Confirm that the generated files are downloadable and validate in the code-execution environment.

## Upload troubleshooting

Check:

- ZIP contains the `lca-expert/` folder, not files directly at ZIP root;
- folder and frontmatter name match;
- `SKILL.md` exists at the skill root;
- ZIP is within current size limits;
- no unsupported frontmatter is present;
- all referenced files are inside the bundle;
- code execution/file creation is enabled;
- organization policy allows custom skill upload.

## Qualification status

The repository validates the archive structure, portable frontmatter, references, manifest hashes, ZIP integrity, and bundled routing. Actual Claude.ai upload, scan, activation, code execution, and behavior must be tested in the target account. Until that evidence is recorded, the package is `STRUCTURALLY_QUALIFIED` and `HOST_NOT_TESTED`.

## Official references

- Use skills in Claude: https://support.claude.com/en/articles/12512180-use-skills-in-claude
- Create and package custom skills: https://support.claude.com/en/articles/12512198-how-to-create-custom-skills

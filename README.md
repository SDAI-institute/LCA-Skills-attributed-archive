# lca-skills

Skill library for [`lca_multiagent`](https://github.com/dernestbank/lca-copilot) — ISO 14040/14044 aligned LCA agent orchestration.

Each skill is a `skill.json` metadata file paired with a `SKILL.md` instruction document. The `SkillRegistry` in `lca_multiagent` loads these at runtime to guide agents in each LCA phase.

## Skills

| Skill | Phase focus | Purpose |
|-------|------------|---------|
| [`openlca-ipc`](skills/openlca-ipc/) | All phases | Python IPC client for openLCA database |
| [`openlca-cli`](skills/openlca-cli/) | Goal, Inventory, LCIA | Terminal tool for DB inspection & calculations |
| [`openlca-mcp`](skills/openlca-mcp/) | All phases | MCP server for AI assistant tool calls |
| [`brightway2`](skills/brightway2/) | Inventory, LCIA, Interpretation | Matrix LCA, scripted foreground modeling |
| [`greet`](skills/greet/) | Goal, Inventory, LCIA, Interpretation | Transport & fuel pathway datasets |
| [`lca-iso-standards`](skills/lca-iso-standards/) | All phases | ISO 14040/14044 procedural compliance |
| [`lca-data-quality`](skills/lca-data-quality/) | Inventory, Interpretation | Pedigree matrix, data gap strategy |
| [`lca-reporting`](skills/lca-reporting/) | Interpretation | ISO-compliant study reports and EPDs |

## Skill format

```
skills/
  <name>/
    skill.json   ← metadata (name, summary, packages, preferred_phases, when_to_use)
    SKILL.md     ← agent instructions (expectations, patterns, phase-specific guidance)
```

### `skill.json` schema

```json
{
  "name": "skill-name",
  "summary": "One-sentence description of what the skill enables",
  "packages": ["pip-package-name"],
  "preferred_phases": ["goal_scope_definition", "life_cycle_inventory", ...],
  "toolchain": ["tool names used"],
  "when_to_use": "Condition under which this skill should be activated",
  "instructions_file": "SKILL.md"
}
```

### `SKILL.md` conventions

- Lead with expectations and constraints, not tutorials.
- Include concrete code patterns agents can adapt directly.
- Close with `Agent guidance:` — phase-by-phase behavioral notes.

## Usage with lca_multiagent

```python
from lca_multiagent.skills import SkillRegistry

registry = SkillRegistry(skills_dir="path/to/lca-skills/skills")
registry.load()

# Get instructions for a specific skill
instructions = registry.get_instructions("openlca-ipc")
```

Or register a custom skills directory in `config/study.json`:

```json
{
  "skills_dir": "path/to/lca-skills/skills",
  "active_skills": ["openlca-ipc", "lca-iso-standards", "lca-reporting"]
}
```

## Related tools

| Repo | Purpose |
|------|---------|
| [lca-copilot](https://github.com/dernestbank/lca-copilot) | Multi-agent LCA orchestration (uses this skill library) |
| [openlca-ipc](https://github.com/dernestbank/openlca-ipc) | Python library for openLCA IPC |
| [openlca-mcp](https://github.com/dernestbank/openlca-mcp) | MCP server for AI assistants |
| [openlca-cli](https://github.com/dernestbank/openlca-cli) | CLI for openLCA IPC |

## License

MIT

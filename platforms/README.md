# Platform overlays and distributions

The canonical `skills/` tree follows the open Agent Skills specification and remains host-neutral. Host-specific behavior is added only during deterministic packaging.

## Build targets

| Target | Source behavior added | Output |
|---|---|---|
| Portable | none; canonical 28-skill tree | `LCA-Skills-Portable-v0.2.0.zip` |
| Claude Code plugin | hints, explicit-only autopilot, agents, hook, MCP | `LCA-Skills-ClaudeCode-v0.2.0.zip` |
| Standalone Claude Code | unnamespaced copied skills/agents and installers | `LCA-Skills-ClaudeStandalone-v0.2.0.zip` |
| Claude.ai | one portable `lca-expert/` upload with 27 bundled modules | `LCA-Skills-ClaudeAI-v0.2.0.zip` |
| ChatGPT | one portable `lca-expert/` upload with 27 bundled modules | `LCA-Skills-ChatGPT-v0.2.0.zip` |
| Codex | portable skills plus `.codex-plugin/plugin.json` | `LCA-Skills-Codex-v0.2.0.zip` |

`claude-code/skill-overrides.json` is the only source of Claude Code-only skill frontmatter. Canonical skills must never be edited to add those fields.

Build and validate:

```bash
python scripts/build_distributions.py --clean
python scripts/validate_distributions.py
```

Every package contains `bundle-manifest.json` with per-file SHA-256 hashes and an explicit structural-qualification label. Build timestamps are normalized for deterministic ZIP output.

See:

- `docs/platforms/claude-code.md`
- `docs/platforms/claude-ai.md`
- `docs/platforms/chatgpt.md`
- `docs/platforms/codex.md`
- `docs/platforms/host-qualification.md`

# Host qualification commands

Repository checks:

```bash
python scripts/validate_repo.py --strict
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/build_distributions.py --clean
python scripts/validate_distributions.py
python -m lca_tools.cli doctor
```

Claude Code, when installed:

```bash
claude plugin validate ./dist/claude-code/lca-skills --strict
claude --plugin-dir ./dist/claude-code/lca-skills
```

Inside Claude Code, test `/lca-skills:lca-doctor`, the MCP `lca_doctor` tool, one read-only specialist agent, and the post-write validation hook. For standalone skills, copy the built `skills/` folders and invoke `/lca-expert`.

Codex skills are invoked using the host's skill syntax, commonly `$lca-expert`; verify against the installed version rather than assuming command syntax.

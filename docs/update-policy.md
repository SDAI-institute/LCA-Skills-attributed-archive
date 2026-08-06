# Update and compatibility policy

## Why updates are mandatory

Standards status, program rules, databases, LCIA implementations, software APIs, Agent Skills schemas, Claude/OpenAI host behavior, MCP protocol versions, GREET products, and future-background scenarios change. “Current” is therefore a versioned, dated, source-grounded claim.

## Review cadence

- **Monthly:** Claude Code, Claude.ai, ChatGPT/Codex Skills/Plugins, Agent Skills, MCP, openLCA IPC, Brightway, GREET, and repository dependency release notes/issues.
- **Quarterly:** ISO status pages, EC Environmental Footprint guidance/packages, GHG Protocol, TRACI, ecoinvent, Federal LCA Commons/USLCI, major open databases, and LCIA method releases.
- **At every study start:** governing program/PCR/PEFCR/OEFSR/regulatory rules, required database/method/tool versions, and review requirements.
- **Immediately:** material calculation bug, withdrawn/replaced standard, changed characterization factors, provider erratum, security issue, license change, host package schema change, or critical eval failure.

## Update procedure

1. Open an issue naming the source, affected versions, workflows, and risk.
2. Verify the change from a primary/official source.
3. Record previous/new status, publication/effective dates, and transition rules.
4. Update `docs/source-register.md` and relevant skill/reference/platform/runtime documentation.
5. Add or amend a behavioral eval that fails under the obsolete behavior.
6. Add deterministic tests when contracts/code change.
7. Rebuild all six distributions and regenerate qualification evidence.
8. Update `CHANGELOG.md` and version according to impact.
9. Retain narrower qualification statuses until host/scientific tests are rerun.

## Versioning

- **Patch:** wording/link fixes, non-behavioral clarifications, compatible examples, source-status corrections that do not change contracts.
- **Minor:** new skill/agent/tool, backward-compatible artifact fields, new gate/check, updated host/tool behavior with preserved contracts.
- **Major:** renamed/removed skills, changed workspace artifact contracts requiring migration, changed invocation/build architecture, or materially changed methodological defaults.

Every canonical skill metadata version and plugin/package manifest version must match `pyproject.toml`.

## Compatibility matrix

Maintain explicit status by:

- canonical Agent Skills specification date/version;
- Claude Code build and plugin/skill schema;
- Claude.ai upload behavior;
- ChatGPT/Codex skill/plugin surface;
- MCP protocol version;
- Python version;
- openLCA desktop/server plus `olca_ipc`/`olca_schema`;
- Brightway package set;
- GREET product/release/platform;
- database/system model and LCIA package.

Never state “latest compatible” without a dated test.

## Deprecation

Do not silently delete obsolete guidance or fields. Mark them:

- deprecation version/date;
- last valid context;
- replacement path;
- migration instructions;
- removal target if applicable.

Keep a regression eval until no supported workflow relies on the old behavior.

## Source-health labels

- `CURRENT` — primary source checked and applicable.
- `CURRENT_UNDER_REVISION` — current edition remains applicable while a replacement is being developed.
- `TRANSITIONAL` — time-bounded migration or temporary guidance.
- `LEGACY` — retained only to reproduce historical studies.
- `VERIFY_PER_PROGRAM` — governing program/client/regulator controls.
- `UNKNOWN` — must not support formal conclusions until verified.

## Qualification expiry

Host/tool evidence expires when a retest trigger occurs. A previous passing report may remain historical evidence but cannot be silently carried forward to a changed version set. Update the qualification record with `expired`, reason, and replacement test status.

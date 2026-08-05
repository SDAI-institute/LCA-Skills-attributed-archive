---
name: lca-compound
description: "Capture a validated LCA modeling lesson, tool fix, dataset mapping, review finding, or sector convention as reusable repository knowledge. Use after a problem is solved and verified so future studies can retrieve the reasoning and prevention checks."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---
# Compound LCA Knowledge

Turn validated project work into reusable institutional knowledge without leaking confidential or licensed content.

## Eligibility gate

Compound only when:

- the issue and root cause are understood;
- the fix has validation evidence;
- the lesson generalizes beyond one chat;
- confidential data can be removed;
- no restricted dataset rows or standard text are required.

Do not compound speculative conclusions or unresolved modeling debates as facts.

## Procedure

1. Search `knowledge/solutions/` for an existing entry and use `references/solution-template.md`.
2. Create or update a concise markdown file named `<domain>-<problem>.md`.
3. Include:
   - context and symptoms;
   - why the issue was hard;
   - root cause;
   - resolution and decision logic;
   - validation evidence;
   - affected tools/databases/method versions;
   - limits and counterexamples;
   - prevention or automated check;
   - sources and date.
4. Generalize names and values; preserve technical meaning.
5. Add or update an eval case if the lesson should change agent behavior.
6. Run repository validation and tests.

## Promotion rule

Promote a solution into a skill reference only after it recurs, is strongly source-backed, or closes a material quality gap. Record the change in `CHANGELOG.md`.

## Deliverable

Return the knowledge file path, validation performed, and any skill/eval updates. Keep the original study decision log as the authoritative case record.

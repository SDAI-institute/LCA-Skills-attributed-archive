# GREET automation

## Preferred hierarchy

1. Official supported export/batch/plugin interfaces for the installed release.
2. .NET plugin API using current interfaces and examples.
3. Controlled workbook automation only for releases/modules explicitly designed for it.
4. UI automation as a last resort with strong validation.

## Plugin API

The GREET site documents a .NET plugin lifecycle and access to model/controller objects, but examples can be release-specific. Resolve DLLs and interfaces from the installed release; do not copy old 2016 references uncritically.

## Workbook automation

Avoid raw cell addresses when named ranges/tables or documented interfaces exist. Macro-enabled files are untrusted inputs; use protected copies and checksum outputs. Excel recalc/settings can affect results.

## Validation

For every automated run compare one scenario with a manual GUI result, including pathway, units, boundary, totals, and stage contributions. Fail closed on missing entities or changed labels.

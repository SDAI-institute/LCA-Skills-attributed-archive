# Release manifest

Every released result should resolve to a machine-readable manifest.

## Required fields

- study ID, title, release ID, status, date, owner, reviewers;
- intended use/audience and confidentiality;
- functional unit/reference flow;
- boundary and modeling approach;
- scenario and parameter set;
- software/package versions;
- database names, versions, system models, licenses;
- LCIA method/category versions;
- model/project/product-system identifiers;
- calculation settings, allocation, cutoffs, normalization/weighting;
- source-control commit or archive hash;
- raw result file hashes and processing script hashes;
- unresolved assumptions and limitations;
- review status and claim authorization.

## Release rule

A plot or table without the manifest ID is draft. Recalculations create a new release ID. Do not overwrite previously released files; supersede them with an explicit link and reason.

# Current database and method errata gate

**Status date:** 2026-08-07

Use this file as a dated screening gate, not as a permanent substitute for the provider's current release notes, known-issues page, method repository, or corrected files. Recheck official sources before every decision-use model, public comparison, EPD/PCF release, regulatory filing, or database upgrade.

## Mandatory pre-use check

For each background database and LCIA package:

1. record release, system model, format, provider, access date, and checksum where permitted;
2. review the release notes, known issues, corrections, and method implementation notes;
3. identify whether the affected dataset, system model, elementary flow, or impact category is used;
4. apply only provider-authorized corrections or a clearly documented local patch;
5. preserve the unmodified source, patch script, rationale, before/after result, and sensitivity;
6. do not silently repair licensed data or redistribute corrected unit-process content;
7. block release when the provider advises that a result should not be used.

## ecoinvent 3.12 known issues at the status date

The official ecoinvent 3.12 release page lists the following material issues. Revalidate this list because the provider can publish corrections or a newer release.

### Cut-off Ecological Scarcity 2021 biotic-resource results

Numerical instability affected two Ecological Scarcity 2021 biotic-resource categories in the **cut-off** system model. The provider advises users not to use those category results until corrected. Treat use of either affected category as a release blocker rather than averaging, suppressing, or explaining away the score.

### Australian cereal biogenic-carbon assignment

Several Australian cereal datasets contain a carbon imbalance caused by an incorrect elementary-flow assignment for embodied biogenic carbon. Use the provider's correction file or a newer corrected release, preserve the patch provenance, and rerun carbon-balance and climate-result checks. Do not generalize the correction to other crops or geographies without evidence.

### Consequential aluminium cast-alloy market

The global consequential market for aluminium cast alloy is reported with a 1 kg reference output but only 0.312 kg of aluminium input. The provider advises manual mass-balance correction pending the next release. Any study using this dataset must either apply and document the provider-directed correction, use a validated alternative, or stop the release.

### Tiny non-zero waste-market scores

Three waste markets can show extremely small non-zero scores where zero is expected because of numerical solver artifacts. These values are reported as negligible, but the model should still identify them as numerical noise rather than a physical burden. Never use them to support a comparative claim or to infer a new emission pathway.

## LCIA implementation gate

ecoinvent directs users to its LCIA implementation repository for current method issues. Independently verify the exact method implementation packaged in openLCA, Brightway, SimaPro, Sphera, or another tool; identical method family names do not guarantee identical elementary-flow mappings or characterization factors.

## Required study record

Add an entry to `decision-log.md` and `data-register.csv` containing:

- issue source and access date;
- affected database release/system model/dataset or method;
- applicability decision;
- correction, exclusion, or release block;
- responsible reviewer;
- before/after or sensitivity result;
- residual uncertainty and recheck trigger.

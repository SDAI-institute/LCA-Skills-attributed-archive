# Goal and scope — Synthetic electrolytic hydrogen screening example

**Study ID:** `synthetic-hydrogen-screening`  
**Status:** `INVENTORY_READY`  
**Use restriction:** Training and regression example only. No impact factors or decision-use results are provided.

## Intended application and audience

Demonstrate the LCA Skills workspace, physical inventory closure, source labeling, scenario registration, and release controls. The audience is plugin maintainers. The model must not support procurement, policy, marketing, an EPD, a product carbon footprint, or a public comparison.

## Function, functional unit, and reference flow

- Function: produce hydrogen by water electrolysis.
- Functional unit: **1 kg hydrogen at the electrolyzer outlet, 99.9% purity**.
- Reference flow: 1 kg hydrogen.
- Compression, storage pressure, reliability, and delivery are excluded, so comparisons requiring those services are invalid.

## Boundary and approach

- Attributional cradle-to-gate screening.
- Included: deionized water production, example electricity supply, and foreground electrolysis.
- Excluded: electrolyzer manufacture, compression, storage, distribution, use, and end of life. These exclusions are acceptable only for this artifact demonstration.
- Example Region and illustrative 2026 scenario; all operational numbers marked `SCENARIO` or `CALCULATED`.

## Multifunctionality

Oxygen is physically produced but receives no credit in the baseline because marketability, purity, compression, demand, and displacement are unspecified. A future oxygen-use case must be a separately documented scenario; it may not be added as an automatic avoided-product credit.

## Inventory and quality requirements

- Close water-to-hydrogen-plus-oxygen mass balance within 1%.
- Use a separate parameter for electricity intensity.
- Keep all example values synthetic and openly redistributable.
- Select actual background datasets, database/system model, LCIA method, geography, and uncertainty only in a real study.

## Review and reporting

Internal regression check only. Status cannot advance to `CALCULATED` because no LCIA calculation has been performed.

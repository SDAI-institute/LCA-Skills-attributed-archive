# LCA routing map

Use the narrowest skill that can complete the task, but retain the orchestrator quality gates.

| Need | Primary skill | Supporting skills |
|---|---|---|
| New full study | `lca-expert` | all as routed |
| Goal, function, boundary, comparison | `lca-scope` | `lca-sector`, `lca-epd-pcf` |
| Process flows, direct emissions, balances | `lca-inventory` | `lca-sector`, `lca-data` |
| Database choice, dataset fit, mapping | `lca-data` | selected tool skill |
| Impact method/categories/factors | `lca-impact` | `lca-epd-pcf` where rules apply |
| Results, hotspots, sensitivity, uncertainty | `lca-interpret` | selected tool skill |
| Model/report audit | `lca-review` | all relevant specialists |
| Report or external communication | `lca-report` | `lca-review` |
| openLCA | `lca-openlca` | methodology skills still govern |
| Brightway | `lca-brightway` | methodology skills still govern |
| R&D GREET | `lca-greet` | `lca-sector`, `lca-impact` |
| Future technology, policy, marginal response | `lca-prospective` | tool and sector skills |
| PCF, EPD, PEF, PCR | `lca-epd-pcf` | `lca-scope`, `lca-review` |
| Organizational or social life cycle | `lca-organization-social` | `lca-data`, `lca-review` |
| Evidence gap/current source | `lca-research` | requesting skill |
| Reusable validated lesson | `lca-compound` | eval update |

## Tool selection heuristic

- **openLCA:** transparent GUI modeling, broad format/database support, projects, product systems, client collaboration, IPC automation.
- **Brightway:** research-grade Python control, custom matrices, large scenario sets, prospective/dynamic methods, reproducible code.
- **R&D GREET:** U.S.-oriented fuel/vehicle/energy technology pathways and official Argonne assumptions/modules.
- **EEIO/USEEIO/EXIOBASE:** spend/sector screening, organizational hotspots, truncation completion, hybrid models.
- **Commercial/program tools:** use when client/program compatibility, licensed data, verification ecosystem, or organizational workflow requires them; preserve methodology outside the GUI.

Tool choice never resolves methodological choices automatically.

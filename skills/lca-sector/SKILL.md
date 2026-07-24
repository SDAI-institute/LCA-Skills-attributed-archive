---
name: lca-sector
description: "Load sector-specific LCA knowledge, process conventions, direct-emission models, functional units, datasets, and red flags. Use for energy/fuels, chemicals/bioprocesses, metals/materials/batteries, manufacturing/electronics, buildings, transport, agriculture/food, water, waste/recycling, or circular-economy studies."
license: MIT
compatibility: "Portable Agent Skills instructions. Python 3.10+ is required only for bundled validators and adapters; openLCA, Brightway, GREET, standards, and databases require separately installed or licensed software and data."
metadata:
  author: SDAI Lab
  version: "0.2.0"
---
# Sector Knowledge Router

Sector knowledge changes what “complete” means. Select every applicable module; many systems span more than one.

## Routing

- Energy, power, hydrogen, fuels, CCS: `references/energy-fuels.md`
- Chemicals, refining, polymers, biotech, bioprocesses: `references/chemicals-bioprocesses.md`
- Metals, minerals, cement, materials, batteries: `references/materials-batteries.md`
- Manufacturing, machinery, electronics, semiconductors: `references/manufacturing-electronics.md`
- Buildings, construction products, infrastructure: `references/buildings-construction.md`
- Passenger/freight transport and logistics: `references/transport.md`
- Agriculture, forestry, food, bio-based systems: `references/agriculture-food.md`
- Water supply, treatment, wastewater, desalination: `references/water-systems.md`
- Waste, recycling, recovery, circular systems: `references/waste-circularity.md`

## Sector specialist pass

For the selected module:

1. Confirm the performance-based functional unit and quality constraints.
2. Identify life-cycle stages and processes that commonly dominate.
3. Identify direct emissions/resources not captured by purchase records.
4. Identify operating state, capacity factor, lifetime, yield, degradation, and maintenance parameters.
5. Identify co-products, wastes, recycling, land/use change, or substitution conventions.
6. Select sector-appropriate primary data and official factors.
7. Add sector red flags to the QA checklist.
8. Test at least one sector-specific conservation or benchmark relation.

## Boundary discipline

Do not let sector modules override the frozen goal and scope. When a sector convention conflicts with a program rule or study purpose, document the conflict and route back to `lca-scope`.

## Deliverable

Create a sector modeling memo with required processes, parameters, data sources, direct-emission equations, benchmark ranges, and QA tests. Link each item to the inventory and assumptions registers.

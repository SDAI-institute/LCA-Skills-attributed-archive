# Manufacturing, machinery, electronics, and semiconductors

## Functional unit

Define the service delivered, throughput, precision, uptime, lifetime, repairability, duty cycle, and replacement. For electronics include compute/storage/network function where devices differ materially.

## Inventory

Include bill of materials, purchased components, fabrication yield and scrap, machining/forming energy, heat treatment, coatings/plating, cleanroom/HVAC, compressed air, process gases, ultrapure water, solvents, packaging, logistics, capital equipment when material, standby energy, maintenance, consumables, software-enabled utilization effects, repair/refurbishment, and end of life.

Semiconductor inventories need wafer size/node, die area, dies per wafer, yield, fab electricity/water, fluorinated gases and abatement, deposition/etch/clean steps, packaging, testing, and allocation across products. Use supplier data or transparent proxies; generic “electronics” datasets can conceal orders-of-magnitude differences.

## Checks

- bill-of-material mass reconciles with finished product plus scrap;
- yield is applied once, at the correct production step;
- recycled scrap loops do not create burden-free material;
- facility energy is allocated using causal drivers where possible;
- use-phase energy uses realistic workload and grid, including idle/standby;
- lifetime extension assumptions include repair parts and performance obsolescence;
- data centers and AI workloads need system boundary across compute, cooling, networking, utilization, and hardware turnover.

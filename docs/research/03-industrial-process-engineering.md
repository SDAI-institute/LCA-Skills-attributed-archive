# Industrial process engineering research notes

## Why this layer is essential

Foreground LCI quality is often limited less by LCA software than by incomplete process understanding. Purchase records miss reaction emissions, losses, recycles, utilities, and waste transformations; laboratory recipes do not scale linearly; database proxies can violate mass or energy conservation.

The skill therefore needs a process-engineering mode.

## 1. Define process basis

Record product amount and specification, operating period, capacity, capacity factor, batch/continuous operation, geography, technology vintage, steady/transient state, allocation period, and data reconciliation period. Convert every source to a common basis before linking processes.

## 2. Build the process map

Represent unit operations, feeds, intermediates, recycles, purges, products, co-products, emissions, wastes, and utilities. Mark measurement/model/source ownership and boundary crossings. Separate foreground control from background provider datasets.

## 3. Material and elemental balances

At minimum:

- total mass by process and plant;
- components for key materials;
- carbon for fuels, organics, biogenic systems, and CCS;
- hydrogen/oxygen where water or hydrogen matters;
- nitrogen for agriculture, fermentation, wastewater, and N2O/NH3/NOx;
- sulfur/halogens/metals for direct emissions and hazardous residues.

Use reaction stoichiometry and conversion/selectivity/yield definitions consistently. Distinguish wet/dry, solution/solute, pure/technical grade, standard/actual volume, mass/molar basis.

A closure gap triggers investigation of accumulation, measurement error, moisture, unmeasured purge, venting, sampling, or inconsistent periods. It is not repaired by arbitrary normalization.

## 4. Energy balances and utilities

Inventory electricity, fuels, process heat by temperature/pressure level, cooling, refrigeration, compressed air, vacuum, pumping, agitation, separation work, steam generation/condensate, heat recovery, and onsite generation.

Check:

- efficiency definitions and HHV/LHV;
- heat duty against phase change/reaction/separation needs;
- boiler/CHP allocation and exported energy;
- pump/compressor work against flow/head/pressure/efficiency;
- annual energy against runtime and load;
- heat integration does not erase required temperature driving force or auxiliary loads.

## 5. Reactions, yield, and separations

Track limiting reactant, excess reagent, conversion, selectivity, isolated yield, recovery, recycle, purge, solvent loss, catalyst life, adsorbent/media replacement, concentration, and product purity. A chain yield is the product of step recoveries only when bases are consistent.

Separation modeling should include phase equilibrium/feasibility, reflux or solvent ratio, evaporation/distillation duty, membrane recovery/rejection, drying, crystallization, extraction, filtration/centrifugation, and wastewater/off-gas treatment.

## 6. Direct emissions

Model direct flows from:

- reaction chemistry and carbon/element balances;
- combustion and process heaters;
- venting, flaring, blowdown, storage, loading, and fugitive leaks;
- VOC/solvent losses;
- refrigerants and fire suppressants;
- process N2O, CH4, CO, NOx, SOx, particulates, acid gases;
- wastewater COD/BOD, N/P, metals, salts, temperature;
- solid residues, catalysts, filters, sludge, ash, tailings, slag;
- land-use/soil/biological processes where relevant.

Permitted limits are not necessarily actual emissions; non-detect is not zero; treatment removal transfers mass to another medium or residue.

## 7. Infrastructure, lifetime, and maintenance

Include buildings, reactors, tanks, pipelines, equipment, catalysts, membranes, batteries, replacement parts, maintenance, and decommissioning when material to the goal. Annualize by actual lifetime/output, not nameplate life alone. Include capacity factor, degradation, replacement count, and utilization.

Infrastructure is often immaterial for high-throughput fossil processes but can dominate low-utilization pilots, renewables, storage, or emerging plants. Test before excluding.

## 8. Scale-up

For laboratory/pilot technologies:

- separate fixed experimental overhead from scalable process need;
- replace lab solvent/water/excess reagent with engineered recovery scenarios;
- include industrial separation and emissions control;
- model commercial purity, productivity, capacity factor, and reliability;
- account for off-spec batches/startup/shutdown;
- compare both emerging and incumbent systems in the same future context;
- use conservative/central/advanced scenarios and break-even thresholds.

## 9. Data reconciliation and uncertainty

Prioritize metered primary data, then design/simulation, equipment specs, permits, official statistics, transparent literature, databases, and proxies. Reconcile inconsistent measurements with documented equations and uncertainty rather than silently choosing the convenient value.

Correlated parameters must remain correlated: yield and waste, recovery and energy, grid mix components, product/co-product quantities, composition shares, and price allocation factors. Independent Monte Carlo sampling can create impossible plants.

## 10. Process-LCA coupling

For Aspen/HYSYS/ChemCAD/BioSTEAM/QSDsan/other simulators, export a versioned stream and utility table with component IDs, units, reference conditions, scenario, convergence status, and checksum. Map simulation species to LCA product and elementary flows through a reviewed mapping table. Keep simulation thermodynamics and LCA boundary assumptions separate.

## 11. Minimum engineering QA

Before LCIA:

- reference flow and production amount reconcile;
- mass/component/element closures meet defined tolerance;
- energy generation and consumption signs are consistent;
- yields, recycles, and purges are not applied twice;
- units and standard conditions are explicit;
- direct emissions have causal calculations or defensible factors;
- wastes have treatment providers and residual fates;
- utility levels and efficiencies are plausible;
- co-product and recycling logic is singular and documented;
- results are within plausible intensity ranges or explained.

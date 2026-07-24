# Energy, fuels, hydrogen, and carbon management

## Functional units

Use delivered service: kWh or MWh of electricity at a defined voltage/location; MJ of useful heat at temperature; MJ fuel lower/upper heating value; vehicle-km or tonne-km; kg H2 at pressure/purity/location; tonne CO2 durably stored for a specified permanence period. Record HHV/LHV and conversion basis.

## Required modeling

- upstream extraction, processing, methane leakage, flaring and venting;
- plant efficiency at representative load, startup/shutdown, capacity factor, lifetime;
- auxiliary loads, transmission/distribution, compression, storage, boil-off, conditioning;
- construction and replacement when material;
- combustion stoichiometry and non-CO2 emissions;
- grid mix appropriate to decision: average, contractual, residual, or marginal;
- temporal correlation for variable electricity where relevant;
- hydrogen production, water, compression/liquefaction, delivery, leakage and end use;
- CO2 capture energy/material penalty, transport, injection, leakage, monitoring, permanence and counterfactual.

## Checks

- reconcile energy input/output and efficiency on a common HHV/LHV basis;
- check annual production = capacity × capacity factor × time;
- check carbon in feed against CO2/CO/CH4/products/residues;
- distinguish biogenic and fossil carbon;
- report gross generation and delivered electricity separately;
- do not treat renewable certificates as physical marginal supply without the selected accounting rule;
- do not call captured fossil CO2 a negative emission.

GREET is often useful for fuel/vehicle pathways; process LCA tools are often better for customized plants. Preserve boundary and basis when transferring results.

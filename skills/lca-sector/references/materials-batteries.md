# Metals, minerals, cement, materials, and batteries

## Functional unit

Specify grade, composition, form, mechanical/electrical/thermal performance, recycled content, location, and service life. For batteries use delivered energy or service (for example kWh throughput at defined depth of discharge, efficiency, lifetime, climate, and duty cycle), not only kg or nominal kWh.

## Required stages

Mining/ore grade, beneficiation, concentration, smelting/refining, reagents, tailings, slag/residue, energy source, water, direct process emissions, forming/finishing, scrap loops, use-phase effects, collection, reuse/second life, recycling, and final disposal.

Cement/concrete models require clinker ratio, kiln fuel and efficiency, calcination CO2, supplementary cementitious materials, carbonation boundary/timing, strength class, mix design, curing, transport, construction loss, service life, and demolition/recycling.

Battery models require active-material chemistry, precursor route, cell format, electrode loading/yield, dry-room energy, formation cycling, pack/BMS/thermal system, production scrap, usable capacity, degradation, replacement, charging losses, electricity profile, safety-driven design, collection and recycling route.

## Checks

- ore grade and recovery imply plausible mined mass;
- metal content is conserved through products, scrap, slag, tailings, and emissions;
- recycled content and end-of-life credits are not double counted;
- production yield losses loop only when physically recovered;
- compare equal lifetime service, not nameplate capacity;
- critical-mineral supply and future recycling assumptions are scenario explicit;
- negative recycling results do not conceal large gross burdens.

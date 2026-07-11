# Reproducible data extraction

For every extracted value preserve the chain from source to model.

## Required fields

- source ID, full citation, stable identifier/URL, access date;
- table/figure/page/section or API query;
- quoted label (minimal), value, unit, uncertainty/range;
- numerator/denominator and reference flow;
- dry/wet, mass/molar/volume, HHV/LHV, standard conditions;
- technology, scale, location, year, operating state;
- system boundary and included/excluded processes;
- allocation/substitution/recycling treatment;
- transformation formula and unit conversion;
- final parameter name, value, unit, scenario/distribution;
- reviewer and validation status;
- license/confidentiality restrictions.

## Extraction rules

1. Extract surrounding definitions before the number.
2. Recalculate unit conversions independently.
3. Preserve significant digits from evidence but use practical reporting precision.
4. Do not digitize a chart when a table or data file exists.
5. Do not average values with incompatible boundaries; first normalize or model differences.
6. Treat “not detected,” zero, and missing as different states.
7. Capture denominators such as kg product, kg feed, batch, operating hour, or plant-year.
8. Store raw source-derived value and modeled/adjusted value separately.

A parameter without a traceable source or assumption record is provisional.

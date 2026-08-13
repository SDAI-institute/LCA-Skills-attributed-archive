# Synthetic hydrogen study example

This workspace is a **training and regression fixture**, not a real hydrogen LCA. It demonstrates:

- a service-defined functional unit and explicit exclusions;
- source classes and provider candidates;
- a closed foreground mass balance;
- no automatic oxygen co-product credit;
- parameter/scenario registration;
- status discipline: physical inventory ready, LCIA not calculated.

Run:

```bash
python scripts/validate_study.py examples/synthetic-hydrogen-screening
python scripts/check_balance.py examples/synthetic-hydrogen-screening/balances.csv
```

A real study must replace synthetic parameters, select and license background datasets, define geography/time/technology, freeze an LCIA method, quantify uncertainty, and pass review gates.

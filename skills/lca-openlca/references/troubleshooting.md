# openLCA troubleshooting

| Symptom | Likely checks |
|---|---|
| Zero/empty result | reference amount, product system links, method/flow mapping, calculation setup |
| Unexpected huge score | unit property, reference product amount/sign, allocation, duplicate provider, parameter formula |
| Missing upstream | unlinked exchange, provider policy, market/product mismatch |
| Negative score | substitution/waste sign, avoided product, negative elementary flow, allocation/system model |
| IPC connection failure | server started, active database, port, localhost/firewall, client compatibility |
| IPC memory growth | results/simulators not disposed |
| Allocation not changing | factors not recalculated/saved, calculation allocation setting, formula/parameter scope |
| Import duplicates | flow/method mapping, database merge strategy, format loss |
| GUI/API mismatch | different active database, UUID, amount, method, parameters, allocation, version |

Always reproduce in a minimal model before modifying a production database.

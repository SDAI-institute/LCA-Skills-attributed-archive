# Gate dependencies

```text
Intake -> Goal/scope -> Data/model plan -> Inventory construction -> Inventory QA
       -> Calculation identity -> LCIA -> Interpretation -> Review -> Corrections
       -> Recalculation/validation -> Report/claims -> Release candidate -> Handoff
```

Parallel work is safe only when it does not depend on an unresolved upstream choice. Literature research, supplier data requests, and tool-environment setup can often run in parallel after the decision and preliminary function are known. Allocation implementation, method selection, and comparisons cannot be frozen independently of scope.

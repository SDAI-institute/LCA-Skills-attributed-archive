# Autopilot stage contract

Each stage returns a receipt before the next begins:

```text
stage | status | inputs | outputs | checks | decisions | blockers | next stage
```

The pipeline is plan-first and gate-driven. A failed gate routes backward to the skill responsible for the defect, not forward with a disclaimer. Model-affecting fixes trigger recalculation and re-review of affected conclusions.

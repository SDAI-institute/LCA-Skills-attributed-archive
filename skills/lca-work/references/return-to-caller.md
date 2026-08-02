# Return-to-caller contract

A child workflow returns control when its assigned task batch is complete or blocked. It must not silently begin the next methodological stage.

Return:

- status and completed task IDs;
- evidence and artifacts;
- exact failed gate or new decision;
- residual risk and uncertainty;
- recommended next skill/task;
- whether recalculation or reviewer recheck is required.

This contract prevents an implementation agent from redefining scope or approving its own review findings.

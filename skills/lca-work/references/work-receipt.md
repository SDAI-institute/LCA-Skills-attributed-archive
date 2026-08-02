# Work receipt

Machine-readable receipt fields:

```json
{
  "receipt_version": "1.0",
  "study_id": "...",
  "plan_revision": "...",
  "task_ids": ["..."],
  "status": "completed|partial|blocked|failed",
  "changes": [],
  "commands_or_tools": [],
  "checks": [],
  "decisions": [],
  "assumptions_added": [],
  "before_after_metrics": [],
  "artifacts": [],
  "open_findings": [],
  "next_gate": "...",
  "next_action": "..."
}
```

Every path or model object needs a stable identity. Every check includes command/method, timestamp, outcome, and evidence path.

# Finding schema

```json
{
  "finding_id": "REV-...",
  "persona": "...",
  "severity": "CRITICAL|MAJOR|MINOR|OBSERVATION|QUESTION",
  "confidence": "high|medium|low",
  "title": "...",
  "requirement_or_test": "...",
  "evidence": [{"artifact": "...", "location": "...", "detail": "..."}],
  "reasoning": "...",
  "potential_influence": "...",
  "recommended_action": "...",
  "verification": "...",
  "status": "open"
}
```

Severity is based on influence on model validity, conclusion, claim, reproducibility, or required process—not stylistic preference. Findings without evidence are questions, not defects.

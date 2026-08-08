# LCA Skills behavioral evaluations

These evaluations test whether the plugin behaves like a careful senior LCA practitioner rather than a fluent calculator. They are model- and host-agnostic: run each prompt with the indicated skill available, capture the response and artifacts, then score against `rubric.md` and the case-specific expectations.

## Recommended execution modes

1. **Cold route:** expose all skill metadata and issue the prompt without naming a skill. Test routing.
2. **Direct skill:** invoke the expected skill explicitly. Test procedural execution.
3. **Artifact mode:** provide a synthetic study workspace and allow file/script tools. Test durable outputs and deterministic checks.
4. **Adversarial follow-up:** pressure the agent to skip review, hide uncertainty, reuse restricted data, or make a stronger claim. Test refusal and correction.
5. **Version drift:** change a tool/database/method version in the prompt. Test verification rather than memorized commands.

## Pass criteria

- No critical-fail condition in `rubric.md`.
- At least 85/100 for a world-class pass.
- All case-specific `must_detect`, `must_do`, and `must_not` conditions satisfied.
- Any calculation is dimensionally traceable and clearly labeled as performed, estimated, or not executed.
- Required artifacts are created or explicitly specified when the runtime cannot create them.

## Evaluation records

For each run, preserve:

- model/runtime and skill/plugin commit;
- prompt and supplied files;
- tool calls and execution logs;
- response and generated artifacts;
- rubric scores and critical failures;
- reviewer notes and regression issue;
- date and source-register status.

Behavior-changing fixes should add or strengthen an eval before release.

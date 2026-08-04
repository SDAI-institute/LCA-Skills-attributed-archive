# Resume protocol

On resume:

1. verify path, branch/revision, study ID, and hashes;
2. inspect status and current gate in `study.yaml` and the plan;
3. re-run `lca-doctor` when the environment may have changed;
4. re-run the last gate validator if inputs or software changed;
5. inspect open findings, assumptions, and data requests;
6. perform the exact next action or return a new blocker;
7. update the handoff before another pause.

Never infer completion from an old chat statement when the durable artifact disagrees.

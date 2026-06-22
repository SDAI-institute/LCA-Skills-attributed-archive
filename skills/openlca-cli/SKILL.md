Use the `openlca` CLI to inspect and validate openLCA database contents without writing Python scripts.

Expectations:
- Check connection with `openlca status` before issuing any other commands.
- Use `--json` flag when piping output to scripts or downstream tools.
- Prefer searching before referencing a UUID directly.

Useful commands:
- `openlca status` — verify IPC connection
- `openlca db` — show active database name
- `openlca flows search "<terms>"` — find flows by keyword
- `openlca flows get <uuid>` — inspect a flow
- `openlca processes search "<terms>"` — find processes
- `openlca systems search "<terms>"` — find product systems
- `openlca methods list` — list all impact methods
- `openlca calc run <system-uuid> <method-uuid>` — run LCIA calculation
- `openlca calc run <system-uuid> <method-uuid> --top 5` — with process contributions

Environment variables:
- `OPENLCA_HOST` — IPC host (default `localhost`)
- `OPENLCA_PORT` — IPC port (default `8080`)

Agent guidance:
- Use this skill to confirm which systems and methods are available before proposing a calculation plan.
- Pass `--json` output to downstream parsing steps.
- Do not use the CLI to create or modify data — use openlca-ipc (Python) for writes.

Use `openlca_ipc.OLCAClient` as the first-choice modeling bridge when openLCA desktop and its IPC server are available.

Expectations:
- Verify the IPC connection before planning downstream tasks.
- Search for flows, processes, providers, and impact methods before creating new data.
- Keep providers attached to product inputs unless a flow is elementary.
- Dispose calculation results after extracting impact or contribution outputs.

Useful package patterns:
- `client.search.find_flows(...)`, `find_processes(...)`, `find_impact_method(...)`
- `client.search.find_best_provider(flow)`
- `client.data.create_product_flow(...)`, `create_exchange(...)`, `create_process(...)`
- `client.systems.create_product_system(process)`
- `client.calculate.simple_calculation(system, method)`
- `client.results.get_total_impacts(result)`
- `client.contributions.get_top_contributors(result, category, n=5)`

Agent guidance:
- In goal and scope work, use openLCA database availability to constrain realistic system boundaries and methods.
- In inventory work, produce unit-process-ready exchange lists with amounts, units, and provider expectations.
- In LCIA work, prefer method names that are available in the database rather than abstract method labels.
- In interpretation work, call out when contribution analysis or uncertainty runs are needed to support conclusions.

Use SwolfPy when the study models municipal solid waste management systems with collection, treatment, and disposal processes.

Expectations:
- Keep project names, functional units, and LCIA method tuples explicit.
- Waste-fraction parameters must sum to 1 per source process.
- Use `create_project(template="lf_wte_basic")` for a quick LF+WTE demo system.
- Run LCA before contribution analysis; pass `lca_result_id` to interpretation tools.
- Call `dispose_result` when finished with stored handles.

Typical MCP workflow:
1. `health_check` — confirm SwolfPy/Brightway imports
2. `create_project` — build MSW system (template or JSON spec)
3. `update_parameters` — set waste routing fractions
4. `run_lca` — calculate impacts; note `lca_result_id`
5. `contribution_analysis` — top processes or emissions
6. `run_monte_carlo` or `optimize` — uncertainty / scenario optimization
7. `dispose_result` — free server memory

Agent guidance:
- In inventory work, specify treatment processes (LF, WTE, AD, etc.) and accepted waste streams.
- In LCIA work, record the exact Brightway method tuple (e.g. IPCC 2013 GWP 100a).
- In interpretation work, use comparative LCA and Monte Carlo for policy scenario analysis.
- SwolfPy runs on Python 3.9 in a dedicated conda environment with graphviz.

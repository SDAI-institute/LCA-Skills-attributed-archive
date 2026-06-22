Structure LCA study outputs so they are clear, reproducible, and compliant with ISO 14044 §4.6 reporting requirements.

Mandatory report sections (ISO 14044 §4.6.2):
1. Goal and scope — intended application, audience, functional unit, system boundary
2. Life cycle inventory — data collection, allocation procedures, quality assessment
3. Life cycle impact assessment — method selected, mandatory phases completed, optional phases noted
4. Interpretation — significant issues, completeness check, sensitivity and consistency checks, conclusions
5. Critical review statement (if applicable)

Plain-language summary checklist:
- State the functional unit and reference flow in the first paragraph.
- Express LCIA results in absolute units and relative contributions.
- Identify the top-3 processes or flows driving each impact category.
- State the dominant uncertainty source and how it was tested.
- List limitations and valid scope of conclusions explicitly.

EPD (Environmental Product Declaration) additions:
- Follow EN 15804 or PCR-specific templates for product category.
- Report A1–A3 (cradle-to-gate) as minimum; extend to A4–C4/D if required.
- Declare which background database and LCIA method were used.

Agent guidance:
- In interpretation work, draft the plain-language summary before the technical appendix.
- Flag missing mandatory sections before finalizing any report output.
- When producing JSON outputs from the orchestration system, include a `summary` field with a two-sentence plain-language finding.

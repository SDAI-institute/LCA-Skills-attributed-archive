Use the openlca-mcp server when the LCA session is driven by an AI assistant that supports MCP tool calls (Claude Desktop, Cursor, VS Code Copilot).

Expectations:
- The MCP server must be running and reachable before the session starts.
- Tool calls are made by the AI client, not by agent code — this skill documents how to configure and reason about the connection.
- Keep the openLCA IPC server and the MCP server running in parallel.

Transport options:
- **stdio** (default): AI client launches `openlca-mcp` as a subprocess. Low setup, no network exposure.
- **SSE**: MCP server runs as an HTTP service (`TRANSPORT=sse`). Required for remote or Docker-hosted openLCA.

Startup (stdio):
```json
{
  "mcpServers": {
    "openlca": {
      "command": "uvx",
      "args": ["openlca-mcp"],
      "env": { "OPENLCA_PORT": "8080" }
    }
  }
}
```

Startup (SSE — after `docker compose up`):
```json
{
  "mcpServers": {
    "openlca": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

Agent guidance:
- In goal and scope work, confirm which MCP tools are exposed before planning tool call sequences.
- Use the `/health` endpoint to verify the SSE server is up before issuing tool calls.
- Do not assume MCP tools have the same granularity as the Python API — map available tool names before proposing steps.

> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Documentation MCP server

Zep's Documentation MCP server enables coding agents to search and retrieve information from Zep's complete documentation in real-time.

**Server details:**

* URL: `docs-mcp.getzep.com`
* Type: Search-based with HTTP transport
* Capabilities: Real-time documentation search and retrieval

The `/sse` endpoint is deprecated and will be removed soon. Please update to the new `/mcp` endpoint with HTTP transport.

## Setting up the MCP server

Add the HTTP server using the CLI:

```bash
claude mcp add zep-docs --transport http https://docs-mcp.getzep.com/mcp
```

Create `.cursor/mcp.json` in your project or `~/.cursor/mcp.json` globally:

```json
{
  "mcpServers": {
    "zep-docs": {
      "url": "https://docs-mcp.getzep.com/mcp"
    }
  }
}
```

Enable MCP servers in Cursor settings, then add and enable the zep-docs server.

Configure your MCP client with HTTP transport:

```
URL: https://docs-mcp.getzep.com/mcp
```

## Using the MCP server

Once configured, coding agents can automatically:

* Search Zep concepts and features
* Find code examples and tutorials
* Access current API documentation
* Retrieve troubleshooting information
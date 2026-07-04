> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Connecting a client

Available to [Enterprise Plan](https://www.getzep.com/pricing) customers only.

This page is for end users connecting an MCP client to their own memory. If you administer the project, see [Configuring authentication](/memory-mcp-server/authentication) first.

## What you need

* An MCP client that supports remote servers over HTTP and OAuth — Claude, ChatGPT, Cursor, and others.

* The project's MCP endpoint URL, which an administrator provides. It has the form:

  ```
  https://api.getzep.com/v1/projects/{project_id}/mcp
  ```

  The host above is for Zep's managed cloud. BYOC deployments use a different host — use the exact URL your administrator gives you.

* An account with the identity provider your organization uses. You sign in with the same credentials you use elsewhere; Zep never sees your password.

## Connect

You only need the endpoint URL. The client discovers how to authenticate, registers itself, and starts the sign-in flow automatically.

Add the endpoint URL as a remote MCP server.

```bash
claude mcp add zep-memory --transport http https://api.getzep.com/v1/projects/{project_id}/mcp
```

Add the server to `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (per project):

```json
{
  "mcpServers": {
    "zep-memory": {
      "url": "https://api.getzep.com/v1/projects/{project_id}/mcp"
    }
  }
}
```

Add a remote MCP server (Streamable HTTP transport) and paste the endpoint URL. Consult your client's documentation for where remote servers are configured.

The client opens your organization's sign-in page. Authenticate as you normally would.

Zep shows a consent screen naming the client and the access it requests — reading your memory, and writing to it if your administrator allows writes. Approve to finish connecting.

After approval, the client lists Zep's tools and can work with your memory. Sessions are short-lived and renew automatically while your access remains valid.

## What you can do

Your client reads and writes **only your own memory** in this project. Every tool operates on your graph implicitly — you never pass a user or graph identifier, and you cannot reach anyone else's memory or another project.

Read access is always available:

* Search your memory for context relevant to a query — a ready-to-use context block by default, or raw observations, thread summaries, or episodes.
* Get a narrative summary of who you are, drawn from your memory.

Write access is available only when your administrator has enabled writes for the connection. When it is enabled, you can add new memory as text, JSON, or a message. If writes are disabled, the write tool does not appear, and a write attempt is refused.

## Troubleshooting

* **Sign-in does not start or the client reports no authorization server.** The project's connection may be disabled, or your client may be pointed at the wrong URL. Confirm the endpoint with your administrator.
* **You are signed in but cannot connect.** Your identity may not be admitted — your email domain or group may be outside the connection's allowed list, or your user may not exist yet and just-in-time provisioning is off. Ask your administrator to admit you or provision your account.
* **Write tools are missing.** The connection is read-only, or the account-level writes kill switch is engaged. Writes are controlled by your administrator.
* **The connection stops working after a while.** Tokens are short-lived and renew automatically. If renewal fails, your session may have been revoked or the connection disabled; reconnect to sign in again.
> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Debugging

> Debug Zep ingestion and retrieval using debug logs from the Zep dashboard and episode lists, with detailed per-episode processing output.

Zep provides detailed debugging capabilities to help you troubleshoot and optimize your graph operations. Debug logging captures detailed workflow execution logs that can be invaluable for understanding how your data flows through the system.

## Enabling Debug Logging

## Accessing Debug Logs

Debug logs are available from episode lists for both individual users and graph-wide operations.

**Note**: Debug logs are not supported when adding data or messages in batch operations.

## Viewing Debug Logs

To view debug logs for a specific episode:

This will open a detailed view of the workflow execution logs for that specific episode, showing you:

* Step-by-step execution flow
* Processing timestamps
* Error messages and stack traces
* Performance metrics
* Data transformation details

## Best Practices for Debug Logging

* **Enable selectively**: Only enable debug logging when actively troubleshooting to avoid unnecessary overhead
* **Time-limited threads**: Debug logging automatically disables after 60 minutes to prevent performance impact
* **Review promptly**: Review debug logs within 24 hours. Stale debug logs are removed after 24 hours.
# MCP Profiles

## Current Position
Do not add heavy MCP profile machinery yet. Start with a lightweight registry of known MCP servers, owners, logs, and health checks.

## Why
The system already has many moving parts. MCP profiles may help later, but first we need consistent server identity, log paths, and health-review behavior.

## Minimum MCP Registry Fields
For each MCP server, capture:

```yaml
name: example-mcp
owner_agent: rocky-hermes-default
scope: global | project:integribilt | agent:<name>
gateway: MCP Toolkit
transport: stdio | http | sse | unknown
command_or_url: unknown
config_path: unknown
log_paths: []
health_check: unknown
last_checked_at: null
known_issues: []
```

## Agent Rule
Each agent is responsible for checking the MCP logs for the MCP servers it uses and correcting issues when safe. If correction is not safe or requires credentials, create a tool checkin and add/update `compiled/global/OPEN_QUESTIONS.md`.

## When To Add MCP Profiles
Add formal profiles only after we know:
- server names;
- scopes;
- log paths;
- expected tools;
- health checks;
- which agents should see which servers.

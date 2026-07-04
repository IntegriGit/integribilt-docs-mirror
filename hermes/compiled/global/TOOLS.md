# Global Tools Registry

## Purpose
Track which tools agents use, what they are for, where they fail, and what should be improved.

## Checkout Required For
- Google Drive / shared-drive searches
- Legal/financial document extraction
- Bankruptcy/foreclosure report generation
- Calls/SMS/telephony actions
- Any tool that mutates files, repo state, cloud resources, or agent configuration
- Any long-running harvester/indexer/maintenance task

## Current Known Tools

### Hermes
- Role: primary orchestration agent, skills, cron, gateway, session search, file/terminal/browser tools.
- Notes: Google Workspace auth currently blocks direct Drive access.

### Honcho
- Role: active peer/state memory.
- Notes: use for user/agent preferences, behavior, durable conclusions, current state.

### Neo4j
- Role: relationship graph for entities, claims, agents, tools, documents, projects.
- Notes: endpoint/config still needs to be registered.

### Redis
- Role: optional hot cache / speed layer.
- Notes: do not treat cache as final truth; all entries need source refs and freshness.

### Antigravity Storage Manager
- Role: network artifact/chat collection from Antigravity IDEs and Google Drive.
- Notes: effectiveness with Antigravity 2.0 needs verification. Drive folder is `AntigravitySync`. ASM also has an MCP server connection path.

### MCP Toolkit
- Role: MCP Gateway.
- Notes: agents must check MCP server logs for MCP servers they use and correct safe issues.

### LiteLLM
- Role: skill and plugin gateway.
- Notes: do not treat as durable brain unless evals prove a specific role.

### Zapier
- Role: experimental skill gateway.
- Notes: testing only until reliability/security/evals are proven.

## Tool Review Rule
After significant tool use, create a review under `reviews/tool-checkins/` using the template.

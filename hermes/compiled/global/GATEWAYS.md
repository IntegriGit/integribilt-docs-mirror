# Gateway Roles

## Purpose
Clarify which system acts as which gateway so agents do not confuse MCP/tool/plugin/skill paths.

## Current Gateway Assignments

### MCP Toolkit
- Role: MCP Gateway.
- Config path: `C:/Users/lmiller.INTEGRIBILT/.docker/mcp/`.
- Key files: `config.yaml`, `catalog.json`, `registry.yaml`, `catalogs/integribilt.yaml`, `mcp-toolkit.db`.
- Responsibility: broker/manage MCP server access.
- Agent rule: each agent must check its MCP server logs and correct MCP server issues when safe.

### LiteLLM
- Role: skill and plugin gateway.
- Config path: SVR02 `/srv/core/litellm/config.yaml` (root-owned).
- Config note: file contains base settings such as request timeout, retries, fallbacks, master key, and `store_model_in_db: true`.
- Model/fallback note: models and fallbacks live in the LiteLLM DB, not only in the YAML file.
- Responsibility: route/evaluate skills/plugins and model/tool access patterns where applicable.
- Agent rule: treat LiteLLM as an integration/control plane, not as canonical memory.

### Zapier
- Role: experimental skill gateway.
- Status: testing.
- Agent rule: use for automation experiments only until reliability/security/evals are proven.

### Hermes
- Role: orchestration, cron, skills, memory access, and local agent execution gateway.
- Agent rule: use Hermes cron/skills for scheduled brain maintenance and reusable procedures.

### Memory Gateway / Brain CLI
- Role: Rocky Brain access layer.
- Status: local v0.1 CLI exists; durable gateway is planned.
- Agent rule: agents should prefer one brain access interface over directly guessing across stores.

## Do Not Confuse
- MCP Toolkit is not the durable brain.
- LiteLLM is not the durable brain.
- Zapier is not the durable brain.
- Redis/cache is not the durable brain.
- Git compiled markdown + source-linked indexes coordinate truth.

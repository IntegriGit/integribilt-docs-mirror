# Antigravity Operating Context

## Purpose
Give Antigravity agents and agents reading Antigravity artifacts a shared operating contract.

## Known Topology
- Antigravity Storage Manager (ASM) connects to IDEs and Google Drive.
- The Google Drive sync folder for ASM is named `AntigravitySync`.
- ASM MCP server name: `antigravity-proxy`.
- Product/extension: Antigravity Storage Manager, VS Code extension `unchase.antigravity-storage-manager-0.14.3`.
- MCP transport: stdio.
- MCP command: `node "C:/Users/lmiller.INTEGRIBILT/.vscode/extensions/unchase.antigravity-storage-manager-0.14.3/dist/mcp/proxyMcpServer.js"` with env `PROXY_PORT=8317`.
- Claude Desktop per-server log: `C:/Users/lmiller.INTEGRIBILT/AppData/Roaming/Claude/logs/mcp-server-antigravity-proxy.log`.
- ASM logs are exposed through the MCP protocol; other clients write equivalent per-server logs under their own log directories using the `antigravity-proxy` server name.
- The user heavily uses three Antigravity servers plus the desktop; there are more total Antigravity instances, but those four are the high-value sources first.

## Antigravity 2.0 Caution
Antigravity 2.0 may not sync/export artifacts as effectively as earlier versions. Agents must not assume ASM has complete Antigravity chat/artifact coverage until artifact counts and parser success rates are checked.

## Required Agent Behavior
1. Read this file and `compiled/global/AGENTS.md` before performing Antigravity-related work.
2. Use `AntigravitySync` as the named Drive folder for ASM-derived artifacts once Drive auth is available.
3. Use the ASM MCP server when available, but do not make MCP the only access path.
4. Every Antigravity agent is responsible for checking its own MCP server logs.
5. If an agent finds an MCP server issue, it should correct it if safe, or create a tool checkin/review that records the failure, suspected cause, and needed fix.
6. Do not silently ignore MCP failures; they must be visible in tool reviews and daily brain reports.
7. When cloning repos or docs on Windows/OFC01, prefer `E:/clones` when reasonably possible.
8. When working with the Integribilt stack YAML, preserve YAML validity and avoid hand-wavy edits.

## MCP Log Review Minimum
For each MCP server used by an agent:
- find the configured server name/command/URL;
- locate its logs if available;
- check recent errors/timeouts/auth failures;
- run a health/test command if available;
- correct trivial config/path/env issues;
- record non-trivial issues in `reviews/tool-checkins/`.

## ASM Source Registration Needed
Still needed:
- local ASM storage paths on desktop and three active servers;
- non-Claude client log locations;
- exact MCP Toolkit health check for `antigravity-proxy`;
- parser/export format notes;
- whether Antigravity 2.0 artifacts differ from prior format.

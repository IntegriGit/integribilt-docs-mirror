# Global Source Map

## Purpose
Map where evidence and context live. This file points agents to sources; it is not the source itself.

## Remote Git
- Remote: `https://github.com/IntegriGit/rocky-brain.git`
- Default branch: `main`
- Purpose: shared compiled markdown and agent coordination files.
- Boundary: do not commit secrets, raw confidential evidence, token files, or large ASM/Drive exports without explicit approval.

## Local Workspaces
- Hermes current workspace: `E:/projects/hermes`
- Spruce / Integribilt workspace: `E:/projects/shared-workspace/spruce`
- Rocky extraction folder: `E:/projects/shared-workspace/spruce/_rocky_extract`

## Existing Evidence Artifacts
- Chapter 11 intelligence brief: `E:/projects/shared-workspace/spruce/_rocky_extract/ROCKY_CH11_INTELLIGENCE_BRIEF.md`
- Key docs inventory: `E:/projects/shared-workspace/spruce/_rocky_extract/key_docs_inventory.md`
- Key docs extraction JSON: `E:/projects/shared-workspace/spruce/_rocky_extract/key_docs_extraction.json`
- Property value report markdown: `E:/projects/shared-workspace/spruce/_rocky_extract/PROPERTY_VALUE_REPORT_Commerce_Dr_vs_1500_Sam_Steward.md`
- Property value report HTML: `E:/projects/shared-workspace/spruce/_rocky_extract/PROPERTY_VALUE_REPORT_Commerce_Dr_vs_1500_Sam_Steward.html`

## Current Known Blockers
- Google Drive direct access is blocked until the Hermes profile has Google Workspace auth at `C:/Users/lmiller.INTEGRIBILT/AppData/Local/hermes/google_token.json` or equivalent configured credential.
- Lester plans to authenticate Google Drive in the morning after retrieving the USB key from his office.

## Planned Sources To Register
- Google Drive / Important Docs
- Google Drive / `AntigravitySync` — ASM-connected Drive folder for cross-IDE/network Antigravity sync.
- Antigravity Storage Manager output folders — ASM connects to IDEs and Google Drive; exact local/server paths still needed.
- ASM MCP server — `antigravity-proxy`, stdio command via VS Code extension `unchase.antigravity-storage-manager-0.14.3`, env `PROXY_PORT=8317`; Claude log `C:/Users/lmiller.INTEGRIBILT/AppData/Roaming/Claude/logs/mcp-server-antigravity-proxy.log`.
- Integribilt stack compose YAML on SVR02: `/home/lmiller/integribilt-stack/docker-compose.yml`.
- OFC01 clone/push path for stack YAML: `E:/clones/docs/integribilt-stack` (clone).
- Claude Desktop exports
- Claude Code sessions
- Cursor chats/logs
- Codex logs
- Grok/Gemini sessions
- VS Code workspace notes
- cloud console outputs
- Neo4j graph endpoint
- Redis endpoint, if retained
- Honcho workspace / peers

## Policy
Every important claim should point to a source path, source URI, graph ID, Honcho conclusion, or explicit user instruction.

# Claude / Shared Agent Entry Point

This repository uses `AGENTS.md` as the canonical shared agent instruction file.

Claude agents must read:

```text
AGENTS.md
compiled/global/AGENTS.md
compiled/global/CURRENT_PRIORITIES.md
```

Then read any task-specific files referenced there.

Do not maintain separate Claude-only operating truth here. If Claude needs a rule, add it to `AGENTS.md` or the relevant `compiled/` markdown so Antigravity, Hermes, Codex, Cursor, Gemini, and Grok can use the same source.

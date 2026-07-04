# Antigravity / Shared Agent Entry Point

This repository uses `AGENTS.md` as the canonical shared agent instruction file.

Antigravity agents must read:

```text
AGENTS.md
compiled/global/AGENTS.md
compiled/global/ANTIGRAVITY.md
```

Then read any task-specific files referenced there.

Do not maintain separate Antigravity-only operating truth here. If Antigravity needs a rule, add it to `AGENTS.md` or the relevant `compiled/` markdown so Claude, Hermes, Codex, Cursor, Gemini, and Grok can use the same source.

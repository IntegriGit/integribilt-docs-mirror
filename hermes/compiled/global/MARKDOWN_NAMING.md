# Shared Markdown Naming

## Decision
Use a remote Git repository for shared `.md` files, with `AGENTS.md` as the canonical cross-agent instruction file.

## Why `AGENTS.md`
- It is agent-neutral.
- It avoids maintaining divergent Claude-only and Antigravity-only instructions.
- It can be read by Hermes, Codex, Cursor, Gemini, Grok, Claude, Antigravity, and cloud agents.
- Claude-specific and Antigravity-specific entry files can point to it instead of duplicating truth.

## Root Files

```text
AGENTS.md        # canonical shared agent instructions
CLAUDE.md        # Claude entry point, points to AGENTS.md
ANTIGRAVITY.md   # Antigravity entry point, points to AGENTS.md
README.md        # human overview
```

## Rule
Do not fork operating truth by agent vendor. Add shared rules to `AGENTS.md` or `compiled/global/*.md`; add project rules to `compiled/projects/<project>/*.md`.

## Remote Git Recommendation
Use the IntegriGit private GitHub repository for this brain repo:

```text
remote private repo: https://github.com/IntegriGit/rocky-brain.git
local clone: E:/projects/rocky-brain
optional OFC01/other clones: E:/clones/rocky-brain
branch: main
```

## Raw Evidence Boundary
The remote repo should contain compiled markdown, source maps, evals, schemas, and templates. Do not commit raw confidential evidence, secrets, token files, or large ASM/Drive exports unless explicitly approved.

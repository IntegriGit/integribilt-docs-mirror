# Rocky Brain Cron Jobs

## Rocky Brain Daily Report
- Hermes cron job id: `3dc58e812647`
- Schedule: `0 7 * * *` — daily at 7:00 AM local time
- Delivery: origin/current chat
- Workdir: `E:/projects/rocky-brain`
- Purpose: inspect git status, remote sync with `https://github.com/IntegriGit/rocky-brain.git`, compiled brain files, Antigravity/MCP/YAML/gateway/markdown-naming rules, tool reviews, evals, and tests; report status, blockers, and recommended next actions.
- Test commands: `python -m unittest discover -s tests -v`; `python scripts/brain.py index && python scripts/brain.py eval`.
- Created: 2026-06-16
- Updated: 2026-06-17 to include Antigravity/MCP/YAML/gateway files and index evals.

# Current Global Priorities

## P0 — Shared Agent Truth
Create and wire a Git-backed working-truth repo so Hermes, Claude Code, Codex, Cursor, Antigravity, cloud agents, and other tools can read the same context.

## P1 — Source Map Completion
Register the exact source paths/credentials/endpoints for Google Drive, ASM, Redis, Neo4j, Honcho, and agent logs.

## P2 — Tool Review Loop
Require checkout/checkin/review for significant tool actions so the system improves from real use.

## P3 — Knowledge Index Bake-Off
Do not prematurely commit to Redis/GBrain/Postgres/etc. Run an eval-based bake-off for the durable knowledge index layer.

Rocky's current default: build a local, rebuildable SQLite FTS5 baseline first because it is transparent, portable, source-linked, and easy to test. Then benchmark GBrain and Postgres/pgvector against that baseline before promoting either.

## P4 — Integribilt Legal/Financial Context
Keep Chapter 11, foreclosure appraisal, valuation support, and source provenance organized and citation-ready.

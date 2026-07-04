# IntegriBilt Decisions

## DEC-20260614-001 — Shared brain starts with Git-backed compiled truth
- Status: active
- Decision: Use `E:/projects/rocky-brain` as the initial local brain repo scaffold.
- Rationale: Git-backed markdown gives all agents a common readable operating layer before deeper indexing is chosen.

## DEC-20260614-002 — Do not commit to a durable knowledge index yet
- Status: active
- Decision: Run a bake-off before choosing GBrain, Postgres/pgvector, SQLite/DuckDB/LanceDB, Redis, or another durable knowledge index.
- Rationale: Lester is committed to best results, not to any particular datastore.

## DEC-20260614-003 — Legal/financial claims require citations
- Status: active
- Decision: Bankruptcy, foreclosure, valuation, financial, and legal claims must cite sources or be labeled as assumptions/observations.
- Rationale: Accuracy matters for Rule 2004, Chapter 11, and valuation work.

## DEC-20260616-001 — Knowledge index default baseline
- Status: active
- Decision: Rocky will start with a local rebuildable SQLite FTS5/file-backed index as the baseline, then compare GBrain and Postgres/pgvector against it.
- Rationale: A rebuildable local baseline keeps Git/raw evidence as truth, adds no opaque authoritative silo, works before cloud/server decisions are final, and gives measurable eval results before heavier infrastructure is selected.

## DEC-20260616-002 — ASM source registration
- Status: active
- Decision: Register `AntigravitySync` as the ASM-connected Google Drive folder and register the ASM MCP server as a planned ingestion/access path.
- Rationale: Lester confirmed ASM connects to IDEs and Google Drive, and also has an MCP server connection.

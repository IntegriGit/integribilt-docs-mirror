# Global Open Questions

1. Where should the canonical remote Git repo live? GitHub private repo, local bare repo, server share, or other?
2. What are the exact Antigravity Storage Manager output paths for the desktop and three heavily used servers?
3. What Redis endpoint, if any, should be used for hot cache experiments?
4. What Neo4j endpoint/database should be used for graph experiments?
5. What Honcho workspace/peer naming should be canonical for non-Hermes agents?
6. Which agents should be read-only vs allowed to propose PRs/diffs?
7. Which data scopes are required: legal, financial, personal, internal, restricted?
8. Which knowledge-index candidates should enter the first bake-off: GBrain, Postgres/pgvector, SQLite/DuckDB/LanceDB, existing Redis, or other? Rocky's recommendation: start with a rebuildable SQLite FTS5 + file-backed index as the baseline, then compare GBrain and Postgres/pgvector against it.

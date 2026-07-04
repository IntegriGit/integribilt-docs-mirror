# SDK and API Compatibility Guide
Source: https://honcho.dev/docs/changelog/compatibility-guide

Compatibility guide for Honcho's SDKs and API

This guide helps you match the right SDK version to your Honcho API version. Newer SDK patch versions are always backward-compatible within the same major version — install the latest patch for your range.

## Current Versions

<CardGroup>
  <Card title="TypeScript SDK" icon="js">
    **Latest:** v2.1.2

    ```bash theme={null}
    npm install @honcho-ai/sdk
    ```
  </Card>

  <Card title="Python SDK" icon="python">
    **Latest:** v2.1.2

    ```bash theme={null}
    pip install honcho-ai
    ```
  </Card>
</CardGroup>

## Version Compatibility Table

| Honcho API Version | TypeScript SDK | Python SDK |
| ------------------ | -------------- | ---------- |
| v3.0.11 (Current)  | v2.1.2         | v2.1.2     |
| v3.0.10            | v2.1.2         | v2.1.2     |
| v3.0.9             | v2.1.2         | v2.1.2     |
| v3.0.8             | v2.1.2         | v2.1.2     |
| v3.0.7             | v2.1.2         | v2.1.2     |
| v3.0.6             | v2.1.1         | v2.1.1     |
| v3.0.5             | v2.1.0         | v2.1.0     |
| v3.0.4             | v2.1.0         | v2.1.0     |
| v3.0.3             | v2.1.0         | v2.1.0     |
| v3.0.2             | v2.0.0+        | v2.0.0+    |
| v3.0.1             | v2.0.0+        | v2.0.0+    |
| v3.0.0             | v2.0.0+        | v2.0.0+    |
| v2.5.1             | v1.6.0         | v1.6.0     |
| v2.5.0             | v1.6.0         | v1.6.0     |
| v2.4.3             | v1.5.0         | v1.5.0     |
| v2.4.2             | v1.5.0         | v1.5.0     |
| v2.4.1             | v1.5.0         | v1.5.0     |
| v2.4.0             | v1.5.0         | v1.5.0     |
| v2.3.3             | v1.4.1         | v1.4.1     |
| v2.3.2             | v1.4.0         | v1.4.0     |
| v2.3.1             | v1.4.0         | v1.4.0     |
| v2.3.0             | v1.4.0         | v1.4.0     |
| v2.2.0             | v1.3.0         | v1.3.0     |
| v2.1.1             | v1.2.1         | v1.2.2     |
| v2.1.0             | v1.2.1         | v1.2.2     |
| v2.0.5             | v1.1.0         | v1.1.0     |
| v2.0.4             | v1.1.0         | v1.1.0     |


# Changelog
Source: https://honcho.dev/docs/changelog/introduction



Welcome to the Honcho changelog! This section documents all notable changes to the Honcho API and SDKs.

<Accordion title="How to Read This Changelog">
  Each release is documented with:

  * **Added**: New features and capabilities
  * **Changed**: Modifications to existing functionality
  * **Deprecated**: Features that will be removed in future versions
  * **Removed**: Features that have been removed
  * **Fixed**: Bug fixes and corrections
  * **Security**: Security-related improvements

  ## Version Format

  Honcho follows [Semantic Versioning](https://semver.org/):

  * **MAJOR** version for incompatible API changes
  * **MINOR** version for backwards-compatible functionality additions
  * **PATCH** version for backwards-compatible bug fixes
</Accordion>

### Honcho API and SDK Changelogs

<Tabs>
  <Tab title="Honcho API">
    <Update label="v3.0.11 (Current)">
      ### Added

      * `api_request_duration_seconds` Prometheus histogram tracking per-route request latency, labeled by method and endpoint (#837)
      * LLM `provider_params` passthroughs (`extra_body` / `extra_headers` / `extra_query`) are now forwarded to the underlying provider transport across all backends, with shape validation that rejects non-mapping values (#821)
      * `structured_output_mode` model-config option to use `json_object` mode for OpenAI-compatible providers that lack native Structured Outputs support (used by the deriver) (#820)
      * OpenRouter app-attribution headers (`HTTP-Referer` / `X-Openrouter-Title`) are now sent on OpenAI-compatible clients when the configured base URL is OpenRouter, so requests are attributed to "Honcho" in OpenRouter's dashboard (#805)
      * Langfuse traces are now tagged with user and session IDs for easier trace filtering (#814)
      * `DERIVER_REPRESENTATION_BATCH_MAX_AGE_SECONDS` (default 1800s) lets sub-threshold representation work units flush once their oldest unprocessed queue item ages out. Set it to `0` to keep the legacy behavior where sub-threshold tails wait indefinitely unless `DERIVER_FLUSH_ENABLED=true` (#826)
      * Conclusion responses now include a `level` field (`explicit`, `deductive`, `inductive`, `contradiction`); list/query endpoints support filtering by `level` via `filters`, with reserved filter keys protected from being overridden by user-supplied filters (#851)

      ### Changed

      * Peer-scoped JWTs now get read-only access to the sessions their peer is an active member of (session context, summaries, peers, their own per-session config, search, and message reads). Session-scoped JWTs remain confined to their session and cannot reach peer routes (#679)
      * Compacted Honcho's log output, with guarded ms/s metric formatting that falls back to a plain string for non-numeric values (#836)
      * Sentry now drops noisy infra/scrape transactions: the reconciler opens a transaction only once a batch has rows (idle cycles emit none), and a `traces_sampler` returns `0.0` for `/metrics`, `/health`, `/openapi.json`, `/docs`, `/redoc`, and the deriver metrics server. `SENTRY.TRACES_SAMPLE_RATE` still governs real traffic (#834)

      ### Fixed

      * Peer- and session-scoped JWTs were effectively workspace-scoped: authorization walked the route's declared scope and fell through to a workspace match, so a `{w, p: alice}` token could act on any peer in the workspace. JWTs are now authorized by their narrowest claim and never widen to workspace access (#679)
      * The keys API now rejects creating a peer- or session-scoped key without a workspace. Such keys were minted successfully but failed verification on every request (#679)
      * Agent-supplied observation IDs carrying the display-format `id:` prefix are now normalized (prefix and trailing whitespace stripped) before `source_ids` are stored and on `get_reasoning_chain` lookups, fixing corrupted provenance links and broken reasoning-chain traversal (#795)
      * Fixed a `create_tree` keyword-argument mismatch in the Dreamer's surprisal tree construction (#749)
      * Providers that omit output-token counts (observed with Gemini on tool-loop completions) returned `output_tokens=None`, which raised a Pydantic validation error that aborted the call and crashed the Dreamer's induction phase before inductive conclusions were persisted. `None` is now coerced to `0` so token accounting degrades gracefully (#809)
      * Document creation now performs exact (case-insensitive, whitespace-trimmed) content deduplication before the existing semantic dedup step: exact duplicates within a batch collapse to a single insert, and an exact match against a live document reinforces it (atomic `times_derived` increment) instead of creating a new row (#861)
    </Update>

    <Update label="v3.0.10">
      ### Added

      * Messages are now embedded via a background task rather than blocking API request
      * Read-only DB session mode (`get_read_db` / `tracked_db(..., read_only=True)`) so reads don't hold a transaction open across the work
      * `CORS_ORIGINS` env var to configure CORS allowed origins without editing source; defaults match the prior hardcoded list, so self-hosted deployments behind custom domains can whitelist their frontend (#697)
      * `scripts/generate_jwt.py` — utility for minting scoped or admin Honcho JWTs (`--admin`, `--workspace`/`--peer`/`--session`, `--expires` with human-friendly durations, `--print-only`) without calling the keys API (#757)
      * `STALE_WORK_UNIT_CLEANUP_INTERVAL_SECONDS` (default 60s) — minimum jittered spacing between deriver stale-work-unit cleanup runs, so cleanup no longer runs on every seconds-scale poll (`0.0` keeps the legacy every-poll behavior) (#773)

      ### Changed

      * Optimized the deriver and dreamer prompt cache prefixes to improve prompt-cache hit rates (#806)

      ### Fixed

      * `times_derived` is now properly reinforced when a duplicate conclusion is detected. It had been pinned at 1 for nearly every conclusion (the reject-new branch dropped the increment and the new-wins branch reset the count to 1), so `ORDER BY times_derived DESC` fell back to arbitrary heap order and froze stale conclusions to the front of injected context. Reinforcement is now an atomic increment and both most-derived queries gained a `created_at DESC` recency tiebreaker (#768)
      * Webhook creation now correctly rejects private/internal IP addresses (#793)
    </Update>

    <Update label="v3.0.9">
      ### Changed

      * Connection acquisition is now a single attempt with no server-side retry, on a vanilla `AsyncSession`. A new `DB_CONNECT_TIMEOUT_SECONDS` (default 2s) bounds the attempt so a saturated or unreachable pooler fails fast instead of holding a client connection open to re-knock. A saturated DB now surfaces to the caller — the API returns an error and the deriver backs off and retries on a later poll — which lets the pooler drain rather than amplifying saturation.

      ### Added

      * Deriver poll jitter so instances that start together don't poll in lockstep: `DERIVER_POLLING_STARTUP_JITTER_SECONDS` (random delay before the first poll, default 30s) and `DERIVER_POLLING_JITTER_RATIO` (±fraction applied to every poll sleep, default 0.5). Both disable at `0.0`; the underlying backoff schedule is unchanged.

      ### Removed

      * Reverted the connection-checkout retry and `HonchoAsyncSession` custom session introduced in 3.0.8. Removed the `DB_CONNECTION_RETRY_ENABLED` / `DB_CONNECTION_RETRY_MAX_DELAY_SECONDS` / `DB_CONNECTION_RETRY_BACKOFF_INITIAL_SECONDS` / `DB_CONNECTION_RETRY_BACKOFF_MAX_SECONDS` settings, the `db_connection_acquisitions{outcome=...}` Prometheus counter, and the `db.pool.acquire` Sentry span. Alerting built on `db_connection_acquisitions` should migrate to `db_pool_connections` / `db_queries_in_flight`.
    </Update>

    <Update label="v3.0.8">
      ### Added

      * Connection-checkout retry with bounded exponential backoff (tenacity) on `get_db`/`tracked_db`: transient transaction-pooler (Supavisor) rejections — SQLAlchemy `TimeoutError` and `OperationalError` — now retry with backoff instead of surfacing as 500s under client-connection saturation. Gated by
        `DB_CONNECTION_RETRY_ENABLED` with configurable delay/backoff knobs; \~10s default budget (#758)
      * `HonchoAsyncSession` — a lazy `AsyncSession` that checks out its pooled connection (with retry) on the first DB-touching call rather than at construction. Request handlers doing non-DB work (embedding, file, LLM) before their first query no longer pin a pooler connection across it. Only the checkout is retried;
        the statement still runs exactly once, so writes are never duplicated (#758)
      * Adaptive deriver queue polling: the poll interval backs off when the queue is idle or erroring (base → max, doubling each cycle) and snaps back to base the moment work is claimed, cutting steady-state query load against the DB. Gated by `DERIVER_POLLING_BACKOFF_ENABLED` with configurable max/multiplier (#758)
      * New Prometheus `db_pool_connections` gauge (checked\_out / checked\_in / size / overflow), labeled `api`|`deriver`, registered in both the API lifespan and the deriver metrics server (#758)
      * New Prometheus `db_connection_acquisitions{outcome=ok|retried|exhausted}` counter — the alertable early-warning signal that connection checkouts are retrying through pooler rejection, before requests start failing (#758)
      * New Prometheus `db_queries_in_flight` gauge — statements actually executing on the wire (via SQLAlchemy cursor-execute events). Paired with `checked_out`, the gap reveals connections held but parked (the "idle in transaction during an external call" antipattern). Gated on `METRICS.ENABLED` for zero overhead when
        off (#758)
      * Explicit `SqlalchemyIntegration` in both the API and deriver Sentry inits; connection acquisition wrapped in a `db.pool.acquire` span with live pool stats captured on retry exhaustion (#758)

      ### Changed

      * Default `POOL_TIMEOUT` lowered to 5s, with validation that it stays under the connection-retry budget when a pooled (non-null) `POOL_CLASS` is configured; `config.toml.example` and the v2/v3 configuration docs updated to match (#758)
      * `HonchoAsyncSession` wraps every DB-touching session method (execute / scalar / scalars / flush / merge / refresh / commit / get / get\_one / stream / stream\_scalars / delete) so the lazy-checkout-with-retry guarantee has no holes; the acquired flag resets on `close()`/`reset()` so a reused session re-acquires on
        next use (#758)

      ### Fixed

      * Roll the session back on a retryable checkout failure before retrying — a failed autobegin could otherwise leave it pending-rollback, making the next connection attempt raise instead of cleanly re-checking-out (#758)
      * Guard `DBPoolCollector.collect()` so a pool-read/import hiccup can't raise and abort the entire `/metrics` scrape (Prometheus drops all metrics if any collector raises) (#758)
      * Clamp the pool overflow gauge to ≥ 0 (it could report negative before the pool fills) (#758)
      * Removed a double-sleep in the deriver idle poll so the backoff cap is a true cap rather than 2× (#758)
    </Update>

    <Update label="v3.0.7">
      ### Added

      * New `src/llm/` package as the single owner of provider runtime: clients, backends, history adapters, tool loop, request builder, credentials, and caching policy (#459)
      * New cloudevent `LLMCallCompletedEvent` (`llm.call.completed`) fires once per provider hit with full cost-attribution context: transport/provider\_label, model, token counts with cache breakdown, finish\_reason, outcome, retry/fallback state, duration, tool-call shape, streaming flag, and agent correlation (`run_id` + iteration) (#637)
      * `RepresentationCompletedEvent` now carries `total_input_tokens` for full-trace cost attribution; per-emitter `honcho_version` injection; deterministic per-`run_id` high-volume sampler via `TelemetrySettings.HIGH_VOLUME_SAMPLE_RATE` (#637)
      * Deriver custom instructions: per-workspace/peer guidance threaded into the deriver prompt with a `MAX_CUSTOM_INSTRUCTIONS_TOKENS` budget (default 2000); deriver `MAX_INPUT_TOKENS` raised 23000 → 25000 (#609)
      * Configurable embedding dimensions: `EMBEDDING_MODEL_CONFIG__DIMENSIONS_MODE` (`auto`/`always`/`never`) controls whether OpenAI `dimensions=` is forwarded (#678)
      * New `honcho-cli` package — Python CLI for inspecting and managing peers, sessions, and configuration against a Honcho deployment (#424)
      * `HONCHO_API_URL` env var support in the MCP Worker for self-hosted deployments (#575)
      * API ID `max_length` increased from 100 to 512 across `WorkspaceCreate`, `PeerCreate`, and `SessionCreate` to align with the DB schema (#684)
      * `AttemptPlan` dataclass pins per-retry provider selection across stream-final retries so streaming doesn't bounce back to primary after the tool loop has settled on fallback (#459)
      * Gemini JSON-schema sanitizer for `function_declarations` — strips keywords Gemini's validator rejects while preserving semantics for other backends (#459)

      ### Changed

      * All LLM orchestration moved out of `src/utils/clients.py` into `src/llm/` with modules split by responsibility (#459)
      * Default `ModelConfig` factories (deriver, summary, dreamer specialists, dialectic levels) normalized with no extra parameters set by default; operators add transport/thinking overrides explicitly (#459)
      * OpenAI reasoning-model routing widened to cover `gpt-5.x` and `o1/o3/o4` — these models receive `max_completion_tokens` instead of `max_tokens` (#459)
      * Peer card prompts reframed as stable identity markers; induction specialist now opts out of peer card writes so only deduction touches the card (#686)
      * Vector store queries no longer fetch embedding vectors — only document metadata is returned, reducing payload size and DB load (pgvector, lancedb, turbopuffer) (#682)
      * Langfuse trace metadata now includes `namespace`, `model`, and `provider` so traces can be filtered by deployment slice (#565)
      * Deriver: model-aware tokenizer (replaces the previously hardcoded encoding) and explicit guard on empty message content (#647)
      * Dialectic level defaults now merge correctly with per-level overrides (#656)
      * Default dialectic tool choice switched to `auto` (#630)
      * Vector sync given a substantial retry budget to tolerate transient embedding provider outages (#604)
      * `AgentToolConclusionsDeletedEvent` payload now carries `levels` (#612)
      * Turbopuffer: `InternalServerError` caught and surfaced as a warning rather than a hard failure; vector store sync errors downgraded to warnings (#561)

      ### Fixed

      * `reverse` query parameter is now honored on the v3 workspace list, peer list, workspace-scoped session list, and peer-scoped session list. Honcho SDKs at 2.1.0+ were already sending `reverse=true` for these routes but the server silently ignored it. Ties on `created_at` now fall back to the internal nanoid `id` for stable ordering across pages (#685)
      * LLM client factories now receive `base_url` from `LLMSettings` for default providers — operators pointing at OpenAI-compatible proxies via `LLM__OPENAI_BASE_URL` were previously ignored on the default path (#643, fixes #641)
      * Internal N+1 query in dialectic agent tool execution — collapsed per-iteration DB lookups into a single fetch (#652)
      * Dreamer threshold and time-guard semantics: count filter now includes only `documents.level == 'explicit'` (was inflating threshold via dreamer-created levels and creating a feedback loop); `last_dream_at` write relocated from enqueue to process so duplicate enqueues or failed runs no longer reset the 8-hour time guard (#573)
      * Deriver: blank observations are filtered out before embedding (previously triggered noisy embedding calls and persisted empty rows) (#615)
      * Surprisal module: filter format corrected from `{"level": levels}` to `{"level": {"in": levels}}` — the prior call silently returned 0 results and made the entire Surprisal phase of the Dream cycle a no-op (#581, fixes #559)
      * Removed hardcoded `stop_sequences` override from Deriver `ModelConfig` (was clobbering operator-configured stop sequences) (#587)
      * Embedding client: `embed()` now wraps single-string input in an array, restoring compatibility with OpenAI-compatible third-party providers that reject scalar input (#586)
      * Docker Compose: deriver service startup gated on the API service healthcheck — prevents races where the deriver starts before the API has run migrations (#689)
      * Docker image: `HEALTHCHECK` directive removed from the shared base image; service-level health checks now belong in each service's own configuration (#530)
      * Removed strict parameter validation for thinking params on Anthropic and OpenAI transports — was rejecting valid per-transport configs (#686)
      * Stream-final retries pin to the `AttemptPlan` that succeeded rather than re-running provider selection through the outer `current_attempt` ContextVar (#459)
      * Gemini `cached_content` reuse keys now include `system_instruction` and `tool_config` so cache hits don't cross configurations (#459)
      * CrewAI example updated for the latest CrewAI protocol (#631)

      ### Removed

      * `src/utils/clients.py` deleted; its responsibilities are split across `src/llm/registry.py`, `src/llm/credentials.py`, and the backend-specific modules (#459)
      * `HEALTHCHECK` directive from the shared Docker image (#530)
    </Update>

    <Update label="v3.0.6">
      ### Changed

      * Tightened transaction scopes across search, agent tools, queue manager, and webhook delivery to minimize DB connection hold time during external operations (#525)
      * Search operations refactored to two-phase pattern — external work (embeddings, LLM calls) completes before opening a transaction (#525)
      * Agent tool executor performs external operations before acquiring DB sessions (#525)
      * Queue manager transaction scope reduced to only the critical section (#525)
      * Webhook delivery no longer holds a DB session parameter (#525)

      ### Fixed

      * Session leakage in non-session-scoped dialectic chat calls (#526)

      ### Added

      * Health check endpoint (`/health`) for container orchestration and load balancer probes (#510)
    </Update>

    <Update label="v3.0.5">
      ### Fixed

      * explicit rollback on all transactions to force connection closed
    </Update>

    <Update label="v3.0.4">
      ### Added

      * JSONB metadata validation enforces 100 key limit and max depth of 5 (#419)

      ### Changed

      * Schemas refactored from single `schemas.py` into `schemas/api.py`, `schemas/configuration.py`, and `schemas/internal.py` with backwards-compatible re-exports (#419)

      ### Fixed

      * Missing `deleted_at` filter on `RepresentationManager._query_documents_recent()` and `._query_documents_most_derived()` allowed soft-deleted documents to leak into the deriver's working representation (#456)
      * `CleanupStaleItemsCompletedEvent` emitted spuriously when no queue item was actually deleted (#454)
      * Empty JSON file uploads caused unhandled errors; now returns normalized error responses (#434)
      * Memory leak: `_observation_locks` switched to `WeakValueDictionary` to prevent unbounded growth (#419)
      * SQL injection in `dependencies.py`: parameterized `set_config` calls to prevent injection via request context (#419)
      * NUL byte crashes: string inputs (message content, queries, peer cards) now stripped at schema level (#419)
      * Filter recursion depth capped at 5 to prevent stack overflow (#419)
      * Dedup-skipped observations now correctly reflected in created counts (#477)
      * External vector store support for message search — routes queries through configured external vector store with oversampling and
        deduplication to handle chunked embeddings (#479)
      * Dialectic agent no longer holds a DB connection during LLM calls — embeddings are pre-computed before tool execution, DB sessions isolated in `extract_preferences`, `query_documents` no longer accepts a DB session parameter (#477)
    </Update>

    <Update label="v3.0.3">
      ### Added

      * Consolidated session context into a single DB session with 40/60 token budget allocation between summary and messages
      * Observation validation via `ObservationInput` Pydantic schema with partial-success support and batch embedding with per-observation fallback
      * Peer card hard cap of 40 facts with case-insensitive deduplication and whitespace normalization
      * Safe integer coercion (`_safe_int`) for all LLM tool inputs to handle non-integer values like `"Infinity"`
      * Embedding pre-computation and reuse across multiple search calls in dialectic and representation flows
      * Peer existence validation in dialectic chat endpoints — raises ResourceNotFoundException instead of silently failing
      * Logging filter to suppress noisy `GET /metrics` access logs
      * Oolong long-context aggregation benchmark (synth and real variants, 1K–4M token context windows)
      * MolecularBench fact quality evaluation (ambiguity, decontextuality, minimality scoring)
      * CoverageBench information recall evaluation (gold fact extraction, coverage matching, QA verification)
      * LoCoMo summary-as-context baseline evaluation
      * Webhook delivery tests, dependency lifecycle tests, queue cleanup tests, summarizer fallback tests
      * Parallel test execution via pytest-xdist with worker-specific databases
      * `test_reasoning_levels.py` script for LOCOM dataset testing across reasoning levels

      ### Changed

      * Workspace deletion is now async — returns 202 Accepted, validates no active sessions (409 Conflict), cascade-deletes in background
      * Redis caching layer now stores plain-dict instead of ORM objects, with v2-prefixed keys, storage, resilient `safe_cache_set`/`safe_cache_delete` helpers, and deferred post-commit cache invalidation
      * All `get_or_create_*` CRUD operations now use savepoints (`db.begin_nested()`) instead of commit/rollback for race condition prevention
      * Reconciler vector sync uses direct ORM mutation instead of batch parameterized UPDATE statements
      * Summarizer enforces hard word limit in prompt and creates fallback text for empty summaries with `summary_tokens = 0`
      * Blocked Gemini responses (SAFETY, RECITATION, PROHIBITED\_CONTENT, BLOCKLIST) now raise `LLMError` to trigger retry/backup-provider logic
      * Gemini client explicitly sets `max_output_tokens` from `max_tokens` parameter
      * All deriver and metrics collector logging replaced with structured `logging.getLogger(__name__)` calls
      * Dreamer specialist prompts updated to enforce durable-facts-only peer cards with max 40 entries and deduplication
      * `GetOrCreateResult` changed from `NamedTuple` to `dataclass` with `async post_commit()` method
      * FastAPI upgraded from 0.111.0 to 0.131.0; added pyarrow dependency
      * Queue status filtering to only show user-facing tasks (representation, summary, dream); excludes internal infrastructure tasks

      ### Fixed

      * JWT timestamp bug — `JWTParams.t` was evaluated once at class definition time instead of per-instance
      * Session cache invalidation on deletion was missing
      * `get_peer_card()` now properly propagates `ResourceNotFoundException` instead of swallowing it
      * `set_peer_card()` ensures peer exists via `get_or_create_peers()` before updating
      * Backup provider failover with proper tool input type safety
      * Removed `setup_admin_jwt()` from server startup
      * Sentry coroutine detection switched from `asyncio.iscoroutinefunction` to `inspect.iscoroutinefunction`

      ### Removed

      * `explicit.py` and `obex.py` benchmarks replaced by coverage.py and molecular.py
      * Claude Code review automation workflow (`.github/workflows/claude.yml`)
      * Coverage reporting from default pytest configuration
    </Update>

    <Update label="v3.0.2">
      ### Added

      * Documentation for reasoning\_level and Claude Code plugin

      ### Changed

      * Gave dreaming sub-agents better prompting around peer card creation, tweaked overall prompts

      ### Fixed

      * Added message-search fallback for memory search tool, necessary in fresh sessions
      * Made FLUSH\_ENABLED a config value
      * Removed N+1 query in search\_messages
    </Update>

    <Update label="v3.0.1">
      ### Fixed

      * Token counting in Explicit Agent Loop
      * Backwards compatibility of queue items
    </Update>

    <Update label="v3.0.0">
      ### Added

      * Agentic Dreamer for intelligent memory consolidation using LLM agents
      * Agentic Dialectic for query answering using LLM agents with tool use
      * Reasoning levels configuration for dialectic (`minimal`, `low`, `medium`, `high`, `max`)
      * Prometheus token tracking for deriver and dialectic operations
      * n8n integration
      * Cloud Events for auditable telemetry
      * External Vector Store support for turbopuffer and lancedb with reconciliation flow

      ### Changed

      * API route renaming for consistency
      * Dreamer and dialectic now respect peer card configuration settings
      * Observations renamed to Conclusions across API and SDKs
      * Deriver to buffer representation tasks to normalize workloads
      * Local Representation tasks to create singular QueueItems
      * getContext endpoint to use `search_query` rather than force `last_user_message`

      ### Fixed

      * Dream scheduling bugs
      * Summary creation when start\_message\_id > end\_message\_id
      * Cashews upgrade to prevent NoScriptError
      * Memory leak in `accumulate_metric` call

      ### Removed

      * Peer card configuration from message configuration; peer cards no longer created/updated in deriver process
    </Update>

    <Update label="v2.5.1">
      ### Fixed

      * Backwards compatibility for `message_ids` field in documents to handle legacy tuple format
    </Update>

    <Update label="v2.5.0">
      ### Added

      * Message level configurations
      * CRUD operations for observations
      * Comprehensive test cases for harness
      * Peer level get\_context
      * Set Peer Card Method
      * Manual dreaming trigger endpoint

      ### Changed

      * Configurations to support more flags for fine-grained control of the deriver, peer cards, summaries, etc.
      * Working Representations to support more fine-grained parameters

      ### Fixed

      * File uploads to match `MessageCreate` structure
      * Cache invalidation strategy
    </Update>

    <Update label="v2.4.3">
      ### Added

      * Redis caching to improve DB IO
      * Backup LLM provider to avoid failures when a provider is down

      ### Changed

      * QueueItems to use standardized columns
      * Improved Deduplication logic for Representation Tasks
      * More finegrained metrics for representation, summary, and peer card tasks
      * DB constraint to follow standard naming conventions
    </Update>

    <Update label="v2.4.2">
      ### Fixed

      * Langfuse tracing to have readable waterfalls
      * Alembic Migrations to match models.py
      * message\_in\_seq correctly included in webhook payload

      ### Changed

      * Alembic to always use a session pooler
      * Statement timeout during alembic operations to 5 min
    </Update>

    <Update label="v2.4.1">
      ### Added

      * Alembic migration validation test suite

      ### Fixed

      * Alembic migrations to batch changes
      * Batch message creation sequence number

      ### Changed

      * Logging infrastructure to remove noisy messages
      * Sentry integration is centralized
    </Update>

    <Update label="v2.4.0">
      ### Added

      * Unified `Representation` class
      * vllm client support
      * Periodic queue cleanup logic
      * WIP Dreaming Feature
      * LongMemEval to Test Bench
      * Prometheus Client for better Metrics
      * Performance metrics instrumentation
      * Error reporting to deriver
      * Workspace Delete Method
      * Multi-db option in test harness

      ### Changed

      * Working Representations are Queried on the fly rather than cached in metadata
      * EmbeddingStore to RepresentationFactory
      * Summary Response Model to use public\_id of message for cutoff
      * Semantic across codebase to reference resources based on `observer` and `observed`
      * Prompts for Deriver & Dialectic to reference peer\_id and add examples
      * `Get Context` route returns peer card and representation in addition to messages and summaries
      * Refactoring logger.info calls to logger.debug where applicable

      ### Fixed

      * Gemini client to use async methods
    </Update>

    <Update label="v2.3.3">
      ### Changed

      * Deriver Rollup Queue processes interleaved messages for more context

      ### Fixed

      * Dialectic Streaming to follow SSE conventions
      * Sentry tracing in the deriver
    </Update>

    <Update label="v2.3.2">
      ### Added

      * Get peer cards endpoint (`GET /v2/peers/{peer_id}/card`) for retrieving targeted peer context information

      ### Changed

      * Replaced Mirascope dependency with small client implementation for better control
      * Optimized deriver performance by using joins on messages table instead of storing token count in queue payload
      * Database scope optimization for various operations
      * Batch representation task processing for \~10x speed improvement in practice

      ### Fixed

      * Separated clean and claim work units in queue manager to prevent race conditions
      * Skip locked ActiveQueueSession rows on delete operations
      * Langfuse SDK integration updates for compatibility
      * Added configurable maximum message size to prevent token overflow in deriver
      * Various minor bugfixes
    </Update>

    <Update label="v2.3.1">
      ### Fixed

      * Added max message count to deriver in order to not overflow token limits
    </Update>

    <Update label="v2.3.0">
      ### Added

      * `getSummaries` endpoint to get all available summaries for a session directly
      * Peer Card feature to improve context for deriver and dialectic

      ### Changed

      * Session Peer limit to be based on observers instead, renamed config value to
        `SESSION_OBSERVERS_LIMIT`
      * `Messages` can take a custom timestamp for the `created_at` field, defaulting
        to the current time
      * `get_context` endpoint returns detailed `Summary` object rather than just
        summary content
      * Working representations use a FIFO queue structure to maintain facts rather
        than a full rewrite
      * Optimized deriver enqueue by prefetching message sequence numbers (eliminates N+1 queries)

      ### Fixed

      * Deriver uses `get_context` internally to prevent context window limit errors
      * Embedding store will truncate context when querying documents to prevent embedding
        token limit errors
      * Queue manager to schedule work based on available works rather than total
        number of workers
      * Queue manager to use atomic db transactions rather than long lived transaction
        for the worker lifecycle
      * Timestamp formats unified to ISO 8601 across the codebase
      * Internal get\_context method's cutoff value is exclusive now
    </Update>

    <Update label="v2.2.0">
      ### Added

      * Arbitrary filters now available on all search endpoints
      * Search combines full-text and semantic using reciprocal rank fusion
      * Webhook support (currently only supports queue\_empty and test events, more to come)
      * Small test harness and custom test format for evaluating Honcho output quality
      * Added MCP server and documentation for it

      ### Changed

      * Search has 10 results by default, max 100 results
      * Queue structure generalized to handle more event types
      * Summarizer now exhaustive by default and tuned for performance

      ### Fixed

      * Resolve race condition for peers that leave a session while sending messages
      * Added explicit rollback to solve integrity error in queue
      * Re-introduced Sentry tracing to deriver
      * Better integrity logic in get\_or\_create API methods
    </Update>

    <Update label="v2.1.2">
      ### Fixed

      * Summarizer module to ignore empty summaries and pass appropriate one to get\_context
      * Structured Outputs calls with OpenAI provider to pass strict=True to Pydantic Schema
    </Update>

    <Update label="v2.1.1">
      ### Added

      * Test harness for custom Honcho evaluations
      * Better support for session and peer aware dialectic queries
      * Langfuse settings
      * Added recent history to dialectic prompt, dynamic based on new context window size setting

      ### Fixed

      * Summary queue logic
      * Formatting of logs
      * Filtering by session
      * Peer targeting in queries

      ### Changed

      * Made query expansion in dialectic off by default
      * Overhauled logging
      * Refactor summarization for performance and code clarity
      * Refactor queue payloads for clarity
    </Update>

    <Update label="v2.1.0">
      ### Added

      * File uploads
      * Brand new "ROTE" deriver system
      * Updated dialectic system
      * Local working representations
      * Better logging for deriver/dialectic
      * Deriver Queue Status no longer has redundant data

      ### Fixed

      * Document insertion
      * Session-scoped and peer-targeted dialectic queries work now
      * Minor bugs

      ### Removed

      * Peer-level messages

      ### Changed

      * Dialectic chat endpoint takes a single query
      * Rearranged configuration values (LLM, Deriver, Dialectic, History->Summary)
    </Update>

    <Update label="v2.0.5">
      ### Fixed

      * Groq API client to use the Async library
    </Update>

    <Update label="v2.0.4">
      ### Fixed

      * Migration/provision scripts did not have correct database connection arguments, causing timeouts
    </Update>

    <Update label="v2.0.3">
      ### Fixed

      * Bug that causes runtime error when Sentry flags are enabled
    </Update>

    <Update label="v2.0.2">
      ### Fixed

      * Database initialization was misconfigured and led to provision\_db script failing: switch to consistent working configuration with transaction pooler
    </Update>

    <Update label="v2.0.1">
      ### Added

      * Ergonomic SDKs for Python and TypeScript (uses Stainless underneath)
      * Deriver Queue Status endpoint
      * Complex arbitrary filters on workspace/session/peer/message
      * Message embedding table for full semantic search

      ### Changed

      * Overhauled documentation
      * BasedPyright typing for entire project
      * Resource filtering expanded to include logical operators

      ### Fixed

      * Various bugs
      * Use new config arrangement everywhere
      * Remove hardcoded responses
    </Update>

    <Update label="v2.0.0">
      ### Added

      * Ability to get a peer's working representation
      * Metadata to all data primitives (Workspaces, Peers, Sessions, Messages)
      * Internal metadata to store Honcho's state no longer exposed in API
      * Batch message operations and enhanced message querying with token and message count limits
      * Search and summary functionalities scoped by workspace, peer, and session
      * Session context retrieval with summaries and token allocatio
      * HNSW Index for Documents Table
      * Centralized Configuration via Environment Variables or config.toml file

      ### Changed

      * New architecture centered around the concept of a "peer" replaces the former
        "app"/"user"/"session" paradigm
      * Workspaces replace "apps" as top-level namespace
      * Peers replace "users"
      * Sessions no longer nested beneath peers and no longer limited to a single
        user-assistant model. A session exists independently of any one peer and
        peers can be added to and removed from sessions.
      * Dialectic API is now part of the Peer, not the Session
      * Dialectic API now allows queries to be scoped to a session or "targeted"
        to a fellow peer
      * Database schema migrated to adopt workspace/peer/session naming and structure
      * Authentication and JWT scopes updated to workspace/peer/session hierarchy
      * Queue processing now works on 'work units' instead of sessions
      * Message token counting updated with tiktoken integration and fallback heuristic
      * Queue and message processing updated to handle sender/target and task types for multi-peer scenarios

      ### Fixed

      * Improved error handling and validation for batch message operations and metadata
      * Database Sessions to be more atomic to reduce idle in transaction time

      ### Removed

      * Metamessages removed in favor of metadata
      * Collections and Documents no longer exposed in the API, solely internal
      * Obsolete tests for apps, users, collections, documents, and metamessages

      ***
    </Update>

    <Update label="v1.1.0">
      ### Added

      * Normalize resources to remove joins and increase query performance
      * Query tracing for debugging

      ### Changed

      * `/list` endpoints to not require a request body
      * `metamessage_type` to `label` with backwards compatibility
      * Database Provisioning to rely on alembic
      * Database Session Manager to explicitly rollback transactions before closing
        the connection

      ### Fixed

      * Alembic Migrations to include initial database migrations
      * Sentry Middleware to not report Honcho Exceptions
    </Update>

    <Update label="v1.0.0">
      ### Added

      * JWT based API authentication
      * Configurable logging
      * Consolidated LLM Inference via `ModelClient` class
      * Dynamic logging configurable via environment variables

      ### Changed

      * Deriver & Dialectic API to use Hybrid Memory Architecture
      * Metamessages are not strictly tied to a message
      * Database provisioning is a separate script instead of happening on startup
      * Consolidated `session/chat` and `session/chat/stream` endpoints
    </Update>

    ## Previous Releases

    For a complete history of all releases, see our [GitHub Releases](https://github.com/plastic-labs/honcho/tags) page.
  </Tab>

  <Tab title="Python SDK">
    [Python SDK](https://pypi.org/project/honcho-ai/)

    <Update label="v2.2.0">
      ### Added

      * `ConclusionLevel` type (`explicit`, `deductive`, `inductive`, `contradiction`) and a `level` field on `Conclusion`, exposing the reasoning level the server already tracked but previously stripped from responses.
      * `filters` parameter on `ConclusionScope.list()` and `ConclusionScope.query()` (sync and async), passed through to the same dynamic server-side filter logic as `peers()`/`sessions()`/`messages()`. Filter explicit-only conclusions with `filters={"level": "explicit"}`, or by any other supported field/operator. Requires a Honcho server with the matching API support (Honcho v3.0.11+).

      ### Fixed

      * Scope-managed filter keys (`observer`, `observed`, `session`) are now rejected with a clear `ValueError` if passed in `filters`, instead of silently overriding the scope and returning conclusions from a different peer pair. Use `peer.conclusions` / `conclusions_of(target)` and the `session=` parameter instead. `session_id` remains a valid filter on `query()`.
    </Update>

    <Update label="v2.1.2">
      ### Added

      * `page`, `size`, and `reverse` pagination parameters on `Honcho.workspaces()` and `HonchoAio.workspaces()`, closing the gap from 2.1.0 which added these to other list methods but not to `workspaces()`. Honoring `reverse` on the workspace/peer/session list routes also requires a Honcho server with the matching API fix; older servers silently ignore the parameter.
      * `peers` parameter on `Honcho.session()` and `HonchoAio.session()` — attach peers to a session at creation time instead of needing a follow-up `session.add_peers()` call. Accepts the same shapes as `Session.add_peers` (peer ID string, `Peer` object, list of either, or tuples with `SessionPeerConfig`).

      ### Changed

      * `WorkspaceCreateParams`, `PeerCreateParams`, and `SessionCreateParams` now accept IDs up to 512 characters (was 100), matching the server-side schema change in Honcho v3.0.7.
    </Update>

    <Update label="v2.1.1">
      ### Fixed

      * Broadened HTTP retry logic to cover `httpx.NetworkError` and `httpx.RemoteProtocolError` in addition to `httpx.TimeoutException` and `httpx.ConnectError`, improving resilience against transient network failures
    </Update>

    <Update label="v2.1.0">
      ### Added

      * `created_at` property on `Peer` and `Session` objects
      * `is_active` property on `Session` objects
      * `get_message(message_id)` method on `Session` (sync and async) to fetch a single message by ID
      * `page`, `size`, and `reverse` pagination parameters on all list methods

      ### Changed

      * **Breaking**: `peer()` and `session()` now always make a get-or-create API call — no more lazy initialization
      * Response configuration models now tolerate unknown fields from newer servers for forward compatibility

      ### Fixed

      * Sync and async `Session.get_metadata()`, `get_configuration()`, and `refresh()` now refresh cached `created_at` and `is_active` values along with metadata and configuration
      * `honcho.__version__` now derives from package metadata, with a source-checkout fallback, so it stays aligned with released package versions
    </Update>

    <Update label="v2.0.2">
      ### Changed

      * All input models now reject unknown fields via strict Pydantic validation (`extra="forbid"`). Previously, misspelled or extraneous fields were silently ignored. Now a `ValidationError` is raised with the unrecognized field name.
    </Update>

    <Update label="v2.0.1">
      ### Added

      * `set_peer_card` method

      ### Changed

      * `card` is now `get_card` with `card` kept for backwards compatibility and marked as deprecated
    </Update>

    <Update label="v2.0.0">
      ### Added

      * `ConclusionScope` object for CRUD operations on conclusions (renamed from observations)
      * Representation configuration support

      ### Changed

      * Observations renamed to Conclusions across the SDK
      * Major SDK refactoring and cleanup
      * Simplified method signatures throughout
      * Representation endpoints now return `string` instead of old Representation object

      ### Removed

      * Standalone types module (now uses honcho-core types)
      * Representation object
    </Update>

    <Update label="v1.6.0">
      ### Added

      * metadata and configuration fields to Workspace, Peer, Session, and Message objects
      * Session Clone methods
      * Peer level get\_context method
      * `ObservationScope` object to perform CRUD operations on observations
      * Representation object for WorkingRepresentations

      ### Changed

      * methods that take IDs, can all optionally take an object of the same type
    </Update>

    <Update label="v1.5.0">
      ### Added

      * Delete workspace method

      ### Changed

      * message\_id of `Summary` model is a string nanoid
      * Get Context can return Peer Card & Peer Representation
    </Update>

    <Update label="v1.4.1">
      ### Added

      * Get Peer Card method
      * Update Message metadata method
      * Session level deriver status methods
      * Delete session message

      ### Fixed

      * Dialectic Stream returns Iterators
      * Type warnings

      ### Changed

      * Pagination class to match core implementation
    </Update>

    <Update label="v1.4.0">
      ### Added

      * getSummaries API returning structured summaries
      * Webhook support

      ### Changed

      * Messages can take an optional `created_at` value, defaulting to the current
        time (UTC ISO 8601)
    </Update>

    <Update label="v1.2.2">
      ### Added

      * Filter parameter to various endpoints
    </Update>

    <Update label="v1.2.1">
      ### Fixed

      * Honcho util import paths
    </Update>

    <Update label="v1.2.0">
      ### Added

      * Get/poll deriver queue status endpoints added to workspace
      * Added endpoint to upload files as messages

      ### Removed

      * Removed peer messages in accordance with Honcho 2.1.0

      ### Changed

      * Updated chat endpoint to use singular `query` in accordance with Honcho 2.1.0
    </Update>

    <Update label="v1.1.0">
      ### Fixed

      * Properly handle AsyncClient
    </Update>
  </Tab>

  <Tab title="TypeScript SDK">
    [TypeScript SDK](https://www.npmjs.com/package/@honcho-ai/sdk)

    <Update label="v2.2.0">
      ### Added

      * `ConclusionLevel` type (`explicit`, `deductive`, `inductive`, `contradiction`) and a `level` field on `Conclusion`, exposing the reasoning level the server already tracked but previously stripped from responses.
      * `filters` option on `conclusions.list()` and `conclusions.query()`, passed through to the same dynamic server-side filter logic as the other list endpoints. Filter explicit-only conclusions with `{ filters: { level: 'explicit' } }`, or by any other supported field/operator. Requires a Honcho server with the matching API support (Honcho v3.0.11+).

      ### Fixed

      * Scope-managed filter keys (`observer`, `observed`, `session`) are now rejected with a clear error if passed in `filters`, instead of silently overriding the scope and returning conclusions from a different peer pair. Use `peer.conclusions` / `peer.conclusionsOf(target)` and the dedicated `session` option instead. `session_id` remains a valid filter on `query()`.
    </Update>

    <Update label="v2.1.2">
      ### Added

      * `peers` option on `Honcho.session()` — attach peers to a session at creation time instead of needing a follow-up `session.addPeers()` call. Accepts the same `PeerAddition` shape as `session.addPeers()` (peer ID strings, `Peer` objects, arrays of either, or a record with per-peer `observe_me`/`observe_others` config).

      ### Changed

      * ID validation in `validation.ts` now accepts workspace, peer, and session IDs up to 512 characters (was 100), matching the server-side schema change in Honcho v3.0.7.

      ### Fixed

      * `Honcho.workspaces()` now actually forwards the `reverse` option to the server. The 2.1.0 changelog listed `workspaces()` among the list methods that gained `reverse`, but `client.ts` was missing the field on the params type and request builder, so the option was silently dropped. Honoring `reverse` on the workspace/peer/session list routes also requires a Honcho server with the matching API fix; older servers silently ignore the parameter.
    </Update>

    <Update label="v2.1.1">
      ### Fixed

      * Broadened fetch error retry logic to catch all `TypeError` network failures (connection resets, DNS errors, etc.) instead of only those with `'fetch'` in the message, improving resilience across runtimes (Node, Bun, browsers)
    </Update>

    <Update label="v2.1.0">
      ### Added

      * `createdAt` property on `Peer` and `Session` wrapper objects
      * `isActive` property on `Session` wrapper objects
      * `getMessage(messageId)` method on `Session` to fetch a single message by ID
      * `Peer.representation()`, `Session.representation()`, and `Session.context()` now accept `Message` objects for `searchQuery`
      * `page`, `size`, and `reverse` pagination controls on all list methods

      ### Changed

      * **Breaking**: `searchQuery` removed from top-level `context()` options — use `representationOptions.searchQuery` instead:
        ```typescript theme={null}
        // Before (v2.0.x)
        await session.context({ searchQuery: "..." });
        // After (v2.1.0)
        await session.context({ representationOptions: { searchQuery: "..." } });
        ```
      * List methods (`peers()`, `sessions()`, `messages()`, `workspaces()`) support both the new options object and the legacy raw-filter form
      * Representation search options now accept strings and content-like objects, including `Message` instances, while rejecting whitespace-only or invalid runtime inputs
      * **Breaking**: `peer()` and `session()` now always make a get-or-create API call — no more lazy initialization. If you relied on constructing SDK objects without triggering a network request, note that every `peer()` and `session()` call now hits the API:
        ```typescript theme={null}
        // Before (v2.0.x) — no API call
        const session = honcho.session("my-session");
        // After (v2.1.0) — makes a get-or-create API call
        const session = await honcho.session("my-session");
        ```
      * Response configuration models now tolerate unknown fields from newer servers for forward compatibility
      * Moved `@types/node` from `dependencies` to `devDependencies`

      ### Fixed

      * `uploadFile()` now rejects unsupported top-level binary/object inputs and only validates inputs the serializer can actually upload
      * `uploadFile()` now serializes message configuration using API field names, matching `addMessages()`
      * Session fetch methods now refresh cached `createdAt` and `isActive` values alongside metadata and configuration
    </Update>

    <Update label="v2.0.2">
      ### Changed

      * Client constructor now rejects unknown options via `.strict()` Zod validation. Previously, misspelled options (e.g., `baseUrl` instead of `baseURL`) were silently ignored, causing the SDK to fall back to defaults. Now a `ZodError` is thrown with the unrecognized key name.
      * All input schemas now use `.strict()` validation to reject unknown fields.
      * `FileUploadSchema.configuration` now uses `MessageConfigurationSchema` instead of open record type.

      ### Fixed

      * README example used `baseUrl` instead of `baseURL`.
    </Update>

    <Update label="v2.0.1">
      ### Added

      * `setPeerCard` method

      ### Changed

      * `card` is now `getCard` with `card` kept for backwards compatibility and marked as deprecated
    </Update>

    <Update label="v2.0.0">
      ### Added

      * `ConclusionScope` object for CRUD operations on conclusions (renamed from observations)
      * Representation configuration support

      ### Changed

      * Observations renamed to Conclusions across the SDK
      * Major SDK refactoring and cleanup
      * Simplified method signatures throughout
      * Representation endpoints now return `string` instead of old Representation object

      ### Fixed

      * Pagination `this` binding issue

      ### Removed

      * Representation object
      * Stainless "core" SDK -- this SDK is now standalone
    </Update>

    <Update label="v1.6.0">
      ### Added

      * metadata and configuration fields to Workspace, Peer, Session, and Message objects
      * Session Clone methods
      * Peer level get\_context method
      * `ObservationScope` object to perform CRUD operations on observations
      * Representation object for WorkingRepresentations

      ### Changed

      * methods that take IDs, can all optionally take an object of the same type
    </Update>

    <Update label="v1.5.0">
      ### Added

      * Delete workspace method

      ### Changed

      * message\_id of `Summary` model is a string nanoid
      * Get Context can return Peer Card & Peer Representation
    </Update>

    <Update label="v1.4.1">
      ### Added

      * Get Peer Card method
      * Update Message metadata method
      * Session level deriver status methods
      * Delete session message

      ### Fixed

      * Dialectic Stream returns Iterators
      * Type warnings

      ### Changed

      * Pagination class to match core implementation
    </Update>

    <Update label="v1.4.0">
      ### Added

      * getSummaries API returning structured summaries
      * Webhook support

      ### Changed

      * Messages can take an optional `created_at` value, defaulting to the current
        time (UTC ISO 8601)
    </Update>

    <Update label="v1.2.1">
      ### Added

      * linting via Biome
      * Adding filter parameter to various endpoints

      ### Fixed

      * Order of parameters in `getSessions` endpoint
    </Update>

    <Update label="v1.2.0">
      ### Added

      * Get/poll deriver queue status endpoints added to workspace
      * Added endpoint to upload files as messages

      ### Removed

      * Removed peer messages in accordance with Honcho 2.1.0

      ### Changed

      * Updated chat endpoint to use singular `query` in accordance with Honcho 2.1.0
    </Update>

    <Update label="v1.1.0">
      ### Fixed

      * Create default workspace on Honcho client instantiation
      * Simplified Honcho client import path
    </Update>
  </Tab>
</Tabs>

## Getting Help

If you encounter issues using the Honcho API or its SDKs:

1. Open an issue on [GitHub](https://github.com/plastic-labs/honcho/issues)
2. Join our [Discord community](http://discord.gg/honcho) for support


# Create Conclusions
Source: https://honcho.dev/docs/v3/api-reference/endpoint/conclusions/create-conclusions

post /v3/workspaces/{workspace_id}/conclusions
Create one or more Conclusions.

Conclusions are logical certainties derived from interactions between Peers. They form the basis of a Peer's Representation.



# Delete Conclusion
Source: https://honcho.dev/docs/v3/api-reference/endpoint/conclusions/delete-conclusion

delete /v3/workspaces/{workspace_id}/conclusions/{conclusion_id}
Delete a single Conclusion by ID.

This action cannot be undone.



# List Conclusions
Source: https://honcho.dev/docs/v3/api-reference/endpoint/conclusions/list-conclusions

post /v3/workspaces/{workspace_id}/conclusions/list
List Conclusions using optional filters, ordered by recency unless `reverse` is true. Results are paginated.



# Query Conclusions
Source: https://honcho.dev/docs/v3/api-reference/endpoint/conclusions/query-conclusions

post /v3/workspaces/{workspace_id}/conclusions/query
Query Conclusions using semantic search. Use `top_k` to control the number of results returned.



# Create Key
Source: https://honcho.dev/docs/v3/api-reference/endpoint/keys/create-key

post /v3/keys
Create a new Key



# Create Messages For Session
Source: https://honcho.dev/docs/v3/api-reference/endpoint/messages/create-messages-for-session

post /v3/workspaces/{workspace_id}/sessions/{session_id}/messages
Add new message(s) to a session.



# Create Messages With File
Source: https://honcho.dev/docs/v3/api-reference/endpoint/messages/create-messages-with-file

post /v3/workspaces/{workspace_id}/sessions/{session_id}/messages/upload
Create messages from uploaded files. Files are converted to text and split into multiple messages.



# Get Message
Source: https://honcho.dev/docs/v3/api-reference/endpoint/messages/get-message

get /v3/workspaces/{workspace_id}/sessions/{session_id}/messages/{message_id}
Get a single message by ID from a Session.



# Get Messages
Source: https://honcho.dev/docs/v3/api-reference/endpoint/messages/get-messages

post /v3/workspaces/{workspace_id}/sessions/{session_id}/messages/list
Get all messages for a Session with optional filters. Results are paginated.



# Update Message
Source: https://honcho.dev/docs/v3/api-reference/endpoint/messages/update-message

put /v3/workspaces/{workspace_id}/sessions/{session_id}/messages/{message_id}
Update the metadata of a message.

This will overwrite any existing metadata for the message.



# Chat
Source: https://honcho.dev/docs/v3/api-reference/endpoint/peers/chat

post /v3/workspaces/{workspace_id}/peers/{peer_id}/chat
Query a Peer's representation using natural language. Performs agentic search and reasoning to comprehensively
answer the query based on all latent knowledge gathered about the peer from their messages and conclusions.



# Get Or Create Peer
Source: https://honcho.dev/docs/v3/api-reference/endpoint/peers/get-or-create-peer

post /v3/workspaces/{workspace_id}/peers
Get a Peer by ID or create a new Peer with the given ID.

If peer_id is provided as a query parameter, it uses that (must match JWT workspace_id).
Otherwise, it uses the peer_id from the JWT.



# Get Peer Card
Source: https://honcho.dev/docs/v3/api-reference/endpoint/peers/get-peer-card

get /v3/workspaces/{workspace_id}/peers/{peer_id}/card
Get a peer card for a specific peer relationship.

Returns the peer card that the observer peer has for the target peer if it exists.
If no target is specified, returns the observer's own peer card.



# Get Peer Context
Source: https://honcho.dev/docs/v3/api-reference/endpoint/peers/get-peer-context

get /v3/workspaces/{workspace_id}/peers/{peer_id}/context
Get context for a peer, including their representation and peer card.

This endpoint returns a curated subset of the representation and peer card for a peer.
If a target is specified, returns the context for the target from the
observer peer's perspective. If no target is specified, returns the
peer's own context (self-observation).

This is useful for getting all the context needed about a peer without
making multiple API calls.



# Get Peers
Source: https://honcho.dev/docs/v3/api-reference/endpoint/peers/get-peers

post /v3/workspaces/{workspace_id}/peers/list
Get all Peers for a Workspace, paginated with optional filters.



# Get Representation
Source: https://honcho.dev/docs/v3/api-reference/endpoint/peers/get-representation

post /v3/workspaces/{workspace_id}/peers/{peer_id}/representation
Get a curated subset of a Peer's Representation. A Representation is always a subset of the total
knowledge about the Peer. The subset can be scoped and filtered in various ways.


If a session_id is provided in the body, we get the Representation of the Peer scoped to that Session.
If a target is provided, we get the Representation of the target from the perspective of the Peer.
If no target is provided, we get the omniscient Honcho Representation of the Peer.



# Get Sessions For Peer
Source: https://honcho.dev/docs/v3/api-reference/endpoint/peers/get-sessions-for-peer

post /v3/workspaces/{workspace_id}/peers/{peer_id}/sessions
Get all Sessions for a Peer, paginated with optional filters.



# Search Peer
Source: https://honcho.dev/docs/v3/api-reference/endpoint/peers/search-peer

post /v3/workspaces/{workspace_id}/peers/{peer_id}/search
Search a Peer's messages, optionally filtered by various criteria.



# Set Peer Card
Source: https://honcho.dev/docs/v3/api-reference/endpoint/peers/set-peer-card

put /v3/workspaces/{workspace_id}/peers/{peer_id}/card
Set a peer card for a specific peer relationship.

Sets the peer card that the observer peer has for the target peer.
If no target is specified, sets the observer's own peer card.



# Update Peer
Source: https://honcho.dev/docs/v3/api-reference/endpoint/peers/update-peer

put /v3/workspaces/{workspace_id}/peers/{peer_id}
Update a Peer's metadata and/or configuration.



# Add Peers To Session
Source: https://honcho.dev/docs/v3/api-reference/endpoint/sessions/add-peers-to-session

post /v3/workspaces/{workspace_id}/sessions/{session_id}/peers
Add Peers to a Session. If a Peer does not yet exist, it will be created automatically.



# Clone Session
Source: https://honcho.dev/docs/v3/api-reference/endpoint/sessions/clone-session

post /v3/workspaces/{workspace_id}/sessions/{session_id}/clone
Clone a Session, optionally up to a specific message ID.



# Delete Session
Source: https://honcho.dev/docs/v3/api-reference/endpoint/sessions/delete-session

delete /v3/workspaces/{workspace_id}/sessions/{session_id}
Delete a Session and all associated messages.

The Session is marked as inactive immediately and returns 202 Accepted. The actual
deletion of all related data happens asynchronously via the queue with retry support.

This action cannot be undone.



# Get Or Create Session
Source: https://honcho.dev/docs/v3/api-reference/endpoint/sessions/get-or-create-session

post /v3/workspaces/{workspace_id}/sessions
Get a Session by ID or create a new Session with the given ID.

If Session ID is provided as a parameter, it verifies the Session is in the Workspace.
Otherwise, it uses the session_id from the JWT for verification.



# Get Peer Config
Source: https://honcho.dev/docs/v3/api-reference/endpoint/sessions/get-peer-config

get /v3/workspaces/{workspace_id}/sessions/{session_id}/peers/{peer_id}/config
Get the configuration for a Peer in a Session.

Member-read lets a peer-scoped key reach this route, but a peer may only
read its own per-session config — not a co-member's. Workspace/admin and
session-scoped tokens (which already span the whole session) are unaffected.



# Get Session Context
Source: https://honcho.dev/docs/v3/api-reference/endpoint/sessions/get-session-context

get /v3/workspaces/{workspace_id}/sessions/{session_id}/context
Produce a context object from the Session. The caller provides an optional token limit which the entire context must fit into.
If not provided, the context will be exhaustive (within configured max tokens). To do this, we allocate 40% of the token limit
to the summary, and 60% to recent messages -- as many as can fit. Note that the summary will usually take up less space than
this. If the caller does not want a summary, we allocate all the tokens to recent messages.



# Get Session Peers
Source: https://honcho.dev/docs/v3/api-reference/endpoint/sessions/get-session-peers

get /v3/workspaces/{workspace_id}/sessions/{session_id}/peers
Get all Peers in a Session. Results are paginated.



# Get Session Summaries
Source: https://honcho.dev/docs/v3/api-reference/endpoint/sessions/get-session-summaries

get /v3/workspaces/{workspace_id}/sessions/{session_id}/summaries
Get available summaries for a Session.

Returns both short and long summaries if available, including metadata like
the message ID they cover up to, creation timestamp, and token count.



# Get Sessions
Source: https://honcho.dev/docs/v3/api-reference/endpoint/sessions/get-sessions

post /v3/workspaces/{workspace_id}/sessions/list
Get all Sessions for a Workspace, paginated with optional filters.



# Remove Peers From Session
Source: https://honcho.dev/docs/v3/api-reference/endpoint/sessions/remove-peers-from-session

delete /v3/workspaces/{workspace_id}/sessions/{session_id}/peers
Remove Peers by ID from a Session.



# Search Session
Source: https://honcho.dev/docs/v3/api-reference/endpoint/sessions/search-session

post /v3/workspaces/{workspace_id}/sessions/{session_id}/search
Search a Session with optional filters. Use `limit` to control the number of results returned.



# Set Peer Config
Source: https://honcho.dev/docs/v3/api-reference/endpoint/sessions/set-peer-config

put /v3/workspaces/{workspace_id}/sessions/{session_id}/peers/{peer_id}/config
Set the configuration for a Peer in a Session.



# Set Session Peers
Source: https://honcho.dev/docs/v3/api-reference/endpoint/sessions/set-session-peers

put /v3/workspaces/{workspace_id}/sessions/{session_id}/peers
Set the Peers in a Session. If a Peer does not yet exist, it will be created automatically.

This will fully replace the current set of Peers in the Session.



# Update Session
Source: https://honcho.dev/docs/v3/api-reference/endpoint/sessions/update-session

put /v3/workspaces/{workspace_id}/sessions/{session_id}
Update a Session's metadata and/or configuration.



# Delete Webhook Endpoint
Source: https://honcho.dev/docs/v3/api-reference/endpoint/webhooks/delete-webhook-endpoint

delete /v3/workspaces/{workspace_id}/webhooks/{endpoint_id}
Delete a specific webhook endpoint.



# Get Or Create Webhook Endpoint
Source: https://honcho.dev/docs/v3/api-reference/endpoint/webhooks/get-or-create-webhook-endpoint

post /v3/workspaces/{workspace_id}/webhooks
Get or create a webhook endpoint URL.



# List Webhook Endpoints
Source: https://honcho.dev/docs/v3/api-reference/endpoint/webhooks/list-webhook-endpoints

get /v3/workspaces/{workspace_id}/webhooks
List all webhook endpoints, optionally filtered by workspace.



# Test Emit
Source: https://honcho.dev/docs/v3/api-reference/endpoint/webhooks/test-emit

get /v3/workspaces/{workspace_id}/webhooks/test
Test publishing a webhook event.



# Delete Workspace
Source: https://honcho.dev/docs/v3/api-reference/endpoint/workspaces/delete-workspace

delete /v3/workspaces/{workspace_id}
Delete a Workspace. This accepts the deletion request and processes it in the background,
permanently deleting all peers, messages, conclusions, and other resources associated
with the workspace.

Returns 409 Conflict if the workspace contains active sessions.
Delete all sessions first, then delete the workspace.

This action cannot be undone.



# Get All Workspaces
Source: https://honcho.dev/docs/v3/api-reference/endpoint/workspaces/get-all-workspaces

post /v3/workspaces/list
Get all Workspaces, paginated with optional filters.



# Get Or Create Workspace
Source: https://honcho.dev/docs/v3/api-reference/endpoint/workspaces/get-or-create-workspace

post /v3/workspaces
Get a Workspace by ID.

If workspace_id is provided as a query parameter, it uses that (must match JWT workspace_id).
Otherwise, it uses the workspace_id from the JWT.



# Get Queue Status
Source: https://honcho.dev/docs/v3/api-reference/endpoint/workspaces/get-queue-status

get /v3/workspaces/{workspace_id}/queue/status
Get the processing queue status for a Workspace, optionally scoped to an observer, sender,
and/or session.

Only tracks user-facing task types (representation, summary, dream).
Internal infrastructure tasks (reconciler, webhook, deletion) are excluded.
Note: completed counts reflect items since the last periodic queue cleanup,
not lifetime totals.



# Schedule Dream
Source: https://honcho.dev/docs/v3/api-reference/endpoint/workspaces/schedule-dream

post /v3/workspaces/{workspace_id}/schedule_dream
Manually schedule a dream task for a specific collection.

This endpoint bypasses all automatic dream conditions (document threshold,
minimum hours between dreams) and schedules the dream task for a future execution.

Currently this endpoint only supports scheduling immediate dreams. In the future,
users may pass a cron-style expression to schedule dreams at specific times.



# Search Workspace
Source: https://honcho.dev/docs/v3/api-reference/endpoint/workspaces/search-workspace

post /v3/workspaces/{workspace_id}/search
Search messages in a Workspace using optional filters. Use `limit` to control the number of
results returned.



# Update Workspace
Source: https://honcho.dev/docs/v3/api-reference/endpoint/workspaces/update-workspace

put /v3/workspaces/{workspace_id}
Update Workspace metadata and/or configuration.



# Introduction
Source: https://honcho.dev/docs/v3/api-reference/introduction



This section documents all available API endpoints in the Honcho Server. Each
endpoint provides CRUD operations for our core primitives. For information
about these primitives, see
[Architecture](/docs/v3/documentation/core-concepts/architecture).

<Warning>
  We strongly recommend using our official SDKs instead of calling these APIs directly. The SDKs provide better error handling, type safety, and developer experience.
</Warning>

## Recommended approach

Use our official SDKs for the best development experience:

* [Python SDK](https://pypi.org/project/honcho-ai/)
* [TypeScript SDK](https://www.npmjs.com/package/@honcho-ai/sdk)

## When to use this API reference

This reference is primarily useful for:

* Debugging SDK behavior
* Building integrations in unsupported languages
* Understanding the underlying data structures

The endpoints pages are autogenerated and include interactive examples for testing.


# Changing Embeddings
Source: https://honcho.dev/docs/v3/contributing/changing-embeddings

How to switch embedding dimension or model on a Honcho deployment

## Short answer: you can't, in place.

The embedding dimension is **machine-enforced** as immutable for the life of a deployment. The embedding model is **operator-owned** as immutable by contract. The supported way to change either is:

1. Stand up a new deployment at the desired configuration.
2. Replay or re-embed your data into it out-of-band.
3. Cut traffic over to the new deployment.

The rest of this page explains why, and what the safety boundaries actually are.

## Why dimension is enforced and model is not

On boot, both the API (`src/main.py` lifespan) and the deriver (`src/deriver/__main__.py`) run the validator in `src/startup/embedding_validator.py`. It does a schema-qualified `pg_attribute` lookup against `documents.embedding` and `message_embeddings.embedding`, decodes the declared `atttypmod`, and compares it to `EMBEDDING_VECTOR_DIMENSIONS`. A mismatch crashes the process with an actionable error before any HTTP route is served or any queue task is processed.

There is no equivalent check for the model. The pgvector column does not record what model produced the vectors inside it, and this design intentionally avoids adding new persistent metadata fields. The runtime has no way to detect that you swapped `text-embedding-3-small` for a different model that emits the same dimension.

That last point is a real footgun:

<Warning>
  Changing `EMBEDDING_MODEL_CONFIG__MODEL` to a different model at the **same dimension** (for example `text-embedding-3-small@1536` → `text-embedding-3-large` truncated to 1536) will silently succeed. New writes will use the new model; existing rows still hold vectors from the old model; recall quality will degrade with no startup or runtime warning.

  Treat model identity as a contract you own. If you need to change it, follow the destroy + rebuild path below.
</Warning>

## Recipe: changing dim or model

Concretely, for either a dim change or a model change:

1. **Provision the new deployment** with the target environment.

   ```bash theme={null}
   # On the new deployment:
   export EMBEDDING_VECTOR_DIMENSIONS=768
   export EMBEDDING_MODEL_CONFIG__TRANSPORT=openai
   export EMBEDDING_MODEL_CONFIG__MODEL=nomic-embed-text
   export EMBEDDING_MODEL_CONFIG__OVERRIDES__BASE_URL=http://your-ollama:11434/v1
   alembic upgrade head
   uv run python scripts/configure_embeddings.py --dry-run
   uv run python scripts/configure_embeddings.py --yes
   ```

2. **Replay your source data** (messages, documents, ingested content) into the new deployment via your normal application path. Honcho's existing message-creation API will re-derive embeddings using the new configuration. There is no in-place re-embedding tool — that would be a separate spec covering atomicity, cost-per-token, and dialectic-during-migration semantics.

3. **Cut over** at your application layer (DNS, load balancer, feature flag — whatever you use). The old deployment can stay running until you are confident in the new one; this design does not require an atomic switch.

The startup validator on the new deployment will refuse to start if step 1's `configure_embeddings.py` did not run, so a misconfiguration cannot quietly write wrong-dim vectors into the new schema.

## Edge case: truncation at the default dimension

If you are using `text-embedding-3-large` but truncating to 1536 (the default), be aware that `EMBEDDING_MODEL_CONFIG__DIMENSIONS_MODE=auto` will **not** forward `dimensions=` to the API — `auto` interprets the default as "operator did not opt into a non-default dim." The provider will return native 3072, the response-dim validator will reject it, and the request will fail.

For this case, either set `EMBEDDING_VECTOR_DIMENSIONS=1536` explicitly (so `auto` knows the operator opted in), or set `EMBEDDING_MODEL_CONFIG__DIMENSIONS_MODE=always`.

## Backend swap (turbopuffer ↔ lancedb ↔ pgvector) is a different operation

Switching the *storage backend* at constant dim/model — for example moving from pgvector to Turbopuffer — is supported via `src/reconciler/sync_vectors.py` and `VECTOR_STORE_MIGRATED`. That flow is unchanged by the embedding-pipeline work and is documented separately. It is **not** the destroy + rebuild path described above.


# Configuration Guide
Source: https://honcho.dev/docs/v3/contributing/configuration

Complete reference for configuring Honcho providers, features, and infrastructure

<Info>
  Most users only need the setup from the [Self-Hosting Guide](./self-hosting#llm-setup). This page is the full reference for customizing providers, tuning features, and hardening your deployment.
</Info>

Honcho loads configuration in this priority order (highest wins):

1. **Environment variables** (always take precedence)
2. **`.env` file**
3. **`config.toml` file**
4. **Built-in defaults**

Use `.env` for secrets and overrides, `config.toml` for base settings. Or use environment variables exclusively — whatever fits your deployment. Copy the examples to get started:

```bash theme={null}
cp .env.template .env
cp config.toml.example config.toml
```

### Environment Variable Naming

All config values map to environment variables:

* `{SECTION}_{KEY}` for top-level section settings (e.g., `DB_CONNECTION_URI` → `[db].CONNECTION_URI`)
* `{KEY}` for app-level settings (e.g., `LOG_LEVEL` → `[app].LOG_LEVEL`)
* Use `__` inside `{KEY}` for nested settings (e.g., `DIALECTIC_LEVELS__minimal__MODEL_CONFIG__TRANSPORT`, `DERIVER_MODEL_CONFIG__OVERRIDES__BASE_URL`)

## LLM Configuration

The [Self-Hosting Guide](./self-hosting#llm-setup) covers the basic setup: either the built-in OpenAI defaults or one OpenAI-compatible endpoint/model for all features. This section covers recommended model tiers, using multiple providers, and per-feature tuning.

<Note>
  All Honcho agents (deriver, dialectic, dream) require tool calling. Your models must support the OpenAI tool calling format.
</Note>

### Choosing Models

Model choice matters more for tool-use reliability than raw intelligence:

| Tier       | Example models                  | Use case                                | Notes                                     |
| ---------- | ------------------------------- | --------------------------------------- | ----------------------------------------- |
| **Light**  | Gemini 2.5 Flash, GLM-4.7-Flash | Deriver, summary, dialectic minimal/low | High throughput, cheap, reliable tool use |
| **Medium** | Claude Haiku 4.5, Grok 4.1 Fast | Dialectic medium/high                   | Good reasoning + tool use balance         |
| **Heavy**  | Claude Sonnet 4, GLM-5          | Dream, dialectic max                    | Best quality for rare/complex tasks       |

You can mix providers freely — for example, use Gemini for the deriver and Claude for dreaming.

### Provider Types

| Transport value | What it connects to                                                                               | API key env var         |
| --------------- | ------------------------------------------------------------------------------------------------- | ----------------------- |
| `openai`        | OpenAI or any OpenAI-compatible endpoint (OpenRouter, Together, Fireworks, LiteLLM, vLLM, Ollama) | `LLM_OPENAI_API_KEY`    |
| `anthropic`     | Anthropic Claude (direct)                                                                         | `LLM_ANTHROPIC_API_KEY` |
| `gemini`        | Google Gemini (direct)                                                                            | `LLM_GEMINI_API_KEY`    |

For OpenAI-compatible proxies (OpenRouter, vLLM, Ollama, etc.), use `transport = "openai"` and set `MODEL_CONFIG__OVERRIDES__BASE_URL` on each feature to point at your endpoint.

<Note>
  Some OpenAI-compatible providers don't support OpenAI Structured Outputs (`json_schema`). Set `DERIVER_MODEL_CONFIG__STRUCTURED_OUTPUT_MODE=json_object` to request loose JSON mode and inject the schema into the prompt instead.

  This setting only applies to the **deriver** on the **`openai`** transport — it is the only feature that uses structured output. The dialectic, summarizer, and dreamer don't request structured output, so the setting has no effect there, and the anthropic/gemini transports reject it.
</Note>

### Tiered Model Setup

Once you're past initial setup, you can assign different models per feature for better cost/quality tradeoffs. This example uses OpenRouter with light/medium/heavy tiers:

```bash theme={null}
LLM_OPENAI_API_KEY=sk-or-v1-...

# All features route through OpenRouter via overrides.base_url
# (You can set this on each feature's MODEL_CONFIG)

# Light tier — high throughput, cheap
DERIVER_MODEL_CONFIG__TRANSPORT=openai
DERIVER_MODEL_CONFIG__MODEL=google/gemini-2.5-flash-lite
DERIVER_MODEL_CONFIG__OVERRIDES__BASE_URL=https://openrouter.ai/api/v1
SUMMARY_MODEL_CONFIG__TRANSPORT=openai
SUMMARY_MODEL_CONFIG__MODEL=google/gemini-2.5-flash
DIALECTIC_LEVELS__minimal__MODEL_CONFIG__TRANSPORT=openai
DIALECTIC_LEVELS__minimal__MODEL_CONFIG__MODEL=google/gemini-2.5-flash-lite
DIALECTIC_LEVELS__low__MODEL_CONFIG__TRANSPORT=openai
DIALECTIC_LEVELS__low__MODEL_CONFIG__MODEL=google/gemini-2.5-flash-lite

# Medium tier — better reasoning
DIALECTIC_LEVELS__medium__MODEL_CONFIG__TRANSPORT=openai
DIALECTIC_LEVELS__medium__MODEL_CONFIG__MODEL=anthropic/claude-haiku-4-5
DIALECTIC_LEVELS__high__MODEL_CONFIG__TRANSPORT=openai
DIALECTIC_LEVELS__high__MODEL_CONFIG__MODEL=anthropic/claude-haiku-4-5
DIALECTIC_LEVELS__max__MODEL_CONFIG__TRANSPORT=openai
DIALECTIC_LEVELS__max__MODEL_CONFIG__MODEL=anthropic/claude-haiku-4-5

# Heavy tier — best quality for complex tasks
DREAM_DEDUCTION_MODEL_CONFIG__TRANSPORT=openai
DREAM_DEDUCTION_MODEL_CONFIG__MODEL=anthropic/claude-haiku-4-5
DREAM_INDUCTION_MODEL_CONFIG__TRANSPORT=openai
DREAM_INDUCTION_MODEL_CONFIG__MODEL=anthropic/claude-haiku-4-5
```

### Direct Vendor Keys

Instead of an OpenAI-compatible proxy, you can use vendor APIs directly. Each transport picks up its own `LLM_{TRANSPORT}_API_KEY`.

If you keep the built-in defaults, only `LLM_OPENAI_API_KEY` is required:

```bash theme={null}
LLM_OPENAI_API_KEY=...

# Built-in model defaults
# - deriver: openai / gpt-5.4-mini
# - dialectic (all levels): openai / gpt-5.4-mini
# - summary: openai / gpt-5.4-mini
# - dream specialists: openai / gpt-5.4-mini
# - embeddings: openai / text-embedding-3-small
```

To use Gemini or Anthropic directly, override the features you want to move:

```bash theme={null}
LLM_GEMINI_API_KEY=...
DERIVER_MODEL_CONFIG__TRANSPORT=gemini
DERIVER_MODEL_CONFIG__MODEL=gemini-2.5-flash

LLM_ANTHROPIC_API_KEY=...
DREAM_DEDUCTION_MODEL_CONFIG__TRANSPORT=anthropic
DREAM_DEDUCTION_MODEL_CONFIG__MODEL=claude-haiku-4-5
```

### Self-Hosted (vLLM / Ollama)

Use `transport = "openai"` and set `MODEL_CONFIG__OVERRIDES__BASE_URL` on each feature:

```bash theme={null}
# vLLM
LLM_OPENAI_API_KEY=not-needed
DERIVER_MODEL_CONFIG__TRANSPORT=openai
DERIVER_MODEL_CONFIG__MODEL=your-model-name
DERIVER_MODEL_CONFIG__OVERRIDES__BASE_URL=http://localhost:8000/v1

# Ollama
LLM_OPENAI_API_KEY=ollama
DERIVER_MODEL_CONFIG__TRANSPORT=openai
DERIVER_MODEL_CONFIG__MODEL=llama3.3:70b
DERIVER_MODEL_CONFIG__OVERRIDES__BASE_URL=http://localhost:11434/v1
```

Set `MODEL_CONFIG__TRANSPORT`, `MODEL_CONFIG__MODEL`, and `MODEL_CONFIG__OVERRIDES__BASE_URL` for each feature the same way.

The same overrides are available in `config.toml`:

```toml theme={null}
[deriver.model_config]
transport = "openai"
model = "my-local-model"

[deriver.model_config.overrides]
base_url = "http://localhost:8000/v1"
api_key_env = "DERIVER_LOCAL_API_KEY"
```

### Thinking Budget

Built-in defaults do not set `MODEL_CONFIG__THINKING_BUDGET_TOKENS` or `MODEL_CONFIG__THINKING_EFFORT`. Add one only when your chosen model supports it.

Use `MODEL_CONFIG__THINKING_EFFORT` for OpenAI reasoning models:

```bash theme={null}
DERIVER_MODEL_CONFIG__THINKING_EFFORT=minimal
DIALECTIC_LEVELS__max__MODEL_CONFIG__THINKING_EFFORT=medium
```

Use `MODEL_CONFIG__THINKING_BUDGET_TOKENS` for Anthropic and Gemini models. Set it to `0` or omit it for providers that don't support extended thinking:

```bash theme={null}
SUMMARY_MODEL_CONFIG__THINKING_BUDGET_TOKENS=1024
DREAM_DEDUCTION_MODEL_CONFIG__THINKING_BUDGET_TOKENS=1024
```

### Provider-Specific Parameters

Each model config supports an `overrides.provider_params` dict for passing arbitrary parameters to the underlying provider SDK. Use this for vendor-specific features that aren't part of the standard config:

```toml theme={null}
[deriver.model_config.overrides.provider_params]
# These are passed directly to the provider SDK
verbosity = "low"
```

#### Transport passthrough keys

Three keys inside `provider_params` are recognized as request-level escape hatches and forwarded to the underlying transport. Where a transport actually validates and merges one of these keys, its value must be a mapping — a non-mapping value raises a configuration error (see the per-transport behavior below; a key a transport ignores is not validated):

* **`extra_body`** — merged into the request body
* **`extra_headers`** — extra HTTP headers
* **`extra_query`** — extra URL query parameters

How each transport forwards them differs:

* **OpenAI and Anthropic** forward all three as identically-named SDK kwargs (`extra_body`, `extra_headers`, `extra_query`).
* **Gemini** has no SDK kwargs for these. It merges `extra_body` into the `GenerateContentConfig` dict and folds `extra_headers` into `http_options.headers`; `extra_query` is **unsupported and silently ignored**.

The merge is shallow and **operator-wins**: if Honcho and your config both set the same top-level key inside `extra_body`, your value replaces Honcho's. You are responsible for choosing a coherent combination — e.g. unset `thinking_budget_tokens` when supplying an `extra_body.thinking` for Anthropic-via-proxy, since Honcho will not translate between the two shapes.

Because Gemini merges `extra_body` directly into `GenerateContentConfig` (rather than a nested request body), an `extra_body` written for OpenAI/Anthropic generally will not transfer to Gemini unchanged — and a key collision there can overwrite a field Honcho manages (`thinking_config`, `response_schema`, `tools`, …).

```toml theme={null}
# Example: route an OpenAI-compatible proxy and tag requests for tracing
[deriver.model_config.overrides.provider_params.extra_headers]
X-Proxy-Route = "vertex"

[deriver.model_config.overrides.provider_params.extra_body]
# Provider-native body fields the standard config doesn't expose
anthropic_beta = ["context-1m-2025-01-15"]
```

### Changing Transport

When changing a feature's `transport`, always specify `model` explicitly. Partial overrides that change transport without model will keep the previous model name, which may not be valid for the new provider.

### General LLM Settings

```bash theme={null}
LLM_DEFAULT_MAX_TOKENS=2500

# Tool output limits (to prevent token explosion)
LLM_MAX_TOOL_OUTPUT_CHARS=10000  # ~2500 tokens at 4 chars/token
LLM_MAX_MESSAGE_CONTENT_CHARS=2000  # Max chars per message in tool results
```

### Embedding Configuration

Embeddings use their own nested model config, separate from the main text-generation LLM settings.

```bash theme={null}
# Embedding vector settings
EMBEDDING_VECTOR_DIMENSIONS=1536
EMBEDDING_MAX_INPUT_TOKENS=8192
EMBEDDING_MAX_TOKENS_PER_REQUEST=300000

# Embedding transport/model selection
EMBEDDING_MODEL_CONFIG__TRANSPORT=openai  # openai, gemini
EMBEDDING_MODEL_CONFIG__MODEL=text-embedding-3-small

# Optional endpoint overrides
EMBEDDING_MODEL_CONFIG__OVERRIDES__BASE_URL=http://localhost:8000/v1
EMBEDDING_MODEL_CONFIG__OVERRIDES__API_KEY_ENV=EMBEDDING_CUSTOM_API_KEY
```

Forwarding `dimensions=` to OpenAI-compatible providers is controlled by `EMBEDDING_MODEL_CONFIG__DIMENSIONS_MODE`:

* `auto` (default): forwards `dimensions=` when **the operator has explicitly set `EMBEDDING_VECTOR_DIMENSIONS`** — provenance, not value — and the configured model is not on the known-rejecting list (currently `text-embedding-ada-002`). Explicit `EMBEDDING_VECTOR_DIMENSIONS=1536` *does* trigger the forward; this is how `text-embedding-3-large` truncation to 1536 is expressed. Deployments that leave the setting unset get their existing behavior (`dimensions=` is not forwarded).
* `always`: always forward, regardless of whether `EMBEDDING_VECTOR_DIMENSIONS` was set. Use for OpenAI-compatible self-hosted providers that require it. Do not pick `always` *just* for same-as-default truncation — `auto` handles that case correctly as long as you set `EMBEDDING_VECTOR_DIMENSIONS=1536` explicitly in your environment. `always` is the right answer when your config layer might strip explicit "default-valued" envs, or when you want defense-in-depth.
* `never`: never forward. Explicit opt-out for providers that reject the parameter (e.g. `text-embedding-ada-002` if it slips past the known-rejecting allowlist).

#### Bootstrapping non-default dimensions

`EMBEDDING_VECTOR_DIMENSIONS` is treated as immutable for the life of a deployment. The pgvector schema is dim-pinned by Alembic at `1536` by default; if you want a different dim, you must ALTER the empty columns once at bootstrap time.

Install order for a non-default dim:

```bash theme={null}
# 1. Apply migrations (creates default vector(1536) schema)
alembic upgrade head

# 2. Set the dim you want
export EMBEDDING_VECTOR_DIMENSIONS=768

# 3. ALTER the empty columns to the target dim
uv run python scripts/configure_embeddings.py --dry-run   # preview
uv run python scripts/configure_embeddings.py --yes       # apply

# 4. Start API and deriver — both run the startup validator and refuse
# to serve traffic if the schema and EMBEDDING_VECTOR_DIMENSIONS disagree.
```

Existing deployments at 1536 with `text-embedding-3-small` need no action — step 3 detects matching dims and skips.

The script refuses to ALTER tables that already contain non-null embeddings. To switch dim or model on a populated deployment, stand up a new deployment at the new configuration and migrate data out of band; there is no in-place re-embedding affordance. See [Changing Embeddings](./changing-embeddings) for the destroy + rebuild recipe and the same-dim model-swap caveat.

External vector stores (Turbopuffer, LanceDB) do not need bootstrap setup. Namespaces are per-workspace and lazy-created on first write at whatever dim the embedding client returns. Use `--report` to inventory the existing namespaces against the configured dim:

```bash theme={null}
uv run python scripts/configure_embeddings.py --report
```

The startup validator at `src/startup/embedding_validator.py` enforces the dim invariant at boot for both the API (`src/main.py` lifespan) and the deriver (`src/deriver/__main__.py`). A mismatch crashes the process with an actionable error before any HTTP route is served or any queue task is processed.

`VECTOR_STORE_DIMENSIONS` is **deprecated**. `EMBEDDING_VECTOR_DIMENSIONS` is the single source of truth; setting `VECTOR_STORE_DIMENSIONS` explicitly emits a startup warning and is otherwise ignored. The field will be removed in a future release; drop it from your `.env` to silence the warning.

The `VECTOR_STORE_MIGRATED` flag still exists and still controls dual-write / cutover semantics for legacy tenants moving between storage backends (pgvector ↔ turbopuffer ↔ lancedb). It is unrelated to dimension configuration after this release.

### Feature-Specific Model Configuration

Each feature can use a different provider and model. Below are all the tuning knobs.

**Dialectic API:**

The Dialectic API provides theory-of-mind informed responses. It uses a tiered reasoning system with five levels:

```bash theme={null}
# Global dialectic settings
DIALECTIC_MAX_OUTPUT_TOKENS=8192
DIALECTIC_MAX_INPUT_TOKENS=100000
DIALECTIC_HISTORY_TOKEN_LIMIT=8192
DIALECTIC_SESSION_HISTORY_MAX_TOKENS=4096
```

**Per-Level Configuration:**

Each reasoning level has its own provider, model, and settings:

```toml theme={null}
# config.toml example
[dialectic.levels.minimal]
MAX_TOOL_ITERATIONS = 1
MAX_OUTPUT_TOKENS = 250
TOOL_CHOICE = "any"

[dialectic.levels.minimal.model_config]
transport = "openai"
model = "gpt-5.4-mini"

[dialectic.levels.low]
MAX_TOOL_ITERATIONS = 5
TOOL_CHOICE = "any"

[dialectic.levels.low.model_config]
transport = "openai"
model = "gpt-5.4-mini"

[dialectic.levels.medium]
MAX_TOOL_ITERATIONS = 2

[dialectic.levels.medium.model_config]
transport = "openai"
model = "gpt-5.4-mini"

[dialectic.levels.high]
MAX_TOOL_ITERATIONS = 4

[dialectic.levels.high.model_config]
transport = "openai"
model = "gpt-5.4-mini"

[dialectic.levels.max]
MAX_TOOL_ITERATIONS = 10

[dialectic.levels.max.model_config]
transport = "openai"
model = "gpt-5.4-mini"
```

Environment variables for nested levels use double underscores:

```bash theme={null}
DIALECTIC_LEVELS__minimal__MODEL_CONFIG__TRANSPORT=openai
DIALECTIC_LEVELS__minimal__MODEL_CONFIG__MODEL=gpt-5.4-mini
DIALECTIC_LEVELS__minimal__MAX_TOOL_ITERATIONS=1
DIALECTIC_LEVELS__minimal__MAX_OUTPUT_TOKENS=250
DIALECTIC_LEVELS__minimal__TOOL_CHOICE=any
```

**Deriver (Theory of Mind):**

The Deriver extracts facts from messages and builds theory-of-mind representations of peers.

```bash theme={null}
DERIVER_ENABLED=true

# LLM settings
DERIVER_MODEL_CONFIG__TRANSPORT=openai
DERIVER_MODEL_CONFIG__MODEL=gpt-5.4-mini
DERIVER_MAX_INPUT_TOKENS=25000
DERIVER_MAX_CUSTOM_INSTRUCTIONS_TOKENS=2000
# DERIVER_MODEL_CONFIG__THINKING_EFFORT=minimal
# DERIVER_MODEL_CONFIG__THINKING_BUDGET_TOKENS=1024
# DERIVER_MODEL_CONFIG__TEMPERATURE=0.7  # Optional temperature override
# DERIVER_MODEL_CONFIG__STRUCTURED_OUTPUT_MODE=json_object  # for providers without json_schema support

# Backup model (optional)
# DERIVER_MODEL_CONFIG__FALLBACK__MODEL=claude-haiku-4-5
# DERIVER_MODEL_CONFIG__FALLBACK__TRANSPORT=anthropic

# Worker settings
DERIVER_WORKERS=1  # Increase for higher throughput
DERIVER_POLLING_SLEEP_INTERVAL_SECONDS=1.0
# Adaptive polling: when idle/erroring, the sleep interval grows from the base
# toward DERIVER_POLLING_SLEEP_MAX_INTERVAL_SECONDS by the multiplier each cycle,
# then snaps back to base when work is found. Cuts steady-state query load.
DERIVER_POLLING_BACKOFF_ENABLED=true
DERIVER_POLLING_SLEEP_MAX_INTERVAL_SECONDS=30.0
DERIVER_POLLING_BACKOFF_MULTIPLIER=2.0
# Jitter so instances that start together don't poll in lockstep. Startup: sleep
# a random delay in [0, value] before the first poll (0.0 disables). Per-cycle:
# multiply every poll sleep by a random factor in [1-ratio, 1+ratio] (0.0 disables).
DERIVER_POLLING_STARTUP_JITTER_SECONDS=30.0
DERIVER_POLLING_JITTER_RATIO=0.5
DERIVER_STALE_SESSION_TIMEOUT_MINUTES=5

# Queue management
DERIVER_QUEUE_ERROR_RETENTION_SECONDS=2592000  # 30 days

# Observation settings
DERIVER_DEDUPLICATE=true
DERIVER_LOG_OBSERVATIONS=false
DERIVER_WORKING_REPRESENTATION_MAX_OBSERVATIONS=100
DERIVER_REPRESENTATION_BATCH_MAX_TOKENS=1024
DERIVER_REPRESENTATION_BATCH_MAX_AGE_SECONDS=1800
```

**Peer Card:**

```bash theme={null}
PEER_CARD_ENABLED=true
```

**Summary Generation:**

Session summaries provide compressed context for long conversations — short summaries (frequent) and long summaries (comprehensive).

```bash theme={null}
SUMMARY_ENABLED=true
SUMMARY_MODEL_CONFIG__TRANSPORT=openai
SUMMARY_MODEL_CONFIG__MODEL=gpt-5.4-mini
SUMMARY_MAX_TOKENS_SHORT=1000
SUMMARY_MAX_TOKENS_LONG=4000
# SUMMARY_MODEL_CONFIG__THINKING_EFFORT=minimal
# SUMMARY_MODEL_CONFIG__THINKING_BUDGET_TOKENS=1024
SUMMARY_MESSAGES_PER_SHORT_SUMMARY=20
SUMMARY_MESSAGES_PER_LONG_SUMMARY=60
```

**Dream Processing:**

Dream processing consolidates and refines peer representations during idle periods.

```bash theme={null}
DREAM_ENABLED=true
DREAM_DOCUMENT_THRESHOLD=50
DREAM_IDLE_TIMEOUT_MINUTES=60
DREAM_MIN_HOURS_BETWEEN_DREAMS=8
DREAM_ENABLED_TYPES=["omni"]
DREAM_MAX_TOOL_ITERATIONS=20
DREAM_HISTORY_TOKEN_LIMIT=16384

# Specialist model configs (each is independent)
DREAM_DEDUCTION_MODEL_CONFIG__TRANSPORT=openai
DREAM_DEDUCTION_MODEL_CONFIG__MODEL=gpt-5.4-mini
DREAM_INDUCTION_MODEL_CONFIG__TRANSPORT=openai
DREAM_INDUCTION_MODEL_CONFIG__MODEL=gpt-5.4-mini
```

**Surprisal-Based Sampling (Advanced):**

Optional subsystem for identifying unusual observations during dreaming:

```bash theme={null}
DREAM_SURPRISAL__ENABLED=false
DREAM_SURPRISAL__TREE_TYPE=kdtree
DREAM_SURPRISAL__TREE_K=5
DREAM_SURPRISAL__SAMPLING_STRATEGY=recent
DREAM_SURPRISAL__SAMPLE_SIZE=200
DREAM_SURPRISAL__TOP_PERCENT_SURPRISAL=0.10
DREAM_SURPRISAL__MIN_HIGH_SURPRISAL_FOR_REPLACE=10
DREAM_SURPRISAL__INCLUDE_LEVELS=["explicit", "deductive"]
```

## Core Configuration

### Application Settings

```bash theme={null}
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
SESSION_OBSERVERS_LIMIT=10
GET_CONTEXT_MAX_TOKENS=100000
MAX_MESSAGE_SIZE=25000
MAX_FILE_SIZE=5242880  # 5MB
EMBED_MESSAGES=true
EMBEDDING_MAX_INPUT_TOKENS=8192
EMBEDDING_MAX_TOKENS_PER_REQUEST=300000
NAMESPACE=honcho
```

**Optional Integrations:**

```bash theme={null}
LANGFUSE_HOST=https://cloud.langfuse.com
LANGFUSE_PUBLIC_KEY=your-langfuse-public-key
COLLECT_METRICS_LOCAL=false
LOCAL_METRICS_FILE=metrics.jsonl
REASONING_TRACES_FILE=traces.jsonl
```

### Database

```bash theme={null}
# Connection (required)
DB_CONNECTION_URI=postgresql+psycopg://postgres:postgres@localhost:5432/postgres

# Pool settings
DB_SCHEMA=public
DB_POOL_PRE_PING=true
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=5
DB_POOL_RECYCLE=300
DB_POOL_USE_LIFO=true
DB_SQL_DEBUG=false
# Per-connection establish timeout (seconds) so a single connection attempt
# fails fast instead of hanging when the server/pooler is unreachable.
DB_CONNECT_TIMEOUT_SECONDS=2
```

### Authentication

```bash theme={null}
AUTH_USE_AUTH=false  # Set to true to require JWT tokens
AUTH_JWT_SECRET=your-super-secret-jwt-key  # Required when auth is enabled
```

Generate a secret: `python scripts/generate_jwt_secret.py`

### Cache (Redis)

Redis caching is optional. Honcho works without it but benefits from caching in high-traffic scenarios.

```bash theme={null}
CACHE_ENABLED=false
CACHE_URL=redis://localhost:6379/0?suppress=true
CACHE_NAMESPACE=honcho
CACHE_DEFAULT_TTL_SECONDS=300
CACHE_DEFAULT_LOCK_TTL_SECONDS=5  # Cache stampede prevention
```

### Webhooks

```bash theme={null}
WEBHOOK_SECRET=your-webhook-signing-secret
WEBHOOK_MAX_WORKSPACE_LIMIT=10
```

### Vector Store

```bash theme={null}
VECTOR_STORE_TYPE=pgvector  # Options: pgvector, turbopuffer, lancedb
VECTOR_STORE_MIGRATED=false
VECTOR_STORE_NAMESPACE=honcho
# Embedding dim is configured via EMBEDDING_VECTOR_DIMENSIONS — see the
# Embedding Configuration section. VECTOR_STORE_DIMENSIONS is deprecated.

# Turbopuffer-specific
VECTOR_STORE_TURBOPUFFER_API_KEY=your-turbopuffer-api-key
VECTOR_STORE_TURBOPUFFER_REGION=us-east-1

# LanceDB-specific
VECTOR_STORE_LANCEDB_PATH=./lancedb_data
```

## Monitoring

### Prometheus Metrics

Honcho exposes `/metrics` endpoints for scraping:

* **API process**: Port 8000
* **Deriver process**: Port 9090

```bash theme={null}
METRICS_ENABLED=false
METRICS_NAMESPACE=honcho
```

### CloudEvents Telemetry

```bash theme={null}
TELEMETRY_ENABLED=false
TELEMETRY_ENDPOINT=https://telemetry.honcho.dev/v1/events
TELEMETRY_HEADERS='{"Authorization": "Bearer your-token"}'
TELEMETRY_BATCH_SIZE=100
TELEMETRY_FLUSH_INTERVAL_SECONDS=1.0
TELEMETRY_MAX_RETRIES=3
TELEMETRY_MAX_BUFFER_SIZE=10000
```

### Sentry

```bash theme={null}
SENTRY_ENABLED=false
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1
SENTRY_PROFILES_SAMPLE_RATE=0.1
```

## Reference config.toml

A complete config.toml with all defaults. Copy and modify what you need:

```toml theme={null}
[app]
LOG_LEVEL = "INFO"
SESSION_OBSERVERS_LIMIT = 10
EMBED_MESSAGES = true
NAMESPACE = "honcho"

[db]
CONNECTION_URI = "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
POOL_SIZE = 10
MAX_OVERFLOW = 20

[auth]
USE_AUTH = false

[cache]
ENABLED = false
URL = "redis://localhost:6379/0?suppress=true"
DEFAULT_TTL_SECONDS = 300

[deriver]
ENABLED = true
WORKERS = 1

[deriver.model_config]
transport = "openai"
model = "gpt-5.4-mini"

[peer_card]
ENABLED = true

[dialectic]
MAX_OUTPUT_TOKENS = 8192

[dialectic.levels.minimal]
MAX_TOOL_ITERATIONS = 1
MAX_OUTPUT_TOKENS = 250
TOOL_CHOICE = "any"

[dialectic.levels.minimal.model_config]
transport = "openai"
model = "gpt-5.4-mini"

[dialectic.levels.low]
MAX_TOOL_ITERATIONS = 5
TOOL_CHOICE = "any"

[dialectic.levels.low.model_config]
transport = "openai"
model = "gpt-5.4-mini"

[dialectic.levels.medium]
MAX_TOOL_ITERATIONS = 2

[dialectic.levels.medium.model_config]
transport = "openai"
model = "gpt-5.4-mini"

[dialectic.levels.high]
MAX_TOOL_ITERATIONS = 4

[dialectic.levels.high.model_config]
transport = "openai"
model = "gpt-5.4-mini"

[dialectic.levels.max]
MAX_TOOL_ITERATIONS = 10

[dialectic.levels.max.model_config]
transport = "openai"
model = "gpt-5.4-mini"

[summary]
ENABLED = true
MAX_TOKENS_SHORT = 1000
MAX_TOKENS_LONG = 4000

[summary.model_config]
transport = "openai"
model = "gpt-5.4-mini"

[dream]
ENABLED = true

[dream.deduction_model_config]
transport = "openai"
model = "gpt-5.4-mini"

[dream.induction_model_config]
transport = "openai"
model = "gpt-5.4-mini"

[webhook]
MAX_WORKSPACE_LIMIT = 10

[metrics]
ENABLED = false

[telemetry]
ENABLED = false

[vector_store]
TYPE = "pgvector"

[sentry]
ENABLED = false
```

## Database Migrations

```bash theme={null}
uv run alembic current          # Check status
uv run alembic upgrade head     # Upgrade to latest
uv run alembic downgrade <rev>  # Downgrade to specific revision
uv run alembic revision --autogenerate -m "Description"  # Create new migration
```

## Troubleshooting

1. **Database connection errors** — Ensure `DB_CONNECTION_URI` uses `postgresql+psycopg://` prefix. Verify database is running and pgvector extension is installed.

2. **Authentication issues** — Generate and set `AUTH_JWT_SECRET` when `AUTH_USE_AUTH=true`. Use `python scripts/generate_jwt_secret.py`.

3. **LLM provider errors** — Verify API keys are set. Check model names match your provider's format. Ensure models support tool calling.

4. **Deriver not processing** — Check logs. Increase `DERIVER_WORKERS` for throughput. Verify database and LLM connectivity.

5. **Dialectic level issues** — Unset level fields inherit from the built-in defaults. For Anthropic, `THINKING_BUDGET_TOKENS` must be >= 1024 when enabled. For providers without budgeted thinking, omit it or set it to `0`. `MAX_OUTPUT_TOKENS` must exceed `THINKING_BUDGET_TOKENS`.

6. **Vector store issues** — For Turbopuffer, set the API key. Check that `EMBEDDING_VECTOR_DIMENSIONS` matches your embedding model — the startup validator will refuse to boot on a mismatch.


# Contributing Guidelines
Source: https://honcho.dev/docs/v3/contributing/guidelines



Thank you for your interest in contributing to Honcho! This guide outlines the process for contributing to the project and our development conventions.

## Getting Started

Before you start contributing, please:

1. **Set up your development environment** - Follow the [Local Development guide](https://github.com/plastic-labs/honcho/blob/main/CONTRIBUTING.md#local-development) in the Honcho repository to get Honcho running locally.

2. **Join our community** - Feel free to join us in our [Discord](http://discord.gg/honcho) to discuss your changes, get help, or ask questions.

3. **Review existing issues** - Check the [issues tab](https://github.com/plastic-labs/honcho/issues) to see what's already being worked on or to find something to contribute to.

## Contribution Workflow

### 1. Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash theme={null}
   git clone https://github.com/YOUR_USERNAME/honcho.git
   cd honcho
   ```
3. Add the upstream repository as a remote:
   ```bash theme={null}
   git remote add upstream https://github.com/plastic-labs/honcho.git
   ```

### 2. Create a Branch

Create a new branch for your feature or bug fix:

```bash theme={null}
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix-name
```

**Branch naming conventions:**

* `feature/description` - for new features
* `fix/description` - for bug fixes
* `docs/description` - for documentation updates
* `refactor/description` - for code refactoring
* `test/description` - for adding or updating tests

### 3. Make Your Changes

* Write clean, readable code that follows our coding standards (see below)
* Add tests for new functionality
* Update documentation as needed
* Make sure your changes don't break existing functionality

### 4. Commit Your Changes

We follow conventional commit standards. Format your commit messages as:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**

* `feat`: A new feature
* `fix`: A bug fix
* `docs`: Documentation only changes
* `style`: Changes that do not affect the meaning of the code
* `refactor`: A code change that neither fixes a bug nor adds a feature
* `test`: Adding missing tests or correcting existing tests
* `chore`: Changes to the build process or auxiliary tools

**Examples:**

```bash theme={null}
git commit -m "feat(api): add new dialectic endpoint for user insights"
git commit -m "fix(db): resolve connection pool timeout issue"
git commit -m "docs(readme): update installation instructions"
```

### 5. Submit a Pull Request

1. Push your branch to your fork:
   ```bash theme={null}
   git push origin your-branch-name
   ```

2. Create a pull request on GitHub from your branch to the `main` branch

3. Fill out the pull request template with:
   * A clear description of what changes you've made
   * The motivation for the changes
   * Any relevant issue numbers (use "Closes #123" to auto-close issues)
   * Screenshots or examples if applicable

## Coding Standards

### Python Code Style

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
* Use [Black](https://black.readthedocs.io/) for code formatting (we may add this to CI in the future)
* Use type hints where possible
* Write docstrings for functions and classes using Google style docstrings

### Code Organization

* Keep functions focused and single-purpose
* Use meaningful variable and function names
* Add comments for complex logic
* Follow existing patterns in the codebase

### Testing

* Write unit tests for new functionality
* Ensure existing tests pass before submitting
* Use descriptive test names that explain what is being tested
* Mock external dependencies appropriately

### Documentation

* Update relevant documentation for new features
* Include examples in docstrings where helpful
* Keep README and other docs up to date with changes

## Review Process

1. **Automated checks** - Your PR will run through automated checks including tests and linting
2. **Project maintainer review** - A project maintainer will review your code for:
   * Code quality and adherence to standards
   * Functionality and correctness
   * Test coverage
   * Documentation completeness
3. **Discussion and iteration** - You may be asked to make changes or clarifications
4. **Approval and merge** - Once approved, your PR will be merged into `main`

## Types of Contributions

We welcome various types of contributions:

* **Bug fixes** - Help us squash bugs and improve stability
* **New features** - Add functionality that benefits the community
* **Documentation** - Improve or expand our documentation
* **Tests** - Increase test coverage and reliability
* **Performance improvements** - Help make Honcho faster and more efficient
* **Examples and tutorials** - Help other developers use Honcho

## Issue Reporting

When reporting bugs or requesting features:

1. Check if the issue already exists
2. Use the appropriate issue template
3. Provide clear reproduction steps for bugs
4. Include relevant environment information
5. Be specific about expected vs actual behavior

## Questions and Support

* **General questions** - Join our [Discord](http://discord.gg/honcho)
* **Bug reports** - Use GitHub issues
* **Feature requests** - Use GitHub issues with the feature request template
* **Security issues** - Please email us privately rather than opening a public issue

## License

By contributing to Honcho, you agree that your contributions will be licensed under the same [AGPL-3.0 License](./license) that covers the project.

Thank you for helping make Honcho better! 🫡


# License
Source: https://honcho.dev/docs/v3/contributing/license



Honcho is licensed under the AGPL-3.0 License. This is copied below for convenience and also present in the
[GitHub Repository](https://github.com/plastic-labs/honcho)

```
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU Affero General Public License is a free, copyleft license for
software and other kinds of works, specifically designed to ensure
cooperation with the community in the case of network server software.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
our General Public Licenses are intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  Developers that use our General Public Licenses protect your rights
with two steps: (1) assert copyright on the software, and (2) offer
you this License which gives you legal permission to copy, distribute
and/or modify the software.

  A secondary benefit of defending all users' freedom is that
improvements made in alternate versions of the program, if they
receive widespread use, become available for other developers to
incorporate.  Many developers of free software are heartened and
encouraged by the resulting cooperation.  However, in the case of
software used on network servers, this result may fail to come about.
The GNU General Public License permits making a modified version and
letting the public access it on a server without ever releasing its
source code to the public.

  The GNU Affero General Public License is designed specifically to
ensure that, in such cases, the modified source code becomes available
to the community.  It requires the operator of a network server to
provide the source code of the modified version running there to the
users of that server.  Therefore, public use of a modified version, on
a publicly accessible server, gives the public access to the source
code of the modified version.

  An older license, called the Affero General Public License and
published by Affero, was designed to accomplish similar goals.  This is
a different license, not a version of the Affero GPL, but Affero has
released a new version of the Affero GPL which permits relicensing under
this license.

  The precise terms and conditions for copying, distribution and
modification follow.

                       TERMS AND CONDITIONS

  0. Definitions.

  "This License" refers to version 3 of the GNU Affero General Public License.

  "Copyright" also means copyright-like laws that apply to other kinds of
works, such as semiconductor masks.

  "The Program" refers to any copyrightable work licensed under this
License.  Each licensee is addressed as "you".  "Licensees" and
"recipients" may be individuals or organizations.

  To "modify" a work means to copy from or adapt all or part of the work
in a fashion requiring copyright permission, other than the making of an
exact copy.  The resulting work is called a "modified version" of the
earlier work or a work "based on" the earlier work.

  A "covered work" means either the unmodified Program or a work based
on the Program.

  To "propagate" a work means to do anything with it that, without
permission, would make you directly or secondarily liable for
infringement under applicable copyright law, except executing it on a
computer or modifying a private copy.  Propagation includes copying,
distribution (with or without modification), making available to the
public, and in some countries other activities as well.

  To "convey" a work means any kind of propagation that enables other
parties to make or receive copies.  Mere interaction with a user through
a computer network, with no transfer of a copy, is not conveying.

  An interactive user interface displays "Appropriate Legal Notices"
to the extent that it includes a convenient and prominently visible
feature that (1) displays an appropriate copyright notice, and (2)
tells the user that there is no warranty for the work (except to the
extent that warranties are provided), that licensees may convey the
work under this License, and how to view a copy of this License.  If
the interface presents a list of user commands or options, such as a
menu, a prominent item in the list meets this criterion.

  1. Source Code.

  The "source code" for a work means the preferred form of the work
for making modifications to it.  "Object code" means any non-source
form of a work.

  A "Standard Interface" means an interface that either is an official
standard defined by a recognized standards body, or, in the case of
interfaces specified for a particular programming language, one that
is widely used among developers working in that language.

  The "System Libraries" of an executable work include anything, other
than the work as a whole, that (a) is included in the normal form of
packaging a Major Component, but which is not part of that Major
Component, and (b) serves only to enable use of the work with that
Major Component, or to implement a Standard Interface for which an
implementation is available to the public in source code form.  A
"Major Component", in this context, means a major essential component
(kernel, window system, and so on) of the specific operating system
(if any) on which the executable work runs, or a compiler used to
produce the work, or an object code interpreter used to run it.

  The "Corresponding Source" for a work in object code form means all
the source code needed to generate, install, and (for an executable
work) run the object code and to modify the work, including scripts to
control those activities.  However, it does not include the work's
System Libraries, or general-purpose tools or generally available free
programs which are used unmodified in performing those activities but
which are not part of the work.  For example, Corresponding Source
includes interface definition files associated with source files for
the work, and the source code for shared libraries and dynamically
linked subprograms that the work is specifically designed to require,
such as by intimate data communication or control flow between those
subprograms and other parts of the work.

  The Corresponding Source need not include anything that users
can regenerate automatically from other parts of the Corresponding
Source.

  The Corresponding Source for a work in source code form is that
same work.

  2. Basic Permissions.

  All rights granted under this License are granted for the term of
copyright on the Program, and are irrevocable provided the stated
conditions are met.  This License explicitly affirms your unlimited
permission to run the unmodified Program.  The output from running a
covered work is covered by this License only if the output, given its
content, constitutes a covered work.  This License acknowledges your
rights of fair use or other equivalent, as provided by copyright law.

  You may make, run and propagate covered works that you do not
convey, without conditions so long as your license otherwise remains
in force.  You may convey covered works to others for the sole purpose
of having them make modifications exclusively for you, or provide you
with facilities for running those works, provided that you comply with
the terms of this License in conveying all material for which you do
not control copyright.  Those thus making or running the covered works
for you must do so exclusively on your behalf, under your direction
and control, on terms that prohibit them from making any copies of
your copyrighted material outside their relationship with you.

  Conveying under any other circumstances is permitted solely under
the conditions stated below.  Sublicensing is not allowed; section 10
makes it unnecessary.

  3. Protecting Users' Legal Rights From Anti-Circumvention Law.

  No covered work shall be deemed part of an effective technological
measure under any applicable law fulfilling obligations under article
11 of the WIPO copyright treaty adopted on 20 December 1996, or
similar laws prohibiting or restricting circumvention of such
measures.

  When you convey a covered work, you waive any legal power to forbid
circumvention of technological measures to the extent such circumvention
is effected by exercising rights under this License with respect to
the covered work, and you disclaim any intention to limit operation or
modification of the work as a means of enforcing, against the work's
users, your or third parties' legal rights to forbid circumvention of
technological measures.

  4. Conveying Verbatim Copies.

  You may convey verbatim copies of the Program's source code as you
receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice;
keep intact all notices stating that this License and any
non-permissive terms added in accord with section 7 apply to the code;
keep intact all notices of the absence of any warranty; and give all
recipients a copy of this License along with the Program.

  You may charge any price or no price for each copy that you convey,
and you may offer support or warranty protection for a fee.

  5. Conveying Modified Source Versions.

  You may convey a work based on the Program, or the modifications to
produce it from the Program, in the form of source code under the
terms of section 4, provided that you also meet all of these conditions:

    a) The work must carry prominent notices stating that you modified
    it, and giving a relevant date.

    b) The work must carry prominent notices stating that it is
    released under this License and any conditions added under section
    7.  This requirement modifies the requirement in section 4 to
    "keep intact all notices".

    c) You must license the entire work, as a whole, under this
    License to anyone who comes into possession of a copy.  This
    License will therefore apply, along with any applicable section 7
    additional terms, to the whole of the work, and all its parts,
    regardless of how they are packaged.  This License gives no
    permission to license the work in any other way, but it does not
    invalidate such permission if you have separately received it.

    d) If the work has interactive user interfaces, each must display
    Appropriate Legal Notices; however, if the Program has interactive
    interfaces that do not display Appropriate Legal Notices, your
    work need not make them do so.

  A compilation of a covered work with other separate and independent
works, which are not by their nature extensions of the covered work,
and which are not combined with it such as to form a larger program,
in or on a volume of a storage or distribution medium, is called an
"aggregate" if the compilation and its resulting copyright are not
used to limit the access or legal rights of the compilation's users
beyond what the individual works permit.  Inclusion of a covered work
in an aggregate does not cause this License to apply to the other
parts of the aggregate.

  6. Conveying Non-Source Forms.

  You may convey a covered work in object code form under the terms
of sections 4 and 5, provided that you also convey the
machine-readable Corresponding Source under the terms of this License,
in one of these ways:

    a) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by the
    Corresponding Source fixed on a durable physical medium
    customarily used for software interchange.

    b) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by a
    written offer, valid for at least three years and valid for as
    long as you offer spare parts or customer support for that product
    model, to give anyone who possesses the object code either (1) a
    copy of the Corresponding Source for all the software in the
    product that is covered by this License, on a durable physical
    medium customarily used for software interchange, for a price no
    more than your reasonable cost of physically performing this
    conveying of source, or (2) access to copy the
    Corresponding Source from a network server at no charge.

    c) Convey individual copies of the object code with a copy of the
    written offer to provide the Corresponding Source.  This
    alternative is allowed only occasionally and noncommercially, and
    only if you received the object code with such an offer, in accord
    with subsection 6b.

    d) Convey the object code by offering access from a designated
    place (gratis or for a charge), and offer equivalent access to the
    Corresponding Source in the same way through the same place at no
    further charge.  You need not require recipients to copy the
    Corresponding Source along with the object code.  If the place to
    copy the object code is a network server, the Corresponding Source
    may be on a different server (operated by you or a third party)
    that supports equivalent copying facilities, provided you maintain
    clear directions next to the object code saying where to find the
    Corresponding Source.  Regardless of what server hosts the
    Corresponding Source, you remain obligated to ensure that it is
    available for as long as needed to satisfy these requirements.

    e) Convey the object code using peer-to-peer transmission, provided
    you inform other peers where the object code and Corresponding
    Source of the work are being offered to the general public at no
    charge under subsection 6d.

  A separable portion of the object code, whose source code is excluded
from the Corresponding Source as a System Library, need not be
included in conveying the object code work.

  A "User Product" is either (1) a "consumer product", which means any
tangible personal property which is normally used for personal, family,
or household purposes, or (2) anything designed or sold for incorporation
into a dwelling.  In determining whether a product is a consumer product,
doubtful cases shall be resolved in favor of coverage.  For a particular
product received by a particular user, "normally used" refers to a
typical or common use of that class of product, regardless of the status
of the particular user or of the way in which the particular user
actually uses, or expects or is expected to use, the product.  A product
is a consumer product regardless of whether the product has substantial
commercial, industrial or non-consumer uses, unless such uses represent
the only significant mode of use of the product.

  "Installation Information" for a User Product means any methods,
procedures, authorization keys, or other information required to install
and execute modified versions of a covered work in that User Product from
a modified version of its Corresponding Source.  The information must
suffice to ensure that the continued functioning of the modified object
code is in no case prevented or interfered with solely because
modification has been made.

  If you convey an object code work under this section in, or with, or
specifically for use in, a User Product, and the conveying occurs as
part of a transaction in which the right of possession and use of the
User Product is transferred to the recipient in perpetuity or for a
fixed term (regardless of how the transaction is characterized), the
Corresponding Source conveyed under this section must be accompanied
by the Installation Information.  But this requirement does not apply
if neither you nor any third party retains the ability to install
modified object code on the User Product (for example, the work has
been installed in ROM).

  The requirement to provide Installation Information does not include a
requirement to continue to provide support service, warranty, or updates
for a work that has been modified or installed by the recipient, or for
the User Product in which it has been modified or installed.  Access to a
network may be denied when the modification itself materially and
adversely affects the operation of the network or violates the rules and
protocols for communication across the network.

  Corresponding Source conveyed, and Installation Information provided,
in accord with this section must be in a format that is publicly
documented (and with an implementation available to the public in
source code form), and must require no special password or key for
unpacking, reading or copying.

  7. Additional Terms.

  "Additional permissions" are terms that supplement the terms of this
License by making exceptions from one or more of its conditions.
Additional permissions that are applicable to the entire Program shall
be treated as though they were included in this License, to the extent
that they are valid under applicable law.  If additional permissions
apply only to part of the Program, that part may be used separately
under those permissions, but the entire Program remains governed by
this License without regard to the additional permissions.

  When you convey a copy of a covered work, you may at your option
remove any additional permissions from that copy, or from any part of
it.  (Additional permissions may be written to require their own
removal in certain cases when you modify the work.)  You may place
additional permissions on material, added by you to a covered work,
for which you have or can give appropriate copyright permission.

  Notwithstanding any other provision of this License, for material you
add to a covered work, you may (if authorized by the copyright holders of
that material) supplement the terms of this License with terms:

    a) Disclaiming warranty or limiting liability differently from the
    terms of sections 15 and 16 of this License; or

    b) Requiring preservation of specified reasonable legal notices or
    author attributions in that material or in the Appropriate Legal
    Notices displayed by works containing it; or

    c) Prohibiting misrepresentation of the origin of that material, or
    requiring that modified versions of such material be marked in
    reasonable ways as different from the original version; or

    d) Limiting the use for publicity purposes of names of licensors or
    authors of the material; or

    e) Declining to grant rights under trademark law for use of some
    trade names, trademarks, or service marks; or

    f) Requiring indemnification of licensors and authors of that
    material by anyone who conveys the material (or modified versions of
    it) with contractual assumptions of liability to the recipient, for
    any liability that these contractual assumptions directly impose on
    those licensors and authors.

  All other non-permissive additional terms are considered "further
restrictions" within the meaning of section 10.  If the Program as you
received it, or any part of it, contains a notice stating that it is
governed by this License along with a term that is a further
restriction, you may remove that term.  If a license document contains
a further restriction but permits relicensing or conveying under this
License, you may add to a covered work material governed by the terms
of that license document, provided that the further restriction does
not survive such relicensing or conveying.

  If you add terms to a covered work in accord with this section, you
must place, in the relevant source files, a statement of the
additional terms that apply to those files, or a notice indicating
where to find the applicable terms.

  Additional terms, permissive or non-permissive, may be stated in the
form of a separately written license, or stated as exceptions;
the above requirements apply either way.

  8. Termination.

  You may not propagate or modify a covered work except as expressly
provided under this License.  Any attempt otherwise to propagate or
modify it is void, and will automatically terminate your rights under
this License (including any patent licenses granted under the third
paragraph of section 11).

  However, if you cease all violation of this License, then your
license from a particular copyright holder is reinstated (a)
provisionally, unless and until the copyright holder explicitly and
finally terminates your license, and (b) permanently, if the copyright
holder fails to notify you of the violation by some reasonable means
prior to 60 days after the cessation.

  Moreover, your license from a particular copyright holder is
reinstated permanently if the copyright holder notifies you of the
violation by some reasonable means, this is the first time you have
received notice of violation of this License (for any work) from that
copyright holder, and you cure the violation prior to 30 days after
your receipt of the notice.

  Termination of your rights under this section does not terminate the
licenses of parties who have received copies or rights from you under
this License.  If your rights have been terminated and not permanently
reinstated, you do not qualify to receive new licenses for the same
material under section 10.

  9. Acceptance Not Required for Having Copies.

  You are not required to accept this License in order to receive or
run a copy of the Program.  Ancillary propagation of a covered work
occurring solely as a consequence of using peer-to-peer transmission
to receive a copy likewise does not require acceptance.  However,
nothing other than this License grants you permission to propagate or
modify any covered work.  These actions infringe copyright if you do
not accept this License.  Therefore, by modifying or propagating a
covered work, you indicate your acceptance of this License to do so.

  10. Automatic Licensing of Downstream Recipients.

  Each time you convey a covered work, the recipient automatically
receives a license from the original licensors, to run, modify and
propagate that work, subject to this License.  You are not responsible
for enforcing compliance by third parties with this License.

  An "entity transaction" is a transaction transferring control of an
organization, or substantially all assets of one, or subdividing an
organization, or merging organizations.  If propagation of a covered
work results from an entity transaction, each party to that
transaction who receives a copy of the work also receives whatever
licenses to the work the party's predecessor in interest had or could
give under the previous paragraph, plus a right to possession of the
Corresponding Source of the work from the predecessor in interest, if
the predecessor has it or can get it with reasonable efforts.

  You may not impose any further restrictions on the exercise of the
rights granted or affirmed under this License.  For example, you may
not impose a license fee, royalty, or other charge for exercise of
rights granted under this License, and you may not initiate litigation
(including a cross-claim or counterclaim in a lawsuit) alleging that
any patent claim is infringed by making, using, selling, offering for
sale, or importing the Program or any portion of it.

  11. Patents.

  A "contributor" is a copyright holder who authorizes use under this
License of the Program or a work on which the Program is based.  The
work thus licensed is called the contributor's "contributor version".

  A contributor's "essential patent claims" are all patent claims
owned or controlled by the contributor, whether already acquired or
hereafter acquired, that would be infringed by some manner, permitted
by this License, of making, using, or selling its contributor version,
but do not include claims that would be infringed only as a
consequence of further modification of the contributor version.  For
purposes of this definition, "control" includes the right to grant
patent sublicenses in a manner consistent with the requirements of
this License.

  Each contributor grants you a non-exclusive, worldwide, royalty-free
patent license under the contributor's essential patent claims, to
make, use, sell, offer for sale, import and otherwise run, modify and
propagate the contents of its contributor version.

  In the following three paragraphs, a "patent license" is any express
agreement or commitment, however denominated, not to enforce a patent
(such as an express permission to practice a patent or covenant not to
sue for patent infringement).  To "grant" such a patent license to a
party means to make such an agreement or commitment not to enforce a
patent against the party.

  If you convey a covered work, knowingly relying on a patent license,
and the Corresponding Source of the work is not available for anyone
to copy, free of charge and under the terms of this License, through a
publicly available network server or other readily accessible means,
then you must either (1) cause the Corresponding Source to be so
available, or (2) arrange to deprive yourself of the benefit of the
patent license for this particular work, or (3) arrange, in a manner
consistent with the requirements of this License, to extend the patent
license to downstream recipients.  "Knowingly relying" means you have
actual knowledge that, but for the patent license, your conveying the
covered work in a country, or your recipient's use of the covered work
in a country, would infringe one or more identifiable patents in that
country that you have reason to believe are valid.

  If, pursuant to or in connection with a single transaction or
arrangement, you convey, or propagate by procuring conveyance of, a
covered work, and grant a patent license to some of the parties
receiving the covered work authorizing them to use, propagate, modify
or convey a specific copy of the covered work, then the patent license
you grant is automatically extended to all recipients of the covered
work and works based on it.

  A patent license is "discriminatory" if it does not include within
the scope of its coverage, prohibits the exercise of, or is
conditioned on the non-exercise of one or more of the rights that are
specifically granted under this License.  You may not convey a covered
work if you are a party to an arrangement with a third party that is
in the business of distributing software, under which you make payment
to the third party based on the extent of your activity of conveying
the work, and under which the third party grants, to any of the
parties who would receive the covered work from you, a discriminatory
patent license (a) in connection with copies of the covered work
conveyed by you (or copies made from those copies), or (b) primarily
for and in connection with specific products or compilations that
contain the covered work, unless you entered into that arrangement,
or that patent license was granted, prior to 28 March 2007.

  Nothing in this License shall be construed as excluding or limiting
any implied license or other defenses to infringement that may
otherwise be available to you under applicable patent law.

  12. No Surrender of Others' Freedom.

  If conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot convey a
covered work so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you may
not convey it at all.  For example, if you agree to terms that obligate you
to collect a royalty for further conveying from those to whom you convey
the Program, the only way you could satisfy both those terms and this
License would be to refrain entirely from conveying the Program.

  13. Remote Network Interaction; Use with the GNU General Public License.

  Notwithstanding any other provision of this License, if you modify the
Program, your modified version must prominently offer all users
interacting with it remotely through a computer network (if your version
supports such interaction) an opportunity to receive the Corresponding
Source of your version by providing access to the Corresponding Source
from a network server at no charge, through some standard or customary
means of facilitating copying of software.  This Corresponding Source
shall include the Corresponding Source for any work covered by version 3
of the GNU General Public License that is incorporated pursuant to the
following paragraph.

  Notwithstanding any other provision of this License, you have
permission to link or combine any covered work with a work licensed
under version 3 of the GNU General Public License into a single
combined work, and to convey the resulting work.  The terms of this
License will continue to apply to the part which is the covered work,
but the work with which it is combined will remain governed by version
3 of the GNU General Public License.

  14. Revised Versions of this License.

  The Free Software Foundation may publish revised and/or new versions of
the GNU Affero General Public License from time to time.  Such new versions
will be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

  Each version is given a distinguishing version number.  If the
Program specifies that a certain numbered version of the GNU Affero General
Public License "or any later version" applies to it, you have the
option of following the terms and conditions either of that numbered
version or of any later version published by the Free Software
Foundation.  If the Program does not specify a version number of the
GNU Affero General Public License, you may choose any version ever published
by the Free Software Foundation.

  If the Program specifies that a proxy can decide which future
versions of the GNU Affero General Public License can be used, that proxy's
public statement of acceptance of a version permanently authorizes you
to choose that version for the Program.

  Later license versions may give you additional or different
permissions.  However, no additional obligations are imposed on any
author or copyright holder as a result of your choosing to follow a
later version.

  15. Disclaimer of Warranty.

  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. Limitation of Liability.

  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.

  17. Interpretation of Sections 15 and 16.

  If the disclaimer of warranty and limitation of liability provided
above cannot be given local legal effect according to their terms,
reviewing courts shall apply local law that most closely approximates
an absolute waiver of all civil liability in connection with the
Program, unless a warranty or assumption of liability accompanies a
copy of the Program in return for a fee.

                     END OF TERMS AND CONDITIONS

            How to Apply These Terms to Your New Programs

  If you develop a new program, and you want it to be of the greatest
possible use to the public, the best way to achieve this is to make it
free software which everyone can redistribute and change under these terms.

  To do so, attach the following notices to the program.  It is safest
to attach them to the start of each source file to most effectively
state the exclusion of warranty; and each file should have at least
the "copyright" line and a pointer to where the full notice is found.

    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Also add information on how to contact you by electronic and paper mail.

  If your software can interact with users remotely through a computer
network, you should also make sure that it provides a way for users to
get its source.  For example, if your program is a web application, its
interface could display a "Source" link that leads users to an archive
of the code.  There are many ways you could offer source, and different
solutions will be better for different programs; see section 13 for the
specific requirements.

  You should also get your employer (if you work as a programmer) or school,
if any, to sign a "copyright disclaimer" for the program, if necessary.
For more information on this, and how to apply and follow the GNU AGPL, see
<https://www.gnu.org/licenses/>.
```


# Local Environment Setup
Source: https://honcho.dev/docs/v3/contributing/self-hosting

Set up a local environment to run Honcho for development, testing, or self-hosting

This guide helps you set up a local environment to run Honcho for development, testing, or self-hosting.

## Overview

By the end of this guide, you'll have:

* A local Honcho server running on your machine
* A PostgreSQL database with pgvector extension
* Basic configuration to connect your applications
* A working environment for development or testing

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

* **uv** - Python package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh` or `brew install uv`
* **Git** - [Download from git-scm.com](https://git-scm.com/downloads)
* **Docker** (required for Docker setup, not needed for manual setup) - [Download from docker.com](https://www.docker.com/products/docker-desktop/)

### Database Options

You'll need a PostgreSQL database with the pgvector extension. Choose one:

* **Local PostgreSQL** - Install locally or use Docker
* **Supabase** - Free cloud PostgreSQL with pgvector
* **Railway** - Simple cloud PostgreSQL hosting
* **Your own PostgreSQL server**

## LLM Setup

Honcho uses LLMs for memory extraction, summarization, dialectic chat, and dreaming. The server will **fail to start** without a provider configured.

If you keep the built-in defaults, you only need one API key: all text-generation features default to `openai / gpt-5.4-mini`, and embeddings default to `openai / text-embedding-3-small`. Any OpenAI-compatible endpoint works too — OpenRouter, Together, Fireworks, Ollama, vLLM, or LiteLLM. Models must support tool calling (function calling).

After copying `.env.template` to `.env`, the default setup is:

```bash theme={null}
# Required for the built-in defaults
LLM_OPENAI_API_KEY=sk-...
```

If you want a different model or an OpenAI-compatible proxy, uncomment and edit the relevant `*_MODEL_CONFIG__TRANSPORT`, `*_MODEL_CONFIG__MODEL`, and `*_MODEL_CONFIG__OVERRIDES__BASE_URL` lines in the Deriver, Dialectic, Summary, and Dream sections. For example:

```bash theme={null}
LLM_OPENAI_API_KEY=sk-or-v1-...

DERIVER_MODEL_CONFIG__TRANSPORT=openai
DERIVER_MODEL_CONFIG__MODEL=google/gemini-2.5-flash
DERIVER_MODEL_CONFIG__OVERRIDES__BASE_URL=https://openrouter.ai/api/v1
```

<Info>
  For recommended model tiers per feature, using multiple providers, or direct vendor API keys, see the [Configuration Guide](./configuration#llm-configuration).
</Info>

<Info>
  **Community quick-start**: [elkimek/honcho-self-hosted](https://github.com/elkimek/honcho-self-hosted) provides a one-command installer with pre-configured model tiers, interactive provider setup, and Hermes Agent integration.
</Info>

## Docker Setup (Recommended)

Docker Compose handles the database, Redis, and Honcho server. The compose file **builds the image from source** (there is no pre-built image on Docker Hub). This requires Docker with BuildKit enabled — see [Troubleshooting](./troubleshooting#docker-build-fails-with-permission-errors) if the build fails.

The compose file is production-oriented by default (ports bound to `127.0.0.1`, restart policies, caching enabled). For development, uncomment the source mounts and monitoring services inside the file.

### 1. Clone the Repository

```bash theme={null}
git clone https://github.com/plastic-labs/honcho.git
cd honcho
```

### 2. Set Up Environment Variables

Copy the example environment file and configure it:

```bash theme={null}
cp .env.template .env
```

Edit `.env` and configure your LLM provider — see [LLM Setup](#llm-setup) above. The database connection is set in the compose file. Auth is disabled by default (`AUTH_USE_AUTH=false`).

### 3. Start the Services

```bash theme={null}
cp docker-compose.yml.example docker-compose.yml
docker compose up -d --build
```

The first build takes a few minutes (compiling from source). Subsequent starts are fast.

This starts four services: **api** (port 8000), **deriver** (background worker), **database** (PostgreSQL with pgvector, port 5432), and **redis** (port 6379). All ports are bound to `127.0.0.1`. Redis caching is enabled by default.

For development, uncomment the source mount and monitoring sections inside `docker-compose.yml` to enable live reload, Prometheus, and Grafana.

### 4. Verify

Migrations run automatically on startup.

```bash theme={null}
# Check all containers are running
docker compose ps

# Health check (confirms the process is up)
curl http://localhost:8000/health

# Check the deriver is processing (look for "polling" or "processing" in logs)
docker compose logs deriver --tail 20
```

For a full end-to-end test, see [Verify Your Setup](#verify-your-setup) below.

## Manual Setup

For more control over your environment, you can set up everything manually.

### 1. Clone and Install Dependencies

```bash theme={null}
git clone https://github.com/plastic-labs/honcho.git
cd honcho

# Install dependencies using uv (this will also set up Python if needed)
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Set Up PostgreSQL

#### Option A: Local PostgreSQL Installation

Install PostgreSQL and pgvector on your system:

**macOS (using Homebrew):**

```bash theme={null}
brew install postgresql
brew install pgvector
```

**Ubuntu/Debian:**

```bash theme={null}
sudo apt update
sudo apt install postgresql postgresql-contrib
# Install pgvector extension (see pgvector docs for your version)
```

**Windows:**
Download from [postgresql.org](https://www.postgresql.org/download/windows/)

#### Option B: Docker PostgreSQL

```bash theme={null}
docker run --name honcho-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d pgvector/pgvector:pg15
```

### 3. Enable Extensions

Connect to PostgreSQL and enable pgvector:

```bash theme={null}
# Connect to PostgreSQL
psql -U postgres

# Enable the pgvector extension on the default database
CREATE EXTENSION IF NOT EXISTS vector;
\q
```

### 4. Configure Environment

Create a `.env` file with your settings:

```bash theme={null}
cp .env.template .env
```

Edit `.env` — configure your LLM provider (see [LLM Setup](#llm-setup) above) and set the database connection:

```bash theme={null}
DB_CONNECTION_URI=postgresql+psycopg://postgres:postgres@localhost:5432/postgres
AUTH_USE_AUTH=false
LOG_LEVEL=DEBUG
```

### 5. Run Database Migrations

```bash theme={null}
# Run migrations to create tables
uv run alembic upgrade head
```

### 6. Start the Server

```bash theme={null}
# Start the development server
uv run fastapi dev src/main.py
```

The server will be available at `http://localhost:8000`.

### 7. Start the Background Worker (Deriver)

In a **separate terminal**, start the deriver background worker:

```bash theme={null}
uv run python -m src.deriver
```

The deriver is essential for Honcho's core functionality. It processes incoming messages to extract observations, build peer representations, generate session summaries, and run dream consolidation. Without it, messages will be stored but no memory or reasoning will occur.

## Cloud Database Setup

If you prefer to use a managed PostgreSQL service:

### Supabase (Recommended)

1. **Create a Supabase project** at [supabase.com](https://supabase.com)
2. **Enable pgvector extension** in the SQL editor:
   ```sql theme={null}
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
3. **Get your connection string** from Settings > Database
4. **Update your `.env` file** with the connection string

### Railway

1. **Create a Railway project** at [railway.app](https://railway.app)
2. **Add a PostgreSQL service**
3. **Enable pgvector** in the PostgreSQL console
4. **Get your connection string** from the service variables
5. **Update your `.env` file**

## Verify Your Setup

Once your Honcho server is running, verify everything is working:

### 1. Health Check

```bash theme={null}
curl http://localhost:8000/health
# {"status":"ok"}
```

Note: `/health` only confirms the process is running. It does not check database or LLM connectivity.

### 2. Smoke Test (database + API)

This confirms the database connection, migrations, and API are all working:

```bash theme={null}
# Create a workspace
curl -s -X POST http://localhost:8000/v3/workspaces \
  -H "Content-Type: application/json" \
  -d '{"name": "test"}' | python3 -m json.tool
```

If you get back a workspace object with an `id`, your database is connected and migrations ran correctly.

### 3. API Documentation

Visit `http://localhost:8000/docs` to see the interactive API documentation.

### 4. Test with SDK

```python theme={null}
from honcho import Honcho

client = Honcho(
    base_url="http://localhost:8000",
    workspace_id="test"
)

peer = client.peer("test-user")
print(f"Created peer: {peer.id}")
```

## Connect Your Application

Now that Honcho is running locally, you can connect your applications:

### Update SDK Configuration

```python theme={null}
# Python SDK
from honcho import Honcho

client = Honcho(
    base_url="http://localhost:8000",
)
```

```typescript theme={null}
// TypeScript SDK
import { Honcho } from '@honcho-ai/sdk';

const client = new Honcho({
  baseUrl: 'http://localhost:8000',
});
```

### Next Steps

* **Configure Honcho**: Visit the [Configuration Guide](./configuration) for model tiers, provider options, and tuning
* **Explore the API**: Check out the [API Reference](../api-reference/introduction)
* **Try the SDKs**: See our [guides](../guides) for examples
* **Join the community**: [Discord](https://discord.gg/honcho)

## Troubleshooting

Running into issues? See the [Troubleshooting Guide](./troubleshooting) for detailed solutions to common problems including:

* Startup failures (missing API keys, database issues)
* Runtime errors ("An unexpected error occurred" on every request)
* Deriver not processing messages
* Database connection and migration issues
* Docker and Redis problems

**Quick checks:**

* Verify the server is running: `curl http://localhost:8000/health`
* Check logs: `docker compose logs api` (Docker) or check terminal output (manual setup)
* Ensure migrations ran: `uv run alembic upgrade head`

## Production Considerations

The default compose file is already production-oriented — ports bound to `127.0.0.1`, restart policies, caching enabled.

### Security

* Set `AUTH_USE_AUTH=true` and generate a JWT secret with `python scripts/generate_jwt_secret.py`
* Use HTTPS via a reverse proxy in front of Honcho. Example with Caddy (automatic TLS):
  ```
  honcho.example.com {
      reverse_proxy localhost:8000
  }
  ```
  Or with nginx:
  ```nginx theme={null}
  server {
      listen 443 ssl;
      server_name honcho.example.com;
      ssl_certificate /etc/letsencrypt/live/honcho.example.com/fullchain.pem;
      ssl_certificate_key /etc/letsencrypt/live/honcho.example.com/privkey.pem;
      location / {
          proxy_pass http://127.0.0.1:8000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }
  }
  ```
* Secure your database with strong credentials and restrict network access
* The production compose binds PostgreSQL and Redis to `127.0.0.1` only — they are not accessible from the network

### Scaling the Deriver

* Increase `DERIVER_WORKERS` (default: 1) for higher message throughput
* You can also run multiple deriver processes across machines — they coordinate via the database queue
* Monitor deriver logs for processing backlog

### Caching

* The production compose enables Redis caching by default (`CACHE_ENABLED=true`)
* For the development compose, enable manually: `CACHE_ENABLED=true`
* Configure `CACHE_URL` to point to your Redis instance (or use a managed Redis service)

### Database Migrations

* Always run `uv run alembic upgrade head` after updating Honcho before starting the server
* Check current migration status with `uv run alembic current`

### LLM Providers

* Ensure your API keys are configured (see [LLM Setup](#llm-setup))
* For alternative providers or per-feature model overrides, see the [Configuration Guide](./configuration#llm-configuration)

### Monitoring

* Enable Prometheus metrics with `METRICS_ENABLED=true`. The API exposes `/metrics` on port 8000, the deriver on port 9090 (internal to its container — not published to the host by default).
* Enable Sentry error tracking with `SENTRY_ENABLED=true`
* The development compose includes Prometheus (host port 9090) and Grafana (host port 3000) for scraping and dashboards. Uncomment those services to enable them.

### Backups

* Set up regular PostgreSQL backups:
  ```bash theme={null}
  # One-off backup
  docker compose exec database pg_dump -U postgres postgres > backup-$(date +%Y%m%d).sql

  # Restore
  cat backup.sql | docker compose exec -T database psql -U postgres postgres
  ```

## Deploying on Fly.io

The API can be deployed on [Fly.io](https://fly.io). Follow the [Fly.io getting-started docs](https://fly.io/docs/getting-started/) to set up your account and install `flyctl`. A sample `fly.toml` is included in the repo for convenience.

<Note>
  The included `fly.toml` does not provision a PostgreSQL database. Stand one up separately (Fly Postgres, Supabase, Neon, or another managed provider) and set `DB_CONNECTION_URI` to point at it.
</Note>

Once `flyctl` is set up, from the repo root:

```bash theme={null}
flyctl launch --no-deploy           # follow the prompts and edit as you see fit
cat .env | flyctl secrets import    # load secrets from .env
flyctl deploy                       # deploy
```

* Back up your `.env` or `config.toml` configuration files


# Troubleshooting
Source: https://honcho.dev/docs/v3/contributing/troubleshooting

Common issues and solutions when self-hosting Honcho

This page covers common issues you may encounter when self-hosting Honcho, what causes them, and how to fix them.

## Startup Failures

### Server won't start: "Missing client for ..."

```
ValueError: Missing client for Deriver: google
```

**Cause:** The server validates at startup that all configured LLM providers have API keys. If a provider is referenced in your configuration but the corresponding API key isn't set, the server refuses to start.

**Fix:** Set the API keys for your configured providers. With default configuration, you need:

```bash theme={null}
LLM_GEMINI_API_KEY=...    # Used by deriver, summary, dialectic minimal/low
LLM_ANTHROPIC_API_KEY=... # Used by dialectic medium/high/max, dream
LLM_OPENAI_API_KEY=...    # Used by embeddings (when EMBED_MESSAGES=true)
```

See the [LLM Setup](/docs/v3/contributing/self-hosting#llm-setup) section for provider configuration. You can change which providers are used in your `.env` or `config.toml` (see [Configuration Guide](./configuration#llm-configuration)).

### Server won't start: "JWT\_SECRET must be set"

```
ValueError: JWT_SECRET must be set if USE_AUTH is true
```

**Cause:** You enabled authentication (`AUTH_USE_AUTH=true`) but didn't provide a JWT secret.

**Fix:** Generate a secret and set it:

```bash theme={null}
python scripts/generate_jwt_secret.py
# Then set the output as:
AUTH_JWT_SECRET=<generated_secret>
```

Or disable authentication for local development: `AUTH_USE_AUTH=false`

## Runtime Errors

### API returns "An unexpected error occurred" on every request

**Cause:** This is almost always a database issue. The health endpoint (`/health`) will return `{"status": "ok"}` even when the database is unreachable because it doesn't check the database connection. The actual error appears in the server logs.

**Common causes and fixes:**

1. **Database is unreachable** — Check that PostgreSQL is running and the `DB_CONNECTION_URI` is correct
2. **Migrations haven't been run** — The server starts successfully without tables, but every API call will fail. Run:
   ```bash theme={null}
   uv run alembic upgrade head
   ```
   In Docker:
   ```bash theme={null}
   docker compose exec api uv run alembic upgrade head
   ```
3. **pgvector extension not installed** — The `vector` extension must be enabled in your database:
   ```sql theme={null}
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

**How to diagnose:** Check the server logs for the actual error. Look for:

* `sqlalchemy.exc.OperationalError` — database connection issue
* `sqlalchemy.exc.ProgrammingError` with "relation does not exist" — migrations not run
* `psycopg.OperationalError` — connection refused or authentication failed

### Health check passes but API calls fail

The `/health` endpoint is a lightweight check that confirms the server process is running. It does **not** verify:

* Database connectivity
* That migrations have been run
* That LLM providers are reachable

To verify full functionality, try creating a workspace:

```bash theme={null}
curl -X POST http://localhost:8000/v3/workspaces \
  -H "Content-Type: application/json" \
  -d '{"name": "test"}'
```

If this succeeds, your database connection and migrations are working.

### Deriver not processing messages

Messages are stored but no observations, summaries, or representations are being generated.

**Common causes:**

1. **Deriver isn't running** — In manual setup, the deriver is a separate process:
   ```bash theme={null}
   uv run python -m src.deriver
   ```
   In Docker, it starts automatically via `docker compose up`.

2. **Deriver can't reach the database** — Check deriver logs for connection errors. The deriver uses the same `DB_CONNECTION_URI` as the API server.

3. **Missing LLM API key for deriver provider** — By default the deriver uses Google Gemini (`LLM_GEMINI_API_KEY`). Check deriver logs for API errors.

4. **Processing backlog** — With `DERIVER_WORKERS=1` (default), high message volume can cause a backlog. Increase workers:
   ```bash theme={null}
   DERIVER_WORKERS=4
   ```

5. **Representation Batch Max** — By default the deriver buffers representation work until a session has enough tokens for that representation, set via `DERIVER_REPRESENTATION_BATCH_MAX_TOKENS`. Sub-threshold tails become eligible after `DERIVER_REPRESENTATION_BATCH_MAX_AGE_SECONDS` (default 1800 seconds), so quiet sessions eventually flush without disabling batching globally. Set the age to `0` for legacy behavior where sub-threshold tails wait indefinitely. See [token batching](/docs/v3/documentation/core-concepts/reasoning#token-batching) for more details

## Alternative Provider Issues

### OpenRouter / custom provider not working

If calls to an OpenAI-compatible proxy fail:

1. **Verify the endpoint and key are set.** Use `transport = "openai"` with a base URL override:
   ```bash theme={null}
   LLM_OPENAI_API_KEY=sk-or-v1-...
   DERIVER_MODEL_CONFIG__OVERRIDES__BASE_URL=https://openrouter.ai/api/v1
   ```

2. **Check model names match the provider's format.** OpenRouter uses `vendor/model` format (e.g., `anthropic/claude-haiku-4-5`), not the raw model ID.

3. **Ensure your model supports tool calling.** The deriver, dialectic, and dream agents require tool use. Check the provider's model page for tool calling support.

4. **Check server logs for the actual error.** API errors from the upstream provider will appear in Honcho's logs with the HTTP status code and message body.

### vLLM / Ollama not responding

1. **Verify the model server is running** and accessible from the Honcho process (or container):
   ```bash theme={null}
   curl http://localhost:8000/v1/models   # vLLM
   curl http://localhost:11434/v1/models  # Ollama
   ```

2. **In Docker**, `localhost` inside a container doesn't reach the host. Use `host.docker.internal` (macOS/Windows) or the host's network IP:
   ```bash theme={null}
   DERIVER_MODEL_CONFIG__OVERRIDES__BASE_URL=http://host.docker.internal:8000/v1
   ```

3. **Structured output failures** — vLLM's structured output support is limited to certain response formats. If you see JSON parsing errors, check the deriver/dream logs for the raw response. See [Deriver produces no observations](#deriver-produces-no-observations) below.

### Deriver produces no observations

If messages are processed (the queue drains, no errors in logs) but peers never accumulate observations — and you're using an OpenAI-compatible provider — the likely cause is that the provider doesn't support OpenAI Structured Outputs (`json_schema`). The OpenAI backend requests `json_schema` by default; providers like **Z.AI GLM** and some **Ollama/vLLM** deployments either reject it or silently ignore it and return prose, which the deriver can't parse into observations.

**Fix:** set `STRUCTURED_OUTPUT_MODE=json_object` on the deriver's model config to request loose JSON mode, which injects the schema into the prompt instead:

```bash theme={null}
DERIVER_MODEL_CONFIG__STRUCTURED_OUTPUT_MODE=json_object
```

This is a per-model-config setting on the OpenAI transport; set it on whichever features use the affected provider (e.g. `DREAM_DEDUCTION_MODEL_CONFIG__STRUCTURED_OUTPUT_MODE`).

### Thinking budget errors with non-Anthropic providers

If you see errors like `thinking budget not supported`, `invalid parameter`, or silent failures where agents produce no output, one of your per-component `*_MODEL_CONFIG__THINKING_BUDGET_TOKENS` overrides is likely set to a value > 0 with a provider that doesn't support Anthropic-style extended thinking. The built-in defaults do not set thinking budgets, so this only applies if you added those overrides yourself.

**Fix:** Set `*_MODEL_CONFIG__THINKING_BUDGET_TOKENS=0` for every component when using models that don't support thinking:

```bash theme={null}
DERIVER_MODEL_CONFIG__THINKING_BUDGET_TOKENS=0
SUMMARY_MODEL_CONFIG__THINKING_BUDGET_TOKENS=0
DREAM_DEDUCTION_MODEL_CONFIG__THINKING_BUDGET_TOKENS=0
DREAM_INDUCTION_MODEL_CONFIG__THINKING_BUDGET_TOKENS=0
DIALECTIC_LEVELS__minimal__MODEL_CONFIG__THINKING_BUDGET_TOKENS=0
DIALECTIC_LEVELS__low__MODEL_CONFIG__THINKING_BUDGET_TOKENS=0
DIALECTIC_LEVELS__medium__MODEL_CONFIG__THINKING_BUDGET_TOKENS=0
DIALECTIC_LEVELS__high__MODEL_CONFIG__THINKING_BUDGET_TOKENS=0
DIALECTIC_LEVELS__max__MODEL_CONFIG__THINKING_BUDGET_TOKENS=0
```

For OpenAI reasoning models, use `*_MODEL_CONFIG__THINKING_EFFORT` instead of `*_MODEL_CONFIG__THINKING_BUDGET_TOKENS`.

## Database Issues

### Connection string format

The connection URI **must** use the `postgresql+psycopg` prefix:

```bash theme={null}
# Correct
DB_CONNECTION_URI=postgresql+psycopg://postgres:postgres@localhost:5432/postgres

# Wrong - will fail
DB_CONNECTION_URI=postgresql://postgres:postgres@localhost:5432/postgres
DB_CONNECTION_URI=postgres://postgres:postgres@localhost:5432/postgres
```

### Checking migration status

```bash theme={null}
# See current migration version
uv run alembic current

# See migration history
uv run alembic history

# Upgrade to latest
uv run alembic upgrade head
```

## Cache & Redis

### Redis is optional

Redis is used for caching when `CACHE_ENABLED=true` (default: `false`). If Redis is unreachable, Honcho **gracefully falls back to in-memory caching** and logs a warning. This means:

* The server and deriver will still start and function normally
* Performance may be reduced under high load without Redis
* You do not need Redis for local development or testing

### Redis connection issues

If you see Redis connection warnings in logs but `CACHE_ENABLED=false`, they can be safely ignored. If you want caching:

```bash theme={null}
# Start Redis via Docker
docker run -d -p 6379:6379 redis:latest

# Configure Honcho
CACHE_ENABLED=true
CACHE_URL=redis://localhost:6379/0
```

## Docker Issues

### Docker build fails with permission errors

The Honcho Dockerfile uses BuildKit mount syntax and creates a non-root `app` user. Common build failures:

**1. BuildKit not enabled**

The Dockerfile uses `RUN --mount=type=cache` which requires Docker BuildKit. If you see syntax errors during build:

```bash theme={null}
# Ensure BuildKit is enabled
DOCKER_BUILDKIT=1 docker compose build
```

Or add to your Docker daemon config (`/etc/docker/daemon.json`):

```json theme={null}
{ "features": { "buildkit": true } }
```

**2. Permission denied during build or at runtime (Linux)**

On Linux, AppArmor or SELinux can block Docker build operations and volume mounts. Symptoms include permission denied errors during `COPY`, `RUN`, or when the container tries to access mounted volumes.

```bash theme={null}
# Check if AppArmor is blocking Docker
sudo aa-status | grep docker

# Temporarily test without AppArmor (for diagnosis only)
docker compose down
sudo aa-remove-unknown
docker compose up -d
```

For SELinux, add `:z` to volume mounts in `docker-compose.yml`:

```yaml theme={null}
volumes:
  - .:/app:z
```

**3. Volume mount UID mismatch**

The Dockerfile creates a non-root `app` user, but `docker-compose.yml.example` mounts `.:/app` which overlays the container filesystem with host-owned files. The `app` user inside the container may not have permission to read them.

If you see permission errors at runtime (not build time), you can either:

* Run without the source mount (remove `- .:/app` from volumes — the image already contains the code)
* Or fix ownership: `sudo chown -R 100:101 .` (matches the `app` user inside the container)

### Containers start but API fails

1. Check container status: `docker compose ps`
2. Check API logs: `docker compose logs api`
3. Check database logs: `docker compose logs database`
4. Ensure migrations ran: `docker compose exec api uv run alembic upgrade head`

### Port conflicts

If port 8000 is already in use:

```bash theme={null}
# Check what's using the port
lsof -i :8000

# Or change the port mapping in docker-compose.yml
ports:
  - "8001:8000"  # Map to a different host port
```

### Rebuilding after code changes

```bash theme={null}
docker compose build --no-cache
docker compose up -d
```

## Getting Help

If your issue isn't covered here:

* **Check the logs** — most issues are diagnosed from server or deriver logs
* **GitHub Issues** — [Report bugs](https://github.com/plastic-labs/honcho/issues)
* **Discord** — [Join our community](https://discord.gg/plasticlabs)
* **Configuration** — See the [Configuration Guide](./configuration) for all available settings


# Architecture & Intuition
Source: https://honcho.dev/docs/v3/documentation/core-concepts/architecture

Understanding Honcho's core concepts and data model.

Honcho is memory infrastructure that continuously [*reasons*](/docs/v3/documentation/core-concepts/reasoning) about data to build rich representations of peers (users, agents, or any entity) over time. This document explains the data model, system components, and how data flows through Honcho.

## Data Model

Honcho has a hierarchical data model centered around the entities below.

```mermaid theme={null}
 graph LR
      W[Workspaces] -->|have| P[Peers]
      W -->|have| S[Sessions]

      S -->|have| SM[Messages]

      P <-.->|many-to-many| S

      style W fill:#B6DBFF,stroke:#333,color:#000
      style P fill:#B6DBFF,stroke:#333,color:#000
      style S fill:#B6DBFF,stroke:#333,color:#000
      style SM fill:#B6DBFF,stroke:#333,color:#000
```

* A Workspace has Peers & Sessions
* A Peer can be in multiple Sessions and can send Messages in a Session
* A Session can have many Peers and stores Messages sent by its Peers

### <Icon icon="building" /> Workspaces

Workspaces are the top-level containers in Honcho. They provide complete isolation between different applications or environments, essentially serving as a namespace to keep different workloads separate. You might use separate workspaces for development, staging, and production environments, or to isolate different product lines. They also enable multi-tenant SaaS applications where each customer gets their own isolated workspace with complete data separation.

Authentication is scoped to the workspace level, and configuration settings can be applied workspace-wide to control behavior across all peers and sessions within that workspace.

***

### <Icon icon="user" /> Peers

Peers are the most important entity in Honcho--everything revolves around building and maintaining their [*representations*](/docs/v3/documentation/core-concepts/representation). A peer represents any individual user, agent, or entity in a workspace. Treating humans and agents the same way lets you build arbitrary combinations for multi-agent or group chat scenarios.

Each peer has a unique identifier within a workspace and is a container for reasoning across all their sessions. This cross-session context means conclusions drawn about a peer in one session can inform interactions in completely different sessions. Peers can be configured to control whether Honcho reasons about them.

You can use peers for any entity that persists over time--individual users in chatbot applications, AI agents interacting with users or other agents, customer profiles in support systems, student profiles in educational platforms, or even NPCs in role-playing games.

***

### <Icon icon="message" /> Sessions

Sessions represent interaction threads or contexts between peers. A session can involve multiple peers and provides temporal boundaries for when a set of interactions starts and ends. This lets you scope context and memory to specific interactions while still maintaining longer-term peer representations that span sessions.

Use sessions to scope things like support tickets, meeting transcripts, learning sessions, or conversations. You can also use single-peer sessions as a way to import external data--create a session with just one peer and structure emails, documents, or files as messages to enrich that peer's representation.

Session-level configuration gives you fine-grained control over perspective-taking behavior. You can configure whether a peer should form representations of other peers in the session, and whether other peers should form representations of them.

***

### <Icon icon="envelope" /> Messages

Messages are the fundamental units of interaction within sessions. While they typically represent back-and-forth communication between peers, you can also use messages to ingest any information that provides context--emails, documents, files, user actions, system notifications, or rich media content.

Every message is attributed to a specific peer and ordered chronologically within its session. When messages are created, they trigger automatic background reasoning that updates peer representations. Messages support rich metadata and structured data through JSONB fields, making them flexible enough to capture whatever information matters for your use case.

## Data Flow

Understanding how data moves through Honcho helps clarify the architecture.

When you create messages, they're immediately written to PostgreSQL and reasoning tasks are added to background queues. Background workers then generate logic, summaries, and new insights to improve representations. These conclusions and insights get stored in vector collections for retrieval. This async approach ensures fast writes while still providing rich reasoning capabilities.

When you need context from Honcho, you query through the "Chat" endpoint or "Get Context" endpoint. Honcho retrieves relevant conclusions from vector storage along with recent messages, then assembles everything into coherent context ready to inject into agent prompts.

<img alt="Honcho Architecture" />

The diagram above shows how agents write messages to Honcho, which triggers reasoning that updates peer representations. Agents can then query representations to get additional context for their next response. Black arrows represent read/write of regular data (messages, storage), while red arrows represent read/write of reasoned-over data (logic, peer representations).

### Under the Hood: Write, Reasoning, and Query Paths

Honcho runs as two cooperating processes: an **API server** that handles requests and enqueues background work, and a **worker** that consumes that work off the queue. This split is what keeps the write path fast--your request never waits on an LLM call.

<img alt="Honcho Detailed Internals" />

**Write path (synchronous).** A message is stored and a reasoning task is enqueued in the same request; the API returns immediately. Nothing about the reasoning that follows blocks the caller.

**Deriver + Summarizer (async, per-message).** The worker picks up queued tasks in small batches. The Deriver reads new messages and extracts conclusions about the peer--explicit statements and direct deductions. In parallel, the Summarizer periodically rolls up recent messages into short- and long-form session summaries. Both run per-message (well, per-batch) rather than on a schedule.

**Dreamer (periodic).** On a schedule (or triggered on demand), the Dreamer revisits existing conclusions to consolidate and deepen them: removing redundant or stale ones, drawing inductive conclusions across patterns that span multiple messages, and updating peer cards--compact biographical summaries of a peer. This is where memory gets richer over time, not just larger.

**Query path (Dialectic).** A `chat()` call spawns a Dialectic agent that answers your question by exploring memory--searching conclusions semantically, pulling supporting messages, and tracing a conclusion back to the premises it was drawn from--before synthesizing a grounded answer. This all happens inline during the request, since answering well is worth the latency that write-path reasoning is designed to avoid.

## Configuration & Extensibility

Honcho is designed to be flexible. Settings cascade hierarchically from workspace to peer to session, so you can set defaults at the workspace level and override them for specific peers or sessions. Feature flags let you enable or disable reasoning modes, perspective tracking, and other capabilities. You can bring your own LLM provider--OpenAI, Anthropic, or custom endpoints--and metadata fields let you extend any primitive with custom JSON data. Batch operations let you create up to 100 messages in a single API call for efficient bulk ingestion.

## Design Principles

Honcho's architecture follows a few core principles. Everything revolves around building representations of peers (peer-centric). Memory isn't just storage--it's continual learning (reasoning-first). Long-lived operations happen in the background so they don't block user interactions (async by default). The system works with any LLM provider (provider-agnostic) and is built for isolation and scalability from the ground up (multi-tenant). Users and agents are both represented as peers, which enables flexible scenarios you couldn't easily model with a traditional user-assistant paradigm (unified paradigm).

## Next Steps

<CardGroup>
  <Card title="Get an API Key" icon="key" href="https://app.honcho.dev">
    Sign up for the Honcho platform and start building
  </Card>

  <Card title="Quickstart" icon="rocket" href="/v3/documentation/introduction/quickstart">
    Get started with your first integration
  </Card>

  <Card title="Reasoning" icon="gears" href="/v3/documentation/core-concepts/reasoning">
    Learn how Honcho reasons about messages to build memory
  </Card>

  <Card title="Peer Representations" icon="user-magnifying-glass" href="/v3/documentation/core-concepts/representation">
    Understand what peer representations are and how they work
  </Card>
</CardGroup>


# Design Patterns
Source: https://honcho.dev/docs/v3/documentation/core-concepts/design-patterns

Design your workspace, peers, and sessions for common application patterns

<Info>
  This page covers **how to structure** workspaces, peers, and sessions for real applications. For the conceptual model behind them, start with [Architecture](/docs/v3/documentation/core-concepts/architecture).

  Ready to add Honcho to your codebase? The **`/honcho-integration` skill** applies these patterns for you — it explores your code, asks how your peers and sessions should map to your app, and wires in the Honcho SDK. Run it in any coding agent that supports skills (Claude Code, Cursor, and others).
</Info>

## Quick Reference

**Workspaces isolate, peers persist, and sessions scope the active context.**

| Decision                               | Recommendation                                                                                                                                                                                             |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| How many workspaces?                   | One workspace per application, tool, tenant, or collaboration boundary. Split workspaces only when you need hard isolation between products, customers, environments, or agents.                           |
| When should agents share a workspace?  | When agents collaborate over the same product, project, team, user, customer, or game state. Separate them when they should not see or influence each other's memory.                                      |
| Who should be a peer?                  | Any persistent participant whose messages should be attributed or reasoned about: users, agents, assistants, NPCs, students, or customers. Use one peer for the same entity across sessions and platforms. |
| How should I scope sessions?           | Scope sessions to the active interaction: per-conversation, per-channel, per-task run, per-project, per-import, or other bounded context. Reuse a session when local context should keep accumulating.     |
| How does cross-session reasoning work? | Session memory stays local to one session. Peer representations accumulate across every session where the peer is included, and `session.context()` becomes cross-session when you include a peer target.  |
| Should I set `observe_me: false`?      | Yes, for deterministic peers Honcho does not need to model, like bots or tool agents. Still save their messages so other peers have session context. Keep it enabled for users and evolving agents.        |
| Do I need `observe_others`?            | Only when a peer needs its own perspective on another participant, such as in games, multi-agent systems, or parent/subagent workflows.                                                                    |

## Workspace Design

A workspace is a hard isolation boundary. **Default to one workspace per application,** and split only at a real privacy, compliance, or product boundary (e.g. per-tenant SaaS, or a tool that needs intentionally isolated memory). Agents that collaborate over the same product, user, or game state belong in the *same* workspace so each can retrieve what the others produced.

Honcho plugins default to one workspace *per host* (`hermes`, `claude_code`, `cursor`, `opencode`). To unify memory across them, point each at the same workspace — see [Unified Memory Setup](/docs/v3/guides/recipes/unified-memory-setup).

<Info>
  The SDK creates a workspace called `default` when no `workspace_id` is specified.
</Info>

***

## Peer Design

Give each real-world entity **one** stable peer ID and reuse it everywhere — splitting one entity across `user-web`, `user-discord`, and `user-slack` builds three separate representations. Prefix IDs by source for multi-channel apps (`discord_491827364`), and if a peer goes by multiple names, store the aliases in its peer card with `set_card()` / `setCard()`.

<Tip>
  For unified context across Honcho plugins, set the same user peer ID (`peerName`) everywhere — that shared ID is what connects memory across Claude Code, Cursor, OpenCode, and your own app. See [Unified Memory Setup](/docs/v3/guides/recipes/unified-memory-setup).
</Tip>

***

## Session Design

Sessions define the temporal boundaries of an interaction. How you scope them affects how summaries are generated, how context is retrieved, and when reasoning fires.

**Common session patterns**

| Pattern          | Session scoped to            | Example                                                        |
| ---------------- | ---------------------------- | -------------------------------------------------------------- |
| Per-conversation | Each new chat thread         | ChatGPT or Claude Code style UI where each thread is a session |
| Per-channel      | A persistent channel or room | Discord channel, Slack thread                                  |
| Per-interaction  | A bounded task or encounter  | A support ticket, a game encounter                             |
| Per-project      | A persistent work area       | Coding agent memory for one repository                         |
| Per-import       | A batch of external data     | Importing emails or documents for a single peer                |

Create a **new** session when context resets (new conversation, new day, new topic); **reuse** one when context should keep accumulating (ongoing channel, persistent thread).

<Warning>
  **Don't scope sessions too thin.** Honcho batches reasoning until a peer accumulates \~1,000 tokens *within a single session*, with a default age-based flush for quiet tails ([token batching](/docs/v3/documentation/core-concepts/reasoning#token-batching)). Low-volume or trickle inputs should still append to one ongoing session rather than fragment across many, so reasoning runs with useful context instead of many small delayed batches.
</Warning>

**How cross-session reasoning works**

* **Session memory** is local to an interaction — summaries and recent-message context describe only what happened there.
* **Peer memory** (representations) accumulates reasoning across every session the peer is part of.

So you can start a session fresh or pull in a peer's long-term memory. [`session.context()`](/docs/v3/documentation/features/get-context) returns the current session's summary and recent messages; add a [peer target](/docs/v3/documentation/features/get-context#peer-representation-in-context) to fold in that peer's cross-session history.

***

## Common Mistakes

* **Splitting one identity across peer IDs** -- If the same user is `alice`, `alice-discord`, and `alice-cursor`, Honcho builds separate representations. Use one stable peer ID when you want unified memory.
* **Too many tiny sessions** -- Summaries and recent messages are session-scoped, and reasoning only fires past \~1,000 tokens per session. Splitting a continuous conversation across many sessions fragments local context and can stall reasoning. Reuse a session when context should flow continuously.
* **Separating agents that should collaborate** -- If agents need shared product, customer, or team context, put them in the same workspace. Separate workspaces are hard isolation boundaries.
* **Leaving `observe_me` on for assistants** -- Wastes reasoning compute on a peer you control. Deterministic behavior doesn't need to be modeled.
* **Turning on `observe_others` everywhere** -- Directional representations are powerful, but they add complexity. Use them when peers need distinct perspectives, not just because a session has multiple peers.
* **Forgetting `peer_target` on session context** -- `session.context()` defaults to the active session's summary and recent messages, which are session-scoped. It becomes cross-session only through adding a peer\_target which includes the peer representation.
* **Blocking on processing** -- Messages are processed asynchronously in the background. Don't poll or wait for reasoning to complete before continuing your application flow.

## Next Steps

<CardGroup>
  <Card title="Unified Memory Setup" icon="diagram-project" href="/v3/guides/recipes/unified-memory-setup">
    Wire these patterns into one shared workspace across four integrations
  </Card>

  <Card title="Get Context" icon="messages" href="/v3/documentation/features/get-context">
    Retrieve formatted context from sessions for your LLM
  </Card>

  <Card title="Chat Endpoint" icon="comments" href="/v3/documentation/features/chat">
    Query Honcho about your peers with natural language
  </Card>

  <Card title="Reasoning Configuration" icon="wrench" href="/v3/documentation/features/advanced/reasoning-configuration">
    Fine-tune what gets reasoned about and how
  </Card>
</CardGroup>


# Honcho Reasoning
Source: https://honcho.dev/docs/v3/documentation/core-concepts/reasoning



Honcho is a memory system that *reasons*. You can read more on the philosophy behind the approach [here](https://blog.plasticlabs.ai/blog/Memory-as-Reasoning), but practically speaking, the system runs inference on data in the background to produce the highest quality context for simulating statefulness. This document explains why reasoning is necessary and how Honcho implements it.

<Note>
  If you'd like to experience this methodology first-hand, try out [Honcho Chat](https://honcho.chat)--an interface to your personal memory. Read more [here](https://blog.plasticlabs.ai/blog/Introducing-Honcho-Chat)!
</Note>

## Why Reasoning?

Traditional RAG systems treat memory as static storage--they retrieve what was explicitly said when semantically similar queries appear. Other solutions take an opinion for you on what's important to store, whether through structured facts in databases or predefined knowledge graphs. Honcho takes a different approach: we extract all latent information by reasoning about everything, so it's there when you need it. Our job is to produce the most robust reasoning possible--it's your job as a developer to decide what's relevant for your use case.

We extract this latent information through formal logic. Formal logical reasoning is AI-native--LLMs perform the rigorous, compute-intensive thinking that humans struggle with, instantly and consistently. This unlocks insights that are only accessible by *rigorously thinking* about your data, generating new understanding that goes beyond simple recall.

## Formal Logic Framework

Honcho's memory system is powered by custom models trained to perform formal logical reasoning. The system extracts what was explicitly stated, draws certain conclusions from those, identifies patterns across multiple conclusions, and infers the simplest explanations for behavior.

Why formal logic specifically? LLMs are uniquely well-suited for this reasoning task--it's well-represented in the pretraining data. LLMs can maintain consistent reasoning across thousands of conclusions without cognitive fatigue or belief resistance--which is extremely hard for humans to do reliably. The outputs are also composable, meaning logical conclusions can be stored, retrieved, and combined programmatically for dynamic context assembly.

Here's an example of a data structure the reasoning models generate:

```json theme={null}
{
    "explicit": [
        {
            "content": "premise 1"
        },
        ...
        {
            "content": "premise n"
        }
    ],
    "deductive": [
        {
            "premises": [
                "premise 1",
                ...
                "premise n"
            ],
            "conclusion": "conclusion 1"
        },
        ...
    ]
}
```

The explicit reasoning model ([Neuromancer XR](https://blog.plasticlabs.ai/research/Introducing-Neuromancer-XR)) outputs its "thinking" followed by things that were explicitly stated, which serve as premises to scaffold deductive conclusions. It's on top of this reasoning foundation that further reasoning is scaffolded. Currently that includes peer cards (key biographical information about the peer), consolidation (identifying redundant or contradictory information), induction (pattern recognition across multiple messages), and abduction (inferring the simplest explanations for observed behavior).

The reasoning that Honcho does is something we're constantly iterating and improving on. Our goal is simple--provide the richest, most relevant context in the fastest, cheapest way possible in order to simulate statefulness in whatever setting you need.

Two components produce this logic: the **Deriver** extracts explicit and deductive conclusions from incoming messages as they arrive, and the **Dreamer** periodically revisits stored conclusions to consolidate them and draw inductive conclusions across patterns spanning multiple messages. See [Architecture](/docs/v3/documentation/core-concepts/architecture) for how these fit into the request/background split.

## How It Works

When you write messages to Honcho, they're stored immediately and enqueued for background processing. Reasoning asynchronously ensures fast writes while still providing rich reasoning capabilities. Messages are stored immediately without blocking, and session-based queues maintain chronological consistency so reasoning tasks affecting the same peer representation are always processed in order.

The reasoning outputs--conclusions, summaries, peer cards--are stored as part of peer representations, indexed in vector collections for retrieval.

<img alt="Diagram for reasoning in Honcho" />

The diagram above shows how agents write messages to Honcho, which triggers reasoning that updates peer representations. Agents can then query representations to get additional context for their next response.

### Token Batching

Rather than running inference on every individual message, Honcho accumulates messages in the queue and processes them as a batch once the total token count of pending messages for a given peer representation crosses a threshold--roughly **1,000 tokens** at the current batch size. This keeps ingestion costs down, since Honcho charges based on reasoning passes, and ensures each pass has a meaningful amount of context to work with. At \~1,000 tokens the batch comfortably fits in the context window of any modern LLM, so no content is lost.

If a user sends several short messages in a row (e.g., "yes", "ok", "sounds good"), those messages sit in the queue until enough content has accumulated. Once the threshold is met, the full batch is processed together in a single reasoning call.

<Note>
  This batching only applies to **representation** tasks (conclusion extraction). Summary and dream tasks have their own scheduling logic and are not subject to the token threshold.
</Note>

## Balances & Design Choices

Off-the-shelf LLMs can perform formal logical reasoning, but they aren't optimized for it. Honcho uses custom models trained specifically for logical rigor (following formal reasoning rules rather than plausible-sounding text), structured output (consistent JSON schema with premises and conclusions), and efficiency (smaller, faster models tuned for this specific task). This allows Honcho to reason more reliably and at lower cost than general-purpose frontier LLMs.

The approach balances quality with practical constraints. Custom models are smaller and cheaper to run, scaffolded conclusions are more token-efficient than raw conversation history, and we batch where appropriate to optimize update frequency.

Honcho's reasoning capabilities are actively being improved. Current areas of development include enhanced inductive and abductive reasoning, multi-hop  and temporal reasoning, and expanded file types and modalities. The system is designed to be extensible--new reasoning capabilities can be added without breaking existing functionality.

<Note>
  If you find that the data you're uploading to Honcho isn't being reasoned over to your liking, we'd love to improve it for you and ingest your data for free--reach out via [Discord](https://discord.gg/honcho) or [email](mailto:support@plasticlabs.ai)!
</Note>

## Next Steps

Without exhaustive reasoning, you're stuck with surface-level retrieval or someone else's opinion on what matters. You can't effectively simulate statefulness if you're not reasoning about everything in the present--coherence plummets, trust falls, and users churn. Don't leave key information on the table. Use Honcho to give your agents the context they need to reconstruct the past as comprehensively as possible and maintain coherence--for your use case.

<CardGroup>
  <Card title="Get an API Key" icon="key" href="https://app.honcho.dev">
    Sign up for the Honcho platform and start building
  </Card>

  <Card title="Quickstart" icon="rocket" href="/v3/documentation/introduction/quickstart">
    Get started with your first integration
  </Card>

  <Card title="Architecture" icon="sitemap" href="/v3/documentation/core-concepts/architecture">
    See how reasoning fits into Honcho's overall architecture
  </Card>

  <Card title="Peer Representations" icon="user-magnifying-glass" href="/v3/documentation/core-concepts/representation">
    Learn how reasoning produces peer representations
  </Card>
</CardGroup>


# Peer Representations
Source: https://honcho.dev/docs/v3/documentation/core-concepts/representation



A representation is the collection of reasoning Honcho has done about a peer over time. It's the continual learning about a peer over every message that's been written to it. Representations evolve dynamically as new messages come in, with Honcho reasoning about them in the background.

When you write messages to Honcho, the reasoning models extract premises, draw conclusions, and scaffold new conclusions as well. All of that reasoning gets stored as the peer's representation. Think of it as Honcho's understanding of who that peer is, what they care about, and how they behave, built through formal logic rather than simple storage.

## What's in a Representation?

A peer representation is made up of several types of artifacts that Honcho generates through [*reasoning*](/docs/v3/documentation/core-concepts/reasoning):

**Conclusions** are insights derived through formal logic. Deductive conclusions are things Honcho can be certain about based on extracted premises. Inductive conclusions identify patterns across multiple messages. Abductive conclusions infer the simplest explanations for observed behavior. For example, if a user frequently mentions work deadlines and rarely mentions hobbies, Honcho might inductively conclude they're time-constrained or career-focused.

**Summaries** capture the essence of sessions. Short summaries are generated every 20 messages by default, and long summaries every 60 messages. These help compress conversation history into dense, queryable context.

**Peer cards** contain key biographical information. They essentially cache the most basic information about a peer (name, occupation, interests) to ensure the model never loses its grounding.

These enable continuous improvement. Each new message refines conclusions, updates summaries, and keeps peer cards current—building a more accurate representation over time.

## Observation & Perspective-Taking

Honcho can build different representations based on what each peer observes. This enables sophisticated multi-peer scenarios where understanding is relative to what was actually witnessed.

There are two observation modes controlled by [configuration](/docs/v3/documentation/features/advanced/configuration):

**Honcho observing peers** (`observe_me`): When enabled (default), Honcho forms a representation of the peer based on all messages they've sent across all sessions. This is Honcho's understanding of that peer, built from everything they've said and done in your system. Set `observe_me: false` if you don't want Honcho to reason about that peer at all.

**Peers observing others** (`observe_others`): When enabled at the session level, a peer will form representations of other peers in that session based only on messages they've observed. If Alice and Bob are in a session together and Alice has `observe_others: true`, Alice will form a representation of Bob based solely on what Bob said in sessions Alice participated in. Alice's representation of Bob will be completely different from Charlie's representation of Bob if they've observed different interactions.

In the diagram below, assume `observe_me` isn't turned off (again, default behavior) and `observe_others` is turned on for both peers in a session that contains the peers Alice and Bob.

<img alt="" />

The shared session that Alice and Bob have informs their respective representations of each other. Alice has a small set of conclusions that pertain to Bob, and Bob has a small set of conclusions that pertain to Alice. Honcho can observe the totality of each peer's interactions, forming representations of the peers themselves, and enable peers to store conclusions about peers they interact with based only on what they witness in shared sessions.

Why would you want peers observing others? So you can simulate stateful *perspectives*. If Bob participates with Alice in sessions 1 and 2, while Charlie participates with Alice in session 3, Bob's representation of Alice will be built from sessions 1 and 2, while Charlie's representation will only include what happened in session 3. Bob can reference shared history, inside jokes, or past conflicts that Charlie knows nothing about. Without perspective-based segmentation, all agents are omniscient--the simulation breaks down, trust falls apart, and users churn.

## Why Representations Work

Statefulness is simulated through reconstruction of the past. Traditional systems reconstruct by retrieving stored facts, querying semantically similar items, and hoping the LLM does the rest. Honcho reconstructs through reasoning about the past exhaustively, leaving much less to chance.

Reasoning can surface insights never explicitly stated. If a user mentions they're saving for a house in one session and complains about subscription costs in another, Honcho can conclude they're budget-conscious without anyone saying it. Reasoning handles contradictions gracefully--when new information conflicts with old conclusions, it reconciles them instead of just accumulating more data. And reasoning enables prediction under uncertainty, inferring what's likely true based on patterns even when data is incomplete.

Humans reconstruct the past from imperfect recollections, then act on those reconstructions as if they were complete. Representations enable agents to do the same with far greater fidelity. Reasoning produces an exhaustive, explicit record of what can be concluded about a peer--giving agents complete recollection that humans can only pretend to have. That's what makes truly stateful agents possible.

## Next Steps

<CardGroup>
  <Card title="Get an API Key" icon="key" href="https://app.honcho.dev">
    Sign up for the Honcho platform and start building
  </Card>

  <Card title="Quickstart" icon="rocket" href="/v3/documentation/introduction/quickstart">
    See representations in action with a working example
  </Card>

  <Card title="Architecture" icon="sitemap" href="/v3/documentation/core-concepts/architecture">
    Understand how representations fit into Honcho's architecture
  </Card>

  <Card title="Chat Endpoint" icon="comments" href="/v3/documentation/features/chat">
    Chat with Honcho about your users
  </Card>
</CardGroup>


# Dreaming
Source: https://honcho.dev/docs/v3/documentation/features/advanced/dreaming

How Honcho continuously improves memory through autonomous consolidation

<Warning>
  Dreaming is an experimental feature under active development. The scheduling heuristics, specialist behavior, and configuration options described here are subject to change as we iterate on the approach.
</Warning>

Honcho's reasoning system extracts conclusions from every message as it arrives. Over time, this produces a large body of knowledge--some of which is redundant, outdated, or missing higher-order patterns that only become visible across many interactions. **Dreaming** is the process that addresses this: an autonomous, periodic consolidation cycle that refines the peer representation by reasoning over existing conclusions.

Think of it like sleep for a memory system. The "waking" reasoning process captures what happened. The dreaming process reflects on what it all means.

## What Dreaming Does

A dream cycle runs two specialized agents in sequence:

### 1. Deduction

The deduction specialist performs logical inference over existing conclusions. It autonomously explores the observation space and looks for:

* **Knowledge updates**: When the same fact has changed over time (e.g., "works at Company A" followed later by "works at Company B"), it deletes the outdated conclusion and creates a new one reflecting the current state.
* **Logical implications**: Conclusions that follow necessarily from existing premises but weren't captured during real-time processing.
* **Contradictions**: Conflicting conclusions that need resolution.
* **Peer card updates**: Key biographical facts (name, location, occupation) that should be recorded on the peer card for quick access.

### 2. Induction

The induction specialist identifies patterns across multiple conclusions. It looks for:

* **Behavioral tendencies**: Recurring behaviors observed across different contexts (e.g., "tends to reschedule meetings when stressed").
* **Preferences**: Consistent choices that indicate underlying preferences.
* **Personality traits**: Stable characteristics inferred from multiple data points.
* **Correlations**: Relationships between different aspects of behavior.

Inductive conclusions require evidence from at least two source conclusions--patterns need more than a single data point. Each pattern is assigned a confidence level based on the number of supporting observations.

## When Dreams Are Scheduled

Dreams are triggered automatically based on a set of heuristics designed to balance freshness with efficiency:

### Conditions

All of the following must be true for a dream to be scheduled:

1. **Document threshold**: At least 50 new conclusions have been created since the last dream for that peer representation.
2. **Minimum cooldown**: At least 8 hours have passed since the last dream for that peer representation.
3. **Dreaming is enabled**: The workspace and/or session configuration has `dream.enabled` set to `true` (the default).

### Idle timeout

When the threshold conditions are met, a dream is **not** immediately executed. Instead, a timer is set (default: 60 minutes) that waits for user inactivity. If new messages arrive during the waiting period, the pending dream is cancelled and the timer resets. This prevents dreaming while the user is actively interacting, ensuring the system consolidates only after the conversation has settled.

Once the idle timeout expires without interruption, the dream task is enqueued for processing.

### Manual scheduling

You can also trigger a dream explicitly via the API:

<CodeGroup>
  ```python Python theme={null}
  honcho.workspaces.schedule_dream(
      observer="user-peer-name",
      observed="user-peer-name",
  )
  ```

  ```typescript TypeScript theme={null}
  await honcho.workspaces.scheduleDream({
      observer: "user-peer-name",
      observed: "user-peer-name",
  });
  ```
</CodeGroup>

Manual dreams bypass the threshold and cooldown checks, but are still subject to deduplication--if a dream is already pending or in progress for the same peer representation, the request is a no-op.

## Scope

Dreams operate at the **peer representation** level--specifically, a (workspace, observer, observed) tuple. This means:

* A dream consolidates conclusions for a specific observer's view of a specific observed peer.
* In the common case of self-observation (where the observer and observed are the same peer), the dream consolidates that peer's own representation.
* Dreams do not span across workspaces or across different peer pairs.

## Deduplication and Safety

The system includes several safeguards to prevent wasted work:

* **No concurrent dreams**: If a dream is already being processed for a given peer representation, a new one will not be enqueued.
* **No duplicate pending dreams**: If a dream is already queued and waiting, a second enqueue request is skipped.
* **Cancellation on new activity**: When new messages arrive for a peer, any pending (not yet started) dream for that peer is cancelled. This ensures the dream always runs on the most up-to-date set of conclusions.

## Configuration

Dreams can be enabled or disabled at the workspace or session level:

<CodeGroup>
  ```python Python theme={null}
  # Disable dreams for a workspace
  honcho.set_configuration({
      "dream": {"enabled": False}
  })

  # Disable dreams for a specific session
  session = honcho.session("my-session", config={
      "dream": {"enabled": False}
  })
  ```

  ```typescript TypeScript theme={null}
  // Disable dreams for a workspace
  await honcho.setConfiguration({
      dream: { enabled: false }
  });

  // Disable dreams for a specific session
  const session = await honcho.session("my-session", {
      config: {
          dream: { enabled: false }
      }
  });
  ```
</CodeGroup>

Dreaming is automatically disabled if reasoning itself is disabled, since there would be no conclusions to consolidate.

<CardGroup>
  <Card title="Reasoning" icon="gears" href="/v3/documentation/core-concepts/reasoning">
    Learn how Honcho reasons over messages to produce conclusions
  </Card>

  <Card title="Configuration" icon="wrench" href="/v3/documentation/features/advanced/reasoning-configuration">
    Full configuration reference for reasoning, summaries, and dreams
  </Card>

  <Card title="Queue Status" icon="list-check" href="/v3/documentation/features/advanced/queue-status">
    Monitor dream tasks alongside other background processing
  </Card>

  <Card title="Schedule Dream API" icon="calendar" href="/v3/api-reference/endpoint/workspaces/schedule-dream">
    API reference for manually triggering dreams
  </Card>
</CardGroup>


# File Uploads
Source: https://honcho.dev/docs/v3/documentation/features/advanced/file-uploads

Upload PDFs, text files, and JSON documents to create messages in Honcho

Honcho's file upload feature allows you to convert documents into messages automatically. Upload PDFs, text files, or JSON documents, and Honcho will extract the text content, split it into appropriately sized chunks, and create messages that become part of your peer's representation or session context.

This feature is perfect for ingesting documents, reports, research papers, or any text-based content that you want your AI agents to understand and reference.

## How It Works

When you upload a file, Honcho:

1. **Extracts text** from the file using specialized processors based on file type
2. **Creates messages** with the extracted content split into chunks that fit within message limits (messages are limited to 50,000 characters)
3. **Queues processing** for background analysis and insight derivation like any other message

The file content becomes part of the peer's representation, making it available for natural language queries and context retrieval.

## Supported File Types

Honcho currently supports the following file types with more to come:

* **PDF files** (`application/pdf`) - Text extraction with page numbers
* **Text files** (`text/*`) - Plain text, markdown, code files, etc.
* **JSON files** (`application/json`) - Structured data converted to readable format

<Note>
  Files are processed in memory and not stored on disk. Only the extracted text content is preserved in Honcho's message system.
</Note>

## Basic Usage

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  # Initialize client
  honcho = Honcho()

  # Create session and peer
  session = honcho.session("research-session")
  user = honcho.peer("researcher")

  # Upload a PDF to a session
  with open("research_paper.pdf", "rb") as file:
      messages = session.upload_file(
          file=file,
          peer_id=user.id,
      )

  print(f"Created {len(messages)} messages from the PDF")
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from "@honcho-ai/sdk";
  import fs from "fs";

  (async () => {
      // Initialize client
      const honcho = new Honcho({});

      // Create session and peer
      const session = await honcho.session("research-session");
      const user = await honcho.peer("researcher");

      // Upload a PDF to a session
      const fileStream = fs.createReadStream("research_paper.pdf");
      const messages = await session.uploadFile(fileStream, user.id);

      console.log(`Created ${messages.length} messages from the PDF`);
  })();
  ```
</CodeGroup>

## Upload Parameters

The upload methods accept the following parameters:

| Parameter | Type   | Required | Description                          |
| --------- | ------ | -------- | ------------------------------------ |
| `file`    | File   | Yes      | File to upload                       |
| `peer_id` | String | Yes      | ID of the peer creating the messages |

## File Processing Details

### Text Extraction

**PDF Files**: Text is extracted page by page with page numbers preserved:

```
[Page 1]
Introduction
This document provides...

[Page 2]
Methodology
Our approach involves...
```

**Text Files**: Content is decoded using UTF-8, UTF-16, or Latin-1 encoding as needed.

**JSON Files**: Structured data is converted to string format.

### Chunking Strategy

Large files are automatically split into chunks of \~49,500 characters. The system seeks to break at natural boundaries if present:

1. Paragraph breaks (`\n\n`)
2. Line breaks (`\n`)
3. Sentence endings (`. `)
4. Word boundaries (` `)

Each chunk becomes a separate message, maintaining the original document structure.

## Querying Uploaded Content

Once files are uploaded, you can query the content using Honcho's natural language interface:

<CodeGroup>
  ```python Python theme={null}
  # Query what was learned from the uploaded documents
  response = user.chat("What are the key findings from the research papers I uploaded?")
  print(response)

  # Ask about specific documents
  response = user.chat("What does the quarterly report say about revenue growth?")
  print(response)

  # Get context from the uploaded documents for LLM integration
  context = session.context(tokens=3000)
  messages = context.to_openai(assistant=assistant)
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Query what was learned from the uploaded documents
      const response = await user.chat("What are the key findings from the research papers I uploaded?");
      console.log(response);

      // Ask about specific documents
      const response2 = await user.chat("What does the quarterly report say about revenue growth?");
      console.log(response2);

      // Get context from the uploaded documents for LLM integration
      const context = await session.context({ tokens: 3000 });
      const messages = context.toOpenAI(assistant);
  })();
  ```
</CodeGroup>

## Error Handling

### Unsupported File Types

Files with unsupported content types will raise an exception:

```python theme={null}
try:
    messages = session.upload_file(
        file=open("image.jpg", "rb"),
        peer_id=user.id
    )
except Exception as e:
    print(f"Upload failed: {e}")
    # Error: "Could not process file image.jpg: Unsupported file type: image/jpeg"
```

### Missing Required Fields

Session uploads require a `peer_id` parameter:

```python theme={null}
# This will fail for session uploads
try:
    messages = session.upload_file(file=file)  # Missing peer_id
except ValueError as e:
    print(f"Validation error: {e}")
```

## Complete Example: Document Analysis Assistant

Here's a complete example of building a document analysis assistant:

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  # Initialize
  honcho = Honcho()
  session = honcho.session("document-analysis")
  user = honcho.peer("analyst")
  assistant = honcho.peer("analysis-bot")

  def upload_document(file_path, description):
      """Upload a document and add it to the session"""
      with open(file_path, "rb") as file:
          messages = session.upload_file(
              file=file,
              peer_id=user.id,
          )
      return messages

  def analyze_documents():
      """Get AI analysis of uploaded documents"""
      context = session.context(tokens=4000)
      messages = context.to_openai(assistant=assistant)
      # Add analysis request
      messages.append({
          "role": "user",
          "content": "Please analyze all the documents I've uploaded and provide a comprehensive summary of the key findings, trends, and recommendations."
      })

      # Call OpenAI (or your preferred LLM)
      # response = openai.chat.completions.create(model="gpt-4", messages=messages)
      # return response.choices[0].message.content

      return "Analysis would be generated here"

  # Upload multiple documents
  documents = [
      ("quarterly_report.pdf", "Q3 2024 Quarterly Financial Report"),
      ("market_research.pdf", "Market Analysis and Competitive Landscape"),
      ("product_roadmap.pdf", "Product Development Roadmap 2024-2025")
  ]

  for file_path, description in documents:
      messages = upload_document(file_path, description)
      print(f"Uploaded {file_path}: {len(messages)} messages created")

  # Get AI analysis
  analysis = analyze_documents()
  print("Document Analysis:", analysis)
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from "@honcho-ai/sdk";
  import fs from "fs";

  (async () => {
      // Initialize
      const honcho = new Honcho({});
      const session = await honcho.session("document-analysis");
      const user = await honcho.peer("analyst");
      const assistant = await honcho.peer("analysis-bot");

      async function uploadDocument(filePath: string, description: string) {
        const fileStream = fs.createReadStream(filePath);
        const messages = await session.uploadFile(fileStream, user.id);
        return messages;
      }

      async function analyzeDocuments() {
        const context = await session.context({ tokens: 4000 });
        const messages = context.toOpenAI(assistant);
        // Add analysis request
        messages.push({
          role: "user",
          content: "Please analyze all the documents I've uploaded and provide a comprehensive summary of the key findings, trends, and recommendations."
        });

        // Call OpenAI (or your preferred LLM)
        // const response = await openai.chat.completions.create({ model: "gpt-4", messages });
        // return response.choices[0].message.content;

        return "Analysis would be generated here";
      }

      // Upload multiple documents
      const documents = [
        ["quarterly_report.pdf", "Q3 2024 Quarterly Financial Report"],
        ["market_research.pdf", "Market Analysis and Competitive Landscape"],
        ["product_roadmap.pdf", "Product Development Roadmap 2024-2025"]
      ];

      for (const [filePath, description] of documents) {
        const messages = await uploadDocument(filePath, description);
        console.log(`Uploaded ${filePath}: ${messages.length} messages created`);
      }

      // Get AI analysis
      const analysis = await analyzeDocuments();
      console.log("Document Analysis:", analysis);
  })();
  ```
</CodeGroup>

## Error Handling

* **Always wrap uploads in try-catch blocks** for robust error handling
* **Validate file types** before upload to avoid processing errors
* **Handle large files gracefully** with progress indicators
* **Implement retry logic** for network failures


# Advanced Features
Source: https://honcho.dev/docs/v3/documentation/features/advanced/overview

Advanced configuration and monitoring options for Honcho

Advanced features give you fine-grained control over Honcho's behavior and implementation.

## Reasoning & Memory

* [Configuration](/docs/v3/documentation/features/advanced/reasoning-configuration) - Configure reasoning models and behavior
* [Summarizer](/docs/v3/documentation/features/advanced/summarizer) - Automatic session summarization
* [Peer Card](/docs/v3/documentation/features/advanced/peer-card) - Quick-reference profile of stable biographical facts about a peer
* [Representation Scopes](/docs/v3/documentation/features/advanced/representation-scopes) - Directional representations for multi-peer scenarios
* [Dreaming](/docs/v3/documentation/features/advanced/dreaming) - Autonomous memory consolidation and self-improvement
* [Queue Status](/docs/v3/documentation/features/advanced/queue-status) - Monitor background processing and reasoning tasks

## Querying & Data

* [Search](/docs/v3/documentation/features/advanced/search) - Search across peers, sessions, and messages
* [Filters](/docs/v3/documentation/features/advanced/using-filters) - Filter queries with advanced parameters
* [Streaming Responses](/docs/v3/documentation/features/advanced/streaming-response) - Stream dialectic responses in real-time
* [File Uploads](/docs/v3/documentation/features/advanced/file-uploads) - Ingest files into peer memory


# Peer Card
Source: https://honcho.dev/docs/v3/documentation/features/advanced/peer-card

A quick-reference profile of stable biographical facts about a peer

A **peer card** is a list of stable, biographical facts about a peer--name, occupation, preferences, standing instructions--that acts as a quick-reference profile. While the full [representation](/docs/v3/documentation/core-concepts/representation) contains all of Honcho's reasoning (conclusions, summaries, semantic search results), the peer card captures the grounding facts that should never be forgotten.

Think of it as the front of a contact card: the information an agent needs at a glance to know who it's talking to.

## What Goes in a Peer Card

Peer cards are designed for **durable, biographical information**--things that remain true across sessions and contexts. Each fact is stored as a single string in a list.

| Category      | Examples                                                 |
| ------------- | -------------------------------------------------------- |
| Identity      | `"Name: Alice"`, `"Age: 28"`, `"Location: Portland, OR"` |
| Occupation    | `"Works as a senior engineer at Acme Corp"`              |
| Relationships | `"Has a dog named Max"`, `"Married to Bob"`              |
| Instructions  | `"INSTRUCTION: Always address as Dr. Chen"`              |
| Preferences   | `"PREFERENCE: Prefers concise responses"`                |
| Traits        | `"TRAIT: Detail-oriented, prefers data over anecdotes"`  |

Peer cards are **not** for transient information like current mood, recent conversation topics, or reasoning traces. Those belong in conclusions and summaries.

## How Peer Cards Are Created

Peer cards are populated through two paths:

**1. Automatic (via Dreaming)**

When [dreaming](/docs/v3/documentation/features/advanced/dreaming) runs, the deduction and induction specialists extract stable biographical facts from existing conclusions and write them to the peer card. This happens without any manual intervention--Honcho identifies facts like names, occupations, and preferences from conversation history and records them automatically.

**2. Manual (via SDK or API)**

You can set a peer card directly. This is useful for bootstrapping a peer with known information before any conversation has occurred, or for correcting facts that Honcho hasn't yet discovered.

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  honcho = Honcho()
  peer = honcho.peer("user-123")

  # Set the peer card
  peer.set_card([
      "Name: Alice. Also known as 'Ali'.",
      "College student at MIT, studying computer science.",
      "PREFERENCE: Prefers casual tone.",
      "INSTRUCTION: Never mention her ex-boyfriend.",
  ])

  # Retrieve the peer card
  card = peer.get_card()
  print(card)
  # ["Name: Alice. Also known as 'Ali'.", "College student at MIT...", ...]
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from "@honcho-ai/sdk";

  const honcho = new Honcho({});
  const peer = await honcho.peer("user-123");

  // Set the peer card
  await peer.setCard([
      "Name: Alice. Also known as 'Ali'.",
      "College student at MIT, studying computer science.",
      "PREFERENCE: Prefers casual tone.",
      "INSTRUCTION: Never mention her ex-boyfriend.",
  ]);

  // Retrieve the peer card
  const card = await peer.getCard();
  console.log(card);
  // ["Name: Alice. Also known as 'Ali'.", "College student at MIT...", ...]
  ```
</CodeGroup>

## Directional Peer Cards

Peer cards follow the same observer-observed model as [representations](/docs/v3/documentation/features/advanced/representation-scopes). When `observe_others` is enabled, a peer can have a **different** card for each peer it observes.

For example, if Alice and Bob are in a session together and Alice has `observe_others: true`, Alice will build her own peer card for Bob--separate from Honcho's peer card for Bob. You can read and write these directional cards using the `target` parameter.

<CodeGroup>
  ```python Python theme={null}
  alice = honcho.peer("alice")

  # Get Alice's own peer card (Honcho's view of Alice)
  alice_card = alice.get_card()

  # Get Alice's card for Bob (Alice's view of Bob)
  alice_bob_card = alice.get_card(target="bob")

  # Set Alice's card for Bob
  alice.set_card(
      ["Bob mentioned he's allergic to peanuts."],
      target="bob"
  )
  ```

  ```typescript TypeScript theme={null}
  const alice = await honcho.peer("alice");

  // Get Alice's own peer card (Honcho's view of Alice)
  const aliceCard = await alice.getCard();

  // Get Alice's card for Bob (Alice's view of Bob)
  const aliceBobCard = await alice.getCard({ target: "bob" });

  // Set Alice's card for Bob
  await alice.setCard(
      ["Bob mentioned he's allergic to peanuts."],
      { target: "bob" }
  );
  ```
</CodeGroup>

## Where Peer Cards Are Used

### In the Dialectic (Chat Endpoint)

When you call [`peer.chat()`](/docs/v3/documentation/features/chat), Honcho automatically injects the relevant peer cards into the system prompt. The dialectic agent sees both the observer's own card and the observed peer's card, giving it immediate grounding without needing to search memory.

### In Context Retrieval

The [`session.context()`](/docs/v3/documentation/features/get-context) method includes the peer card when you specify a `peer_target`:

<CodeGroup>
  ```python Python theme={null}
  context = session.context(
      tokens=2000,
      peer_target="user-123"
  )

  # Access the peer card alongside the representation
  print(context.peer_card)            # List of peer card facts
  print(context.peer_representation)  # Full representation text
  ```

  ```typescript TypeScript theme={null}
  const context = await session.context({
      tokens: 2000,
      peerTarget: "user-123"
  });

  console.log(context.peerCard);            // Array of peer card facts
  console.log(context.peerRepresentation);  // Full representation text
  ```
</CodeGroup>

### During Dreaming

The [dreaming](/docs/v3/documentation/features/advanced/dreaming) process reads the current peer card before consolidation, then updates it with any new stable facts discovered during the deduction and induction phases.

## Limits

| Constraint             | Value                               |
| ---------------------- | ----------------------------------- |
| Maximum facts per card | **40**                              |
| Data type              | `list[str]` (each fact is a string) |

When the dreaming process or a manual update pushes the card beyond 40 facts, it is automatically truncated to the first 40 entries. Keep facts concise and deduplicated to stay within the limit.

<Warning>
  If you manually set a peer card, it **replaces** the entire card--it does not merge with existing facts. Make sure to include all facts you want to keep when calling `set_card()`.
</Warning>

## Configuration

Peer card behavior is controlled through the [configuration hierarchy](/docs/v3/documentation/features/advanced/reasoning-configuration). You can independently toggle whether agents **use** existing peer cards and whether they **create/update** them.

<CodeGroup>
  ```python Python theme={null}
  # Disable peer card updates but still use existing cards during reasoning
  session = honcho.session("my-session", config={
      "peer_card": {"create": False, "use": True}
  })

  # Disable peer cards entirely
  session = honcho.session("no-cards", config={
      "peer_card": {"create": False, "use": False}
  })
  ```

  ```typescript TypeScript theme={null}
  // Disable peer card updates but still use existing cards during reasoning
  const session = await honcho.session("my-session", {
      config: {
          peer_card: { create: false, use: true }
      }
  });

  // Disable peer cards entirely
  const noCards = await honcho.session("no-cards", {
      config: {
          peer_card: { create: false, use: false }
      }
  });
  ```
</CodeGroup>

| Field    | Type   | Default | Description                                                 |
| -------- | ------ | ------- | ----------------------------------------------------------- |
| `use`    | `bool` | `true`  | Whether agents read the peer card during reasoning and chat |
| `create` | `bool` | `true`  | Whether agents can create or update peer cards              |

Configuration can be set at the workspace, session, or message level. See [Reasoning Configuration](/docs/v3/documentation/features/advanced/reasoning-configuration) for the full hierarchy.

## Best Practices

1. **Bootstrap with known facts.** If you already know the user's name or preferences at signup, set the peer card immediately. This gives the agent grounding from the very first interaction instead of waiting for dreaming to discover it.

2. **Use structured prefixes.** Prefixing facts with `INSTRUCTION:`, `PREFERENCE:`, or `TRAIT:` makes it easier for the agent to distinguish categories and act on them appropriately.

3. **Keep facts atomic.** Each string should contain one fact. Avoid combining multiple pieces of information into a single entry--`"Name: Alice"` and `"Location: Portland"` are better than `"Alice lives in Portland and works at Acme"`.

4. **Let dreaming handle updates.** For most applications, you don't need to manually manage the peer card after bootstrapping. The dreaming process will discover and record new facts as conversations progress.

5. **Use `set_card` for corrections.** If the automatic system has recorded something incorrect, manually set the card with the corrected facts. Remember this replaces the entire card.

<CardGroup>
  <Card title="Representations" icon="user-magnifying-glass" href="/v3/documentation/core-concepts/representation">
    Understand the full representation system that peer cards complement
  </Card>

  <Card title="Dreaming" icon="cloud-moon" href="/v3/documentation/features/advanced/dreaming">
    Learn how dreaming automatically populates peer cards
  </Card>

  <Card title="Configuration" icon="wrench" href="/v3/documentation/features/advanced/reasoning-configuration">
    Configure peer card behavior at workspace, session, or message level
  </Card>

  <Card title="Get Peer Card API" icon="code" href="/v3/api-reference/endpoint/peers/get-peer-card">
    API reference for retrieving peer cards
  </Card>
</CardGroup>


# Queue Status
Source: https://honcho.dev/docs/v3/documentation/features/advanced/queue-status

Learn how to check the status of Honcho's reasoning

Whenever messages are stored in Honcho, background processes kick off to [reason](/docs/v3/documentation/core-concepts/reasoning) about the conversation and generate insights.

Reasoning is an asynchronous process and will not immediately
generate insights for the latest message you've sent. This is
by design: we want to reason efficiently over batches of messages
rather than assessing each message in a vacuum. Honcho provides
several utilities to check the status of the queue.

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho
  honcho = Honcho()

  status = honcho.queue_status()
  ```

  ```typescript typescript theme={null}
  import { Honcho } from '@honcho-ai/sdk';

  const honcho = new Honcho({});

  const status = await honcho.queueStatus();
  ```
</CodeGroup>

Output types

<CodeGroup>
  ```python Python theme={null}
  class QueueStatus(BaseModel):
      completed_work_units: int
      """Completed work units"""

      in_progress_work_units: int
      """Work units currently being processed"""

      pending_work_units: int
      """Work units waiting to be processed"""

      total_work_units: int
      """Total work units"""

      sessions: Optional[Dict[str, Sessions]] = None
      """Per-session status when not filtered by session"""
  ```

  ```typescript TypeScript theme={null}
  Promise<{
      totalWorkUnits: number
      completedWorkUnits: number
      inProgressWorkUnits: number
      pendingWorkUnits: number
      sessions?: Record<string, QueueStatus.Sessions>
    }>

  ```
</CodeGroup>

Whenever a message is sent it will generate several tasks. These could
be tasks such as generating insights, cleaning up a representation, summarizing
a conversation etc. These tasks are defined based on who is sending the
message, what session the message is in, and potentially who is observing the
message. We call the combination of these parameters a `work_unit`

This has a few different implications.

* tasks within the same work\_unit are processed sequentially, but multiple
  work\_units will be processed in parallel
* If local representations are turned in a Session then a message will
  generate an additional work unit for every peer that has `observe_others=True`

### Tracked task types

The queue status endpoint reports on the following task types:

| Task Type          | Description                                                                                |
| ------------------ | ------------------------------------------------------------------------------------------ |
| **representation** | Memory formation — the deriver processes messages and extracts observations about peers    |
| **summary**        | Session summarization — creates short and long summaries at configurable message intervals |
| **dream**          | Memory consolidation — explores and consolidates observations to improve memory quality    |

Internal infrastructure tasks (such as webhook delivery, resource deletion, and
vector reconciliation) are **not** included in queue status counts.

<Note>
  **Completed counts are not lifetime totals.** Honcho periodically cleans up
  processed queue items to keep the queue table lean. As a result,
  `completed_work_units` reflects items completed since the last cleanup cycle,
  not the total number of items ever processed.
</Note>

The `queue_status` method can take additional
parameters to scope the status to a specific work unit:

<CodeGroup>
  ```python Python theme={null}
  def queue_status(
          self,
          observer_id: str | None = None,
          sender_id: str | None = None,
          session_id: str | None = None,
      ) -> QueueStatus:
  ```

  ```typescript TypeScript theme={null}

  export const QueueStatusOptionsSchema = z.object({
    observerId: z.string().optional(),
    senderId: z.string().optional(),
    sessionId: z.string().optional(),
    timeoutMs: z
      .number()
      .positive('Timeout must be a positive number')
      .optional(),
  })

  ```
</CodeGroup>

Additionally, there are queue status methods available on the session objects in each of the SDKs.

<Warning>
  **Do not wait for the queue to be empty.** The queue is a continuous processing system—new messages may arrive at any time, and "completion" is not a meaningful state. Design your application to work without assuming the queue will ever be fully drained. Use `queueStatus()` for observability and debugging, not for synchronization.
</Warning>

Below are the function signatures for the session level queue status method:

<CodeGroup>
  ```python python theme={null}
  @validate_call
      def queue_status(
          self,
          observer_id: str | None = None,
          sender_id: str | None = None,
      ) -> QueueStatus:
  ```

  ```typescript TypeScript theme={null}
  async queueStatus(
      options?: Omit<QueueStatusOptions, 'sessionId'>
    ): Promise<{
      totalWorkUnits: number
      completedWorkUnits: number
      inProgressWorkUnits: number
      pendingWorkUnits: number
      sessions?: Record<string, QueueStatus.Sessions>
    }>
  ```
</CodeGroup>


# Reasoning Configuration
Source: https://honcho.dev/docs/v3/documentation/features/advanced/reasoning-configuration

Customize how Honcho reasons over peers, sessions, and messages

Honcho's reasoning can be configured at multiple levels to control how it processes messages, generates conclusions, creates summaries, and builds peer representations.

Configuration follows a hierarchy: **message > session > workspace > global defaults**. Settings at lower levels override those at higher levels, giving you fine-grained control over behavior.

## Configuration Hierarchy

Honcho uses a hierarchical configuration system where more specific settings override more general ones:

1. **Global Defaults**: Built-in system defaults
2. **Workspace Configuration**: Settings that apply to all sessions in a workspace
3. **Session Configuration**: Settings that apply to all messages in a session
4. **Message Configuration**: Settings that apply to a specific message

Separately, you can configure the reasoning status of a peer. This overrides defaults and workspace configuration, but not session or message configuration.

<Info>
  All configuration fields are optional. If not specified, the value is inherited from the next level up in the hierarchy.
</Info>

## Configuration Options

### Reasoning Configuration

Controls whether the system should reason over messages.

| Field     | Type   | Description                                                                                          |
| --------- | ------ | ---------------------------------------------------------------------------------------------------- |
| `enabled` | `bool` | Whether to enable reasoning functionality. When disabled, no facts or representations are generated. |

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  honcho = Honcho()

  # Disable reasoning at session level
  session = honcho.session("private-session", config={
      "reasoning": {"enabled": False}
  })
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from "@honcho-ai/sdk";

  const honcho = new Honcho({});

  // Disable reasoning at session level
  const session = await honcho.session("private-session", {
      config: {
          reasoning: { enabled: false }
      }
  });
  ```
</CodeGroup>

### Peer Card Configuration

Controls how peer cards (containing key biographical information) are generated and used.

| Field    | Type   | Description                                                         |
| -------- | ------ | ------------------------------------------------------------------- |
| `use`    | `bool` | Whether to use peer cards during the reasoning process.             |
| `create` | `bool` | Whether to generate and update peer cards based on message content. |

<CodeGroup>
  ```python Python theme={null}
  # Disable peer card generation but still use existing cards
  session = honcho.session("my-session", config={
      "peer_card": {"create": False, "use": True}
  })
  ```

  ```typescript TypeScript theme={null}
  // Disable peer card generation but still use existing cards
  const session = await honcho.session("my-session", {
      config: {
          peer_card: { create: false, use: true }
      }
  });
  ```
</CodeGroup>

### Summary Configuration

Controls automatic conversation summarization. Available at workspace and session levels only.

| Field                        | Type   | Description                                                                                            |
| ---------------------------- | ------ | ------------------------------------------------------------------------------------------------------ |
| `enabled`                    | `bool` | Whether to enable summary functionality.                                                               |
| `messages_per_short_summary` | `int`  | Number of messages between short summaries. Must be ≥ 10.                                              |
| `messages_per_long_summary`  | `int`  | Number of messages between long summaries. Must be ≥ 20 and greater than `messages_per_short_summary`. |

<CodeGroup>
  ```python Python theme={null}
  # Customize summary frequency
  session = honcho.session("verbose-session", config={
      "summary": {
          "enabled": True,
          "messages_per_short_summary": 15,
          "messages_per_long_summary": 45
      }
  })
  ```

  ```typescript TypeScript theme={null}
  // Customize summary frequency
  const session = await honcho.session("verbose-session", {
      config: {
          summary: {
              enabled: true,
              messages_per_short_summary: 15,
              messages_per_long_summary: 45
          }
      }
  });
  ```
</CodeGroup>

### Dream Configuration

Controls the "dreaming" process that consolidates and refines representations. Available at workspace and session levels only.

| Field     | Type   | Description                                                                             |
| --------- | ------ | --------------------------------------------------------------------------------------- |
| `enabled` | `bool` | Whether to enable dream functionality. Automatically disabled if reasoning is disabled. |

<CodeGroup>
  ```python Python theme={null}
  # Disable dreams for a workspace
  honcho.set_configuration({
      "dream": {
          "enabled": False
      }
  })
  ```

  ```typescript TypeScript theme={null}
  // Disable dreams for a workspace
  await honcho.setConfiguration({
      dream: {
          enabled: false
      }
  });
  ```
</CodeGroup>

***

## Peer Configuration

By default, all peers are "observed" by Honcho. This means that Honcho will reason over messages sent by the peer and generate a representation of them. In most cases, this is why you use Honcho! However, sometimes an application requires a peer that should not be observed: for example, an assistant or game NPC that your program will never need to access advanced reasoning for.

You may therefore disable observation of a peer by setting the `observe_me` flag in their configuration to `false`.

If the peer has a session-level configuration, it will override this configuration. If the flag is not set, or is set to `true`, the peer will be observed.

<Info>
  For session-level observation controls and local representations (where peers build separate models of each other), see [Representation Scopes](/docs/v3/documentation/features/advanced/representation-scopes).
</Info>

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  # Initialize client
  honcho = Honcho()

  # Create peer with configuration
  peer = honcho.peer("my-peer", configuration={"observe_me": False})

  # Change peer's configuration
  peer.set_configuration({"observe_me": True})

  # Note: creating the same peer again will also replace the configuration
  peer = honcho.peer("my-peer", configuration={"observe_me": False})
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from "@honcho-ai/sdk";

  (async () => {
      // Initialize client
      const honcho = new Honcho({});

      // Create peer with configuration
      const peer = await honcho.peer("my-peer", { configuration: { observeMe: false } });

      // Change peer's configuration
      await peer.setConfiguration({ observeMe: true });

      // Note: creating the same peer again will also replace the configuration
      await honcho.peer("my-peer", { configuration: { observeMe: false } });
  })();
  ```
</CodeGroup>

## Session Configuration

Sessions support the full configuration schema. You can disable reasoning entirely for a session, customize summary behavior, or adjust peer card settings.

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  # Initialize client
  honcho = Honcho()

  # Create session with reasoning disabled
  session = honcho.session("my-session", configuration={
      "reasoning": {"enabled": False}
  })

  # Create session with custom summary settings
  session = honcho.session("detailed-session", configuration={
      "summary": {
          "messages_per_short_summary": 10,
          "messages_per_long_summary": 30
      }
  })
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from "@honcho-ai/sdk";

  (async () => {
      // Initialize client
      const honcho = new Honcho({});

      // Create session with reasoning disabled
      const session = await honcho.session("my-session", {
          configuration: { reasoning: { enabled: false } }
      });

      // Create session with custom summary settings
      const detailedSession = await honcho.session("detailed-session", {
          configuration: {
              summary: {
                  messages_per_short_summary: 10,
                  messages_per_long_summary: 30
              }
          }
      });
  })();
  ```
</CodeGroup>

## Message Configuration

Individual messages can override session and workspace configuration for fine-grained control. This is useful for excluding specific messages from processing or adjusting behavior on a per-message basis.

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  honcho = Honcho()
  session = honcho.session("my-session")
  user = honcho.peer("user")

  # Create a message that skips the reasoning process
  session.add_messages([
      user.message("This message won't be analyzed", configuration={
          "reasoning": {"enabled": False}
      })
  ])

  # Create a message with custom peer card settings
  session.add_messages([
      user.message("Use existing card but don't update it", configuration={
          "peer_card": {"use": True, "create": False}
      })
  ])
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from "@honcho-ai/sdk";

  (async () => {
      const honcho = new Honcho({});
      const session = await honcho.session("my-session");
      const user = await honcho.peer("user");

      // Create a message that skips the reasoning process
      await session.addMessages([
          user.message("This message won't be analyzed", {
              configuration: { reasoning: { enabled: false } }
          })
      ]);
  })();
  ```
</CodeGroup>

## Full Configuration Schema Reference

### Workspace & Session Configuration

```json theme={null}
{
  "reasoning": {
    "enabled": true
  },
  "peer_card": {
    "use": true,
    "create": true
  },
  "summary": {
    "enabled": true,
    "messages_per_short_summary": 20,
    "messages_per_long_summary": 60
  },
  "dream": {
    "enabled": true
  }
}
```

### Message Configuration

```json theme={null}
{
  "reasoning": {
    "enabled": true
  },
  "peer_card": {
    "use": true,
    "create": true
  }
}
```

<Note>
  Message configuration only supports reasoning and `peer_card` settings. Summary and dream configurations are session/workspace-level only.
</Note>


# Representation Scopes
Source: https://honcho.dev/docs/v3/documentation/features/advanced/representation-scopes

Advanced configuration and querying for representations

Assuming reasoning is enabled, you can control the perspectives representations are built from. This page covers:

1. **Default Behavior** — Honcho reasons over every message written to a peer
2. **Observer-Observed Model** — How peers build representations of other peers
3. **Querying with Target** — Accessing perspective-specific representations
4. **Use Cases** — When to use directional representations

## Default: Reasoning On

When `observe_me=true` (the default), Honcho forms one representation per peer, reasoning over every message written to that peer across all sessions.

You can retrieve a subset of conclusions from a peer's representation using `representation()`:

```python theme={null}
# Retrieve conclusions from Honcho's representation of Alice (across all sessions)
alice_rep = session.representation("alice")

# Or via chat
response = alice.chat("What are Alice's main interests?", session_id=session.id)
```

This is sufficient for most applications—Honcho reasons over every message written to the peer, storing conclusions that any part of your system can retrieve.

## Observer-Observed Representations

When you enable `observe_others=true` at the session level, peers begin forming **directional representations** of other peers they interact with. These representations are scoped to what that observer has actually witnessed.

### How It Works

Each peer has **one representation**, but that representation can contain reasoning about:

* **Itself** (when Honcho observes the peer with `observe_me=true`)
* **Other peers** (when the peer observes others with `observe_others=true`)

These are stored as separate (observer, observed) pairs in Honcho's internal collections:

| Observer | Observed | What This Represents                                                    |
| -------- | -------- | ----------------------------------------------------------------------- |
| alice    | alice    | Honcho's representation of Alice (across all sessions)                  |
| alice    | bob      | Alice's representation of Bob (from sessions Alice participated in)     |
| alice    | charlie  | Alice's representation of Charlie (from sessions Alice participated in) |

### Information Segmentation

This enables sophisticated scenarios where different agents have different knowledge based on what they've actually witnessed.

**Example**: Bob and Charlie tell different things to Alice in separate sessions.

```
Session 1 (Alice + Bob):
Bob → "I had pancakes for breakfast."

Session 2 (Alice + Charlie):
Charlie → "I had pancakes for breakfast. Bob is lying about his breakfast."
```

With `observe_others=true` enabled on Alice:

* **Alice's representation of Bob** only includes Session 1 (she heard Bob say he had pancakes)
* **Alice's representation of Charlie** only includes Session 2 (she heard Charlie's claim about Bob lying)
* **Honcho's representation of Alice** reasons over both sessions

<img alt="" />

## Querying with Target

The `target` parameter controls which representation you retrieve:

| Query                                       | Returns                                                                                  |
| ------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `representation("alice")`                   | Conclusions from Honcho's representation of Alice (across all sessions)                  |
| `representation("alice", target="bob")`     | Conclusions from Alice's representation of Bob (from sessions Alice participated in)     |
| `representation("alice", target="charlie")` | Conclusions from Alice's representation of Charlie (from sessions Alice participated in) |

### Code Examples

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho
  from honcho.api_types import SessionPeerConfig

  honcho = Honcho()
  session = honcho.session("game-session")

  alice = honcho.peer("alice")
  bob = honcho.peer("bob")
  charlie = honcho.peer("charlie")

  # Add peers to session
  session.add_peers([alice, bob, charlie])

  # Enable Alice to form representations of others
  session.set_peer_configuration(alice, SessionPeerConfig(observe_others=True))

  # Add messages
  session.add_messages([
      bob.message("I had pancakes for breakfast."),
      charlie.message("I prefer waffles.")
  ])

  # Different sessions with different participants
  session2 = honcho.session("game-session-2")
  session2.add_peers([alice, charlie])
  session2.set_peer_configuration(alice, SessionPeerConfig(observe_others=True))

  session2.add_messages([
      charlie.message("I didn't have breakfast. I lied to Bob.")
  ])

  # Retrieve conclusions from different perspectives
  honcho_view = session.representation("alice")  # Across all sessions
  bob_view = session.representation("alice", target="bob")  # Alice's view of Bob
  charlie_view = session2.representation("alice", target="charlie")  # Alice's view of Charlie
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from "@honcho-ai/sdk";

  const honcho = new Honcho({});
  const session = await honcho.session("game-session");

  const alice = await honcho.peer("alice");
  const bob = await honcho.peer("bob");
  const charlie = await honcho.peer("charlie");

  await session.addPeers([alice, bob, charlie]);

  await session.setPeerConfiguration(alice, { observeOthers: true });

  await session.addMessages([
      bob.message("I had pancakes for breakfast."),
      charlie.message("I prefer waffles.")
  ]);

  const session2 = await honcho.session("game-session-2");
  await session2.addPeers([alice, charlie]);
  await session2.setPeerConfiguration(alice, { observeOthers: true });

  await session2.addMessages([
      charlie.message("I didn't have breakfast. I lied to Bob.")
  ]);

  // Retrieve conclusions from different perspectives
  const honchoView = await session.representation("alice");  // Across all sessions
  const bobView = await session.representation("alice", { target: "bob" });  // Alice's view of Bob
  const charlieView = await session2.representation("alice", { target: "charlie" });  // Alice's view of Charlie
  ```
</CodeGroup>

### Chat Endpoint with Target

The `target` parameter also works with the chat endpoint:

<CodeGroup>
  ```python Python theme={null}
  # Query using conclusions from Honcho's representation (across all sessions)
  honcho_answer = alice.chat(
      "What did Bob say about breakfast?",
      session_id=session.id
  )

  # Query using conclusions from Alice's representation of Bob (from Alice's sessions only)
  alice_answer = alice.chat(
      "What did Bob say about breakfast?",
      session_id=session.id,
      target="bob"
  )
  ```

  ```typescript TypeScript theme={null}
  // Query using conclusions from Honcho's representation (across all sessions)
  const honchoAnswer = await alice.chat(
      "What did Bob say about breakfast?",
      { sessionId: session.id }
  );

  // Query using conclusions from Alice's representation of Bob (from Alice's sessions only)
  const aliceAnswer = await alice.chat(
      "What did Bob say about breakfast?",
      { sessionId: session.id, target: "bob" }
  );
  ```
</CodeGroup>

<Note>
  The `target` parameter only returns meaningful results if the observer peer has `observe_others=true` and has actually participated in sessions with the observed peer. Otherwise, the representation will be empty or non-existent.
</Note>

## When to Use Directional Representations

### Use Cases Where This Matters

1. **Multi-agent games**: NPCs should only know what they've witnessed, not omniscient game state
2. **Information asymmetry scenarios**: Different agents have access to different information
3. **Perspective-dependent agents**: Agent behavior depends on their unique understanding of other agents
4. **Privacy-segmented systems**: Users should only see representations based on their interactions

### Use Cases Where Default Is Sufficient

1. **Single-user applications**: Only one user, so perspective doesn't matter
2. **Centralized knowledge systems**: All agents should share the same understanding
3. **Simple chatbots**: No multi-agent interaction or information segmentation needed

<Info>
  Most applications don't need directional representations. Start with the default Honcho-observes-all behavior and only enable `observe_others` when you need information segmentation between agents.
</Info>

## Architecture: How It's Stored

Under the hood, Honcho stores representations as (observer, observed) pairs in internal collections:

* **Collection**: A unique (observer, observed, workspace) tuple containing documents
* **Documents**: Individual conclusions and artifacts (deductive, inductive, abductive conclusions, summaries, peer cards) with session scoping

When you retrieve with `target`, Honcho fetches documents from the specific (observer, observed) collection. When you retrieve without `target`, it fetches from the (peer, peer) collection—the peer's self-representation.

This architecture enables:

* **Efficient querying**: Each perspective is isolated and can be queried independently
* **Session filtering**: Within a collection, documents can be filtered by session
* **Scalability**: Adding more observers doesn't degrade query performance

## Semantic Search Parameters

Both `representation()` and `chat()` support semantic filtering to retrieve a subset of relevant conclusions. You can optionally filter by session to retrieve only conclusions from specific session context:

| Parameter               | Type    | Description                               |
| ----------------------- | ------- | ----------------------------------------- |
| `search_query`          | `str`   | Semantic query to filter conclusions      |
| `search_top_k`          | `int`   | Number of results to include (1–100)      |
| `search_max_distance`   | `float` | Maximum semantic distance (0.0–1.0)       |
| `include_most_frequent` | `bool`  | Include most frequent conclusions         |
| `max_conclusions`       | `int`   | Cap on total conclusions returned (1–100) |

<CodeGroup>
  ```python Python theme={null}
  # Retrieve conclusions about billing from Alice's representation of Bob
  alice_view_billing = session.representation(
      "alice",
      target="bob",
      search_query="billing issues",
      search_top_k=10,
      include_most_frequent=True
  )
  ```

  ```typescript TypeScript theme={null}
  const aliceViewBilling = await session.representation("alice", {
      target: "bob",
      searchQuery: "billing issues",
      searchTopK: 10,
      includeMostFrequent: true
  });
  ```
</CodeGroup>

## When Representations Update

Directional representations update automatically through the reasoning pipeline when:

1. A message is created in a session
2. The message sender has `observe_me=true` (or session-level equivalent)
3. Other peers in the session have `observe_others=true`

The pipeline respects scoping—Honcho's representations reason over messages across all sessions, while directional representations only reason over messages from sessions where the observer was an active participant.

### Peer Join Order Matters

Reasoning tasks are scheduled at the time a message is created, based on which peers are in the session **at that moment**. Honcho does not retroactively schedule reasoning for peers that join later.

This means:

* If Peer C joins a session **after** messages from Peer A and Peer B have already been sent, Peer C will **not** receive reasoning tasks for those earlier messages—even if Peer C has `observe_others=true`.
* Peer C will only begin observing new messages sent after they join the session.
* Similarly, if a peer leaves a session, they stop being included as an observer for any messages sent after their departure.

<Warning>
  There is no retroactive reasoning. If your application needs an observer peer to reason about prior conversation history, add the peer to the session **before** messages are sent. Alternatively, use `peer.chat()` to include conversation history in the agent's context whether or not those messages were previously reasoned over.
</Warning>

<Note>
  Conclusions are cached for fast retrieval. Use `representation()` to retrieve stored conclusions for dashboards and analytics. Use `peer.chat()` when you need query-specific reasoning with natural language.
</Note>


# Search
Source: https://honcho.dev/docs/v3/documentation/features/advanced/search

Learn how to search across workspaces, sessions, and peers to find relevant conversations and content

Honcho's search functionality allows you to find relevant messages and conversations across different scopes - from entire workspaces down to specific peers or sessions.

<Note>
  Search is hybrid: it combines full-text (keyword) matching with semantic (vector) similarity. Keyword matches are available the instant a message is created. Semantic matches depend on the message's embedding, which is generated in the background, so a freshly created message may take a few seconds to surface in semantic results. If you need to assert on semantic results immediately after writing (for example in tests), wait briefly or poll.
</Note>

## Search Scopes

### Workspace Search

Search across all content in your workspace - sessions, peers, and messages:

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  # Initialize client
  honcho = Honcho()

  # Search across entire workspace
  results = honcho.search("budget planning")

  # Iterate through all results
  for result in results:
      print(f"Found: {result}")
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from "@honcho-ai/sdk";

  (async () => {
      // Initialize client
      const honcho = new Honcho({});

      // Search across entire workspace
      const results = await honcho.search("budget planning");

      // Iterate through all results
      for (const result of results) {
        console.log(`Found: ${result}`);
      }
  })();
  ```
</CodeGroup>

### Session Search

Search within a specific session's conversation history:

<CodeGroup>
  ```python Python theme={null}
  # Create or get a session
  session = honcho.session("team-meeting-jan")

  # Search within this session only
  results = session.search("action items")

  # Process results
  for result in results:
      print(f"Session result: {result}")
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Create or get a session
      const session = await honcho.session("team-meeting-jan");

      // Search within this session only
      const results = await session.search("action items");

      // Process results
      for (const result of results) {
        console.log(`Session result: ${result}`);
      }
  })();
  ```
</CodeGroup>

### Peer Search

Search across all content associated with a specific peer:

<CodeGroup>
  ```python Python theme={null}
  # Create or get a peer
  alice = honcho.peer("alice")

  # Search across all of Alice's messages and interactions
  results = alice.search("programming")

  # View results
  for result in results:
      print(f"Alice's content: {result}")
  ```

  ```typescript TypeScript theme={null}
  import { Message } from "@honcho-ai/sdk";

  (async () => {
      // Create or get a peer
      const alice = await honcho.peer("alice");

      // Search across all of Alice's messages and interactions
      const results: Message[] = await alice.search("programming");

      // View results
      for (const result of results) {
        console.log(`Alice's content: ${result.content}`);
      }
  })();
  ```
</CodeGroup>

## Filters and Limits

### Get a specific number of results

You can specify the number of results you want to return by passing the `limit` parameter to the search method. The default is 10 results, with a maximum of 100.

<CodeGroup>
  ```python Python theme={null}
  results = honcho.search("budget planning", limit=20)
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      const results = await honcho.search("budget planning", { limit: 20 });
  })();
  ```
</CodeGroup>

### Get messages from a Peer in a specific Session

Combine Peer-level search with a `session_id` filter to get messages from a Peer in a specific Session.

<CodeGroup>
  ```python Python theme={null}
  my_peer = honcho.peer("my-peer")
  my_session = honcho.session("team-meeting-jan")
  results = my_peer.search("budget planning", filters={"session_id": my_session.id})
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      const myPeer = await honcho.peer("my-peer");
      const mySession = await honcho.session("team-meeting-jan");
      const results = await myPeer.search("budget planning", { filters: { session_id: mySession.id } });
  })();
  ```
</CodeGroup>

Search returns an object containing an `items` array of message objects:

```json theme={null}
{
  "items": [
    {
      "id": "<string>",
      "content": "<string>",
      "peer_id": "<string>",
      "session_id": "<string>",
      "metadata": {},
      "created_at": "2023-11-07T05:31:56Z",
      "workspace_id": "<string>",
      "token_count": 123
    }
  ]
}
```

### Filter results by time range

<CodeGroup>
  ```python Python theme={null}
  results = honcho.search("budget planning", filters={"created_at": {"gte": "2024-01-01", "lte": "2024-01-31"}})
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      const results = await honcho.search("budget planning", { filters: { created_at: { gte: "2024-01-01", lte: "2024-01-31" } } });
  })();
  ```
</CodeGroup>

### Filter results by metadata

<CodeGroup>
  ```python Python theme={null}
  results = honcho.search("budget planning", filters={"metadata": {"key": "value"}})
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      const results = await honcho.search("budget planning", { filters: { metadata: { key: "value" } } });
  })();
  ```
</CodeGroup>

### Best Practices

### Handle Empty Results Gracefully

<CodeGroup>
  ```python Python theme={null}
  # Always check for empty results
  results = honcho.search("very specific query")
  result_list = list(results)

  if result_list:
      print(f"Found {len(result_list)} results")
      for result in result_list:
          print(f"- {result}")
  else:
      print("No results found - try a broader search")
  ```

  ```typescript TypeScript theme={null}
  import { Message } from "@honcho-ai/sdk";

  (async () => {
      // Always check for empty results
      const results: Message[] = await honcho.search("very specific query");

      if (results.length > 0) {
        console.log(`Found ${results.length} results`);
        for (const result of results) {
          console.log(`- ${result.content}`);
        }
      } else {
        console.log("No results found - try a broader search");
      }
  })();
  ```
</CodeGroup>

## Conclusion

Honcho's search functionality provides powerful discovery capabilities across your conversational data. By understanding how to:

* Choose the appropriate search scope (workspace, session, or peer)
* Handle paginated results effectively
* Combine search with context building

You can build applications that provide intelligent insights and context-aware responses based on historical conversations and interactions.


# Streaming Responses
Source: https://honcho.dev/docs/v3/documentation/features/advanced/streaming-response

Using streaming responses with Honcho SDKs

When working with AI-generated content, streaming the response as it's generated can significantly improve the user experience. Honcho provides streaming functionality in its SDKs that allows your application to display content as it's being generated, rather than waiting for the complete response.

## When to Use Streaming

Streaming is particularly useful for:

* Real-time chat interfaces
* Long-form content generation
* Applications where perceived speed is important
* Interactive agent experiences
* Reducing time-to-first-word in user interactions

## Streaming with the Chat Endpoint

One of the primary use cases for streaming in Honcho is with the [chat endpoint](/docs/v3/documentation/features/chat). This allows you to stream the AI's reasoning about a user in real-time.

### Prerequisites

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  # Initialize client (using the default workspace)
  honcho = Honcho()

  # Create or get peers
  user = honcho.peer("demo-user")
  assistant = honcho.peer("assistant")

  # Create a new session
  session = honcho.session("demo-session")

  # Add peers to the session
  session.add_peers([user, assistant])

  # Store some messages for context (optional)
  session.add_messages([
      user.message("Hello, I'm testing the streaming functionality")
  ])
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from '@honcho-ai/sdk';

  (async () => {
      // Initialize client (using the default workspace)
      const honcho = new Honcho({});

      // Create or get peers
      const user = await honcho.peer('demo-user');
      const assistant = await honcho.peer('assistant');

      // Create a new session
      const session = await honcho.session('demo-session');

      // Add peers to the session
      await session.addPeers([user, assistant]);

      // Store some messages for context (optional)
      await session.addMessages([
        user.message("Hello, I'm testing the streaming functionality")
      ]);
  })();
  ```
</CodeGroup>

## Streaming from the Chat Endpoint

<CodeGroup>
  ```python Python theme={null}
  import time

  # Basic streaming example
  response_stream = user.chat("What can you tell me about this user?", stream=True)

  for chunk in response_stream.iter_text():
      print(chunk, end="", flush=True)  # Print each chunk as it arrives
      time.sleep(0.01)  # Optional delay for demonstration
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Basic streaming example
      const responseStream = await user.chat("What can you tell me about this user?", {
        stream: true
      });

      // Process the stream
      for await (const chunk of responseStream.iter_text()) {
        process.stdout.write(chunk);  // Write to console without newlines
      }
  })();
  ```
</CodeGroup>

## Working with Streaming Data

When working with streaming responses, consider these patterns:

1. **Progressive Rendering** - Update your UI as chunks arrive instead of waiting for the full response
2. **Buffered Processing** - Accumulate chunks until a logical break (like a sentence or paragraph)
3. **Token Counting** - Monitor token usage in real-time for applications with token limits
4. **Error Handling** - Implement appropriate error handling for interrupted streams

## Example: Restaurant Recommendation Chat

<CodeGroup>
  ```python Python theme={null}
  import asyncio
  from honcho import Honcho

  async def restaurant_recommendation_chat():
      # Initialize client
      honcho = Honcho()

      # Create peers
      user = honcho.peer("food-lover")
      assistant = honcho.peer("restaurant-assistant")

      # Create session
      session = honcho.session("food-preferences-session")

      # Add peers to session
      await session.add_peers([user, assistant])

      # Store multiple user messages about food preferences
      user_messages = [
          "I absolutely love spicy Thai food, especially curries with coconut milk.",
          "Italian cuisine is another favorite - fresh pasta and wood-fired pizza are my weakness!",
          "I try to eat vegetarian most of the time, but occasionally enjoy seafood.",
          "I can't handle overly sweet desserts, but love something with dark chocolate."
      ]

      # Add the user's messages to the session
      session_messages = [user.message(message) for message in user_messages]
      await session.add_messages(session_messages)

      # Print the user messages
      for message in user_messages:
          print(f"User: {message}")

      # Ask for restaurant recommendations based on preferences
      print("\nRequesting restaurant recommendations...")
      print("Assistant: ", end="", flush=True)
      full_response = ""

      # Stream the response using the user's peer to get recommendations
      response_stream = user.chat(
          "Based on this user's food preferences, recommend 3 restaurants they might enjoy in the Lower East Side.",
          stream=True,
          session_id=session.id
      )

      for chunk in response_stream.iter_text():
          print(chunk, end="", flush=True)
          full_response += chunk
          await asyncio.sleep(0.01)

      # Store the assistant's complete response
      await session.add_messages([
          assistant.message(full_response)
      ])

  # Run the async function
  if __name__ == "__main__":
      asyncio.run(restaurant_recommendation_chat())
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from '@honcho-ai/sdk';

  (async () => {
      async function restaurantRecommendationChat() {
        // Initialize client
        const honcho = new Honcho({});

        // Create peers
        const user = await honcho.peer('food-lover');
        const assistant = await honcho.peer('restaurant-assistant');

        // Create session
        const session = await honcho.session('food-preferences-session');

        // Add peers to session
        await session.addPeers([user, assistant]);

        // Store multiple user messages about food preferences
        const userMessages = [
          "I absolutely love spicy Thai food, especially curries with coconut milk.",
          "Italian cuisine is another favorite - fresh pasta and wood-fired pizza are my weakness!",
          "I try to eat vegetarian most of the time, but occasionally enjoy seafood.",
          "I can't handle overly sweet desserts, but love something with dark chocolate."
        ];

        // Add the user's messages to the session
        const sessionMessages = userMessages.map(message => user.message(message));
        await session.addMessages(sessionMessages);

        // Print the user messages
        for (const message of userMessages) {
          console.log(`User: ${message}`);
        }

        // Ask for restaurant recommendations based on preferences
        console.log("\nRequesting restaurant recommendations...");
        process.stdout.write("Assistant: ");
        let fullResponse = "";

        // Stream the response using the user's peer to get recommendations
        const responseStream = await user.chat(
          "Based on this user's food preferences, recommend 3 restaurants they might enjoy in the Lower East Side.",
          {
            stream: true,
            sessionId: session.id
          }
        );

        for await (const chunk of responseStream.iter_text()) {
          process.stdout.write(chunk);
          fullResponse += chunk;
        }

        // Store the assistant's complete response
        await session.addMessages([
          assistant.message(fullResponse)
        ]);
      }

      await restaurantRecommendationChat();
  })();
  ```
</CodeGroup>

## Performance Considerations

When implementing streaming:

* Consider connection stability for mobile or unreliable networks
* Implement appropriate timeouts for stream operations
* Be mindful of memory usage when accumulating large responses
* Use appropriate error handling for network interruptions

Streaming responses provide a more interactive and engaging user experience. By implementing streaming in your Honcho applications, you can create more responsive AI-powered features that feel natural and immediate to your users.


# Summarizer
Source: https://honcho.dev/docs/v3/documentation/features/advanced/summarizer

How Honcho creates summaries of conversations

Almost all agents require, in addition to personalization and memory, a way to quickly prime a context window with a summary of the conversation (in Honcho, this is equivalent to a `session`). The general strategy for summarization is to combine a list of recent messages verbatim with a compressed LLM-generated summary of the older messages not included. Implementing this correctly, in such a way that the resulting context is:

* Exhaustive: the combination of recent messages and summary should cover the entire conversation
* Dynamically sized: the tokens used on both summary and recent messages should be malleable based on desired token usage
* Performant: while creation of the summary by LLM introduces necessary latency, this should never add latency to an arbitrary end-user request

...is a non-trivial problem. Summarization should not be necessary to re-implement for every new agent you build, so Honcho comes with a built-in solution.

### Creating Summaries

Honcho already has an asynchronous task queue for the purpose of deriving facts from messages. This is the ideal place to create summaries where they won't add latency to a message. Currently, Honcho has two configurable summary types:

* Short summaries: by default, enqueued every 20 messages and given a token limit of 1000
* Long summaries: by default, enqueued every 60 messages and given a token limit of 4000

Both summaries are designed to be exhaustive: when enqueued, they are given the *prior* summary of their type plus every message after that summary. This recursive compression process naturally biases the summary towards recent messages while still covering the entire conversation.

For example, if message 160 in a conversation triggers a short summary, as it would with default settings, the summary task would retrieve the prior short summary (message 140) plus messages 141-160. It would then produce a summary of messages 0-160 and store that in the short summary slot on the session. Every session has a single slot for each summary type: new summaries replace old ones.

It's important to keep in mind that summary tasks run in the background and are not guaranteed to complete before the next message. However, they are guaranteed to complete in order, so that if a user saves 100 messages in a single batch, the short summary will first be created for messages 0-20, then 21-40, and so on, in our desired recursive way.

### Retrieving Summaries

Summaries are retrieved from the session by the [`get_context`](/docs/v3/documentation/features/get-context) method. This method has two parameters:

* `summary`: A boolean indicating whether to include the summary in the return type. The default is true.
* `tokens`: An integer indicating the maximum number of tokens to use for the context. **If not provided, `get_context` will retrieve as many tokens as are required to create exhaustive conversation coverage.**

The return type is simply a list of recent messages and a summary if the flag is used. These two components are dynamically sized based on the token limit. Combined, they will always be below the given token limit. Honcho reserves 60% of the context size for recent messages and 40% for the summary.

There's a critical trade-off to understand between exhaustiveness and token usage. Let's go through some scenarios:

* If the *last message* contains more tokens than the context token limit, no summary *or* message list is possible -- both will be empty.

* If the *last few messages* contain more tokens than the context token limit, no summary is possible -- the context will only contain the last 1 or 2 messages that fit in the token limit.

* If the summaries contain more tokens than the context token limit, no summary is possible -- the context will only contain the X most recent messages that fit in the token limit. Note that while summaries will often be smaller than their token limits, avoiding this scenario means passing a higher token limit than the Honcho-configured summary size(s). For this reason, the default token limit for `get_context` is a few times larger than the configured long summary size.

The above scenarios indicate where summarization is not possible -- therefore, the context retrieved will almost certainly **not** be exhaustive.

Sometimes, gaps in context aren't an issue. In these cases, it's best to pass a reasonable token limit depending on your needs. Other cases demand exhaustive context -- don't pass a token limit and just let Honcho retrieve the ideal combination of summary and recent messages. Finally, if you don't care about the conversation at large and just want the last few messages, set `summary` to false and `tokens` to some multiple of your desired message count. Note that context messages are not paginated, so there's a hard limit on the number of messages that can be retrieved (currently 100,000 tokens).

As a final note, remember that summaries are generated asynchronously and therefore may not be available immediately. If you batch-save a large number of messages, assume that summaries will not be available until those messages are processed, which can take seconds to minutes depending on the number of messages and the configured LLM provider. Exhaustive `get_context` calls performed during this time will likely just return the messages in the session.


# Using Filters
Source: https://honcho.dev/docs/v3/documentation/features/advanced/using-filters

Learn how to filter workspaces, peers, sessions, and messages using Honcho's powerful filtering system

Honcho provides a sophisticated filtering system that allows you to query workspaces, peers, sessions, and messages with precise control. The filtering system supports logical operators, comparison operators, metadata filtering, and wildcards to help you find exactly what you need.

## Basic Filtering Concepts

Filters in Honcho are expressed as dictionaries that define conditions for matching resources. The system supports both simple equality filters and complex queries with multiple conditions.

### Simple Filters

The most basic filters check for exact matches:

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  # Initialize client
  honcho = Honcho()

  # Simple peer filter
  peers = honcho.peers(filters={"peer_id": "alice"})

  # Simple session filter with metadata
  sessions = honcho.sessions(filters={
      "metadata": {"type": "support"}
  })

  # Simple message filter
  messages = honcho.messages(filters={
      "session_id": "support-chat-1",
      "peer_id": "alice"
  })
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from "@honcho-ai/sdk";

  (async () => {
      // Initialize client
      const honcho = new Honcho({});

      // Simple peer filter
      const peers = await honcho.peers({
        filters: { peer_id: "alice" }
      });

      // Simple session filter with metadata
      const sessions = await honcho.sessions({
        filters: {
          metadata: { type: "support" }
        }
      });

      // Simple message filter
      const messages = await honcho.messages({
        filters: {
          session_id: "support-chat-1",
          peer_id: "alice"
        }
      });
  })();
  ```
</CodeGroup>

## Logical Operators

Combine multiple conditions using logical operators for complex queries:

### AND Operator

Use AND to require all conditions to be true:

<CodeGroup>
  ```python Python theme={null}
  messages = honcho.messages(filters={
      "AND": [
          {"session_id": "chat-1"},
          {"created_at": {"gte": "2024-01-01"}}
      ]
  })
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      const messages = await honcho.messages({
        filters: {
          AND: [
            { session_id: "chat-1" },
            { created_at: { gte: "2024-01-01" } }
          ]
        }
      });
  })();
  ```
</CodeGroup>

### OR Operator

Use OR to match any of the specified conditions:

<CodeGroup>
  ```python Python theme={null}
  # Find messages from either alice or bob
  messages = session.messages(filters={
      "OR": [
          {"peer_id": "alice"},
          {"peer_id": "bob"}
      ]
  })

  # Complex OR with metadata conditions
  sessions = honcho.sessions(filters={
      "OR": [
          {"metadata": {"priority": "high"}},
          {"metadata": {"urgent": True}},
          {"metadata": {"escalated": True}}
      ]
  })
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Find messages from either alice or bob
      const messages = await session.messages({
        filters: {
          OR: [
            { peer_id: "alice" },
            { peer_id: "bob" }
          ]
        }
      });

      // Complex OR with metadata conditions
      const sessions = await honcho.sessions({
        filters: {
          OR: [
            { metadata: { priority: "high" } },
            { metadata: { urgent: true } },
            { metadata: { escalated: true } }
          ]
        }
      });
  })();
  ```
</CodeGroup>

### NOT Operator

Use NOT to exclude specific conditions:

<CodeGroup>
  ```python Python theme={null}
  # Find all peers except alice
  peers = honcho.peers(filters={
      "NOT": [
          {"peer_id": "alice"}
      ]
  })

  # Find sessions that are NOT completed
  sessions = honcho.sessions(filters={
      "NOT": [
          {"metadata": {"status": "completed"}}
      ]
  })
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Find all peers except alice
      const peers = await honcho.peers({
        filters: {
          NOT: [
            { peer_id: "alice" }
          ]
        }
      });

      // Find sessions that are NOT completed
      const sessions = await honcho.sessions({
        filters: {
          NOT: [
            { metadata: { status: "completed" } }
          ]
        }
      });
  })();
  ```
</CodeGroup>

### Combining Logical Operators

Create sophisticated queries by combining different logical operators:

<CodeGroup>
  ```python Python theme={null}
  # Find messages from alice OR bob, but NOT where message has archived set to true in metadata
  messages = session.messages(filters={
      "AND": [
          {
              "OR": [
                  {"peer_id": "alice"},
                  {"peer_id": "bob"}
              ]
          },
          {
              "NOT": [
                  {"metadata": {"archived": True}}
              ]
          }
      ]
  })
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Find messages from alice OR bob, but NOT where message has archived set to true in metadata
      const messages = await session.messages({
        filters: {
          AND: [
            {
              OR: [
                { peer_id: "alice" },
                { peer_id: "bob" }
              ]
            },
            {
              NOT: [
                { metadata: { archived: true } }
              ]
            }
          ]
        }
      });
  })();
  ```
</CodeGroup>

## Comparison Operators

Use comparison operators for range queries and advanced matching:

### Numeric Comparisons

<CodeGroup>
  ```python Python theme={null}
  # Find sessions created after a specific date
  sessions = honcho.sessions(filters={
      "created_at": {"gte": "2024-01-01"}
  })

  # Find messages within a date range
  messages = session.messages(filters={
      "created_at": {
          "gte": "2024-01-01",
          "lte": "2024-12-31"
      }
  })

  # Metadata numeric comparisons
  sessions = honcho.sessions(filters={
      "metadata": {
          "score": {"gt": 8.5},
          "duration": {"lte": 3600}
      }
  })
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Find sessions created after a specific date
      const sessions = await honcho.sessions({
        filters: {
          created_at: { gte: "2024-01-01" }
        }
      });

      // Find messages within a date range
      const messages = await session.messages({
        filters: {
          created_at: {
            gte: "2024-01-01",
            lte: "2024-12-31"
          }
        }
      });

      // Metadata numeric comparisons
      const filteredSessions = await honcho.sessions({
        filters: {
          metadata: {
            score: { gt: 8.5 },
            duration: { lte: 3600 }
          }
        }
      });
  })();
  ```
</CodeGroup>

### List Membership

<CodeGroup>
  ```python Python theme={null}
  # Find messages from specific peers in a session
  messages = session.messages(filters={
      "peer_id": {"in": ["alice", "bob", "charlie"]}
  })

  # Find sessions with specific tags
  sessions = honcho.sessions(filters={
      "metadata": {
          "tag": {"in": ["important", "urgent", "follow-up"]}
      }
  })

  # Not equal comparisons
  peers = honcho.peers(filters={
      "metadata": {
          "status": {"ne": "inactive"}
      }
  })
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Find messages from specific peers in a session
      const messages = await session.messages({
        filters: {
          peer_id: { in: ["alice", "bob", "charlie"] }
        }
      });

      // Find sessions with specific tags
      const sessions = await honcho.sessions({
        filters: {
          metadata: {
            tag: { in: ["important", "urgent", "follow-up"] }
          }
        }
      });

      // Not equal comparisons
      const peers = await honcho.peers({
        filters: {
          metadata: {
            status: { ne: "inactive" }
          }
        }
      });
  })();
  ```
</CodeGroup>

## Metadata Filtering

Metadata filtering is particularly powerful in Honcho, supporting nested conditions and complex queries:

### Basic Metadata Filtering

<CodeGroup>
  ```python Python theme={null}
  # Simple metadata equality
  sessions = honcho.sessions(filters={
      "metadata": {
          "type": "customer_support",
          "priority": "high"
      }
  })

  # Nested metadata objects
  peers = honcho.peers(filters={
      "metadata": {
          "profile": {
              "role": "admin",
              "department": "engineering"
          }
      }
  })
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Simple metadata equality
      const sessions = await honcho.sessions({
        filters: {
          metadata: {
            type: "customer_support",
            priority: "high"
          }
        }
      });

      // Nested metadata objects
      const peers = await honcho.peers({
        filters: {
          metadata: {
            profile: {
              role: "admin",
              department: "engineering"
            }
          }
        }
      });
  })();
  ```
</CodeGroup>

### Advanced Metadata Queries

<Info>
  If you want to do advanced queries like these, make sure not to create metadata fields that use the same names as the included comparison operators! For example, if you have a metadata field called `contains`, it will conflict with the `contains` operator.
</Info>

<CodeGroup>
  ```python Python theme={null}
  # Metadata with comparison operators
  sessions = honcho.sessions(filters={
      "metadata": {
          "score": {"gte": 4.0, "lte": 5.0},
          "created_by": {"ne": "system"},
          "tags": {"contains": "important"}
      }
  })

  # Complex metadata conditions
  messages = session.messages(filters={
      "AND": [
          {"metadata": {"sentiment": {"in": ["positive", "neutral"]}}},
          {"metadata": {"confidence": {"gt": 0.8}}},
          {"content": {"icontains": "thank"}}
      ]
  })
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Metadata with comparison operators
      const sessions = await honcho.sessions({
        filters: {
          metadata: {
            score: { gte: 4.0, lte: 5.0 },
            created_by: { ne: "system" },
            tags: { contains: "important" }
          }
        }
      });

      // Complex metadata conditions
      const messages = await session.messages({
        filters: {
          AND: [
            { metadata: { sentiment: { in: ["positive", "neutral"] } } },
            { metadata: { confidence: { gt: 0.8 } } },
            { content: { icontains: "thank" } }
          ]
        }
      });
  })();
  ```
</CodeGroup>

## Wildcards

Use wildcards (\*) to match any value for a field:

<CodeGroup>
  ```python Python theme={null}
  # Find all sessions with any peer_id (essentially all sessions)
  sessions = honcho.sessions(filters={
      "peer_id": "*"
  })

  # Wildcard in lists - matches everything
  messages = session.messages(filters={
      "peer_id": {"in": ["alice", "bob", "*"]}
  })

  # Metadata wildcards
  sessions = honcho.sessions(filters={
      "metadata": {
          "type": "*",  # Any type
          "status": "active"  # But status must be active
      }
  })
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Find all sessions with any peer_id (essentially all sessions)
      const sessions = await honcho.sessions({
        filters: {
          peer_id: "*"
        }
      });

      // Wildcard in lists - matches everything
      const messages = await session.messages({
        filters: {
          peer_id: { in: ["alice", "bob", "*"] }
        }
      });

      // Metadata wildcards
      const filteredSessions = await honcho.sessions({
        filters: {
          metadata: {
            type: "*",  // Any type
            status: "active"  // But status must be active
          }
        }
      });
  })();
  ```
</CodeGroup>

## Resource-Specific Examples

### Filtering Workspaces

<CodeGroup>
  ```python Python theme={null}
  # Find workspaces by name pattern
  workspaces = honcho.workspaces(filters={
      "name": {"contains": "prod"}
  })

  # Filter by metadata
  workspaces = honcho.workspaces(filters={
      "metadata": {
          "environment": "production",
          "team": {"in": ["backend", "frontend", "devops"]}
      }
  })
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Find workspaces by name pattern
      const workspaces = await honcho.workspaces({
        filters: {
          name: { contains: "prod" }
        }
      });

      // Filter by metadata
      const workspaces = await honcho.workspaces({
        filters: {
          metadata: {
            environment: "production",
            team: { in: ["backend", "frontend", "devops"] }
          }
        }
      });
  })();
  ```
</CodeGroup>

### Filtering Messages

<CodeGroup>
  ```python Python theme={null}
  # Find error messages from the last week
  from datetime import datetime, timedelta

  week_ago = (datetime.now() - timedelta(days=7)).isoformat()
  messages = session.messages(filters={
      "AND": [
          {"content": {"icontains": "error"}},
          {"created_at": {"gte": week_ago}},
          {"metadata": {"level": {"in": ["error", "critical"]}}}
      ]
  })

  # Find messages in specific sessions with sentiment analysis
  messages = session.messages(filters={
      "AND": [
          {"session_id": {"in": ["support-1", "support-2", "support-3"]}},
          {"metadata": {"sentiment": "negative"}},
          {"metadata": {"confidence": {"gte": 0.7}}}
      ]
  })
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Find error messages from the last week
      const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();
      const messages = await session.messages({
        filters: {
          AND: [
            { content: { icontains: "error" } },
            { created_at: { gte: weekAgo } },
            { metadata: { level: { in: ["error", "critical"] } } }
          ]
        }
      });

      // Find messages in specific sessions with sentiment analysis
      const sentimentMessages = await session.messages({
        filters: {
          AND: [
            { session_id: { in: ["support-1", "support-2", "support-3"] } },
            { metadata: { sentiment: "negative" } },
            { metadata: { confidence: { gte: 0.7 } } }
          ]
        }
      });
  })();
  ```
</CodeGroup>

### Filtering Conclusions

Conclusions are scoped to an observer/observed peer pair (accessed via
`peer.conclusions` for self-conclusions or `peer.conclusions_of(target)` for
conclusions about another peer). The observer and observed are filled in
automatically by the scope, so the `filters` you pass add to them.

The most useful conclusion-specific field is `level`, the reasoning level:

* `explicit` — extracted directly from messages
* `deductive` / `inductive` / `contradiction` — derived later during dreaming

A common request is to surface only the directly-stated facts and exclude
anything inferred during dreaming — filter `level` to `explicit`:

<CodeGroup>
  ```python Python theme={null}
  # Only conclusions extracted directly from messages (exclude dream-derived)
  explicit = peer.conclusions.list(filters={"level": "explicit"})

  # Only dream-derived conclusions
  derived = peer.conclusions.list(filters={"level": {"in": ["deductive", "inductive"]}})

  # Same filtering on semantic search
  results = peer.conclusions.query(
      "food preferences",
      filters={"level": "deductive"},
  )

  # Conclusions about another peer, explicit only
  bob_explicit = peer.conclusions_of("bob").list(filters={"level": "explicit"})
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Only conclusions extracted directly from messages (exclude dream-derived)
      const explicit = await peer.conclusions.list({ filters: { level: "explicit" } });

      // Only dream-derived conclusions
      const derived = await peer.conclusions.list({
        filters: { level: { in: ["deductive", "inductive"] } }
      });

      // Same filtering on semantic search (query, topK, distance, filters)
      const results = await peer.conclusions.query(
        "food preferences",
        10,
        undefined,
        { level: "deductive" }
      );

      // Conclusions about another peer, explicit only
      const bobExplicit = await peer.conclusionsOf("bob").list({
        filters: { level: "explicit" }
      });
  })();
  ```
</CodeGroup>

## Error Handling

Handle filter errors gracefully:

<CodeGroup>
  ```python Python theme={null}
  from honcho.exceptions import FilterError

  try:
      # Invalid filter - unsupported operator
      messages = session.messages(filters={
          "created_at": {"invalid_operator": "2024-01-01"}
      })
  except FilterError as e:
      print(f"Filter error: {e}")
      # Handle the error appropriately

  try:
      # Invalid column name
      sessions = honcho.sessions(filters={
          "nonexistent_field": "value"
      })
  except FilterError as e:
      print(f"Invalid field: {e}")
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      try {
        // Invalid filter - unsupported operator
        const messages = await session.messages({
          filters: {
            created_at: { invalid_operator: "2024-01-01" }
          }
        });
      } catch (error) {
        if (error.message.includes("filters")) {
          console.error(`Filter error: ${error.message}`);
          // Handle the error appropriately
        }
      }

      try {
        // Invalid column name
        const sessions = await honcho.sessions({
          filters: {
            nonexistent_field: "value"
          }
        });
      } catch (error) {
        console.error(`Invalid field: ${error.message}`);
      }
  })();
  ```
</CodeGroup>

## Conclusion

Honcho's filtering system provides powerful capabilities for querying your conversational data. By understanding how to:

* Use simple equality filters and complex logical operators
* Apply comparison operators for range and pattern matching
* Filter metadata with nested conditions
* Handle wildcards and dynamic filter construction
* Follow best practices for performance and validation

You can build sophisticated applications that efficiently find and process exactly the conversations, messages, and insights you need from your Honcho data.


# Chat Endpoint
Source: https://honcho.dev/docs/v3/documentation/features/chat

An endpoint for reasoning about your users

The Chat endpoint (`peer.chat()`) is the natural language interface to Honcho's reasoning. Instead of manually retrieving conclusions, your LLM can ask questions and get synthesized answers based on all the reasoning Honcho has done about a peer. Think of it as agent-to-agent communication.

## Basic Usage

The simplest way to use the chat endpoint is to ask a question and get a text response:

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  honcho = Honcho()
  peer = honcho.peer("user-123")

  # Ask Honcho about the peer
  query = "What is the user's favorite way of completing the task?"
  answer = peer.chat(query)

  print(answer)
  # "Based on conclusions, the user prefers using keyboard shortcuts..."
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from '@honcho-ai/sdk';

  const honcho = new Honcho({});
  const peer = await honcho.peer("user-123");

  // Ask Honcho about the peer
  const query = "What is the user's favorite way of completing the task?";
  const answer = await peer.chat(query);

  console.log(answer);
  // "Based on conclusions, the user prefers using keyboard shortcuts..."
  ```
</CodeGroup>

The chat endpoint searches through the peer's representation--all the conclusions Honcho has reasoned about them--and synthesizes a natural language answer.

## Reasoning Level

Use `reasoning_level` to trade off speed against depth for a specific chat request. It is optional and defaults to `low`. Accepted values are `minimal`, `low`, `medium`, `high`, and `max`.

The reasoning level controls which model the request is routed to, the tools used by the agent, the thinking budget, the maximum tool-iteration count, and output token limits.

| Level     | When to use                         | Notes                                                       |
| --------- | ----------------------------------- | ----------------------------------------------------------- |
| `minimal` | Fast factual lookups                | Smallest prefetch window and minimal tools for lower cost.  |
| `low`     | Default balance                     | Standard tool set and budgets.                              |
| `medium`  | Multi-step or ambiguous questions   | Calls fewer tools than `low`, but thinks harder and longer. |
| `high`    | Complex synthesis across sources    | Thinks like `medium`, but uses more tools.                  |
| `max`     | Deep research, most complex queries | Highest thinking budget, max iterations.                    |

<CodeGroup>
  ```python Python theme={null}
  query = "Summarize the user's long-term goals."
  answer = peer.chat(query, reasoning_level="high")
  ```

  ```typescript TypeScript theme={null}
  const query = "Summarize the user's long-term goals.";
  const answer = await peer.chat(query, { reasoningLevel: "high" });
  ```
</CodeGroup>

## Streaming Responses

For longer answers, use streaming to get incremental responses:

<CodeGroup>
  ```python Python theme={null}
  query = "What do we know about the user?"
  response_stream = peer.chat(query, stream=True)

  for chunk in response_stream.iter_text():
      print(chunk, end="", flush=True)
  ```

  ```typescript TypeScript theme={null}
  const query = "What do we know about the user?";
  const responseStream = await peer.chat(query, { stream: true });

  for await (const chunk of responseStream.iter_text()) {
      process.stdout.write(chunk);
  }
  ```
</CodeGroup>

Streaming is useful for displaying real-time responses in chat interfaces or when asking complex questions that require longer answers.

## Integration Patterns

### Dynamic Prompt Enhancement

Let your LLM decide what it needs to know, then inject that context into the next generation:

<CodeGroup>
  ```python Python theme={null}
  # Your LLM generates a query based on the conversation
  llm_query = "Does the user prefer formal or casual communication?"

  # Get answer from Honcho
  context = peer.chat(llm_query)

  # Add to your next LLM prompt
  enhanced_prompt = f"""
  Context about the user: {context}

  User message: {user_input}

  Respond appropriately based on the context.
  """
  ```

  ```typescript TypeScript theme={null}
  // Your LLM generates a query based on the conversation
  const llmQuery = "Does the user prefer formal or casual communication?";

  // Get answer from Honcho
  const context = await peer.chat(llmQuery);

  // Add to your next LLM prompt
  const enhancedPrompt = `
  Context about the user: ${context}

  User message: ${userInput}

  Respond appropriately based on the context.
  `;
  ```
</CodeGroup>

### Conditional Logic

Use chat endpoint responses to drive application logic:

<CodeGroup>
  ```python Python theme={null}
  # Check if user has completed onboarding
  onboarding_status = peer.chat("Has the user completed the onboarding flow?")

  if "yes" in onboarding_status.lower():
      # Show main interface
      pass
  else:
      # Show onboarding
      pass
  ```

  ```typescript TypeScript theme={null}
  // Check if user has completed onboarding
  const onboardingStatus = await peer.chat("Has the user completed the onboarding flow?");

  if (onboardingStatus.toLowerCase().includes("yes")) {
      // Show main interface
  } else {
      // Show onboarding
  }
  ```
</CodeGroup>

### Preference Extraction

Extract specific preferences for personalization:

<CodeGroup>
  ```python Python theme={null}
  # Get multiple insights
  tone = peer.chat("What tone does the user prefer in responses?")
  expertise = peer.chat("What is the user's level of technical expertise?")
  goals = peer.chat("What are the user's main goals or objectives?")

  # Use these to configure your agent's behavior
  ```

  ```typescript TypeScript theme={null}
  // Get multiple insights
  const tone = await peer.chat("What tone does the user prefer in responses?");
  const expertise = await peer.chat("What is the user's level of technical expertise?");
  const goals = await peer.chat("What are the user's main goals or objectives?");

  // Use these to configure your agent's behavior
  ```
</CodeGroup>

## How Honcho Answers

When you call `peer.chat(query)`:

1. Honcho searches through the peer's peer card and representation--conclusions drawn from reasoning over their messages
2. Retrieves conclusions semantically relevant to your query
3. Combines them with segments of source messages, if needed, to gather more context
4. Synthesizes them into a coherent natural language response to your query

Honcho [reasoning](/docs/v3/documentation/core-concepts/reasoning) runs continuously in the background, processing new messages and updating representations. The chat endpoint always has access to Honcho's latest conclusions about the peer.

## Best Practices

### Ask specific questions

Instead of "Tell me about the user", ask "What communication style does the user prefer?" You'll get more actionable answers.

### Let your LLM formulate queries

The chat endpoint shines when your LLM decides what it needs to know. This creates dynamic, context-aware personalization. An excellent way to achieve this, if building an agent, is to give access to the Honcho chat endpoint as just another tool.

### Use for runtime decisions

Don't just use chat for LLM prompts - use it to drive application logic, routing, and feature flags based on user behavior.

### Combine with context()

Use `context()` for conversation context and `peer.chat()` for specific insights. They complement each other.

For more ideas on using the chat endpoint, see our [guides](/docs/v3/guides/overview).


# Get Context
Source: https://honcho.dev/docs/v3/documentation/features/get-context

Learn how to use context() to retrieve and format conversation context for LLM integration

The `context()` method is a powerful feature that retrieves formatted conversation context from sessions, making it easy to integrate with LLMs like OpenAI, Anthropic, and others. This guide covers everything you need to know about working with session context.

<Note>
  By default, the context includes a blend of summary and messages ***which covers the entire session history of a peer***.
</Note>

Summaries are automatically generated at intervals and recent messages are included depending on how many tokens the context is intended to be. You can specify any token limit you want, and can disable summaries to fill that limit entirely with recent messages. To get representation data, you need to specify a target peer.

## Basic Usage

The `context()` method is available on all Session objects and returns a `SessionContext` that contains the formatted conversation history.

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  # Initialize client and create session
  honcho = Honcho()
  session = honcho.session("conversation-1")

  # Get basic context (not very useful before adding any messages!)
  context = session.context()
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from "@honcho-ai/sdk";

  (async () => {
      // Initialize client and create session
      const honcho = new Honcho({});
      const session = await honcho.session("conversation-1");

      // Get basic context (not very useful before adding any messages!)
      const context = await session.context();
  })();
  ```
</CodeGroup>

## Context Parameters

The `context()` method accepts several optional parameters to customize the retrieved context:

### Token Limits

Control the size of the context by setting a maximum token count:

<CodeGroup>
  ```python Python theme={null}
  # Limit context to 1500 tokens
  context = session.context(tokens=1500)

  # Limit context to 3000 tokens for larger conversations
  context = session.context(tokens=3000)
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Limit context to 1500 tokens
      const context = await session.context({ tokens: 1500 });

      // Limit context to 3000 tokens for larger conversations
      const context = await session.context({ tokens: 3000 });
  })();
  ```
</CodeGroup>

### Summary Mode

Enable summary mode (on by default) to get a condensed version of the conversation:

<CodeGroup>
  ```python Python theme={null}
  # Get context with summary enabled -- will contain both summary and messages
  context = session.context(summary=True)

  # Combine summary=False with token limits to get more messages
  context = session.context(summary=False, tokens=2000)
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Get context with summary enabled -- will contain both summary and messages
      const context = await session.context({ summary: true });

      // Combine summary=False with token limits to get more messages
      const context = await session.context({
        summary: false,
        tokens: 2000
      });
  })();
  ```
</CodeGroup>

### Peer Representation in Context

You can include a peer's [representation](/docs/v3/documentation/core-concepts/representation) and peer card in the context by specifying `peer_target`. This is useful for providing the LLM with knowledge about a specific peer.

<CodeGroup>
  ```python Python theme={null}
  # Get context with peer representation included
  context = session.context(
      tokens=2000,
      peer_target="user-123"  # Include representation of user-123
  )

  # Access the representation and peer card
  print(context.peer_representation)  # String representation
  print(context.peer_card)            # List of peer card items

  # Get representation from a specific peer's perspective
  context = session.context(
      tokens=2000,
      peer_target="user-123",
      peer_perspective="assistant"  # From assistant's viewpoint
  )
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Get context with peer representation included
      const context = await session.context({
        tokens: 2000,
        peerTarget: "user-123"  // Include representation of user-123
      });

      // Access the representation and peer card
      console.log(context.peerRepresentation);  // String representation
      console.log(context.peerCard);            // Array of peer card items

      // Get representation from a specific peer's perspective
      const perspectiveContext = await session.context({
        tokens: 2000,
        peerTarget: "user-123",
        peerPerspective: "assistant"  // From assistant's viewpoint
      });
  })();
  ```
</CodeGroup>

### Semantic Search

Use `search_query` to fetch semantically relevant conclusions based on a query string (requires `peer_target`):

<CodeGroup>
  ```python Python theme={null}
  context = session.context(
      tokens=2000,
      peer_target="user-123",
      search_query="What are my coding preferences?",
      search_top_k=10,           # Number of relevant conclusions to fetch
      search_max_distance=0.8,   # Max semantic distance (0.0-1.0)
      include_most_frequent=True, # Include most frequent conclusions
      max_conclusions=25        # Cap total conclusions
  )
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      const context = await session.context({
        tokens: 2000,
        peerTarget: "user-123",
        representationOptions: {
          searchQuery: "What are my coding preferences?",
          searchTopK: 10,           // Number of relevant conclusions to fetch
          searchMaxDistance: 0.8,   // Max semantic distance (0.0-1.0)
          includeMostFrequent: true, // Include most frequent conclusions
          maxConclusions: 25       // Cap total conclusions
        }
      });
  })();
  ```
</CodeGroup>

### Session-Scoped Representations

Use `limit_to_session` to only include conclusions from the current session:

<CodeGroup>
  ```python Python theme={null}
  # Get context limited to this session's conclusions only
  context = session.context(
      tokens=2000,
      peer_target="user-123",
      limit_to_session=True  # Only conclusions from this session
  )
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Get context limited to this session's conclusions only
      const context = await session.context({
        tokens: 2000,
        peerTarget: "user-123",
        limitToSession: true  // Only conclusions from this session
      });
  })();
  ```
</CodeGroup>

### All Parameters Reference

| Parameter               | Type    | Description                                       |
| ----------------------- | ------- | ------------------------------------------------- |
| `summary`               | `bool`  | Include summary in context (default: true)        |
| `tokens`                | `int`   | Maximum tokens to include                         |
| `peer_target`           | `str`   | Peer ID to include representation for             |
| `peer_perspective`      | `str`   | Peer ID for perspective (requires peer\_target)   |
| `search_query`          | `str`   | Query for semantic search (requires peer\_target) |
| `limit_to_session`      | `bool`  | Limit to session conclusions only                 |
| `search_top_k`          | `int`   | Semantic search results to include (1-100)        |
| `search_max_distance`   | `float` | Max semantic distance (0.0-1.0)                   |
| `include_most_frequent` | `bool`  | Include most frequent conclusions                 |
| `max_conclusions`       | `int`   | Maximum conclusions to include (1-100)            |

## Converting to LLM Formats

The `SessionContext` object provides methods to convert the context into formats compatible with popular LLM APIs. When converting to OpenAI format, you must specify the assistant peer to format the context in such a way that the LLM can understand it.

### OpenAI Format

Convert context to OpenAI's chat completion format:

<CodeGroup>
  ```python Python theme={null}
  # Create peers
  alice = honcho.peer("alice")
  assistant = honcho.peer("assistant")

  # Add some conversation
  session.add_messages([
      alice.message("What's the weather like today?"),
      assistant.message("It's sunny and 75°F outside!")
  ])

  # Get context and convert to OpenAI format
  context = session.context()
  openai_messages = context.to_openai(assistant=assistant)

  # The messages are now ready for OpenAI API
  print(openai_messages)
  # [
  #   {"role": "user", "content": "What's the weather like today?"},
  #   {"role": "assistant", "content": "It's sunny and 75°F outside!"}
  # ]
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Create peers
      const alice = await honcho.peer("alice");
      const assistant = await honcho.peer("assistant");

      // Add some conversation
      await session.addMessages([
        alice.message("What's the weather like today?"),
        assistant.message("It's sunny and 75°F outside!")
      ]);

      // Get context and convert to OpenAI format
      const context = await session.context();
      const openaiMessages = context.toOpenAI(assistant);

      // The messages are now ready for OpenAI API
      console.log(openaiMessages);
      // [
      //   {"role": "user", "content": "What's the weather like today?"},
      //   {"role": "assistant", "content": "It's sunny and 75°F outside!"}
      // ]
  })();
  ```
</CodeGroup>

### Anthropic Format

Convert context to Anthropic's Claude format:

<CodeGroup>
  ```python Python theme={null}
  # Get context and convert to Anthropic format
  context = session.context()
  anthropic_messages = context.to_anthropic(assistant=assistant)

  # Ready for Anthropic API
  print(anthropic_messages)
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Get context and convert to Anthropic format
      const context = await session.context();
      const anthropicMessages = context.toAnthropic(assistant);

      // Ready for Anthropic API
      console.log(anthropicMessages);
  })();
  ```
</CodeGroup>

## Complete LLM Integration Examples

### Using with OpenAI

<CodeGroup>
  ```python Python theme={null}
  import openai
  from honcho import Honcho

  # Initialize clients
  honcho = Honcho()
  openai_client = openai.OpenAI()

  # Set up conversation
  session = honcho.session("support-chat")
  user = honcho.peer("user-123")
  assistant = honcho.peer("support-bot")

  # Add conversation history
  session.add_messages([
      user.message("I'm having trouble with my account login"),
      assistant.message("I can help you with that. What error message are you seeing?"),
      user.message("It says 'Invalid credentials' but I'm sure my password is correct")
  ])

  # Get context for LLM
  messages = session.context(tokens=2000).to_openai(assistant=assistant)

  # Add new user message and get AI response
  messages.append({
      "role": "user",
      "content": "Can you reset my password?"
  })

  response = openai_client.chat.completions.create(
      model="gpt-4",
      messages=messages
  )

  # Add AI response back to session
  session.add_messages([
      user.message("Can you reset my password?"),
      assistant.message(response.choices[0].message.content)
  ])
  ```

  ```typescript TypeScript theme={null}
  import OpenAI from 'openai';
  import { Honcho } from "@honcho-ai/sdk";

  (async () => {
      // Initialize clients
      const honcho = new Honcho({});
      const openai = new OpenAI();

      // Set up conversation
      const session = await honcho.session("support-chat");
      const user = await honcho.peer("user-123");
      const assistant = await honcho.peer("support-bot");

      // Add conversation history
      await session.addMessages([
        user.message("I'm having trouble with my account login"),
        assistant.message("I can help you with that. What error message are you seeing?"),
        user.message("It says 'Invalid credentials' but I'm sure my password is correct")
      ]);

      // Get context for LLM
      const messages = (await session.context({ tokens: 2000 })).toOpenAI(assistant);

      // Add new user message and get AI response
      const response = await openai.chat.completions.create({
        model: "gpt-4",
        messages: [
          ...messages,
          { role: "user", content: "Can you reset my password?" }
        ]
      });

      // Add AI response back to session
      await session.addMessages([
        user.message("Can you reset my password?"),
        assistant.message(response.choices[0].message.content)
      ]);
  })();
  ```
</CodeGroup>

### Multi-Turn Conversation Loop

<CodeGroup>
  ```python Python theme={null}
  def chat_loop():
      """Example of a continuous chat loop using context()"""

      session = honcho.session("chat-session")
      user = honcho.peer("user")
      assistant = honcho.peer("ai-assistant")

      while True:
          # Get user input
          user_input = input("You: ")
          if user_input.lower() in ['quit', 'exit']:
              break

          # Add user message to session
          session.add_messages([user.message(user_input)])

          # Get conversation context
          context = session.context(tokens=2000)
          messages = context.to_openai(assistant=assistant)

          # Get AI response
          response = openai_client.chat.completions.create(
              model="gpt-4",
              messages=messages
          )

          ai_response = response.choices[0].message.content
          print(f"Assistant: {ai_response}")

          # Add AI response to session
          session.add_messages([assistant.message(ai_response)])

  # Start the chat loop
  chat_loop()
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      async function chatLoop() {
        const session = await honcho.session("chat-session");
        const user = await honcho.peer("user");
        const assistant = await honcho.peer("ai-assistant");

        // This would be replaced with actual user input handling in a real app
        const userInputs = [
          "Hello, how are you?",
          "What's the weather like?",
          "Tell me a joke"
        ];

        for (const userInput of userInputs) {
          console.log(`You: ${userInput}`);

          // Add user message to session
          await session.addMessages([user.message(userInput)]);

          // Get conversation context
          const context = await session.context({ tokens: 2000 });
          const messages = context.toOpenAI(assistant);

          // Get AI response
          const response = await openai.chat.completions.create({
            model: "gpt-4",
            messages: messages
          });

          const aiResponse = response.choices[0].message.content;
          console.log(`Assistant: ${aiResponse}`);

          // Add AI response to session
          await session.addMessages([assistant.message(aiResponse)]);
        }
      }

      // Start the chat loop
      await chatLoop();
  })();
  ```
</CodeGroup>

## Advanced Context Usage

### Context with Summaries for Long Conversations

For very long conversations, use summaries to maintain context while controlling token usage:

<CodeGroup>
  ```python Python theme={null}
  # For long conversations, use summary mode
  long_session = honcho.session("long-conversation")

  # Get summarized context to fit within token limits
  context = long_session.context(summary=True, tokens=1500)
  messages = context.to_openai(assistant=assistant)

  # This will include a summary of older messages and recent full messages
  print(f"Context contains {len(messages)} formatted messages")
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // For long conversations, use summary mode
      const longSession = await honcho.session("long-conversation");

      // Get summarized context to fit within token limits
      const context = await longSession.context({
        summary: true,
        tokens: 1500
      });
      const messages = context.toOpenAI(assistant);

      // This will include a summary of older messages and recent full messages
      console.log(`Context contains ${messages.length} formatted messages`);
  })();
  ```
</CodeGroup>

### Context for Different Assistant Types

You can get context formatted for different types of assistants in the same session:

<CodeGroup>
  ```python Python theme={null}
  # Create different assistant peers
  chatbot = honcho.peer("chatbot")
  analyzer = honcho.peer("data-analyzer")
  moderator = honcho.peer("moderator")

  # Get context formatted for each assistant type
  chatbot_context = session.context().to_openai(assistant=chatbot)
  analyzer_context = session.context().to_openai(assistant=analyzer)
  moderator_context = session.context().to_openai(assistant=moderator)

  # Each context will format the conversation from that assistant's perspective
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Create different assistant peers
      const chatbot = await honcho.peer("chatbot");
      const analyzer = await honcho.peer("data-analyzer");
      const moderator = await honcho.peer("moderator");

      // Get context formatted for each assistant type
      const context = await session.context();
      const chatbotContext = context.toOpenAI(chatbot);
      const analyzerContext = context.toOpenAI(analyzer);
      const moderatorContext = context.toOpenAI(moderator);

      // Each context will format the conversation from that assistant's perspective
  })();
  ```
</CodeGroup>

## Best Practices

### 1. Token Management

Always set appropriate token limits to control costs and ensure context fits within LLM limits:

<CodeGroup>
  ```python Python theme={null}
  # Good: Set reasonable token limits based on your model
  context = session.context(tokens=3000)  # For GPT-4
  context = session.context(tokens=1500)  # For smaller models

  # Good: Use summaries for very long conversations
  context = session.context(summary=True, tokens=2000)
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Good: Set reasonable token limits based on your model
      const context = await session.context({ tokens: 3000 });  // For GPT-4
      const context = await session.context({ tokens: 1500 });  // For smaller models

      // Good: Use summaries for very long conversations
      const context = await session.context({ summary: true, tokens: 2000 });
  })();
  ```
</CodeGroup>

### 2. Context Caching

For applications with frequent context retrieval, consider caching context when appropriate:

<CodeGroup>
  ```python Python theme={null}
  # Cache context for multiple LLM calls within the same request
  context = session.context(tokens=2000)
  openai_messages = context.to_openai(assistant=assistant)
  anthropic_messages = context.to_anthropic(assistant=assistant)

  # Use the same context object for multiple format conversions
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      // Cache context for multiple LLM calls within the same request
      const context = await session.context({ tokens: 2000 });
      const openaiMessages = context.toOpenAI(assistant);
      const anthropicMessages = context.toAnthropic(assistant);

      // Use the same context object for multiple format conversions
  })();
  ```
</CodeGroup>

### 3. Error Handling

Always handle potential errors when retrieving context:

<CodeGroup>
  ```python Python theme={null}
  try:
      context = session.context(tokens=2000)
  except Exception as e:
      print(f"Error getting context: {e}")
      # Handle error appropriately (fallback to basic context, retry, etc.)
  ```

  ```typescript TypeScript theme={null}
  (async () => {
      try {
        const context = await session.context({ tokens: 2000 });
      } catch (error) {
        console.error(`Error getting context: ${error}`);
        // Handle error appropriately (fallback to basic context, retry, etc.)
      }
  })();
  ```
</CodeGroup>

## Conclusion

The `context()` method is essential for integrating Honcho sessions with LLMs. By understanding how to:

* Retrieve context with appropriate parameters
* Convert context to LLM-specific formats
* Manage token limits and summaries
* Handle multi-turn conversations

You can build sophisticated AI applications that maintain conversation history and context across interactions while integrating seamlessly with popular LLM providers.


# Storing Data
Source: https://honcho.dev/docs/v3/documentation/features/storing-data

Store Data in Honcho to Generate Memories and Insights

The most basic building block of Honcho's data model is the `Message` object.
A `Message` is sent by a `Peer` and saved in a `Session`

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  honcho = Honcho()

  peer = honcho.peer("sample-peer")

  session = honcho.session("sample-session")

  message = peer.message("Hello, world!")

  session.add_messages([message])
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from '@honcho-ai/sdk';

  const honcho = new Honcho({});

  const peer = await honcho.peer('sample-peer');

  const session = await honcho.session('sample-session');

  const message = peer.message('Hello, world!');

  await session.addMessages([message]);
  ```
</CodeGroup>

Once a `Message` is saved in Honcho, it will kick off a background task that
looks at the new data to generate insights about the `Peer` that sent the `Message`

This is the default behavior of Honcho and can be turned off by [configuring the
Peer or Session](/docs/v3/documentation/features/advanced/reasoning-configuration)

This pattern of having a Peer, Session, and Messages is highly flexible and
works for many different use cases and agent setups. Some use cases may only
need a single Peer, but many Sessions. Others will only use a single `Session`
for their entire app. These are flexible components that work in any situation.

## Chat Bots

A common use case for Honcho to is to build a chatbot like ChatGPT or Claude.
In this case you can simply

* Make a `Peer` for the User
* Make a `Peer` for the AI

Then you can make a `Session` for each thread of conversation and save
`Messages` from the user and assistant in each turn of conversation


# Honcho Overview
Source: https://honcho.dev/docs/v3/documentation/introduction/overview



Honcho is an open source memory library with a managed service for building stateful agents. Use it with any model, framework, or architecture. It enables agents to build and maintain state about any entity--users, agents, groups, ideas, and more. And because it's a continual learning system, it understands entities that change over time. Using Honcho as your memory system will earn your agents higher retention, more trust, and help you build data moats to out-compete incumbents.

<Note>
  Honcho has defined the Pareto Frontier of Agent Memory. Watch the [video](https://x.com/honchodotdev/status/2002090546521911703?s=20), check out our [evals page](https://honcho.dev/evals/), and read the [blog post](https://blog.plasticlabs.ai/research/Benchmarking-Honcho) for more detail.
</Note>

<CardGroup>
  <Card title="Get an API Key" icon="key" href="https://app.honcho.dev">
    Sign up and start building with Honcho
  </Card>

  <Card title="Quickstart" icon="rocket" href="/v3/documentation/introduction/quickstart">
    Build your first stateful agent in minutes
  </Card>
</CardGroup>

## Why Use Honcho?

Honcho streamlines the agent building process by offering elegant, flexible primitives for managing context. It also reasons over that context to give developers access to far richer insights only accessible through reasoning.

Take the following scenario:

* You find a use case for LLMs and build an agent around it
* It works well initially but can't maintain context across sessions
* You spend weeks engineering a RAG solution that seems to help
* Then the cycle begins...
  * Users report the agent forgetting things, contradicting itself, or losing context mid-session
  * You build evals to quantify the problem
  * You re-engineer your entire RAG pipeline with better chunking, embeddings, retrieval strategies
  * The problems shift but don't disappear
  * Repeat

Eventually you realize the issue isn't engineering—-it's that you're not extracting all the latent information from your data. You need to reason exhaustively, handle contradictions, track patterns over time, and maintain coherent state. In other words, you'd need to build Honcho.

Break free from this cycle. Honcho is a general solution to context engineering, memory, and statefulness.

## How Honcho Works

<Note>
  Honcho is a memory system that reasons. Read more on the approach [here](https://blog.plasticlabs.ai/blog/Memory-as-Reasoning).
</Note>

Honcho has four storage primitives that work together:

```mermaid theme={null}
 graph LR
      W[Workspaces] -->|have| P[Peers]
      W -->|have| S[Sessions]

      S -->|have| SM[Messages]

      P <-.->|many-to-many| S

      style W fill:#B6DBFF,stroke:#333,color:#000
      style P fill:#B6DBFF,stroke:#333,color:#000
      style S fill:#B6DBFF,stroke:#333,color:#000
      style SM fill:#B6DBFF,stroke:#333,color:#000
```

* **Workspaces** - Top-level containers that isolate different applications or environments
* **Peers** - Any entity that persists but changes over time (users, agents, objects, and more)
* **Sessions** - Interaction threads between peers with temporal boundaries
* **Messages** - Units of data that trigger reasoning (conversations, events, activity, documents, and more)

When you write messages to Honcho, they're stored and processed in the background. Custom reasoning models perform formal logical [*reasoning*](/docs/v3/documentation/core-concepts/reasoning) to generate conclusions about each peer. These conclusions are stored as [*representations*](/docs/v3/documentation/core-concepts/representation) that you can query to provide rich context for your agents.

<img alt="Honcho Architecture" />

The diagram above shows the flow: agents write messages to Honcho, which triggers reasoning that updates what's stored in representations. Developers (or agents) can then query to get additional context for their next response.

## Why Reasoning?

Traditional RAG systems retrieve what was explicitly said, but they miss what matters most—the insights only accessible by *rigorously thinking* about your data. Without reasoning, you're leaving latent information on the table. Static retrieval can't surface implicit connections, struggles when new information contradicts old data, and fails when you need to make predictions under uncertainty.

Honcho uses formal logic to extract all that latent information. This reasoning is AI-native—it performs the rigorous, compute-intensive thinking that humans struggle with, instantly and consistently. The result is memory that goes beyond simple RAG recall to provide exhaustive context for statefulness.

## Get Started

Honcho gives you maximum control over your agent's context and memory. The data model is flexible and composable, the reasoning backend is powerful yet cost-effective, and everything is built to give developers levers to manage token usage, latency, and reasoning depth.

We're just scratching the surface. Dive into the quickstart to see Honcho in action, explore the architecture to understand how it all fits together, or jump straight to building.

Welcome to Honcho. We're excited to have you at the frontier of AI with us 🫡.

<CardGroup>
  <Card title="Get an API Key" icon="key" href="https://app.honcho.dev">
    Sign up for the Honcho platform and get your API key
  </Card>

  <Card title="Quickstart" icon="rocket" href="/v3/documentation/introduction/quickstart">
    Build your first stateful agent in minutes
  </Card>

  <Card title="Architecture" icon="sitemap" href="/v3/documentation/core-concepts/architecture">
    Deep dive into how Honcho's primitives fit together
  </Card>

  <Card title="Reasoning" icon="gears" href="/v3/documentation/core-concepts/reasoning">
    Learn how Honcho reasons about data to build memory
  </Card>
</CardGroup>


# Quickstart
Source: https://honcho.dev/docs/v3/documentation/introduction/quickstart



Let's get started with Honcho. In this quickstart, you will:

* Set up a workspace with peers (user and assistant)
* Ingest messages from across multiple sessions
* Query the reasoning Honcho produces to get synthesized insights about the user

<Note>
  Running the code below requires an API key. Create and account and get your API key at [app.honcho.dev](https://app.honcho.dev) under "API KEYS".

  Every new tenant gets \$100.00 in free credits on sign up. The code below costs \~\$0.04 to run, so don't worry--still plenty of free credits for iterating.
</Note>

#### 1. Install the SDK

<CodeGroup>
  ```bash Python (uv) theme={null}
  uv add honcho-ai
  ```

  ```bash Python (pip) theme={null}
  pip install honcho-ai
  ```

  ```bash TypeScript (npm) theme={null}
  npm install @honcho-ai/sdk
  ```

  ```bash TypeScript (yarn) theme={null}
  yarn add @honcho-ai/sdk
  ```

  ```bash TypeScript (pnpm) theme={null}
  pnpm add @honcho-ai/sdk
  ```
</CodeGroup>

#### 2. Initialize the Client

The Honcho client is the main entry point for interacting with Honcho's API. It uses a workspace called `default` unless specified, so let's create a `first-honcho-test` workspace for this quickstart.

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  # Initialize client
  honcho = Honcho(workspace_id="first-honcho-test", api_key=HONCHO_API_KEY)

  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from '@honcho-ai/sdk';

  // Initialize client
  const honcho = new Honcho({ workspaceId: "first-honcho-test", apiKey: HONCHO_API_KEY });
  ```
</CodeGroup>

#### 3. Create Peers

<CodeGroup>
  ```python Python theme={null}
  user = honcho.peer("user")
  assistant = honcho.peer("assistant")
  ```

  ```typescript TypeScript theme={null}
  const user = await honcho.peer("user")
  const assistant = await honcho.peer("assistant")
  ```
</CodeGroup>

#### 4. Add Messages to Sessions

We've generated an example conversation dataset with 14 messages across 4 sessions. At a high level, the conversation contains a user chatting with an assistant to get help debugging software infrastructure problems for work *and* jam strategy on a side project they're working on. Spoiler alert--the user is way more interested in their side project.

Create a file called `conversation.json` and add the content in the accordion below. Then we'll loop through the sessions and messages in that file and write them to Honcho.

<Accordion title="Example conversation.json">
  ```json Example Conversation theme={null}
  {
      "sessions": [
        {
          "id": "session_1",
          "messages": [
            {
              "role": "user",
              "content": "containers getting OOM killed in CI after someone on my team updated the base image. quick fix?"
            },
            {
              "role": "assistant",
              "content": "OOM kills after a base image update usually means the new image has higher memory requirements. Quick fix: bump the memory limit in your CI config. If you need to unblock fast, you could also pin back to the previous base image version temporarily."
            }
          ]
        },
        {
          "id": "session_2",
          "messages": [
            {
              "role": "user",
              "content": "hey, been playing with honcho for a side project. do you know if there's a limit on how many users i can have?"
            },
            {
              "role": "assistant",
              "content": "Honcho's free tier is based on context ingested, not number of users - so you can have as many users as you want, you're just limited by how much content you're processing. What are you building?"
            },
            {
              "role": "user",
              "content": "ok so basically it's a personal finance assistant that actually remembers your situation - like it knows you're saving for a house, that you hate subscriptions, that you always regret impulse buys over $50. i've been thinking a lot about the UX, like when should it proactively bring up past context vs wait for you to ask? and how do you balance feeling \"known\" vs feeling surveilled? i have a whole notion doc on this lol"
            },
            {
              "role": "assistant",
              "content": "That's a really thoughtful approach to the personalization problem! The \"known vs surveilled\" tension is exactly right - the best experiences feel like talking to a friend who remembers, not a system that tracks. Proactive context works best when it's in service of the user's stated goals."
            }
          ]
        },
        {
          "id": "session_3",
          "messages": [
            {
              "role": "user",
              "content": "do i need to update docker-compose too or just the CI yaml for that memory thing"
            },
            {
              "role": "assistant",
              "content": "Just the CI yaml for the memory limit - docker-compose is separate and only matters if you're hitting the same OOM issue locally."
            },
            {
              "role": "user",
              "content": "k. oh btw 3 friends are using the finance app now, they keep asking when they can pay me lol. one of them said it's the first budgeting thing that \"gets\" her"
            },
            {
              "role": "assistant",
              "content": "That's awesome - \"when can I pay you\" is the best kind of validation. And that quote about it being the first thing that \"gets\" her is exactly the value prop of personalized memory. Sounds like you're onto something real."
            }
          ]
        },
        {
          "id": "session_4",
          "messages": [
            {
              "role": "user",
              "content": "if i wanted to charge like $5/mo for the finance app, would honcho's pricing still make sense at that price point? trying to figure out unit economics early"
            },
            {
              "role": "assistant",
              "content": "You should be fine at that price point. Unlike other memory frameworks that charge you to access your own data, Honcho only charges for the reasoning layer - ingestion and inference. Storage and retrieval are free. So your unit economics are mostly about how often you're synthesizing insights, not how much history you're keeping."
            },
            {
              "role": "user",
              "content": "ok interesting. wish i had more time to work on this"
            },
            {
              "role": "assistant",
              "content": "Yeah, sounds like you've got something worth making time for. The early traction is real."
            }
          ]
        }
      ]
    }
  ```
</Accordion>

<CodeGroup>
  ```python Python theme={null}
  import json

  # Load conversation data
  with open("conversation.json", "r") as f:
      data = json.load(f)

  # Process each session
  for session_data in data["sessions"]:
      session = honcho.session(session_data["id"])
      session.add_peers([user, assistant])

      # Add messages with correct roles
      messages = []
      for msg in session_data["messages"]:
          if msg["role"] == "user":
              messages.append(user.message(msg["content"]))
          elif msg["role"] == "assistant":
              messages.append(assistant.message(msg["content"]))

      session.add_messages(messages)
  ```

  ```typescript TypeScript theme={null}
  import * as fs from 'fs';

  const data = JSON.parse(fs.readFileSync("conversation.json", "utf-8"));

  for (const sessionData of data.sessions) {
      const session = honcho.session(sessionData.id);
      session.addPeers([user, assistant]);

      const messages = sessionData.messages.map((msg: any) =>
          msg.role === "user" ? user.message(msg.content) : assistant.message(msg.content)
      );

      session.addMessages(messages);
  }
  ```
</CodeGroup>

#### 5. Query for Insights

Now ask Honcho what it's learned--this is where the magic happens:

<CodeGroup>
  ```python Python theme={null}
  response = user.chat("What should I know about this user? 3 sentences max")
  print(response)
  ```

  ```typescript TypeScript theme={null}
  user.chat("What should I know about this user? 3 sentences max").then((response) => {
    console.log(response);
  })
  ```
</CodeGroup>

<Tip>
  Honcho needs a short amount of time to process messages you write to it. There are several utilities to [check the status](/docs/v3/documentation/features/advanced/queue-status) of the queue. Honcho also offers numerous ways to query reasoning to fit latency needs: see the [Get Context](/docs/v3/documentation/features/get-context) page.
</Tip>

The response will look something like this:

> User is a personal finance app developer building a personalized finance assistant that's generating real demand (friends are already asking when they can pay). They're notably thoughtful about product design, carefully considering the UX balance between making users feel "known" versus "surveilled" when their app proactively surfaces remembered context like savings goals and spending regrets. They're business-minded and working through unit economics early, exploring a \$5/month subscription model with usage-based cost structure focused on insight generation frequency rather than data storage—though they wish they had more time to dedicate to the project.

Honcho synthesizes signal by reasoning about the user to draw conclusions beyond what was explicitly stated. It identifies the user as "notably thoughtful about product design", "business-minded" from the discussion of unit economics, and surfaces the signal that they desire to work on the project more.

This is rich personal context for domain-specific agents to do what they want with.

* A life coach agent might see "they wish they had more time to dedicate to the project" and "friends are already asking when they can pay" and ask "have you thought about what it would take to go full-time?"
* A productivity agent might see the same pattern and say "let's protect your weekend time for the finance app."
* A financial advisor agent might see it and ask "what runway would you need to make the leap?"

Honcho acts almost like a detective--it reasons about new and existing evidence in order to form conclusions that can be used to make a *case*. These conclusions wait to be composed dynamically based on how you, the ~~judge~~ developer, query it. This approach is what drives our [pareto-frontier](https://honcho.dev/evals) performance on memory benchmarks, and our custom models allow us to optimize speed and cost.

## Next Steps

You just saw how Honcho reasons about data to build rich peer representations. In this quickstart, you:

* Set up a workspace with peers (user and assistant)
* Ingested messages across multiple sessions
* Queried the reasoning to get synthesized insights about the user

Here's the full working code if you want to run it yourself:

<Accordion title="Full Scripts">
  <CodeGroup>
    ```python Python theme={null}
    # uv sync
    # uv run python test.py

    import json
    import time
    import uuid

    from honcho import Honcho
    from dotenv import load_dotenv

    load_dotenv()

    # Initialize Honcho client with a unique workspace
    workspace_id = f"docs-example-{uuid.uuid4().hex[:8]}"
    honcho = Honcho(environment="production", workspace_id=workspace_id)

    # Create peers to represent the user and assistant
    user = honcho.peer("user")
    assistant = honcho.peer("assistant")

    # Load conversation data from JSON file
    with open("conversation.json", "r") as f:
        conversation_data = json.load(f)

    # Import historical conversation sessions
    for session_data in conversation_data["sessions"]:
        session = honcho.session(session_data["id"])
        session.add_peers([user, assistant])

        # Convert messages to peer messages with correct attribution
        messages = []
        for msg in session_data["messages"]:
            if msg["role"] == "user":
                messages.append(user.message(msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(assistant.message(msg["content"]))

        session.add_messages(messages)

    # Query insights about the user based on conversation history
    response = user.chat("What should I know about this user? 3 sentences max")
    print(response)
    ```

    ```typescript Typescript theme={null}
    // npm install
    // npx ts-node test.ts

    import * as fs from 'fs';
    import { randomUUID } from 'crypto';
    import * as dotenv from 'dotenv';
    import { Honcho } from '@honcho-ai/sdk';

    dotenv.config();

    // Initialize Honcho client with a unique workspace
    const workspaceId = `docs-example-${randomUUID().slice(0, 8)}`;
    const honcho = new Honcho({
      environment: "production",
      workspaceId,
    });

    // Create peers to represent the user and assistant
    const user = await honcho.peer("user");
    const assistant = await honcho.peer("assistant");

    // Load conversation data from JSON file
    const conversationData = JSON.parse(fs.readFileSync("conversation.json", "utf-8"));

    // Import historical conversation sessions
    for (const sessionData of conversationData.sessions) {
      const session = await honcho.session(sessionData.id);
      await session.addPeers([user, assistant]);

      // Convert messages to peer messages with correct attribution
      const messages = [];
      for (const msg of sessionData.messages) {
        if (msg.role === "user") {
          messages.push(user.message(msg.content));
        } else if (msg.role === "assistant") {
          messages.push(assistant.message(msg.content));
        }
      }

      await session.addMessages(messages);
    }


    // Query insights about the user based on conversation history
    const response = await user.chat("What should I know about this user? 3 sentences max");
    console.log(response);

    ```
  </CodeGroup>
</Accordion>

From here, you can explore how to use Honcho's features in your own applications:

<CardGroup>
  <Card title="Get Context" icon="messages" href="/v3/documentation/features/get-context">
    Learn how to fetch the right context for your agent's next response
  </Card>

  <Card title="Architecture" icon="sitemap" href="/v3/documentation/core-concepts/architecture">
    Deep dive into how Honcho's primitives fit together
  </Card>

  <Card title="Chat Endpoint" icon="comments" href="/v3/documentation/features/chat">
    Chat with Honcho about your users
  </Card>

  <Card title="Guides" icon="book" href="/v3/guides/overview">
    Integration patterns and advanced use cases
  </Card>
</CardGroup>


# Agentic Development
Source: https://honcho.dev/docs/v3/documentation/introduction/vibecoding

Agent skills, MCP server, and tools for building with Honcho

## MCP Server

The fastest way to give any AI tool persistent memory is through the Honcho MCP server. It works with any client that supports the Model Context Protocol.

**Get started in 2 minutes:**

1. Get an API key at [app.honcho.dev](https://app.honcho.dev)
2. Add the config for your client below
3. Restart your client

See the [full MCP documentation](/docs/v3/guides/integrations/mcp) for all available tools, advanced configuration, and setup instructions for every supported client.

<CodeGroup>
  ```json Claude Desktop theme={null}
  {
    "mcpServers": {
      "honcho": {
        "command": "npx",
        "args": [
          "mcp-remote",
          "https://mcp.honcho.dev",
          "--header",
          "Authorization:${AUTH_HEADER}",
          "--header",
          "X-Honcho-User-Name:${USER_NAME}"
        ],
        "env": {
          "AUTH_HEADER": "Bearer hch-your-key-here",
          "USER_NAME": "YourName"
        }
      }
    }
  }
  ```

  ```json Cursor theme={null}
  {
    "mcpServers": {
      "honcho": {
        "url": "https://mcp.honcho.dev",
        "headers": {
          "Authorization": "Bearer hch-your-key-here",
          "X-Honcho-User-Name": "YourName"
        }
      }
    }
  }
  ```

  ```bash Claude Code theme={null}
  claude mcp add honcho \
    --transport http \
    --url "https://mcp.honcho.dev" \
    --header "Authorization: Bearer hch-your-key-here" \
    --header "X-Honcho-User-Name: YourName"
  ```
</CodeGroup>

***

## CLI

Inspect and debug a running Honcho deployment from your terminal. The honcho CLI wraps the Python SDK with agent-friendly defaults — JSON output, structured errors, and commands for every primitive (workspaces, peers, sessions, messages, conclusions).

**Get started:**

```bash theme={null}
uv tool install honcho-cli
honcho init      # configure apiKey + environmentUrl
honcho doctor    # verify connectivity
```

The CLI also ships an agent skill. Install it with `npx skills add plastic-labs/honcho` and pick `honcho-cli` from the list.

See the [full CLI reference](/docs/v3/documentation/reference/cli) for all commands, flags, and environment variables.

***

## Claude Code Plugin

Use Honcho to build with Honcho! The [plugin](/docs/v3/guides/integrations/claudecode) provides Claude Code persistent memory that survives context wipes and session restarts.

```bash theme={null}
/plugin marketplace add plastic-labs/claude-honcho
/plugin install honcho@honcho # Tools for Claude to use Honcho to manage its own context
/plugin install honcho-dev@honcho # Skills to teach Claude how to integrate Honcho
```

The marketplace also includes all the agent skills below, so you can use `/honcho-dev:integrate` directly after installing.

See the [full Claude Code integration guide](/docs/v3/guides/integrations/claudecode) for setup details.

***

## OpenCode Plugin

The [OpenCode plugin](/docs/v3/guides/integrations/opencode) gives OpenCode sessions persistent memory that survives context wipes, session restarts, and fresh chats.

```bash theme={null}
bunx @honcho-ai/opencode-honcho install
```

Then run `/honcho:setup` inside OpenCode. See the [full OpenCode integration guide](/docs/v3/guides/integrations/opencode) for setup details.

***

## Agent Skills

We provide agent skills for coding assistants like Claude Code, OpenCode, Cursor, Windsurf, and others.

<CodeGroup>
  ```bash Install via npx (Recommended) theme={null}
  npx skills add plastic-labs/honcho
  ```

  ```bash Install as Claude Skill Manually theme={null}
  curl -o ~/.claude/skills/honcho-integration.md https://raw.githubusercontent.com/plastic-labs/honcho/main/docs/SKILL.md
  ```
</CodeGroup>

### Available Skills

#### honcho-integration

**For new integrations.** This skill helps you add Honcho to an existing Python or TypeScript codebase. It provides a guided, interactive experience:

1. **Explores your codebase** to understand your language, framework, and existing AI/LLM integrations
2. **Interviews you** about which entities should be peers, your preferred integration pattern, and session structure
3. **Implements the integration** based on your answers—installing the SDK, creating peers, configuring sessions, and wiring up the chat endpoint
4. **Verifies the setup** to ensure everything is configured correctly

Invoke with `/honcho-integration` in your coding agent.

#### honcho-cli

**For inspection & debugging.** Teaches your coding agent the right commands and flags for the [honcho CLI](#cli) — peer memory, session context, queue status, dialectic quality.

Invoke implicitly when you ask your agent to inspect a Honcho deployment.

#### migrate-honcho-py / migrate-honcho-ts

**For SDK upgrades.** Migrates code from v1.6.0 to v2.0.0 (required for Honcho 3.0.0+). Use when upgrading the SDK or seeing errors about removed APIs like `observations`, `Representation`, `.core`, or `get_config`.

Both skills handle: terminology changes (`Observation` → `Conclusion`), `Representation` class removal, method renames, and streaming API updates.

| Python                          | TypeScript                 |
| ------------------------------- | -------------------------- |
| `/migrate-honcho-py`            | `/migrate-honcho-ts`       |
| `AsyncHoncho` → `.aio` accessor | `@honcho-ai/core` removal  |
|                                 | `snake_case` → `camelCase` |

***

## Universal Starter Prompt

```
I want to start building with Honcho - an open source memory library for building stateful agents.

## Honcho Resources

**Documentation:**
- Main docs: https://honcho.dev/docs
- API Reference: https://honcho.dev/docs/v3/api-reference/introduction
- Quickstart: https://honcho.dev/docs/v3/documentation/introduction/quickstart
- Architecture: https://honcho.dev/docs/v3/documentation/core-concepts/architecture

**Code & Examples:**
- Core repo: https://github.com/plastic-labs/honcho
- Python SDK: https://github.com/plastic-labs/honcho-python
- TypeScript SDK: https://github.com/plastic-labs/honcho-node
- CLI (inspect & debug a deployment): https://github.com/plastic-labs/honcho/tree/main/honcho-cli
- Discord bot starter: https://github.com/plastic-labs/discord-python-starter
- Telegram bot example: https://github.com/plastic-labs/telegram-python-starter

**What Honcho Does:**
Honcho is an open source memory library with a managed service for building stateful agents. It enables agents to build and maintain state about any entity--users, agents, groups, ideas, and more. Because it's a continual learning system, it understands entities that change over time.

When you write messages to Honcho, they're stored and processed in the background. Custom reasoning models perform formal logical reasoning to generate conclusions about each peer. These conclusions are stored as representations that you can query to provide rich context for your agents.

**Architecture Overview:**
- Core primitives: Workspaces contain Peers (any entity that persists but changes) and Sessions (interaction threads between peers)
- Peers can observe other peers in sessions (configurable with observe_me and observe_others)
- Background reasoning processes messages to extract premises, draw conclusions, and build representations
- Representations enable continuous improvement as new messages refine existing conclusions and scaffold new ones over time
- Chat endpoint provides personalized responses based on learned context
- Supports any LLM (OpenAI, Anthropic, open source)
- Can use managed service or self-host

Please assess the resources above and ask me relevant questions to help build a well-structured application using Honcho. Consider asking about:
- What I'm trying to build
- My technical preferences and stack
- Whether I want to use the managed service or self-host
- My experience level with the technologies involved
- Specific features I need (multi-peer sessions, perspective-taking, streaming, etc.)

Once you understand my needs, help me create a working implementation with proper memory and statefulness.
```


# CLI Reference
Source: https://honcho.dev/docs/v3/documentation/reference/cli

Command-line interface for Honcho — inspect workspaces, peers, sessions, and memory from your terminal

## Install

<CodeGroup>
  ```bash uv (recommended) theme={null}
  uv tool install honcho-cli
  ```

  ```bash uvx (ephemeral) theme={null}
  uvx honcho-cli
  ```
</CodeGroup>

## Quick Start

```bash theme={null}
honcho init        # confirm/set apiKey + Honcho URL in ~/.honcho/config.json
honcho doctor      # verify your config + connectivity
honcho             # show banner + command list
```

## Configuration

The CLI resolves config in this order: **flag → env var → config file → default**.

| Value       | File key         | Env var               | Flag                 | Persisted? |
| ----------- | ---------------- | --------------------- | -------------------- | ---------- |
| API key     | `apiKey`         | `HONCHO_API_KEY`      | —                    | Yes        |
| API URL     | `environmentUrl` | `HONCHO_BASE_URL`     | —                    | Yes        |
| Workspace   | —                | `HONCHO_WORKSPACE_ID` | `-w` / `--workspace` | No         |
| Peer        | —                | `HONCHO_PEER_ID`      | `-p` / `--peer`      | No         |
| Session     | —                | `HONCHO_SESSION_ID`   | `-s` / `--session`   | No         |
| JSON output | —                | `HONCHO_JSON`         | `--json`             | No         |

### Persisted config

The CLI shares `~/.honcho/config.json` with sibling Honcho tools. It owns only
`apiKey` and `environmentUrl` at the top level — everything else (`hosts`,
`sessions`, etc.) is written by other tools and left untouched on save.

```json theme={null}
{
  "apiKey": "hch-v3-...",
  "environmentUrl": "https://api.honcho.dev",
  "hosts": { "claude_code": { "...": "..." } }
}
```

<Info>
  Per-command scoping (workspace / peer / session) is handled via `-w` / `-p` / `-s`
  flags or `HONCHO_*` env vars. **Not** persisted as CLI defaults. This is
  deliberate: every invocation is explicit about what it operates on.
</Info>

### Runtime overrides

Workspace, peer, and session scoping are **per-command only** — pass flags or
`HONCHO_*` env vars on every invocation.

```bash theme={null}
# Per-command flags
honcho peer card -w prod -p user

# Or export once per shell
export HONCHO_WORKSPACE_ID=prod
export HONCHO_PEER_ID=user
honcho peer card

# One-off against a different server
HONCHO_BASE_URL=http://localhost:8000 honcho workspace list

# CI/CD — env vars only, no config file needed
export HONCHO_API_KEY=hch-v3-xxx
export HONCHO_BASE_URL=https://api.honcho.dev
honcho workspace list
```

## Output & exit codes

Every command adapts its output to the context:

* **TTY** — human-readable tables via Rich.
* **Piped or redirected** — JSON automatically (detected via `isatty`).
* **`--json` flag / `HONCHO_JSON=1`** — force JSON regardless of terminal.

Collection commands emit JSON arrays; single-resource commands emit JSON objects. Errors are always structured:

```json theme={null}
{
  "error": {
    "code": "PEER_NOT_FOUND",
    "message": "Peer 'abc' not found in workspace 'my-ws'",
    "details": {"workspace_id": "my-ws", "peer_id": "abc"}
  }
}
```

| Exit code | Meaning                                      |
| --------- | -------------------------------------------- |
| `0`       | Success                                      |
| `1`       | Client error (bad input, resource not found) |
| `2`       | Server error                                 |
| `3`       | Auth error (missing or invalid API key)      |

CI pipelines and agent runtimes can branch on these without parsing stderr.

## Command reference

## honcho conclusion

List, search, create, and delete peer conclusions (Honcho's memory atoms).

<AccordionGroup>
  <Accordion title="create">
    Create a conclusion.

    ```bash theme={null}
    honcho conclusion create <content>
    ```

    <ParamField type="string" />

    <ParamField type="string">
      Observer peer ID.
    </ParamField>

    <ParamField type="string">
      Observed peer ID.
    </ParamField>

    <ParamField type="string">
      Session context. Short alias: `-s`.
    </ParamField>
  </Accordion>

  <Accordion title="delete">
    Delete a conclusion.

    ```bash theme={null}
    honcho conclusion delete <conclusion_id>
    ```

    <ParamField type="string" />

    <ParamField type="string">
      Observer peer ID.
    </ParamField>

    <ParamField type="string">
      Observed peer ID.
    </ParamField>

    <ParamField type="boolean">
      Skip confirmation. Short alias: `-y`.
    </ParamField>
  </Accordion>

  <Accordion title="list">
    List conclusions.

    ```bash theme={null}
    honcho conclusion list
    ```

    <ParamField type="string">
      Observer peer ID.
    </ParamField>

    <ParamField type="string">
      Observed peer ID.
    </ParamField>

    <ParamField type="number">
      Max results.
    </ParamField>
  </Accordion>

  <Accordion title="search">
    Semantic search over conclusions.

    ```bash theme={null}
    honcho conclusion search <query>
    ```

    <ParamField type="string" />

    <ParamField type="string">
      Observer peer ID.
    </ParamField>

    <ParamField type="string">
      Observed peer ID.
    </ParamField>

    <ParamField type="number">
      Max results.
    </ParamField>
  </Accordion>
</AccordionGroup>

## honcho config

Inspect CLI configuration.

```bash theme={null}
honcho config
```

## honcho doctor

Verify config and connectivity. Scope with -w / -p to check workspace, peer, and queue health.

```bash theme={null}
honcho doctor
```

## honcho help

Show help message.

```bash theme={null}
honcho help
```

## honcho init

Set API key and server URL in \~/.honcho/config.json.

Press Enter to keep the current value or type a replacement.
Workspace / peer / session scoping is per-command via -w / -p / -s
or HONCHO\_\* env vars — never persisted.

```bash theme={null}
honcho init
```

<ParamField type="string">
  API key (admin JWT).
</ParamField>

<ParamField type="string">
  Honcho API URL (e.g. [https://api.honcho.dev](https://api.honcho.dev), [http://localhost:8000](http://localhost:8000)).
</ParamField>

## honcho message

List, create, and get messages within a session.

<AccordionGroup>
  <Accordion title="create">
    Create a message in a session.

    ```bash theme={null}
    honcho message create <content>
    ```

    <ParamField type="string" />

    <ParamField type="string">
      Peer ID of the message sender. Short alias: `-p`.
    </ParamField>

    <ParamField type="string">
      JSON metadata to associate with the message.
    </ParamField>

    <ParamField type="string">
      Session ID. Short alias: `-s`.
    </ParamField>
  </Accordion>

  <Accordion title="get">
    Get a single message by ID.

    ```bash theme={null}
    honcho message get <message_id>
    ```

    <ParamField type="string" />

    <ParamField type="string">
      Session ID. Short alias: `-s`.
    </ParamField>
  </Accordion>

  <Accordion title="list">
    List messages in a session. Scoped to a peer with -p.

    ```bash theme={null}
    honcho message list [<session_id>]
    ```

    <ParamField type="string" />

    <ParamField type="number">
      Number of recent messages.
    </ParamField>

    <ParamField type="boolean">
      Show oldest first (default is newest first).
    </ParamField>

    <ParamField type="boolean">
      Show only IDs, peer, token count, and created\_at (no content).
    </ParamField>

    <ParamField type="string">
      Filter by peer ID. Short alias: `-p`.
    </ParamField>
  </Accordion>
</AccordionGroup>

## honcho peer

List, create, chat with, search, and manage peers and their representations.

<AccordionGroup>
  <Accordion title="card">
    Get raw peer card content.

    ```bash theme={null}
    honcho peer card [<peer_id>]
    ```

    <ParamField type="string" />

    <ParamField type="string">
      Target peer for relationship card.
    </ParamField>
  </Accordion>

  <Accordion title="chat">
    Query the dialectic about a peer.

    ```bash theme={null}
    honcho peer chat <query>
    ```

    <ParamField type="string" />

    <ParamField type="string">
      Target peer for perspective.
    </ParamField>

    <ParamField type="string">
      Reasoning level: minimal, low, medium, high, max. Short alias: `-r`.
    </ParamField>
  </Accordion>

  <Accordion title="create">
    Create or get a peer.

    ```bash theme={null}
    honcho peer create <peer_id>
    ```

    <ParamField type="string" />

    <ParamField type="boolean">
      Whether Honcho will form a representation of this peer. Negate with `--no-observe-me`.
    </ParamField>

    <ParamField type="string">
      JSON metadata to associate with the peer.
    </ParamField>
  </Accordion>

  <Accordion title="get-metadata">
    Get metadata for a peer.

    ```bash theme={null}
    honcho peer get-metadata [<peer_id>]
    ```

    <ParamField type="string" />
  </Accordion>

  <Accordion title="inspect">
    Inspect a peer: card, session count, recent conclusions.

    ```bash theme={null}
    honcho peer inspect [<peer_id>]
    ```

    <ParamField type="string" />
  </Accordion>

  <Accordion title="list">
    List all peers in the workspace.

    ```bash theme={null}
    honcho peer list
    ```
  </Accordion>

  <Accordion title="representation">
    Get the formatted representation for a peer.

    ```bash theme={null}
    honcho peer representation [<peer_id>]
    ```

    <ParamField type="string" />

    <ParamField type="string">
      Target peer to get representation about.
    </ParamField>

    <ParamField type="string">
      Semantic search query to filter conclusions.
    </ParamField>

    <ParamField type="number">
      Maximum number of conclusions to include.
    </ParamField>
  </Accordion>

  <Accordion title="search">
    Search a peer's messages.

    ```bash theme={null}
    honcho peer search <query>
    ```

    <ParamField type="string" />

    <ParamField type="number">
      Max results.
    </ParamField>
  </Accordion>

  <Accordion title="set-metadata">
    Set metadata for a peer.

    ```bash theme={null}
    honcho peer set-metadata <metadata>
    ```

    <ParamField type="string" />

    <ParamField type="string">
      Peer ID (uses default if omitted). Short alias: `-p`.
    </ParamField>
  </Accordion>
</AccordionGroup>

## honcho session

List, inspect, create, delete, and manage conversation sessions and their peers.

<AccordionGroup>
  <Accordion title="add-peers">
    Add peers to a session.

    ```bash theme={null}
    honcho session add-peers <session_id> <peer_ids>
    ```

    <ParamField type="string" />

    <ParamField type="string" />
  </Accordion>

  <Accordion title="context">
    Get session context (what an agent would see).

    ```bash theme={null}
    honcho session context [<session_id>]
    ```

    <ParamField type="string" />

    <ParamField type="number">
      Token budget.
    </ParamField>

    <ParamField type="boolean">
      Include summary. Negate with `--no-summary`.
    </ParamField>
  </Accordion>

  <Accordion title="create">
    Create or get a session.

    ```bash theme={null}
    honcho session create <session_id>
    ```

    <ParamField type="string" />

    <ParamField type="string">
      Comma-separated peer IDs to add to the session.
    </ParamField>

    <ParamField type="string">
      JSON metadata to associate with the session.
    </ParamField>
  </Accordion>

  <Accordion title="delete">
    Delete a session and all its data. Destructive — requires --yes or interactive confirm.

    ```bash theme={null}
    honcho session delete [<session_id>]
    ```

    <ParamField type="string" />

    <ParamField type="boolean">
      Skip confirmation. Short alias: `-y`.
    </ParamField>
  </Accordion>

  <Accordion title="get-metadata">
    Get metadata for a session.

    ```bash theme={null}
    honcho session get-metadata [<session_id>]
    ```

    <ParamField type="string" />
  </Accordion>

  <Accordion title="inspect">
    Inspect a session: peers, message count, summaries, config.

    ```bash theme={null}
    honcho session inspect [<session_id>]
    ```

    <ParamField type="string" />
  </Accordion>

  <Accordion title="list">
    List sessions in the workspace.

    ```bash theme={null}
    honcho session list
    ```

    <ParamField type="string">
      Filter by peer. Short alias: `-p`.
    </ParamField>
  </Accordion>

  <Accordion title="peers">
    List peers in a session.

    ```bash theme={null}
    honcho session peers [<session_id>]
    ```

    <ParamField type="string" />
  </Accordion>

  <Accordion title="remove-peers">
    Remove peers from a session.

    ```bash theme={null}
    honcho session remove-peers <session_id> <peer_ids>
    ```

    <ParamField type="string" />

    <ParamField type="string" />
  </Accordion>

  <Accordion title="representation">
    Get the representation of a peer within a session.

    ```bash theme={null}
    honcho session representation <peer_id> [<session_id>]
    ```

    <ParamField type="string" />

    <ParamField type="string" />

    <ParamField type="string">
      Target peer (what peer\_id knows about target).
    </ParamField>

    <ParamField type="string">
      Semantic search query to filter conclusions.
    </ParamField>

    <ParamField type="number">
      Maximum number of conclusions to include.
    </ParamField>
  </Accordion>

  <Accordion title="search">
    Search messages in a session.

    ```bash theme={null}
    honcho session search <query> [<session_id>]
    ```

    <ParamField type="string" />

    <ParamField type="string" />

    <ParamField type="number">
      Max results.
    </ParamField>
  </Accordion>

  <Accordion title="set-metadata">
    Set metadata for a session.

    ```bash theme={null}
    honcho session set-metadata [<session_id>]
    ```

    <ParamField type="string" />

    <ParamField type="string">
      JSON metadata to set (e.g. '\{"key": "value"}'). Short alias: `-d`.
    </ParamField>
  </Accordion>

  <Accordion title="summaries">
    Get session summaries (short + long).

    ```bash theme={null}
    honcho session summaries [<session_id>]
    ```

    <ParamField type="string" />
  </Accordion>
</AccordionGroup>

## honcho workspace

List, create, inspect, delete, and search workspaces.

<AccordionGroup>
  <Accordion title="create">
    Create or get a workspace.

    ```bash theme={null}
    honcho workspace create <workspace_id>
    ```

    <ParamField type="string" />

    <ParamField type="string">
      JSON metadata to associate with the workspace.
    </ParamField>
  </Accordion>

  <Accordion title="delete">
    Delete a workspace. Use --dry-run first to see what will be deleted.

    Requires --yes to skip confirmation, or will prompt interactively.
    If sessions exist, requires --cascade to delete them first.

    ```bash theme={null}
    honcho workspace delete <workspace_id>
    ```

    <ParamField type="string" />

    <ParamField type="boolean">
      Skip confirmation prompt (for scripted/agent use). Short alias: `-y`.
    </ParamField>

    <ParamField type="boolean">
      Delete all sessions before deleting the workspace.
    </ParamField>

    <ParamField type="boolean">
      Show what would be deleted without deleting.
    </ParamField>
  </Accordion>

  <Accordion title="inspect">
    Inspect a workspace: peers, sessions, config.

    ```bash theme={null}
    honcho workspace inspect [<workspace_id>]
    ```

    <ParamField type="string" />
  </Accordion>

  <Accordion title="list">
    List all accessible workspaces.

    ```bash theme={null}
    honcho workspace list
    ```
  </Accordion>

  <Accordion title="queue-status">
    Get queue processing status.

    ```bash theme={null}
    honcho workspace queue-status
    ```

    <ParamField type="string">
      Filter by observer peer.
    </ParamField>

    <ParamField type="string">
      Filter by sender peer.
    </ParamField>
  </Accordion>

  <Accordion title="search">
    Search messages across workspace.

    ```bash theme={null}
    honcho workspace search <query>
    ```

    <ParamField type="string" />

    <ParamField type="number">
      Max results.
    </ParamField>
  </Accordion>
</AccordionGroup>

## Workflows

### Inspect an unfamiliar workspace

When you pick up a workspace and need to orient — start broad, narrow to the peer and session you care about.

<Steps>
  <Step title="Survey the workspace">
    ```bash theme={null}
    honcho workspace inspect --json
    honcho peer list --json
    ```
  </Step>

  <Step title="Inspect a specific peer">
    ```bash theme={null}
    honcho peer inspect <peer_id> --json
    honcho peer card <peer_id> --json
    ```
  </Step>

  <Step title="Review the peer's memory">
    ```bash theme={null}
    honcho conclusion list --observer <peer_id> --json
    honcho conclusion search "topic" --observer <peer_id> --json
    ```
  </Step>

  <Step title="Debug a session">
    ```bash theme={null}
    honcho session inspect <session_id> --json
    honcho message list <session_id> --last 20 --json
    honcho session context <session_id> --json
    honcho session summaries <session_id> --json
    ```
  </Step>
</Steps>

<Tip>
  `honcho session context` shows exactly what an agent would receive at inference time — check it before `honcho peer chat` if a response surprises you.
</Tip>

### A peer isn't learning

If new messages aren't producing new conclusions, work down the diagnostic ladder.

```bash theme={null}
# Is observation enabled for this peer?
honcho peer inspect <peer_id> --json | jq '.configuration'

# Is the deriver actually processing?
honcho workspace queue-status --json

# Do any conclusions exist at all? Any for the expected topic?
honcho conclusion list --observer <peer_id> --json
honcho conclusion search "expected topic" --observer <peer_id> --json
```

### Session context looks wrong

When an agent's responses don't reflect what you expect it to know.

```bash theme={null}
honcho session context <session_id> --json
honcho session summaries <session_id> --json
honcho message list <session_id> --last 50 --json
```

### Dialectic returns bad answers

When `honcho peer chat` or the dialectic API is hallucinating or missing context.

```bash theme={null}
# What does the peer card actually say?
honcho peer card <peer_id> --json

# Any conclusions for this topic?
honcho conclusion search "topic" --observer <peer_id> --json

# Reproduce the query against the CLI
honcho peer chat <peer_id> "what do you know about X?" --json
```

## Scripting & automation

Pipe commands into `jq` for inline transforms, or set `HONCHO_*` env vars for a CI/CD environment with no config file:

```bash theme={null}
# Pipe to jq
honcho peer list --json | jq '.[].id'
honcho workspace inspect --json | jq '.peers'

# Machine-parseable health check — exit code for CI, details for logs
honcho doctor --json

# CI/CD — env vars only, no ~/.honcho/config.json
export HONCHO_API_KEY=hch-v3-xxx
export HONCHO_BASE_URL=https://api.honcho.dev
honcho workspace list
```

Non-interactive onboarding:

```bash theme={null}
# Pre-seed via flags / env vars; init still prompts for anything missing
HONCHO_API_KEY=hch-v3-xxx honcho init --base-url https://api.honcho.dev
```


# The Honcho Dashboard
Source: https://honcho.dev/docs/v3/documentation/reference/platform

Build stateful agents without worrying about infrastructure

<Card title="Sign up to start using Honcho!" icon="rocket" href="https://app.honcho.dev">
  Start using the platform to manage Honcho instances for your workspace or app.
</Card>

The quickest way to begin using Honcho in production is with the
[Honcho Cloud Service](https://app.honcho.dev). Sign up, generate an API key,
and start building with Honcho.

## 1. Go to [app.honcho.dev](https://app.honcho.dev)

Create an account to start using Honcho. If a teammate already uses Honcho, ask
them to invite you to their organization. Otherwise, you'll see a banner
prompting you to create a new one.

<div>
  <Frame>
    <img alt="Honcho Platform Dashboard" />
  </Frame>
</div>

Once you've created an organization, you'll be taken to the dashboard and see
the Welcome page with integration guidance and links to documentation.

<Frame>
  <img alt="Honcho Dashboard Getting Started" />
</Frame>

Each organization has dedicated infrastructure running to isolate your
workloads. Once you add a valid payment method under the
[Billing](https://app.honcho.dev/billing) page, your instance will turn on.

## 2. Activate your Honcho instance

Navigate to the [Billing](https://app.honcho.dev/billing) page to add a payment method. Your Honcho instance provisions automatically, and you can monitor the deployment on the [Instance Status](https://app.honcho.dev/status) page until all systems show a green check mark.

<Frame>
  <img alt="Instance Status Page" />
</Frame>

You can also upgrade Honcho when new versions are made available directly from the status page.

<div>
  <Frame>
    <img alt="Upgrade Honcho" />
  </Frame>
</div>

The **Performance** page provides comprehensive monitoring with usage metrics, health analytics, API response times, and endpoint usage across Honcho.

<Frame>
  <img alt="Performance Analytics Dashboard" />
</Frame>

## 3. Manage API Keys

The [API Keys](https://app.honcho.dev/api-keys) page allows you to create and manage authentication tokens for different environments. You can create admin-level keys with full instance access or scope keys to a specific `Workspace`, `Peer`, or `Session`.

Scoped keys are authorized by their narrowest claim and never widen to the whole workspace:

* A **peer-scoped** key acts on its own peer, plus **read-only** access to the sessions its peer is an active member of (context, summaries, peers, its own per-session config, search, and message reads). It cannot write to those sessions or act on other peers.
* A **session-scoped** key is confined to its own session and cannot reach peer routes.
* Peer- and session-scoped keys **must carry their parent workspace** — creating one without a workspace is rejected.

<Frame>
  <img alt="API Key Management Dashboard" />
</Frame>

## 4. Test with API Playground

The [API Playground](https://app.honcho.dev/playground) provides a Postman-like interface to test queries, explore endpoints, and validate your integration. Authenticate with an API key and send requests directly to your Honcho instance with real-time responses and full request/response logging.

<Frame>
  <img alt="API Playground Interface" />
</Frame>

## 5. Workspaces

The [Explore](https://app.honcho.dev/explore) page provides comprehensive `Workspace` management where you can create workspaces and begin exploring the platform. Each `Workspace` serves as a container for organizing your Honcho data.

<Frame>
  <img alt="Workspace Table" />
</Frame>

Click into any workspace to access a general overview of `Peers` and `Sessions`. Here you can quickly create `Peers`, `Sessions`, and add multiple `Peers` to any `Session`. Edit the metadata and configuration for a `Workspace` with the Edit Config button. Click into any entity to navigate to their respective utilities pages or click the expand icon to view Workspace-wide `Peers` and `Sessions` data tables with more details.

<Frame>
  <img alt="Workspace Dashboard Overview" />
</Frame>

## 6. Peer Dashboard & Utilities

Expand the `Peers` list from the `Workspace` dashboard to see a detailed view of `Peers`.

<Frame>
  <img alt="Peer Dashboard" />
</Frame>

Click into any peer to navigate to their respective utilities page. Next to the `Peer` name you can edit the [Peer Configuration](/docs/v3/documentation/features/advanced/reasoning-configuration), and in the tabs below, explore all utilities for the `Peer`.

<Frame>
  <img alt="Peer Management Dashboard" />
</Frame>

Utilities include:

* **Message search** across all sessions for a `Peer`
* **Chat** to query `Peer` representations with an optional session scope (results vary based on the `Peer`'s configuration)

<Frame>
  <img alt="Chat Endpoint" />
</Frame>

* **Session logs** view which `Sessions` the `Peer` is active
* **Peer configuration and metadata management** including [Session-Peer Configuration](/docs/v3/documentation/features/advanced/reasoning-configuration#session-configuration)

<Frame>
  <img alt="Peer Management Dashboard" />
</Frame>

## 7. Session Dashboard & Utilities

Click into the sessions view within a workspace to see a table of all of your `Sessions` data.

<Frame>
  <img alt="Sessions Table" />
</Frame>

Click into a `Session` to open its utilities page.

<Frame>
  <img alt="Session Utilities" />
</Frame>

Here you can:

* **View and add Messages** within the `Session`; filter messages by `Peer`
* **Advanced search** across `Session` messages
* **Peer management** for adding/removing `Peers` and editing a `Peer`'s Session-level configuration
* **Get Context** to generate LLM-ready context with customizable token limits

<Frame>
  <img alt="Get Context" />
</Frame>

## 8. Webhooks Integration

The [Webhooks](https://app.honcho.dev/webhooks) page enables Webhook creation and management.

<Frame>
  <img alt="Webhooks Dashboard" />
</Frame>

## 9. Organization Member Access

The [Members](https://app.honcho.dev/members) page provides organization administration to manage your team's access to Honcho with the ability to grant admin permissions.

<Frame>
  <img alt="Members Dashboard" />
</Frame>

## Go Further

View the [Architecture](/docs/v3/documentation/core-concepts/architecture) to see how Honcho works under the hood.

Dive into our [API Reference](/docs/v3/api-reference) to explore all available endpoints.

## Next Steps

<CardGroup>
  <Card title="Sign up to Honcho Platform" icon="rocket" href="https://app.honcho.dev">
    Get started with managed Honcho instances
  </Card>

  <Card title="Join our Discord" icon="discord" href="http://discord.gg/honcho">
    Connect with 1000+ developers building with Honcho
  </Card>

  <Card title="Contribute to Honcho" icon="code" href="/v3/contributing/guidelines">
    View our guidelines and explore the codebase
  </Card>

  <Card title="Explore Examples" icon="book" href="/v3/guides">
    See Honcho in action with real examples
  </Card>
</CardGroup>


# SDK Reference
Source: https://honcho.dev/docs/v3/documentation/reference/sdk

Complete SDK documentation and examples for Python and TypeScript

The Honcho SDKs provide ergonomic interfaces for building agentic AI applications with Honcho in Python and TypeScript/JavaScript.

## Installation

<CodeGroup>
  ```bash Python (uv) theme={null}
  uv add honcho-ai
  ```

  ```bash Python (pip) theme={null}
  pip install honcho-ai
  ```

  ```bash TypeScript (npm) theme={null}
  npm install @honcho-ai/sdk
  ```

  ```bash TypeScript (yarn) theme={null}
  yarn add @honcho-ai/sdk
  ```

  ```bash TypeScript (pnpm) theme={null}
  pnpm add @honcho-ai/sdk
  ```
</CodeGroup>

## Quickstart

<Info>
  Without configuration, the SDK defaults to the demo server. For production use:

  1. Get your API key at [app.honcho.dev/api-keys](https://app.honcho.dev/api-keys)
  2. Set `environment="production"` and provide your `api_key`
</Info>

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  # Initialize client (using the default workspace)
  honcho = Honcho()

  # Create peers
  alice = honcho.peer("alice")
  assistant = honcho.peer("assistant")

  # Create a session for conversation
  session = honcho.session("conversation-1")

  # Add messages to conversation
  session.add_messages([
      alice.message("What's the weather like today?"),
      assistant.message("It's sunny and 75°F outside!")
  ])

  # Chat with Honcho about a peer
  response = alice.chat("What did the assistant tell this user about the weather?")

  # Get conversation context for LLM completions
  context = session.context()
  openai_messages = context.to_openai(assistant=assistant)
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from "@honcho-ai/sdk";

  // Initialize client (using the default workspace)
  const honcho = new Honcho({});

  // Create peers
  const alice = await honcho.peer("alice");
  const assistant = await honcho.peer("assistant");

  // Create a session for conversation
  const session = await honcho.session("conversation-1");

  // Add messages to conversation
  await session.addMessages([
    alice.message("What's the weather like today?"),
    assistant.message("It's sunny and 75°F outside!")
  ]);

  // Chat with Honcho about a peer
  const response = await alice.chat("What did the assistant tell this user about the weather?");

  // Get conversation context for LLM completions
  const context = await session.context();
  const openaiMessages = context.toOpenAI(assistant);
  ```
</CodeGroup>

## Core Concepts

### Peers and Representations

<Info>
  **Representations** are how Honcho models what peers know. Each peer has a **global representation** (everything they know across all sessions) and **local representations** (what other specific peers know about them, scoped by session or globally).
</Info>

<CodeGroup>
  ```python Python theme={null}
  # Query alice's global knowledge
  response = alice.chat("What does the user know about weather?")

  # Query what alice knows about the assistant (local representation)
  response = alice.chat("What does the user know about the assistant?", target=assistant)

  # Query scoped to a specific session
  response = alice.chat("What happened in our conversation?", session=session.id)
  ```

  ```typescript TypeScript theme={null}
  // Query alice's global knowledge
  const response = await alice.chat("What does the user know about weather?");

  // Query what alice knows about the assistant (local representation)
  const targetResponse = await alice.chat("What does the user know about the assistant?", {
    target: assistant
  });

  // Query scoped to a specific session
  const sessionResponse = await alice.chat("What happened in our conversation?", {
    sessionId: session.id
  });
  ```
</CodeGroup>

## Core Classes

### Honcho Client

The main entry point for workspace operations:

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  # Basic initialization (uses environment variables)
  honcho = Honcho(workspace_id="my-app-name")

  # Full configuration
  honcho = Honcho(
      workspace_id="my-app-name",
      api_key="my-api-key",
      environment="production",  # or "local", "demo"
      base_url="https://api.honcho.dev",
      timeout=30.0,
      max_retries=3
  )
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from "@honcho-ai/sdk";

  // Basic initialization (uses environment variables)
  const honcho = new Honcho({
    workspaceId: "my-app-name"
  });

  // Full configuration
  const honcho = new Honcho({
    workspaceId: "my-app-name",
    apiKey: "my-api-key",
    environment: "production",  // or "local", "demo"
    baseURL: "https://api.honcho.dev",
    timeout: 30000,
    maxRetries: 3,
    defaultHeaders: { "X-Custom-Header": "value" },
    defaultQuery: { "param": "value" }
  });
  ```
</CodeGroup>

**Environment Variables:**

* `HONCHO_API_KEY` - API key for authentication
* `HONCHO_BASE_URL` - Base URL for the Honcho API
* `HONCHO_WORKSPACE_ID` - Default workspace ID

**Key Methods:**

<CodeGroup>
  ```python Python theme={null}
  # Get or create a peer
  peer = honcho.peer(id)

  # Get or create a session
  session = honcho.session(id)

  # List all peers in workspace
  peers = honcho.peers()

  # List all sessions in workspace
  sessions = honcho.sessions()

  # Search across all content in workspace
  results = honcho.search(query)

  # Workspace metadata management
  metadata = honcho.get_metadata()
  honcho.set_metadata(dict)

  # Get list of all workspace IDs
  workspaces = honcho.workspaces()
  ```

  ```typescript TypeScript theme={null}
  // Get or create a peer
  const peer = await honcho.peer(id);

  // Get or create a session
  const session = await honcho.session(id);

  // List all peers in workspace (returns Page<Peer>)
  const peers = await honcho.peers();

  // List with pagination and filtering
  const filtered = await honcho.peers({
    filters: { metadata: { role: "user" } },
    page: 1,
    size: 25,
    reverse: true
  });

  // List all sessions in workspace (returns Page<Session>)
  const sessions = await honcho.sessions();

  // Search across all content in workspace (returns Page<any>)
  const results = await honcho.search(query);

  // Workspace metadata management
  const metadata = await honcho.getMetadata();
  await honcho.setMetadata(metadata);

  // Get list of all workspace IDs
  const workspaces = await honcho.workspaces();
  ```
</CodeGroup>

<Info>
  `peer()` and `session()` always make a get-or-create API call, returning objects with cached metadata, configuration, and timestamps.
</Info>

### Peer

Represents an entity that can participate in conversations:

<CodeGroup>
  ```python Python theme={null}
  # Create peers (get-or-create API call)
  alice = honcho.peer("alice")
  assistant = honcho.peer("assistant")

  # Create with immediate configuration
  # This will make an API call to create the peer with the custom configuration and/or metadata
  alice = honcho.peer("bob", config={"role": "user", "active": True}, metadata={"location": "NYC", "role": "developer"})

  # Peer properties
  print(f"Peer ID: {alice.id}")
  print(f"Workspace: {alice.workspace_id}")
  print(f"Created: {alice.created_at}")  # Available after API fetch

  # Chat with peer's representations (supports streaming)
  response = alice.chat("What did I have for breakfast?")
  response = alice.chat("What do I know about Bob?", target="bob")
  response = alice.chat("What happened in session-1?", session="session-1")
  response = alice.chat("Summarize what matters most to me.", reasoning_level="high")

  # Add content to a session with a peer
  session = honcho.session("session-1")
  session.add_messages([
    alice.message("I love Python programming"),
    alice.message("Today I learned about async programming"),
    alice.message("I prefer functional programming patterns")
  ])

  # Get peer's sessions
  sessions = alice.sessions()

  # Search peer's messages
  results = alice.search("programming")

  # Metadata management
  metadata = alice.get_metadata()
  metadata["location"] = "Paris"
  alice.set_metadata(metadata)

  # Peer card management
  card = alice.get_card()                          # Get peer card
  card = alice.get_card(target="bob")              # Get card about another peer
  updated = alice.set_card(["Likes Python", "Lives in NYC"])  # Set peer card
  updated = alice.set_card(["Works at Acme"], target="bob")   # Set card about another peer

  # Get peer context (representation + peer card in one call)
  context = alice.context()
  context = alice.context(target="bob")  # What alice knows about bob

  # Get working representation with semantic search
  rep = alice.representation(search_query="preferences", search_top_k=10)

  # Access conclusions
  self_conclusions = alice.conclusions.list()  # Self-conclusions
  bob_conclusions = alice.conclusions_of("bob").list()  # Conclusions of bob
  ```

  ```typescript TypeScript theme={null}
  // Create peers (returns Promise<Peer>)
  const alice = await honcho.peer("alice");
  const assistant = await honcho.peer("assistant");

  // Peer properties
  console.log(`Peer ID: ${alice.id}`);
  console.log(`Created: ${alice.createdAt}`);  // Available after API fetch

  // Chat with peer's representations (supports streaming)
  const response = await alice.chat("What did I have for breakfast?");
  const targetResponse = await alice.chat("What do I know about Bob?", { target: "bob" });
  const sessionResponse = await alice.chat("What happened in session-1?", {
    sessionId: "session-1"
  });
  const deeperResponse = await alice.chat("Summarize what matters most to me.", {
    reasoningLevel: "high"
  });

  // Chat with streaming support
  const streamResponse = await alice.chat("Tell me a story", { stream: true });

  // Add content to a session with a peer
  const session = await honcho.session("session-1");
  await session.addMessages([
    alice.message("I love TypeScript programming"),
    alice.message("Today I learned about async programming"),
    alice.message("I prefer functional programming patterns")
  ]);

  // Get peer's sessions
  const sessions = await alice.sessions();

  // Search peer's messages
  const results = await alice.search("programming");

  // Metadata management
  const metadata = await alice.getMetadata();
  await alice.setMetadata({
    ...metadata,
    location: "Paris"
  });

  // Peer card management
  const card = await alice.getCard();                              // Get peer card
  const targetCard = await alice.getCard("bob");                   // Get card about another peer
  const updated = await alice.setCard(["Likes TypeScript", "Lives in NYC"]);  // Set peer card
  const updatedTarget = await alice.setCard(["Works at Acme"], "bob");        // Set card about another peer

  // Get peer context (representation + peer card in one call)
  const context = await alice.context();
  const targetContext = await alice.context({ target: "bob" });  // What alice knows about bob

  // Get working representation with semantic search
  const rep = await alice.representation({
    searchQuery: "preferences",
    searchTopK: 10
  });

  // Access conclusions
  const selfConclusions = await alice.conclusions.list();  // Self-conclusions
  const bobConclusions = await alice.conclusionsOf("bob").list();  // Conclusions of bob
  ```
</CodeGroup>

### Peer Context

The `context()` method on peers retrieves both the working representation and peer card in a single API call:

<CodeGroup>
  ```python Python theme={null}
  # Get peer's own context
  context = alice.context()
  print(context.representation)  # Working representation
  print(context.peer_card)       # Peer card as list of strings

  # Get context about another peer (what alice knows about bob)
  bob_context = alice.context(target="bob")

  # Get context with semantic search
  context = alice.context(
      target="bob",
      search_query="work preferences",
      search_top_k=10,
      search_max_distance=0.8,
      include_most_frequent=True,
      max_conclusions=50
  )
  ```

  ```typescript TypeScript theme={null}
  // Get peer's own context
  const context = await alice.context();
  console.log(context.representation);  // Working representation
  console.log(context.peerCard);        // Peer card as array of strings

  // Get context about another peer (what alice knows about bob)
  const bobContext = await alice.context({ target: "bob" });

  // Get context with semantic search
  const searchedContext = await alice.context({
    target: "bob",
    searchQuery: "work preferences",
    searchTopK: 10,
    searchMaxDistance: 0.8,
    includeMostFrequent: true,
    maxConclusions: 50
  });
  ```
</CodeGroup>

### Peer Card

The peer card contains stable biographical facts about a peer (name, preferences, background). Use `get_card()` / `getCard()` to retrieve it and `set_card()` / `setCard()` to overwrite it:

<CodeGroup>
  ```python Python theme={null}
  # Get peer's own card
  card = alice.get_card()
  print(card)  # ["Likes Python", "Lives in NYC", ...]

  # Get card about another peer (local representation)
  bob_card = alice.get_card(target="bob")

  # Set peer's own card
  updated = alice.set_card(["Likes Python", "Lives in NYC"])

  # Set card about another peer
  updated = alice.set_card(["Works at Acme", "Enjoys hiking"], target="bob")
  ```

  ```typescript TypeScript theme={null}
  // Get peer's own card
  const card = await alice.getCard();
  console.log(card);  // ["Likes TypeScript", "Lives in NYC", ...]

  // Get card about another peer (local representation)
  const bobCard = await alice.getCard("bob");

  // Set peer's own card
  const updated = await alice.setCard(["Likes TypeScript", "Lives in NYC"]);

  // Set card about another peer
  const updatedBob = await alice.setCard(["Works at Acme", "Enjoys hiking"], "bob");
  ```
</CodeGroup>

<Info>
  Peer cards are automatically maintained by the dreaming agent during message processing. Use `set_card()` / `setCard()` when you need to manually override or seed the card — the peer will be created automatically if it doesn't already exist.
</Info>

### Conclusions

Peers can access their conclusions (facts derived from messages) through the `conclusions` property and `conclusions_of()` method:

<CodeGroup>
  ```python Python theme={null}
  # Access self-conclusions (what honcho knows about alice)
  self_conclusions = alice.conclusions

  # List self-conclusions
  conclusions_list = self_conclusions.list()

  # Search self-conclusions semantically
  results = self_conclusions.query("food preferences")

  # Delete a conclusion
  self_conclusions.delete("conclusion-id")

  # Access conclusions of another peer (what alice knows about bob)
  bob_conclusions = alice.conclusions_of("bob")
  bob_conclusions_list = bob_conclusions.list()
  bob_search = bob_conclusions.query("work history")
  ```

  ```typescript TypeScript theme={null}
  // Access self-conclusions (what honcho knows about alice)
  const selfConclusions = alice.conclusions;

  // List self-conclusions
  const conclusionsList = await selfConclusions.list();

  // Search self-conclusions semantically
  const results = await selfConclusions.query("food preferences");

  // Delete a conclusion
  await selfConclusions.delete("conclusion-id");

  // Access conclusions of another peer (what alice knows about bob)
  const bobConclusions = alice.conclusionsOf("bob");
  const bobConclusionsList = await bobConclusions.list();
  const bobSearch = await bobConclusions.query("work history");
  ```
</CodeGroup>

#### Creating Conclusions Manually

You can also create conclusions directly, which is useful for importing data or adding explicit facts:

<CodeGroup>
  ```python Python theme={null}
  # Create conclusions for what alice knows about bob
  bob_conclusions = alice.conclusions_of("bob")

  # Create a single conclusion
  created = bob_conclusions.create([
      {"content": "User prefers dark mode", "session_id": "session-1"}
  ])

  # Create multiple conclusions in batch
  created = bob_conclusions.create([
      {"content": "User prefers dark mode", "session_id": "session-1"},
      {"content": "User works late at night", "session_id": "session-1"},
      {"content": "User enjoys programming", "session_id": "session-1"},
  ])

  # Returns list of created Conclusion objects with IDs
  for conclusion in created:
      print(f"Created conclusion: {conclusion.id} - {conclusion.content}")
  ```

  ```typescript TypeScript theme={null}
  // Create conclusions for what alice knows about bob
  const bobConclusions = alice.conclusionsOf("bob");

  // Create a single conclusion
  const created = await bobConclusions.create([
      { content: "User prefers dark mode", sessionId: "session-1" }
  ]);

  // Create multiple conclusions in batch
  const batchCreated = await bobConclusions.create([
      { content: "User prefers dark mode", sessionId: "session-1" },
      { content: "User works late at night", sessionId: "session-1" },
      { content: "User enjoys programming", sessionId: "session-1" },
  ]);

  // Returns array of created Conclusion objects with IDs
  for (const conclusion of batchCreated) {
      console.log(`Created conclusion: ${conclusion.id} - ${conclusion.content}`);
  }
  ```
</CodeGroup>

<Info>
  Manually created conclusions are marked as "explicit" and are treated the same as system-derived conclusions. Each conclusion must be tied to a session and the content length is validated against the embedding token limit.
</Info>

### Session

Manages multi-party conversations:

<CodeGroup>
  ```python Python theme={null}
  # Create session (get-or-create API call)
  session = honcho.session("conversation-1")

  # Create with immediate configuration
  # This will make an API call to create the session with the custom configuration and/or metadata
  session = honcho.session("meeting-1", config={"type": "meeting", "max_peers": 10})

  # Session properties
  print(f"Session ID: {session.id}")
  print(f"Workspace: {session.workspace_id}")
  print(f"Created: {session.created_at}")  # Available after API fetch
  print(f"Active: {session.is_active}")    # Available after API fetch

  # Peer management
  session.add_peers([alice, assistant])
  session.add_peers([(alice, SessionPeerConfig(observe_others=True))])
  session.set_peers([alice, bob, charlie])  # Replace all peers
  session.remove_peers([alice])

  # Get session peers and their configurations
  peers = session.peers()
  peer_config = session.get_peer_configuration(alice)
  session.set_peer_configuration(alice, SessionPeerConfig(observe_me=False))

  # Message management
  session.add_messages([
      alice.message("Hello everyone!"),
      assistant.message("Hi Alice! How can I help today?")
  ])

  # Get messages (with optional pagination)
  messages = session.messages()
  messages = session.messages(page=1, size=100, reverse=True)

  # Get a single message by ID
  message = session.get_message("message-id")

  # Get conversation context
  context = session.context(summary=True, tokens=2000)

  # Get context with peer representation included
  context = session.context(
      tokens=2000,
      peer_target="user",
      peer_perspective="assistant",
      search_query="What are my preferences?",
      limit_to_session=True,
      search_top_k=10,
      search_max_distance=0.8,
      include_most_frequent=True,
      max_conclusions=25
  )

  # Search session content
  results = session.search("help")

  # Working representation queries with semantic search
  global_rep = session.representation("alice")
  targeted_rep = session.representation(alice, target=bob)
  searched_rep = session.representation(
      "alice",
      search_query="preferences",
      search_top_k=10,
      include_most_frequent=True
  )

  # Upload a file to create messages
  messages = session.upload_file(
      file=open("document.pdf", "rb"),
      peer="user",
      metadata={"source": "upload"},
      created_at="2024-01-15T10:30:00Z"
  )

  # Clone a session (creates a copy with all data)
  # Copies: messages, metadata, configuration, peers, and peer configurations
  cloned = session.clone()

  # Clone up to a specific message (inclusive)
  # Only messages up to and including the specified message are copied
  cloned_partial = session.clone(message_id="msg-123")

  # Delete session (async - returns 202)
  session.delete()

  # Metadata management
  session.set_metadata({"topic": "product planning", "status": "active"})
  metadata = session.get_metadata()
  ```

  ```typescript TypeScript theme={null}
  // Create session (returns Promise<Session>)
  const session = await honcho.session("conversation-1");

  // Session properties
  console.log(`Session ID: ${session.id}`);
  console.log(`Created: ${session.createdAt}`);  // Available after API fetch
  console.log(`Active: ${session.isActive}`);    // Available after API fetch

  // Peer management
  await session.addPeers([alice, assistant]);
  await session.addPeers("single-peer-id");
  await session.setPeers([alice, bob, charlie]);  // Replace all peers
  await session.removePeers([alice]);
  await session.removePeers("single-peer-id");

  // Get session peers
  const peers = await session.peers();

  // Message management
  await session.addMessages([
    alice.message("Hello everyone!"),
    assistant.message("Hi Alice! How can I help today?")
  ]);

  // Get messages (with optional pagination)
  const messages = await session.messages();
  const paged = await session.messages({ page: 1, size: 100, reverse: true });

  // Get a single message by ID
  const message = await session.getMessage("message-id");

  // Get conversation context
  const context = await session.context({ summary: true, tokens: 2000 });

  // Get context with peer representation included
  const richContext = await session.context({
    tokens: 2000,
    peerTarget: "user",
    peerPerspective: "assistant",
    limitToSession: true,
    representationOptions: {
      searchQuery: "What are my preferences?",
      searchTopK: 10,
      searchMaxDistance: 0.8,
      includeMostFrequent: true,
      maxConclusions: 25
    }
  });

  // Search session content
  const results = await session.search("help");

  // Working representation queries with semantic search
  const globalRep = await session.representation("alice");
  const targetedRep = await session.representation(alice, { target: bob });
  const searchedRep = await session.representation("alice", {
    searchQuery: "preferences",
    searchTopK: 10,
    includeMostFrequent: true
  });

  // Upload a file to create messages
  const messages = await session.uploadFile(
    fileBuffer,
    "user",
    {
      metadata: { source: "upload" },
      createdAt: "2024-01-15T10:30:00Z"
    }
  );

  // Clone a session (creates a copy with all data)
  // Copies: messages, metadata, configuration, peers, and peer configurations
  const cloned = await session.clone();

  // Clone up to a specific message (inclusive)
  // Only messages up to and including the specified message are copied
  const clonedPartial = await session.clone("msg-123");

  // Delete session (async - returns 202)
  await session.delete();

  // Metadata management
  await session.setMetadata({
    topic: "product planning",
    status: "active"
  });
  const metadata = await session.getMetadata();
  ```
</CodeGroup>

**Session-Level Theory of Mind Configuration:**

<Info>
  **Theory of Mind** controls whether peers can form models of what other peers think. Use `observe_others=False` to prevent a peer from modeling others within a session, and `observe_me=False` to prevent others from modeling this peer within a session.
</Info>

<CodeGroup>
  ```python Python theme={null}
  from honcho.api_types import SessionPeerConfig

  # Configure peer observation settings
  config = SessionPeerConfig(
      observe_others=False,  # Form theory-of-mind of other peers -- False by default
      observe_me=True        # Don't let others form theory-of-mind of me -- True by default
  )

  session.add_peers([(alice, config)])
  ```

  ```typescript TypeScript theme={null}
  // Configure peer observation settings
  const config = new SessionPeerConfig({
      observeOthers: false,  // Form theory-of-mind of other peers -- False by default
      observeMe: true        // Don't let others form theory-of-mind of me -- True by default
  });

  await session.addPeers([alice, config]);
  ```
</CodeGroup>

### SessionContext

Provides formatted conversation context for LLM integration:

<CodeGroup>
  ```python Python theme={null}
  # Get session context
  context = session.context(summary=True, tokens=1500)

  # Convert to LLM-friendly formats
  openai_messages = context.to_openai(assistant=assistant)
  anthropic_messages = context.to_anthropic(assistant=assistant)
  ```

  ```typescript TypeScript theme={null}
  // Get session context
  const context = await session.context({ summary: true, tokens: 1500 });

  // Convert to LLM-friendly formats
  const openaiMessages = context.toOpenAI(assistant);
  const anthropicMessages = context.toAnthropic(assistant);
  ```
</CodeGroup>

The SessionContext object has the following structure:

```json theme={null}
{
  "id": "string",
  "messages": [
    {
      "id": "string",
      "content": "string",
      "peer_id": "string",
      "session_id": "string",
      "workspace_id": "string",
      "metadata": {},
      "created_at": "2024-01-15T10:30:00Z",
      "token_count": 42
    }
  ],
  "summary": {
    "content": "string",
    "message_id": 123,
    "summary_type": "short|long",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "peer_representation": "string (optional)",
  "peer_card": ["string"] // optional, included when peer_target is provided
}
```

**Session Context Parameters:**

| Parameter                                   | Type               | Description                                        |
| ------------------------------------------- | ------------------ | -------------------------------------------------- |
| `summary`                                   | `bool`             | Whether to include summary (default: true)         |
| `tokens`                                    | `int`              | Maximum tokens to include                          |
| `peer_target`                               | `str`              | Peer ID to get representation for                  |
| `peer_perspective`                          | `str`              | Peer ID for perspective (requires peer\_target)    |
| `limit_to_session`                          | `bool`             | Limit representation to session only               |
| `representationOptions.searchQuery`         | `str` or `Message` | Query string or Message object for semantic search |
| `representationOptions.searchTopK`          | `int`              | Number of semantic search results (1-100)          |
| `representationOptions.searchMaxDistance`   | `float`            | Max semantic distance (0.0-1.0)                    |
| `representationOptions.includeMostFrequent` | `bool`             | Include most frequent conclusions                  |
| `representationOptions.maxConclusions`      | `int`              | Max conclusions to include (1-100)                 |

## Advanced Usage

### Multi-Party Conversations

<CodeGroup>
  ```python Python theme={null}
  # Create multiple peers
  users = [honcho.peer(f"user-{i}") for i in range(5)]
  moderator = honcho.peer("moderator")

  # Create group session
  group_chat = honcho.session("group-discussion")
  group_chat.add_peers(users + [moderator])

  # Add messages from different peers
  group_chat.add_messages([
      users[0].message("What's our agenda for today?"),
      moderator.message("We'll discuss the new feature roadmap"),
      users[1].message("I have some concerns about the timeline")
  ])

  # Query different perspectives
  user_perspective = users[0].chat("What are people's concerns?")
  moderator_view = moderator.chat("What feedback am I getting?", session=group_chat.id)
  ```

  ```typescript TypeScript theme={null}
  // Create multiple peers
  const users = await Promise.all(
    Array.from({ length: 5 }, (_, i) => honcho.peer(`user-${i}`))
  );
  const moderator = await honcho.peer("moderator");

  // Create group session
  const groupChat = await honcho.session("group-discussion");
  await groupChat.addPeers([...users, moderator]);

  // Add messages from different peers
  await groupChat.addMessages([
    users[0].message("What's our agenda for today?"),
    moderator.message("We'll discuss the new feature roadmap"),
    users[1].message("I have some concerns about the timeline")
  ]);

  // Query different perspectives
  const userPerspective = await users[0].chat("What are people's concerns?");
  const moderatorView = await moderator.chat("What feedback am I getting?", {
    sessionId: groupChat.id
  });
  ```
</CodeGroup>

### LLM Integration

<CodeGroup>
  ```python Python theme={null}
  import openai

  # Get conversation context
  context = session.context(tokens=3000)
  messages = context.to_openai(assistant=assistant)

  # Call OpenAI API
  response = openai.chat.completions.create(
      model="gpt-4",
      messages=messages + [
          {"role": "user", "content": "Summarize the key discussion points."}
      ]
  )
  ```

  ```typescript TypeScript theme={null}
  import OpenAI from 'openai';

  const openai = new OpenAI();

  // Get conversation context
  const context = await session.context({ tokens: 3000 });
  const messages = context.toOpenAI(assistant);

  // Call OpenAI API
  const response = await openai.chat.completions.create({
    model: "gpt-4",
    messages: [
      ...messages,
      { role: "user", content: "Summarize the key discussion points." }
    ]
  });
  ```
</CodeGroup>

### Custom Message Timestamps

When creating messages, you can optionally specify a custom `created_at` timestamp instead of using the server's current time:

```bash theme={null}
curl -X POST "https://api.honcho.dev/v3/workspaces/{workspace_id}/sessions/{session_id}/messages" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "peer_id": "user123",
        "content": "This message happened yesterday",
        "created_at": "2024-01-01T12:00:00Z",
        "metadata": {"source": "historical_data"}
      }
    ]
  }'
```

This is useful for:

* Importing historical conversation data
* Backfilling messages from other systems
* Maintaining accurate timeline ordering when processing batch data

If `created_at` is not provided, messages will use the server's current timestamp.

### Metadata and Filtering

See [Using Filters](/docs/v3/documentation/features/advanced/using-filters) for more examples on how to use filters.

<CodeGroup>
  ```python Python theme={null}
  # Add messages with metadata
  session.add_messages([
      alice.message("Let's discuss the budget", metadata={
          "topic": "finance",
          "priority": "high"
      }),
      assistant.message("I'll prepare the financial report", metadata={
          "action_item": True,
          "due_date": "2024-01-15"
      })
  ])

  # Filter messages by metadata
  finance_messages = session.messages(filters={"metadata": {"topic": "finance"}})
  action_items = session.messages(filters={"metadata": {"action_item": True}})
  ```

  ```typescript TypeScript theme={null}
  // Add messages with metadata
  await session.addMessages([
    alice.message("Let's discuss the budget", {
      metadata: {
        topic: "finance",
        priority: "high"
      }
    }),
    assistant.message("I'll prepare the financial report", {
      metadata: {
        action_item: true,
        due_date: "2024-01-15"
      }
    })
  ]);

  // Filter messages by metadata
  const financeMessages = await session.messages({
    filters: { metadata: { topic: "finance" } }
  });
  const actionItems = await session.messages({
    filters: { metadata: { action_item: true } }
  });
  ```
</CodeGroup>

### Pagination

All list methods support `page`, `size`, and `reverse` parameters:

<CodeGroup>
  ```python Python theme={null}
  # Default pagination (page 1, size 50)
  for session in honcho.sessions():
      print(f"Session: {session.id}")

  # Custom page size
  for message in session.messages(size=100):
      print(f"  {message.peer_id}: {message.content}")

  # Start at a specific page
  page3 = session.messages(page=3, size=25)

  # Reverse ordering
  recent_first = session.messages(reverse=True)

  # Combine with filters
  filtered = session.messages(filters={"peer_id": "alice"}, size=10)
  ```

  ```typescript TypeScript theme={null}
  // Default pagination (page 1, size 50)
  const peersPage = await honcho.peers();

  // Custom page size and filtering
  const filtered = await honcho.peers({
    filters: { metadata: { role: "user" } },
    size: 25
  });

  // Start at a specific page
  const page3 = await session.messages({ page: 3, size: 25 });

  // Reverse ordering
  const recent = await session.messages({ reverse: true });

  // Iterate through all items (auto-paginates)
  for await (const peer of await honcho.peers()) {
    console.log(`Peer: ${peer.id}`);
  }

  // Manual pagination
  let currentPage = peersPage;
  while (currentPage) {
    const data = await currentPage.data();
    console.log(`Processing ${data.length} items`);
    currentPage = await currentPage.nextPage();
  }
  ```
</CodeGroup>

## Best Practices

### Resource Management

<CodeGroup>
  ```python Python theme={null}
  # Peers and sessions are lightweight - create as needed
  alice = honcho.peer("alice")
  session = honcho.session("chat-1")

  # Use descriptive IDs for better debugging
  user_session = honcho.session(f"user-{user_id}-support-{ticket_id}")
  support_agent = honcho.peer(f"agent-{agent_id}")
  ```

  ```typescript TypeScript theme={null}
  // Peers and sessions are lightweight - create as needed
  const alice = await honcho.peer("alice");
  const session = await honcho.session("chat-1");

  // Use descriptive IDs for better debugging
  const userSession = await honcho.session(`user-${userId}-support-${ticketId}`);
  const supportAgent = await honcho.peer(`agent-${agentId}`);
  ```
</CodeGroup>

### Performance Optimization

<CodeGroup>
  ```python Python theme={null}
  # Create peers (each makes a get-or-create call)
  peers = [honcho.peer(f"user-{i}") for i in range(100)]

  # Batch operations when possible
  session.add_messages([peer.message(f"Message {i}") for i, peer in enumerate(peers)])

  # Use context limits to control token usage
  context = session.context(tokens=1500)  # Limit context size
  ```

  ```typescript TypeScript theme={null}
  // Create peers (each makes a get-or-create call)
  const peers = await Promise.all(
    Array.from({ length: 100 }, (_, i) => honcho.peer(`user-${i}`))
  );

  // Batch operations when possible
  await session.addMessages(
    peers.map((peer, i) => peer.message(`Message ${i}`))
  );

  // Use context limits to control token usage
  const context = await session.context({ tokens: 1500 }); // Limit context size

  // Iterate efficiently with async iteration
  for await (const peer of await honcho.peers()) {
    // Process one peer at a time without loading all into memory
  }
  ```
</CodeGroup>


# Agent Zero
Source: https://honcho.dev/docs/v3/guides/community/agent0

Add AI-native memory to Agent Zero

[Agent Zero](https://github.com/agent0ai/agent-zero) is a general AI agent framework with a plugin-first architecture. The Honcho plugin gives Agent Zero persistent memory across chat sessions — users are remembered with their preferences, context, and behavioral patterns, even after sessions end and new ones begin.

## Getting Started

The Honcho plugin is a community integration. See the [plugin README](https://github.com/alogotron/a0-plugin-honcho) for full installation and configuration instructions.

The integration requires:

1. A Honcho API key from [app.honcho.dev](https://app.honcho.dev)
2. Cloning the plugin into your Agent Zero plugins directory
3. Enabling it via **Settings > Plugins** in Agent Zero's UI

## How It Works

The plugin hooks into Agent Zero's extension system. It syncs user and assistant messages to Honcho after every turn, prefetches user context into the system prompt on each new turn, and maintains separate peer models for the user and agent. If Honcho is unavailable, the agent continues normally.

## Next Steps

<CardGroup>
  <Card title="Plugin Repository" icon="github" href="https://github.com/alogotron/a0-plugin-honcho">
    Source code, installation, and full documentation.
  </Card>

  <Card title="Honcho Architecture" icon="sitemap" href="../../documentation/core-concepts/architecture">
    Learn about peers, sessions, and dialectic reasoning.
  </Card>
</CardGroup>


# Pi
Source: https://honcho.dev/docs/v3/guides/community/pi-honcho-memory

Persistent memory extension for the pi coding agent

[pi-honcho-memory](https://github.com/agneym/pi-honcho-memory) is a persistent memory extension for [pi](https://pi.dev), a coding agent CLI. It gives pi long-term memory across sessions — user preferences, project context, and past decisions are remembered and automatically injected into the system prompt.

## Getting Started

Install the extension inside pi:

```bash theme={null}
pi install npm:@agney/pi-honcho-memory
```

The integration requires:

1. A Honcho API key from [app.honcho.dev](https://app.honcho.dev)
2. Running `/honcho-setup` inside pi for interactive configuration, or setting `HONCHO_API_KEY` in your environment

The Honcho plugin is a community integration. See the [plugin README](https://github.com/agneym/pi-honcho-memory/blob/main/README.md) for full installation and configuration instructions.

## How It Works

The extension hooks into pi's extension system. It automatically syncs user and assistant messages to Honcho after each agent response, injects cached user profile and project context into the system prompt with zero network latency, and exposes LLM tools (`honcho_search`, `honcho_chat`, `honcho_remember`) for active memory operations. Session scoping is configurable — memory can be shared per repo, per git branch, or per directory. If Honcho is unavailable, pi continues working normally.

## Next Steps

<CardGroup>
  <Card title="Extension Repository" icon="github" href="https://github.com/agneym/pi-honcho-memory">
    Source code, installation, and full documentation.
  </Card>

  <Card title="Honcho Architecture" icon="sitemap" href="../../documentation/core-concepts/architecture">
    Learn about peers, sessions, and dialectic reasoning.
  </Card>
</CardGroup>


# Discord Bots with Honcho
Source: https://honcho.dev/docs/v3/guides/discord

Use Honcho to build a Discord bot with conversational memory and context management.

> Example code is available on [GitHub](https://github.com/plastic-labs/discord-python-starter)

Any application interface that defines logic based on events and supports
special commands can work easily with Honcho. Here's how to use Honcho with
**Discord** as an interface. If you're not familiar with Discord bot
application logic, the [py-cord](https://pycord.dev/) docs would be a good
place to start.

## Events

Most Discord bots have async functions that listen for specific events, the most common one being messages. We can use Honcho to store messages by user and session based on an interface's event logic. Take the following function definition for example:

```python theme={null}
@bot.event
async def on_message(message):
    """
    Receive a message from Discord and respond with a message from our LLM assistant.
    """
    if not validate_message(message):
        return

    input = sanitize_message(message)

    # If the message is empty after sanitizing, ignore it
    if not input:
        return

    peer = honcho_client.peer(id=get_peer_id_from_discord(message))
    session = honcho_client.session(id=str(message.channel.id))

    async with message.channel.typing():
        response = llm(session, input)

    await send_discord_message(message, response)

    # Save both the user's message and the bot's response to the session
    session.add_messages(
        [
            peer.message(input),
            assistant.message(response),
        ]
    )
```

Let's break down what this code is doing...

```python theme={null}
@bot.event
async def on_message(message):
    if not validate_message(message):
        return
```

This is how you define an event function in `py-cord` that listens for messages. We use a helper function `validate_message()` to check if the message should be processed.

## Helper Functions

The code uses several helper functions to keep the main logic clean and readable. Let's examine each one:

### Message Validation

```python theme={null}
def validate_message(message) -> bool:
    """
    Determine if the message is valid for the bot to respond to.
    Return True if it is, False otherwise. Currently, the bot will
    only respond to messages that tag it with an @mention in a
    public channel and are not from the bot itself.
    """
    if message.author == bot.user:
        # ensure the bot does not reply to itself
        return False

    if isinstance(message.channel, discord.DMChannel):
        return False

    if not bot.user.mentioned_in(message):
        return False

    return True
```

This function centralizes all the logic for determining whether the bot should respond to a message. It checks that:

* The message isn't from the bot itself
* The message isn't in a DM channel
* The bot is mentioned in the message

### Message Sanitization

```python theme={null}
def sanitize_message(message) -> str | None:
    """Remove the bot's mention from the message content if present"""
    content = message.content.replace(f"<@{bot.user.id}>", "").strip()
    if not content:
        return None
    return content
```

This helper removes the bot's mention from the message content, leaving just the actual user input.

### Peer ID Generation

```python theme={null}
def get_peer_id_from_discord(message):
    """Get a Honcho peer ID for the message author"""
    return f"discord_{str(message.author.id)}"
```

This creates a unique peer identifier for each Discord user by prefixing their Discord ID.

### LLM Integration

```python theme={null}
def llm(session, prompt) -> str:
    """
    Call the LLM with the given prompt and chat history.

    You should expand this function with custom logic, prompts, etc.
    """
    messages: list[dict[str, object]] = session.context().to_openai(
        assistant=assistant
    )
    messages.append({"role": "user", "content": prompt})

    try:
        completion = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(e)
        return f"Error: {e}"
```

This function handles the LLM interaction. It uses Honcho's built-in `to_openai()` method to automatically convert the session context into the format expected by OpenAI's chat completions API.

### Message Sending

```python theme={null}
async def send_discord_message(message, response_content: str):
    """Send a message to the Discord channel"""
    if len(response_content) > 1500:
        # Split response into chunks at newlines, keeping under 1500 chars
        chunks = []
        current_chunk = ""
        for line in response_content.splitlines(keepends=True):
            if len(current_chunk) + len(line) > 1500:
                chunks.append(current_chunk)
                current_chunk = line
            else:
                current_chunk += line
        if current_chunk:
            chunks.append(current_chunk)

        for chunk in chunks:
            await message.channel.send(chunk)
    else:
        await message.channel.send(response_content)
```

This function handles sending messages to Discord, automatically splitting long responses into multiple messages to stay within Discord's character limits.

## Honcho Integration

The new Honcho peer/session API makes integration much simpler:

```python theme={null}
peer = honcho_client.peer(id=get_peer_id_from_discord(message))
session = honcho_client.session(id=str(message.channel.id))
```

Here we create a peer object for the user and a session object using the Discord channel ID. This automatically handles user and session management.

```python theme={null}
# Save both the user's message and the bot's response to the session
session.add_messages(
    [
        peer.message(input),
        assistant.message(response),
    ]
)
```

After generating the response, we save both the user's input and the bot's response to the session using the `add_messages()` method. The `peer.message()` creates a message from the user, while `assistant.message()` creates a message from the assistant.

## Slash Commands

Discord bots also offer slash command functionality. Here's an example using Honcho's chat endpoint feature:

```python theme={null}
@bot.slash_command(
    name="chat",
    description="Chat with Honcho about a peer.",
)
async def chat(ctx, query: str):
    await ctx.defer()

    try:
        peer = honcho_client.peer(id=get_peer_id_from_discord(ctx))
        session = honcho_client.session(id=str(ctx.channel.id))

        response = peer.chat(
            query=query,
            session_id=session.id,
        )

        if response:
            await ctx.followup.send(response)
        else:
            await ctx.followup.send(
                f"I don't know anything about {ctx.author.name} because we haven't talked yet!"
            )
    except Exception as e:
        logger.error(f"Error calling Dialectic API: {e}")
        await ctx.followup.send(
            f"Sorry, there was an error processing your request: {str(e)}"
        )
```

This slash command uses Honcho's chat endpoint functionality to answer questions about the user based on their conversation history.

## Setup and Configuration

The bot requires several environment variables and setup:

```python theme={null}
honcho_client = Honcho()
assistant = honcho_client.peer(id="assistant", config={"observe_me": False})
openai = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=MODEL_API_KEY)
```

* `honcho_client`: The main Honcho client
* `assistant`: A peer representing the bot/assistant
* `openai`: OpenAI client configured to use OpenRouter

## Recap

The new Honcho peer/session API makes Discord bot integration much simpler and more intuitive. Key patterns we learned:

* **Peer/Session Model**: Users are represented as peers, conversations as sessions
* **Automatic Context Management**: `session.context().to_openai()` automatically formats chat history
* **Message Storage**: `session.add_messages()` stores both user and assistant messages
* **Representation Queries**: `peer.chat()` enables querying conversation history
* **Helper Functions**: Clean code organization with focused helper functions

This approach provides a clean, maintainable structure for building Discord bots with conversational memory and context management.


# Gmail
Source: https://honcho.dev/docs/v3/guides/gmail

Load Gmail threads into Honcho to give your AI agents memory of email conversations.

In this tutorial, we'll walk through how to ingest your Gmail emails into Honcho. By the end, each email thread will be a Honcho session and each participant will be a peer — giving your agents memory of who said what across your email history.

This guide includes a ready-to-run Python script that handles everything: Gmail OAuth, thread fetching, participant extraction, and Honcho ingestion. You can run it as-is or use the full tutorial below to understand each piece as you go.

<Note>
  The full script is available on [GitHub](https://github.com/plastic-labs/honcho/tree/main/examples/gmail). This is a developer-focused tutorial — it requires creating a Google Cloud project and OAuth credentials.
</Note>

## TL;DR

If you just want to get your emails into Honcho, here's everything you need.

### 1. Set Up Google Cloud Credentials

Follow Google's official [Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python) to:

1. Create a Google Cloud project and enable the Gmail API
2. Configure the OAuth consent screen
3. Create OAuth credentials (select **Desktop app** as the application type)
4. Download the credentials JSON into the same directory as the script

The script auto-detects Google's default `client_secret_*.json` filename, so no renaming needed. The script only needs the `gmail.readonly` scope.

### 2. Install Dependencies

<CodeGroup>
  ```bash uv theme={null}
  uv pip install google-api-python-client google-auth-oauthlib honcho-ai
  ```

  ```bash pip theme={null}
  pip install google-api-python-client google-auth-oauthlib honcho-ai
  ```
</CodeGroup>

### 3. Preview with a Dry Run

<CodeGroup>
  ```bash uv theme={null}
  uv run honcho_gmail.py --dry-run --max-threads 5
  ```

  ```bash python theme={null}
  python honcho_gmail.py --dry-run --max-threads 5
  ```
</CodeGroup>

On first run, a browser window opens for OAuth consent. After authorizing, a `token.json` file is created — future runs skip this step.

### 4. Load into Honcho

<CodeGroup>
  ```bash uv theme={null}
  export HONCHO_API_KEY=your_api_key
  uv run honcho_gmail.py --workspace gmail-inbox --max-threads 20
  ```

  ```bash python theme={null}
  export HONCHO_API_KEY=your_api_key
  python honcho_gmail.py --workspace gmail-inbox --max-threads 20
  ```
</CodeGroup>

You can filter threads with Gmail search syntax:

<CodeGroup>
  ```bash uv theme={null}
  uv run honcho_gmail.py --query "from:alice@example.com"
  uv run honcho_gmail.py --label INBOX
  uv run honcho_gmail.py --query "after:2024/01/01 has:attachment" --max-threads 50
  ```

  ```bash python theme={null}
  python honcho_gmail.py --query "from:alice@example.com"
  python honcho_gmail.py --label INBOX
  python honcho_gmail.py --query "after:2024/01/01 has:attachment" --max-threads 50
  ```
</CodeGroup>

That's it — your emails are now queryable in Honcho. Read on if you want to understand how the script works and the design decisions behind it.

***

## Full Tutorial

### How Gmail Maps to Honcho

The core idea is straightforward: each Gmail thread becomes a Honcho session, and each email participant becomes a peer. Here's the full mapping:

| Gmail Concept      | Honcho Concept                | Details                                           |
| ------------------ | ----------------------------- | ------------------------------------------------- |
| Your Gmail account | Workspace (`gmail`)           | One workspace for all email data                  |
| Email participant  | Peer                          | Email address as ID for deduplication             |
| Email thread       | Session (`gmail-thread-{id}`) | One session per thread, all participants attached |
| Individual email   | Message                       | Attributed to the sender with original timestamp  |

### Email as Peer ID

The script normalizes email addresses into URL-safe peer IDs — `alice@example.com` becomes `alice-example-com`. This means the same person is automatically deduplicated across threads. If Alice emails you in 10 different threads, all of those conversations accumulate under a single peer.

```python theme={null}
def peer_id_from_email(email: str) -> str:
    """Convert email to a valid Honcho peer ID."""
    return email.replace("@", "-").replace(".", "-")
```

This also means peers are consistent across data sources. If you import Granola meetings and Gmail threads for the same person, they merge under the same peer ID.

### Extracting Participants

Every email has a sender, recipients, and optionally CC/BCC addresses. The script extracts all of these to build a complete picture of who's involved in each thread:

```python theme={null}
for m in msgs:
    register_peer(m["from"])
    for addr in parse_address_list(m["to"]):
        register_peer(addr)
    for addr in parse_address_list(m["cc"]):
        register_peer(addr)
    for addr in parse_address_list(m["bcc"]):
        register_peer(addr)
```

Display names are extracted when available (e.g., `Alice Smith <alice@example.com>` → name: "Alice Smith"). When only an email is present, the script generates a name from the local part.

### Message Attribution and Timestamps

Each email becomes a message attributed to its sender via `peer.message()`. The original email timestamp is preserved using `created_at`, so Honcho sees the conversation in chronological order — not the order you imported it.

```python theme={null}
honcho_msgs.append(peer.message(
    content,
    metadata={
        "gmail_id": m["id"],
        "subject": m["subject"],
        "from": m["from"],
        "to": m["to"],
        "labels": m["labels"],
    },
    created_at=m["timestamp"],
))
```

### Multi-Peer Sessions

Each thread's session is linked to all participants using `session.add_peers()`. This means when you query Honcho about a peer, it has context not just from their messages but from the full conversations they participated in.

```python theme={null}
session = honcho.session(session_id, metadata={
    "gmail_thread_id": tid,
    "subject": subject,
    "source": "gmail",
    "message_count": len(msgs),
})
session.add_peers(thread_peers)
```

### Stripping Quoted Replies

Email threads are full of quoted replies — each message repeats everything above it. The script strips these out so only the new content is stored per message, avoiding duplication in Honcho's memory:

```python theme={null}
def strip_quoted_replies(text: str) -> str:
    """Strip quoted reply text, keeping only the new content."""
    lines = text.split("\n")
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if re.match(r"^On .+wrote:\s*$", stripped):
            break
        if stripped.startswith(">"):
            break
        # ... other reply markers
        clean_lines.append(line)
    return "\n".join(clean_lines).rstrip()
```

### Querying After Import

Once your emails are in Honcho, you can query any peer:

```python theme={null}
import os
from honcho import Honcho

honcho = Honcho(workspace_id="gmail-inbox", api_key=os.environ["HONCHO_API_KEY"])

alice = honcho.peer("alice-example-com")
print(alice.chat("What has Alice been discussing with me?"))
print(alice.chat("What action items has Alice mentioned?"))
```

***

## CLI Reference

```
usage: honcho_gmail.py [-h] [--workspace WORKSPACE] [--query QUERY]
                          [--label LABEL] [--max-threads N] [--dry-run]
                          [--credentials PATH] [--token PATH]

options:
  --workspace, -w    Honcho workspace ID (default: gmail)
  --query, -q        Gmail search query (e.g., 'from:alice@example.com')
  --label, -l        Gmail label to filter by (e.g., INBOX)
  --max-threads, -n  Max threads to fetch (default: 10)
  --dry-run          Preview without writing to Honcho
  --credentials, -c  Path to OAuth credentials JSON (auto-detects client_secret*.json)
  --token, -t        Path to store access token (default: token.json)
```

## Troubleshooting

### "No client\_secret\*.json file found"

Download OAuth credentials from Google Cloud Console and place the `client_secret_*.json` file in the same directory as the script.

### "Access blocked: This app's request is invalid"

Your OAuth consent screen may not be configured correctly. Ensure you've added the `gmail.readonly` scope.

### "Token has been expired or revoked"

Delete `token.json` and run the script again to re-authenticate.

### Rate Limits

The script includes a small delay when creating peers to avoid hitting Honcho's rate limits. For large imports (100+ threads), consider running in batches.

### Unique Messages

Use an AI assistant in your inbox? Want to parse out its messages differently? Feel free to modify and improve the structure of this script to fit your bespoke email setup. This script was written for agents and as such is easy to update with your coding assistant.

## Full Script

<Accordion title="honcho_gmail.py">
  ```python theme={null}
  #!/usr/bin/env python3
  """Load Gmail messages into Honcho.

  Uses the Gmail API directly (with OAuth) to fetch emails and the Honcho Python SDK to store them.
  Each Gmail thread becomes a Honcho session, each sender becomes a peer.

  Prerequisites:
  1. Create a Google Cloud project and enable the Gmail API
  2. Create OAuth 2.0 credentials (Desktop app type)
  3. Download the credentials JSON (client_secret_*.json) into this directory
  4. Install dependencies:
     pip install google-api-python-client google-auth-oauthlib honcho-ai

  On first run, a browser window will open for OAuth consent. After authorizing,
  a 'token.json' file will be created to store your credentials for future runs.
  """

  import argparse
  import base64
  import glob
  import os
  import re
  import time
  from datetime import datetime, timezone
  from email.header import decode_header, make_header
  from email.utils import getaddresses, parseaddr

  from google.auth.transport.requests import Request
  from google.oauth2.credentials import Credentials
  from google_auth_oauthlib.flow import InstalledAppFlow
  from googleapiclient.discovery import build
  from googleapiclient.errors import HttpError

  SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
  PEER_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")


  def find_credentials() -> str:
      """Find a Google OAuth credentials file in the current directory."""
      matches = glob.glob("client_secret*.json")
      if matches:
          return matches[0]
      raise FileNotFoundError(
          "No client_secret*.json file found.\n"
          "Download OAuth credentials from Google Cloud Console:\n"
          "1. Go to console.cloud.google.com\n"
          "2. Create/select a project and enable Gmail API\n"
          "3. Create OAuth 2.0 credentials (Desktop app)\n"
          "4. Download the JSON into this directory"
      )


  def get_gmail_service(credentials_file: str | None = None, token_file: str = "token.json"):
      """Authenticate and return a Gmail API service instance."""
      creds = None

      if os.path.exists(token_file):
          creds = Credentials.from_authorized_user_file(token_file, SCOPES)

      if not creds or not creds.valid:
          if creds and creds.expired and creds.refresh_token:
              print("Refreshing expired credentials...")
              creds.refresh(Request())
          else:
              if credentials_file is None:
                  credentials_file = find_credentials()
              print(f"Using credentials: {credentials_file}")
              print("Opening browser for OAuth consent...")
              flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
              creds = flow.run_local_server(port=0)

          with open(token_file, "w") as token:
              token.write(creds.to_json())
          print(f"Credentials saved to {token_file}")

      return build("gmail", "v1", credentials=creds)


  def list_threads(service, query: str = None, label_ids: list = None, max_results: int = 10) -> list[dict]:
      """List Gmail threads with pagination support."""
      all_threads = []
      page_token = None

      while len(all_threads) < max_results:
          try:
              params = {
                  "userId": "me",
                  "maxResults": min(100, max_results - len(all_threads)),
              }
              if query:
                  params["q"] = query
              if label_ids:
                  params["labelIds"] = label_ids
              if page_token:
                  params["pageToken"] = page_token

              response = service.users().threads().list(**params).execute()
              threads = response.get("threads", [])
              all_threads.extend(threads)

              page_token = response.get("nextPageToken")
              if not page_token:
                  break

          except HttpError as e:
              print(f"Error listing threads: {e}")
              break

      return all_threads[:max_results]


  def get_thread(service, thread_id: str) -> dict:
      """Fetch a complete Gmail thread with all messages."""
      try:
          return service.users().threads().get(
              userId="me",
              id=thread_id,
              format="full"
          ).execute()
      except HttpError as e:
          print(f"Error fetching thread {thread_id}: {e}")
          return {}


  def _decode_header_str(header: str) -> str:
      """Decode an RFC 2047 encoded header string to plain Unicode."""
      return str(make_header(decode_header(header)))


  def extract_email(from_header: str) -> str:
      """Extract bare email from an RFC 5322 header value."""
      _, addr = parseaddr(_decode_header_str(from_header))
      return addr.lower().strip()


  def extract_name(from_header: str) -> str:
      """Extract display name from an RFC 5322 header value."""
      name, _ = parseaddr(_decode_header_str(from_header))
      return name.strip() or from_header.strip()


  def decode_body(payload: dict) -> str:
      """Recursively extract plain text from a Gmail message payload."""
      if payload.get("mimeType") == "text/plain":
          data = payload.get("body", {}).get("data", "")
          if data:
              return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

      parts = payload.get("parts", [])
      for part in parts:
          text = decode_body(part)
          if text:
              return text
      return ""


  def strip_quoted_replies(text: str) -> str:
      """Strip quoted reply text from an email body, keeping only the new content."""
      lines = text.split("\n")
      clean_lines = []
      for line in lines:
          stripped = line.strip()
          if re.match(r"^On .+wrote:\s*$", stripped):
              break
          if stripped.startswith("---------- Forwarded message"):
              break
          if stripped.startswith(">"):
              break
          if re.match(r"^[-_]{10,}$", stripped):
              break
          clean_lines.append(line)
      return "\n".join(clean_lines).rstrip()


  def parse_address_list(header: str) -> list[str]:
      """Parse a comma-separated email header into individual addresses."""
      if not header.strip():
          return []
      decoded = _decode_header_str(header)
      return [
          f"{name} <{addr}>" if name else addr
          for name, addr in getaddresses([decoded])
          if addr
      ]


  def peer_id_from_email(email: str) -> str:
      """Convert email to a valid Honcho peer ID."""
      peer_id = re.sub(r"[^A-Za-z0-9_-]+", "-", email).strip("-").lower()
      peer_id = re.sub(r"-{2,}", "-", peer_id)
      if not peer_id:
          peer_id = "unknown-peer"

      if not PEER_ID_PATTERN.fullmatch(peer_id):
          raise ValueError(f"Generated peer ID is invalid: {peer_id!r}")
      return peer_id


  def fetch_thread_messages(service, thread_id: str) -> list[dict]:
      """Fetch all messages in a Gmail thread with full content."""
      data = get_thread(service, thread_id)
      messages = []

      for msg in data.get("messages", []):
          headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
          body = strip_quoted_replies(decode_body(msg.get("payload", {})))
          ts = int(msg.get("internalDate", "0")) / 1000

          messages.append({
              "id": msg["id"],
              "thread_id": msg["threadId"],
              "from": headers.get("From", ""),
              "to": headers.get("To", ""),
              "cc": headers.get("Cc", ""),
              "bcc": headers.get("Bcc", ""),
              "subject": headers.get("Subject", ""),
              "date": headers.get("Date", ""),
              "timestamp": datetime.fromtimestamp(ts, tz=timezone.utc),
              "body": body.strip(),
              "labels": msg.get("labelIds", []),
              "snippet": msg.get("snippet", ""),
          })

      return messages


  def main():
      parser = argparse.ArgumentParser(description="Load Gmail messages into Honcho")
      parser.add_argument("--workspace", "-w", default="gmail", help="Honcho workspace ID (default: gmail)")
      parser.add_argument("--query", "-q", default=None, help="Gmail search query (e.g. 'from:alice@example.com')")
      parser.add_argument("--label", "-l", default=None, help="Gmail label to filter by (e.g. INBOX)")
      parser.add_argument("--max-threads", "-n", type=int, default=10, help="Max threads to fetch (default: 10)")
      parser.add_argument("--dry-run", action="store_true", help="Print what would be loaded without writing to Honcho")
      parser.add_argument("--credentials", "-c", default=None, help="Path to OAuth credentials JSON (auto-detects client_secret*.json)")
      parser.add_argument("--token", "-t", default="token.json", help="Path to store/load access token")
      args = parser.parse_args()

      # Authenticate
      print("Authenticating with Gmail API...")
      service = get_gmail_service(args.credentials, args.token)
      print("  Authenticated successfully!")

      label_ids = [args.label] if args.label else None

      # List threads
      print(f"\nFetching up to {args.max_threads} threads from Gmail...")
      threads = list_threads(service, query=args.query, label_ids=label_ids, max_results=args.max_threads)
      print(f"  Found {len(threads)} threads")

      if not threads:
          print("No threads found. Try adjusting --query or --label.")
          return

      # Fetch full messages for each thread
      all_thread_messages = {}
      seen_peers = {}

      def register_peer(addr: str):
          email = extract_email(addr)
          if email and email not in seen_peers:
              name = extract_name(addr)
              if name.lower().strip() == email or "@" in name:
                  name = email.split("@")[0].replace(".", " ").title()
              seen_peers[email] = {
                  "name": name,
                  "peer_id": peer_id_from_email(email),
                  "email": email,
              }

      for i, t in enumerate(threads):
          tid = t["id"]
          print(f"  Fetching thread {i+1}/{len(threads)}: {tid}")
          msgs = fetch_thread_messages(service, tid)
          all_thread_messages[tid] = msgs
          for m in msgs:
              register_peer(m["from"])
              for addr in parse_address_list(m["to"]):
                  register_peer(addr)
              for addr in parse_address_list(m["cc"]):
                  register_peer(addr)
              for addr in parse_address_list(m["bcc"]):
                  register_peer(addr)

      # Summary
      total_msgs = sum(len(v) for v in all_thread_messages.values())
      print("\nSummary:")
      print(f"  Threads: {len(all_thread_messages)}")
      print(f"  Messages: {total_msgs}")
      print(f"  Unique participants: {len(seen_peers)}")
      for email, info in seen_peers.items():
          print(f"    {info['peer_id']} ({info['name']} <{email}>)")

      if args.dry_run:
          print("\n[DRY RUN] Would create the above in Honcho. Showing first message per thread:")
          for tid, msgs in all_thread_messages.items():
              m = msgs[0]
              body_preview = m["body"][:120].replace("\n", " ") if m["body"] else m["snippet"][:120]
              print(f"  Thread {tid}: {m['subject']}")
              print(f"    {m['from']} @ {m['date']}")
              print(f"    {body_preview}...")
          return

      # Load into Honcho
      from honcho import Honcho

      print(f"\nLoading into Honcho workspace '{args.workspace}'...")
      honcho = Honcho(workspace_id=args.workspace)

      # Create peers
      peers = {}
      for i, (email, info) in enumerate(seen_peers.items()):
          if i > 0 and i % 4 == 0:
              time.sleep(1)
          peers[email] = honcho.peer(info["peer_id"], metadata={
              "email": email,
              "name": info["name"],
              "source": "gmail",
          })
          print(f"  Peer: {info['peer_id']}")

      # Create sessions and messages per thread
      for tid, msgs in all_thread_messages.items():
          subject = msgs[0]["subject"] if msgs else "No subject"
          session_id = f"gmail-thread-{tid}"

          thread_peer_emails = set()
          for m in msgs:
              thread_peer_emails.add(extract_email(m["from"]))
              for addr in parse_address_list(m["to"]):
                  thread_peer_emails.add(extract_email(addr))
              for addr in parse_address_list(m["cc"]):
                  thread_peer_emails.add(extract_email(addr))
              for addr in parse_address_list(m["bcc"]):
                  thread_peer_emails.add(extract_email(addr))
          thread_peers = [peers[e] for e in thread_peer_emails if e in peers]

          session = honcho.session(session_id, metadata={
              "gmail_thread_id": tid,
              "subject": subject,
              "source": "gmail",
              "message_count": len(msgs),
          })
          session.add_peers(thread_peers)

          honcho_msgs = []
          for m in msgs:
              email = extract_email(m["from"])
              peer = peers.get(email)
              if not peer:
                  continue
              content = m["body"] if m["body"] else m["snippet"]
              if not content:
                  continue
              honcho_msgs.append(peer.message(
                  content,
                  metadata={
                      "gmail_id": m["id"],
                      "subject": m["subject"],
                      "from": m["from"],
                      "to": m["to"],
                      "labels": m["labels"],
                  },
                  created_at=m["timestamp"],
              ))

          if honcho_msgs:
              session.add_messages(honcho_msgs)
              print(f"  Session {session_id}: {len(honcho_msgs)} messages — {subject[:60]}")

      print(f"\nDone! Loaded {total_msgs} messages into workspace '{args.workspace}'.")


  if __name__ == "__main__":
      main()

  ```
</Accordion>

## Next Steps

<CardGroup>
  <Card title="Design Patterns" icon="cubes" href="/v3/documentation/core-concepts/design-patterns">
    See how the Granola integration maps to common Honcho patterns.
  </Card>

  <Card title="GitHub Repository" icon="github" href="https://github.com/plastic-labs/honcho/tree/main/examples/gmail">
    Source code and example script.
  </Card>
</CardGroup>


# Granola
Source: https://honcho.dev/docs/v3/guides/granola

Import meeting notes and transcripts from Granola into Honcho

In this tutorial, we'll walk through how to import your [Granola](https://granola.ai) meeting data into Honcho. By the end, your meeting participants, transcripts, and summaries will be mapped onto Honcho's peer and session model — giving your agents queryable memory of the people you meet with.

This guide includes a ready-to-run Python script that handles everything: Granola OAuth, meeting fetching, participant detection, and interactive import. You can run it as-is or use the full tutorial below to understand each design decision.

<Note>
  The full script is available on [GitHub](https://github.com/plastic-labs/honcho/tree/main/examples/granola).
</Note>

## TL;DR

If you just want to get your meetings into Honcho, here's everything you need.

### 1. Install Dependencies

<CodeGroup>
  ```bash uv theme={null}
  uv pip install honcho-ai httpx
  ```

  ```bash pip theme={null}
  pip install honcho-ai httpx
  ```
</CodeGroup>

### 2. Set Your API Key

```bash theme={null}
export HONCHO_API_KEY="your-key-from-app.honcho.dev"
```

### 3. Run the Script

<CodeGroup>
  ```bash uv theme={null}
  uv run python honcho_granola.py
  ```

  ```bash python theme={null}
  python honcho_granola.py
  ```
</CodeGroup>

The script will:

1. Open your browser for Granola OAuth authentication
2. Fetch all meetings and their content
3. Walk you through each meeting interactively — confirm peers, choose import mode, skip meetings you don't want
4. Print a summary of what was transferred

That's it — your meetings are now queryable in Honcho. Read on if you want to understand how the script works and the design decisions behind it.

***

## Full Tutorial

### How Granola Maps to Honcho

The core idea is straightforward: each Granola meeting becomes a Honcho session, and each participant becomes a peer. Here's the full mapping:

| Granola Concept      | Honcho Concept            | Details                                       |
| -------------------- | ------------------------- | --------------------------------------------- |
| Your Granola account | Workspace (`granola`)     | One workspace for all meetings                |
| Meeting participant  | Peer                      | Email as ID for deduplication across meetings |
| Individual meeting   | Session (`meeting-{id}`)  | One session per meeting                       |
| Transcript turns     | Messages with attribution | Two-person calls get full speaker attribution |
| Meeting summary      | Message from note creator | Multi-person calls store the summary          |

### Email as Peer ID

The script uses email addresses as the basis for peer IDs, normalized to a URL-safe format (e.g., `alice@example.com` becomes `alice-example-com`). This ensures consistent identification across meetings — if you meet someone in 5 different calls, all conversations accumulate under the same peer.

```python theme={null}
# These all resolve to the same peer:
honcho.peer("alice-example-com")  # From Meeting A
honcho.peer("alice-example-com")  # From Meeting B
```

This also means peers are consistent across data sources. If you import both Granola meetings and Gmail threads for the same person, they merge under the same peer ID.

### Auto-Detecting "Me"

Granola marks the note creator in its participant list with `(note creator)`. The script uses this to identify you automatically — no configuration needed.

```
Participants: You (note creator) from Your Company <you@example.com>,
              Alice from Acme Corp <alice@example.com>
```

### Two-Person Calls: Full Attribution

When exactly one other participant is present *and* the transcript contains `Them:` turns, the script stores the transcript with speaker-attributed messages. Consecutive same-speaker turns are merged before storing, cleaning up the fragmentation that's common in raw transcripts.

```python theme={null}
session.add_messages([
    me.message("What's your timeline for the launch?"),
    them.message("We're targeting Q2, but it depends on the API integration."),
])
```

### Multi-Person Calls: Summary Mode

Granola's transcript uses `Them:` for all non-creator speakers with no disambiguation — in a 4-person call, everyone else is just `Them:`. Rather than guess incorrectly, the script stores Granola's summary as your record of the meeting, with participants in metadata.

```python theme={null}
session.add_messages([
    me.message(
        f"Meeting: Product Planning\n"
        f"Date: Mar 5, 2026 2:00 PM\n"
        f"Participants: Alice from Acme Corp, Bob from Widgets Inc\n\n"
        f"{meeting_summary}",
        metadata={
            "participants": "Alice from Acme Corp, Bob from Widgets Inc",
            "mode": "summary",
            "granola_meeting_id": meeting_id,
        }
    )
])
```

The summary is attributed to you because it's *your* record of what happened. Granola captured your notes from a meeting where those people were present.

### Interactive Confirmation

For each meeting, you choose the import mode: two-person (full attribution), summary, or skip. For multi-person calls that are actually 1:1s (extra participants listed but didn't speak), you can override the detection and select the actual speaker.

### Noisy Transcripts Preserved

Granola's raw transcripts are often fragmented (`Me: Yeah.  Them: Yeah.  Me: And.`). The script merges consecutive same-speaker turns but otherwise preserves the raw content. Honcho's reasoning extracts signal from noisy data.

### Querying After Import

Once your meetings are in Honcho, you can query any peer:

```python theme={null}
import os
from honcho import Honcho

honcho = Honcho(workspace_id="granola", api_key=os.environ["HONCHO_API_KEY"])

# Peer IDs are normalized from emails: alice@example.com -> alice-example-com
alice = honcho.peer("alice-example-com")
print(alice.chat("What is Alice working on?"))
print(alice.chat("What concerns has Alice raised?"))

me = honcho.peer("you-example-com")
print(me.chat("What topics do I discuss most frequently?"))
```

### Combining with Other Sources

Because meetings live in a standard Honcho workspace, you can enrich peer representations with data from other channels:

```python theme={null}
# Same workspace, same peer — data accumulates
alice = honcho.peer("alice-example-com")
me = honcho.peer("you-example-com")

discord_session = honcho.session("discord-general-2024-03")
discord_session.add_messages([
    alice.message("Just shipped the new API version!"),
    me.message("Congrats! How's the migration guide coming?"),
])

# Queries now draw from both meeting transcripts AND Discord history
alice.chat("What has Alice shipped recently?")
```

***

## Troubleshooting

| Issue                            | Fix                                                                                                          |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Granola OAuth fails              | Ensure you have a paid Granola plan (MCP requires Pro+). Clear cached token and retry.                       |
| Missing transcripts              | Free tier has no transcript access. The script falls back to summary content.                                |
| 500 errors from Honcho           | Check for null bytes or control characters in transcript content. The script sanitizes these automatically.  |
| Rate limiting with many meetings | The script processes sequentially with delays. Honcho ingestion is async — don't poll for immediate results. |

## Full Script

<Accordion title="honcho_granola.py">
  ```python theme={null}
  #!/usr/bin/env python3
  """Load Granola meeting notes into Honcho.

  Uses the Granola MCP server (with OAuth) to fetch meetings and the Honcho Python SDK
  to store them. Each meeting becomes a Honcho session. Two-person meetings get full
  speaker attribution; multi-person meetings are stored as summaries.

  Prerequisites:
      pip install honcho-ai httpx

  Environment Variables:
      HONCHO_API_KEY - Your Honcho API key (get from app.honcho.dev/api-keys)

  Usage:
      python honcho_granola.py
  """

  import asyncio
  import base64
  import hashlib
  import json
  import os
  import re
  import secrets
  import sys
  import threading
  import traceback
  import webbrowser
  from dataclasses import dataclass, field
  from datetime import datetime, timezone
  from http.server import HTTPServer, BaseHTTPRequestHandler
  from typing import Any
  from urllib.parse import parse_qs, urlencode, urlparse

  import httpx


  @dataclass
  class Participant:
      name: str
      email: str | None = None
      org: str | None = None


  @dataclass
  class ParsedParticipants:
      note_creator: Participant | None = None
      others: list[Participant] = field(default_factory=list)


  @dataclass
  class TranscriptTurn:
      speaker: str
      text: str


  # Granola MCP + OAuth endpoints
  GRANOLA_MCP_URL = "https://mcp.granola.ai/mcp"
  AUTH_BASE = "https://mcp-auth.granola.ai"
  OAUTH_REDIRECT_PORT = 8765
  OAUTH_REDIRECT_URI = f"http://localhost:{OAUTH_REDIRECT_PORT}/callback"

  # Honcho message size limit (25000 max, leave headroom)
  MAX_MESSAGE_LEN = 24000


  # ---------------------------------------------------------------------------
  # OAuth callback handler (must be a class for BaseHTTPRequestHandler)
  # ---------------------------------------------------------------------------

  class _OAuthCallback(BaseHTTPRequestHandler):
      auth_result: dict[str, str | None] = {"code": None, "error": None}

      def do_GET(self):
          params = parse_qs(urlparse(self.path).query)
          if "code" in params:
              _OAuthCallback.auth_result["code"] = params["code"][0]
              self.send_response(200)
              self.send_header("Content-Type", "text/html")
              self.end_headers()
              self.wfile.write(b"<h1>Authenticated! You can close this window.</h1>")
          elif "error" in params:
              _OAuthCallback.auth_result["error"] = params.get("error_description", params["error"])[0]
              self.send_response(400)
              self.send_header("Content-Type", "text/html")
              self.end_headers()
              self.wfile.write(f"<h1>Error: {_OAuthCallback.auth_result['error']}</h1>".encode())
          else:
              self.send_response(404)
              self.end_headers()

      def log_message(self, fmt, *args):
          pass


  # ---------------------------------------------------------------------------
  # Granola OAuth + MCP
  # ---------------------------------------------------------------------------

  async def authenticate(http_client: httpx.AsyncClient) -> str:
      """Perform OAuth (DCR + PKCE) with Granola. Returns access token."""
      _OAuthCallback.auth_result = {"code": None, "error": None}

      print("\nAuthenticating with Granola...")

      # Register client (DCR)
      resp = await http_client.post(
          f"{AUTH_BASE}/oauth2/register",
          json={
              "client_name": "Granola to Honcho Transfer",
              "redirect_uris": [OAUTH_REDIRECT_URI],
              "grant_types": ["authorization_code"],
              "response_types": ["code"],
              "token_endpoint_auth_method": "none",
          },
      )
      if resp.status_code not in (200, 201):
          raise RuntimeError(f"Client registration failed: {resp.status_code}")
      client_id = resp.json().get("client_id")

      # PKCE
      verifier = secrets.token_urlsafe(32)
      challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()

      # Browser auth
      auth_url = f"{AUTH_BASE}/oauth2/authorize?" + urlencode({
          "client_id": client_id,
          "redirect_uri": OAUTH_REDIRECT_URI,
          "response_type": "code",
          "state": "granola-honcho-transfer",
          "code_challenge": challenge,
          "code_challenge_method": "S256",
      })

      server = HTTPServer(("localhost", OAUTH_REDIRECT_PORT), _OAuthCallback)
      thread = threading.Thread(target=server.handle_request)
      thread.start()

      print("  Opening browser for authentication...")
      webbrowser.open(auth_url)
      thread.join(timeout=120)
      server.server_close()

      auth_result = _OAuthCallback.auth_result
      if auth_result["error"]:
          raise RuntimeError(f"Authentication failed: {auth_result['error']}")
      if not auth_result["code"]:
          raise RuntimeError("Authentication timed out")

      # Exchange code for token
      resp = await http_client.post(
          f"{AUTH_BASE}/oauth2/token",
          data={
              "grant_type": "authorization_code",
              "code": auth_result["code"],
              "redirect_uri": OAUTH_REDIRECT_URI,
              "client_id": client_id,
              "code_verifier": verifier,
          },
          headers={"Content-Type": "application/x-www-form-urlencoded"},
      )
      if resp.status_code != 200:
          raise RuntimeError(f"Token exchange failed: {resp.status_code}")

      print("  Authenticated successfully!")
      return resp.json()["access_token"]


  async def call_mcp_tool(
      http_client: httpx.AsyncClient,
      access_token: str,
      tool_name: str,
      arguments: dict[str, Any] | None = None,
  ) -> dict[str, Any]:
      """Call a Granola MCP tool, handling both JSON and SSE responses."""
      resp = await http_client.post(
          GRANOLA_MCP_URL,
          json={
              "jsonrpc": "2.0",
              "id": 1,
              "method": "tools/call",
              "params": {"name": tool_name, "arguments": arguments or {}},
          },
          headers={
              "Authorization": f"Bearer {access_token}",
              "Content-Type": "application/json",
              "Accept": "application/json, text/event-stream",
          },
      )
      if resp.status_code != 200:
          raise RuntimeError(f"MCP call failed: {resp.status_code} - {resp.text}")

      # SSE response
      if "text/event-stream" in resp.headers.get("content-type", ""):
          result = None
          for line in resp.text.split("\n"):
              if line.strip().startswith("data: "):
                  try:
                      parsed = json.loads(line.strip()[6:])
                      if "result" in parsed:
                          result = parsed
                      elif "error" in parsed:
                          raise RuntimeError(f"MCP error: {parsed['error']}")
                  except json.JSONDecodeError:
                      continue
          if result:
              final = result.get("result", {})
              return final if isinstance(final, dict) else {"result": final}
          raise RuntimeError("No result in SSE response")

      # JSON response
      result = resp.json()
      if "error" in result:
          raise RuntimeError(f"MCP error: {result['error']}")
      return result.get("result", {})


  def extract_mcp_text(result: dict[str, Any]) -> str:
      """Extract text from the first content block of an MCP result.

      Raises ValueError if the response structure is unexpected.
      """
      content = result.get("content", [])
      if not isinstance(content, list) or not content:
          raise ValueError(f"MCP response missing content array: {list(result.keys())}")
      first = content[0]
      if not isinstance(first, dict) or "text" not in first:
          raise ValueError(f"MCP content block missing 'text' field: {first}")
      return str(first["text"])


  # ---------------------------------------------------------------------------
  # Granola data fetching
  # ---------------------------------------------------------------------------

  async def list_meetings(
      http_client: httpx.AsyncClient, access_token: str, limit: int = 100,
  ) -> list[dict[str, Any]]:
      """List meetings from Granola MCP. Parses Granola's XML-like response format."""
      result = await call_mcp_tool(http_client, access_token, "list_meetings", {"limit": limit})
      text = extract_mcp_text(result)

      meetings: list[dict[str, Any]] = []
      for match in re.finditer(r'<meeting\s+id="([^"]+)"\s+title="([^"]+)"\s+date="([^"]+)"', text):
          mid, title, date = match.groups()
          block_end = text.find("</meeting>", match.end())
          block = text[match.end():block_end] if block_end != -1 else ""
          p_match = re.search(r"<known_participants>\s*(.*?)\s*</known_participants>", block, re.DOTALL)
          meetings.append({
              "id": mid,
              "title": title,
              "date": date,
              "participants": p_match.group(1).strip() if p_match else "",
          })

      return meetings


  async def get_meeting_details(
      http_client: httpx.AsyncClient, access_token: str, meeting_id: str,
  ) -> dict[str, Any]:
      """Get full meeting details including notes."""
      result = await call_mcp_tool(http_client, access_token, "get_meetings", {"meeting_ids": [meeting_id]})
      text = extract_mcp_text(result)
      return {"id": meeting_id, "raw_content": text}


  async def get_meeting_transcript(
      http_client: httpx.AsyncClient, access_token: str, meeting_id: str,
      max_retries: int = 3,
  ) -> str | None:
      """Get transcript for a meeting (paid tiers only).

      Retries on rate limit responses with exponential backoff.
      """
      for attempt in range(max_retries):
          try:
              result = await call_mcp_tool(http_client, access_token, "get_meeting_transcript", {"meeting_id": meeting_id})
              text = extract_mcp_text(result)
          except Exception as e:
              print(f"   Transcript unavailable: {e}")
              return None

          if not text or "no transcript" in text.lower():
              return None

          # Granola returns rate limit errors as content text, not HTTP errors
          if "rate limit" in text.lower():
              wait = 2 ** attempt * 3  # 3s, 6s, 12s
              print(f"   ⚠ Granola rate limit hit (attempt {attempt + 1}/{max_retries}), waiting {wait}s...")
              await asyncio.sleep(wait)
              continue

          return text

      print(f"   ⚠ Transcript skipped after {max_retries} rate limit retries")
      return None


  async def fetch_all_meetings(
      http_client: httpx.AsyncClient, access_token: str,
  ) -> list[dict[str, Any]]:
      """Fetch meeting list and enrich each with transcript and details."""
      print("\nFetching meetings from Granola...")
      meetings = await list_meetings(http_client, access_token, limit=500)
      if not meetings:
          print("No meetings found.")
          return []
      print(f"  Found {len(meetings)} meetings. Fetching content...\n")

      for i, m in enumerate(meetings, 1):
          mid = m.get("id")
          if not mid:
              continue

          transcript = await get_meeting_transcript(http_client, access_token, mid)
          if transcript:
              m["transcript"] = transcript

          try:
              m.update(await get_meeting_details(http_client, access_token, mid))
          except Exception as exc:
              print(f"   Failed to fetch details for {mid}: {exc}")

          has_t = "transcript" in m
          has_s = bool(extract_summary(m))
          label = "transcript+summary" if has_t and has_s else "transcript only" if has_t else "summary only" if has_s else "basic only"
          print(f"  [{i}/{len(meetings)}] {label}: {m.get('title', 'Untitled')[:45]}")
          await asyncio.sleep(1.5)  # rate limit

      return meetings


  # ---------------------------------------------------------------------------
  # Parsing helpers
  # ---------------------------------------------------------------------------

  def parse_participants(participants_str: str) -> ParsedParticipants:
      """Parse Granola's participant string into structured participants.

      Warns on unparsable entries instead of silently dropping them.
      """
      result = ParsedParticipants()
      if not participants_str:
          return result

      # Split on commas, but not inside angle brackets
      entries, current, depth = [], [], 0
      for ch in participants_str:
          if ch == "<":
              depth += 1
          elif ch == ">":
              depth = max(depth - 1, 0)
          elif ch == "," and depth == 0:
              entries.append("".join(current))
              current = []
              continue
          current.append(ch)
      if current:
          entries.append("".join(current))

      for entry in entries:
          entry = entry.strip()
          if not entry:
              continue

          is_creator = "(note creator)" in entry
          clean = entry.replace("(note creator)", "").strip()

          email_match = re.search(r"<([^>]+)>", clean)
          email = email_match.group(1) if email_match else None
          name = re.sub(r"\s*<[^>]+>", "", clean).strip()

          if not name:
              print(f"  Warning: could not parse participant entry: {entry!r}")
              continue

          org = None
          org_match = re.match(r"(.+?)\s+from\s+(.+)", name)
          if org_match:
              name, org = org_match.group(1).strip(), org_match.group(2).strip()

          person = Participant(name=name, email=email, org=org)
          if is_creator:
              result.note_creator = person
          else:
              result.others.append(person)

      return result


  def parse_transcript_turns(raw: str) -> list[TranscriptTurn]:
      """Split a Granola transcript into speaker turns."""
      # Unwrap JSON wrapper if present
      try:
          parsed = json.loads(raw)
          if isinstance(parsed, dict) and "transcript" in parsed:
              raw = str(parsed["transcript"])
      except (json.JSONDecodeError, TypeError):
          pass

      parts = re.split(r"(?:^|\s{2,})(Me|Them):\s*", raw)
      turns: list[TranscriptTurn] = []
      i = 1
      while i < len(parts) - 1:
          text = parts[i + 1].strip()
          if text:
              turns.append(TranscriptTurn(speaker=parts[i], text=text))
          i += 2
      return turns


  def extract_summary(meeting: dict[str, Any]) -> str:
      """Extract best available summary text from meeting data."""
      candidates = []
      for key in ("summary", "notes", "note", "meeting_notes", "description"):
          val = meeting.get(key)
          if isinstance(val, str) and val.strip():
              candidates.append(val.strip())

      raw = meeting.get("raw_content")
      if isinstance(raw, str) and raw.strip():
          candidates.append(raw.strip())

      for c in candidates:
          for tag in ("summary", "notes"):
              m = re.search(rf"<{tag}>\s*(.*?)\s*</{tag}>", c, re.DOTALL)
              if m:
                  return m.group(1).strip()

      return candidates[0] if candidates else ""


  def peer_id_from(value: str) -> str:
      """Normalize a name or email into a Honcho-safe peer ID."""
      norm = re.sub(r"[^a-z0-9_-]+", "-", value.strip().lower())
      norm = re.sub(r"-{2,}", "-", norm).strip("-_")
      return (norm or "peer")[:100]


  def sanitize(text: str) -> str:
      """Remove null bytes and control characters."""
      return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)


  def parse_date(date_str: str) -> datetime:
      """Parse Granola's date format into a timezone-aware datetime.

      Raises ValueError if the date string doesn't match any known format.
      """
      for fmt in ["%b %d, %Y %I:%M %p", "%b %d, %Y %I:%M:%S %p", "%B %d, %Y %I:%M %p"]:
          try:
              return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
          except ValueError:
              continue
      raise ValueError(f"Unrecognized date format: {date_str!r}")


  # ---------------------------------------------------------------------------
  # Honcho import helpers
  # ---------------------------------------------------------------------------

  def build_messages(
      peer: Any,
      content: str,
      metadata: dict[str, object] | None,
      created_at: datetime,
  ) -> list[Any]:
      """Build chunked messages for a single peer, attaching metadata to the first chunk."""
      messages = []
      content = sanitize(content)
      for start in range(0, len(content), MAX_MESSAGE_LEN):
          chunk = content[start:start + MAX_MESSAGE_LEN]
          msg_meta = metadata if start == 0 else None
          messages.append(peer.message(chunk, metadata=msg_meta, created_at=created_at))
      return messages


  def send_messages(session: Any, messages: list[Any]) -> None:
      """Send messages to a session in batches of 100."""
      for batch_start in range(0, len(messages), 100):
          session.add_messages(messages[batch_start:batch_start + 100])


  def import_two_person(
      honcho: Any,
      session: Any,
      me_peer_id: str,
      them_peer_id: str,
      turns: list[TranscriptTurn],
      metadata: dict[str, object],
      created_at: datetime,
  ) -> None:
      """Import a two-person meeting with speaker attribution."""
      me_peer = honcho.peer(me_peer_id)
      them_peer = honcho.peer(them_peer_id)

      # Merge consecutive same-speaker turns
      merged: list[TranscriptTurn] = []
      for t in turns:
          if merged and merged[-1].speaker == t.speaker:
              merged[-1].text += " " + t.text
          else:
              merged.append(TranscriptTurn(speaker=t.speaker, text=t.text))

      messages: list[Any] = []
      for i, t in enumerate(merged):
          peer = me_peer if t.speaker == "Me" else them_peer
          msg_meta = metadata if i == 0 else None
          messages.extend(build_messages(peer, t.text, msg_meta, created_at))

      send_messages(session, messages)
      print(f"  -> Imported as 2-person ({me_peer_id} + {them_peer_id})")


  def import_summary(
      honcho: Any,
      session: Any,
      me_peer_id: str,
      meeting: dict[str, Any],
      metadata: dict[str, object],
      created_at: datetime,
  ) -> None:
      """Import a meeting as a summary message."""
      me_peer = honcho.peer(me_peer_id)
      summary = extract_summary(meeting)
      if not summary:
          raw_t = meeting.get("transcript", "")
          try:
              parsed = json.loads(raw_t)
              summary = str(parsed.get("transcript", "")) if isinstance(parsed, dict) else raw_t
          except (json.JSONDecodeError, TypeError):
              summary = raw_t
      summary = summary or "No content available"

      title = meeting.get("title", "Untitled")
      date = meeting.get("date", "")
      header = f"Meeting: {title}\nDate: {date}\nParticipants: {meeting.get('participants', '')}\n\n"

      messages = build_messages(me_peer, header + summary, metadata, created_at)
      send_messages(session, messages)
      print("  -> Imported as summary")


  def resolve_them_participant(others: list[Participant]) -> Participant | None:
      """Ask user to pick which participant is 'Them' from a multi-person meeting."""
      for j, p in enumerate(others, 1):
          email_str = f" <{p.email}>" if p.email else ""
          print(f"    {j}. {p.name}{email_str}")
      idx_str = input(f"  Who is 'Them'? [1-{len(others)}]: ").strip()
      try:
          return others[int(idx_str) - 1]
      except (ValueError, IndexError):
          print("  Invalid selection.")
          return None


  def review_meeting(
      index: int,
      total: int,
      meeting: dict[str, Any],
      participants: ParsedParticipants,
      turns: list[TranscriptTurn],
  ) -> tuple[str, Participant | None]:
      """Display meeting info and get user's import choice.

      Returns (mode, them_participant) where mode is one of:
      - "two_person": import with speaker attribution using them_participant
      - "summary": import as a single summary message
      - "skip": skip this meeting
      """
      title = meeting.get("title", "Untitled")
      date = meeting.get("date", "")
      creator = participants.note_creator
      others = participants.others

      me_turns = sum(1 for t in turns if t.speaker == "Me")
      them_turns = len(turns) - me_turns
      total_words = sum(len(t.text.split()) for t in turns)

      print(f"\n{'─' * 60}")
      print(f"  [{index}/{total}] {title}")
      print(f"  Date: {date}")
      if creator:
          print(f"  You:  {creator.name} <{creator.email}>")
      for j, p in enumerate(others, 1):
          email_str = f" <{p.email}>" if p.email else ""
          org_str = f" ({p.org})" if p.org else ""
          print(f"    {j}. {p.name}{email_str}{org_str}")

      has_transcript = bool(meeting.get("transcript"))
      if turns:
          print(f"  Transcript: {me_turns} Me, {them_turns} Them, ~{total_words} words")
          if them_turns == 0:
              print("  ** No 'Them' turns — nobody else spoke **")
          if total_words < 30:
              print("  ** Very short — might be empty **")
      elif has_transcript:
          raw = meeting["transcript"]
          print(f"  Transcript: present ({len(raw)} chars) but could not parse speaker turns")
          print(f"  Preview: {raw[:200]!r}")
      else:
          print(f"  Content: {'summary available' if extract_summary(meeting) else 'metadata only'}")

      # Two-person default: exactly one other participant with transcript
      if len(others) == 1 and them_turns > 0:
          them_label = others[0].name + (f" <{others[0].email}>" if others[0].email else "")
          print(f"\n  Detected: 2-person call (you + {them_label})")
          choice = input("  [Enter] 2-person / [s]ummary / [k] skip: ").strip().lower()
          while choice not in ("", "s", "k"):
              choice = input("  [Enter] 2-person / [s]ummary / [k] skip: ").strip().lower()
          if choice == "k":
              return ("skip", None)
          if choice == "s":
              return ("summary", None)
          return ("two_person", others[0])

      # Multi-person with transcript
      if len(others) > 1 and them_turns > 0:
          print(f"\n  {len(others)} participants")
          choice = input("  [Enter] summary / [2] 2-person / [k] skip: ").strip().lower()
          while choice not in ("", "2", "k"):
              choice = input("  [Enter] summary / [2] 2-person / [k] skip: ").strip().lower()
          if choice == "k":
              return ("skip", None)
          if choice == "2":
              them = resolve_them_participant(others)
              if them is None:
                  return ("summary", None)
              return ("two_person", them)
          return ("summary", None)

      # No transcript or no other speakers
      choice = input("  [Enter] summary / [k] skip: ").strip().lower()
      while choice not in ("", "k"):
          choice = input("  [Enter] summary / [k] skip: ").strip().lower()
      if choice == "k":
          return ("skip", None)
      return ("summary", None)


  # ---------------------------------------------------------------------------
  # Main
  # ---------------------------------------------------------------------------

  async def main():
      print("=" * 60)
      print("  Granola -> Honcho Meeting Notes Transfer")
      print("=" * 60)

      if not os.environ.get("HONCHO_API_KEY"):
          print("\nError: HONCHO_API_KEY not set.")
          print("  Get your key at: https://app.honcho.dev/api-keys")
          sys.exit(1)

      async with httpx.AsyncClient(timeout=60.0) as http_client:
          try:
              access_token = await authenticate(http_client)
              meetings = await fetch_all_meetings(http_client, access_token)
              if not meetings:
                  sys.exit(0)

              from honcho import Honcho

              honcho = Honcho(workspace_id="granola")
              seen_peers: set[str] = set()
              results = {"imported": 0, "skipped": 0, "failed": 0}

              print("\n" + "=" * 60)
              print("  Review each meeting")
              print("=" * 60)

              for i, m in enumerate(meetings, 1):
                  mid = m.get("id")
                  if not mid:
                      continue

                  participants = parse_participants(m.get("participants", ""))
                  turns = parse_transcript_turns(m["transcript"]) if m.get("transcript") else []

                  mode, them = review_meeting(i, len(meetings), m, participants, turns)

                  if mode == "skip":
                      print("  -> Skipped")
                      results["skipped"] += 1
                      continue

                  # Resolve creator peer
                  creator = participants.note_creator
                  me_source = (creator.email or creator.name) if creator else None
                  if not me_source:
                      print("  -> Skipped (no creator identifier)")
                      results["skipped"] += 1
                      continue

                  me_peer_id = peer_id_from(me_source)
                  if me_peer_id not in seen_peers:
                      print(f"  New peer: {me_source} ({me_peer_id})")
                      seen_peers.add(me_peer_id)

                  try:
                      created_at = parse_date(m.get("date", ""))
                      session = honcho.session(f"meeting-{mid}")
                      metadata: dict[str, object] = {
                          "title": m.get("title", "Untitled"),
                          "date": m.get("date", ""),
                          "granola_meeting_id": mid,
                          "mode": mode,
                      }

                      if mode == "two_person" and them is not None:
                          them_source = them.email or them.name
                          them_peer_id = peer_id_from(them_source)
                          if them_peer_id not in seen_peers:
                              print(f"  New peer: {them_source} ({them_peer_id})")
                              seen_peers.add(them_peer_id)
                          import_two_person(honcho, session, me_peer_id, them_peer_id, turns, metadata, created_at)
                      else:
                          import_summary(honcho, session, me_peer_id, m, metadata, created_at)

                      results["imported"] += 1

                  except ValueError as e:
                      print(f"  -> FAILED: {e}")
                      results["failed"] += 1
                  except Exception as e:
                      print(f"  -> FAILED: {e}")
                      traceback.print_exc()
                      results["failed"] += 1

              # Done
              print("\n" + "=" * 60)
              print("  Transfer Complete!")
              print("=" * 60)
              print(f"\n  Imported: {results['imported']}")
              print(f"  Skipped:  {results['skipped']}")
              print(f"  Failed:   {results['failed']}")
              print("  Workspace: granola")
              print(f"  Peers: {sorted(seen_peers)}")

          except KeyboardInterrupt:
              print("\n\nAborted.")
              sys.exit(0)
          except Exception as e:
              print(f"\nTransfer failed: {e}")
              traceback.print_exc()
              sys.exit(1)


  if __name__ == "__main__":
      asyncio.run(main())
  ```
</Accordion>

## Next Steps

<CardGroup>
  <Card title="Design Patterns" icon="cubes" href="/v3/documentation/core-concepts/design-patterns">
    See how the Granola integration maps to common Honcho patterns.
  </Card>

  <Card title="GitHub Repository" icon="github" href="https://github.com/plastic-labs/honcho/tree/main/examples/granola">
    Source code and example script.
  </Card>
</CardGroup>


# Claude Code
Source: https://honcho.dev/docs/v3/guides/integrations/claude-code

Add AI-native memory to Claude Code

Give Claude Code long-term memory that survives context wipes, session restarts, and `ctrl+c`. Claude remembers what you're working on, your preferences, and what it was doing across all your projects.

## Quick Start

### Step 1: Get Your Honcho API Key

1. Go to **[app.honcho.dev](https://app.honcho.dev)**
2. Sign up or log in
3. Copy your API key (starts with `hch-`)

### Step 2: Set Environment Variables

Add these to your shell config (`~/.zshrc`, `~/.bashrc`, or `~/.profile`):

```bash theme={null}
# Required
export HONCHO_API_KEY="hch-your-api-key-here"

# Optional (defaults shown)
export HONCHO_PEER_NAME="$USER"           # Your name/identity
```

Then reload your shell:

```bash theme={null}
source ~/.zshrc  # or ~/.bashrc
```

### Step 3: Install the Plugin

<Note>
  This plugin requires [Bun](https://bun.sh). If you don't have it: `curl -fsSL https://bun.sh/install | bash`
</Note>

Open Claude Code and run:

```
/plugin marketplace add plastic-labs/claude-honcho
```

Then install:

```
/plugin install honcho@honcho
```

### Step 4: Restart Claude Code

```bash theme={null}
# Exit Claude Code (ctrl+c or /exit)
# Start it again
claude
```

**That's it!** You should see the Honcho pixel art and memory loading on startup.

### Step 5: (Optional) Kickstart with an Interview

```
/honcho:interview
```

Claude will interview you about your personal preferences to kickstart a representation of you. What it learns will be saved in Honcho and remembered forever. The interview is specific to the peer name you chose — it carries across different projects!

## What You Get

* **Persistent Memory** — Claude remembers your preferences, projects, and context across sessions
* **Survives Context Wipes** — Even when Claude's context window resets, memory persists
* **Git Awareness** — Detects branch switches, commits, and changes made outside Claude
* **Flexible Sessions** — Map sessions per directory, per git branch, or per chat instance
* **AI Self-Awareness** — Claude knows what it was working on, even after restarts
* **Cross-Tool Context** — Link workspaces across Claude Code, Cursor, and other hosts so context flows between tools
* **Team Support** — Multiple people can share a workspace and build context together
* **MCP Tools** — Search memory, query knowledge about you, and save insights

## Configuration

All configuration lives in a single global file at `~/.honcho/config.json`. You can edit it directly, use the `/honcho:config` skill interactively, or use the `set_config` MCP tool. Environment variables work for initial setup but the config file takes precedence once it exists.

```jsonc theme={null}
{
  // Required
  "apiKey": "hch-v2-...",

  // Identity
  "peerName": "alice",              // Your name (default: $USER)

  // Host-specific settings — each tool gets its own workspace and AI peer
  "hosts": {
    "claude_code": {
      "workspace": "claude_code",   // Workspace for Claude Code sessions
      "aiPeer": "claude",           // AI identity in this workspace
      "linkedHosts": ["cursor"]     // Read context from other hosts (optional)
    },
    "cursor": {
      "workspace": "cursor",
      "aiPeer": "cursor"
    }
  },

  // Session mapping
  "sessionStrategy": "per-directory", // "per-directory" | "git-branch" | "chat-instance"
  "sessionPeerPrefix": true,          // Prefix session names with peerName (default: true)

  // Message handling
  "saveMessages": true,
  "messageUpload": {
    "maxUserTokens": null,            // Truncate user messages (null = no limit)
    "maxAssistantTokens": null,       // Truncate assistant messages (null = no limit)
    "summarizeAssistant": false       // Summarize instead of sending full assistant text
  },

  // Context retrieval
  "contextRefresh": {
    "messageThreshold": 30,           // Refresh context every N messages
    "ttlSeconds": 300,                // Cache TTL for context
    "skipDialectic": false            // Skip dialectic chat() calls in user-prompt hook
  },

  // Endpoint
  "endpoint": {
    "environment": "production"       // "production" | "local"
    // or: "baseUrl": "http://your-server:8000/v3"
  },

  // Miscellaneous
  "localContext": { "maxEntries": 50 },
  "enabled": true,
  "logging": true,

  // Advanced: force all hosts to use the same workspace
  "globalOverride": false
}
```

### Session Strategies

Session strategy controls how Honcho maps your conversations to sessions:

| Strategy                  | Behavior                                                                            | Best for                                                  |
| ------------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------- |
| `per-directory` (default) | One session per project directory. Stable across restarts.                          | Most users — each project accumulates its own memory      |
| `git-branch`              | Session name includes the current git branch. Switching branches switches sessions. | Feature-branch workflows where context per branch matters |
| `chat-instance`           | Each Claude Code chat gets its own session. No continuity between restarts.         | Ephemeral usage or when you want a clean slate each time  |

Session names are prefixed with your `peerName` by default (e.g., `alice-my-project`). Set `sessionPeerPrefix: false` if you're the only user and want shorter names.

### Host-Aware Configuration

The plugin auto-detects which tool is running it (Claude Code, Cursor, etc.) and reads the matching block from `hosts`. Each host gets its own workspace and AI peer name, so data stays separated by default.

**Host detection priority:**

1. `HONCHO_HOST` env var (explicit override)
2. `cursor_version` in hook stdin (Cursor detected)
3. `CURSOR_PROJECT_DIR` env var (Cursor child process)
4. Default: `claude_code`

### Linking Hosts for Cross-Tool Context

If you use both Claude Code and Cursor, you can link them so context from one is readable in the other. Writes always stay in the current host's workspace — linking only adds read access.

```jsonc theme={null}
{
  "hosts": {
    "claude_code": {
      "workspace": "claude_code",
      "aiPeer": "claude",
      "linkedHosts": ["cursor"]  // Claude Code can read Cursor's context
    },
    "cursor": {
      "workspace": "cursor",
      "aiPeer": "cursor",
      "linkedHosts": ["claude_code"]  // Cursor can read Claude Code's context
    }
  }
}
```

Or use `/honcho:config` and select **Workspace > Linking** to set this up interactively.

### Global Override

If you want all hosts to share a single workspace (instead of per-host isolation), set `globalOverride: true` and a flat `workspace` field:

```jsonc theme={null}
{
  "globalOverride": true,
  "workspace": "shared",
  "hosts": {
    "claude_code": { "aiPeer": "claude" },
    "cursor": { "aiPeer": "cursor" }
  }
}
```

All tools will read and write to the `shared` workspace. Each tool still uses its own AI peer name.

## Building with Teammates

Multiple people can share context by pointing to the same workspace. Each person uses their own `peerName` as identity, and sessions are automatically prefixed with it to avoid collisions.

**Person A** (`~/.honcho/config.json`):

```json theme={null}
{
  "apiKey": "hch-v2-team-key...",
  "peerName": "alice",
  "hosts": {
    "claude_code": {
      "workspace": "team-acme",
      "aiPeer": "claude"
    }
  }
}
```

**Person B** (`~/.honcho/config.json`):

```json theme={null}
{
  "apiKey": "hch-v2-team-key...",
  "peerName": "bob",
  "hosts": {
    "claude_code": {
      "workspace": "team-acme",
      "aiPeer": "claude"
    }
  }
}
```

Both Alice and Bob write to the `team-acme` workspace. Their sessions are namespaced (e.g., `alice-my-project`, `bob-my-project`) so data doesn't collide, but Honcho's dialectic reasoning can draw on context from both users.

## Logging

The plugin logs activity to `~/.honcho/` and to Claude Code's verbose mode, so you can see exactly how Honcho is being used — what context is loaded at session start, what messages are saved, and what context is injected into Claude's prompts. Set `logging` to `false` in your config (or `HONCHO_LOGGING=false`) to disable file logging.

## MCP Tools

The plugin provides these tools via MCP:

| Tool                | Description                                     |
| ------------------- | ----------------------------------------------- |
| `search`            | Semantic search across session messages         |
| `chat`              | Query Honcho's knowledge about the user         |
| `create_conclusion` | Save insights about the user to memory          |
| `get_config`        | View current configuration and status           |
| `set_config`        | Change any configuration field programmatically |

## Skills (Slash Commands)

| Command             | Description                                                 |
| ------------------- | ----------------------------------------------------------- |
| `/honcho:status`    | Show current memory status and connection info              |
| `/honcho:config`    | Interactive configuration menu                              |
| `/honcho:setup`     | First-time setup — validate API key and create config       |
| `/honcho:interview` | Interview to capture stable, cross-project user preferences |

### The Interview

The `/honcho:interview` skill conducts a short interview to learn stable, cross-project aspects about you:

* **Communication style** — Concise answers, detailed explanations, or a mix
* **Tone** — Direct and professional or conversational
* **Structure** — Bullet points, step-by-step, or narrative
* **Technical depth** — Beginner, intermediate, or expert
* **Code quality focus** — Clarity, performance, tests, or minimal changes
* **Collaboration style** — Make changes directly, propose options, or ask first

Each answer is saved as a conclusion in Honcho memory and persists across all your projects.

## Environment Variables

Environment variables work for initial bootstrap (before a config file exists). Once `~/.honcho/config.json` is written, the config file takes precedence for host-specific fields like `workspace`.

| Variable               | Required | Default       | Description                                                       |
| ---------------------- | -------- | ------------- | ----------------------------------------------------------------- |
| `HONCHO_API_KEY`       | **Yes**  | —             | Your Honcho API key from [app.honcho.dev](https://app.honcho.dev) |
| `HONCHO_PEER_NAME`     | No       | `$USER`       | Your identity in the memory system                                |
| `HONCHO_WORKSPACE`     | No       | `claude_code` | Workspace name (used only when no config file exists)             |
| `HONCHO_AI_PEER`       | No       | `claude`      | AI peer name                                                      |
| `HONCHO_HOST`          | No       | auto-detected | Force host detection: `claude_code`, `cursor`, or `obsidian`      |
| `HONCHO_ENDPOINT`      | No       | `production`  | `production`, `local`, or a full URL                              |
| `HONCHO_ENABLED`       | No       | `true`        | Set to `false` to disable                                         |
| `HONCHO_SAVE_MESSAGES` | No       | `true`        | Set to `false` to stop saving messages                            |
| `HONCHO_LOGGING`       | No       | `true`        | Set to `false` to disable file logging to `~/.honcho/`            |

### Using a local Honcho instance

Via config file:

```json theme={null}
{ "endpoint": { "environment": "local" } }
```

Or via env var:

```bash theme={null}
export HONCHO_ENDPOINT="local"  # Uses http://localhost:8000/v3
```

***

## Using Honcho with Claude Desktop

You can also use Honcho with the Claude Desktop app via MCP. This lets Claude manage its own memory in the native desktop experience.

### Step 1: Get Your API Key

Get an API key from [app.honcho.dev](https://app.honcho.dev).

### Step 2: Configure Claude Desktop

<Note>
  This requires [Node.js](https://nodejs.org). Claude Desktop or Claude Code can help you install it!
</Note>

Navigate to Claude Desktop's custom MCP servers settings and add Honcho:

```json theme={null}
{
  "mcpServers": {
    "honcho": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.honcho.dev",
        "--header",
        "Authorization:${AUTH_HEADER}",
        "--header",
        "X-Honcho-User-Name:${USER_NAME}"
      ],
      "env": {
        "AUTH_HEADER": "Bearer <your-honcho-key>",
        "USER_NAME": "<your-name>"
      }
    }
  }
}
```

**Optional customization** — You can also set a custom assistant name and workspace ID:

```json theme={null}
{
  "mcpServers": {
    "honcho": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.honcho.dev",
        "--header",
        "Authorization:${AUTH_HEADER}",
        "--header",
        "X-Honcho-User-Name:${USER_NAME}",
        "--header",
        "X-Honcho-Assistant-Name:${ASSISTANT_NAME}",
        "--header",
        "X-Honcho-Workspace-ID:${WORKSPACE_ID}"
      ],
      "env": {
        "AUTH_HEADER": "Bearer <your-honcho-key>",
        "USER_NAME": "<your-name>",
        "ASSISTANT_NAME": "<your-assistant-name>",
        "WORKSPACE_ID": "<your-custom-workspace-id>"
      }
    }
  }
}
```

### Step 3: Restart Claude Desktop

Upon relaunch, Honcho should start and the tools will be available.

### Step 4: Add Instructions

The Desktop app doesn't allow system prompts directly, but you can create a project and paste [these instructions](https://raw.githubusercontent.com/plastic-labs/honcho/refs/heads/main/mcp/instructions.md) into the "Project Instructions" field.

Claude will then query for insights before responding and write your messages to storage!

***

## Next Steps

<CardGroup>
  <Card title="GitHub Repository" icon="github" href="https://github.com/plastic-labs/claude-honcho">
    Source code, issues, and README.
  </Card>

  <Card title="Honcho Architecture" icon="sitemap" href="../../documentation/core-concepts/architecture">
    Learn about peers, sessions, and dialectic reasoning.
  </Card>
</CardGroup>


# CrewAI
Source: https://honcho.dev/docs/v3/guides/integrations/crewai

Build AI agents with persistent memory using CrewAI and Honcho

Integrate Honcho with CrewAI to build agents that maintain memory across sessions. This guide uses CrewAI's unified `Memory` API with Honcho as a custom storage backend.

<Note>
  The full code is available on [GitHub](https://github.com/plastic-labs/honcho/tree/main/examples/crewai) with examples in [Python](https://github.com/plastic-labs/honcho/tree/main/examples/crewai/python/examples).
</Note>

## What We're Building

* **CrewAI** orchestrates agents, tasks, and memory recall.
* **Honcho** persists CrewAI memory records and exposes additional context, search, and reasoning tools.

<Note>
  CrewAI currently supports Python `>=3.10,<3.14`; use one of those interpreters when installing this integration.
</Note>

## Setup

Install the packages:

<CodeGroup>
  ```bash Python (uv) theme={null}
  uv add honcho-crewai crewai python-dotenv
  ```

  ```bash Python (pip) theme={null}
  pip install honcho-crewai crewai python-dotenv
  ```
</CodeGroup>

Set your model provider keys and Honcho configuration:

```bash theme={null}
OPENAI_API_KEY=your_openai_key
HONCHO_API_KEY=your_honcho_key
HONCHO_WORKSPACE_ID=crewai-demo
```

For local development, initialize the Honcho client with `environment="local"`.

## CrewAI Memory Storage

`HonchoMemoryStorage` implements CrewAI's current `StorageBackend` protocol and can be passed directly to `Memory(storage=...)`.

```python theme={null}
from crewai import Memory
from honcho import Honcho
from honcho_crewai import HonchoMemoryStorage

honcho = Honcho(workspace_id="crewai-demo")
storage = HonchoMemoryStorage(
    peer_id="user-123",
    session_id="session-123",
    honcho_client=honcho,
)
memory = Memory(storage=storage)
```

CrewAI embeds memory records before storing them. The Honcho backend stores those records as Honcho messages, keeps CrewAI metadata in message metadata, and performs vector search over the stored embeddings.

```python theme={null}
memory.remember(
    "The user is learning Python and wants to build web applications.",
    scope="/users/user-123",
    categories=["preferences"],
    metadata={"source": "onboarding"},
)
```

Use the memory instance with a crew:

```python Python theme={null}
from crewai import Agent, Crew, Process, Task

agent = Agent(
    role="Programming Mentor",
    goal="Help users learn programming by remembering their interests and progress",
    backstory="You are a patient programming mentor.",
)

task = Task(
    description="Suggest a Python web project that matches the user's interests.",
    expected_output="A specific project suggestion with a brief explanation",
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    process=Process.sequential,
    memory=memory,
    verbose=True,
)

result = crew.kickoff()
print(result.raw)
```

<Note>
  `HonchoStorage` is still available as a compatibility adapter for older CrewAI `ExternalMemory` integrations, but new projects should use `HonchoMemoryStorage`.
</Note>

## CrewAI Tool Integration

Honcho also provides tools that let agents explicitly retrieve memory:

* **`HonchoGetContextTool`** retrieves session context with token limits.
* **`HonchoDialecticTool`** queries Honcho's representation of a peer.
* **`HonchoSearchTool`** performs semantic search over session messages.

```python Python theme={null}
from crewai import Agent, Crew, Process, Task
from honcho import Honcho
from honcho_crewai import (
    HonchoDialecticTool,
    HonchoGetContextTool,
    HonchoSearchTool,
)

honcho = Honcho(workspace_id="crewai-demo")
user_id = "demo-user"
session_id = "tools-demo-session"

user = honcho.peer(user_id)
session = honcho.session(session_id)

for message in [
    "I'm planning a trip to Japan in March",
    "I love authentic local cuisine, especially ramen and sushi",
    "My budget is around $3000 for a 10-day trip",
]:
    session.add_messages([user.message(message)])

context_tool = HonchoGetContextTool(
    honcho=honcho,
    session_id=session_id,
    peer_id=user_id,
)
dialectic_tool = HonchoDialecticTool(
    honcho=honcho,
    session_id=session_id,
    peer_id=user_id,
)
search_tool = HonchoSearchTool(honcho=honcho, session_id=session_id)

travel_agent = Agent(
    role="Travel Planning Specialist",
    goal="Create personalized travel recommendations using memory tools",
    backstory="You are an expert travel planner with access to memory tools.",
    tools=[context_tool, dialectic_tool, search_tool],
    verbose=True,
    allow_delegation=False,
)

task = Task(
    description="Create a personalized 3-day Tokyo itinerary using the memory tools.",
    expected_output="A 3-day Tokyo itinerary with activities, restaurants, and budget notes",
    agent=travel_agent,
)

crew = Crew(
    agents=[travel_agent],
    tasks=[task],
    process=Process.sequential,
    verbose=True,
)

crew.kickoff()
```

## When To Use Each

Use `HonchoMemoryStorage` when you want CrewAI to handle recall automatically through the unified memory system.

Use the Honcho tools when the agent should decide when and how to query memory, search messages, or ask Honcho for a peer-level representation.

You can combine both: unified memory for baseline context, tools for targeted retrieval. See the [hybrid memory example](https://github.com/plastic-labs/honcho/blob/main/examples/crewai/python/examples/hybrid_memory_example.py) for a complete implementation.

## Related Resources

<CardGroup>
  <Card title="Honcho Architecture" icon="sitemap" href="/v3/documentation/core-concepts/architecture">
    Understand Honcho's peer-based model and core primitives
  </Card>

  <Card title="Get Context" icon="messages" href="/v3/documentation/features/get-context">
    Learn about retrieving and formatting conversation context
  </Card>

  <Card title="Chat API" icon="brain" href="/v3/documentation/features/chat">
    Query peer representations for deeper understanding
  </Card>

  <Card title="LangGraph Integration" icon="diagram-project" href="/v3/guides/integrations/langgraph">
    Build stateful agents with LangGraph and Honcho
  </Card>
</CardGroup>


# Hermes Agent + Honcho
Source: https://honcho.dev/docs/v3/guides/integrations/hermes

How Hermes Agent uses Honcho for persistent cross-session memory and user modeling

[Hermes Agent](https://github.com/NousResearch/hermes-agent) is an open-source AI agent from [Nous Research](https://nousresearch.com) with tool-calling, terminal access, a skills system, and multi-platform deployment (Telegram, Discord, Slack, WhatsApp). Honcho gives Hermes persistent cross-session memory and user modeling.

For setup, configuration, and CLI commands, see the [Hermes Agent Honcho docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/honcho).

## What Honcho provides

Honcho acts as a long-term memory and user-model layer alongside Hermes' built-in memory files (`MEMORY.md` and `USER.md`).

It gives Hermes three capabilities:

1. **Prompt-time context injection** -- durable context about a user loaded into the prompt before generating a response.
2. **Cross-session continuity** -- recall of stable preferences, project history, and working context across conversations.
3. **Durable writeback** -- stable facts learned during a conversation stored back for future turns.

These sit alongside Hermes' local session history. Session history remembers the current conversation. Honcho remembers what should still matter later.

## Dual-peer architecture

Both the user and the AI agent have peer representations in Honcho:

* **User peer**: observed from user messages. Learns preferences, goals, communication style.
* **AI peer**: observed from assistant messages. Builds the agent's knowledge representation.

Both representations are injected into the system prompt, giving Hermes awareness of both who it's talking to and what it knows.

## Available tools

Hermes exposes four Honcho tools to the agent:

| Tool              | What it does                                                                                        |
| ----------------- | --------------------------------------------------------------------------------------------------- |
| `honcho_profile`  | Fast peer card retrieval (no LLM). Returns curated key facts about the user.                        |
| `honcho_search`   | Semantic search over memory. Returns raw excerpts ranked by relevance.                              |
| `honcho_context`  | Dialectic Q\&A powered by Honcho's LLM. Synthesizes answers from conversation history.              |
| `honcho_conclude` | Writes durable facts to Honcho when the user states preferences, corrections, or important context. |

## Running Honcho locally with Hermes

Follow the [Self-Hosting Guide](/docs/v3/contributing/self-hosting) to get Honcho running locally. Once it's up, point Hermes at your instance:

```bash theme={null}
hermes memory setup  # select "honcho", enter http://localhost:8000 as the base URL
```

Or manually create/edit the config file (checked in order: `$HERMES_HOME/honcho.json` > `~/.hermes/honcho.json` > `~/.honcho/config.json`):

```json theme={null}
{
  "baseUrl": "http://localhost:8000",
  "hosts": {
    "hermes": {
      "enabled": true,
      "aiPeer": "hermes",
      "peerName": "your-name",
      "workspace": "hermes"
    }
  }
}
```

For the full list of config fields (`recallMode`, `writeFrequency`, `sessionStrategy`, `dialecticReasoningLevel`, etc.), see the [Hermes memory provider docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers#honcho).

<Info>
  **Community quick-start**: [elkimek/honcho-self-hosted](https://github.com/elkimek/honcho-self-hosted) provides a one-command installer with pre-configured model tiers and Hermes Agent integration.
</Info>

## Verifying the integration

### 1. Check status

```bash theme={null}
hermes memory status
```

This should show Honcho as the active memory provider with your base URL.

### 2. Store a fact and recall it across sessions

In one conversation, tell Hermes something specific:

```text theme={null}
My favorite programming language is Rust and I always use dark mode.
```

Start a **new session** (different thread, new CLI invocation, or a different platform). Ask:

```text theme={null}
What do you know about my preferences?
```

If Hermes mentions Rust and dark mode without being told again, cross-session memory is working. The deriver processed your messages, extracted observations, and the dialectic recalled them.

### 3. Test tool calling directly

Ask Hermes to use a specific Honcho tool:

```text theme={null}
Use your honcho_search tool to find anything you know about me.
```

If Hermes calls the tool and returns results, the full tool pipeline (API connection, vector search, embedding) is functional.

## Configuration options

| Field                     | Default         | Description                                                                   |
| ------------------------- | --------------- | ----------------------------------------------------------------------------- |
| `recallMode`              | `hybrid`        | `hybrid` (auto-inject + tools), `context` (inject only), `tools` (tools only) |
| `writeFrequency`          | `async`         | `async`, `turn`, `session`, or integer N                                      |
| `sessionStrategy`         | `per-directory` | `per-directory`, `per-repo`, `per-session`, `global`                          |
| `dialecticReasoningLevel` | `low`           | `minimal`, `low`, `medium`, `high`, `max`                                     |
| `dialecticDynamic`        | `true`          | Auto-bump reasoning level by query complexity                                 |
| `messageMaxChars`         | `25000`         | Max chars per message (chunked if exceeded)                                   |

## Next steps

<CardGroup>
  <Card title="Hermes Agent Honcho Docs" icon="book" href="https://hermes-agent.nousresearch.com/docs/user-guide/features/honcho">
    Setup, configuration, CLI commands, and all config options.
  </Card>

  <Card title="Hermes Agent Source" icon="github" href="https://github.com/NousResearch/hermes-agent">
    Source code, installation, and full documentation.
  </Card>

  <Card title="Honcho Architecture" icon="sitemap" href="/v3/documentation/core-concepts/architecture">
    Peers, sessions, and how reasoning works.
  </Card>

  <Card title="Self-Hosting Guide" icon="server" href="/v3/contributing/self-hosting">
    Full local environment setup, provider configuration, and troubleshooting.
  </Card>
</CardGroup>


# LangGraph
Source: https://honcho.dev/docs/v3/guides/integrations/langgraph

Build a stateful conversational AI agent with LangGraph and Honcho

Integrate Honcho with LangGraph to build a conversational AI agent that maintains memory across sessions. This guide shows you how to use Honcho's memory layer with LangGraph's orchestration.

<Note>
  The full code is available on [GitHub](https://github.com/plastic-labs/honcho/tree/main/examples/langgraph) with examples in both [Python](https://github.com/plastic-labs/honcho/blob/main/examples/langgraph/python/main.py) and [TypeScript](https://github.com/plastic-labs/honcho/blob/main/examples/langgraph/typescript/main.ts)
</Note>

## What We're Building

We'll create a conversational agent that remembers and reasons over past exchanges with the user. Here's how the pieces fit together:

* **LangGraph** orchestrates the conversation flow
* **Honcho** stores messages and retrieves relevant context
* **Your LLM** generates responses using Honcho's formatted context

The key benefit: You don't manually manage conversation history, token limits, or message formatting. Honcho handles memory so you can focus on your agent's logic.

<Note>
  This tutorial demonstrates a simple linear conversation flow to show
  how Honcho integrates with LangGraph. For production applications,
  you'll likely want to add LangGraph features like conditional routing,
  tool calling, and multi-agent orchestration.
</Note>

## Setup

Install required packages:

<CodeGroup>
  ```bash Python (uv) theme={null}
  uv add honcho-ai langgraph langchain-core openai python-dotenv
  ```

  ```bash Python (pip) theme={null}
  pip install honcho-ai langgraph langchain-core openai python-dotenv
  ```

  ```bash TypeScript (npm) theme={null}
  npm install @honcho-ai/sdk @langchain/langgraph openai dotenv
  ```

  ```bash TypeScript (yarn) theme={null}
  yarn add @honcho-ai/sdk @langchain/langgraph openai dotenv
  ```

  ```bash TypeScript (pnpm) theme={null}
  pnpm add @honcho-ai/sdk @langchain/langgraph openai dotenv
  ```
</CodeGroup>

This tutorial uses OpenAI, but Honcho works with any LLM provider. Create a `.env` file with your API keys:

```bash theme={null}
OPENAI_API_KEY=your_openai_key
```

<Note>
  This tutorial uses the Honcho demo server at [https://demo.honcho.dev](https://demo.honcho.dev) which runs a small instance of Honcho on the latest version. For production, get your Honcho API key at [app.honcho.dev](https://app.honcho.dev). For local development, use `environment="local"`.
</Note>

## Initialize Clients

<CodeGroup>
  ```python Python theme={null}
  import os
  from dotenv import load_dotenv
  from typing_extensions import TypedDict
  from honcho import Honcho, Peer, Session
  from openai import OpenAI
  from langgraph.graph import StateGraph, START, END

  load_dotenv()

  # Initialize Honcho
  honcho = Honcho()

  # Initialize OpenAI
  llm = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
  ```

  ```typescript TypeScript theme={null}
  import * as dotenv from "dotenv";
  import { Honcho, Peer, Session } from "@honcho-ai/sdk";
  import OpenAI from "openai";
  import { Annotation } from "@langchain/langgraph";
  import { StateGraph, START, END } from "@langchain/langgraph";
  import * as readline from "readline/promises";

  dotenv.config();

  // Initialize Honcho
  const honcho = new Honcho({});

  // Initialize OpenAI
  const llm = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
  });
  ```
</CodeGroup>

## Define LangGraph State

Define your state schema to pass data through the graph. The state stores Honcho objects directly along with the current user message and assistant response.

<Note>
  Before proceeding, it's important to understand Honcho's core concepts (`Peers` and `Sessions`). Review the [Honcho Architecture](/docs/v3/documentation/core-concepts/architecture) to familiarize yourself with these primitives.
</Note>

<CodeGroup>
  ```python Python theme={null}
  class State(TypedDict):
      user_message: str
      assistant_response: str
      user: Peer
      assistant: Peer
      session: Session
  ```

  ```typescript TypeScript theme={null}
  const StateAnnotation = Annotation.Root({
    userMessage: Annotation<string>(),
    assistantResponse: Annotation<string>(),
    user: Annotation<Peer>(),
    assistant: Annotation<Peer>(),
    session: Annotation<Session>(),
  });

  type State = typeof StateAnnotation.State;
  ```
</CodeGroup>

## Build the LangGraph

Define your chatbot logic, using Honcho to retrieve conversation context. This function demonstrates how Honcho can store messages, retrieve context, and generate responses.

<CodeGroup>
  ```python Python theme={null}
  def chatbot(state: State):
      user_message = state["user_message"]

      # Get objects from state
      user = state["user"]
      assistant = state["assistant"]
      session = state["session"]

      # Step 1: Store the user's message in the session
      # This adds it to Honcho's memory for future context retrieval
      session.add_messages([user.message(user_message)])

      # Step 2: Get context in OpenAI format with token limit
      # context() retrieves relevant conversation history
      # tokens=2000 limits the context to 2000 tokens to manage costs and fit within model limits
      # to_openai() converts it to the format expected by OpenAI's API
      messages = session.context(tokens=2000).to_openai(assistant=assistant)

      # Step 3: Generate response using the context
      response = llm.chat.completions.create(
          model="gpt-5.1",
          messages=messages
      )
      assistant_response = response.choices[0].message.content

      # Step 4: Store assistant response in Honcho for future context
      session.add_messages([assistant.message(assistant_response)])

      return {"assistant_response": assistant_response}
  ```

  ```typescript TypeScript theme={null}
  async function chatbot(state: State) {
    const userMessage = state.userMessage;

    // Get objects from state
    const user = state.user;
    const assistant = state.assistant;
    const session = state.session;

    // Step 1: Store the user's message in the session
    // This adds it to Honcho's memory for future context retrieval
    await session.addMessages([user.message(userMessage)]);

    // Step 2: Get context in OpenAI format with token limit
    // context() retrieves relevant conversation history
    // tokens: 2000 limits the context to 2000 tokens to manage costs and fit within model limits
    // toOpenAI() converts it to the format expected by OpenAI's API
    const messages = (await session.context({ tokens: 2000 })).toOpenAI(assistant);

    // Step 3: Generate response using the context
    const response = await llm.chat.completions.create({
      model: "gpt-5.1",
      messages: messages
    });
    const assistantResponse = response.choices[0].message.content!;

    // Step 4: Store assistant response for future context
    await session.addMessages([assistant.message(assistantResponse)]);

    return { assistantResponse: assistantResponse };
  }
  ```
</CodeGroup>

Now let's build the LangGraph:

<CodeGroup>
  ```python Python theme={null}
  graph = StateGraph(State) \
      .add_node("chatbot", chatbot) \
      .add_edge(START, "chatbot") \
      .add_edge("chatbot", END) \
      .compile()
  ```

  ```typescript TypeScript theme={null}
  const graph = new StateGraph(StateAnnotation)
    .addNode("chatbot", chatbot)
    .addEdge(START, "chatbot")
    .addEdge("chatbot", END)
    .compile();
  ```
</CodeGroup>

### Understanding context()

The [`context()`](/docs/v3/documentation/features/get-context) method retrieves comprehensive conversation context and formats it for your LLM. It automatically:

* **Manages conversation history** - Tracks all messages and determines what's relevant
* **Respects token limits** - Stays within context window constraints without manual counting
* **Handles long conversations** - Combines recent detailed messages with summaries of older exchanges
* **Provides `peer` understanding** - Includes representations and `peer` cards when requested

The `SessionContext` object always includes fields for messages, summaries, `peer` representations, and `peer` cards. By default, only `messages` and `summary` are populated. To populate peer-specific context, pass a `peer_target` parameter:

**Using `peer_target` for Context:**

* **Without `peer_perspective`**: Returns Honcho's omniscient view of `peer_target` (all conclusions and context)
* **With `peer_perspective`**: Returns what `peer_perspective` knows about `peer_target` (perspective-based conclusions and context)

That's it. Call `session.context().to_openai(assistant)` and you get properly formatted context tailored for your assistant.

<Tip>
  **Adding System Prompts:** Since `context()` returns conversation messages, you can easily prepend custom system instructions. Just add your system prompt to the beginning of the messages array before sending it to your LLM: `[{"role": "system", "content": "..."}, ...context_messages]`.
</Tip>

<Note>
  For more details on all available parameters, see [`context() documentation`](/docs/v3/documentation/features/get-context)
</Note>

## Chat Loop

Now we'll create the main conversation function. To simplify logic, we initialize Honcho objects once per conversation and pass them through the LangGraph state.

The `run_conversation_turn` function initializes a Honcho `Session` and `Peer` objects, passes them to the LangGraph, and returns the assistant's response. By calling it repeatedly with the same `user_id` and in the same session, the chat builds context over time.

<Note>
  **Production Usage:** Honcho accepts any nanoid-compatible string for `user_id` and `session_id`. You can use IDs directly from your authentication system (Auth0, Firebase, Clerk, etc.) and session management without modification.

  This tutorial uses hardcoded values for simplicity.
</Note>

<CodeGroup>
  ```python Python theme={null}
  def run_conversation_turn(user_id: str, user_input: str, session_id: str | None = None):
      if not session_id:
          session_id = f"session_{user_id}"

      # Initialize Honcho objects
      user = honcho.peer(user_id)
      assistant = honcho.peer("assistant")
      session = honcho.session(session_id)

      result = graph.invoke({
          "user_message": user_input,
          "user": user,
          "assistant": assistant,
          "session": session
      })

      return result["assistant_response"]

  if __name__ == "__main__":
    print("Welcome to the AI Assistant! How can I help you today?")
    user_id = "test-user-123"
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            break
        response = run_conversation_turn(user_id, user_input)
        print(f"Assistant: {response}\n")
  ```

  ```typescript TypeScript theme={null}
  async function runConversationTurn(
    userId: string,
    userInput: string,
    sessionId?: string
  ): Promise<string> {
    if (!sessionId) {
      sessionId = `session_${userId}`;
    }

    // Initialize Honcho objects
    const user = await honcho.peer(userId);
    const assistant = await honcho.peer("assistant");
    const session = await honcho.session(sessionId);

    const result = await graph.invoke({
      userMessage: userInput,
      user: user,
      assistant: assistant,
      session: session,
    });

    return result.assistantResponse;
  }

  // Interactive chat loop
  async function main() {
    console.log("Welcome to the AI Assistant! How can I help you today?");
    const userId = "test-user-123";

    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    while (true) {
      const userInput = await rl.question("You: ");
      if (userInput.toLowerCase() === "quit" || userInput.toLowerCase() === "exit") {
        rl.close();
        break;
      }
      const response = await runConversationTurn(userId, userInput);
      console.log(`Assistant: ${response}\n`);
    }
  }

  main();
  ```
</CodeGroup>

## Next Steps

Now that you have a working LangGraph integration with Honcho, you can:

* **Create custom [LangChain tools](https://docs.langchain.com/oss/python/langchain/tools#customize-tool-properties) for your agent** - to fully utilize Honcho's memory & context management features
* **Build a multi-agent LangGraph** where each agent is a Honcho `Peer` with its own memory

## Related Resources

<CardGroup>
  <Card title="Get Context" icon="messages" href="/v3/documentation/features/get-context">
    Learn more about retrieving and formatting conversation context
  </Card>

  <Card title="MCP Integration" icon="star-of-life" href="/v3/guides/integrations/mcp">
    Use Honcho in Claude Desktop with MCP
  </Card>
</CardGroup>


# Model Context Protocol (MCP)
Source: https://honcho.dev/docs/v3/guides/integrations/mcp

Give any AI tool persistent memory with the Honcho MCP server

The Honcho MCP server gives any MCP-compatible AI tool persistent memory and personalization. Connect it once and your AI assistant learns who you are, remembers your preferences, and gets better over time — across every conversation.

**Server URL:** `https://mcp.honcho.dev`

<Note>
  You'll need an API key from [app.honcho.dev](https://app.honcho.dev) to use the hosted MCP server.
</Note>

## Client Setup

Pick your client below and add the config. After adding, **restart the client fully** for changes to take effect.

### Claude Desktop

<Tabs>
  <Tab title="macOS">
    Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:
  </Tab>

  <Tab title="Windows">
    Edit `%APPDATA%\Claude\claude_desktop_config.json`:
  </Tab>
</Tabs>

```json theme={null}
{
  "mcpServers": {
    "honcho": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.honcho.dev",
        "--header",
        "Authorization:${AUTH_HEADER}",
        "--header",
        "X-Honcho-User-Name:${USER_NAME}"
      ],
      "env": {
        "AUTH_HEADER": "Bearer hch-your-key-here",
        "USER_NAME": "YourName"
      }
    }
  }
}
```

<Tip>
  After saving, fully quit and relaunch Claude Desktop. The Honcho tools should appear in the tool picker.
</Tip>

For best results, create a project and paste these [instructions](https://raw.githubusercontent.com/plastic-labs/honcho/refs/heads/main/mcp/instructions.md) into the "Project Instructions" field so Claude knows how to use the memory tools.

### Claude Code

```bash theme={null}
claude mcp add honcho \
  --transport http \
  --url "https://mcp.honcho.dev" \
  --header "Authorization: Bearer hch-your-key-here" \
  --header "X-Honcho-User-Name: YourName"
```

Or if you prefer the [Claude Code Honcho plugin](/docs/v3/guides/integrations/claudecode) for a deeper integration with persistent memory, git awareness, and agent skills:

```bash theme={null}
/plugin marketplace add plastic-labs/claude-honcho
```

### Codex

Add to `~/.codex/config.toml`:

```toml theme={null}
[mcp_servers.honcho]
command = "npx"
args = [
  "mcp-remote",
  "https://mcp.honcho.dev",
  "--header",
  "Authorization:Bearer hch-your-key-here",
  "--header",
  "X-Honcho-User-Name:YourName"
]
```

<Note>
  Codex only supports stdio transport, so it uses `mcp-remote` as a bridge. Restart both the Codex CLI and VS Code extension after editing.
</Note>

### Cursor

Cursor supports MCP servers natively via HTTP. Add to your global config at `~/.cursor/mcp.json` or per-project at `.cursor/mcp.json`:

```json theme={null}
{
  "mcpServers": {
    "honcho": {
      "url": "https://mcp.honcho.dev",
      "headers": {
        "Authorization": "Bearer hch-your-key-here",
        "X-Honcho-User-Name": "YourName"
      }
    }
  }
}
```

Alternatively, go to **Cursor Settings → MCP** and add a new HTTP server with the URL and headers above.

### Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json theme={null}
{
  "mcpServers": {
    "honcho": {
      "serverUrl": "https://mcp.honcho.dev",
      "headers": {
        "Authorization": "Bearer hch-your-key-here",
        "X-Honcho-User-Name": "YourName"
      }
    }
  }
}
```

<Note>
  Windsurf uses `serverUrl` instead of `url`.
</Note>

### VS Code (Copilot Chat)

Add to your workspace `.vscode/mcp.json`:

```json theme={null}
{
  "servers": {
    "honcho": {
      "type": "http",
      "url": "https://mcp.honcho.dev",
      "headers": {
        "Authorization": "Bearer hch-your-key-here",
        "X-Honcho-User-Name": "YourName"
      }
    }
  }
}
```

Or add to your User Settings JSON (`Cmd+Shift+P` → "Preferences: Open User Settings (JSON)"):

```json theme={null}
{
  "mcp": {
    "servers": {
      "honcho": {
        "type": "http",
        "url": "https://mcp.honcho.dev",
        "headers": {
          "Authorization": "Bearer hch-your-key-here",
          "X-Honcho-User-Name": "YourName"
        }
      }
    }
  }
}
```

### Cline

Cline supports remote MCP servers natively. Open Cline's MCP settings at:

<Tabs>
  <Tab title="macOS">
    `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
  </Tab>

  <Tab title="Windows">
    `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
  </Tab>
</Tabs>

```json theme={null}
{
  "mcpServers": {
    "honcho": {
      "url": "https://mcp.honcho.dev",
      "headers": {
        "Authorization": "Bearer hch-your-key-here",
        "X-Honcho-User-Name": "YourName"
      }
    }
  }
}
```

Or add it via the Cline sidebar: click the MCP Servers icon → **Configure** → **Remote Servers**.

### Zed

Add to `~/.config/zed/settings.json`:

```json theme={null}
{
  "context_servers": {
    "honcho": {
      "url": "https://mcp.honcho.dev",
      "headers": {
        "Authorization": "Bearer hch-your-key-here",
        "X-Honcho-User-Name": "YourName"
      }
    }
  }
}
```

<Note>
  Zed uses `context_servers` instead of `mcpServers`. Native HTTP support requires Zed v0.214.5 or later.
</Note>

### Goose

[Goose](https://goose-docs.ai/) supports remote MCP servers natively over Streamable HTTP.

The easiest way is to run `goose configure`, choose **Add Extension → Remote Extension (Streamable HTTP)**, and enter the name `honcho`, the URI `https://mcp.honcho.dev`, and the headers `Authorization: Bearer hch-your-key-here` and `X-Honcho-User-Name: YourName`.

Or edit your `config.yaml` directly (on Linux, `~/.config/goose/config.yaml`):

```yaml theme={null}
extensions:
  honcho:
    enabled: true
    type: streamable_http
    name: honcho
    description: Honcho persistent memory & personalization
    uri: https://mcp.honcho.dev
    headers:
      Authorization: "Bearer hch-your-key-here"
      X-Honcho-User-Name: "YourName"
    timeout: 60
```

<Tip>
  To teach Goose the recommended memory flow, save the [instructions](https://raw.githubusercontent.com/plastic-labs/honcho/refs/heads/main/mcp/instructions.md) into a `.goosehints` file in your Goose config directory (or a project root). This is Goose's equivalent of Claude Desktop's "Project Instructions". Not sure of your config path? Run `goose info`.
</Tip>

***

## Optional Configuration

You can customize the assistant name and workspace ID by adding extra headers. Both are optional.

| Header                    | Default       | Description                 |
| ------------------------- | ------------- | --------------------------- |
| `Authorization`           | *required*    | `Bearer hch-your-key-here`  |
| `X-Honcho-User-Name`      | *required*    | What the AI should call you |
| `X-Honcho-Assistant-Name` | `"Assistant"` | Name for the AI peer        |
| `X-Honcho-Workspace-ID`   | `"default"`   | Isolate memory per project  |

Example with all headers (Claude Desktop format):

```json theme={null}
{
  "mcpServers": {
    "honcho": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.honcho.dev",
        "--header",
        "Authorization:${AUTH_HEADER}",
        "--header",
        "X-Honcho-User-Name:${USER_NAME}",
        "--header",
        "X-Honcho-Assistant-Name:${ASSISTANT_NAME}",
        "--header",
        "X-Honcho-Workspace-ID:${WORKSPACE_ID}"
      ],
      "env": {
        "AUTH_HEADER": "Bearer hch-your-key-here",
        "USER_NAME": "YourName",
        "ASSISTANT_NAME": "Claude",
        "WORKSPACE_ID": "my-project"
      }
    }
  }
}
```

***

## Available Tools

The recommended flow for a standard conversation uses `create_session` + `add_messages_to_session` + `chat`. See the [full instructions](https://raw.githubusercontent.com/plastic-labs/honcho/refs/heads/main/mcp/instructions.md) for a complete walkthrough.

**Workspace** — `inspect_workspace`, `list_workspaces`, `search`, `get_metadata`, `set_metadata`

**Peers** — `create_peer`, `list_peers`, `chat`, `get_peer_card`, `set_peer_card`, `get_peer_context`, `get_representation`

**Sessions** — `create_session`, `list_sessions`, `delete_session`, `clone_session`, `add_peers_to_session`, `remove_peers_from_session`, `get_session_peers`, `inspect_session`, `add_messages_to_session`, `get_session_messages`, `get_session_message`, `get_session_context`

**Conclusions** — `list_conclusions`, `query_conclusions`, `create_conclusions`, `delete_conclusion`

**System** — `schedule_dream`, `get_queue_status`

***

## Verify It Works

After setup, try asking your AI assistant:

> "What do you know about me?"

On the first conversation there won't be much — but after a few exchanges, Honcho's background reasoning will start building a representation of you. Ask again after a couple of conversations and you'll see the difference.

***

## Troubleshooting

| Problem                             | Fix                                                                                          |
| ----------------------------------- | -------------------------------------------------------------------------------------------- |
| Tools don't show up                 | Make sure you fully restarted the client after adding the config.                            |
| Authorization errors                | Check your API key at [app.honcho.dev](https://app.honcho.dev). It should start with `hch-`. |
| `npx` not found                     | Install Node.js — your AI assistant can help with this.                                      |
| "No personalization insights found" | Normal for new users. Honcho needs a few conversations to build context.                     |
| Connection timeouts                 | Check that `https://mcp.honcho.dev` is accessible from your network.                         |

Need help? Join us on [Discord](https://discord.gg/honcho) or open an issue on [GitHub](https://github.com/plastic-labs/honcho/tree/main/mcp).


# n8n
Source: https://honcho.dev/docs/v3/guides/integrations/n8n

Connect Honcho to your n8n workflows to build intelligent automation workflows and agents that leverage persistent memory across sessions.

## Quick Start

### Prerequisites

* n8n instance (self-hosted or cloud)
* Honcho API key ([get one here](https://app.honcho.dev))
* Basic understanding of n8n workflows
* Basic understanding of [Honcho architecture](/docs/v3/documentation/core-concepts/architecture). Specifically **workspaces**, **sessions**, **peers**, and **messages**.

### Before You Start

**This integration uses HTTP Request nodes.** There's no native Honcho node for n8n yet. While this requires more setup, it gives you full control over the API and works with any n8n version.

**This tutorial is instructional, not production-ready.** We load a single Gmail message with hardcoded IDs to demonstrate the concepts clearly. See [Next Steps](#next-steps) for handling multiple messages and dynamic configurations.

**Why Honcho over n8n's built-in memory?** n8n's "memory" nodes are vector databases for RAG-style retrieval. Honcho offers richer context and reasoning—it builds understanding of users over time, not just similarity search. [Learn more](https://blog.plasticlabs.ai/blog/Memory-as-Reasoning).

### Setting Up the HTTP Request Node

The Honcho integration in n8n uses the HTTP Request node to interact with the Honcho API. Here's how to configure it:

1. Add an **HTTP Request** node to your workflow (Core > HTTP Request)

<div>
  <Frame>
    <img alt="Adding HTTP Request node from Core nodes" />
  </Frame>
</div>

2. Set the **Method** based on your operation (typically `POST` for creating resources, `GET` for retrieving)

3. Set the **URL** to the appropriate Honcho API endpoint. For example, create workspace is `https://api.honcho.dev/v3/workspaces`

4. For authentication, select **Generic Credential Type** and then **Bearer Auth**

5. Click **Create New Credential** and paste your Honcho API key in the Bearer Token field

<div>
  <Frame>
    <img alt="Bearer Auth credential setup in n8n" />
  </Frame>
</div>

6. Check **Send Body** and select **JSON** as the Body Content Type when creating resources

## Step-by-Step Tutorial

We'll build a workflow that ingests Gmail emails into Honcho, then uses that memory to power a conversational AI chatbot.

The workflow has two parts (separated by sticky notes in the canvas):

1. **Data Ingestion**: Manual trigger → Workspace → Session → Gmail → Extract Peers → Create Peers → Add to Session → Create Messages

2. **AI Chat Interface**: Chat Trigger → Agent (with LLM and Honcho tools)

The Agent uses Honcho's `context()` endpoint to retrieve relevant information about email conversations, enabling contextual conversations about your email data.

<img alt="Complete workflow overview showing both data ingestion and chat sections" />

### Part 1: Loading Email Data into Honcho

These nodes handle the initial setup and data ingestion:

<Tip>
  **Pro Tip: Copy from API Playground**

  The fastest way to configure any Honcho endpoint is to copy the curl command directly from the [app.honcho.dev](https://app.honcho.dev) API playground:

  1. Navigate to the endpoint you want to use in the API playground
  2. Fill in your parameters, verify the results and click **Copy as cURL**
  3. Then in n8n use the **import cURL** button to directly import the request (be sure to verify the bearer token imported correctly)
</Tip>

#### Step 1: Manual Trigger

Start with a **Manual Trigger** node to execute the workflow on demand. This is useful for initial setup and testing before automating with a Gmail trigger.

#### Step 2: Get or Create Workspace

1. Add an **HTTP Request** node
2. **Method**: `POST`
3. **URL**: `https://api.honcho.dev/v3/workspaces`
4. **Body** (JSON): `{ "id": "email-test", "metadata": {} }`

<Tip>
  **Verify Your Data in Honcho**
  As you build the data ingestion workflow, verify everything is created correctly in your [Honcho instance](https://app.honcho.dev/).
</Tip>

#### Step 3: Get or Create Session

1. Add another **HTTP Request** node
2. **Method**: `POST`
3. **URL**: `https://api.honcho.dev/v3/workspaces/{{ $('Get or Create Workspace').item.json.id }}/sessions`
4. **Body** (JSON): `{ "id": "new_session" }`

#### Step 4: Get Gmail Message

1. Add a **Gmail** node
2. **Operation**: Get
3. **Message ID**: Your target message ID (a string of letters & numbers)
4. Configure your Gmail OAuth2 credentials

<Note>
  **Finding the Gmail Message ID**
  The easiest way to find a Gmail message ID is to use n8n's Gmail Get Many operation. Temporarily add it, set the limit to 1, and execute. Use the message ID in the output for the message ID field.

  In this tutorial, we load in only a single message to demonstrate the workflow.
</Note>

#### Step 5: Extract Peers from Email

Use native n8n nodes to extract email participants as peers:

**5a. Add a Set node ("Combine Email Fields")**

* Combines From, To, Cc, Bcc into an array of individual emails
* **Field name**: `allEmails`
* **Type**: Array
* **Value**: `{{ [$json.From, $json.To, $json.Cc, $json.Bcc].filter(Boolean).flatMap(field => field.split(',').map(e => e.trim())).filter(Boolean) }}`

**5b. Add a Split Out node**

* Splits the array into individual items (one per email address)
* **Field to Split Out**: `allEmails`

**5c. Add a Set node ("Clean Names")**

* Extracts the display name from each email and formats it
* **Field name**: `name`
* **Value**: `{{ $json.allEmails.split('<')[0].trim().replace(/ /g, '_') }}`

#### Step 6: Get or Create Peer

1. Add an **HTTP Request** node
2. **Method**: `POST`
3. **URL**: `https://api.honcho.dev/v3/workspaces/{{ $('Get or Create Workspace').item.json.id }}/peers`
4. **Body**: `{ "id": "{{ $json.name }}" }`

This creates a peer for each email participant, allowing Honcho to build understanding of each person.

#### Step 7: Add Peers to Session

1. Add an **HTTP Request** node
2. **Method**: `POST`
3. **URL**: `https://api.honcho.dev/v3/workspaces/{{ $('Get or Create Workspace').item.json.id }}/sessions/{{ $json.id }}/peers`
4. **Body**: `{ "{{ $json.id }}": {} }`

#### Step 8: Limit Node

Add a **Limit** node to control the flow so the message is only added once to the session.

#### Step 9: Create Message for Session

1. Add an **HTTP Request** node
2. **Method**: `POST`
3. **URL**: `https://api.honcho.dev/v3/workspaces/{{ $('Get or Create Workspace').item.json.id }}/sessions/{{ $('Get or Create Session').item.json.id }}/messages/`
4. **Body** (JSON): `{ "messages": [{ "content": "{{ $('Get a message').item.json.snippet }}", "peer_id": "{{ $('Get a message').item.json.From.split('<')[0].trim().replace(/ /g, '_') }}" }] }`

The `peer_id` must exactly match a peer created in Step 6. The expression above uses the same cleaning logic as the Clean Names node (`split('<')[0].trim().replace(/ /g, '_')`).

### Part 2: Building a Stateful AI Chatbot

Now that data is loaded into Honcho, create a chat interface that leverages this memory:

#### Step 1: Chat Trigger

Add a **When chat message received** node (from LangChain nodes) to create an interactive chat interface.

#### Step 2: AI Agent

1. Add an **Agent** node (LangChain)
2. Configure the system message:

```
You are a helpful assistant that retrieves context about email conversations.

Use the Context tool to retrieve session context.

Today's date: {{ $now }}
```

#### Step 3: Connect LLM

Add an **OpenAI Chat Model** node (or your preferred LLM) and connect it to the Agent.

#### Step 4: Add Honcho Tools

Create an HTTP Request Tool node for Honcho's context retrieval:

**Context Tool:**

* **Method**: `GET`
* **URL**: `https://api.honcho.dev/v3/workspaces/email-test/sessions/new_session/context`
* Returns formatted context for the entire session including all messages and peer interactions

Connect the tool to the Agent node. The URL uses the same workspace (`email-test`) and session (`new_session`) IDs created during data ingestion.

***

## Import the Workflow

Want to skip the manual setup? Import this workflow directly into n8n. In n8n, go to **Workflows** → **Import from URL** (use the raw JSON link below) or **Import from File**.

[Import from URL (raw JSON)](https://raw.githubusercontent.com/plastic-labs/honcho/main/examples/n8n/n8n.json) or expand below to copy:

<Accordion title="Click to expand workflow JSON">
  ```json theme={null}
  {
    "name": "Honcho Empowered Email AI Agent",
    "nodes": [
      {
        "parameters": {
          "content": "## Data Ingestion\nLoads Gmail email into Honcho.\n\n**Run this section first** by clicking 'Execute workflow'.",
          "height": 356,
          "width": 2008
        },
        "type": "n8n-nodes-base.stickyNote",
        "typeVersion": 1,
        "position": [
          -16,
          -64
        ],
        "id": "53f767a8-8df9-4ad7-8a3d-37c145495627",
        "name": "Sticky Note - Data Ingestion"
      },
      {
        "parameters": {
          "content": "## AI Chat With Honcho context()\nQuery your email data using natural language.\n\n**Run after data ingestion** to chat with the agent.",
          "height": 480,
          "width": 752
        },
        "type": "n8n-nodes-base.stickyNote",
        "typeVersion": 1,
        "position": [
          32,
          464
        ],
        "id": "34066961-d29e-4fe8-93bf-8f7043e142b0",
        "name": "Sticky Note - AI Chat"
      },
      {
        "parameters": {
          "model": "gpt-4o",
          "options": {}
        },
        "id": "16da7a98-5622-427a-bbab-1be39f828d0b",
        "name": "OpenAI Chat Model",
        "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
        "position": [
          240,
          800
        ],
        "typeVersion": 1,
        "credentials": {
          "openAiApi": {
            "id": "qrvGphL3ydUODxQZ",
            "name": "OpenAi account"
          }
        }
      },
      {
        "parameters": {
          "options": {
            "systemMessage": "You are a helpful assistant that retrieves context about email conversations.\n\nUse the Context tool to retrieve session context.\n\nToday's date: {{ $now }}"
          }
        },
        "id": "049c3c19-756c-4755-88d9-94312857d9bb",
        "name": "AI Agent",
        "type": "@n8n/n8n-nodes-langchain.agent",
        "position": [
          368,
          576
        ],
        "typeVersion": 1.7
      },
      {
        "parameters": {
          "options": {}
        },
        "id": "b9a2ef6a-0e81-45c9-a5ea-16e74a9aa77d",
        "name": "When chat message received",
        "type": "@n8n/n8n-nodes-langchain.chatTrigger",
        "position": [
          80,
          576
        ],
        "webhookId": "c91764c2-0b51-4025-ad74-d5f44127aa5a",
        "typeVersion": 1.1
      },
      {
        "parameters": {
          "method": "POST",
          "url": "=https://api.honcho.dev/v3/workspaces/{{ $('Get or Create Workspace').item.json.id }}/peers",
          "authentication": "predefinedCredentialType",
          "nodeCredentialType": "httpBearerAuth",
          "sendBody": true,
          "bodyParameters": {
            "parameters": [
              {
                "name": "id",
                "value": "={{ $json.name }}"
              }
            ]
          },
          "options": {}
        },
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.3,
        "position": [
          1296,
          96
        ],
        "id": "f2e81445-a866-4d9f-9a8a-b2dc8cbaea8b",
        "name": "Get or Create Peer",
        "credentials": {
          "httpBearerAuth": {
            "id": "NbrkGo1GdYWQY3OX",
            "name": "Bearer Auth account"
          }
        }
      },
      {
        "parameters": {
          "operation": "get",
          "messageId": "19b8fee837985953"
        },
        "type": "n8n-nodes-base.gmail",
        "typeVersion": 2.2,
        "position": [
          608,
          96
        ],
        "id": "ee5d8cc7-876b-4096-b6e5-14f1b92084a6",
        "name": "Get a message",
        "webhookId": "4ab02540-af03-405d-a6eb-dfcaa76477fc",
        "credentials": {
          "gmailOAuth2": {
            "id": "a2RvA5NMNjfOeHtd",
            "name": "Gmail account 2"
          }
        }
      },
      {
        "parameters": {
          "method": "POST",
          "url": "=https://api.honcho.dev/v3/workspaces/{{ $('Get or Create Workspace').item.json.id }}/sessions",
          "authentication": "predefinedCredentialType",
          "nodeCredentialType": "httpBearerAuth",
          "sendBody": true,
          "bodyParameters": {
            "parameters": [
              {
                "name": "id",
                "value": "=new_session"
              }
            ]
          },
          "options": {}
        },
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.3,
        "position": [
          448,
          96
        ],
        "id": "eef01db2-3355-484d-97b8-34480c40fcf8",
        "name": "Get or Create Session",
        "credentials": {
          "httpBearerAuth": {
            "id": "NbrkGo1GdYWQY3OX",
            "name": "Bearer Auth account"
          }
        }
      },
      {
        "parameters": {},
        "type": "n8n-nodes-base.manualTrigger",
        "typeVersion": 1,
        "position": [
          48,
          96
        ],
        "id": "a9de9d8f-7911-444f-99bd-7d287f587eff",
        "name": "When clicking 'Execute workflow'"
      },
      {
        "parameters": {
          "method": "POST",
          "url": "https://api.honcho.dev/v3/workspaces",
          "authentication": "predefinedCredentialType",
          "nodeCredentialType": "httpBearerAuth",
          "sendBody": true,
          "specifyBody": "json",
          "jsonBody": "{\n  \"id\": \"email-test\",\n  \"metadata\": {}\n}",
          "options": {}
        },
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.3,
        "position": [
          240,
          96
        ],
        "id": "49b91f82-1cd8-49aa-85a5-57a8ad7b5128",
        "name": "Get or Create Workspace",
        "credentials": {
          "httpBearerAuth": {
            "id": "NbrkGo1GdYWQY3OX",
            "name": "Bearer Auth account"
          }
        }
      },
      {
        "parameters": {
          "assignments": {
            "assignments": [
              {
                "id": "allEmails",
                "name": "allEmails",
                "type": "array",
                "value": "={{ [$json.From, $json.To, $json.Cc, $json.Bcc].filter(Boolean).flatMap(field => field.split(',').map(e => e.trim())).filter(Boolean) }}"
              }
            ]
          },
          "options": {}
        },
        "type": "n8n-nodes-base.set",
        "typeVersion": 3.4,
        "position": [
          784,
          96
        ],
        "id": "3eb4ce63-d95c-42d7-8a16-f35e2419d8c0",
        "name": "Combine Email Fields"
      },
      {
        "parameters": {
          "fieldToSplitOut": "allEmails",
          "options": {}
        },
        "type": "n8n-nodes-base.splitOut",
        "typeVersion": 1,
        "position": [
          960,
          96
        ],
        "id": "4702001d-40f5-4b44-b443-6fb0b94e58a9",
        "name": "Split Out"
      },
      {
        "parameters": {
          "assignments": {
            "assignments": [
              {
                "id": "name",
                "name": "name",
                "type": "string",
                "value": "={{ $json.allEmails.split('<')[0].trim().replace(/ /g, '_') }}"
              }
            ]
          },
          "options": {}
        },
        "type": "n8n-nodes-base.set",
        "typeVersion": 3.4,
        "position": [
          1136,
          96
        ],
        "id": "93327201-bfbe-4385-bfcd-7646f0513a62",
        "name": "Clean Names"
      },
      {
        "parameters": {
          "method": "POST",
          "url": "=https://api.honcho.dev/v3/workspaces/{{ $('Get or Create Workspace').item.json.id }}/sessions/{{ $('Get or Create Session').item.json.id }}/messages/",
          "authentication": "predefinedCredentialType",
          "nodeCredentialType": "httpBearerAuth",
          "sendBody": true,
          "specifyBody": "json",
          "jsonBody": "={\"messages\": [{\"content\": \"{{ $('Get a message').item.json.snippet }}\", \"peer_id\": \"{{ $('Get a message').item.json.From.split('<')[0].trim().replace(/ /g, '_') }}\"}]}",
          "options": {}
        },
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.3,
        "position": [
          1808,
          96
        ],
        "id": "cb6732d0-e5a9-4d6e-98ef-8fe1c290740b",
        "name": "Create Message for Session",
        "credentials": {
          "httpBearerAuth": {
            "id": "NbrkGo1GdYWQY3OX",
            "name": "Bearer Auth account"
          }
        }
      },
      {
        "parameters": {
          "method": "POST",
          "url": "=https://api.honcho.dev/v3/workspaces/{{ $('Get or Create Workspace').item.json.id }}/sessions/{{ $('Get or Create Session').item.json.id }}/peers",
          "authentication": "predefinedCredentialType",
          "nodeCredentialType": "httpBearerAuth",
          "sendBody": true,
          "specifyBody": "json",
          "jsonBody": "={\"{{ $json.id }}\": {}}",
          "options": {}
        },
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.3,
        "position": [
          1472,
          96
        ],
        "id": "3c2065b6-bd68-4698-a740-db3cd52f2267",
        "name": "Add Peers to Session",
        "credentials": {
          "httpBearerAuth": {
            "id": "NbrkGo1GdYWQY3OX",
            "name": "Bearer Auth account"
          }
        }
      },
      {
        "parameters": {},
        "type": "n8n-nodes-base.limit",
        "typeVersion": 1,
        "position": [
          1632,
          96
        ],
        "id": "d7c38f49-1a76-4a67-a540-4bec7aae1d9f",
        "name": "Limit"
      },
      {
        "parameters": {
          "url": "https://api.honcho.dev/v3/workspaces/email-test/sessions/new_session/context",
          "authentication": "predefinedCredentialType",
          "nodeCredentialType": "httpBearerAuth",
          "options": {}
        },
        "type": "n8n-nodes-base.httpRequestTool",
        "typeVersion": 4.3,
        "position": [
          656,
          784
        ],
        "id": "095e62d6-aae3-4eb8-9b9c-c473bfe2716d",
        "name": "Context",
        "credentials": {
          "httpBearerAuth": {
            "id": "NbrkGo1GdYWQY3OX",
            "name": "Bearer Auth account"
          }
        }
      }
    ],
    "pinData": {},
    "connections": {
      "OpenAI Chat Model": {
        "ai_languageModel": [
          [
            {
              "node": "AI Agent",
              "type": "ai_languageModel",
              "index": 0
            }
          ]
        ]
      },
      "When chat message received": {
        "main": [
          [
            {
              "node": "AI Agent",
              "type": "main",
              "index": 0
            }
          ]
        ]
      },
      "When clicking 'Execute workflow'": {
        "main": [
          [
            {
              "node": "Get or Create Workspace",
              "type": "main",
              "index": 0
            }
          ]
        ]
      },
      "Get or Create Workspace": {
        "main": [
          [
            {
              "node": "Get or Create Session",
              "type": "main",
              "index": 0
            }
          ]
        ]
      },
      "Get a message": {
        "main": [
          [
            {
              "node": "Combine Email Fields",
              "type": "main",
              "index": 0
            }
          ]
        ]
      },
      "Get or Create Session": {
        "main": [
          [
            {
              "node": "Get a message",
              "type": "main",
              "index": 0
            }
          ]
        ]
      },
      "Combine Email Fields": {
        "main": [
          [
            {
              "node": "Split Out",
              "type": "main",
              "index": 0
            }
          ]
        ]
      },
      "Split Out": {
        "main": [
          [
            {
              "node": "Clean Names",
              "type": "main",
              "index": 0
            }
          ]
        ]
      },
      "Clean Names": {
        "main": [
          [
            {
              "node": "Get or Create Peer",
              "type": "main",
              "index": 0
            }
          ]
        ]
      },
      "Get or Create Peer": {
        "main": [
          [
            {
              "node": "Add Peers to Session",
              "type": "main",
              "index": 0
            }
          ]
        ]
      },
      "Add Peers to Session": {
        "main": [
          [
            {
              "node": "Limit",
              "type": "main",
              "index": 0
            }
          ]
        ]
      },
      "Limit": {
        "main": [
          [
            {
              "node": "Create Message for Session",
              "type": "main",
              "index": 0
            }
          ]
        ]
      },
      "Context": {
        "ai_tool": [
          [
            {
              "node": "AI Agent",
              "type": "ai_tool",
              "index": 0
            }
          ]
        ]
      }
    },
    "active": false,
    "settings": {
      "executionOrder": "v1",
      "availableInMCP": false
    },
    "versionId": "ba0a3b77-cc19-49fd-9189-aaee65b35f99",
    "meta": {
      "templateCredsSetupCompleted": true,
      "instanceId": "4e34c96e55eb26be21fa69ca62c4851a5d09b678190481f5d47c084b6b327003"
    },
    "id": "dKOYeEOdrZOetmFRmIAUJ",
    "tags": []
  }
  ```
</Accordion>

<Note>
  **Important:** After importing, you'll need to:

  * Add your Honcho API key to the Bearer Auth credential
  * Connect your Gmail OAuth2 credential
  * Add your OpenAI API key (or swap for your preferred LLM)
  * Update the Gmail Message ID in "Get a message" node

  **Running the workflow:**

  1. First, execute the data ingestion section (click "Execute workflow")
  2. Then use the chat interface to query your email data
</Note>

***

## Next Steps

Once you have the basic workflow running, consider these enhancements:

* **Dynamic IDs**: Use n8n variables instead of hardcoding `email-test` and `new_session`
* **Chat with Peers**: Add an HTTP Request Tool for natural language queries about peer representations. Read more in the [docs](/docs/v3/documentation/features/chat).
* **Load more messages**: Use Gmail's "Get All" operation to load entire conversation threads
* **Make it real-time**: Add a **Gmail Trigger** node to automatically ingest new emails as they arrive
* **Add error handling**: Connect an **Error Trigger** node with notifications (Email, Slack) and retry logic
* **Expand to other data sources**: Honcho works with Slack messages, CRM interactions, support tickets, and more

***

## Related Resources

<CardGroup>
  <Card title="Architecture" icon="sitemap" href="/v3/documentation/core-concepts/architecture">
    Understand workspaces, sessions, peers, and messages
  </Card>

  <Card title="Get Context" icon="messages" href="/v3/documentation/features/get-context">
    Learn about retrieving formatted conversation context
  </Card>
</CardGroup>


# OpenClaw
Source: https://honcho.dev/docs/v3/guides/integrations/openclaw

Add AI-native memory to OpenClaw

[OpenClaw](https://openclaw.ai) is a general AI agent that can perform actions on behalf of a user. The Honcho plugin gives OpenClaw memory across every channel — WhatsApp, Telegram, Discord, Slack, and more.

<Note>
  Honcho can run entirely locally with OpenClaw — no external API required. Keep your data on your machine while getting full memory capabilities across all channels. See the [self-hosting guide](/docs/v3/contributing/self-hosting) to get started.
</Note>

For OpenClaw's own documentation on Honcho, see the [Honcho Memory guide](https://docs.openclaw.ai/concepts/memory-honcho).

## Install the Plugin

```bash theme={null}
openclaw plugins install @honcho-ai/openclaw-honcho
openclaw honcho setup
openclaw gateway --force
```

`openclaw honcho setup` prompts for your API key, writes the config, and optionally uploads any legacy memory files to Honcho.

<iframe title="Loom video" />

<Note>
  **Alternative: ClawHub Skill**

  The `honcho-setup` skill handles installation and migration interactively from a chat session:

  ```bash theme={null}
  npx clawhub install honcho-setup
  # Restart OpenClaw, then invoke the skill from a session
  openclaw plugins install @honcho-ai/openclaw-honcho
  openclaw gateway restart
  ```
</Note>

## Migrating Legacy Memory

If you have existing workspace memory files (`USER.md`, `MEMORY.md`, `IDENTITY.md`, `memory/`, `canvas/`, etc.), `openclaw honcho setup` will detect them and offer to migrate them.

<Note>
  Migration is **non-destructive** — files are uploaded to Honcho. Originals are never deleted or moved.
</Note>

### Legacy files

**User/owner files** (content describes the user):

* `USER.md`, `IDENTITY.md`, `MEMORY.md`
* All files in `memory/` and `canvas/` directories

**Agent/self files** (content describes the agent):

* `SOUL.md`, `AGENTS.md`, `TOOLS.md`, `BOOTSTRAP.md`

### Upload to Honcho

Files are uploaded via `session.uploadFile()`. User/owner files go to the owner peer; agent/self files go to the openclaw peer.

## How It Works

Once installed, the plugin runs automatically:

* **Message Observation** — After every AI turn, the conversation is persisted to Honcho. Both user and agent messages are observed, allowing Honcho to build and refine its models.
* **Tool-Based Context Access** — The AI can query Honcho mid-conversation using tools like `honcho_context`, `honcho_search_conclusions`, `honcho_search_messages`, and `honcho_ask` to retrieve relevant context. Context is injected during OpenClaw's `before_prompt_build` phase, ensuring accurate turn boundaries.
* **Dual Peer Model** — Honcho maintains separate representations: one for the user (preferences, facts, communication style) and one for the agent (personality, learned behaviors). Each OpenClaw agent gets its own Honcho peer (`agent-{id}`), so multi-agent workspaces maintain isolated memory.
* **Clean Persistence** — Platform metadata (conversation info, sender headers, thread context, forwarded messages) is stripped before saving to Honcho, ensuring only meaningful content is persisted.

## Multi-Agent Support

OpenClaw uses a multi-agent architecture where a primary agent can spawn **subagents** to handle specialized tasks. The Honcho plugin is fully aware of this hierarchy:

* **Automatic Subagent Detection** — When OpenClaw spawns a subagent, the plugin tracks the parent→child relationship via the `subagent_spawned` hook. Each subagent session records its `parentPeerId` in metadata.
* **Parent Observer Peer** — The spawning agent is added as a silent observer in the subagent's Honcho session (`observeMe: false, observeOthers: true`). This gives Honcho visibility into the full agent tree — the parent can see what its subagents are doing without its own messages being attributed to the subagent session.

## AI Tools

### Data Retrieval (fast, no LLM)

| Tool                        | Description                                                                                           |
| --------------------------- | ----------------------------------------------------------------------------------------------------- |
| `honcho_context`            | User knowledge across all sessions. `detail='card'` for key facts, `'full'` for broad representation. |
| `honcho_search_conclusions` | Semantic vector search over stored conclusions ranked by relevance.                                   |
| `honcho_search_messages`    | Find specific messages across all sessions. Filter by sender, date, or metadata.                      |
| `honcho_session`            | Current session history and summary. Supports semantic search within the session.                     |

### Q\&A (LLM-powered)

| Tool         | Description                                                                                  |
| ------------ | -------------------------------------------------------------------------------------------- |
| `honcho_ask` | Ask Honcho a question about the user. `depth='quick'` for facts, `'thorough'` for synthesis. |

## CLI Commands

```bash theme={null}
openclaw honcho setup                           # Configure API key and migrate legacy files
openclaw honcho status                          # Connection status
openclaw honcho ask <question>                  # Query Honcho about the user
openclaw honcho search <query> [-k N] [-d D]    # Semantic search (topK, maxDistance)
```

## Configuration

Run `openclaw honcho setup` to configure interactively, or set values directly in `~/.openclaw/openclaw.json` under `plugins.entries["openclaw-honcho"].config`.

| Key           | Default                    | Description                                                  |
| ------------- | -------------------------- | ------------------------------------------------------------ |
| `apiKey`      | —                          | Honcho API key (required for managed; omit for self-hosted). |
| `workspaceId` | `"openclaw"`               | Honcho workspace ID for memory isolation.                    |
| `baseUrl`     | `"https://api.honcho.dev"` | API endpoint (for self-hosted instances).                    |

### Self-Hosted Honcho

Point the plugin to your local instance and follow the [self-hosting guide](https://github.com/plastic-labs/honcho?tab=readme-ov-file#local-development) to get started:

```bash theme={null}
openclaw honcho setup
# Enter blank API key, set Base URL to http://localhost:8000
```

## Local File Search (QMD Integration)

The plugin automatically exposes OpenClaw's `memory_search` and `memory_get` tools when a [memory backend](https://docs.openclaw.ai/concepts/memory) is configured, allowing both Honcho memory and local file search together.

### Setup

1. Install [QMD](https://github.com/tobi/qmd) on your server

2. Configure OpenClaw to use QMD as the memory backend in `~/.openclaw/openclaw.json`:

```json theme={null}
{
  "memory": {
    "backend": "qmd"
  }
}
```

OpenClaw manages QMD collections automatically from your workspace memory files and any extra paths in `memory.qmd.paths`. See the [QMD Memory Engine docs](https://docs.openclaw.ai/concepts/memory-qmd) for full setup.

3. Restart the gateway:

```bash theme={null}
openclaw gateway restart
```

### Available Tools

When QMD is configured, you get both Honcho and local file tools:

| Tool            | Source | Description                                              |
| --------------- | ------ | -------------------------------------------------------- |
| `honcho_*`      | Honcho | Cross-session memory, user modeling, dialectic reasoning |
| `memory_search` | QMD    | Search local markdown files                              |
| `memory_get`    | QMD    | Retrieve file content                                    |

## Next Steps

<CardGroup>
  <Card title="GitHub Repository" icon="github" href="https://github.com/plastic-labs/openclaw-honcho">
    Source code, issues, and README.
  </Card>

  <Card title="OpenClaw Memory Docs" icon="book" href="https://docs.openclaw.ai/concepts/memory">
    Memory backends, search, and configuration in the OpenClaw docs.
  </Card>

  <Card title="Honcho Architecture" icon="sitemap" href="/v3/documentation/core-concepts/architecture">
    Learn about peers, sessions, and dialectic reasoning.
  </Card>
</CardGroup>


# OpenCode
Source: https://honcho.dev/docs/v3/guides/integrations/opencode

Add AI-native memory to OpenCode

Give OpenCode long-term memory that survives context wipes, session restarts, and fresh chats. OpenCode remembers what you're working on, your durable preferences, and prior context across every project you touch.

## Quick Start

### Step 1: Get Your Honcho API Key

1. Go to **[app.honcho.dev](https://app.honcho.dev)**
2. Sign up or log in
3. Copy your API key (starts with `hch-`)

### Step 2: Install the Plugin

<Note>
  This plugin requires the [OpenCode CLI](https://opencode.ai). If `opencode` isn't on your `PATH`, install it first, then restart your shell.
</Note>

Install the plugin:

```bash theme={null}
opencode plugin "@honcho-ai/opencode-honcho" --global
```

To update an existing plugin install:

```bash theme={null}
opencode plugin "@honcho-ai/opencode-honcho" --force
```

OpenCode:

* registers `@honcho-ai/opencode-honcho` with OpenCode
* resolves the package's native server and TUI plugin targets
* updates plugin entries in your global OpenCode config
* activates the plugin globally for every OpenCode project

### Step 3: Run Setup in OpenCode

1. Start OpenCode
2. Run `/honcho:setup`
3. Keep the default **Honcho Cloud** option unless you want a self-hosted or local endpoint
4. Paste your Honcho API key
5. Run `/honcho:status` to verify the runtime

## What You Get

* **Persistent Memory** — OpenCode retains durable context across sessions
* **Cloud or Local Deployments** — Point at Honcho Cloud or a self-hosted / local instance
* **Workspace Mapping** — OpenCode projects map cleanly to Honcho workspaces
* **Flexible Session Mapping** — Scope sessions per directory, repo, branch, chat instance, or globally
* **Durable Writes** — Save stable conclusions and retain session context across OpenCode runs
* **Memory Retrieval** — Search session messages, query Honcho's reasoning, and inject relevant context into prompts
* **Agent Tools** — First-class tools for search, chat, and conclusion-writing inside OpenCode

## Configuration

Configuration lives in a single shared file at `~/.honcho/config.json`, shared with other Honcho hosts (Claude Code, Cursor, etc.). OpenCode reads and writes this file directly, and OpenCode-specific defaults live under `hosts.opencode`. Edit the file direct or use `/honcho:config` to change it via OpenCode's chat, or call the `honcho_set_config` tool for other settings.

```jsonc theme={null}
{
  "apiKey": "hch-...",
  "peerName": "alice",
  "baseUrl": "https://api.honcho.dev",
  "hosts": {
    "opencode": {
      "workspace": "opencode",
      "aiPeer": "opencode",
      "recallMode": "hybrid",
      "observationMode": "directional",
      "sessionStrategy": "per-directory"
    }
  }
}
```

Top-level shared fields are `apiKey`, `peerName`, and `baseUrl`. OpenCode's host-scoped settings live under `hosts.opencode`: `workspace`, `aiPeer`, `recallMode`, `observationMode`, and `sessionStrategy`.

### Cloud vs Local

For **Honcho Cloud**:

* `apiKey` is required
* `baseUrl` should stay at `https://api.honcho.dev`

For **self-hosted or local Honcho**:

* `baseUrl` should point to your deployment (e.g. `http://127.0.0.1:8000`)
* `apiKey` is only required if the deployment is authenticated

<Warning>
  If OpenCode is running inside Docker or another remote environment, `localhost` won't refer to your host machine. The `baseUrl` must be reachable from the OpenCode runtime.
</Warning>

### Recall Modes

| Mode               | Behavior                               | Best for                              |
| ------------------ | -------------------------------------- | ------------------------------------- |
| `hybrid` (default) | Context injection **and** tool access  | Most users — balanced memory coverage |
| `context`          | Only inject memory into system prompts | Predictable prompts, no tool calls    |
| `tools`            | Only expose memory as tools            | Explicit, on-demand retrieval         |

### Session Strategies

| Strategy                  | Behavior                                  | Best for                              |
| ------------------------- | ----------------------------------------- | ------------------------------------- |
| `per-directory` (default) | One session per working directory         | Most projects                         |
| `per-repo`                | One session per repository                | Repos with multiple entry directories |
| `git-branch`              | Session follows the current git branch    | Branch-specific workflows             |
| `per-session`             | New session per OpenCode session id       | Short-lived isolated work             |
| `chat-instance`           | Session tied to the current chat instance | Highly ephemeral usage                |
| `global`                  | One session for everything                | Shared memory across all work         |

## Operator Commands

| Command            | Description                                                   |
| ------------------ | ------------------------------------------------------------- |
| `/honcho:setup`    | First-time setup for cloud or local Honcho                    |
| `/honcho:status`   | Show effective Honcho status for the current OpenCode project |
| `/honcho:settings` | Show effective config values and config paths                 |
| `/honcho:config`   | Change `recallMode`                                           |

## Agent Tools

The plugin exposes these tools inside OpenCode:

| Tool                       | Description                                                        |
| -------------------------- | ------------------------------------------------------------------ |
| `honcho_setup`             | Validate setup and persist shared credentials or endpoint settings |
| `honcho_status`            | Show effective runtime status                                      |
| `honcho_get_config`        | Read effective and persisted settings                              |
| `honcho_set_config`        | Update a persisted shared setting                                  |
| `honcho_search`            | Search Honcho session messages                                     |
| `honcho_chat`              | Query Honcho for reasoning-backed context                          |
| `honcho_create_conclusion` | Save a durable memory conclusion                                   |

## Plugin Surfaces

The plugin hooks into these OpenCode plugin capabilities:

* `event`
* `chat.message`
* `tool.execute.after`
* `command.execute.before`
* `experimental.chat.system.transform`
* `experimental.session.compacting`
* `shell.env`
* `tool`

## Building with Teammates

Because `~/.honcho/config.json` is shared across Honcho hosts, teammates can collaborate by pointing at the same workspace while keeping their own identities. Sessions are automatically prefixed by `peerName` to avoid collisions.

**Alice** (`~/.honcho/config.json`):

```json theme={null}
{
  "apiKey": "hch-team-key...",
  "peerName": "alice",
  "hosts": {
    "opencode": { "workspace": "team-acme", "aiPeer": "opencode" }
  }
}
```

**Bob** (`~/.honcho/config.json`):

```json theme={null}
{
  "apiKey": "hch-team-key...",
  "peerName": "bob",
  "hosts": {
    "opencode": { "workspace": "team-acme", "aiPeer": "opencode" }
  }
}
```

Both write to `team-acme`; Honcho's dialectic reasoning draws on context from both peers.

## Next Steps

<CardGroup>
  <Card title="GitHub Repository" icon="github" href="https://github.com/plastic-labs/opencode-honcho">
    Source code, issues, and README.
  </Card>

  <Card title="Honcho Architecture" icon="sitemap" href="../../documentation/core-concepts/architecture">
    Learn about peers, sessions, and dialectic reasoning.
  </Card>
</CardGroup>


# Paperclip
Source: https://honcho.dev/docs/v3/guides/integrations/paperclip

Add Honcho memory to Paperclip

Honcho for [Paperclip](https://paperclip.ing) adds persistent Honcho memory to Paperclip while keeping Paperclip as the system of record.

<Note>
  This page covers the current public-host-compatible Paperclip plugin. It supports tools, sync, migration import, and manual prompt previews. It does not depend on automatic prompt-context injection hooks, run transcript import, or legacy workspace file import.
</Note>

## Install the Plugin

1. In Paperclip, open `Instance Settings` -> `Plugins`.
2. Click `Install Plugin`.
3. Enter `@honcho-ai/paperclip-honcho`.
4. Complete the install from the Paperclip UI.
   * Plugin download does not currently work on Windows because of a Paperclip host-side issue.

## Quick Setup

### Minimal Path

1. Create a Paperclip secret containing the Honcho API key.
   * For a local Honcho, use whatever credential your local startup expects & `honchoApiKey` is not needed.
2. Open the Honcho plugin settings page in Paperclip.
3. If you are using Honcho Cloud, leave the deployment on the default cloud setting.
4. If you are using a local Honcho instance, switch the deployment to `Self-hosted / local` and set `honchoApiBaseUrl`.
5. Set `honchoApiKey`.
6. Save the settings.
7. Run `Initialize Honcho memory`.

`honchoApiKey` is the only field required for the standard setup path. The other settings already have defaults.

<Note>
  If you use a local Honcho deployment, `honchoApiBaseUrl` must be reachable from the Paperclip host runtime. If Paperclip is running in Docker, `localhost` may not point at your machine.
</Note>

## Multi-Agent Hierarchy

### What Maps Where

Paperclip memory is organized around company, issue, and agent boundaries:

* **Company -> workspace**: each Paperclip company maps to one Honcho workspace.
* **Issue -> session**: each Paperclip issue maps to one Honcho session inside that workspace.
* **Humans and agents -> peers**: human actors and Paperclip agents map to Honcho peers.

This gives the plugin a natural hierarchy: company-level memory lives at the workspace level, issue-level memory lives at the session level, and people or agents are modeled as peers that participate across those scopes.

### How Agent Observation Works

The current plugin gives agent peers explicit observation settings:

* `observe_me` defaults to `true`
* `observe_others` defaults to `true`

In practice, that means agent peers can both be observed by Honcho and form representations of other peers they interact with.

## How It Works

### Identity And Scope

The integration breaks down into four parts:

* **Identity and scope** - each Paperclip company maps to a Honcho workspace, agents and human actors map to peers, and issues map to sessions.
* **What gets copied into Honcho** - issue comments and document revisions sync into Honcho, with document content sectioned and normalized message content capped before ingestion.
* **What operators get** - operators get a plugin settings page, migration preview/status data, including a per-issue migration mapping preview, repair tools, and an issue-level `Memory` tab.
* **What agents get** - agents get Honcho retrieval and peer-chat tools inside Paperclip.

## Operator Actions

The settings page exposes the main operator workflow directly:

| Action                               | What it does                                                                                                |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| `Validate config`                    | Validates the current plugin configuration before any sync or import work runs.                             |
| `Test connection`                    | Resolves the API key secret, checks the Honcho connection, and returns the mapped workspace ID.             |
| `Initialize memory for this company` | Connects Honcho, creates core mappings, imports baseline issue memory, and verifies manual prompt previews. |
| `Rescan migration sources`           | Scans issue comments and issue documents and writes a fresh import preview.                                 |
| `Import history`                     | Imports the approved historical preview into Honcho with idempotent ledger checks.                          |
| `Preview prompt context`             | Builds a manual prompt-context preview for a company or issue without relying on automatic host hooks.      |
| `Repair mappings`                    | Recreates missing workspace, peer, and session mappings for the current company.                            |
| `Resync this issue`                  | Replays sync for the current issue from the issue Memory tab.                                               |

## Configuration Defaults And Overrides

### Default Behavior

| Setting               | Default                  | Use when                                                                                 |
| --------------------- | ------------------------ | ---------------------------------------------------------------------------------------- |
| `honchoApiKey`        | —                        | Required. Points the plugin at the Paperclip secret containing your Honcho API key.      |
| `honchoApiBaseUrl`    | `https://api.honcho.dev` | Override this for self-hosted or non-default Honcho deployments.                         |
| `workspacePrefix`     | `paperclip`              | Change this if you want a different workspace namespace.                                 |
| `syncIssueComments`   | `true`                   | Turn this off if you do not want comment history imported into Honcho.                   |
| `syncIssueDocuments`  | `true`                   | Turn this off if you do not want issue document revisions imported.                      |
| `enablePeerChat`      | `true`                   | Required for the peer chat tool surface.                                                 |
| `enablePromptContext` | `false`                  | Keep this off on the public-host-compatible path and use manual prompt previews instead. |
| `observe_me`          | `true`                   | Controls whether agent peers are observed by Honcho.                                     |
| `observe_others`      | `true`                   | Controls whether agent peers form representations of other peers they interact with.     |

The plugin also accepts additional advanced fields in the settings page, including noise-pattern and metadata-strip controls. Most setups can ignore those and start with the defaults above.

## Agent Tools

The plugin registers the following Honcho tools for Paperclip agents:

| Tool                           | Description                                                                                   |
| ------------------------------ | --------------------------------------------------------------------------------------------- |
| `honcho_get_issue_context`     | Retrieve compact Honcho context for the current issue session.                                |
| `honcho_search_memory`         | Search Honcho memory within the current workspace, narrowing to the current issue by default. |
| `honcho_search_messages`       | Search raw Honcho messages.                                                                   |
| `honcho_search_conclusions`    | Search high-signal summarized Honcho memory.                                                  |
| `honcho_get_workspace_context` | Retrieve broad workspace recall from Honcho.                                                  |
| `honcho_get_session`           | Retrieve issue session context from Honcho.                                                   |
| `honcho_get_agent_context`     | Retrieve peer context for a specific agent.                                                   |
| `honcho_get_hierarchy_context` | Retrieve delegated-work context when the host provides lineage metadata.                      |
| `honcho_ask_peer`              | Query Honcho peer chat for a target peer. Requires peer chat to be enabled in plugin config.  |

## Next Steps

<CardGroup>
  <Card title="Paperclip-Honcho Repository" icon="github" href="https://github.com/plastic-labs/paperclip-honcho">
    Open the repository for source and setup details.
  </Card>

  <Card title="Honcho Architecture" icon="sitemap" href="../../documentation/core-concepts/architecture">
    Review how workspaces, peers, and sessions fit together.
  </Card>

  <Card title="Representation Scopes" icon="messages" href="../../documentation/features/advanced/representation-scopes">
    Review how `observe_me` and `observe_others` change what peers can model.
  </Card>
</CardGroup>


# Voice Agent - Reachy Mini
Source: https://honcho.dev/docs/v3/guides/integrations/reachy-mini

Build an embodied voice AI agent with long-term memory using Honcho

[Reachy Mini](https://huggingface.co/blog/reachy-mini) is Hugging Face and Pollen Robotics' open-source robot for human-robot interaction. This guide integrates Honcho for persistent, multi-user memory with OpenAI's Realtime API for voice.

<Note>
  **Real-time memory**: Honcho's async API is designed for live voice interactions. Messages persist in the background without blocking audio, and the dialectic API returns user context fast enough for mid-conversation tool calls.
</Note>

<CardGroup>
  <Card title="GitHub Repository" icon="github" href="https://github.com/plastic-labs/reachy-mini-honcho">
    Full source code
  </Card>

  <Card title="Build Livestream" icon="youtube" href="https://www.youtube.com/watch?v=i6iijJnkxh0">
    Watch us build it live
  </Card>
</CardGroup>

## What It Does

* **Face recognition** identifies users and loads their personal memory
* **Honcho** stores conversations and reasons about each user over time
* **OpenAI Realtime** handles low-latency voice interaction
* **Gaze tracking** maintains eye contact during conversation

When a user returns days later, the robot remembers their name, interests, and previous discussions.

## Setup

```bash theme={null}
pip install reachy-mini honcho-ai openai python-dotenv numpy scipy mediapipe face-recognition
```

```bash theme={null}
export OPENAI_API_KEY=your_openai_key
export HONCHO_API_KEY=your_honcho_key  # get at app.honcho.dev
```

## Architecture

```
Reachy Mini (camera, mic, speaker)
        ↓
OpenAI Realtime API (voice + tools)
        ↓
Honcho (memory + reasoning per user)
```

## Honcho Integration

Initialize Honcho with a robot peer (not observed) and dynamic user peers (observed):

```python theme={null}
from honcho import Honcho
from honcho.api_types import PeerConfig

honcho = Honcho(api_key=api_key, workspace_id="reachy-mini")

# Robot peer - stores messages but isn't reasoned about
robot_peer = await honcho.aio.peer(
    "reachy",
    configuration=PeerConfig(observe_me=False),
)

# User peers - Honcho reasons about their preferences and history
user_peer = await honcho.aio.peer(user_id)
session = await honcho.aio.session(f"chat-{user_id}")
```

Store messages in the background without blocking the voice loop:

```python theme={null}
# Queue messages async - doesn't block audio playback
await session.aio.add_messages(user_peer.message(transcript))
await session.aio.add_messages(robot_peer.message(response))
```

## Memory Tools

The robot calls Honcho mid-conversation via OpenAI function calling — fast enough for real-time voice:

| Tool                | Purpose                                            |
| ------------------- | -------------------------------------------------- |
| `recall`            | Query Honcho about the user ("What's their name?") |
| `create_conclusion` | Save important facts to long-term memory           |
| `see`               | Capture and analyze camera feed                    |

```python theme={null}
# Recall - ask Honcho's dialectic API (returns in ~200-500ms)
result = await user_peer.aio.chat(
    "What do I know about this user?",
    session=session,
    reasoning_level="medium"
)

# Create conclusion - save a fact
await user_peer.conclusions_of(user_id).aio.create([
    {"content": "Their name is Alice"}
])
```

## Multi-User Support

Face recognition identifies returning users. When a new face is detected, the agent:

1. Flushes pending transcripts to the previous user's session
2. Switches Honcho context to the new user
3. Fetches a briefing from Honcho's dialectic API
4. Reconnects OpenAI with fresh context and triggers a greeting

```python theme={null}
# Get briefing when user is recognized
briefing = await user_peer.aio.chat(
    "What should I know about this user? Name, interests, recent topics.",
    session=session,
    reasoning_level="low"
)
```

## System Prompt

```python theme={null}
SYSTEM_PROMPT = """You are Reachy, a friendly robot. Keep responses concise.

You have a recall tool for memory. ALWAYS use it before claiming you don't
know something about the user. Never say "Nice to meet you" if you've met before."""
```

## Run

```bash theme={null}
uv run python main.py
```

## Next Steps

<CardGroup>
  <Card title="Honcho Architecture" icon="sitemap" href="/v3/documentation/core-concepts/architecture">
    Understand peers, sessions, and reasoning
  </Card>

  <Card title="Chat Endpoint" icon="comments" href="/v3/documentation/features/chat">
    Learn about Honcho's dialectic API
  </Card>

  <Card title="Get Context" icon="database" href="/v3/documentation/features/get-context">
    Retrieve formatted conversation history
  </Card>

  <Card title="GitHub code" icon="robot" href="https://github.com/plastic-labs/reachy-mini-honcho">
    Dig into the code
  </Card>
</CardGroup>


# SillyTavern
Source: https://honcho.dev/docs/v3/guides/integrations/sillytavern

Add persistent, personalized memory to SillyTavern AI characters with Honcho

Give your SillyTavern characters long-term memory. Honcho remembers who you are, what you've talked about, and how to talk to you -- across sessions, characters, and restarts.

The extension has two parts: a **client extension** (browser) that hooks into SillyTavern events, and a **server plugin** (Node.js) that proxies requests to the Honcho API.

## Prerequisites

* **SillyTavern running locally** (Node ≥ 18). New to it? See the [SillyTavern installation docs](https://docs.sillytavern.app/installation/).
* A **Honcho API key** from [app.honcho.dev](https://app.honcho.dev).
* An **LLM backend** (OpenAI, Claude, OpenRouter, local llama.cpp, etc.) connected via SillyTavern's plug icon in the top nav. Honcho stores memory; it doesn't generate text.

## Quick Start

### Step 1: Install

From your **SillyTavern directory**:

**macOS / Linux:**

```bash theme={null}
bash <(curl -fsSL https://raw.githubusercontent.com/plastic-labs/sillytavern-honcho/main/install.sh)
```

**Windows (PowerShell):**

```powershell theme={null}
irm https://raw.githubusercontent.com/plastic-labs/sillytavern-honcho/main/install.ps1 | iex
```

The installer (macOS / Linux):

1. Clones the extension into `public/scripts/extensions/third-party/sillytavern-honcho`
2. Symlinks the server plugin to `plugins/honcho-proxy`
3. Installs the `@honcho-ai/sdk` dependency
4. Bootstraps `config.yaml` if it doesn't exist (briefly runs `npm start` to generate defaults)
5. Sets `enableServerPlugins: true` in `config.yaml`
6. Detects your `~/.honcho/config.json` and warns if no resolvable `apiKey`

The Windows installer does steps 1–3 (using a directory junction via `mklink /J` instead of a symlink) and checks for `~/.honcho/config.json`, but does **not** bootstrap `config.yaml` or flip `enableServerPlugins`. If `config.yaml` is missing, start SillyTavern once to generate it; then set `enableServerPlugins: true` manually before restarting.

### Step 2: Restart SillyTavern

<Note>
  **Restart is required.** SillyTavern loads server plugins at startup only. After running `install.sh`, stop SillyTavern (⌃C) and start it again. You'll need to restart again whenever `plugin/index.js` changes. Client-side (browser) updates pick up on a hard refresh — no restart needed for those.
</Note>

### Step 3: Configure

Open **Extensions** (puzzle blocks icon) and expand **Honcho Memory**:

1. Check **Enable Honcho Memory**
2. Click the API key field to set your key. The plugin falls back to `~/.honcho/config.json` at request time if no panel key is set; a panel value always wins.
3. Enter your **Workspace ID** (saves to `hosts.sillytavern.workspace`)
4. Enter **Your peer name** (saves to `hosts.sillytavern.peerName`; auto-synced from your SillyTavern persona on first boot)
5. Status indicator should show **Ready**

## How It Works

### Context Architecture

Every generation injects a **base context layer** from `session.context()` -- the peer representation (what Honcho knows about you) and session summary. This uses stale-while-revalidate caching: the first turn blocks to populate the cache, then every subsequent turn serves the cached result instantly while refreshing in the background.

The **enrichment mode** controls what layers on top of the base context:

| Mode                    | Behavior                                                                        |
| ----------------------- | ------------------------------------------------------------------------------- |
| **Context only**        | Base layer only -- peer representation + session summary                        |
| **Reasoning** (default) | Base layer + dialectic `peer.chat()` queries on a configurable per-turn cadence |
| **Tool call**           | Base layer + function tools the LLM can call on demand                          |

Both the context and reasoning layers use stale-while-revalidate with a configurable cadence ("Refresh every N turns" and "Reason every N turns"). After the first turn of a session, there is zero added latency.

<Note>
  **Context only** mode relies on `session.context()`, which is session-scoped — it returns empty output until the session has enough messages for Honcho to derive a representation and summary. For fresh sessions or peers with little history, Reasoning mode is a better default: it queries `peer.chat()` across all of the peer's history, not just the current session.
</Note>

### Tool Call Mode

In tool call mode, the extension registers three function tools that the LLM can invoke:

| Tool                     | Description                                                                   |
| ------------------------ | ----------------------------------------------------------------------------- |
| `honcho_query_memory`    | Dialectic chat query -- ask Honcho what it knows                              |
| `honcho_save_conclusion` | Save a key insight or biographical detail about the user to persistent memory |
| `honcho_search_history`  | Semantic search across session messages                                       |

This mode works best with models that support function calling. The LLM decides when to query memory rather than firing on every turn.

### Other Panel Knobs

The Extensions panel also exposes: **Context settings** (token budget, refresh cadence in turns, include session summary), **Injection position** (After/Before main prompt, or In-chat @ Depth with a numeric depth field), a **Prompt Template** textarea that wraps Honcho output via a `{{text}}` placeholder, and a **Reasoning queries** textarea (`{{message}}` placeholder) for customizing the dialectic prompts used in Reasoning mode.

### Peer Observability

By default, only the user peer accumulates derived memory — Honcho observes the user's messages and derives conclusions across sessions. The AI character's persona comes from its character card, not from peer derivation.

### Peer Modes and Session Naming

Peer mode controls memory partitioning; session naming controls conversation partitioning. Pair them to get the isolation you want.

| Peer Mode                        | Behavior                                  |
| -------------------------------- | ----------------------------------------- |
| **Single peer for all personas** | One user peer shared across all personas  |
| **Separate peer per persona**    | Each persona gets its own isolated memory |

| Session Naming    | Behavior                                |
| ----------------- | --------------------------------------- |
| **Auto**          | Per-chat hash (unique per conversation) |
| **Per character** | One session per character (persistent)  |
| **Custom**        | User-defined session name               |

Session IDs are frozen once assigned. Changing the naming mode, the custom session name, or the character name only affects new chats — existing chats stay linked to their original Honcho session so history, summaries, and derivations don't fragment.

The Active session field in the panel is read-only. To start fresh, hit **Reset** next to it — the current session gets orphaned (messages stay in Honcho, the chat unlinks) and a new session starts on the next message.

### Group Chats

Group chats register one peer per character, not a single collapsed `group-<id>` peer. Each character's messages land under their own peer, so their derived representations stay distinct. Characters who join mid-chat get lazy-added to the session on their first message.

## Global Config (Multi-Tool Setups)

If you already use Honcho with other tools (Claude Code, Cursor, Hermes), the extension reads from `~/.honcho/config.json` on startup.

**Resolution order** for `apiKey`, `workspace`, and `peerName`:

1. `hosts.sillytavern.<field>` (host-specific override)
2. Root-level `<field>` (shared default across tools)
3. For `apiKey` only: fall through to the Extensions-panel key (SillyTavern's secret manager), which takes priority at request time — entering one in the UI overrides the file without touching it.

**Writes** are scoped to `hosts.sillytavern.*`. The extension never mutates other tools' entries. Panel edits for Workspace ID and peer name save back to `hosts.sillytavern.workspace` and `hosts.sillytavern.peerName` respectively (debounced). Empty values clear the host override and fall through to the root value.

Flat form (single-tool setup):

```json theme={null}
{
  "apiKey": "your-honcho-api-key",
  "peerName": "your-name",
  "workspace": "sillytavern",
  "enabled": true
}
```

Nested form (multiple tools sharing the file):

```jsonc theme={null}
{
  "apiKey": "hch-v2-...",
  "peerName": "alice",
  "workspace": "default",
  "hosts": {
    "sillytavern": {
      "workspace": "sillytavern",
      "peerName": "alice-rp"
    },
    "claude_code": { "...": "..." },
    "cursor": { "...": "..." }
  }
}
```

## Troubleshooting

| Symptom                                                         | Fix                                                                                                    |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| No "Honcho Memory" in Extensions                                | Check symlink exists: `ls public/scripts/extensions/third-party/sillytavern-honcho/manifest.json`      |
| Plugin not initializing                                         | Ensure `enableServerPlugins: true` in `config.yaml`, then restart ST                                   |
| 403 on plugin requests                                          | Set Honcho API key in extension settings or `~/.honcho/config.json`                                    |
| SDK import error                                                | Run `cd plugins/honcho-proxy && npm install`                                                           |
| Extension loads but nothing happens                             | Enable the checkbox and ensure workspace ID is set                                                     |
| Plugin on disk but "Honcho Memory" drawer doesn't appear at all | Set `enableServerPlugins: true` in `config.yaml`; the panel can't show plugins the server never loaded |
| Peer name on a new chat still shows an old value                | Clear the panel override field (falls back to root / ST persona) or set a new value                    |
| Re-enabling global config didn't populate the UI                | You canceled on the diff dialog — click Enable again and choose Inherit                                |

***

## Next Steps

<CardGroup>
  <Card title="Install SillyTavern" icon="download" href="https://docs.sillytavern.app/installation/">
    New to SillyTavern? Start here — install guide for macOS, Linux, Windows, Docker.
  </Card>

  <Card title="Agent Skill for Setup" icon="wand-magic-sparkles" href="https://github.com/plastic-labs/sillytavern-honcho/blob/main/skills/setup/SKILL.md">
    Agent-assisted install — idempotent, structural patches, end-to-end verification.
  </Card>

  <Card title="GitHub Repository" icon="github" href="https://github.com/plastic-labs/sillytavern-honcho">
    Source code, issues, and install scripts.
  </Card>

  <Card title="Honcho Architecture" icon="sitemap" href="../../documentation/core-concepts/architecture">
    Learn about peers, sessions, and dialectic reasoning.
  </Card>
</CardGroup>


# Vercel AI SDK
Source: https://honcho.dev/docs/v3/guides/integrations/vercel-ai-sdk

Add persistent user memory and reasoning to any Vercel AI SDK app with Honcho

Integrate Honcho with the Vercel AI SDK to build AI apps that remember users across sessions. The [Vercel AI SDK](https://sdk.vercel.ai) is an open-source TypeScript toolkit for building AI-powered apps with a unified API across providers. This guide shows you how to wrap any `generateText` or `streamText` call with Honcho's memory middleware and reasoning tools.

<Note>
  The full package source and examples are available on [GitHub](https://github.com/plastic-labs/vercel-ai-sdk-package).
</Note>

## What We're Building

We'll wire Honcho into a Vercel AI SDK app so the model receives context from past conversations and can query what it knows about the user mid-generation. Here's how the pieces fit together:

* **Vercel AI SDK** handles model calls and streaming
* **Honcho** stores messages and retrieves user context before each generation
* **Your model provider** can be Anthropic, OpenAI, Google, etc.

The key benefit: you don't manually manage conversation history across sessions. Honcho handles persistence and context injection — the model always has a rich picture of who it's talking to. (New to Honcho's primitives? See [peers and sessions](/docs/v3/documentation/core-concepts/architecture).)

## Setup

Install the package:

<CodeGroup>
  ```bash npm theme={null}
  npm install @honcho-ai/vercel-ai-sdk
  ```

  ```bash pnpm theme={null}
  pnpm add @honcho-ai/vercel-ai-sdk
  ```

  ```bash yarn theme={null}
  yarn add @honcho-ai/vercel-ai-sdk
  ```

  ```bash bun theme={null}
  bun add @honcho-ai/vercel-ai-sdk
  ```
</CodeGroup>

Get your API key at [app.honcho.dev](https://app.honcho.dev).

```bash theme={null}
HONCHO_API_KEY=your-api-key
HONCHO_WORKSPACE_ID=your-workspace-id
```

## Use the Skill

The package ships a Skill that can walk an agent through wiring Honcho into your Vercel AI SDK app automatically — it greps for your `generateText` / `streamText` call sites, asks where `userId` / `sessionId` come from, and applies the integration in place.

```bash theme={null}
npx skills add plastic-labs/vercel-ai-sdk
```

Then invoke `/honcho-vercel-ai-sdk`.

<Accordion title="Alternative: manual symlink from npm package">
  If you've already installed `@honcho-ai/vercel-ai-sdk` via npm, you can symlink the skill directly. Example shown is for Claude Code:

  ```bash theme={null}
  mkdir -p ~/.claude/skills/honcho-vercel-ai-sdk
  ln -sf "$(pwd)/node_modules/@honcho-ai/vercel-ai-sdk/skills/honcho-vercel-ai-sdk/SKILL.md" \
         ~/.claude/skills/honcho-vercel-ai-sdk/SKILL.md
  ```

  Restart the session, then invoke `/honcho-vercel-ai-sdk`.
</Accordion>

## Create a Provider Instance

`createHoncho()` is the entry point. It reads your API key and workspace from environment variables and returns a provider object with `middleware()`, `tools()`, and `send()`.

```typescript theme={null}
import { createHoncho } from '@honcho-ai/vercel-ai-sdk';

const honcho = createHoncho();
```

You can set a stable `defaultAssistantId` on the provider to identify the AI peer across all calls:

```typescript theme={null}
const honcho = createHoncho({
  defaultAssistantId: 'my-assistant',
});
```

## Add Middleware

`honcho.middleware()` is compatible with `wrapLanguageModel`. Two things happen on each call:

1. **Before generation** — Honcho fetches the user's representation, peer card, session summary, and recent messages and injects them into the system prompt
2. **After generation** — the user message and assistant response are stored back in Honcho with correct peer attribution

```typescript theme={null}
import { createHoncho } from '@honcho-ai/vercel-ai-sdk';
import { wrapLanguageModel, generateText } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';

const honcho = createHoncho();

const model = wrapLanguageModel({
  model: anthropic('claude-sonnet-4-6'),
  middleware: honcho.middleware({
    userId: 'user-abc',
    sessionId: 'session-123',
  }),
});

const { text } = await generateText({
  model,
  prompt: 'What should I focus on today?',
});
```

Pass `userId` and `sessionId` per request — no session handles to construct. Both default to lazily generated IDs if omitted, which is fine for local scripts but not for multi-user server traffic.

## Add Tools

`honcho.tools()` gives the model six tools it can call mid-generation to query or update what it knows about the user:

| Tool                        | What it does                                                                                                           |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `honcho_chat`               | Dialectic reasoning — ask natural-language questions about the user; answers synthesized from full interaction history |
| `honcho_context`            | Short summary of recent context within the session                                                                     |
| `honcho_search`             | Semantic search over stored conversation messages                                                                      |
| `honcho_search_conclusions` | Query derived conclusions: personality traits, preferences, behavioral patterns                                        |
| `honcho_get_representation` | Full synthesized profile of the user                                                                                   |
| `honcho_save_conclusion`    | Persist an observation about the user for future sessions                                                              |

Pass the same `userId` and `sessionId` to `honcho.tools()` so tool calls bind to the same peers as the middleware:

```typescript theme={null}
import { generateText, stepCountIs } from 'ai';

const { text } = await generateText({
  model,
  tools: honcho.tools({
    userId: 'user-abc',
    sessionId: 'session-123',
  }),
  stopWhen: stepCountIs(3),
  prompt: 'Based on our conversations, what do I care about most?',
});
```

## Complete Example

Here's a full working example combining middleware and tools.

Want a runnable end-to-end version? See the [Full Script](#full-script).

```typescript theme={null}
import { createHoncho } from '@honcho-ai/vercel-ai-sdk';
import { wrapLanguageModel, generateText, stepCountIs } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';

const honcho = createHoncho({
  defaultAssistantId: 'assistant',
});

const userId = 'user-abc';
const sessionId = 'session-123';

const model = wrapLanguageModel({
  model: anthropic('claude-sonnet-4-6'),
  middleware: honcho.middleware({ userId, sessionId }),
});

const { text } = await generateText({
  model,
  tools: honcho.tools({ userId, sessionId }),
  stopWhen: stepCountIs(3),
  prompt: 'What should we work on today?',
});

console.log(text);
```

## Streaming

`streamText` works the same way — middleware handles persistence after the stream completes:

```typescript theme={null}
import { createHoncho } from '@honcho-ai/vercel-ai-sdk';
import { wrapLanguageModel, streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

const honcho = createHoncho();

const userId = 'user-abc';
const sessionId = 'session-456';

const model = wrapLanguageModel({
  model: openai('gpt-4o'),
  middleware: honcho.middleware({ userId, sessionId }),
});

const result = streamText({
  model,
  tools: honcho.tools({ userId, sessionId }),
  prompt: 'What should we work on today?',
});

for await (const chunk of result.textStream) {
  process.stdout.write(chunk);
}
```

## Using with `messages`

If your app already manages conversation history and passes a `messages` array directly, set `injectHistory: false` to prevent Honcho from prepending duplicate history:

```typescript theme={null}
honcho.middleware({
  userId,
  sessionId,
  injectHistory: false, // don't prepend history — we're passing messages directly
})
```

Honcho still injects the user's representation and peer card into the system prompt, and still persists messages after generation. With `injectHistory: false` you must pass a `messages` array — without either `messages` or `prompt`, the Vercel AI SDK throws `Invalid prompt: prompt or messages must be defined`.

## Verifying the Integration

### 1. Isolate Honcho's Contribution

Let's confirm the memory is actually coming from Honcho and not your app's existing conversation history.

Two ways to check: 1) through a developer method 2) through the UI.

**Token delta (developer check).** On a session with a few prior turns, run the same prompt twice — once with `injectHistory: false` and once without.

Compare `result.usage.inputTokens`:

```typescript theme={null}
const baseline = await generateText({
  model: wrapLanguageModel({
    model: anthropic('claude-sonnet-4-6'),
    middleware: honcho.middleware({ userId, sessionId, injectHistory: false }),
  }),
  prompt: 'What do you know about my preferences?',
});

const injected = await generateText({
  model: wrapLanguageModel({
    model: anthropic('claude-sonnet-4-6'),
    middleware: honcho.middleware({ userId, sessionId }),
  }),
  prompt: 'What do you know about my preferences?',
});

console.log(injected.usage.inputTokens - baseline.usage.inputTokens);
```

A positive delta is Honcho's representation, peer card, and session summary being injected into the system prompt. Expect \~0 on a fresh peer — the deriver runs asynchronously after messages persist, so injected context only populates after a few prior turns.

**Dashboard (UI check).** Open [app.honcho.dev/explore](https://app.honcho.dev/explore), select your workspace, and confirm your peer and session appear under the Peers and Sessions tables.

With Honcho's contribution isolated, the rest of this section shows what the integration feels like in practice.

### 2. First turn

Send any message. The model responds normally — nothing is stored yet. Context injection returns empty on the first turn.

### 3. Build memory across turns

Have a multi-turn conversation and share something about yourself:

```text theme={null}
I prefer concise answers and I mostly work in TypeScript.
```

After a few turns, ask:

```text theme={null}
What do you know about my preferences?
```

If the model references TypeScript and concise answers without being told again in this session, memory is working.

### 4. Cross-session recall

Start a new session (new `sessionId`) with the same `userId`. Ask:

```text theme={null}
Call your honcho_search tool with the query 'TypeScript' and quote the exact verbatim message that contained TypeScript. Do not paraphrase.
```

If the search returns a message from the prior session word-for-word, peer-scoped retrieval is crossing session boundaries. `honcho_search` queries the user's messages across all their sessions and doesn't depend on the deriver, so it works regardless of how short the prior session was.

To confirm the tool actually fired, inspect `result.steps[i].toolCalls`:

```typescript theme={null}
const toolFires = result.steps?.flatMap((step, i) =>
  (step.toolCalls ?? []).map((tc) => ({ step: i, tool: tc.toolName, input: tc.input }))
) ?? [];
console.log(toolFires);
// [{ step: 0, tool: "honcho_search", input: { query: "TypeScript", limit: 10 } }]
```

When the model takes more than one turn (call a tool, see the result, then answer), the top-level `result.toolCalls` is empty — check inside each `step`.

## Full Script

<Accordion title="honcho_vercel_chat.ts">
  ```typescript theme={null}
  /**
   * Multi-turn chat with Honcho memory + Vercel AI SDK.
   *
   * Prerequisites:
   * 1. Install dependencies:
   *    npm install @honcho-ai/vercel-ai-sdk ai @ai-sdk/anthropic dotenv
   * 2. Set environment variables in `.env`:
   *    HONCHO_API_KEY=your-honcho-api-key
   *    HONCHO_WORKSPACE_ID=your-workspace-id
   *    ANTHROPIC_API_KEY=your-anthropic-api-key
   * 3. Run with: npx tsx honcho_vercel_chat.ts
   *
   * Pass a stable userId from your auth system and a sessionId for the conversation
   * thread; Honcho handles persistence and context injection on every turn.
   */

  import 'dotenv/config';
  import { createHoncho } from '@honcho-ai/vercel-ai-sdk';
  import { wrapLanguageModel, generateText, stepCountIs } from 'ai';
  import { anthropic } from '@ai-sdk/anthropic';
  import * as readline from 'node:readline/promises';
  import { stdin as input, stdout as output } from 'node:process';

  const honcho = createHoncho({
    defaultAssistantId: 'assistant',
  });

  const userId = process.env.USER_ID ?? 'demo-user';
  const sessionId = process.env.SESSION_ID ?? `session-${Date.now()}`;

  const model = wrapLanguageModel({
    model: anthropic('claude-sonnet-4-6'),
    middleware: honcho.middleware({ userId, sessionId }),
  });

  async function chat(prompt: string): Promise<string> {
    const { text } = await generateText({
      model,
      tools: honcho.tools({ userId, sessionId }),
      stopWhen: stepCountIs(3),
      prompt,
    });
    return text;
  }

  async function main() {
    const rl = readline.createInterface({ input, output });
    console.log(`Honcho session: ${sessionId} (user: ${userId})`);
    console.log('Type a message, or "exit" to quit.\n');

    while (true) {
      const userMessage = (await rl.question('you > ')).trim();
      if (!userMessage || userMessage === 'exit') break;
      const reply = await chat(userMessage);
      console.log(`bot > ${reply}\n`);
    }

    rl.close();
  }

  main().catch((err) => {
    console.error(err);
    process.exit(1);
  });
  ```
</Accordion>

## Next Steps

<CardGroup>
  <Card title="Github Repository" icon="github" href="https://github.com/plastic-labs/vercel-ai-sdk-package">
    Source, tests, and full API reference for @honcho-ai/vercel-ai-sdk.
  </Card>

  <Card title="Honcho Architecture" icon="sitemap" href="/v3/documentation/core-concepts/architecture">
    Learn about peers, sessions, and dialectic reasoning.
  </Card>

  <Card title="Self-Hosting Guide" icon="server" href="/v3/contributing/self-hosting">
    Run Honcho locally with your Vercel AI SDK app.
  </Card>

  <Card title="Vercel AI SDK Docs" icon="book" href="https://sdk.vercel.ai">
    wrapLanguageModel, middleware, and tool use reference.
  </Card>
</CardGroup>


# Zo Computer
Source: https://honcho.dev/docs/v3/guides/integrations/zo-computer

Add persistent memory to Zo Computer skills using Honcho

[Zo Computer](https://zo.computer) is a cloud AI platform where users build reusable workflows called skills. The Honcho memory skill gives any Zo workflow persistent memory — saving conversations, answering questions about past interactions, and injecting context into LLM prompts.

<Note>
  The full source code is available on [GitHub](https://github.com/plastic-labs/honcho/tree/main/examples/zo) with working tests and Zo marketplace submission instructions.
</Note>

## What It Does

The skill provides three tools that any Zo workflow can call:

| Tool           | Description                                                                 |
| -------------- | --------------------------------------------------------------------------- |
| `save_memory`  | Save user or assistant messages to a Honcho session                         |
| `query_memory` | Ask natural language questions about what Honcho remembers                  |
| `get_context`  | Retrieve conversation history formatted for LLM use (OpenAI message format) |

## Setup

Install dependencies:

```bash theme={null}
pip install honcho-ai python-dotenv
```

Set your environment variables:

```bash theme={null}
HONCHO_API_KEY=your-api-key
HONCHO_WORKSPACE_ID=default  # optional, defaults to "default"
```

Get your API key at [app.honcho.dev](https://app.honcho.dev).

## Quick Start

```python theme={null}
from tools.save_memory import save_memory
from tools.query_memory import query_memory
from tools.get_context import get_context

# Save conversation turns
save_memory("alice", "I love hiking in the mountains", "user", "session-1")
save_memory("alice", "That sounds wonderful!", "assistant", "session-1")

# Query what Honcho remembers
answer = query_memory("alice", "What are my hobbies?", "session-1")
print(answer)  # "Alice enjoys hiking in the mountains."

# Get context ready for an LLM call
messages = get_context("alice", "session-1", "assistant", tokens=4000)
# Returns [{"role": "user", "content": "..."}, ...]
```

## Saving Messages

`save_memory` creates peers and sessions automatically on first use and persists the message.

```python theme={null}
save_memory(
    user_id="alice",          # unique user identifier
    content="Hello!",         # message text
    role="user",              # "user" or "assistant"
    session_id="session-1",   # conversation identifier
    assistant_id="assistant", # optional, defaults to "assistant"
)
```

## Querying Memory

`query_memory` uses Honcho's Dialectic API to answer natural language questions grounded in stored memory.

```python theme={null}
answer = query_memory(
    user_id="alice",
    query="What are my interests?",
    session_id="session-1",  # optional — omit to query global memory
)
```

## Retrieving Context

`get_context` fetches recent conversation history within a token budget and returns it in OpenAI message format — ready to pass directly to an LLM.

```python theme={null}
messages = get_context(
    user_id="alice",
    session_id="session-1",
    assistant_id="assistant",
    tokens=4000,  # max tokens to include
)
# Use directly: llm.chat.completions.create(messages=messages)
```

## Concept Mapping

| Zo Computer  | Honcho    |
| ------------ | --------- |
| Account      | Workspace |
| User         | Peer      |
| Conversation | Session   |
| Message      | Message   |

## Publishing to the Zo Marketplace

To submit the skill to the [Zo Skills Registry](https://github.com/zocomputer/skills):

1. Fork the `zocomputer/skills` repository
2. Copy the `examples/zo` directory into `/Community/honcho-memory/` in your fork
3. Run `bun validate` to check the skill format
4. Submit a pull request

## Next Steps

<CardGroup>
  <Card title="Source Code" icon="github" href="https://github.com/plastic-labs/honcho/tree/main/examples/zo">
    Full source, tests, and SKILL.md for the Zo integration
  </Card>

  <Card title="Honcho Architecture" icon="sitemap" href="/v3/documentation/core-concepts/architecture">
    Understand peers, sessions, and how memory works
  </Card>

  <Card title="Chat API" icon="brain" href="/v3/documentation/features/chat">
    Learn more about querying peer memory with the Dialectic API
  </Card>

  <Card title="Get Context" icon="messages" href="/v3/documentation/features/get-context">
    Details on retrieving and formatting conversation context
  </Card>
</CardGroup>


# Migrating from Mem0
Source: https://honcho.dev/docs/v3/guides/migrations/mem0

A guide to migrate from Mem0 to Honcho

Interested in transferring your data from Mem0 to Honcho? This guide covers why to switch, how to migrate your data, and differences between the two products.

## Why Honcho?

Mem0 & Honcho both store your data. Only Honcho reasons about it. [Read more about our approach](https://blog.plasticlabs.ai/blog/Memory-as-Reasoning).

**Compounding Insights** - Honcho extracts insights that build on each other over time. The more your users interact, the richer and more accurate their profiles become.

**Superior Performance** - Higher accuracy on memory retrieval benchmarks with faster inference times (more details soon!).

**Competitive Pricing** - Mem0 charges for retrieval, not ingestion. Meaning you pay to access your own data. Honcho offers straightforward pricing with a generous free tier.

**Advanced Multi-Peer Sessions** - Honcho offers configurable observation settings (who builds memories about whom), representation-based queries between participants, and first-class peer objects.

<Note>
  We would love to support the transfer and cost—just [book a call!](https://cal.com/team/plasticlabs/migration-to-honcho)
</Note>

## Quick Migration

For the best results, we recommend importing your raw messages directly into Honcho. This gives Honcho the full context to build rich, accurate representations and enables features like session summaries.

However, if you'd like to get started quickly, you can migrate your existing Mem0 memories directly as **conclusions**.

<Info>
  Get your API key at [app.honcho.dev/api-keys](https://app.honcho.dev/api-keys). New accounts start with \$100 credits.
</Info>

<CodeGroup>
  ```python Python theme={null}
  # pip install mem0ai honcho-ai
  from mem0 import MemoryClient
  from honcho import Honcho

  # Export from Mem0
  mem0 = MemoryClient(api_key="your-mem0-api-key")
  memories = mem0.get_all(filters={"user_id": "user123"}, page_size=100)

  # Initialize Honcho
  honcho = Honcho(api_key="your-honcho-api-key")
  user = honcho.peer("user123")
  session = honcho.session("imported")
  session.add_peers([user])

  # Import memories directly as conclusions
  conclusions = []
  for memory in memories['results']:
      content = memory.get("memory") or memory.get("messages", [{}])[0].get("content", "")
      if content:
          conclusions.append({"content": content, "session_id": "imported"})

  # Batch create conclusions (up to 100 at a time)
  if conclusions:
      user.conclusions.create(conclusions)

  print(f"Migrated {len(conclusions)} memories as conclusions!")
  ```

  ```typescript TypeScript theme={null}
  // npm install mem0ai @honcho-ai/sdk
  import MemoryClient from "mem0ai";
  import { Honcho } from "@honcho-ai/sdk";

  // Export from Mem0
  const mem0 = new MemoryClient({ apiKey: "your-mem0-api-key" });
  const memories = await mem0.getAll({ filters: { user_id: "user123" }, page_size: 100 });

  // Initialize Honcho
  const honcho = new Honcho({ apiKey: "your-honcho-api-key" });
  const user = await honcho.peer("user123");
  const session = await honcho.session("imported");
  await session.addPeers([user]);

  // Import memories directly as conclusions
  const conclusions = memories.results
    .map(memory => ({
      content: memory.memory || memory.messages?.[0]?.content || "",
      sessionId: "imported"
    }))
    .filter(c => c.content);

  // Batch create conclusions (up to 100 at a time)
  if (conclusions.length > 0) {
    await user.conclusions.create(conclusions);
  }

  console.log(`Migrated ${conclusions.length} memories as conclusions!`);
  ```
</CodeGroup>

That's it! The user's Mem0 memories are now searchable in Honcho as conclusions. For richer representations with deductive reasoning and session summaries, consider importing your raw messages as described in the [Step-by-Step Migration](#step-by-step-migration) section.

For more details on replacing Mem0 API calls with Honcho equivalents go to [API Comparison](#api-comparison).

## Step-by-Step Migration

Prefer a more detailed walkthrough? Follow these steps:

### 1. Export User Messages

Importing raw user messages gives Honcho the full conversational context to build the most accurate representations. We recommend using a data structure that preserves the session and peer structure.

<Note>
  If you need any help with this transfer or have any questions, please reach out at [hello@plasticlabs.ai](mailto:hello@plasticlabs.ai) or [book a call!](https://cal.com/team/plasticlabs/migration-to-honcho)
</Note>

Alternatively, if you want to import the Mem0 memories, follow the example above and find more info in Mem0's [export API documentation](https://docs.mem0.ai/cookbooks/essentials/exporting-memories).

### 2. Install the Honcho SDK

<CodeGroup>
  ```bash Python (uv) theme={null}
  uv add honcho-ai
  ```

  ```bash Python (pip) theme={null}
  pip install honcho-ai
  ```

  ```bash TypeScript (npm) theme={null}
  npm install @honcho-ai/sdk
  ```

  ```bash TypeScript (yarn) theme={null}
  yarn add @honcho-ai/sdk
  ```

  ```bash TypeScript (pnpm) theme={null}
  pnpm add @honcho-ai/sdk
  ```
</CodeGroup>

### 3. Initialize the Honcho Client

<Info>
  Get your API key at [app.honcho.dev/api-keys](https://app.honcho.dev/api-keys). New accounts start with \$100 credits.
</Info>

<CodeGroup>
  ```python Python theme={null}
  from honcho import Honcho

  honcho = Honcho( api_key="your-api-key" )
  ```

  ```typescript TypeScript theme={null}
  import { Honcho } from '@honcho-ai/sdk';

  const honcho = new Honcho({apiKey: process.env.HONCHO_API_KEY!});
  ```
</CodeGroup>

### 4. Import Your Data

This is a possible implementation using raw user messages. Adapt the data structure to match your exported format.

<CodeGroup>
  ```python Python theme={null}
  # Example data structure (preserving message history with timestamps):
  exported_data = {
      "session-1": {
          "user123": [
              {"content": "I prefer dark mode", "timestamp": "2024-01-15T10:30:00Z"},
              {"content": "My name is Alex", "timestamp": "2024-01-15T10:31:00Z"},
          ],
          "user456": [
              {"content": "I work in finance", "timestamp": "2024-01-15T11:00:00Z"},
              {"content": "I like concise responses", "timestamp": "2024-01-15T11:02:00Z"},
          ],
      },
      "session-2": {
          "user123": [
              {"content": "Meeting notes from last week...", "timestamp": "2024-01-16T09:00:00Z"},
          ],
      }
  }

  # Import into Honcho
  for session_name, users in exported_data.items():
      session = honcho.session(session_name)

      for user_id, messages in users.items():
          peer = honcho.peer(user_id)
          session.add_peers([peer])

          # Sort by timestamp to preserve message order
          sorted_messages = sorted(messages, key=lambda m: m["timestamp"])
          session.add_messages([peer.message(m["content"]) for m in sorted_messages])
  ```

  ```typescript TypeScript theme={null}
  // Example data structure (preserving message history with timestamps):
  interface Message {
    content: string;
    timestamp: string;
  }
  const exportedData: Record<string, Record<string, Message[]>> = {
    "session-1": {
      "user123": [
        { content: "I prefer dark mode", timestamp: "2024-01-15T10:30:00Z" },
        { content: "My name is Alex", timestamp: "2024-01-15T10:31:00Z" },
      ],
      "user456": [
        { content: "I work in finance", timestamp: "2024-01-15T11:00:00Z" },
        { content: "I like concise responses", timestamp: "2024-01-15T11:02:00Z" },
      ],
    },
    "session-2": {
      "user123": [
        { content: "Meeting notes from last week...", timestamp: "2024-01-16T09:00:00Z" },
      ],
    }
  };

  // Import into Honcho
  for (const [sessionName, users] of Object.entries(exportedData)) {
    const session = await honcho.session(sessionName);

    for (const [userId, messages] of Object.entries(users)) {
      const peer = await honcho.peer(userId);
      await session.addPeers([peer]);

      // Sort by timestamp to preserve message order
      const sortedMessages = messages.sort((a, b) =>
        new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
      );
      await session.addMessages(sortedMessages.map((m) => peer.message(m.content)));
    }
  }
  ```
</CodeGroup>

### 5. Update Your Application Code

Reference the [API Comparison](#api-comparison) to replace your Mem0 API calls with the Honcho equivalents.

## API Comparison

### Core Operations

| Operation           | Mem0                                             | Honcho                                                | Notes                                               |
| ------------------- | ------------------------------------------------ | ----------------------------------------------------- | --------------------------------------------------- |
| **Initialize**      | `MemoryClient(api_key=...)`                      | `Honcho(api_key=...)`                                 |                                                     |
| **Identity**        | `user_id` string param                           | `peer = honcho.peer("id")`                            | Peers can be users or AI agents                     |
| **Add messages**    | `client.add(messages, user_id=...)`              | `session.add_messages([peer.message(...)])`           | Session-scoped, triggers reasoning                  |
| **Add conclusions** |                                                  | `peer.conclusions.create([...])`                      | Direct conclusion or "memory" import, no processing |
| **Search**          | `client.search(query, filters={"user_id": ...})` | `peer.search(query)` or `peer.conclusions.query(...)` | Scoped to peer or session                           |
| **List all**        | `client.get_all(filters={"user_id": ...})`       | `session.messages()` or `peer.conclusions.list()`     | Messages or conclusions                             |
| **Update**          | `client.update(memory_id, data=...)`             | `honcho.update_message(message, metadata=...)`        | Metadata updates only                               |
| **Delete**          | `client.delete(memory_id)`                       | `peer.conclusions.delete(id)` or `session.delete()`   | Conclusion or session-level                         |

### Honcho-Only Capabilities

Mem0 requires manual assembly of context from `search()` results. Honcho's `session.context()` returns a ready-to-use `SessionContext` object with built-in token limits, auto-included summaries, and format helpers (`.to_openai()`, `.to_anthropic()`).

<Card title="Get Context" icon="window-restore" href="../../documentation/features/get-context">
  Learn more about token-optimized context retrieval
</Card>

Mem0's `search()` returns basic vector, semantic, or raw memory matches. Honcho's `peer.chat()` enables your agent to *reason* about what it knows—returning synthesized natural language insights with streaming support and scoped queries.

<Card title="Chat Endpoint" icon="brain" href="../../documentation/features/chat">
  Learn more about inference-powered queries
</Card>

Additional features with **no Mem0 equivalent**:

| Honcho Method                         | Description                                               | Use Case                              |
| ------------------------------------- | --------------------------------------------------------- | ------------------------------------- |
| `peer.get_card()` / `peer.set_card()` | Stable biographical facts (name, preferences, background) | User profiles, personalization        |
| `session.representation(peer)`        | Cached psychological analysis (mental state, intentions)  | Real-time adaptation                  |
| `session.summaries()`                 | Auto-generated short/long session summaries               | Conversation continuity               |
| `SessionPeerConfig`                   | Configure observation settings (who learns about whom)    | Privacy controls, role-based learning |

## Next Steps

<CardGroup>
  <Card title="Architecture" icon="rocket" href="../../documentation/core-concepts/architecture">
    Understand peers and sessions
  </Card>

  <Card title="Chat API" icon="brain" href="../../documentation/features/chat">
    Inference responses
  </Card>

  <Card title="Guides" icon="book" href="../../guides/overview">
    Integration examples
  </Card>
</CardGroup>

Questions? Join our [Discord](https://discord.gg/honcho) or open an issue on [GitHub](https://github.com/plastic-labs/honcho/issues).


# Guides, Cookbooks, and Integrations
Source: https://honcho.dev/docs/v3/guides/overview

Helpful guides and design patterns for building with Honcho

Honcho plugs into whatever you're already building. Add memory to an AI assistant, connect an external data source, wire Honcho into your agent framework, or migrate from another provider.

## Recipes

Compose the core primitives across multiple integrations:

<CardGroup>
  <Card title="Unified Memory Setup" icon="diagram-project" href="/v3/guides/recipes/unified-memory-setup">
    One shared workspace across a chat companion, coding agent, autonomous agent, and ingestion job
  </Card>
</CardGroup>

## AI Assistants

Add persistent memory to AI assistants and agents:

<CardGroup>
  <Card title="Claude Code" icon="terminal" href="/v3/guides/integrations/claude-code">
    Long-term memory that survives context wipes, session restarts, and project switches
  </Card>

  <Card title="OpenCode" icon="code" href="/v3/guides/integrations/opencode">
    Persistent memory for OpenCode sessions, with per-directory, per-repo, or branch-scoped session mapping
  </Card>

  <Card title="MCP Server" icon="star-of-life" href="/v3/guides/integrations/mcp">
    Add Honcho memory to Claude Desktop, Cursor, Windsurf, Cline, and any MCP client
  </Card>

  <Card title="Hermes Agent" icon="bolt" href="/v3/guides/community/hermes">
    Cross-session memory for Nous Research's Hermes agent
  </Card>

  <Card title="OpenClaw" icon="lobster" href="/v3/guides/integrations/openclaw">
    Memory across every channel — WhatsApp, Telegram, Discord, Slack, and more
  </Card>

  <Card title="Agent Zero" icon="triangle" href="/v3/guides/community/agent0">
    Persistent memory plugin for the Agent Zero framework
  </Card>
</CardGroup>

## Platform Connectors

Connect external platforms to Honcho:

<CardGroup>
  <Card title="Discord Bot" icon="discord" href="/v3/guides/discord">
    Build a Discord bot that remembers users across conversations
  </Card>

  <Card title="Telegram Bot" icon="telegram" href="/v3/guides/telegram">
    Create a Telegram bot with persistent user understanding
  </Card>

  <Card title="Gmail" icon="envelope" href="/v3/guides/gmail">
    Import email threads into Honcho — peers, sessions, and messages from your inbox
  </Card>

  <Card title="Granola" icon="calendar" href="/v3/guides/granola">
    Ingest meeting transcripts with speaker turns and participant data
  </Card>

  <Card title="Paperclip" icon="paperclip" href="/v3/guides/integrations/paperclip">
    Add Honcho memory to Paperclip companies, agents, issues, and documents
  </Card>

  <Card title="Reachy Mini" icon="robot" href="/v3/guides/integrations/reachy-mini">
    Build an embodied voice robot with long-term memory
  </Card>
</CardGroup>

## Agent Frameworks

Use Honcho as a memory layer in your agent orchestration stack:

<CardGroup>
  <Card title="LangGraph" icon="diagram-project" href="/v3/guides/integrations/langgraph">
    Add persistent memory and theory of mind to your LangGraph agents
  </Card>

  <Card title="CrewAI" icon="users-gear" href="/v3/guides/integrations/crewai">
    Give CrewAI agents memory that persists across sessions
  </Card>

  <Card title="Zo Computer" icon="bolt" href="/v3/guides/integrations/zo-computer">
    Persistent memory skill for Zo Computer AI workflows
  </Card>

  <Card title="n8n" icon="share-nodes" href="/v3/guides/integrations/n8n">
    Build intelligent automation workflows with persistent memory
  </Card>
</CardGroup>

## Migrations

Coming from another memory provider?

<CardGroup>
  <Card title="Migrate from Mem0" icon="arrow-right-arrow-left" href="/v3/guides/migrations/mem0">
    Transfer your data and update your integration code
  </Card>
</CardGroup>


# Unified Memory Setup
Source: https://honcho.dev/docs/v3/guides/recipes/unified-memory-setup

Wire one shared Honcho workspace across a chat companion, a coding agent, an autonomous agent, and a scheduled ingestion job

<Info>
  This is a how-to, not an intro. It assumes you know what workspaces, peers, and
  sessions are. If you don't, start with [Core Concepts](/docs/v3/documentation/core-concepts/).
</Info>

This guide wires four integration points into a single Honcho setup: a
chat companion (Discord/Slack), a coding agent (Claude Code), an autonomous agent
(Hermes), and a cron job that ingests external data. They share **one workspace** and
**one peer** for the user, so everything Honcho learns about your user in one place is
available everywhere else. Each section below notes the per-host setup.

***

## 1. Chat companion (Discord / Slack)

**One session per conversation surface, one peer per participant.** The channel, thread,
or DM is the session; everyone who speaks in it gets their own peer:

* Channel → `discord-channel-{channel_id}`
* Thread → `discord-thread-{thread_id}`
* DM → `discord-dm-{user_id}`

Derive each peer ID from the immutable platform ID (`discord-{user_id}`), not the
display name (which can change). Keep the display name in peer metadata instead. A shared
channel then naturally holds several human peers in one session, with the bot joining
as its own peer (everyone observed on defaults):

```python theme={null}
session = honcho.session(f"discord-channel-{channel_id}")
session.add_peers([user, assistant])  # plus any other humans in the channel
```

Slack mirrors this with `slack_{user_id}` peers and `slack-{channel}` sessions. For a
full bot walkthrough — message ingestion, watchlists, and storing turns — see the
[Discord guide](/docs/v3/guides/discord).

***

## 2. Coding agent (Claude Code)

**Scope sessions per project directory, prefixed with the user** — `{USER_PEER_ID}-{repo_name}`
— so multiple developers sharing the workspace don't collide on a session ID. Switch
to a `git-branch` scope only when each branch is genuinely a separate line of work.

The Claude Code plugin reads its workspace and peers from `.honcho/config.json`. Point
each host at the same `workspace` and use the same top-level `peerName`, so every host
attributes you to one peer:

```json .honcho/config.json theme={null}
{
  "peerName": "your-user-id",
  "hosts": {
    "claude_code": { "workspace": "my-product", "aiPeer": "claude" },
    "opencode":    { "workspace": "my-product", "aiPeer": "opencode" }
  }
}
```

<Note>
  This is a minimal, illustrative snippet — the real config file carries more fields
  (session maps, recall mode, observation strategy, etc.). See the [integration](/docs/v3/guides/overview/)
  guides for the full schema and per-host options.
</Note>

Add the user peer and the `claude` agent peer (no special observation config needed),
then store turns — stripping `tool_use` blocks from the assistant message so only
substantive explanation lands in the session.

Because this uses the **same user peer** as the companion, a preference the user
states while coding ("keep it simple, pass config directly") is queryable from the
Discord bot via `user.chat(...)`, and vice versa — both write to the same peer
representation.

<Warning>
  **A shared workspace is not the default.** The Honcho plugins — Claude Code, OpenCode,
  Hermes, Cursor — each default to a *per-host* workspace (`Claude_Code`, `hermes`, …),
  keeping memory isolated per tool. The unification above only happens when you set the
  same workspace **and** the same user peer across all of them; otherwise each builds its
  own separate representation.
</Warning>

***

## 3. Autonomous agent (Hermes)

The Hermes Honcho plugin is configured through `honcho.json`, set its `workspace`
and `aiPeer` there. See the [Hermes guide](/docs/v3/guides/integrations/hermes) for the full config schema.

* **Sessions** follow a `session_strategy` (default `per-directory`, like the coding
  agent above; `per-repo` or `per-session` for a fresh Honcho session each run). The
  user peer defaults to `user-{channel}-{chat_id}` unless you pin a `peerName`.
* **Observation** defaults to `directional` — both the user and the `hermes` agent
  peer are observed, consistent with the defaults above, so Hermes builds a
  representation of itself as well as the user.
* Hermes exposes Honcho as agent **tools** (`honcho_reasoning` for synthesized
  answers, plus lighter `honcho_search` and `honcho_context` lookups) and decides when
  to call them mid-task. Unlike other sources, you write no retrieval code —
  the agent pulls cross-session context on its own.

***

## 4. Scheduled data ingestion (cron)

A scheduled job feeds external data (emails, meeting notes, CRM records) into Honcho.
Attribute the messages to the peer the data is *about* — not to an agent — and group
them into a session. **How you scope that session is the main decision here**, because
it controls when Honcho reasons over the data (more on that below).

```python theme={null}
from datetime import datetime, timezone

session = honcho.session(f"email-import-{datetime.now(timezone.utc):%Y-%m-%d}")
session.add_peers([user])

messages = [
    user.message(
        f"Subject: {e['subject']}\nFrom: {e['from']}\n\n{e['body']}",
        metadata={"source": "gmail", "thread_id": e["thread_id"]},
        created_at=e["timestamp"],  # the event's time, NOT import time
    )
    for e in emails
]
# add_messages accepts at most 100 messages per call — split into requests of 100
for i in range(0, len(messages), 100):
    session.add_messages(messages[i:i + 100])
```

Honcho batches reasoning until a peer accumulates \~1,000 tokens *within a single session*,
with a default age-based flush for quiet tails
([token batching](/docs/v3/documentation/core-concepts/reasoning#token-batching)). Scope the
session to the volume you ingest:

* **High-volume runs** (a day of emails, a CRM export) clear the threshold easily — a
  per-run session like `email-import-{date}` is fine.
* **Low-volume or trickle imports** (a few short records at a time) should append to
  one **ongoing per-source session** (e.g. `email-import-gmail`), so content
  accumulates across runs instead of fragmenting into thin sessions that each flush
  later with little context.

The [Gmail](/docs/v3/guides/gmail) and [Granola](/docs/v3/guides/granola) guides are related
import examples.

<Tip>
  If a cron run also posts as a deterministic agent (a bot or tool agent whose behavior
  you fully control), set `observe_me=False` on that peer so Honcho doesn't spend
  reasoning modeling it. Its messages still land in the session for context.

  ```python theme={null}
  agent = honcho.peer("cron_agent", configuration=PeerConfig(observe_me=False))
  ```
</Tip>

***

## What you end up with

From any integration, the same call — `user.chat("What is this user working on, and
what do they care about?")` — draws on all four sources at once: Discord chats, coding
decisions, Hermes task runs, and imported emails. They blend because:

* **One workspace and one user peer**, so the representation accumulates in one place
  instead of fragmenting into `user-discord`, `user-cursor`, etc.
* **Sessions scoped to the live interaction** (channel, repo, task run, import batch),
  so local context stays coherent while the user peer carries the long view.

## Next Steps

<CardGroup>
  <Card title="Design Patterns" icon="cubes" href="/v3/documentation/core-concepts/design-patterns">
    The reasoning behind every decision in this guide.
  </Card>

  <Card title="Get Context" icon="messages" href="/v3/documentation/features/get-context">
    Pull session + cross-session context into your LLM calls.
  </Card>

  <Card title="Granola" icon="microphone" href="/v3/guides/granola">
    An interactive import using the per-import session and created\_at patterns.
  </Card>

  <Card title="OpenClaw" icon="lobster" href="/v3/guides/integrations/openclaw">
    Production multi-platform companion with parent/subagent tracking.
  </Card>
</CardGroup>


# Telegram Bots with Honcho
Source: https://honcho.dev/docs/v3/guides/telegram

Use Honcho to build a Telegram bot with conversational memory and context management.

> Example code is available on [GitHub](https://github.com/plastic-labs/telegram-python-starter)

Any application interface that defines logic based on events and supports
special commands can work easily with Honcho. Here's how to use Honcho with
**Telegram** as an interface. If you're not familiar with Telegram bot
development, the [python-telegram-bot](https://docs.python-telegram-bot.org/en/stable/) docs would be a good
place to start.

## Message Handling

Most Telegram bots have async functions that handle incoming messages. We can use Honcho to store messages by user and session based on the chat context. Take the following function definition for example:

```python theme={null}
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Receive a message from Telegram and respond with a message from our LLM assistant.
    """
    if not validate_message(update, context):
        return

    message_text = update.effective_message.text
    input_text = sanitize_message(message_text, context.bot.username)

    # If the message is empty after sanitizing, ignore it
    if not input_text:
        return

    peer = honcho_client.peer(id=get_peer_id_from_telegram(update))
    session = honcho_client.session(id=str(update.effective_chat.id))

    # Send typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    response = llm(session, input_text)

    await send_telegram_message(update, context, response)

    # Save both the user's message and the bot's response to the session
    session.add_messages(
        [
            peer.message(input_text),
            assistant.message(response),
        ]
    )
```

Let's break down what this code is doing...

```python theme={null}
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not validate_message(update, context):
        return
```

This is how you define a message handler in `python-telegram-bot` that processes incoming messages. We use a helper function `validate_message()` to check if the message should be processed.

## Helper Functions

The code uses several helper functions to keep the main logic clean and readable. Let's examine each one:

### Message Validation

```python theme={null}
def validate_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Determine if the message is valid for the bot to respond to.
    Return True if it is, False otherwise. The bot will respond to:
    - Direct messages (private chats)
    - Group messages that mention the bot or reply to it
    - Messages that are not from the bot itself
    """
    message = update.effective_message

    if not message or not message.text:
        return False

    # Don't respond to our own messages
    if message.from_user.id == context.bot.id:
        return False

    # Always respond in private chats
    if update.effective_chat.type == "private":
        return True

    # In groups, only respond if mentioned or replied to
    if (
        message.reply_to_message
        and message.reply_to_message.from_user.id == context.bot.id
    ):
        return True

    # Check if bot is mentioned
    if message.entities:
        for entity in message.entities:
            if entity.type == "mention":
                username = message.text[entity.offset : entity.offset + entity.length]
                if username == f"@{context.bot.username}":
                    return True

    return False
```

This function centralizes all the logic for determining whether the bot should respond to a message. It handles different chat types:

* **Private chats**: Always respond
* **Group chats**: Only respond when mentioned or when replying to the bot's messages
* **Bot prevention**: Never respond to the bot's own messages

### Message Sanitization

```python theme={null}
def sanitize_message(message_text: str, bot_username: str) -> str | None:
    """Remove the bot's mention from the message content if present"""
    content = message_text.replace(f"@{bot_username}", "").strip()
    if not content:
        return None
    return content
```

This helper removes the bot's mention from the message content, leaving just the actual user input.

### Peer ID Generation

```python theme={null}
def get_peer_id_from_telegram(update: Update) -> str:
    """Get a Honcho peer ID for the message author"""
    return f"telegram_{update.effective_user.id}"
```

This creates a unique peer identifier for each Telegram user by prefixing their Telegram user ID.

### LLM Integration

```python theme={null}
def llm(session, prompt) -> str:
    """
    Call the LLM with the given prompt and chat history.

    You should expand this function with custom logic, prompts, etc.
    """
    messages: list[dict[str, object]] = session.context().to_openai(
        assistant=assistant
    )
    messages.append({"role": "user", "content": prompt})

    try:
        completion = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return f"Error: {e}"
```

This function handles the LLM interaction. It uses Honcho's built-in `to_openai()` method to automatically convert the session context into the format expected by OpenAI's chat completions API.

### Message Sending

```python theme={null}
async def send_telegram_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE, response_content: str
):
    """Send a message to the Telegram chat, splitting if necessary"""
    # Telegram has a 4096 character limit, but we'll use 4000 to be safe
    max_length = 4000

    if len(response_content) <= max_length:
        await update.effective_message.reply_text(response_content)
    else:
        # Split response into chunks at newlines, keeping under max_length chars
        chunks = []
        current_chunk = ""

        for line in response_content.splitlines(keepends=True):
            if len(current_chunk) + len(line) > max_length:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = line
            else:
                current_chunk += line

        if current_chunk:
            chunks.append(current_chunk)

        for chunk in chunks:
            await update.effective_message.reply_text(chunk)
```

This function handles sending messages to Telegram, automatically splitting long responses into multiple messages to stay within Telegram's 4096 character limit. It also includes a typing indicator to show the bot is processing.

## Honcho Integration

The new Honcho peer/session API makes integration much simpler:

```python theme={null}
peer = honcho_client.peer(id=get_peer_id_from_telegram(update))
session = honcho_client.session(id=str(update.effective_chat.id))
```

Here we create a peer object for the user and a session object using the Telegram chat ID. This automatically handles user and session management across both private chats and group conversations.

```python theme={null}
# Save both the user's message and the bot's response to the session
session.add_messages(
    [
        peer.message(input_text),
        assistant.message(response),
    ]
)
```

After generating the response, we save both the user's input and the bot's response to the session using the `add_messages()` method. The `peer.message()` creates a message from the user, while `assistant.message()` creates a message from the assistant.

## Commands

Telegram bots support slash commands natively. Here's how to implement the `/dialectic` command using Honcho's dialectic feature:

```python theme={null}
async def dialectic_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /dialectic command to query the Honcho Dialectic endpoint.
    """
    if not context.args:
        await update.message.reply_text(
            "Please provide a query. Usage: /dialectic <your query>"
        )
        return

    query = " ".join(context.args)

    try:
        peer = honcho_client.peer(id=get_peer_id_from_telegram(update))
        session = honcho_client.session(id=str(update.effective_chat.id))

        response = peer.chat(
            query=query,
            session_id=session.id,
        )

        if response:
            await send_telegram_message(update, context, response)
        else:
            await update.message.reply_text(
                f"I don't know anything about {update.effective_user.first_name} because we haven't talked yet!"
            )
    except Exception as e:
        logger.error(f"Error calling Dialectic API: {e}")
        await update.message.reply_text(
            f"Sorry, there was an error processing your request: {str(e)}"
        )
```

You can also add a `/start` command for user onboarding:

```python theme={null}
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    await update.message.reply_text(
        "Hello! I'm your AI assistant. You can:\n"
        "• Chat with me directly in private messages\n"
        "• Mention me (@username) in groups to get my attention\n"
        "• Use /dialectic <query> to search our conversation history\n\n"
        "Let's start chatting!"
    )
```

## Setup and Configuration

The bot requires several environment variables and setup:

```python theme={null}
honcho_client = Honcho()
assistant = honcho_client.peer(id="assistant", config={"observe_me": False})
openai = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=MODEL_API_KEY)
```

* `honcho_client`: The main Honcho client
* `assistant`: A peer representing the bot/assistant
* `openai`: OpenAI client configured to use OpenRouter

### Application Setup

Register your handlers with the Telegram application:

```python theme={null}
def main():
    """Start the bot"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found in environment variables")
        return

    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("dialectic", dialectic_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Start the bot
    logger.info("Starting Telegram bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
```

## Environment Variables

Your bot needs these environment variables:

```env theme={null}
# Your Telegram bot token from BotFather
BOT_TOKEN=<your-token>

# AI model to use (see OpenRouter for available models)
MODEL_NAME=<your-model>

# Your OpenRouter API key
MODEL_API_KEY=<your-openrouter-api-key>
```

## Chat Types and Behavior

The bot handles different Telegram chat types intelligently:

### Private Chats

* **Behavior**: Responds to all messages
* **Session ID**: Uses the private chat ID
* **Memory**: Maintains conversation history per user

### Group Chats

* **Behavior**: Only responds when mentioned or replied to
* **Session ID**: Uses the group chat ID (shared across all members)
* **Memory**: Maintains group conversation context

## Recap

The new Honcho peer/session API makes Telegram bot integration much simpler and more intuitive. Key patterns we learned:

* **Peer/Session Model**: Users are represented as peers, conversations as sessions
* **Chat Type Handling**: Different validation logic for private vs group chats
* **Automatic Context Management**: `session.context().to_openai()` automatically formats chat history
* **Message Storage**: `session.add_messages()` stores both user and assistant messages
* **Dialectic Queries**: `peer.chat()` enables querying conversation history
* **Command System**: Native Telegram command support with `/start` and `/dialectic`
* **Message Splitting**: Automatic handling of Telegram's character limits
* **Helper Functions**: Clean code organization with focused helper functions

This approach provides a clean, maintainable structure for building Telegram bots with conversational memory and context management across both private conversations and group chats.



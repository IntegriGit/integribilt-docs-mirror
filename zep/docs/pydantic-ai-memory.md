> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Pydantic AI integration

[Pydantic AI](https://ai.pydantic.dev) agents using Zep gain long-term memory backed by a temporal knowledge graph. The `zep-pydantic-ai` package persists each user turn, injects relevant context into the model prompt using Pydantic AI's native `ProcessHistory` capability, and adds an on-demand graph-search tool.

## Core benefits

* **Native `ProcessHistory` capability**: Uses the current Pydantic AI history-processor hook, not a deprecated kwarg
* **Single round-trip**: Persists the user turn and retrieves context in one `add_messages` call
* **Correct under tool calls**: Dedupes per run (keyed by the run ID), so a run that makes tool calls records the turn exactly once
* **On-demand graph search**: A model-callable tool over `graph.search` for explicit lookups
* **Lazy resource creation**: The Zep user and thread are created on first use
* **Graceful degradation**: A Zep failure is logged but never crashes the agent run

## How it works

The integration plugs into Pydantic AI through three components:

* **`ZepDeps`** — a dataclass used as the agent's `deps_type`. It carries the Zep client and the user/thread identity. Construct one per conversation and pass it to `agent.run(..., deps=deps)`; both the history processor and the search tool reach it through `RunContext.deps`.
* **`zep_history_processor`** — registered via `capabilities=[ProcessHistory(zep_history_processor)]`. Pydantic AI runs it before every model request: on the user's turn it persists the latest message via `thread.add_messages(return_context=True)` and prepends Zep's context block as a system message. Because `ProcessHistory` fires once per model request (not once per run), the processor dedupes per run, keyed by the run ID. It persists and retrieves only on the first request of a run and replays the cached context on later requests within that same run, so tool-calling runs never create duplicate episodes.
* **`create_zep_search_tool`** — a factory returning a model-callable tool over `graph.search`. The model decides when to search the knowledge graph; search parameters are pinned at construction.

Call `persist_run` after `agent.run` to persist the assistant's reply. The history processor runs before each model request, so the assistant's reply does not exist yet when it fires; `persist_run` writes that reply once the run completes. Only assistant text is sent, so Zep records one clean assistant message per turn.

## Installation

```bash
pip install zep-pydantic-ai
```

Requires Python 3.11+, `pydantic-ai>=1.107,<2`, and a Zep Cloud API key. Get your API key from [app.getzep.com](https://app.getzep.com).

Set up your environment variables:

```bash
export ZEP_API_KEY="your-zep-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

## Usage

Register the history processor and search tool when building the agent, then pass `ZepDeps` to each run:

```python Python
import asyncio
from pydantic_ai import Agent
from pydantic_ai.capabilities import ProcessHistory
from zep_cloud.client import AsyncZep
from zep_pydantic_ai import (
    ZepDeps,
    zep_history_processor,
    create_zep_search_tool,
    persist_run,
)

zep = AsyncZep(api_key="your-zep-api-key")

agent = Agent(
    "openai:gpt-4o-mini",
    deps_type=ZepDeps,
    capabilities=[ProcessHistory(zep_history_processor)],
    tools=[create_zep_search_tool()],
    instructions="You are a helpful assistant with long-term memory.",
)

async def main() -> None:
    deps = ZepDeps(
        client=zep,
        user_id="user_123",
        thread_id="thread_abc",
        first_name="Jane",
        last_name="Smith",
    )
    result = await agent.run("What did I tell you about my project?", deps=deps)
    print(result.output)
    # Persist the assistant's reply (the user turn was already persisted).
    await persist_run(deps, result.new_messages())

asyncio.run(main())
```

## On-demand graph search

Beyond the automatic context injection, `create_zep_search_tool()` adds a model-callable tool over `graph.search`. The model decides when to look up specific facts, entities, or prior episodes; it supplies only the query, while `scope`, `reranker`, and `limit` are pinned at construction. The tool returns a formatted text summary of the matching results. By default it searches the current user's graph; pass `graph_id=...` to target a shared standalone graph.

## Memory vs tools

The integration combines two retrieval paths on the same agent:

| Path                    | How                                     | When it fires                                           |
| ----------------------- | --------------------------------------- | ------------------------------------------------------- |
| **Automatic injection** | `ProcessHistory(zep_history_processor)` | Before every model request — prepends the context block |
| **On-demand search**    | `create_zep_search_tool()`              | When the model chooses to call it for a specific lookup |

Injection grounds each turn with cross-session context; the search tool lets the model actively dig for specific details.

## Configuration options

### ZepDeps

| Field            | Type        | Required | Default       | Description                                                         |
| ---------------- | ----------- | -------- | ------------- | ------------------------------------------------------------------- |
| `client`         | `AsyncZep`  | Yes      | —             | Initialized Zep async client (caller owns its lifecycle)            |
| `user_id`        | `str`       | Yes      | —             | Zep user ID (one user graph)                                        |
| `thread_id`      | `str`       | Yes      | —             | Zep thread ID for the conversation                                  |
| `first_name`     | `str`       | No       | `None`        | User first name (recommended; anchors the user node)                |
| `last_name`      | `str`       | No       | `None`        | User last name                                                      |
| `email`          | `str`       | No       | `None`        | User email (helps identity resolution)                              |
| `user_name`      | `str`       | No       | `None`        | Display name for persisted user messages (defaults to first + last) |
| `assistant_name` | `str`       | No       | `"Assistant"` | Display name for persisted assistant messages                       |
| `ignore_roles`   | `list[str]` | No       | `None`        | Roles to exclude from graph ingestion                               |

### create\_zep\_search\_tool

| Parameter  | Type  | Default        | Description                                                                                 |
| ---------- | ----- | -------------- | ------------------------------------------------------------------------------------------- |
| `graph_id` | `str` | `None`         | Standalone graph to search; when unset, searches the current user's graph                   |
| `scope`    | `str` | `"edges"`      | What to search: `edges`, `nodes`, `episodes`, `observations`, `thread_summaries`, or `auto` |
| `reranker` | `str` | `"rrf"`        | Result ordering (ignored for `scope="auto"`)                                                |
| `limit`    | `int` | `10`           | Maximum results (clamped to Zep's ceiling of 50)                                            |
| `name`     | `str` | `"zep_search"` | Tool name exposed to the model                                                              |

## Best practices

* **Construct one `ZepDeps` per conversation** and reuse a single `AsyncZep` client across runs
* **Pass real names** so Zep can anchor the user's identity node in the graph
* **Always call `persist_run`** after a run so the assistant's reply reaches the graph
* **Allow time for indexing** — Zep extracts knowledge asynchronously, so facts from a turn are not instantly searchable

## Next steps

* Explore [customizing graph structure](/customizing-graph-structure) for advanced knowledge organization
* Learn about [searching the graph](/searching-the-graph) and how to tune search
* See [code examples](https://github.com/getzep/zep/tree/main/integrations/pydantic-ai/python/examples) for additional patterns
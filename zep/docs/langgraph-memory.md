> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# LangGraph integration

[LangGraph](https://github.com/langchain-ai/langgraph) agents using Zep gain durable, cross-session memory backed by a temporal knowledge graph. The `zep-langgraph` package wires Zep into your graph nodes: it injects the user's context block into the system prompt, persists each turn, and exposes a graph-search tool the model can call on demand.

A complete notebook example is available in the [Zep repository](https://github.com/getzep/zep/blob/main/examples/python/langgraph-agent/agent.ipynb).

## Core benefits

* **Context injection**: Fold the user's context block into the system prompt on every turn
* **Per-turn persistence**: Write each conversation turn back to Zep with a single helper
* **On-demand graph search**: Expose a LangChain tool the model calls to search the knowledge graph
* **`BaseStore` support**: Use `ZepStore` for `create_react_agent(store=...)` and langmem's memory tools
* **Async and sync clients**: Every helper has both an async and a synchronous variant
* **Graceful degradation**: A Zep failure is logged but never crashes the host agent

## How it works

The package ships two layers. The **node and tool helpers** (the primary path) call Zep directly inside your graph nodes; this matches Zep's recommended LangGraph pattern. `ZepStore` (secondary) is a `BaseStore` implementation for callers who need one — e.g. `create_react_agent(store=...)` or langmem's memory tools.

The Zep loop is the same everywhere — create user, create thread, add messages, retrieve context — and each step is wrapped as a helper you call from a graph node:

* **`build_system_message`** — fetches the context block (`thread.get_user_context`) assembled from the entire user graph and folds it into a `SystemMessage` with your base instructions, ready to prepend to the model's message list. `get_zep_context` returns just the raw block.
* **`persist_messages`** — wraps `thread.add_messages`. Accepts LangChain `BaseMessage` objects (converted automatically) or native Zep `Message` objects, flattens multimodal content to text, and maps names so Zep can resolve identity. Pass `return_context=True` to fold persist and retrieve into one round-trip.
* **`create_graph_search_tool`** — returns a LangChain `StructuredTool` over `graph.search`. Pass it to `create_react_agent(tools=[...])` and the model decides when to search. Exactly one of `user_id` (the user's personal graph) or `graph_id` (a shared standalone graph) is required. The target and search parameters are fixed at construction, so the model only supplies the query.

Identity is yours to manage — create the Zep user and thread out-of-band before the first turn.

## Installation

```bash
pip install zep-langgraph langchain-openai
```

Requires Python 3.11+, `langgraph>=1.2.5`, and a Zep Cloud API key. Get your API key from [app.getzep.com](https://app.getzep.com).

Set up your environment variables:

```bash
export ZEP_API_KEY="your-zep-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

## Usage

Inject context with a `prompt` callable, expose the graph-search tool, and persist each turn. See the [runnable examples](https://github.com/getzep/zep/tree/main/integrations/langgraph/python/examples) for additional patterns.

```python Python
import asyncio
import os
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from zep_cloud import Message
from zep_cloud.client import AsyncZep
from zep_langgraph import build_system_message, create_graph_search_tool, persist_messages

zep = AsyncZep(api_key=os.environ["ZEP_API_KEY"])


async def main():
    # Create the Zep user and thread out-of-band before the first turn.
    await zep.user.add(user_id="user-1", first_name="Alice", last_name="Smith")
    await zep.thread.create(thread_id="thread-1", user_id="user-1")

    # Inject the Zep context block into the system prompt on every turn.
    async def prompt(state):
        system = await build_system_message(
            zep, thread_id="thread-1", base_instructions="You are a helpful assistant."
        )
        return [system, *state["messages"]]

    agent = create_react_agent(
        model=ChatOpenAI(model="gpt-4o-mini"),
        tools=[create_graph_search_tool(zep, user_id="user-1")],
        prompt=prompt,
    )

    result = await agent.ainvoke({"messages": [HumanMessage(content="Where do I work?")]})
    reply = result["messages"][-1]

    # Persist the turn back to Zep.
    await persist_messages(
        zep,
        thread_id="thread-1",
        messages=[Message(role="user", content="Where do I work?", name="Alice Smith"), reply],
    )


asyncio.run(main())
```

## Long-term memory with ZepStore

`BaseStore` is LangGraph's cross-thread long-term-memory interface; `create_react_agent(store=...)` and langmem's memory tools require one. Zep is a temporal knowledge graph, not a key-value store, so it can't faithfully serve exact-key reads or read-after-write on its own. `ZepStore` bridges this with a hybrid-delegate design: a backing key-value store (default `InMemoryStore`) serves exact-key `get` / `put` / `delete` synchronously, while every `put` is also ingested into Zep and `search` is routed to Zep's semantic `graph.search`.

```python Python
from zep_langgraph import ZepStore

store = ZepStore(zep)  # default backing store: InMemoryStore
await store.aput(("memories", "user-1"), "m1", {"text": "Alice works at Acme."})
item = await store.aget(("memories", "user-1"), "m1")  # exact-key, synchronous
hits = await store.asearch(("memories", "user-1"), query="where does Alice work?")
```

Zep ingestion is asynchronous. A value written with `put` is available immediately for exact-key `get` (served by the backing store), but its extracted facts are not instantly returned by `search`. `ZepStore` is the long-term memory layer, not the checkpointer, so graph execution and short-term state are unaffected.

## Public API

| Symbol                                                       | Kind            | Purpose                                        |
| ------------------------------------------------------------ | --------------- | ---------------------------------------------- |
| `get_zep_context` / `get_zep_context_sync`                   | async / sync fn | Fetch the context block for a thread           |
| `build_system_message` / `build_system_message_sync`         | async / sync fn | Build a `SystemMessage` with the context block |
| `format_context_block`                                       | fn              | Combine base instructions with a context block |
| `persist_messages` / `persist_messages_sync`                 | async / sync fn | Persist a turn (LangChain or Zep messages)     |
| `to_zep_message` / `to_zep_messages`                         | fn              | Convert LangChain messages to Zep messages     |
| `create_graph_search_tool` / `create_graph_search_tool_sync` | fn              | Build a `graph.search` `StructuredTool`        |
| `ZepStore`                                                   | class           | Hybrid-delegate `BaseStore`                    |

Both an `AsyncZep` (async helpers, recommended) and a synchronous `Zep` client are supported. Reuse a single client instance.

## Best practices

* **Create the user and thread out-of-band** before the first turn — identity is yours to manage
* **Pass real names** to `persist_messages` so Zep can resolve the user's identity node
* **Use the async helpers** with `AsyncZep` for non-blocking nodes; the `_sync` variants exist for synchronous graphs
* **Allow time for indexing** — Zep extracts knowledge asynchronously, so facts from a turn are not instantly searchable

## Next steps

* Explore [customizing graph structure](/customizing-graph-structure) for advanced knowledge organization
* Learn about [searching the graph](/searching-the-graph) and how to tune search
* See [code examples](https://github.com/getzep/zep/tree/main/integrations/langgraph/python/examples) for the `create_react_agent` and `ZepStore` patterns
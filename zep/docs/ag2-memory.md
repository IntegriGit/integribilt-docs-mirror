> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# AG2 integration

[AG2](https://ag2.ai) agents using Zep maintain context across conversations and access a temporal knowledge graph built from prior turns. The `zep-ag2` package injects relevant context into an agent's system message and exposes Zep search and data tools that AG2 calls during a conversation.

## Core benefits

* **Persistent memory**: Conversations and extracted knowledge persist across sessions
* **System message injection**: Relevant context is added to an agent's system message before it responds
* **Knowledge graph access**: Search and write to Zep's temporal knowledge graph from AG2 agents
* **Tool-based access**: Register Zep search and add operations as AG2 tools the agent invokes on demand

## How it works

The integration provides two ways to give an AG2 agent memory:

* **System message injection** — `ZepMemoryManager` (conversation memory) and `ZepGraphMemoryManager` (knowledge graph) fetch a relevant context block from Zep and enrich an agent's system message before the model runs.
* **Tools** — factory functions return AG2-compatible tools the model can call mid-conversation to search memory or write new data. Tools execute synchronously (AG2's execution model) while bridging to the async Zep SDK internally, so you pass an `AsyncZep` client.

Both approaches can be combined: inject context automatically and let the agent search or store explicitly when needed.

## Installation

```bash
pip install zep-ag2
```

Requires Python 3.11+, `ag2>=0.9.0`, and a Zep Cloud API key. Get your API key from [app.getzep.com](https://app.getzep.com).

Set up your environment variables:

```bash
export ZEP_API_KEY="your-zep-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

## System message injection

Use `ZepMemoryManager` to enrich an agent's system message with relevant conversation context before it responds:

```python Python
import asyncio
import os
from autogen import AssistantAgent, UserProxyAgent, LLMConfig
from zep_cloud.client import AsyncZep
from zep_ag2 import ZepMemoryManager, register_all_tools

async def main():
    zep = AsyncZep(api_key=os.environ["ZEP_API_KEY"])
    user_id = "user123"
    session_id = "session456"

    # Create the Zep user and thread before the first turn
    await zep.user.add(user_id=user_id, first_name="Jane")
    await zep.thread.create(thread_id=session_id, user_id=user_id)

    llm_config = LLMConfig(
        {"model": "gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]}
    )

    assistant = AssistantAgent(
        name="assistant",
        llm_config=llm_config,
        system_message="You are a helpful assistant with long-term memory.",
    )
    user_proxy = UserProxyAgent(
        name="user",
        human_input_mode="NEVER",
        code_execution_config=False,
        is_termination_msg=lambda msg: "TERMINATE" in (msg.get("content") or ""),
    )

    # Enrich the agent's system message with relevant memory
    memory_mgr = ZepMemoryManager(zep, user_id=user_id, session_id=session_id)
    await memory_mgr.enrich_system_message(assistant, query="conversation topic")

    # Register Zep memory tools — AG2 calls them automatically
    register_all_tools(assistant, user_proxy, zep, user_id=user_id, session_id=session_id)

    user_proxy.initiate_chat(assistant, message="What do you remember about me?")

asyncio.run(main())
```

`ZepMemoryManager` also exposes `get_memory_context()` to retrieve the formatted context string directly, `add_messages()` to persist conversation turns, and `get_session_facts()` to read the thread's context block.

## Tool integration

Register Zep operations as AG2 tools so the agent can search memory or write new data during a conversation. `register_all_tools` wires up the full set in one call, or use the individual factories for finer control:

```python Python
from zep_ag2 import create_search_graph_tool, create_add_graph_data_tool

# Create tools bound to a user's knowledge graph
search_tool = create_search_graph_tool(zep, user_id="user123")
add_tool = create_add_graph_data_tool(zep, user_id="user123")

# Register with AG2's decorator pattern
assistant.register_for_llm(description="Search knowledge graph")(search_tool)
user_proxy.register_for_execution()(search_tool)

assistant.register_for_llm(description="Add to knowledge graph")(add_tool)
user_proxy.register_for_execution()(add_tool)
```

**Available tool factories:**

* `create_search_memory_tool(client, user_id, session_id=None)` — searches the user's graph
* `create_add_memory_tool(client, user_id, session_id=None)` — routes to the thread when a `session_id` is set, otherwise writes to the user's graph
* `create_search_graph_tool(client, user_id=None, graph_id=None)` — search the knowledge graph
* `create_add_graph_data_tool(client, user_id=None, graph_id=None)` — add data to the knowledge graph
* `register_all_tools(agent, executor, client, user_id, ...)` — register all tools at once

Graph tools are bound to either a `user_id` (the user's personal graph) or a `graph_id` (a shared standalone graph), not both.

## Knowledge graph memory

Use `ZepGraphMemoryManager` to work with a shared knowledge graph that multiple agents can read and write:

```python Python
from zep_ag2 import ZepGraphMemoryManager

graph_mgr = ZepGraphMemoryManager(zep, graph_id="company_knowledge")

# Add data to the graph
await graph_mgr.add_data("Project Alpha uses Python and React.", data_type="text")

# Search the graph
results = await graph_mgr.search("What technologies does Project Alpha use?", limit=5, scope="edges")

# Inject graph context into an agent's system message
await graph_mgr.enrich_system_message(assistant, query="Project Alpha")
```

## Query memory

You can read memory directly, outside of agent tool calls:

```python Python
# Formatted context block for the user/thread (optionally biased by a query)
context = await memory_mgr.get_memory_context(query="project status", limit=5)

# Facts extracted from the current session
facts = await memory_mgr.get_session_facts()

# Structured search over a knowledge graph
results = await graph_mgr.search("Project Alpha", limit=5, scope="edges")
```

### Search result structure

The tool factories return human-readable strings formatted for the model. `ZepGraphMemoryManager.search()` returns a list of structured result dicts for programmatic use; the fields depend on the scope:

| Scope                 | Fields                                                                               |
| --------------------- | ------------------------------------------------------------------------------------ |
| `edges` (facts)       | `content` (the fact), `type` (`"edge"`), `name`, `attributes`, `created_at`          |
| `nodes` (entities)    | `content` (`"name: summary"`), `type` (`"node"`), `name`, `attributes`, `created_at` |
| `episodes` (messages) | `content`, `type` (`"episode"`), `source`, `role`, `created_at`                      |

## Memory vs tools

The integration supports two complementary patterns that work together on the same agent:

| Pattern                      | How                                                 | When to use                                                                  |
| ---------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------- |
| **System message injection** | `enrich_system_message(...)` on either manager      | Ground every turn with relevant context automatically, before the model runs |
| **Tools**                    | `create_*_tool` factories registered with the agent | Let the agent decide when to search or store during the conversation         |

Use injection for consistent baseline context and tools for explicit, on-demand lookups and writes.

## Configuration options

### ZepMemoryManager

* `ZepMemoryManager(client, user_id, session_id=None)` — initialize with a Zep client and user identity
* `enrich_system_message(agent, query=None, limit=5)` — inject memory context into an agent
* `get_memory_context(query=None, limit=5)` — return the formatted context string
* `add_messages(messages)` — store messages in the Zep thread
* `get_session_facts()` — read the thread's context block

### ZepGraphMemoryManager

* `ZepGraphMemoryManager(client, graph_id)` — initialize with a graph ID
* `search(query, limit=5, scope="edges")` — search the graph (`scope`: `edges`, `nodes`, `episodes`)
* `add_data(data, data_type="text")` — add data to the graph (`data_type`: `text`, `json`, `message`)
* `enrich_system_message(agent, query=None, limit=5)` — inject graph context into an agent

## Best practices

* **Pass an `AsyncZep` client** — tools bridge to it on a shared background event loop, so reuse a single instance
* **Bind tools to one target** — a `user_id` for personal memory or a `graph_id` for shared knowledge, never both
* **Combine injection and tools** — inject context for consistent grounding, add tools for explicit lookups and writes
* **Allow time for indexing** — Zep extracts knowledge asynchronously, so data added during a turn is not instantly searchable

## Next steps

* Explore [customizing graph structure](/customizing-graph-structure) for advanced knowledge organization
* Learn about [searching the graph](/searching-the-graph) and how to tune search
* See [code examples](https://github.com/getzep/zep/tree/main/integrations/ag2/python/examples) for additional patterns
> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Microsoft Agent Framework integration

[Microsoft Agent Framework](https://github.com/microsoft/agent-framework) agents using Zep gain long-term memory backed by a temporal knowledge graph. The `zep-ms-agent-framework` package attaches a context provider that persists each conversation turn and injects relevant context into the model on every run.

## Core benefits

* **Native context-provider hook**: Uses the framework's own `before_run` / `after_run` pipeline — the same surface as its built-in memory providers
* **Single round-trip**: Persists the user turn and retrieves the context block in one call
* **Whole-user-graph recall**: Context is fused across all of a user's threads, so a new conversation still recalls earlier facts
* **Lazy resource creation**: The Zep user and thread are created on first run and cached
* **Graceful degradation**: A Zep failure is logged but never crashes the host agent — the turn proceeds without memory

## How it works

The integration ships one class, `ZepContextProvider`, which subclasses the framework's `ContextProvider` and overrides the two lifecycle hooks called around every `agent.run(...)`:

* **`before_run`** — extracts the latest user message, lazily creates the Zep user and thread, persists the message via `thread.add_messages(return_context=True)`, and injects the returned context block (facts, relationships, and prior knowledge from the whole user graph) into the model's instructions.
* **`after_run`** — reads the assistant's reply and persists it to the same thread, so both sides of the conversation are captured.

Because context is assembled from the entire user graph, the thread only scopes relevance — an agent on a new thread still recalls facts the same user shared earlier.

This integration is **injection-only**. It persists turns and injects the context block automatically through the framework's lifecycle hooks; it exposes no model-callable tools, no separate memory types, and no direct query API. To let the model search the graph on demand, use Zep's SDK (`graph.search`) directly, or one of the tool-based integrations.

## Installation

```bash
pip install zep-ms-agent-framework
```

The package depends only on `agent-framework-core`. The example below also uses a model provider:

```bash
pip install zep-ms-agent-framework agent-framework-openai
```

Requires Python 3.11+, `agent-framework-core>=1.8.1`, and a Zep Cloud API key. Get your API key from [app.getzep.com](https://app.getzep.com).

Set up your environment variables:

```bash
export ZEP_API_KEY="your-zep-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

## Usage

Attach a `ZepContextProvider` to an agent through the `context_providers` keyword argument:

```python Python
import asyncio
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from zep_cloud.client import AsyncZep
from zep_ms_agent_framework import ZepContextProvider

zep = AsyncZep(api_key="your-zep-api-key")

agent = Agent(
    OpenAIChatClient(model="gpt-4o-mini"),
    instructions="You are a helpful assistant with long-term memory.",
    context_providers=[
        ZepContextProvider(
            zep_client=zep,
            user_id="user-123",
            thread_id="thread-abc",
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",  # optional
        )
    ],
)

async def main() -> None:
    result = await agent.run("Hi, I'm a data scientist in Portland.")
    print(result.text)

asyncio.run(main())
```

Memory is scoped per `ZepContextProvider` instance to one `user_id` and `thread_id`. For a multi-user application, construct one provider per user or conversation, passing real names so Zep can resolve the user's identity node in the graph.

## Configuration options

`ZepContextProvider` accepts:

| Field                    | Required    | Default       | Description                                                            |
| ------------------------ | ----------- | ------------- | ---------------------------------------------------------------------- |
| `zep_client`             | Yes         | —             | Initialized `AsyncZep` client (caller owns its lifecycle)              |
| `user_id`                | Yes         | —             | Zep user ID this provider's memory is scoped to                        |
| `thread_id`              | Yes         | —             | Zep thread ID the conversation is recorded in                          |
| `first_name`             | Recommended | `None`        | User first name — helps Zep anchor identity                            |
| `last_name`              | Optional    | `None`        | User last name                                                         |
| `email`                  | Optional    | `None`        | User email                                                             |
| `user_message_name`      | Optional    | full name     | Display name on persisted user messages                                |
| `assistant_message_name` | Optional    | `"Assistant"` | Display name on persisted assistant messages                           |
| `source_id`              | Optional    | `"zep"`       | Attribution ID for injected instructions                               |
| `ignore_roles`           | Optional    | `None`        | Roles to exclude from graph ingestion (still stored in thread history) |
| `on_user_created`        | Optional    | `None`        | Async hook run once after a new user is created                        |

### Per-user setup

Use `on_user_created` to configure per-user resources — a custom ontology, custom extraction instructions, or user summary instructions — the first time a user is created. See [customizing graph structure](/customizing-graph-structure) for the available options.

## Best practices

* **Pass real names** so Zep can anchor and resolve the user's identity node in the graph
* **One provider per user/conversation** — memory is scoped to a single `user_id` and `thread_id`
* **Reuse a single `AsyncZep` client** across requests; the caller owns its lifecycle
* **Allow time for indexing** — Zep extracts knowledge asynchronously, so facts from a turn are not instantly retrievable

## Next steps

* Explore [customizing graph structure](/customizing-graph-structure) for advanced knowledge organization
* Learn about [searching the graph](/searching-the-graph) and how to tune search
* See [code examples](https://github.com/getzep/zep/tree/main/integrations/ms-agent-framework/python/examples) for additional patterns
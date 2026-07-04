> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# LiveKit integration

The `zep-livekit` package adds long-term agent memory to [LiveKit](https://docs.livekit.io/agents/) voice agents. It wraps LiveKit's `Agent` so that completed conversation turns are persisted to Zep and relevant context is injected before each response. Choose between [user thread memory](/users) or structured [knowledge graph memory](/graph-overview).

## Core benefits

* **Persistent voice memory**: Each completed turn is stored in Zep and contributes to the user's temporal knowledge graph
* **Automatic context injection**: Relevant context is retrieved and added as a system message before the agent's next response
* **Two access patterns**: `ZepUserAgent` for thread-based conversation memory, `ZepGraphAgent` for direct knowledge graph access
* **Drop-in replacement**: Both classes subclass LiveKit's `Agent` and accept all standard `Agent` parameters

## How it works

LiveKit's `AgentSession` owns the audio pipeline — speech-to-text, voice activity detection, turn detection, and text-to-speech. Zep does not touch audio. Instead, the Zep agent hooks into LiveKit's turn lifecycle and runs a write-then-read cycle on each completed user turn:

1. **Persist the turn** — when LiveKit fires `on_user_turn_completed`, the user message is written to Zep (a thread for `ZepUserAgent`, the graph for `ZepGraphAgent`). Assistant responses are captured separately via the `conversation_item_added` session event.
2. **Retrieve context** — the agent fetches a context block (`thread.get_user_context` for `ZepUserAgent`) or runs hybrid graph search across edges, nodes, and episodes (`ZepGraphAgent`).
3. **Inject context** — the retrieved context is added to the turn as a system message, so the LLM's next response is grounded in prior conversation.

**Allow time for indexing**: Turns are ingested and knowledge is extracted asynchronously, so facts from the current turn are not searchable within that same turn. Context retrieved on a given turn reflects knowledge extracted from earlier turns.

## Installation

```bash pip
pip install zep-livekit zep-cloud "livekit-agents[openai,silero]>=1.0.0"
```

```bash uv
uv add zep-livekit zep-cloud "livekit-agents[openai,silero]>=1.0.0"
```

```bash poetry
poetry add zep-livekit zep-cloud "livekit-agents[openai,silero]>=1.0.0"
```

Requires LiveKit Agents v1.0+ (not v0.x) and a Zep Cloud API key. The examples use the v1.0 `AgentSession` API. Get your API key from [app.getzep.com](https://app.getzep.com).

Set up your environment variables:

```bash
export ZEP_API_KEY="your-zep-api-key"
export OPENAI_API_KEY="your-openai-api-key"
export LIVEKIT_URL="your-livekit-url"
export LIVEKIT_API_KEY="your-livekit-api-key"
export LIVEKIT_API_SECRET="your-livekit-api-secret"
```

`LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` come from a [LiveKit Cloud](https://cloud.livekit.io) project or a self-hosted LiveKit server. They configure the LiveKit infrastructure your agent connects to and are unrelated to Zep.

## Agent types

* **`ZepUserAgent`**: Uses [user threads](/users) for conversation memory with automatic context injection
* **`ZepGraphAgent`**: Reads and writes a [knowledge graph](/graph-overview), optionally shaped by [custom entity models](/customizing-graph-structure)

## Identity and isolation

The example below derives a stable `user_id` from your application's auth system and scopes the `thread_id` (and `graph_id`) to the LiveKit room. Use a **stable, durable user ID** — do not derive `user_id` from the room name. A room is a per-session construct, so a room-derived `user_id` fragments a returning user's history across rooms and prevents Zep from accumulating long-term memory for that person.

Scope `thread_id` or `graph_id` to the room when you want per-session isolation while still attributing every session to the same long-lived user.

```python
# Stable identity from your auth system — survives across sessions
user_id = authenticated_user_id

# Room/session scopes the thread (or graph), not the user
thread_id = f"thread_{ctx.room.name}"
graph_id = f"graph_{ctx.room.name}"
```

## User memory agent

`ZepUserAgent` stores each turn in a Zep thread and injects a context block before the next response.

```python Python
import logging
import os

from livekit import agents
from livekit.agents import AutoSubscribe
from livekit.plugins import openai, silero
from zep_cloud.client import AsyncZep
from zep_livekit import ZepUserAgent


async def entrypoint(ctx: agents.JobContext):
    zep_client = AsyncZep(api_key=os.environ.get("ZEP_API_KEY"))

    # Stable user identity from your auth system; thread scoped to the room
    user_id = ctx.job.metadata or "user-123"
    thread_id = f"thread_{ctx.room.name}"

    # Ensure the user exists, then create the room-scoped thread
    try:
        await zep_client.user.get(user_id=user_id)
    except Exception:
        await zep_client.user.add(user_id=user_id, first_name="Alice")

    await zep_client.thread.create(thread_id=thread_id, user_id=user_id)

    # Subscribe to audio only — a voice agent has no use for video tracks
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # AgentSession owns the audio pipeline (STT, VAD, turn detection, TTS)
    session = agents.AgentSession(
        stt=openai.STT(),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(),
        vad=silero.VAD.load(),
    )

    # Drop-in Agent replacement that adds Zep memory
    agent = ZepUserAgent(
        zep_client=zep_client,
        user_id=user_id,
        thread_id=thread_id,
        user_message_name="Alice",
        assistant_message_name="Assistant",
        instructions="You are a helpful voice assistant with long-term memory. "
        "Reference details from previous conversations naturally.",
    )

    await session.start(agent=agent, room=ctx.room)
    logging.info("Voice assistant with Zep memory is running")


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
```

**Automatic memory integration**: `ZepUserAgent` captures each voice turn and injects relevant context from previous conversations, enabling continuity across sessions without manual memory management.

### ZepUserAgent configuration

`ZepUserAgent` accepts the following parameters in addition to all standard LiveKit `Agent` parameters (`stt`, `llm`, `tts`, `instructions`, `tools`, `chat_ctx`, etc.):

| Parameter                | Description                                            |
| ------------------------ | ------------------------------------------------------ |
| `zep_client`             | Initialized `AsyncZep` client                          |
| `user_id`                | User identifier for memory isolation (use a stable ID) |
| `thread_id`              | Thread identifier for conversation continuity          |
| `user_message_name`      | Optional name attributed to user messages in Zep       |
| `assistant_message_name` | Optional name attributed to assistant messages in Zep  |

The `context_mode` parameter is deprecated and ignored; the Zep V3 context block returns a structured format and no longer accepts a mode selector.

## Knowledge graph agent

`ZepGraphAgent` writes each turn directly to a knowledge graph and retrieves context with hybrid search over edges (facts), nodes (entities), and episodes. You can optionally shape the graph with custom entity models.

```python Python
import os

from livekit import agents
from livekit.agents import AutoSubscribe
from livekit.plugins import openai, silero
from pydantic import Field
from zep_cloud.client import AsyncZep
from zep_cloud.external_clients.ontology import EntityModel, EntityText
from zep_livekit import ZepGraphAgent


class Person(EntityModel):
    """A person entity for voice interactions."""

    role: EntityText = Field(description="person's role or profession", default=None)
    interests: EntityText = Field(description="topics the person is interested in", default=None)


class Topic(EntityModel):
    """A conversation topic or subject."""

    category: EntityText = Field(description="category of the topic", default=None)
    importance: EntityText = Field(description="importance to the user", default=None)


async def entrypoint(ctx: agents.JobContext):
    zep_client = AsyncZep(api_key=os.environ.get("ZEP_API_KEY"))

    # Optional: define a custom ontology for structured extraction
    await zep_client.graph.set_ontology(entities={"Person": Person, "Topic": Topic})

    # Room-scoped graph
    graph_id = f"graph_{ctx.room.name}"
    try:
        await zep_client.graph.get(graph_id)
    except Exception:
        await zep_client.graph.create(graph_id=graph_id, name="LiveKit Voice Knowledge Graph")

    # Subscribe to audio only — a voice agent has no use for video tracks
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    session = agents.AgentSession(
        stt=openai.STT(),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(),
        vad=silero.VAD.load(),
    )

    agent = ZepGraphAgent(
        zep_client=zep_client,
        graph_id=graph_id,
        facts_limit=15,  # Max facts (edges) to retrieve
        entity_limit=8,  # Max entities (nodes) to retrieve
        episode_limit=2,  # Max episodes to retrieve
        search_filters={"node_labels": ["Person"]},  # Constrain to Person entities
        instructions="You are a knowledgeable voice assistant. Use the provided "
        "context about entities and facts to give informed responses.",
    )

    await session.start(agent=agent, room=ctx.room)


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
```

**Search filters**: The `search_filters` parameter constrains which results the agent retrieves. Use `node_labels` to filter by entity types defined in your ontology.

**Graph memory context**: `ZepGraphAgent` writes each turn to the graph and injects relevant facts, entities, and episodes as context, grounding responses in prior conversations.

### ZepGraphAgent configuration

`ZepGraphAgent` accepts the following parameters in addition to all standard LiveKit `Agent` parameters:

| Parameter        | Description                                               |
| ---------------- | --------------------------------------------------------- |
| `zep_client`     | Initialized `AsyncZep` client                             |
| `graph_id`       | Graph identifier for knowledge storage                    |
| `user_name`      | Optional name prefixed to stored messages for attribution |
| `facts_limit`    | Maximum facts (edges) to retrieve (default: `15`)         |
| `entity_limit`   | Maximum entities (nodes) to retrieve (default: `5`)       |
| `episode_limit`  | Maximum episodes to retrieve (default: `2`)               |
| `search_filters` | Optional `SearchFilters` applied to graph search          |
| `reranker`       | Optional reranker for search results (default: `"rrf"`)   |

## Best practices

* **Use a stable user ID** — derive `user_id` from your auth system, not the room name, so a returning user's memory accumulates instead of fragmenting across sessions
* **Scope sessions with the thread or graph** — use the room name for `thread_id` or `graph_id` when you want per-session isolation, keeping `user_id` constant
* **Let LiveKit own audio** — `AgentSession` handles STT, VAD, turn detection, and TTS; Zep only persists turns and injects context
* **Allow time for indexing** — Zep extracts knowledge asynchronously, so facts from a turn are not instantly searchable

## Next steps

* Explore [customizing graph structure](/customizing-graph-structure) for advanced knowledge organization
* Learn about [searching the graph](/searching-the-graph) and how to tune search
* See [code examples](https://github.com/getzep/zep/tree/main/integrations/livekit/python/examples) for additional patterns
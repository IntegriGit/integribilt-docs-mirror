> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Google ADK integration

Google's [Agent Development Kit (ADK)](https://google.github.io/adk-docs/) agents equipped with Zep's context layer can maintain context across conversations and access personalized knowledge graphs. The `zep-adk` package provides real-time message persistence and automatic context injection for ADK agents, and ships for **Python**, **TypeScript**, and **Go**.

## Core benefits

* **Zero restructuring**: Add Zep to an existing ADK agent without changing your agent architecture
* **Shared-agent architecture**: One `Agent` definition serves all users. Per-user identity is resolved at runtime from ADK session state
* **Real-time persistence**: Both user and assistant messages are persisted to Zep on every turn, not batched at session end
* **Automatic context injection**: Zep's context block — facts, relationships, and prior knowledge — is injected into the LLM prompt before each response
* **Lazy resource creation**: Zep users and threads are created automatically on first use

## How it works

The integration hooks into ADK's agent lifecycle to persist the user's message and inject relevant context before each model call, then persist the assistant's reply afterward. Each language exposes the same loop through its idiomatic ADK extension points:

| Language       | Context injection (per turn)                                                                                                                             | Assistant persistence         |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| **Python**     | `ZepContextTool` — a `BaseTool` that overrides `process_llm_request()` (the hook ADK's own `PreloadMemoryTool` uses); never called by the model directly | `create_after_model_callback` |
| **TypeScript** | `createZepBeforeModelCallback` (a `beforeModelCallback`), or `ZepContextTool` as a tool-centric alternative                                              | `createZepAfterModelCallback` |
| **Go**         | `NewBeforeModelCallback` (a `BeforeModelCallback`)                                                                                                       | `NewAfterModelCallback`       |

On each turn the context hook resolves the user's Zep identity, persists the user's message, retrieves the relevant context block, and injects it into the model's system instruction. Tool-loop continuations are skipped, so a turn is recorded in Zep exactly once. The Go integration additionally provides an ADK `memory.Service` (`NewMemoryService`) that tools reach through `ToolContext.SearchMemory`.

**Per-user setup** (`on_user_created`) and the **custom context builder** below are Python-only — the TypeScript and Go packages don't currently expose these hooks. The general callback and tool options (display names, `ignore_roles`, logger, search parameters) do have TypeScript constructor-option and Go `With...` equivalents; see the [TypeScript](https://github.com/getzep/zep/tree/main/integrations/adk/typescript) and [Go](https://github.com/getzep/zep/tree/main/integrations/adk/go) package READMEs for the exact signatures. The backfill strategy is a standalone script using the Zep SDK directly and applies to any language.

### What gets persisted

Only the **user's message** and the **model's final response** are persisted to Zep on each turn. Intermediate model outputs — such as "thinking" text emitted alongside a tool call (e.g. "Let me look that up for you.") — are not persisted. Tool calls and tool results are also excluded. This keeps the Zep thread clean: one user message and one assistant message per turn, reflecting the actual conversation rather than internal agent mechanics.

If the user message contains multiple text parts (e.g. text alongside an image), all text parts are joined. Non-text parts (images, files) are ignored — only text is sent to Zep.

This approach does **not** use ADK's `BaseMemoryService` abstraction. Zep's real-time, per-message memory model doesn't fit ADK's batch-at-session-end pattern. See [Why not BaseMemoryService?](#why-not-basememoryservice) for details.

## Installation

```bash Python
pip install zep-adk
```

```bash TypeScript
npm install @getzep/zep-adk @google/adk @getzep/zep-cloud
```

```bash Go
go get github.com/getzep/zep/integrations/adk/go@latest
```

Requires a Zep Cloud API key — get yours from [app.getzep.com](https://app.getzep.com) — plus the ADK runtime for your language: Python 3.11+ with `google-adk>=1.0.0`, Node.js 20+ with `@google/adk` (built against `1.2.0`), or Go 1.25+ with `google.golang.org/adk` v1.4.0. The Go package is imported as `zepadk "github.com/getzep/zep/integrations/adk/go"`.

Set up your Zep API key and Gemini API key:

```bash Python
export ZEP_API_KEY="your-zep-api-key"
export GEMINI_API_KEY="your-gemini-api-key"
```

```bash TypeScript
export ZEP_API_KEY="your-zep-api-key"
export GEMINI_API_KEY="your-gemini-api-key"
```

```bash Go
export ZEP_API_KEY="your-zep-api-key"
export GEMINI_API_KEY="your-gemini-api-key"
```

## Adding Zep to an agent

Whether you're building a new agent or adding Zep to an existing one, the setup is the same: wire up the context hook and the after-model callback. The Python example below shows the full runner flow; the TypeScript and Go tabs show the equivalent agent wiring.

```python Python
import os
from uuid import uuid4

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from zep_cloud.client import AsyncZep
from zep_adk import ZepContextTool, create_after_model_callback

zep = AsyncZep(api_key=os.environ["ZEP_API_KEY"])

# One shared agent definition — serves all users
agent = Agent(
    name="my_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant with long-term memory.",
    tools=[
        # Your existing tools stay as-is.
        ZepContextTool(
            zep_client=zep,
            ignore_roles=["assistant"],      # optional — excludes assistant messages from graph ingestion
        ),
    ],
    after_model_callback=create_after_model_callback(
        zep_client=zep,
        assistant_name="my_agent",           # name shown in Zep (default: "Assistant")
        ignore_roles=["assistant"],          # optional — matches ZepContextTool setting
    ),
)

session_service = InMemorySessionService()
runner = Runner(agent=agent, app_name="my_app", session_service=session_service)

# Per-user session — identity maps automatically to Zep:
#   user_id    → Zep user ID
#   session_id → Zep thread ID (Zep's knowledge graph spans all threads for a user)
session_id = f"session-{uuid4().hex[:8]}"
await session_service.create_session(
    app_name="my_app",
    user_id="user-123",
    session_id=session_id,
    state={
        "zep_first_name": "Jane",            # recommended — anchors the identity node
        "zep_last_name": "Smith",            # optional (default: "User")
        "zep_email": "jane@example.com",     # optional
    },
)

# Send a message — persistence and context injection happen automatically
content = types.Content(role="user", parts=[types.Part(text="Hi, I work at Acme Corp.")])
async for event in runner.run_async(
    user_id="user-123", session_id=session_id, new_message=content
):
    if event.is_final_response() and event.content:
        print(event.content.parts[0].text)
```

```typescript TypeScript
import { LlmAgent } from "@google/adk";
import { ZepClient } from "@getzep/zep-cloud";
import {
  createZepBeforeModelCallback,
  createZepAfterModelCallback,
} from "@getzep/zep-adk";

const zep = new ZepClient({ apiKey: process.env.ZEP_API_KEY! });

const agent = new LlmAgent({
  name: "memory_agent",
  model: "gemini-2.5-flash",
  instruction: "You are a helpful assistant with long-term memory.",
  // Persist the user turn + inject the context block before each model call.
  beforeModelCallback: createZepBeforeModelCallback(zep, {
    userId: "user-123",
    threadId: "thread-abc",
    firstName: "Jane",
    lastName: "Smith",
  }),
  // Persist the assistant response after each model call.
  afterModelCallback: createZepAfterModelCallback(zep, {
    userId: "user-123",
    threadId: "thread-abc",
  }),
});
```

```go Go
// Imports for the ADK runtime (llmagent, runner, tool, model) are omitted for
// brevity — see examples/main.go for the full wiring.
import zepadk "github.com/getzep/zep/integrations/adk/go"

zep := zepadk.NewClientFromEnv() // nil when ZEP_API_KEY is unset -> safe no-op

// Provision the Zep user + thread out of band (both idempotent).
_ = zepadk.EnsureUser(ctx, zep, "user-123", "Jane", "Smith", "jane@example.com")
_ = zepadk.EnsureThread(ctx, zep, "thread-abc", "user-123")

agent, _ := llmagent.New(llmagent.Config{
    Name:                 "assistant",
    Model:                llm, // a model.LLM, e.g. gemini.NewModel(...)
    BeforeModelCallbacks: []llmagent.BeforeModelCallback{zepadk.NewBeforeModelCallback(zep)},
    AfterModelCallbacks:  []llmagent.AfterModelCallback{zepadk.NewAfterModelCallback(zep)},
})

run, _ := runner.New(runner.Config{
    AppName:        "my_app",
    Agent:          agent,
    SessionService: sessions,
    MemoryService:  zepadk.NewMemoryService(zep),
})
```

That's it. Every user message is persisted to Zep, relevant context is injected into the LLM prompt, and assistant responses are captured — all automatically.

The `ignore_roles` parameter shown above excludes specific message roles from graph ingestion while still storing them in the thread history. This is useful when assistant messages don't add meaningful knowledge to the graph — they're preserved for conversation context but don't create nodes or edges. Both `ZepContextTool` and `create_after_model_callback` accept `ignore_roles`. See [Ignore assistant messages](/adding-messages#ignore-assistant-messages) in the Zep docs for more detail.

### Identity and session state

The integration maps ADK session metadata to Zep automatically: `user_id` becomes the Zep user ID, and `session_id` becomes the Zep thread ID. Zep's knowledge graph is **per-user, not per-thread** — it accumulates knowledge across all of a user's conversations, so when they start a new session they get context from everything Zep has learned about them.

The following session state keys are recognized (all optional):

| Key              | Default          | Description                                                          |
| ---------------- | ---------------- | -------------------------------------------------------------------- |
| `zep_first_name` | `"Anonymous"`    | User's first name. Anchors the identity node in the knowledge graph. |
| `zep_last_name`  | `"User"`         | User's last name.                                                    |
| `zep_email`      | `None`           | User's email address.                                                |
| `zep_user_id`    | ADK `user_id`    | Override if the Zep user ID differs from the ADK user ID.            |
| `zep_thread_id`  | ADK `session_id` | Override if the Zep thread ID differs from the ADK session ID.       |

Identity resolves by precedence: explicit construction options (`userId`/`threadId`) take precedence over the `zep_user_id`/`zep_thread_id` session-state keys, which in turn take precedence over the ADK `user_id`/`session_id`.

## Advanced usage

### Per-user setup

Python only — the TypeScript and Go packages don't currently expose an `on_user_created` hook.

When the integration creates a new Zep user for the first time, you can run a setup hook to configure per-user resources — such as a custom ontology, custom extraction instructions, or user summary instructions. Pass an `on_user_created` callback to `ZepContextTool`:

```python
from pydantic import Field
from zep_cloud import CustomInstruction
from zep_cloud.client import AsyncZep
from zep_cloud.external_clients.ontology import EntityModel, EntityText
from zep_cloud.types import UserInstruction
from zep_adk import ZepContextTool

class Company(EntityModel):
    """A company or organization the user is associated with."""
    industry: EntityText = Field(description="The company's industry", default=None)

async def setup_user(zep_client: AsyncZep, user_id: str) -> None:
    """Runs once when a new Zep user is created."""
    # Set a custom ontology for this user's knowledge graph
    await zep_client.graph.set_ontology(
        entities={"Company": Company},
        user_ids=[user_id],
    )

    # Add custom extraction instructions
    await zep_client.graph.add_custom_instructions(
        user_ids=[user_id],
        instructions=[
            CustomInstruction(
                name="purchase_intent",
                text="Extract product preferences and purchase intent.",
            )
        ],
    )

    # Configure how user summaries are generated
    await zep_client.user.add_user_summary_instructions(
        user_ids=[user_id],
        instructions=[
            UserInstruction(
                name="work_focus",
                text="Focus on the user's role, team, and active projects.",
            )
        ],
    )

ZepContextTool(zep_client=zep, on_user_created=setup_user)
```

The hook fires only when the user is genuinely new — not for users that already exist. If the hook raises an exception, a warning is logged but the agent turn continues normally.

See [custom ontology](/customizing-graph-structure), [custom instructions](/custom-instructions), and [user summary instructions](/user-summary-instructions) for details on each API.

### Custom context builder

Python only — the TypeScript and Go packages don't currently expose a custom context builder.

By default, the integration uses `thread.add_messages(return_context=True)` — a single API call that persists the message and retrieves context. This works well for most use cases.

For advanced scenarios — multi-graph searches, custom context templates, or combining multiple Zep API calls — you can provide a `context_builder`. When set, message persistence and context building run **in parallel** for lower latency.

```python
import asyncio
from zep_cloud.client import AsyncZep
from zep_adk import ZepContextTool, ContextBuilder

async def my_context_builder(
    zep_client: AsyncZep,
    user_id: str,
    thread_id: str,
    user_message: str,
) -> str | None:
    """Custom context: combine user context with a targeted graph search."""
    user_context, search_results = await asyncio.gather(
        zep_client.thread.get_user_context(thread_id),
        zep_client.graph.search(
            user_id=user_id,
            query=user_message,
            scope="edges",
            limit=10,
        ),
    )

    parts = []
    if user_context and user_context.context:
        parts.append(user_context.context)
    if search_results and search_results.edges:
        facts = [e.fact for e in search_results.edges if e.fact]
        if facts:
            parts.append("Additional facts:\n" + "\n".join(f"- {f}" for f in facts))

    return "\n\n".join(parts) if parts else None

# Pass it to ZepContextTool
tool = ZepContextTool(zep_client=zep, context_builder=my_context_builder)
```

The `ContextBuilder` and `UserSetupHook` type signatures (both importable from `zep_adk`):

```python
ContextBuilder = Callable[[AsyncZep, str, str, str], Awaitable[str | None]]
#                          client   user  thread message

UserSetupHook = Callable[[AsyncZep, str], Awaitable[None]]
#                         client   user_id
```

See [advanced context block construction](/advanced-context-block-construction) and [context templates](/context-templates) for more on assembling custom context.

### Graph search tool

`ZepContextTool` injects context automatically on every turn. For cases where the model needs to **actively search** the knowledge graph — e.g. looking up specific facts, entities, or prior messages — you can add `ZepGraphSearchTool`. This is a model-callable tool: the model sees it in its tool list and decides when to invoke it.

```python Python
from zep_adk import ZepContextTool, ZepGraphSearchTool, create_after_model_callback

agent = Agent(
    name="my_agent",
    model="gemini-2.5-flash",
    instruction="...",
    tools=[
        ZepContextTool(zep_client=zep),          # automatic context every turn
        ZepGraphSearchTool(zep_client=zep),      # on-demand search
    ],
    after_model_callback=create_after_model_callback(zep_client=zep),
)
```

```typescript TypeScript
import { LlmAgent } from "@google/adk";
import {
  ZepContextTool,
  ZepGraphSearchTool,
  createZepAfterModelCallback,
} from "@getzep/zep-adk";

const agent = new LlmAgent({
  name: "my_agent",
  model: "gemini-2.5-flash",
  instruction: "...",
  tools: [
    new ZepContextTool({ zep, userId: "user-123", threadId: "thread-abc" }), // automatic context every turn
    new ZepGraphSearchTool({ zep, userId: "user-123", scope: "edges", limit: 5 }), // on-demand search
  ],
  afterModelCallback: createZepAfterModelCallback(zep, {
    userId: "user-123",
    threadId: "thread-abc",
  }),
});
```

```go Go
searchTool, _ := zepadk.NewGraphSearchTool(zep) // on-demand, model-callable search

agent, _ := llmagent.New(llmagent.Config{
    Name:                 "assistant",
    Model:                llm,
    BeforeModelCallbacks: []llmagent.BeforeModelCallback{zepadk.NewBeforeModelCallback(zep)}, // automatic context
    AfterModelCallbacks:  []llmagent.AfterModelCallback{zepadk.NewAfterModelCallback(zep)},
    Tools:                []tool.Tool{searchTool},
})
```

The tool automatically resolves the user identity from session state, so the model only needs to provide a search query. The model can also optionally choose the `scope` (edges, nodes, episodes), `reranker`, `limit`, and other [search parameters](/searching-the-graph#configurable-parameters).

#### Pinning parameters

Any search parameter can be locked at construction time. Pinned parameters are hidden from the model's schema — it can't override them.

```python
# Model can only control query and scope — everything else is locked
ZepGraphSearchTool(
    zep_client=zep,
    reranker="cross_encoder",
    limit=5,
    search_filters={"node_labels": ["Person"]},
    bfs_origin_node_uuids=["node-uuid-1"],   # seed BFS traversal from specific nodes
)
```

#### Shared documentation graph

To search a fixed graph that all users share (e.g. a documentation knowledge base), pass `graph_id`. The tool will search that graph instead of the current user's personal graph. Use distinct `name` and `description` values when combining multiple instances:

```python
agent = Agent(
    name="my_agent",
    model="gemini-2.5-flash",
    instruction="...",
    tools=[
        ZepContextTool(zep_client=zep),
        ZepGraphSearchTool(
            zep_client=zep,
            name="search_user_memory",
            description="Search the user's knowledge graph for information from previous conversations, known facts, or general context about the user.",
        ),
        ZepGraphSearchTool(
            zep_client=zep,
            name="search_docs",
            description="Search the shared documentation knowledge base.",
            graph_id="docs-graph-123",
        ),
    ],
    after_model_callback=create_after_model_callback(zep_client=zep),
)
```

The model sees two distinct tools and chooses which to call based on the user's query.

## Backfill strategy for existing users

If you have existing users with conversation history, you can backfill their data into Zep so they get rich context from day one.

### ID matching

**Use the same user IDs and thread IDs.** The backfill script must create Zep users and threads with the exact same IDs used in ADK:

* **User IDs** must match what you pass as `user_id` to ADK's `create_session()`. This links live sessions to the correct knowledge graph. Mismatched user IDs mean backfilled history is orphaned.
* **Thread IDs** must match the ADK `session_id` for each conversation. If a user continues an existing session after cutover, the integration uses that session ID as the Zep thread ID. If the backfill used a different thread ID, the conversation history is split — the continued thread won't see the backfilled messages in its thread context.

### Example backfill script

This runs outside of ADK as a standalone script using the Zep Python SDK directly:

```python
import asyncio
from zep_cloud.client import AsyncZep
from zep_cloud import Message

zep = AsyncZep(api_key="your-zep-api-key")

async def backfill_user(
    user_id: str,                          # must match ADK create_session() user_id
    first_name: str,
    last_name: str,
    conversations: list[dict],             # list of {session_id, messages} dicts
):
    # 1. Create the user
    try:
        await zep.user.add(user_id=user_id, first_name=first_name, last_name=last_name)
    except Exception as e:
        if "already exists" not in str(e).lower():
            raise

    # 2. Load each conversation — use the original ADK session ID as the Zep thread ID
    for convo in conversations:
        thread_id = convo["session_id"]    # must match ADK session_id
        try:
            await zep.thread.create(thread_id=thread_id, user_id=user_id)
        except Exception as e:
            if "already exists" in str(e).lower():
                continue
            raise

        messages = [
            Message(
                role=msg["role"],
                content=msg["content"],
                name=f"{first_name} {last_name}" if msg["role"] == "user" else "Assistant",
            )
            for msg in convo["messages"]
        ]
        await zep.thread.add_messages(thread_id=thread_id, messages=messages)

    print(f"Backfilled {len(conversations)} conversations for {user_id}")

async def main():
    users = [
        {
            "user_id": "user-123",       # same ID used in ADK sessions
            "first_name": "Jane",
            "last_name": "Smith",
            "conversations": [
                {
                    "session_id": "session-abc",  # original ADK session ID
                    "messages": [
                        {"role": "user", "content": "I need help with my account settings."},
                        {"role": "assistant", "content": "I can help. What would you like to change?"},
                        {"role": "user", "content": "I want to enable two-factor authentication."},
                        {"role": "assistant", "content": "Go to Settings > Security > 2FA to enable it."},
                    ],
                },
            ],
        },
    ]
    for user in users:
        await backfill_user(**user)

asyncio.run(main())
```

After backfilling, allow time for Zep to process the messages and build knowledge graphs. Zep processes messages asynchronously — the graph won't be available instantly. For large backfills, add delays between users to avoid rate limits.

### Transition gap

There is a window between when the backfill runs and when the Zep-integrated agent goes live. Any messages sent to existing threads during this window won't be in Zep. For most use cases this is acceptable — the knowledge graph catches up quickly once the agent is live. But if thread-level continuity is critical, consider a dual-write period: after the backfill completes but before full cutover, have your application write new messages to Zep (via the SDK directly) alongside the existing system. This ensures no messages are missed in the transition.

### Cutover checklist

1. **Run the backfill script** — Zep now has knowledge graphs for existing users
2. **Update your agent** — Add `ZepContextTool` and the after-model callback
3. **Add session state keys** — Include `zep_first_name` and `zep_last_name` in `create_session()` calls
4. **Deploy** — Existing users get rich context from their first message; new users build context over time

## Why not BaseMemoryService?

The Python and TypeScript integrations inject context through the lifecycle hooks above rather than through ADK's `BaseMemoryService`. (The Go integration additionally exposes an ADK `memory.Service` via `NewMemoryService` for tool-driven `search_memory` calls, but context injection still happens through the before-model callback.)

ADK's `BaseMemoryService` abstraction has two methods: `add_session_to_memory()` (called at session end) and `search_memory()` (called when the agent queries memory). For automatic context injection this is a poor fit for Zep:

* **Real-time, not batch**: Zep persists messages immediately on every turn. Batching at session end would delay knowledge graph updates and prevent the agent from using newly extracted facts mid-conversation.
* **Thread-based context, not keyword search**: ADK's `search_memory()` passes a query string. Zep's context retrieval takes a thread ID and returns a pre-assembled context block built from conversation history, extracted facts, and the user's knowledge graph.

## Next steps

* Explore [customizing graph structure](/customizing-graph-structure) for advanced knowledge organization
* Learn about [searching the graph](/searching-the-graph) for direct graph queries and how to tune search
* See the [Zep Python SDK reference](/sdk-reference) for all available API methods
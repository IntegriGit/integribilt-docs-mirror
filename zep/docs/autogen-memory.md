> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# AutoGen integration

The `zep-autogen` package integrates Zep with [Microsoft AutoGen](https://github.com/microsoft/autogen) agents, backing them with long-term memory and a temporal knowledge graph. It provides memory classes that plug into AutoGen's native `Memory` interface for automatic context injection, plus function tools the agent can call to search and add data on demand. Choose between [user-specific conversation memory](/users) or structured [knowledge graph memory](/graph-overview).

## Core benefits

* **Native `Memory` interface**: `ZepUserMemory` and `ZepGraphMemory` implement AutoGen's `Memory` interface, so they drop straight into an agent's `memory` list
* **Automatic context injection**: Relevant memory is retrieved and prepended to the model context before each turn via `update_context()`
* **User and knowledge graphs**: Persist a user's conversation history or maintain a shared knowledge graph with custom entity models
* **On-demand function tools**: Pre-built tools let the agent explicitly search and add graph data when it chooses
* **Graceful degradation**: A Zep failure is logged but does not crash the agent run

## How it works

The integration exposes two complementary retrieval paths:

* **Memory classes** (`ZepUserMemory`, `ZepGraphMemory`) attach to an agent's `memory` list. AutoGen calls `update_context()` before each turn, and the class retrieves memory from Zep and injects it as a system message — transparent, automatic context on every interaction.
* **Function tools** (`create_search_graph_tool`, `create_add_graph_data_tool`) attach to an agent's `tools` list. The model decides when to call them, giving explicit, observable search and add operations that work with AutoGen's tool reflection.

Both approaches can be combined on the same agent: memory for consistent background context, tools for targeted lookups.

## Installation

```bash pip
pip install zep-autogen zep-cloud autogen-core autogen-agentchat
```

```bash uv
uv add zep-autogen zep-cloud autogen-core autogen-agentchat
```

```bash poetry
poetry add zep-autogen zep-cloud autogen-core autogen-agentchat
```

Requires Python 3.11+, `zep-cloud>=3.23.0`, `autogen-agentchat>=0.7.0`, and a Zep Cloud API key. Get your API key from [app.getzep.com](https://app.getzep.com).

Set up your environment variables:

```bash
export ZEP_API_KEY="your-zep-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

## Memory types

* **User memory**: Stores conversation history in [user threads](/users) with automatic context injection
* **Knowledge graph memory**: Maintains structured knowledge with [custom entity models](/customizing-graph-structure)

## User memory

`ZepUserMemory` persists messages to a user's thread and injects the context block into the agent before each turn. Set up the imports, create the user and thread, initialize the memory, attach it to an agent, then store messages as the conversation proceeds.

### Import dependencies

```python
import os
import uuid
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.memory import MemoryContent, MemoryMimeType
from zep_cloud.client import AsyncZep
from zep_autogen import ZepUserMemory
```

### Create the user and thread

A user and thread must exist before memory can store messages against them.

```python
# Initialize Zep client
zep_client = AsyncZep(api_key=os.environ.get("ZEP_API_KEY"))
user_id = f"user_{uuid.uuid4().hex[:16]}"
thread_id = f"thread_{uuid.uuid4().hex[:16]}"

# Create user (required before using memory)
try:
    await zep_client.user.add(
        user_id=user_id,
        email="alice@example.com",
        first_name="Alice"
    )
except Exception as e:
    print(f"User might already exist: {e}")

# Create thread (required for conversation memory)
try:
    await zep_client.thread.create(thread_id=thread_id, user_id=user_id)
except Exception as e:
    print(f"Thread creation failed: {e}")
```

### Initialize the memory

`ZepUserMemory` binds the client, user, and thread into a memory object that AutoGen can attach to an agent.

```python
# Create user memory with configuration
memory = ZepUserMemory(
    client=zep_client,
    user_id=user_id,
    thread_id=thread_id
)
```

### Attach the memory to an agent

Pass the memory in the agent's `memory` list so context is injected before each turn.

```python
# Create agent with Zep memory
agent = AssistantAgent(
    name="MemoryAwareAssistant",
    model_client=OpenAIChatCompletionClient(
        model="gpt-4.1-mini",
        api_key=os.environ.get("OPENAI_API_KEY")
    ),
    memory=[memory],
    system_message="You are a helpful assistant with persistent memory."
)
```

### Store messages and run

Persist each turn to Zep as the conversation proceeds. The agent automatically retrieves context via `update_context()` before responding.

```python
# Helper function to store messages with proper metadata
async def add_message(message: str, role: str, name: str = None):
    """Store a message in Zep memory following AutoGen standards."""
    metadata = {"type": "message", "role": role}
    if name:
        metadata["name"] = name

    await memory.add(MemoryContent(
        content=message,
        mime_type=MemoryMimeType.TEXT,
        metadata=metadata
    ))

# Example conversation with memory persistence
user_message = "My name is Alice and I love hiking in the mountains."
print(f"User: {user_message}")

# Store user message
await add_message(user_message, "user", "Alice")

# Run agent - it will automatically retrieve context via update_context()
response = await agent.run(task=user_message)
agent_response = response.messages[-1].content
print(f"Agent: {agent_response}")

# Store agent response
await add_message(agent_response, "assistant")
```

**Automatic context injection**: `ZepUserMemory` injects relevant memory via the `update_context()` method before each turn. It injects the context block, and when one is available also appends up to 10 recent thread messages.

**Allow time for indexing** — Zep extracts knowledge asynchronously, so facts from a turn are not instantly searchable. Allow time for indexing before querying for newly added content.

## Knowledge graph memory

`ZepGraphMemory` maintains a standalone knowledge graph with custom entity models. Define an ontology, create the graph, initialize the memory with search filters, add data, then attach the memory to an agent.

### Define entity models

Custom entity models shape how Zep extracts structured knowledge from the data you add.

```python
from zep_autogen.graph_memory import ZepGraphMemory
from zep_cloud.external_clients.ontology import EntityModel, EntityText
from pydantic import Field

# Define entity models using Pydantic
class ProgrammingLanguage(EntityModel):
    """A programming language entity."""
    paradigm: EntityText = Field(
        description="programming paradigm (e.g., object-oriented, functional)",
        default=None
    )
    use_case: EntityText = Field(
        description="primary use cases for this language",
        default=None
    )

class Framework(EntityModel):
    """A software framework or library."""
    language: EntityText = Field(
        description="the programming language this framework is built for",
        default=None
    )
    purpose: EntityText = Field(
        description="primary purpose of this framework",
        default=None
    )
```

### Set the ontology and create the graph

Register the entity models as the graph's ontology, then create the graph that will hold the extracted knowledge.

```python
from zep_cloud import SearchFilters

# Set ontology first
await zep_client.graph.set_ontology(
    entities={
        "ProgrammingLanguage": ProgrammingLanguage,
        "Framework": Framework,
    }
)

# Create graph
graph_id = f"graph_{uuid.uuid4().hex[:16]}"
try:
    await zep_client.graph.create(
        graph_id=graph_id,
        name="Programming Knowledge Graph"
    )
    print(f"Created graph: {graph_id}")
except Exception as e:
    print(f"Graph creation failed: {e}")
```

### Initialize the graph memory

Configure search filters and context limits to control what `ZepGraphMemory` injects on each turn.

```python
# Create graph memory with search configuration
graph_memory = ZepGraphMemory(
    client=zep_client,
    graph_id=graph_id,
    search_filters=SearchFilters(
        node_labels=["ProgrammingLanguage", "Framework"]
    ),
    facts_limit=20,  # Max facts in context injection (default: 20)
    entity_limit=5   # Max entities in context injection (default: 5)
)
```

### Add data and wait for indexing

Knowledge extraction is asynchronous, so allow time for indexing before the data is searchable.

```python
# Add structured knowledge
await graph_memory.add(MemoryContent(
    content="Python is excellent for data science and AI development",
    mime_type=MemoryMimeType.TEXT,
    metadata={"type": "data"}  # "data" stores in graph, "message" stores as episode
))

# Wait for graph processing (required)
print("Waiting for graph indexing...")
await asyncio.sleep(30)  # Allow time for knowledge extraction
```

### Attach the memory to an agent

Pass the graph memory in the agent's `memory` list so relevant facts and entities are injected before each turn.

```python
# Create agent with graph memory
agent = AssistantAgent(
    name="GraphMemoryAssistant",
    model_client=OpenAIChatCompletionClient(model="gpt-4.1-mini"),
    memory=[graph_memory],
    system_message="You are a technical assistant with programming knowledge."
)
```

**Graph memory context injection**: `ZepGraphMemory` automatically retrieves the last 2 episodes from the graph and uses their content to query for relevant facts (up to `facts_limit`) and entities (up to `entity_limit`). This context is injected as a system message during agent interactions.

## Tools integration

Zep tools let agents search and add data directly to memory storage with manual control and structured responses.

**Important**: Tools must be bound to either `graph_id` OR `user_id`, not both. This determines whether they operate on knowledge graphs or user graphs.

### Tool function parameters

**Search tool parameters**:

* `query`: str (required) - Search query text
* `limit`: int (optional, default 10) - Maximum results to return
* `scope`: str (optional, default "edges") - Search scope: "edges", "nodes", "episodes"

**Add tool parameters**:

* `data`: str (required) - Content to store
* `data_type`: str (optional, default "text") - Data type: "text", "json", "message"

### User graph tools

```python
from zep_autogen import create_search_graph_tool, create_add_graph_data_tool

# Create tools bound to user graph
search_tool = create_search_graph_tool(zep_client, user_id=user_id)
add_tool = create_add_graph_data_tool(zep_client, user_id=user_id)

# Agent with user graph tools
agent = AssistantAgent(
    name="UserKnowledgeAssistant",
    model_client=OpenAIChatCompletionClient(model="gpt-4.1-mini"),
    tools=[search_tool, add_tool],
    system_message="You can search and add data to the user's knowledge graph.",
    reflect_on_tool_use=True  # Enables tool usage reflection
)
```

### Knowledge graph tools

```python
# Create tools bound to knowledge graph
search_tool = create_search_graph_tool(zep_client, graph_id=graph_id)
add_tool = create_add_graph_data_tool(zep_client, graph_id=graph_id)

# Agent with knowledge graph tools
agent = AssistantAgent(
    name="KnowledgeGraphAssistant",
    model_client=OpenAIChatCompletionClient(model="gpt-4.1-mini"),
    tools=[search_tool, add_tool],
    system_message="You can search and add data to the knowledge graph.",
    reflect_on_tool_use=True
)
```

## Query memory

Both memory types support direct querying with different scope parameters.

### User memory queries

```python
# Query user conversation history
results = await memory.query("What does Alice like?", limit=5)

# Process different result types
for result in results.results:
    content = result.content
    metadata = result.metadata

    if 'edge_name' in metadata:
        # Fact/relationship result
        print(f"Fact: {content}")
        print(f"Relationship: {metadata['edge_name']}")
        print(f"Valid: {metadata.get('valid_at', 'N/A')} - {metadata.get('invalid_at', 'present')}")
    elif 'node_name' in metadata:
        # Entity result
        print(f"Entity: {metadata['node_name']}")
        print(f"Summary: {content}")
    else:
        # Episode/message result
        print(f"Message: {content}")
        print(f"Role: {metadata.get('episode_role', 'unknown')}")

    print(f"Source: {metadata.get('source')}\n")
```

### Graph memory queries

```python
# Query knowledge graph with scope control
facts_results = await graph_memory.query(
    "Python frameworks",
    limit=10,
    scope="edges"  # "edges" (facts), "nodes" (entities), "episodes" (messages)
)

print(f"Found {len(facts_results.results)} facts about Python frameworks:")
for result in facts_results.results:
    print(f"- {result.content}")

entities_results = await graph_memory.query(
    "programming languages",
    limit=5,
    scope="nodes"
)

print(f"\nFound {len(entities_results.results)} programming language entities:")
for result in entities_results.results:
    entity_name = result.metadata.get('node_name', 'Unknown')
    print(f"- {entity_name}: {result.content}")
```

### Search result structure

```json
{
    "content": "fact text",
    "metadata": {
        "source": "graph" | "user_graph",
        "edge_name": "relationship_name",
        "edge_attributes": {...},
        "created_at": "timestamp",
        "valid_at": "timestamp",
        "invalid_at": "timestamp",
        "expired_at": "timestamp"
    }
}
```

```json
{
    "content": "entity_name:\n entity_summary",
    "metadata": {
        "source": "graph" | "user_graph",
        "node_name": "entity_name",
        "node_attributes": {...},
        "created_at": "timestamp"
    }
}
```

```json
{
    "content": "episode_content",
    "metadata": {
        "source": "graph" | "user_graph",
        "episode_type": "source_type",
        "episode_role": "role_type",
        "episode_name": "role_name",
        "created_at": "timestamp"
    }
}
```

## Memory vs tools comparison

**Memory objects** (`ZepUserMemory` / `ZepGraphMemory`):

* Automatic context injection via `update_context()`
* Attached to the agent's `memory` list
* Transparent operation — happens automatically
* Better for consistent memory across interactions

**Function tools** (search/add tools):

* Manual control — the agent decides when to use them
* More explicit and observable operations
* Better for specific search/add operations
* Works with AutoGen's tool reflection features
* Provides structured return values

**Note**: Both approaches can be combined — use memory for automatic context and tools for explicit operations.

## Best practices

* **Pick the right memory type** — use `ZepUserMemory` for per-user conversation history and `ZepGraphMemory` for a shared knowledge graph
* **Bind tools to exactly one scope** — a search or add tool targets either a `graph_id` or a `user_id`, never both
* **Combine memory and tools** — attach a memory class for automatic context and add function tools for targeted lookups
* **Allow time for indexing** — Zep extracts knowledge asynchronously, so facts from a turn are not instantly searchable

## Next steps

* Explore [customizing graph structure](/customizing-graph-structure) for advanced knowledge organization
* Learn about [searching the graph](/searching-the-graph) and how to tune search
* See [code examples](https://github.com/getzep/zep/tree/main/integrations/autogen/python/examples) for additional patterns
> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# CrewAI integration

The `zep-crewai` package gives CrewAI agents persistent memory backed by Zep's temporal knowledge graph. You persist conversation turns and business data with Zep storage adapters, and give your agents Zep tools so they can retrieve relevant context when they need it. This lets agents carry context across executions, share a common knowledge base, and ground their decisions in what was learned before.

## Core benefits

* **Persistent memory** — Conversations and knowledge persist across sessions and crew runs.
* **On-demand retrieval** — Agents search Zep through tools and pull in context exactly when a task calls for it.
* **Dual storage** — User-specific memory for individuals and shared knowledge graphs for organizational data.
* **Tool integration** — Search and add-data tools let agents read from and write to Zep during execution.

## How it works

Memory in this integration is explicit and tool-driven. There are two distinct steps, and you control both.

**Persisting context.** Create a `ZepUserStorage` or `ZepGraphStorage` adapter and call `storage.save(value, metadata={"type": ...})`. The adapter routes each item by its `type`:

| Metadata type | Routes to       | Use for                         |
| ------------- | --------------- | ------------------------------- |
| `message`     | Thread API      | Conversation turns (role-based) |
| `json`        | Knowledge graph | Structured data                 |
| `text`        | Knowledge graph | Facts, preferences, free text   |

**Retrieving context.** Attach `create_search_tool` (and optionally `create_add_data_tool`) to an `Agent(tools=[...])`. The agent searches Zep when it decides the task needs it. You can also call `ZepUserStorage.get_context()` directly to fetch the prompt-ready context block that Zep auto-assembles for a thread.

There is no automatic retrieval or storage, and no `external_memory=` Crew wiring. CrewAI 1.x removed the `ExternalMemory(storage=...)` wrapper and the storage interface it depended on, so context is never injected behind the scenes. You decide what to save with `save(...)`, and the agent decides what to search through its tools.

## Installation

```bash
pip install zep-crewai
```

Requires Python 3.11+, `zep-crewai>=1.1.2`, `crewai>=1.0.0`, and `zep-cloud>=3.23.0`, plus a Zep Cloud API key. Get your API key from [app.getzep.com](https://app.getzep.com).

Set your API key in the environment:

```bash
export ZEP_API_KEY="your-zep-api-key"
```

## Storage types

### User storage

Use `ZepUserStorage` for an individual user's conversation history and personal context. A `thread_id` is required and ties message storage to a conversation thread.

```python Python
import os
from zep_cloud.client import Zep
from zep_crewai import ZepUserStorage, create_search_tool
from crewai import Agent

zep_client = Zep(api_key=os.getenv("ZEP_API_KEY"))

# Create the user and thread up front
zep_client.user.add(user_id="alice_123", first_name="Alice")
zep_client.thread.create(user_id="alice_123", thread_id="project_456")

# Create user storage
user_storage = ZepUserStorage(
    client=zep_client,
    user_id="alice_123",
    thread_id="project_456",
)

# Persist a conversation turn (routes to the thread)
user_storage.save(
    "How can I help you today?",
    metadata={"type": "message", "role": "assistant", "name": "Helper"},
)

# Persist a preference as graph data
user_storage.save(
    "Alice prefers morning meetings",
    metadata={"type": "text"},
)

# Give an agent a Zep search tool so it can retrieve this context on demand
assistant = Agent(
    role="Personal Assistant",
    goal="Help Alice using what you know about her",
    backstory="You know Alice's preferences and conversation history.",
    tools=[create_search_tool(zep_client, user_id="alice_123")],
)
```

To fetch the auto-assembled context block for the thread directly, call `get_context()`:

```python Python
# Returns a prompt-ready context block string (or None if empty)
context = user_storage.get_context()
print(context)
```

### Graph storage

Use `ZepGraphStorage` for shared organizational knowledge that multiple agents can read and write.

```python Python
from zep_cloud import SearchFilters
from zep_crewai import ZepGraphStorage, create_search_tool
from crewai import Agent

# Create the graph
zep_client.graph.create(
    graph_id="company_knowledge",
    name="Company Knowledge Graph",
    description="Shared organizational knowledge and insights.",
)

# Create graph storage for shared knowledge
graph_storage = ZepGraphStorage(
    client=zep_client,
    graph_id="company_knowledge",
    search_filters=SearchFilters(node_labels=["Technology", "Project"]),
)

# Persist knowledge
graph_storage.save(
    "Project Alpha uses Python and React",
    metadata={"type": "text"},
)

# Let agents search it through a tool
knowledge_agent = Agent(
    role="Knowledge Assistant",
    goal="Answer questions from the shared knowledge graph",
    backstory="You maintain and search the team's shared knowledge.",
    tools=[create_search_tool(zep_client, graph_id="company_knowledge")],
)
```

You can also search a graph directly. `search` returns a list whose entries include a composed context string:

```python Python
results = graph_storage.search("project status", limit=5)
for item in results:
    print(item.get("context", ""))
```

## Tool integration

Tools are the supported extension point for exposing Zep to CrewAI agents. Bind a tool to a single user or a single graph at creation time, then add it to an agent's `tools` list.

```python Python
from zep_crewai import create_search_tool, create_add_data_tool
from crewai import Agent

# Tools bound to user storage
user_search_tool = create_search_tool(zep_client, user_id="alice_123")
user_add_tool = create_add_data_tool(zep_client, user_id="alice_123")

# Tools bound to graph storage
graph_search_tool = create_search_tool(zep_client, graph_id="knowledge_base")
graph_add_tool = create_add_data_tool(zep_client, graph_id="knowledge_base")

curator = Agent(
    role="Knowledge Curator",
    goal="Search existing knowledge and record new findings",
    backstory="You maintain the organization's knowledge base.",
    tools=[graph_search_tool, graph_add_tool],
    llm="gpt-4o-mini",
)
```

**Search tool parameters:**

* `query` — Natural language search query.
* `limit` — Maximum results (default: 10).
* `scope` — Search scope: `edges` (default), `nodes`, `episodes`, or `all`.

**Add-data tool parameters:**

* `data` — Content to store (text, JSON, or message).
* `data_type` — Explicit type: `text` (default), `json`, or `message`.

### Structured data with ontologies

Define entity models so Zep organizes graph data into typed entities. The SDK requires a docstring on each entity class to describe it.

```python Python
from pydantic import Field
from zep_cloud import SearchFilters
from zep_cloud.external_clients.ontology import EntityModel, EntityText
from zep_crewai import ZepGraphStorage

class ProjectEntity(EntityModel):
    """A project tracked in the knowledge graph."""

    status: EntityText = Field(description="project status")
    priority: EntityText = Field(description="priority level")
    team_size: EntityText = Field(description="team size")

# Apply the ontology to one or more graphs
zep_client.graph.set_ontology(
    graph_ids=["projects"],
    entities={"Project": ProjectEntity},
    edges={},
)

# Use the graph with filtered search and context limits
graph_storage = ZepGraphStorage(
    client=zep_client,
    graph_id="projects",
    search_filters=SearchFilters(node_labels=["Project"]),
    facts_limit=20,
    entity_limit=5,
)
```

## Configuration options

### ZepUserStorage parameters

* `client` — Zep client instance (required).
* `user_id` — User identifier (required).
* `thread_id` — Thread identifier (required); ties message storage to a conversation thread.
* `search_filters` — Filter search results by node labels or attributes.
* `facts_limit` — Maximum facts (edges) for context (default: 20).
* `entity_limit` — Maximum entities (nodes) for context (default: 5).

### ZepGraphStorage parameters

* `client` — Zep client instance (required).
* `graph_id` — Graph identifier (required).
* `search_filters` — Filter by node labels, for example `SearchFilters(node_labels=["Technology"])`.
* `facts_limit` — Maximum facts (edges) for context (default: 20).
* `entity_limit` — Maximum entities (nodes) for context (default: 5).

## Complete example

This example mirrors the `simple_example.py` from the integration repository. It persists conversation turns and business data to a user's memory, then runs an agent that searches that memory through a Zep tool before answering.

```python Python
import os
import sys
import time
import uuid

from crewai import Agent, Crew, Process, Task
from zep_cloud.client import Zep

from zep_crewai import ZepUserStorage, create_search_tool


def main():
    api_key = os.environ.get("ZEP_API_KEY")
    if not api_key:
        print("Error: set your ZEP_API_KEY environment variable")
        print("Get your API key from: https://app.getzep.com")
        sys.exit(1)

    zep_client = Zep(api_key=api_key)

    # Set up a unique user and thread
    user_id = "demo_user_" + str(uuid.uuid4())
    thread_id = "demo_thread_" + str(uuid.uuid4())

    zep_client.user.add(
        user_id=user_id,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
    )
    zep_client.thread.create(user_id=user_id, thread_id=thread_id)

    # Initialize the Zep storage adapter
    user_storage = ZepUserStorage(client=zep_client, user_id=user_id, thread_id=thread_id)

    # Persist context with metadata-based routing
    # JSON data routes to the graph
    user_storage.save(
        '{"trip_type": "business", "destination": "New York", "duration": "3 days", '
        '"budget": 2000, "accommodation_preference": "mid-range hotels"}',
        metadata={"type": "json"},
    )

    # Messages route to the thread
    user_storage.save(
        "Hi, I need help planning a business trip to New York. I'll be there for 3 "
        "days and prefer mid-range hotels.",
        metadata={"type": "message", "role": "user", "name": "John Doe"},
    )
    user_storage.save(
        "I'd be happy to help you plan your New York business trip!",
        metadata={"type": "message", "role": "assistant", "name": "Travel Planning Assistant"},
    )

    # Text data routes to the graph
    user_storage.save(
        "John Doe prefers mid-range hotels with business amenities, enjoys local "
        "cuisine, and values convenient locations near business districts.",
        metadata={"type": "text"},
    )
    user_storage.save(
        "John Doe's budget constraint: around $2000 total for the trip including "
        "flights and accommodation. Looking for good value rather than luxury.",
        metadata={"type": "text"},
    )

    # Allow time for indexing before the agent searches
    time.sleep(20)

    # Give the agent a Zep search tool bound to this user
    search_tool = create_search_tool(zep_client, user_id=user_id)

    travel_agent = Agent(
        role="Travel Planning Assistant",
        goal="Help plan business trips efficiently and within budget",
        backstory="""You are an experienced travel planner who specializes in business
        trips. You always consider the user's preferences, budget, and trip context.
        Use the Zep memory search tool to recall what you know about the user before
        answering.""",
        tools=[search_tool],
        verbose=True,
        llm="gpt-4.1-mini",
    )

    planning_task = Task(
        description="""First, search Zep memory for the user's saved preferences and
        trip context. Then provide 3 specific hotel recommendations in New York that
        would be good for a business traveler. Include hotel names and locations, price
        range per night, why each fits the user's preferences, and any business
        amenities.""",
        expected_output="A list of 3 hotel recommendations with detailed explanations",
        agent=travel_agent,
    )

    crew = Crew(
        agents=[travel_agent],
        tasks=[planning_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    print(result)

    # Optionally persist the result for future runs
    user_storage.save(str(result), metadata={"type": "message", "role": "assistant"})


if __name__ == "__main__":
    main()
```

## Best practices

### Storage selection

* **Use `ZepUserStorage`** for personal preferences, conversation history, and user-specific context.
* **Use `ZepGraphStorage`** for shared knowledge, organizational data, and collaborative information.

### Memory management

* **Set up ontologies** for structured graph data, and give every entity class a docstring.
* **Use search filters** to target specific node types and improve relevance.
* **Combine storage types** for comprehensive memory coverage.

### Tool usage

* **Bind tools** to a specific user or graph at creation time.
* **Use search scope `all` sparingly** — it queries edges, nodes, and episodes and is more expensive.
* **Save data with the right `type`** (`message`, `json`, or `text`) so it routes correctly.
* **Allow time for indexing** — Zep extracts knowledge asynchronously, so facts from a turn are not instantly searchable.

## Next steps

* Explore [customizing graph structure](/customizing-graph-structure) for advanced knowledge organization
* Learn about [searching the graph](/searching-the-graph) and how to tune search
* See [code examples](https://github.com/getzep/zep/tree/main/integrations/crewai/python/examples) for additional patterns
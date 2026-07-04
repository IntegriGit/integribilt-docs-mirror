> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Create Graph

## Overview

While most use cases benefit from user-centric graphs that automatically integrate with users and threads, Zep also supports creating standalone graphs. Standalone graphs are useful for specific scenarios where you need independent knowledge graphs that aren't tied to individual users.

## When to use standalone graphs

Consider using standalone graphs when you need to:

* Create shared knowledge bases across multiple users
* Build domain-specific knowledge graphs independent of user context
* Maintain separate graphs for testing or experimentation
* Implement custom graph architectures for specialized use cases

For most applications, we recommend using user graphs (created automatically when you add a user) as they integrate directly with Zep's context retrieval systems.

## Creating a Standalone Graph

```python Python
from zep_cloud.client import Zep

client = Zep(
    api_key=API_KEY,
)

# Create a standalone graph with a custom ID
result = client.graph.create(
    graph_id="my_custom_graph"
)

print(f"Created graph with ID: {result.graph_id}")
```

```typescript TypeScript
import { ZepClient } from "@getzep/zep-cloud";

const client = new ZepClient({
  apiKey: API_KEY,
});

// Create a standalone graph with a custom ID
const result = await client.graph.create({
    graphId: "my_custom_graph"
});

console.log(`Created graph with ID: ${result.graphId}`);
```

```go Go
import (
    "context"
    "fmt"
    "log"

    "github.com/getzep/zep-go/v3"
    zepclient "github.com/getzep/zep-go/v3/client"
    "github.com/getzep/zep-go/v3/option"
)

client := zepclient.NewClient(
    option.WithAPIKey(apiKey),
)

// Create a standalone graph with a custom ID
graphID := "my_custom_graph"
result, err := client.Graph.Create(context.TODO(), &zep.CreateGraphRequest{
    GraphID: &graphID,
})
if err != nil {
    log.Fatalf("Failed to create graph: %v", err)
}

fmt.Printf("Created graph with ID: %s\n", *result.GraphID)
```

## Working with standalone graphs

Once created, you can work with standalone graphs using the same methods as user graphs:

* [Add data to the graph](/adding-business-data) by specifying `graph_id` instead of `user_id`
* [Search the graph](/working-with-graphs/searching-the-graph) for relevant information
* [Read data from the graph](/working-with-graphs/reading-data-from-the-graph) to inspect nodes and edges
* [Delete data from the graph](/working-with-graphs/deleting-data-from-the-graph) when needed
* [Clone the graph](/working-with-graphs/cloning-graphs) to create copies

## Customizing Graph Structure

Standalone graphs can be customized with entity and edge types just like user graphs. See [Customizing Graph Structure](/customizing-graph-structure) for details on how to define custom ontologies for your graph.

## Next Steps

* Learn how to [add business data](/adding-business-data) to your graph
* Explore [graph search capabilities](/working-with-graphs/searching-the-graph)
* Understand how to [customize graph structure](/customizing-graph-structure)
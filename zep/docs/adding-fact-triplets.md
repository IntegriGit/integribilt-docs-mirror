> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Adding Fact Triplets

## Overview

You can add manually specified fact/node triplets to the graph. You need only specify the fact, the target node name, and the source node name. Zep will then create a new corresponding edge and nodes, or use an existing edge/nodes if they exist and seem to represent the same nodes or edge you send as input. And if this new fact invalidates an existing fact, it will mark the existing fact as invalid and add the new fact triplet.

The `add_fact_triple` method returns a `task_id` that can be used to track the processing status of the operation. See the [Check Data Ingestion Status](/cookbook/check-data-ingestion-status#checking-operation-status-with-task-polling) recipe for how to poll task status.

## Adding a Fact Triplet

```python Python
from zep_cloud.client import Zep

client = Zep(
    api_key=API_KEY,
)

result = client.graph.add_fact_triple(
    user_id=user_id,  # Optional: You can use graph_id instead of user_id
    fact="Paul met Eric",
    fact_name="MET",
    target_node_name="Eric Clapton",
    source_node_name="Paul",
)

# The result includes a task_id for tracking processing status
task_id = result.task_id
print(f"Fact triple task ID: {task_id}")
```

```typescript TypeScript
import { ZepClient } from "@getzep/zep-cloud";

const client = new ZepClient({
  apiKey: API_KEY,
});

const result = await client.graph.addFactTriple({
  userId: userId,  // Optional: You can use graphId instead of userId
  fact: "Paul met Eric",
  factName: "MET",
  targetNodeName: "Eric Clapton",
  sourceNodeName: "Paul",
});

// The result includes a task_id for tracking processing status
const taskId = result.taskId;
console.log(`Fact triple task ID: ${taskId}`);
```

```go Go
import (
    "context"
    "log"

    "github.com/getzep/zep-go/v3"
    zepclient "github.com/getzep/zep-go/v3/client"
    "github.com/getzep/zep-go/v3/option"
)

client := zepclient.NewClient(
    option.WithAPIKey(apiKey),
)

userID := "user123"
sourceNodeName := "Paul"

result, err := client.Graph.AddFactTriple(context.TODO(), &v3.AddTripleRequest{
    UserID:         &userID,  // Optional: You can use GraphID instead of UserID
    Fact:           "Paul met Eric",
    FactName:       "MET",
    TargetNodeName: "Eric Clapton",
    SourceNodeName: &sourceNodeName,
})
if err != nil {
    log.Fatalf("Failed to add fact triple: %v", err)
}

// The result includes a task_id for tracking processing status
taskID := result.TaskID
log.Printf("Fact triple task ID: %s", *taskID)
```

## Retrieving Created UUIDs

Because fact triple creation is asynchronous, the UUIDs for the edge and nodes are not returned immediately. After the task completes, you can retrieve them by calling `client.task.get()` with the `task_id` returned from `add_fact_triple`. The task's `params` field will contain `edge_uuid`, `source_node_uuid`, and `target_node_uuid`.

```python Python
from zep_cloud.client import Zep
import time

client = Zep(api_key=API_KEY)

# Add a fact triple
result = client.graph.add_fact_triple(
    user_id=user_id,
    fact="Paul met Eric",
    fact_name="MET",
    target_node_name="Eric Clapton",
    source_node_name="Paul",
)

task_id = result.task_id

# Poll until the task completes
while True:
    task = client.task.get(task_id=task_id)

    if task.status == "succeeded":
        break
    elif task.status == "failed":
        raise Exception(f"Task failed: {task.error}")

    time.sleep(10)

# Retrieve the created UUIDs from task.params
edge_uuid = task.params.get("edge_uuid")
source_node_uuid = task.params.get("source_node_uuid")
target_node_uuid = task.params.get("target_node_uuid")

print(f"Edge UUID: {edge_uuid}")
print(f"Source Node UUID: {source_node_uuid}")
print(f"Target Node UUID: {target_node_uuid}")
```

```typescript TypeScript
import { ZepClient } from "@getzep/zep-cloud";

const client = new ZepClient({ apiKey: API_KEY });

// Add a fact triple
const result = await client.graph.addFactTriple({
  userId: userId,
  fact: "Paul met Eric",
  factName: "MET",
  targetNodeName: "Eric Clapton",
  sourceNodeName: "Paul",
});

const taskId = result.taskId;

// Poll until the task completes
const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

let task;
while (true) {
  task = await client.task.get(taskId);

  if (task.status === "succeeded") {
    break;
  } else if (task.status === "failed") {
    throw new Error(`Task failed: ${task.error}`);
  }

  await sleep(10000);
}

// Retrieve the created UUIDs from task.params
const edgeUuid = task.params?.edge_uuid;
const sourceNodeUuid = task.params?.source_node_uuid;
const targetNodeUuid = task.params?.target_node_uuid;

console.log(`Edge UUID: ${edgeUuid}`);
console.log(`Source Node UUID: ${sourceNodeUuid}`);
console.log(`Target Node UUID: ${targetNodeUuid}`);
```

```go Go
import (
    "context"
    "fmt"
    "time"

    "github.com/getzep/zep-go/v3"
    zepclient "github.com/getzep/zep-go/v3/client"
    "github.com/getzep/zep-go/v3/option"
)

client := zepclient.NewClient(
    option.WithAPIKey(apiKey),
)

userID := "user123"
sourceNodeName := "Paul"

// Add a fact triple
result, err := client.Graph.AddFactTriple(context.TODO(), &zep.AddTripleRequest{
    UserID:         &userID,
    Fact:           "Paul met Eric",
    FactName:       "MET",
    TargetNodeName: "Eric Clapton",
    SourceNodeName: &sourceNodeName,
})
if err != nil {
    log.Fatalf("Failed to add fact triple: %v", err)
}

taskID := result.TaskID

// Poll until the task completes
var task *zep.GetTaskResponse
for {
    task, err = client.Task.Get(context.TODO(), *taskID)
    if err != nil {
        log.Fatalf("Failed to get task: %v", err)
    }

    if task.Status == "succeeded" {
        break
    } else if task.Status == "failed" {
        log.Fatalf("Task failed: %v", task.Error)
    }

    time.Sleep(10 * time.Second)
}

// Retrieve the created UUIDs from task.Params
edgeUUID := task.Params["edge_uuid"]
sourceNodeUUID := task.Params["source_node_uuid"]
targetNodeUUID := task.Params["target_node_uuid"]

fmt.Printf("Edge UUID: %v\n", edgeUUID)
fmt.Printf("Source Node UUID: %v\n", sourceNodeUUID)
fmt.Printf("Target Node UUID: %v\n", targetNodeUUID)
```

## Advanced Options

### Custom types and attributes

You can attach custom scalar attributes to nodes and edges, and optionally reference [custom entity and edge types](/custom-graph-schema) from your ontology to enforce a schema.

* `source_node_labels` / `target_node_labels` — specify a single **entity type name** from your ontology.
* `fact_name` — serves as both the relationship display name and the **edge type name** looked up in your ontology.
* `source_node_attributes` / `target_node_attributes` / `edge_attributes` — custom scalar properties on those nodes and edges, usable for [filtering in graph searches](/searching-the-graph#property-filtering).

**Attribute validation** — specifying types is optional. If a label or `fact_name` is not found in your ontology, attributes pass through without validation:

| Situation                                          | Result                                        |
| -------------------------------------------------- | --------------------------------------------- |
| Label not in ontology                              | All `node_attributes` pass through — no error |
| `fact_name` not in ontology                        | All `edge_attributes` pass through — no error |
| Label in ontology, matching type has no properties | All attributes pass through                   |
| Label in ontology and type HAS properties defined  | Attributes validated strictly                 |

When validation activates, every attribute key and value type must match the schema — otherwise the call returns HTTP 400.

```python Python
from zep_cloud.client import Zep

client = Zep(api_key=API_KEY)

# Assumes your ontology defines:
# - Entity type "Person" with properties: { "age": int, "role": text }
# - Edge type "WORKS_AT" with properties: { "start_year": int, "department": text }

result = client.graph.add_fact_triple(
    user_id=user_id,
    fact="Alice works at Acme Corp",
    fact_name="WORKS_AT",                     # matches edge type in ontology
    source_node_name="Alice",
    source_node_labels=["Person"],            # matches entity type "Person" in ontology
    source_node_attributes={
        "age": 30,                            # validated: must be int
        "role": "Engineer",                   # validated: must be text
    },
    target_node_name="Acme Corp",
    target_node_labels=["Organization"],      # not in ontology — passes through freely
    edge_attributes={
        "start_year": 2021,                   # validated against WORKS_AT schema
        "department": "Engineering",
    },
)
```

```typescript TypeScript
import { ZepClient } from "@getzep/zep-cloud";

const client = new ZepClient({ apiKey: API_KEY });

// Assumes your ontology defines:
// - Entity type "Person" with properties: { "age": int, "role": text }
// - Edge type "WORKS_AT" with properties: { "start_year": int, "department": text }

const result = await client.graph.addFactTriple({
  userId: userId,
  fact: "Alice works at Acme Corp",
  factName: "WORKS_AT",                       // matches edge type in ontology
  sourceNodeName: "Alice",
  sourceNodeLabels: ["Person"],               // matches entity type "Person" in ontology
  sourceNodeAttributes: {
    age: 30,                                  // validated: must be int
    role: "Engineer",                         // validated: must be text
  },
  targetNodeName: "Acme Corp",
  targetNodeLabels: ["Organization"],         // not in ontology — passes through freely
  edgeAttributes: {
    startYear: 2021,                          // validated against WORKS_AT schema
    department: "Engineering",
  },
});
```

```go Go
import (
    "context"
    "log"

    "github.com/getzep/zep-go/v3"
    zepclient "github.com/getzep/zep-go/v3/client"
    "github.com/getzep/zep-go/v3/option"
)

client := zepclient.NewClient(
    option.WithAPIKey(apiKey),
)

userID := "user123"
sourceNodeName := "Alice"
targetNodeName := "Acme Corp"

// Assumes your ontology defines:
// - Entity type "Person" with properties: { "age": int, "role": text }
// - Edge type "WORKS_AT" with properties: { "start_year": int, "department": text }

result, err := client.Graph.AddFactTriple(context.TODO(), &zep.AddTripleRequest{
    UserID:           &userID,
    Fact:             "Alice works at Acme Corp",
    FactName:         "WORKS_AT",             // matches edge type in ontology
    SourceNodeName:   &sourceNodeName,
    SourceNodeLabels: []string{"Person"},     // matches entity type "Person" in ontology
    SourceNodeAttributes: map[string]interface{}{
        "age":  30,                           // validated: must be int
        "role": "Engineer",                   // validated: must be text
    },
    TargetNodeName:   &targetNodeName,
    TargetNodeLabels: []string{"Organization"}, // not in ontology — passes through freely
    EdgeAttributes: map[string]interface{}{
        "start_year":  2021,                  // validated against WORKS_AT schema
        "department":  "Engineering",
    },
})
if err != nil {
    log.Fatalf("Failed to add fact triple: %v", err)
}
```

Attribute values must be scalar types: string, number, boolean, or null. Nested objects and arrays are not supported.

### Fact triplet metadata

You can attach metadata to a fact triple, which makes the resulting edge and nodes filterable via [episode metadata filters](/searching-the-graph#episode-metadata-filtering) in graph search. See [Episode metadata](/adding-business-data#episode-metadata) for full details on metadata constraints and update semantics.

Metadata values must be scalar types (string, number, boolean, or null). A maximum of 10 keys are allowed.

```python Python
from zep_cloud.client import Zep

client = Zep(api_key=API_KEY)

result = client.graph.add_fact_triple(
    user_id=user_id,
    fact="Alice works at Acme Corp",
    fact_name="WORKS_AT",
    source_node_name="Alice",
    target_node_name="Acme Corp",
    metadata={"source": "crm_import", "confidence": 0.95},
)
```

```typescript TypeScript
import { ZepClient } from "@getzep/zep-cloud";

const client = new ZepClient({ apiKey: API_KEY });

const result = await client.graph.addFactTriple({
  userId: userId,
  fact: "Alice works at Acme Corp",
  factName: "WORKS_AT",
  sourceNodeName: "Alice",
  targetNodeName: "Acme Corp",
  metadata: { source: "crm_import", confidence: 0.95 },
});
```

```go Go
import (
    "context"
    "log"

    "github.com/getzep/zep-go/v3"
    zepclient "github.com/getzep/zep-go/v3/client"
    "github.com/getzep/zep-go/v3/option"
)

client := zepclient.NewClient(
    option.WithAPIKey(apiKey),
)

userID := "user123"
sourceNodeName := "Alice"

result, err := client.Graph.AddFactTriple(context.TODO(), &zep.AddTripleRequest{
    UserID:         &userID,
    Fact:           "Alice works at Acme Corp",
    FactName:       "WORKS_AT",
    SourceNodeName: &sourceNodeName,
    TargetNodeName: "Acme Corp",
    Metadata: map[string]interface{}{
        "source":     "crm_import",
        "confidence": 0.95,
    },
})
if err != nil {
    log.Fatalf("Failed to add fact triple: %v", err)
}
```

### Specifying Node UUIDs

You can optionally specify `source_node_uuid` and/or `target_node_uuid` to control which nodes are used. The behavior depends on whether you provide a UUID:

| Scenario                                 | Behavior                                                                                                     |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **UUID provided and node exists**        | Uses the existing node with that UUID                                                                        |
| **UUID provided but node doesn't exist** | Returns a 404 error. You must omit the UUID to create a new node.                                            |
| **UUID omitted**                         | Searches for an existing node by name. If no match is found, creates a new node with an auto-generated UUID. |

See the [associated SDK reference](/sdk-reference/graph/add-fact-triple) for complete details on all available parameters.

## Field limits

| Field                                        | Limit                                                     |
| -------------------------------------------- | --------------------------------------------------------- |
| `fact`                                       | Maximum 250 characters                                    |
| `fact_name`                                  | Maximum 50 characters; must be `SCREAMING_SNAKE_CASE`     |
| `source_node_name`, `target_node_name`       | Maximum 50 characters each                                |
| `source_node_summary`, `target_node_summary` | Maximum 500 characters each                               |
| `valid_at`, `invalid_at`                     | RFC 3339 / ISO 8601 format (e.g., `2024-01-15T10:30:00Z`) |
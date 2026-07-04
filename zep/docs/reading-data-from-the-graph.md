> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Reading Data from the Graph

Zep provides APIs to read Edges, Nodes, and Episodes from the graph. These elements can be retrieved individually using their `UUID`, or as lists associated with a specific `user_id` or `graph_id`. The latter method returns all objects in that user's or graph's data.

Examples of each retrieval method are provided below.

## Reading Edges

```python Python
from zep_cloud.client import Zep

client = Zep(
    api_key=API_KEY,
)

edge = client.graph.edge.get(edgeUuid)
```

```typescript TypeScript
import { ZepClient } from "@getzep/zep-cloud";

const client = new ZepClient({
  apiKey: API_KEY,
});

const edge = await client.graph.edge.get(edgeUuid);
```

```go Go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/getzep/zep-go/v3/client"
    "github.com/getzep/zep-go/v3/option"
)

func main() {
    ctx := context.Background()

    zepClient := client.NewClient(option.WithAPIKey(apiKey))

    edge, err := zepClient.Graph.Edge.Get(ctx, edgeUUID)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("Edge: %+v\n", edge)
}
```

## Reading Nodes

```python Python
from zep_cloud.client import Zep

client = Zep(
    api_key=API_KEY,
)

node = client.graph.node.get_by_user(userUuid)
```

```typescript TypeScript
import { ZepClient } from "@getzep/zep-cloud";

const client = new ZepClient({
  apiKey: API_KEY,
});

const node = await client.graph.node.getByUser(userUuid);
```

```go Go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/getzep/zep-go/v3/client"
    "github.com/getzep/zep-go/v3/option"
)

func main() {
    ctx := context.Background()

    zepClient := client.NewClient(option.WithAPIKey(apiKey))

    nodes, err := zepClient.Graph.Node.GetByUserID(ctx, userUUID, nil)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("Nodes: %+v\n", nodes)
}
```

## Reading Episodes

```python Python
from zep_cloud.client import Zep

client = Zep(
    api_key=API_KEY,
)

episode = client.graph.episode.get_by_graph_id(graph_uuid)
```

```typescript TypeScript
import { ZepClient } from "@getzep/zep-cloud";

const client = new ZepClient({
  apiKey: API_KEY,
});

const episode = client.graph.episode.getByGraphId(graph_uuid);
```

```go Go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/getzep/zep-go/v3/client"
    "github.com/getzep/zep-go/v3/option"
)

func main() {
    ctx := context.Background()

    zepClient := client.NewClient(option.WithAPIKey(apiKey))

    episodes, err := zepClient.Graph.Episode.GetByGraphID(ctx, graphUUID, nil)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("Episodes: %+v\n", episodes)
}
```
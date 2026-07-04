> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Get Graph

GET https://api.getzep.com/api/v2/graph/{graphId}

Returns a graph.

Reference: https://help.getzep.com/sdk-reference/graph/get-graph

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /graph/{graphId}:
    get:
      operationId: get-graph
      summary: Get Graph
      description: Returns a graph.
      tags:
        - graph
      parameters:
        - name: graphId
          in: path
          description: The graph_id of the graph to get.
          required: true
          schema:
            type: string
      responses:
        '200':
          description: The graph that was retrieved.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.Graph'
        '404':
          description: Not Found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.APIError'
        '500':
          description: Internal Server Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.APIError'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    apidata.Graph:
      type: object
      properties:
        created_at:
          type: string
        description:
          type: string
        graph_id:
          type: string
        id:
          type: integer
        name:
          type: string
        project_uuid:
          type: string
        uuid:
          type: string
      title: apidata.Graph
    apidata.APIError:
      type: object
      properties:
        message:
          type: string
      title: apidata.APIError

```

## Examples



**Response**

```json
{
  "created_at": "string",
  "description": "string",
  "graph_id": "string",
  "id": 1,
  "name": "string",
  "project_uuid": "string",
  "uuid": "string"
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.graph.get(
    graph_id="graphId",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.graph.get("graphId");

```

```go
import (
	context "context"
	option "github.com/getzep/zep-go/v3/option"
	v3client "github.com/getzep/zep-go/v3/client"
)

client := v3client.NewClient(
	option.WithAPIKey(
		"<YOUR_APIKey>",
	),
)
response, err := client.Graph.Get(
	context.TODO(),
	"graphId",
)

```
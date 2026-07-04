> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Clone graph

POST https://api.getzep.com/api/v2/graph/clone
Content-Type: application/json

Clone a user or group graph.

Reference: https://help.getzep.com/sdk-reference/graph/clone-graph

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /graph/clone:
    post:
      operationId: clone-graph
      summary: Clone graph
      description: Clone a user or group graph.
      tags:
        - data
      responses:
        '202':
          description: >-
            Response object containing graph_id or user_id pointing to the new
            graph
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.CloneGraphResponse'
        '400':
          description: Bad Request
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
      requestBody:
        description: Clone graph request
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/apidata.CloneGraphRequest'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    apidata.CloneGraphRequest:
      type: object
      properties:
        source_graph_id:
          type: string
          description: >-
            source_graph_id is the ID of the graph to be cloned. Required if
            source_user_id is not provided
        source_user_id:
          type: string
          description: >-
            user_id of the user whose graph is being cloned. Required if
            source_graph_id is not provided
        target_graph_id:
          type: string
          description: >-
            target_graph_id is the ID to be set on the cloned graph. Must not
            point to an existing graph. Required if target_user_id is not
            provided.
        target_user_id:
          type: string
          description: >-
            user_id to be set on the cloned user. Must not point to an existing
            user. Required if target_graph_id is not provided.
      title: apidata.CloneGraphRequest
    apidata.CloneGraphResponse:
      type: object
      properties:
        graph_id:
          type: string
          description: graph_id is the ID of the cloned graph
        task_id:
          type: string
          description: Task ID of the clone graph task
        user_id:
          type: string
      title: apidata.CloneGraphResponse
    apidata.APIError:
      type: object
      properties:
        message:
          type: string
      title: apidata.APIError

```

## Examples



**Request**

```json
{}
```

**Response**

```json
{
  "graph_id": "string",
  "task_id": "string",
  "user_id": "string"
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.graph.clone()

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.graph.clone();

```

```go
import (
	context "context"
	option "github.com/getzep/zep-go/v3/option"
	v3 "github.com/getzep/zep-go/v3"
	v3client "github.com/getzep/zep-go/v3/client"
)

client := v3client.NewClient(
	option.WithAPIKey(
		"<YOUR_APIKey>",
	),
)
response, err := client.Graph.Clone(
	context.TODO(),
	&v3.CloneGraphRequest{},
)

```
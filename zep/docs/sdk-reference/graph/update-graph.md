> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Update Graph.

PATCH https://api.getzep.com/api/v2/graph/{graphId}
Content-Type: application/json

Updates information about a graph.

Reference: https://help.getzep.com/sdk-reference/graph/update-graph

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /graph/{graphId}:
    patch:
      operationId: update-graph
      summary: Update Graph.
      description: Updates information about a graph.
      tags:
        - graph
      parameters:
        - name: graphId
          in: path
          description: Graph ID
          required: true
          schema:
            type: string
      responses:
        '201':
          description: The updated graph object
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.Graph'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.APIError'
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
      requestBody:
        description: Graph
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/apidata.UpdateGraphRequest'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    apidata.UpdateGraphRequest:
      type: object
      properties:
        description:
          type: string
        name:
          type: string
      title: apidata.UpdateGraphRequest
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



**Request**

```json
{}
```

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
client.graph.update(
    graph_id="graphId",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.graph.update("graphId");

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
response, err := client.Graph.Update(
	context.TODO(),
	"graphId",
	&v3.UpdateGraphRequest{},
)

```
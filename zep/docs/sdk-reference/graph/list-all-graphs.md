> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# List all graphs.

GET https://api.getzep.com/api/v2/graph/list-all

Returns all graphs. In order to list users, use user.list_ordered instead

Reference: https://help.getzep.com/sdk-reference/graph/list-all-graphs

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /graph/list-all:
    get:
      operationId: list-all-graphs
      summary: List all graphs.
      description: >-
        Returns all graphs. In order to list users, use user.list_ordered
        instead
      tags:
        - graph
      parameters:
        - name: pageNumber
          in: query
          description: Page number for pagination, starting from 1.
          required: false
          schema:
            type: integer
        - name: pageSize
          in: query
          description: Number of graphs to retrieve per page.
          required: false
          schema:
            type: integer
        - name: search
          in: query
          description: Search term for filtering graphs by graph_id.
          required: false
          schema:
            type: string
        - name: order_by
          in: query
          description: Column to sort by (created_at, group_id, name).
          required: false
          schema:
            type: string
        - name: asc
          in: query
          description: Sort in ascending order.
          required: false
          schema:
            type: boolean
      responses:
        '200':
          description: Successfully retrieved list of graphs.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.GraphListResponse'
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
    apidata.GraphListResponse:
      type: object
      properties:
        graphs:
          type: array
          items:
            $ref: '#/components/schemas/apidata.Graph'
        row_count:
          type: integer
        total_count:
          type: integer
      title: apidata.GraphListResponse
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
  "graphs": [
    {
      "created_at": "string",
      "description": "string",
      "graph_id": "string",
      "id": 1,
      "name": "string",
      "project_uuid": "string",
      "uuid": "string"
    }
  ],
  "row_count": 1,
  "total_count": 1
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.graph.list_all(
    page_number=1,
    page_size=1,
    search="search",
    order_by="order_by",
    asc=True,
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.graph.listAll({
    pageNumber: 1,
    pageSize: 1,
    search: "search",
    orderBy: "order_by",
    asc: true
});

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
response, err := client.Graph.ListAll(
	context.TODO(),
	&v3.GraphListAllRequest{
		PageNumber: v3.Int(
			1,
		),
		PageSize: v3.Int(
			1,
		),
		Search: v3.String(
			"search",
		),
		OrderBy: v3.String(
			"order_by",
		),
		Asc: v3.Bool(
			true,
		),
	},
)

```
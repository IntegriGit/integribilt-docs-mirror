> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Get User Nodes

POST https://api.getzep.com/api/v2/graph/node/user/{user_id}
Content-Type: application/json

Returns all nodes for a user

Reference: https://help.getzep.com/sdk-reference/graph/node/get-user-nodes

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /graph/node/user/{user_id}:
    post:
      operationId: get-user-nodes
      summary: Get User Nodes
      description: Returns all nodes for a user
      tags:
        - entity
      parameters:
        - name: user_id
          in: path
          description: User ID
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Nodes
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/graphiti.EntityNode'
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
        description: Pagination parameters
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/apidata.GraphNodesRequest'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    apidata.GraphNodesRequest:
      type: object
      properties:
        limit:
          type: integer
          description: Maximum number of items to return
        uuid_cursor:
          type: string
          description: >-
            UUID based cursor, used for pagination. Should be the UUID of the
            last item in the previous page
      title: apidata.GraphNodesRequest
    graphiti.EntityNode:
      type: object
      properties:
        attributes:
          type: object
          additionalProperties:
            description: Any type
          description: Additional attributes of the node. Dependent on node labels
        created_at:
          type: string
          description: Creation time of the node
        labels:
          type: array
          items:
            type: string
          description: Labels associated with the node
        name:
          type: string
          description: Name of the node
        relevance:
          type: number
          format: double
          description: >-
            Relevance is an experimental rank-aligned score in [0,1] derived
            from Score via logit transformation.

            Only populated when using cross_encoder reranker; omitted for other
            reranker types (e.g., RRF).
        score:
          type: number
          format: double
          description: >-
            Score is the reranker output: sigmoid-distributed logits [0,1] when
            using cross_encoder reranker, or RRF ordinal rank when using rrf
            reranker
        selection_rank:
          type: integer
          description: >-
            SelectionRank is the global cross-scope rank assigned by auto scope
            selection.
        summary:
          type: string
          description: Regional summary of surrounding edges
        uuid:
          type: string
          description: UUID of the node
      required:
        - created_at
        - name
        - summary
        - uuid
      title: graphiti.EntityNode
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
[
  {
    "created_at": "string",
    "name": "string",
    "summary": "string",
    "uuid": "string",
    "attributes": {},
    "labels": [
      "string"
    ],
    "relevance": 1.1,
    "score": 1.1,
    "selection_rank": 1
  }
]
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.graph.node.get_by_user_id(
    user_id="user_id",
)

```

```typescript
import { ZepClient, Zep } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.graph.node.getByUserId("user_id", {});

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
response, err := client.Graph.Node.GetByUserID(
	context.TODO(),
	"user_id",
	&v3.GraphNodesRequest{},
)

```
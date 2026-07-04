> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Get User Node

GET https://api.getzep.com/api/v2/users/{userId}/node

Returns a user's node.

Reference: https://help.getzep.com/sdk-reference/user/get-user-node

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /users/{userId}/node:
    get:
      operationId: get-user-node
      summary: Get User Node
      description: Returns a user's node.
      tags:
        - user
      parameters:
        - name: userId
          in: path
          description: The user_id of the user to get the node for.
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Response object containing the User node.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.UserNodeResponse'
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
    apidata.UserNodeResponse:
      type: object
      properties:
        node:
          $ref: '#/components/schemas/graphiti.EntityNode'
      title: apidata.UserNodeResponse
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
  "node": {
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
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.user.get_node(
    user_id="userId",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.user.getNode("userId");

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
response, err := client.User.GetNode(
	context.TODO(),
	"userId",
)

```
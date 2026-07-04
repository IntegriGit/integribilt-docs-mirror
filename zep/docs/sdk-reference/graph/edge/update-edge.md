> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Update Edge

PATCH https://api.getzep.com/api/v2/graph/edge/{uuid}
Content-Type: application/json

Updates an entity edge by UUID.

Reference: https://help.getzep.com/sdk-reference/graph/edge/update-edge

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /graph/edge/{uuid}:
    patch:
      operationId: update-edge
      summary: Update Edge
      description: Updates an entity edge by UUID.
      tags:
        - graph
      parameters:
        - name: uuid
          in: path
          description: Edge UUID
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Updated edge
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/graphiti.EntityEdge'
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
        description: Update edge request
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/apidata.UpdateEdgeRequest'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    apidata.UpdateEdgeRequest:
      type: object
      properties:
        attributes:
          type: object
          additionalProperties:
            description: Any type
          description: >-
            Updated attributes. Merged with existing attributes. Set a key to
            null to delete it.
        expired_at:
          type: string
          description: Updated time at which the edge expires
        fact:
          type: string
          description: Updated fact for the edge
        invalid_at:
          type: string
          description: Updated time at which the fact stopped being true
        name:
          type: string
          description: Updated name (relationship type) for the edge
        valid_at:
          type: string
          description: Updated time at which the fact becomes true
      title: apidata.UpdateEdgeRequest
    graphiti.EntityEdge:
      type: object
      properties:
        attributes:
          type: object
          additionalProperties:
            description: Any type
          description: Additional attributes of the edge. Dependent on edge types
        created_at:
          type: string
          description: Creation time of the edge
        episodes:
          type: array
          items:
            type: string
          description: List of episode ids that reference these entity edges
        expired_at:
          type: string
          description: Datetime of when the node was invalidated
        fact:
          type: string
          description: Fact representing the edge and nodes that it connects
        invalid_at:
          type: string
          description: Datetime of when the fact stopped being true
        name:
          type: string
          description: Name of the edge, relation name
        relevance:
          type: number
          format: double
          description: >-
            Relevance is an experimental rank-aligned score in [0,1] derived
            from Score via logit transformation.

            Only populated when using cross_encoder reranker; omitted for other
            reranker types (e.g., RRF).
        scope:
          type: string
          description: Scope of the edge (e.g. "entity", "maybe_related")
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
        source_node_uuid:
          type: string
          description: UUID of the source node
        target_node_uuid:
          type: string
          description: UUID of the target node
        uuid:
          type: string
          description: UUID of the edge
        valid_at:
          type: string
          description: Datetime of when the fact became true
      required:
        - created_at
        - fact
        - name
        - source_node_uuid
        - target_node_uuid
        - uuid
      title: graphiti.EntityEdge
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
  "fact": "string",
  "name": "string",
  "source_node_uuid": "string",
  "target_node_uuid": "string",
  "uuid": "string",
  "attributes": {},
  "episodes": [
    "string"
  ],
  "expired_at": "string",
  "invalid_at": "string",
  "relevance": 1.1,
  "scope": "string",
  "score": 1.1,
  "selection_rank": 1,
  "valid_at": "string"
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.graph.edge.update(
    uuid_="uuid",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.graph.edge.update("uuid");

```

```go
import (
	context "context"
	graph "github.com/getzep/zep-go/v3/graph"
	option "github.com/getzep/zep-go/v3/option"
	v3client "github.com/getzep/zep-go/v3/client"
)

client := v3client.NewClient(
	option.WithAPIKey(
		"<YOUR_APIKey>",
	),
)
response, err := client.Graph.Edge.Update(
	context.TODO(),
	"uuid",
	&graph.UpdateEdgeRequest{},
)

```
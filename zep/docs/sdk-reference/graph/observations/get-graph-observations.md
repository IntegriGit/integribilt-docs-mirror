> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Get Graph Observations

POST https://api.getzep.com/api/v2/graph/observation/graph/{graph_id}
Content-Type: application/json

Returns read-only observation nodes for a graph.

Reference: https://help.getzep.com/sdk-reference/graph/observations/get-graph-observations

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /graph/observation/graph/{graph_id}:
    post:
      operationId: get-graph-observations
      summary: Get Graph Observations
      description: Returns read-only observation nodes for a graph.
      tags:
        - observation
      parameters:
        - name: graph_id
          in: path
          description: Graph ID
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Observations
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/graphiti.DerivedNode'
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
        description: Pagination parameters
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/apidata.GraphObservationsRequest'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    apidata.GraphObservationsRequest:
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
      title: apidata.GraphObservationsRequest
    graphiti.DerivedNode:
      type: object
      properties:
        attributes:
          type: object
          additionalProperties:
            description: Any type
          description: Additional attributes of the derived node.
        created_at:
          type: string
          description: Creation time of the node
        end_at:
          type: string
          description: |-
            EndAt is the close timestamp of the evidence window. Set when the
            underlying pattern is no longer supported (closed observations);
            nil for active observations.
        episode_ids:
          type: array
          items:
            type: string
          description: >-
            Episode UUIDs that support this observation. Only populated for
            observation nodes in web API responses.
        labels:
          type: array
          items:
            type: string
          description: Labels associated with the node
        latest_evidence_at:
          type: string
          description: |-
            LatestEvidenceAt is the most recent source-episode timestamp from
            which this observation drew evidence.
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
        start_at:
          type: string
          description: |-
            StartAt is the earliest source-episode timestamp from which this
            observation was derived. Only populated for observation nodes.
        summary:
          type: string
          description: Region summary of member nodes
        uuid:
          type: string
          description: UUID of the node
      required:
        - created_at
        - name
        - uuid
      title: graphiti.DerivedNode
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
    "uuid": "string",
    "attributes": {},
    "end_at": "string",
    "episode_ids": [
      "string"
    ],
    "labels": [
      "string"
    ],
    "latest_evidence_at": "string",
    "relevance": 1.1,
    "score": 1.1,
    "selection_rank": 1,
    "start_at": "string",
    "summary": "string"
  }
]
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.graph.observation.get_by_graph_id(
    graph_id="graph_id",
)

```

```typescript
import { ZepClient, Zep } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.graph.observation.getByGraphId("graph_id", {});

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
response, err := client.Graph.Observation.GetByGraphID(
	context.TODO(),
	"graph_id",
	&v3.GraphObservationsRequest{},
)

```
> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Get Observation

GET https://api.getzep.com/api/v2/graph/observation/{uuid}

Returns a specific observation node by UUID. Observation nodes are read-only.

Reference: https://help.getzep.com/sdk-reference/graph/observations/get-observation

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /graph/observation/{uuid}:
    get:
      operationId: get-observation
      summary: Get Observation
      description: >-
        Returns a specific observation node by UUID. Observation nodes are
        read-only.
      tags:
        - observation
      parameters:
        - name: uuid
          in: path
          description: Observation UUID
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Observation
          content:
            application/json:
              schema:
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
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
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



**Response**

```json
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
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.graph.observation.get(
    uuid_="uuid",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.graph.observation.get("uuid");

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
response, err := client.Graph.Observation.Get(
	context.TODO(),
	"uuid",
)

```
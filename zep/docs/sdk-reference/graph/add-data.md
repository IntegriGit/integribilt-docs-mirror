> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Add Data

POST https://api.getzep.com/api/v2/graph
Content-Type: application/json

Add data to the graph.

Reference: https://help.getzep.com/sdk-reference/graph/add-data

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /graph:
    post:
      operationId: add-data
      summary: Add Data
      description: Add data to the graph.
      tags:
        - data
      responses:
        '202':
          description: Added episode
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.GraphEpisode'
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
        description: Add data request
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/apidata.AddDataRequest'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    models.GraphDataType:
      type: string
      enum:
        - text
        - json
        - message
        - fact_triple
      title: models.GraphDataType
    apidata.AddDataRequest:
      type: object
      properties:
        created_at:
          type: string
        data:
          type: string
        graph_id:
          type: string
          description: >-
            graph_id is the ID of the graph to which the data will be added. If
            adding to the user graph, please use user_id field instead.
        metadata:
          type: object
          additionalProperties:
            description: Any type
          description: >-
            Optional metadata key-value pairs. Max 10 keys. Values must be
            strings, numbers, booleans, or arrays of scalars.
        source_description:
          type: string
        type:
          $ref: '#/components/schemas/models.GraphDataType'
        user_id:
          type: string
          description: >-
            User ID is the ID of the user to which the data will be added. If
            not adding to a user graph, please use graph_id field instead.
      required:
        - data
        - type
      title: apidata.AddDataRequest
    apidata.RoleType:
      type: string
      enum:
        - norole
        - system
        - assistant
        - user
        - function
        - tool
      title: apidata.RoleType
    apidata.GraphEpisode:
      type: object
      properties:
        content:
          type: string
        created_at:
          type: string
        metadata:
          type: object
          additionalProperties:
            description: Any type
        processed:
          type: boolean
        relevance:
          type: number
          format: double
          description: >-
            Relevance is an experimental rank-aligned score in [0,1] derived
            from Score via logit transformation.

            Only populated when using cross_encoder reranker; omitted for other
            reranker types (e.g., RRF).
        role:
          type: string
          description: >-
            Optional role, will only be present if the episode was created using
            memory.add API
        role_type:
          $ref: '#/components/schemas/apidata.RoleType'
          description: >-
            Optional role_type, will only be present if the episode was created
            using memory.add API
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
        source:
          $ref: '#/components/schemas/models.GraphDataType'
        source_description:
          type: string
        task_id:
          type: string
          description: >-
            Optional task ID to poll episode processing status. Currently only
            available for batch ingestion.
        thread_id:
          type: string
          description: >-
            Optional thread ID, will be present if the episode is part of a
            thread
        uuid:
          type: string
      required:
        - content
        - created_at
        - uuid
      title: apidata.GraphEpisode
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
{
  "data": "string",
  "type": "text"
}
```

**Response**

```json
{
  "content": "string",
  "created_at": "string",
  "uuid": "string",
  "metadata": {},
  "processed": true,
  "relevance": 1.1,
  "role": "string",
  "role_type": "norole",
  "score": 1.1,
  "selection_rank": 1,
  "source": "text",
  "source_description": "string",
  "task_id": "string",
  "thread_id": "string"
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.graph.add(
    data="data",
    type="text",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.graph.add({
    data: "data",
    type: "text"
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
response, err := client.Graph.Add(
	context.TODO(),
	&v3.AddDataRequest{
		Data: "data",
		Type: v3.GraphDataTypeText,
	},
)

```
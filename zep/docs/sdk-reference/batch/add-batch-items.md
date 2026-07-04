> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Add Batch Items

POST https://api.getzep.com/api/v2/batches/{batchId}/items
Content-Type: application/json

Add graph episodes and thread messages to a draft batch. Items are appended in request order.

Reference: https://help.getzep.com/sdk-reference/batch/add-batch-items

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /batches/{batchId}/items:
    post:
      operationId: add-batch-items
      summary: Add Batch Items
      description: >-
        Add graph episodes and thread messages to a draft batch. Items are
        appended in request order.
      tags:
        - batch
      parameters:
        - name: batchId
          in: path
          description: The batch ID.
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Added batch items
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/apidata.BatchItemDetail'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.APIError'
        '403':
          description: Forbidden
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
        '409':
          description: Conflict
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
        description: Batch items to add
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/apidata.AddBatchItemsRequest'
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
    models.BatchItemKind:
      type: string
      enum:
        - graph_episode
        - thread_message
      title: models.BatchItemKind
    apidata.BatchAddItem:
      type: object
      properties:
        content:
          type: string
        created_at:
          type: string
        data:
          type: string
        data_type:
          $ref: '#/components/schemas/models.GraphDataType'
        graph_id:
          type: string
        metadata:
          type: object
          additionalProperties:
            description: Any type
        name:
          type: string
        role:
          $ref: '#/components/schemas/apidata.RoleType'
        source_description:
          type: string
        thread_id:
          type: string
        type:
          $ref: '#/components/schemas/models.BatchItemKind'
        user_id:
          type: string
      required:
        - type
      title: apidata.BatchAddItem
    apidata.AddBatchItemsRequest:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/apidata.BatchAddItem'
      required:
        - items
      title: apidata.AddBatchItemsRequest
    models.BatchItemStatus:
      type: string
      enum:
        - pending
        - queued
        - processing
        - succeeded
        - failed
        - skipped
        - canceled
      title: models.BatchItemStatus
    apidata.BatchItemDetail:
      type: object
      properties:
        created_at:
          type: string
        episode_uuid:
          type: string
          description: >-
            EpisodeUUID is the UUID of the episode that will be (or has been)
            created

            for this batch item. Populated for every item kind and always equal
            to

            SourceUUID — the underlying source row's UUID is reused as the
            episode

            UUID during processing.
        error:
          type: object
          additionalProperties:
            description: Any type
        graph_id:
          type: string
        item_id:
          type: string
        kind:
          $ref: '#/components/schemas/models.BatchItemKind'
        sequence_index:
          type: integer
        source_uuid:
          type: string
        status:
          $ref: '#/components/schemas/models.BatchItemStatus'
        thread_id:
          type: string
        updated_at:
          type: string
        user_id:
          type: string
      title: apidata.BatchItemDetail
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
  "items": [
    {
      "type": "graph_episode"
    }
  ]
}
```

**Response**

```json
[
  {
    "created_at": "string",
    "episode_uuid": "string",
    "error": {},
    "graph_id": "string",
    "item_id": "string",
    "kind": "graph_episode",
    "sequence_index": 1,
    "source_uuid": "string",
    "status": "pending",
    "thread_id": "string",
    "updated_at": "string",
    "user_id": "string"
  }
]
```

**SDK Code**

```python
from zep_cloud import BatchAddItem, Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.batch.add(
    batch_id="batchId",
    items=[
        BatchAddItem(
            type="graph_episode",
        )
    ],
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.batch.add("batchId", {
    items: [{
            type: "graph_episode"
        }]
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
response, err := client.Batch.Add(
	context.TODO(),
	"batchId",
	&v3.ApidataAddBatchItemsRequest{
		Items: []*v3.BatchAddItem{
			&v3.BatchAddItem{
				Type: v3.ApidataBatchAddItemTypeGraphEpisode,
			},
		},
	},
)

```
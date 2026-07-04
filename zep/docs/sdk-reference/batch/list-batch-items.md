> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# List Batch Items

GET https://api.getzep.com/api/v2/batches/{batchId}/items

List items in a batch, including derived runtime status when the batch has been processed.

Reference: https://help.getzep.com/sdk-reference/batch/list-batch-items

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /batches/{batchId}/items:
    get:
      operationId: list-batch-items
      summary: List Batch Items
      description: >-
        List items in a batch, including derived runtime status when the batch
        has been processed.
      tags:
        - batch
      parameters:
        - name: batchId
          in: path
          description: The batch ID.
          required: true
          schema:
            type: string
        - name: limit
          in: query
          description: Maximum number of batch items to return.
          required: false
          schema:
            type: integer
        - name: cursor
          in: query
          description: Pagination cursor from a previous response.
          required: false
          schema:
            type: integer
        - name: status
          in: query
          description: Batch item status filter.
          required: false
          schema:
            type: string
      responses:
        '200':
          description: Batch item list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.BatchItemListResponse'
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
    models.BatchItemKind:
      type: string
      enum:
        - graph_episode
        - thread_message
      title: models.BatchItemKind
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
    apidata.BatchItemListResponse:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/apidata.BatchItemDetail'
        next_cursor:
          type: integer
      title: apidata.BatchItemListResponse
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
  "items": [
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
  ],
  "next_cursor": 1
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.batch.list_items(
    batch_id="batchId",
    limit=1,
    cursor=1,
    status="status",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.batch.listItems("batchId", {
    limit: 1,
    cursor: 1,
    status: "status"
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
response, err := client.Batch.ListItems(
	context.TODO(),
	"batchId",
	&v3.BatchListItemsRequest{
		Limit: v3.Int(
			1,
		),
		Cursor: v3.Int(
			1,
		),
		Status: v3.String(
			"status",
		),
	},
)

```
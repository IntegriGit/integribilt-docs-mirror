> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# List Batches

GET https://api.getzep.com/api/v2/batches

List batches for the current project, optionally filtered by batch status.

Reference: https://help.getzep.com/sdk-reference/batch/list-batches

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /batches:
    get:
      operationId: list-batches
      summary: List Batches
      description: >-
        List batches for the current project, optionally filtered by batch
        status.
      tags:
        - batch
      parameters:
        - name: limit
          in: query
          description: Maximum number of batches to return.
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
          description: Batch status filter.
          required: false
          schema:
            type: string
      responses:
        '200':
          description: Batch list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.BatchListResponse'
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
    apidata.BatchProgress:
      type: object
      properties:
        canceled_items:
          type: integer
        failed_items:
          type: integer
        percent_complete:
          type: number
          format: double
        processing_items:
          type: integer
        queued_items:
          type: integer
        skipped_items:
          type: integer
        succeeded_items:
          type: integer
        total_items:
          type: integer
      title: apidata.BatchProgress
    models.BatchStatus:
      type: string
      enum:
        - draft
        - invalid
        - queued
        - processing
        - succeeded
        - partial
        - failed
        - canceled
      title: models.BatchStatus
    apidata.BatchSummary:
      type: object
      properties:
        batch_id:
          type: string
        completed_at:
          type: string
        created_at:
          type: string
        ignore_roles:
          type: array
          items:
            $ref: '#/components/schemas/apidata.RoleType'
        item_count:
          type: integer
        metadata:
          type: object
          additionalProperties:
            description: Any type
        processed_at:
          type: string
        progress:
          $ref: '#/components/schemas/apidata.BatchProgress'
        status:
          $ref: '#/components/schemas/models.BatchStatus'
        updated_at:
          type: string
      title: apidata.BatchSummary
    apidata.BatchListResponse:
      type: object
      properties:
        batches:
          type: array
          items:
            $ref: '#/components/schemas/apidata.BatchSummary'
        next_cursor:
          type: integer
      title: apidata.BatchListResponse
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
  "batches": [
    {
      "batch_id": "string",
      "completed_at": "string",
      "created_at": "string",
      "ignore_roles": [
        "norole"
      ],
      "item_count": 1,
      "metadata": {},
      "processed_at": "string",
      "progress": {
        "canceled_items": 1,
        "failed_items": 1,
        "percent_complete": 1.1,
        "processing_items": 1,
        "queued_items": 1,
        "skipped_items": 1,
        "succeeded_items": 1,
        "total_items": 1
      },
      "status": "draft",
      "updated_at": "string"
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
client.batch.list(
    limit=1,
    cursor=1,
    status="status",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.batch.list({
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
response, err := client.Batch.List(
	context.TODO(),
	&v3.BatchListRequest{
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
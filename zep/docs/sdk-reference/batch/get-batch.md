> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Get Batch

GET https://api.getzep.com/api/v2/batches/{batchId}

Get a batch summary, including runtime progress when the batch has been processed.

Reference: https://help.getzep.com/sdk-reference/batch/get-batch

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /batches/{batchId}:
    get:
      operationId: get-batch
      summary: Get Batch
      description: >-
        Get a batch summary, including runtime progress when the batch has been
        processed.
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
          description: Batch summary
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.BatchSummary'
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
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.batch.get(
    batch_id="batchId",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.batch.get("batchId");

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
response, err := client.Batch.Get(
	context.TODO(),
	"batchId",
)

```
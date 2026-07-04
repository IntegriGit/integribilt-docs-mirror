> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Get threads

GET https://api.getzep.com/api/v2/threads

Returns all threads.

Reference: https://help.getzep.com/sdk-reference/thread/get-threads

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /threads:
    get:
      operationId: get-threads
      summary: Get threads
      description: Returns all threads.
      tags:
        - thread
      parameters:
        - name: page_number
          in: query
          description: Page number for pagination, starting from 1
          required: false
          schema:
            type: integer
        - name: page_size
          in: query
          description: Number of threads to retrieve per page.
          required: false
          schema:
            type: integer
        - name: order_by
          in: query
          description: >-
            Field to order the results by: created_at, updated_at, user_id,
            thread_id.
          required: false
          schema:
            type: string
        - name: asc
          in: query
          description: 'Order direction: true for ascending, false for descending.'
          required: false
          schema:
            type: boolean
      responses:
        '200':
          description: List of threads
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.ThreadListResponse'
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
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    apidata.Thread:
      type: object
      properties:
        created_at:
          type: string
        project_uuid:
          type: string
        thread_id:
          type: string
        user_id:
          type: string
        uuid:
          type: string
      title: apidata.Thread
    apidata.ThreadListResponse:
      type: object
      properties:
        response_count:
          type: integer
        threads:
          type: array
          items:
            $ref: '#/components/schemas/apidata.Thread'
        total_count:
          type: integer
      title: apidata.ThreadListResponse
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
  "response_count": 1,
  "threads": [
    {
      "created_at": "string",
      "project_uuid": "string",
      "thread_id": "string",
      "user_id": "string",
      "uuid": "string"
    }
  ],
  "total_count": 1
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.thread.list_all(
    page_number=1,
    page_size=1,
    order_by="order_by",
    asc=True,
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.thread.listAll({
    pageNumber: 1,
    pageSize: 1,
    orderBy: "order_by",
    asc: true
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
response, err := client.Thread.ListAll(
	context.TODO(),
	&v3.ThreadListAllRequest{
		PageNumber: v3.Int(
			1,
		),
		PageSize: v3.Int(
			1,
		),
		OrderBy: v3.String(
			"order_by",
		),
		Asc: v3.Bool(
			true,
		),
	},
)

```
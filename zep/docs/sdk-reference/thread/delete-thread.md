> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Delete thread

DELETE https://api.getzep.com/api/v2/threads/{threadId}

Deletes a thread.

Reference: https://help.getzep.com/sdk-reference/thread/delete-thread

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /threads/{threadId}:
    delete:
      operationId: delete-thread
      summary: Delete thread
      description: Deletes a thread.
      tags:
        - thread
      parameters:
        - name: threadId
          in: path
          description: The ID of the thread for which memory should be deleted.
          required: true
          schema:
            type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.SuccessResponse'
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
    apidata.SuccessResponse:
      type: object
      properties:
        message:
          type: string
      title: apidata.SuccessResponse
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
  "message": "string"
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.thread.delete(
    thread_id="threadId",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.thread.delete("threadId");

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
response, err := client.Thread.Delete(
	context.TODO(),
	"threadId",
)

```
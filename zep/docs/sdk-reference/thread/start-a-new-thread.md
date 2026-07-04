> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Start a new thread.

POST https://api.getzep.com/api/v2/threads
Content-Type: application/json

Start a new thread.

Reference: https://help.getzep.com/sdk-reference/thread/start-a-new-thread

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /threads:
    post:
      operationId: start-a-new-thread
      summary: Start a new thread.
      description: Start a new thread.
      tags:
        - thread
      responses:
        '201':
          description: The thread object.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.Thread'
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
        description: Thread
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/models.CreateThreadRequest'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    models.CreateThreadRequest:
      type: object
      properties:
        thread_id:
          type: string
          description: The unique identifier of the thread.
        user_id:
          type: string
          description: The unique identifier of the user associated with the thread
      required:
        - thread_id
        - user_id
      title: models.CreateThreadRequest
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
  "thread_id": "string",
  "user_id": "string"
}
```

**Response**

```json
{
  "created_at": "string",
  "project_uuid": "string",
  "thread_id": "string",
  "user_id": "string",
  "uuid": "string"
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.thread.create(
    thread_id="thread_id",
    user_id="user_id",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.thread.create({
    threadId: "thread_id",
    userId: "user_id"
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
response, err := client.Thread.Create(
	context.TODO(),
	&v3.CreateThreadRequest{
		ThreadID: "thread_id",
		UserID:   "user_id",
	},
)

```
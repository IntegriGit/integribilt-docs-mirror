> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Get messages of a thread

GET https://api.getzep.com/api/v2/threads/{threadId}/messages

Returns messages for a thread.

Reference: https://help.getzep.com/sdk-reference/thread/get-messages-of-a-thread

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /threads/{threadId}/messages:
    get:
      operationId: get-messages-of-a-thread
      summary: Get messages of a thread
      description: Returns messages for a thread.
      tags:
        - thread
      parameters:
        - name: threadId
          in: path
          description: Thread ID
          required: true
          schema:
            type: string
        - name: limit
          in: query
          description: Limit the number of results returned
          required: false
          schema:
            type: integer
        - name: cursor
          in: query
          description: Cursor for pagination
          required: false
          schema:
            type: integer
            format: int64
        - name: lastn
          in: query
          description: >-
            Number of most recent messages to return (overrides limit and
            cursor)
          required: false
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.ThreadMessageListResponse'
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
    apidata.ThreadMessage:
      type: object
      properties:
        content:
          type: string
          description: The content of the message.
        created_at:
          type: string
          description: The timestamp of when the message was created.
        metadata:
          type: object
          additionalProperties:
            description: Any type
          description: The metadata associated with the message.
        name:
          type: string
          description: >-
            Customizable name of the sender of the message (e.g., "john",
            "sales_agent").
        processed:
          type: boolean
          description: Whether the message has been processed.
        role:
          $ref: '#/components/schemas/apidata.RoleType'
          description: The role of message sender (e.g., "user", "system").
        uuid:
          type: string
          description: The unique identifier of the message.
      required:
        - content
        - role
      title: apidata.ThreadMessage
    apidata.ThreadMessageListResponse:
      type: object
      properties:
        messages:
          type: array
          items:
            $ref: '#/components/schemas/apidata.ThreadMessage'
          description: A list of message objects.
        row_count:
          type: integer
          description: The number of messages returned.
        thread_created_at:
          type: string
          description: The thread creation timestamp.
        total_count:
          type: integer
          description: The total number of messages.
        user_id:
          type: string
          description: The user ID associated with this thread.
      title: apidata.ThreadMessageListResponse
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
  "messages": [
    {
      "content": "string",
      "role": "norole",
      "created_at": "string",
      "metadata": {},
      "name": "string",
      "processed": true,
      "uuid": "string"
    }
  ],
  "row_count": 1,
  "thread_created_at": "string",
  "total_count": 1,
  "user_id": "string"
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.thread.get(
    thread_id="threadId",
    limit=1,
    cursor=1000000,
    lastn=1,
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.thread.get("threadId", {
    limit: 1,
    cursor: 1000000,
    lastn: 1
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
response, err := client.Thread.Get(
	context.TODO(),
	"threadId",
	&v3.ThreadGetRequest{
		Limit: v3.Int(
			1,
		),
		Cursor: v3.Int64(
			1000000,
		),
		Lastn: v3.Int(
			1,
		),
	},
)

```
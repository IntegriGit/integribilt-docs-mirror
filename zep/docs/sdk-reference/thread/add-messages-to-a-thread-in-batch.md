> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Add messages to a thread in batch

POST https://api.getzep.com/api/v2/threads/{threadId}/messages-batch
Content-Type: application/json

Deprecated. Use the [Batch API](/adding-batch-data) (`client.batch.*` with `type: "thread_message"`) instead.

Adds messages to a thread in batch mode, processing messages concurrently.


Reference: https://help.getzep.com/sdk-reference/thread/add-messages-to-a-thread-in-batch

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /threads/{threadId}/messages-batch:
    post:
      operationId: add-messages-to-a-thread-in-batch
      summary: Add messages to a thread in batch
      description: >
        Deprecated. Use the [Batch API](/adding-batch-data) (`client.batch.*`
        with `type: "thread_message"`) instead.


        Adds messages to a thread in batch mode, processing messages
        concurrently.
      tags:
        - thread
      parameters:
        - name: threadId
          in: path
          description: The ID of the thread to which messages should be added.
          required: true
          schema:
            type: string
      responses:
        '200':
          description: >-
            An object, optionally containing user context retrieved for the last
            thread message
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.AddThreadMessagesResponse'
        '500':
          description: Internal Server Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.APIError'
      requestBody:
        description: An object representing the thread messages to be added.
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/apidata.AddThreadMessagesRequest'
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
    apidata.AddThreadMessagesRequest:
      type: object
      properties:
        ignore_roles:
          type: array
          items:
            $ref: '#/components/schemas/apidata.RoleType'
          description: >-
            Optional list of role types to ignore when adding messages to graph
            memory.

            The message itself will still be added, retained and used as context
            for messages

            that are added to a user's graph.
        messages:
          type: array
          items:
            $ref: '#/components/schemas/apidata.ThreadMessage'
          description: >-
            A list of message objects, where each message contains a role and
            content.
        return_context:
          type: boolean
          description: >-
            Optionally return context block relevant to the most recent
            messages.
      required:
        - messages
      title: apidata.AddThreadMessagesRequest
    apidata.AddThreadMessagesResponse:
      type: object
      properties:
        context:
          type: string
        message_uuids:
          type: array
          items:
            type: string
        task_id:
          type: string
      title: apidata.AddThreadMessagesResponse
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
  "messages": [
    {
      "content": "string",
      "role": "norole"
    }
  ]
}
```

**Response**

```json
{
  "context": "string",
  "message_uuids": [
    "string"
  ],
  "task_id": "string"
}
```

**SDK Code**

```python
from zep_cloud import Message, Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.thread.add_messages_batch(
    thread_id="threadId",
    messages=[
        Message(
            content="content",
            role="norole",
        )
    ],
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.thread.addMessagesBatch("threadId", {
    messages: [{
            content: "content",
            role: "norole"
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
response, err := client.Thread.AddMessagesBatch(
	context.TODO(),
	"threadId",
	&v3.AddThreadMessagesRequest{
		Messages: []*v3.Message{
			&v3.Message{
				Content: "content",
				Role:    v3.RoleTypeNoRole,
			},
		},
	},
)

```
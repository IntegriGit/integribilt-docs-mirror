> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Updates a message.

PATCH https://api.getzep.com/api/v2/messages/{messageUUID}
Content-Type: application/json

Updates a message.

Reference: https://help.getzep.com/sdk-reference/thread/message/updates-a-message

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /messages/{messageUUID}:
    patch:
      operationId: updates-a-message
      summary: Updates a message.
      description: Updates a message.
      tags:
        - ''
      parameters:
        - name: messageUUID
          in: path
          description: The UUID of the message.
          required: true
          schema:
            type: string
      responses:
        '200':
          description: The updated message.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.ThreadMessage'
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
      requestBody:
        description: The updates.
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/models.ThreadMessageUpdate'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    models.ThreadMessageUpdate:
      type: object
      properties:
        metadata:
          type: object
          additionalProperties:
            description: Any type
      required:
        - metadata
      title: models.ThreadMessageUpdate
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
  "metadata": {}
}
```

**Response**

```json
{
  "content": "string",
  "role": "norole",
  "created_at": "string",
  "metadata": {},
  "name": "string",
  "processed": true,
  "uuid": "string"
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.thread.message.update(
    message_uuid="messageUUID",
    metadata={"key": "value"},
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.thread.message.update("messageUUID", {
    metadata: {
        "key": "value"
    }
});

```

```go
import (
	context "context"
	option "github.com/getzep/zep-go/v3/option"
	thread "github.com/getzep/zep-go/v3/thread"
	v3client "github.com/getzep/zep-go/v3/client"
)

client := v3client.NewClient(
	option.WithAPIKey(
		"<YOUR_APIKey>",
	),
)
response, err := client.Thread.Message.Update(
	context.TODO(),
	"messageUUID",
	&thread.ThreadMessageUpdate{
		Metadata: map[string]interface{}{
			"key": "value",
		},
	},
)

```
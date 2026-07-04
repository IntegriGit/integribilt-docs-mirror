> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Get user context

GET https://api.getzep.com/api/v2/threads/{threadId}/context

Returns most relevant context from the user graph (including memory from any/all past threads) based on the content of the past few messages of the given thread.

Reference: https://help.getzep.com/sdk-reference/thread/get-user-context

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /threads/{threadId}/context:
    get:
      operationId: get-user-context
      summary: Get user context
      description: >-
        Returns most relevant context from the user graph (including memory from
        any/all past threads) based on the content of the past few messages of
        the given thread.
      tags:
        - thread
      parameters:
        - name: threadId
          in: path
          description: The ID of the current thread (for which context is being retrieved).
          required: true
          schema:
            type: string
        - name: template_id
          in: query
          description: Optional template ID to use for custom context rendering.
          required: false
          schema:
            type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.ThreadContextResponse'
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
    apidata.ThreadContextResponse:
      type: object
      properties:
        context:
          type: string
          description: >-
            Context block containing relevant facts, entities, and
            messages/episodes from the user graph. Meant to be replaced in the
            system prompt on every chat turn.
      title: apidata.ThreadContextResponse
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
  "context": "string"
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.thread.get_user_context(
    thread_id="threadId",
    template_id="template_id",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.thread.getUserContext("threadId", {
    templateId: "template_id"
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
response, err := client.Thread.GetUserContext(
	context.TODO(),
	"threadId",
	&v3.ThreadGetUserContextRequest{
		TemplateID: v3.String(
			"template_id",
		),
	},
)

```
> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Get User Threads

GET https://api.getzep.com/api/v2/users/{userId}/threads

Returns all threads for a user.

Reference: https://help.getzep.com/sdk-reference/user/get-user-threads

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /users/{userId}/threads:
    get:
      operationId: get-user-threads
      summary: Get User Threads
      description: Returns all threads for a user.
      tags:
        - user
      parameters:
        - name: userId
          in: path
          description: User ID
          required: true
          schema:
            type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/apidata.Thread'
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
[
  {
    "created_at": "string",
    "project_uuid": "string",
    "thread_id": "string",
    "user_id": "string",
    "uuid": "string"
  }
]
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.user.get_threads(
    user_id="userId",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.user.getThreads("userId");

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
response, err := client.User.GetThreads(
	context.TODO(),
	"userId",
)

```
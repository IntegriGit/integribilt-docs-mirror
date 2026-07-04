> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Update User

PATCH https://api.getzep.com/api/v2/users/{userId}
Content-Type: application/json

Updates a user.

Reference: https://help.getzep.com/sdk-reference/user/update

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /users/{userId}:
    patch:
      operationId: update
      summary: Update User
      description: Updates a user.
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
          description: The user that was updated.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.User'
        '400':
          description: Bad Request
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
      requestBody:
        description: Update User Request
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/apidata.UpdateUserRequest'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    apidata.UpdateUserRequest:
      type: object
      properties:
        disable_default_ontology:
          type: boolean
          description: >-
            When true, disables the use of default/fallback ontology for the
            user's graph.
        email:
          type: string
          description: The email address of the user.
        first_name:
          type: string
          description: The first name of the user.
        last_name:
          type: string
          description: The last name of the user.
        metadata:
          type: object
          additionalProperties:
            description: Any type
          description: The metadata to update
      title: apidata.UpdateUserRequest
    apidata.User:
      type: object
      properties:
        created_at:
          type: string
        deleted_at:
          type: string
        disable_default_ontology:
          type: boolean
        email:
          type: string
        first_name:
          type: string
        id:
          type: integer
        last_name:
          type: string
        metadata:
          type: object
          additionalProperties:
            description: Any type
          description: Deprecated
        project_uuid:
          type: string
        session_count:
          type: integer
          description: Deprecated
        updated_at:
          type: string
          description: Deprecated
        user_id:
          type: string
        uuid:
          type: string
      title: apidata.User
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
{}
```

**Response**

```json
{
  "created_at": "string",
  "deleted_at": "string",
  "disable_default_ontology": true,
  "email": "string",
  "first_name": "string",
  "id": 1,
  "last_name": "string",
  "metadata": {},
  "project_uuid": "string",
  "session_count": 1,
  "updated_at": "string",
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
client.user.update(
    user_id="userId",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.user.update("userId");

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
response, err := client.User.Update(
	context.TODO(),
	"userId",
	&v3.UpdateUserRequest{},
)

```
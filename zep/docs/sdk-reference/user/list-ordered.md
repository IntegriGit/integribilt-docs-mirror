> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Get Users

GET https://api.getzep.com/api/v2/users-ordered

Returns all users.

Reference: https://help.getzep.com/sdk-reference/user/list-ordered

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /users-ordered:
    get:
      operationId: list-ordered
      summary: Get Users
      description: Returns all users.
      tags:
        - user
      parameters:
        - name: pageNumber
          in: query
          description: Page number for pagination, starting from 1
          required: false
          schema:
            type: integer
        - name: pageSize
          in: query
          description: Number of users to retrieve per page
          required: false
          schema:
            type: integer
        - name: search
          in: query
          description: Search term for filtering users by user_id, name, or email
          required: false
          schema:
            type: string
        - name: order_by
          in: query
          description: Column to sort by (created_at, user_id, email)
          required: false
          schema:
            type: string
        - name: asc
          in: query
          description: Sort in ascending order
          required: false
          schema:
            type: boolean
      responses:
        '200':
          description: Successfully retrieved list of users
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.UserListResponse'
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
    apidata.UserListResponse:
      type: object
      properties:
        row_count:
          type: integer
        total_count:
          type: integer
        users:
          type: array
          items:
            $ref: '#/components/schemas/apidata.User'
      title: apidata.UserListResponse
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
  "row_count": 1,
  "total_count": 1,
  "users": [
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
  ]
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.user.list_ordered(
    page_number=1,
    page_size=1,
    search="search",
    order_by="order_by",
    asc=True,
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.user.listOrdered({
    pageNumber: 1,
    pageSize: 1,
    search: "search",
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
response, err := client.User.ListOrdered(
	context.TODO(),
	&v3.UserListOrderedRequest{
		PageNumber: v3.Int(
			1,
		),
		PageSize: v3.Int(
			1,
		),
		Search: v3.String(
			"search",
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
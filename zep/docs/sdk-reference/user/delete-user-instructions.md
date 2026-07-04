> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Delete User Instructions

DELETE https://api.getzep.com/api/v2/user-summary-instructions
Content-Type: application/json

Deletes user summary/instructions for users or project wide defaults.

Reference: https://help.getzep.com/sdk-reference/user/delete-user-instructions

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /user-summary-instructions:
    delete:
      operationId: delete-user-instructions
      summary: Delete User Instructions
      description: Deletes user summary/instructions for users or project wide defaults.
      tags:
        - user
      responses:
        '200':
          description: Instructions deleted successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.SuccessResponse'
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
        description: The instructions to delete
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/apidata.DeleteUserInstructionsRequest'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    apidata.DeleteUserInstructionsRequest:
      type: object
      properties:
        instruction_names:
          type: array
          items:
            type: string
          description: >-
            Unique identifier for the instructions to be deleted. If empty
            deletes all instructions.
        user_ids:
          type: array
          items:
            type: string
          description: >-
            Determines which users will have their custom instructions deleted.
            If no users are provided, the project-wide custom instructions will
            be effected.
      title: apidata.DeleteUserInstructionsRequest
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



**Request**

```json
{}
```

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
client.user.delete_user_summary_instructions()

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.user.deleteUserSummaryInstructions();

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
response, err := client.User.DeleteUserSummaryInstructions(
	context.TODO(),
	&v3.DeleteUserInstructionsRequest{},
)

```
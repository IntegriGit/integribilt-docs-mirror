> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Add User Instructions

POST https://api.getzep.com/api/v2/user-summary-instructions
Content-Type: application/json

Adds new summary instructions for users graphs without removing existing ones. If user_ids is empty, adds to project-wide default instructions.

Reference: https://help.getzep.com/sdk-reference/user/add-user-instructions

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /user-summary-instructions:
    post:
      operationId: add-user-instructions
      summary: Add User Instructions
      description: >-
        Adds new summary instructions for users graphs without removing existing
        ones. If user_ids is empty, adds to project-wide default instructions.
      tags:
        - user
      responses:
        '200':
          description: Instructions added successfully
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
        description: The instructions to add
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/apidata.AddUserInstructionsRequest'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    apidata.UserInstruction:
      type: object
      properties:
        name:
          type: string
        text:
          type: string
      required:
        - name
        - text
      title: apidata.UserInstruction
    apidata.AddUserInstructionsRequest:
      type: object
      properties:
        instructions:
          type: array
          items:
            $ref: '#/components/schemas/apidata.UserInstruction'
          description: Instructions to add to the user summary generation.
        user_ids:
          type: array
          items:
            type: string
          description: >-
            User IDs to add the instructions to. If empty, the instructions are
            added to the project-wide default.
      required:
        - instructions
      title: apidata.AddUserInstructionsRequest
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
{
  "instructions": [
    {
      "name": "string",
      "text": "string"
    }
  ]
}
```

**Response**

```json
{
  "message": "string"
}
```

**SDK Code**

```python
from zep_cloud import UserInstruction, Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.user.add_user_summary_instructions(
    instructions=[
        UserInstruction(
            name="name",
            text="text",
        )
    ],
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.user.addUserSummaryInstructions({
    instructions: [{
            name: "name",
            text: "text"
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
response, err := client.User.AddUserSummaryInstructions(
	context.TODO(),
	&v3.AddUserInstructionsRequest{
		Instructions: []*v3.UserInstruction{
			&v3.UserInstruction{
				Name: "name",
				Text: "text",
			},
		},
	},
)

```
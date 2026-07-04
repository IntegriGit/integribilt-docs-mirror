> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Add Custom Instructions

POST https://api.getzep.com/api/v2/custom-instructions
Content-Type: application/json

Adds new custom instructions for graphs without removing existing ones. If user_ids or graph_ids is empty, adds to project-wide default instructions.

Reference: https://help.getzep.com/sdk-reference/graph/custom-instructions/add-custom-instructions

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /custom-instructions:
    post:
      operationId: add-custom-instructions
      summary: Add Custom Instructions
      description: >-
        Adds new custom instructions for graphs without removing existing ones.
        If user_ids or graph_ids is empty, adds to project-wide default
        instructions.
      tags:
        - graph
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
              $ref: '#/components/schemas/apidata.AddCustomInstructionsRequest'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    apidata.CustomInstruction:
      type: object
      properties:
        name:
          type: string
        text:
          type: string
      required:
        - name
        - text
      title: apidata.CustomInstruction
    apidata.AddCustomInstructionsRequest:
      type: object
      properties:
        graph_ids:
          type: array
          items:
            type: string
          description: >-
            Graph IDs to add the instructions to. If empty, the instructions are
            added to the project-wide default.
        instructions:
          type: array
          items:
            $ref: '#/components/schemas/apidata.CustomInstruction'
          description: Instructions to add to the graph.
        user_ids:
          type: array
          items:
            type: string
          description: >-
            User IDs to add the instructions to. If empty, the instructions are
            added to the project-wide default.
      required:
        - instructions
      title: apidata.AddCustomInstructionsRequest
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
from zep_cloud import CustomInstruction, Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.graph.add_custom_instructions(
    instructions=[
        CustomInstruction(
            name="name",
            text="text",
        )
    ],
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.graph.addCustomInstructions({
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
response, err := client.Graph.AddCustomInstructions(
	context.TODO(),
	&v3.AddCustomInstructionsRequest{
		Instructions: []*v3.CustomInstruction{
			&v3.CustomInstruction{
				Name: "name",
				Text: "text",
			},
		},
	},
)

```
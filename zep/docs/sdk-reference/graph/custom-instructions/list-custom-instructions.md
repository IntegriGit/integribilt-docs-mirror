> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# List Custom Instructions

GET https://api.getzep.com/api/v2/custom-instructions

Lists all custom instructions for a project, user, or graph.

Reference: https://help.getzep.com/sdk-reference/graph/custom-instructions/list-custom-instructions

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /custom-instructions:
    get:
      operationId: list-custom-instructions
      summary: List Custom Instructions
      description: Lists all custom instructions for a project, user, or graph.
      tags:
        - graph
      parameters:
        - name: user_id
          in: query
          description: User ID to get user-specific instructions
          required: false
          schema:
            type: string
        - name: graph_id
          in: query
          description: Graph ID to get graph-specific instructions
          required: false
          schema:
            type: string
      responses:
        '200':
          description: The list of instructions.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.ListCustomInstructionsResponse'
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
    apidata.ListCustomInstructionsResponse:
      type: object
      properties:
        instructions:
          type: array
          items:
            $ref: '#/components/schemas/apidata.CustomInstruction'
      title: apidata.ListCustomInstructionsResponse
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
  "instructions": [
    {
      "name": "string",
      "text": "string"
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
client.graph.list_custom_instructions(
    user_id="user_id",
    graph_id="graph_id",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.graph.listCustomInstructions({
    userId: "user_id",
    graphId: "graph_id"
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
response, err := client.Graph.ListCustomInstructions(
	context.TODO(),
	&v3.GraphListCustomInstructionsRequest{
		UserID: v3.String(
			"user_id",
		),
		GraphID: v3.String(
			"graph_id",
		),
	},
)

```
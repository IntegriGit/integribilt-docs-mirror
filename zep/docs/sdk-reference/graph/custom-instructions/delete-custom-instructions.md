> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Delete Custom Instructions

DELETE https://api.getzep.com/api/v2/custom-instructions
Content-Type: application/json

Deletes custom instructions for graphs or project wide defaults.

Reference: https://help.getzep.com/sdk-reference/graph/custom-instructions/delete-custom-instructions

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /custom-instructions:
    delete:
      operationId: delete-custom-instructions
      summary: Delete Custom Instructions
      description: Deletes custom instructions for graphs or project wide defaults.
      tags:
        - graph
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
              $ref: '#/components/schemas/apidata.DeleteCustomInstructionsRequest'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    apidata.DeleteCustomInstructionsRequest:
      type: object
      properties:
        graph_ids:
          type: array
          items:
            type: string
          description: >-
            Determines which group graphs will have their custom instructions
            deleted. If no graphs are provided, the project-wide custom
            instructions will be affected.
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
            Determines which user graphs will have their custom instructions
            deleted. If no users are provided, the project-wide custom
            instructions will be affected.
      title: apidata.DeleteCustomInstructionsRequest
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
client.graph.delete_custom_instructions()

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.graph.deleteCustomInstructions();

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
response, err := client.Graph.DeleteCustomInstructions(
	context.TODO(),
	&v3.DeleteCustomInstructionsRequest{},
)

```
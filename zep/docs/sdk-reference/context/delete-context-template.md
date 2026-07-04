> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Delete Context Template

DELETE https://api.getzep.com/api/v2/context-templates/{template_id}

Deletes a context template by template_id.

Reference: https://help.getzep.com/sdk-reference/context/delete-context-template

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /context-templates/{template_id}:
    delete:
      operationId: delete-context-template
      summary: Delete Context Template
      description: Deletes a context template by template_id.
      tags:
        - context
      parameters:
        - name: template_id
          in: path
          description: Template ID
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Template deleted successfully
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
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
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
client.context.delete_context_template(
    template_id="template_id",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.context.deleteContextTemplate("template_id");

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
response, err := client.Context.DeleteContextTemplate(
	context.TODO(),
	"template_id",
)

```
> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# List Context Templates

GET https://api.getzep.com/api/v2/context-templates

Lists all context templates.

Reference: https://help.getzep.com/sdk-reference/context/list-context-templates

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /context-templates:
    get:
      operationId: list-context-templates
      summary: List Context Templates
      description: Lists all context templates.
      tags:
        - context
      responses:
        '200':
          description: The list of context templates.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.ListContextTemplatesResponse'
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
    apidata.ContextTemplateResponse:
      type: object
      properties:
        template:
          type: string
          description: The template content.
        template_id:
          type: string
          description: Unique identifier for the template (max 100 characters).
        uuid:
          type: string
          description: Unique identifier for the template.
      title: apidata.ContextTemplateResponse
    apidata.ListContextTemplatesResponse:
      type: object
      properties:
        templates:
          type: array
          items:
            $ref: '#/components/schemas/apidata.ContextTemplateResponse'
      title: apidata.ListContextTemplatesResponse
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
  "templates": [
    {
      "template": "string",
      "template_id": "string",
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
client.context.list_context_templates()

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.context.listContextTemplates();

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
response, err := client.Context.ListContextTemplates(
	context.TODO(),
)

```
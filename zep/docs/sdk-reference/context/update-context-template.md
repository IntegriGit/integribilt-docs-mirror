> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Update Context Template

PUT https://api.getzep.com/api/v2/context-templates/{template_id}
Content-Type: application/json

Updates an existing context template by template_id.

Reference: https://help.getzep.com/sdk-reference/context/update-context-template

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /context-templates/{template_id}:
    put:
      operationId: update-context-template
      summary: Update Context Template
      description: Updates an existing context template by template_id.
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
          description: The updated context template.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.ContextTemplateResponse'
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
        description: The updated template content
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/apidata.UpdateContextTemplateRequest'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    apidata.UpdateContextTemplateRequest:
      type: object
      properties:
        template:
          type: string
          description: The template content (max 1200 characters).
      required:
        - template
      title: apidata.UpdateContextTemplateRequest
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
  "template": "string"
}
```

**Response**

```json
{
  "template": "string",
  "template_id": "string",
  "uuid": "string"
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.context.update_context_template(
    template_id="template_id",
    template="template",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.context.updateContextTemplate("template_id", {
    template: "template"
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
response, err := client.Context.UpdateContextTemplate(
	context.TODO(),
	"template_id",
	&v3.UpdateContextTemplateRequest{
		Template: "template",
	},
)

```
> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Create Context Template

POST https://api.getzep.com/api/v2/context-templates
Content-Type: application/json

Creates a new context template.

Reference: https://help.getzep.com/sdk-reference/context/create-context-template

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /context-templates:
    post:
      operationId: create-context-template
      summary: Create Context Template
      description: Creates a new context template.
      tags:
        - context
      responses:
        '200':
          description: The created context template.
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
        '500':
          description: Internal Server Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.APIError'
      requestBody:
        description: The context template to create
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/apidata.CreateContextTemplateRequest'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    apidata.CreateContextTemplateRequest:
      type: object
      properties:
        template:
          type: string
          description: The template content (max 1200 characters).
        template_id:
          type: string
          description: Unique identifier for the template (max 100 characters).
      required:
        - template
        - template_id
      title: apidata.CreateContextTemplateRequest
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
  "template": "string",
  "template_id": "string"
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
client.context.create_context_template(
    template="template",
    template_id="template_id",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.context.createContextTemplate({
    template: "template",
    templateId: "template_id"
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
response, err := client.Context.CreateContextTemplate(
	context.TODO(),
	&v3.CreateContextTemplateRequest{
		Template:   "template",
		TemplateID: "template_id",
	},
)

```
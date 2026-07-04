> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Retrieves project information

GET https://api.getzep.com/api/v2/projects/info

Retrieve project info based on the provided api key.

Reference: https://help.getzep.com/sdk-reference/project/retrieves-project-information

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /projects/info:
    get:
      operationId: retrieves-project-information
      summary: Retrieves project information
      description: Retrieve project info based on the provided api key.
      tags:
        - project
      responses:
        '200':
          description: Retrieved
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.ProjectInfoResponse'
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
    apidata.ProjectInfo:
      type: object
      properties:
        created_at:
          type: string
        description:
          type: string
        name:
          type: string
        uuid:
          type: string
      title: apidata.ProjectInfo
    apidata.ProjectInfoResponse:
      type: object
      properties:
        project:
          $ref: '#/components/schemas/apidata.ProjectInfo'
      title: apidata.ProjectInfoResponse
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
  "project": {
    "created_at": "string",
    "description": "string",
    "name": "string",
    "uuid": "string"
  }
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.project.get()

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.project.get();

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
response, err := client.Project.Get(
	context.TODO(),
)

```
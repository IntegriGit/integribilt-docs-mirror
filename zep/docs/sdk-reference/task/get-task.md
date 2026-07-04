> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Get Task

GET https://api.getzep.com/api/v2/tasks/{task_id}

Gets a task by its ID

Reference: https://help.getzep.com/sdk-reference/task/get-task

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /tasks/{task_id}:
    get:
      operationId: get-task
      summary: Get Task
      description: Gets a task by its ID
      tags:
        - task
      parameters:
        - name: task_id
          in: path
          description: Task ID
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Task
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.GetTaskResponse'
        '404':
          description: Task not found
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
    apidata.TaskErrorResponse:
      type: object
      properties:
        code:
          type: string
        details:
          type: object
          additionalProperties:
            description: Any type
        message:
          type: string
      title: apidata.TaskErrorResponse
    apidata.TaskProgress:
      type: object
      properties:
        message:
          type: string
        stage:
          type: string
      title: apidata.TaskProgress
    apidata.GetTaskResponse:
      type: object
      properties:
        completed_at:
          type: string
        created_at:
          type: string
        error:
          $ref: '#/components/schemas/apidata.TaskErrorResponse'
        params:
          type: object
          additionalProperties:
            description: Any type
        progress:
          $ref: '#/components/schemas/apidata.TaskProgress'
        started_at:
          type: string
        status:
          type: string
        task_id:
          type: string
        type:
          type: string
        updated_at:
          type: string
      title: apidata.GetTaskResponse
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
  "completed_at": "string",
  "created_at": "string",
  "error": {
    "code": "string",
    "details": {},
    "message": "string"
  },
  "params": {},
  "progress": {
    "message": "string",
    "stage": "string"
  },
  "started_at": "string",
  "status": "string",
  "task_id": "string",
  "type": "string",
  "updated_at": "string"
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.task.get(
    task_id="task_id",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.task.get("task_id");

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
response, err := client.Task.Get(
	context.TODO(),
	"task_id",
)

```
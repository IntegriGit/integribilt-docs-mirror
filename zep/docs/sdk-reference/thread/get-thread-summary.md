> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Get thread summary

GET https://api.getzep.com/api/v2/threads/{threadId}/summary

Returns the incremental summary generated from messages in the thread. Returns 404 if no summary exists for the thread.

Reference: https://help.getzep.com/sdk-reference/thread/get-thread-summary

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /threads/{threadId}/summary:
    get:
      operationId: get-thread-summary
      summary: Get thread summary
      description: >-
        Returns the incremental summary generated from messages in the thread.
        Returns 404 if no summary exists for the thread.
      tags:
        - thread
      parameters:
        - name: threadId
          in: path
          description: The thread ID.
          required: true
          schema:
            type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.ThreadSummary'
        '403':
          description: Forbidden
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
    apidata.ThreadSummary:
      type: object
      properties:
        created_at:
          type: string
          description: CreatedAt is when the summary node was first created.
        last_summarized_at:
          type: string
          description: |-
            LastSummarizedAt is the wall-clock timestamp of the most recent
            summary update. This is an ingestion-time watermark; for the
            event-time recency of the summary's content, use
            LastSummarizedEpisodeValidAt instead.
        last_summarized_episode_valid_at:
          type: string
          description: |-
            LastSummarizedEpisodeValidAt is the maximum episode reference time
            (valid_at) covered by the most recent summary. Use this when
            answering "how recent is this summary's content in event-time?".
        summary:
          type: string
          description: Summary is the incremental summary content.
        thread_id:
          type: string
          description: |-
            ThreadID is the ID of the thread this summary belongs to.
            When a thread was created without an explicit thread_id, this
            field falls back to the thread's UUID. Clients should treat it
            as an opaque identifier.
        uuid:
          type: string
          description: UUID of the thread summary node.
      title: apidata.ThreadSummary
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
  "created_at": "string",
  "last_summarized_at": "string",
  "last_summarized_episode_valid_at": "string",
  "summary": "string",
  "thread_id": "string",
  "uuid": "string"
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.thread.get_summary(
    thread_id="threadId",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.thread.getSummary("threadId");

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
response, err := client.Thread.GetSummary(
	context.TODO(),
	"threadId",
)

```
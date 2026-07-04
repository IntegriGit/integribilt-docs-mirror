> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# List graph ontology

GET https://api.getzep.com/api/v2/graph/list-ontology

Retrieves the current entity and edge types configured for your graph.

See the [full documentation](/customizing-graph-structure) for details.


Reference: https://help.getzep.com/sdk-reference/graph/list-ontology

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /graph/list-ontology:
    get:
      operationId: list-ontology
      summary: List graph ontology
      description: |
        Retrieves the current entity and edge types configured for your graph.

        See the [full documentation](/customizing-graph-structure) for details.
      tags:
        - graph
      responses:
        '200':
          description: Current ontology
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.EntityTypeResponse'
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
    models.EntityPropertyType:
      type: string
      enum:
        - Text
        - Int
        - Float
        - Boolean
      title: models.EntityPropertyType
    apidata.EntityProperty:
      type: object
      properties:
        description:
          type: string
        name:
          type: string
        type:
          $ref: '#/components/schemas/models.EntityPropertyType'
      required:
        - description
        - name
        - type
      title: apidata.EntityProperty
    apidata.EntityEdgeSourceTarget:
      type: object
      properties:
        source:
          type: string
          description: >-
            Source represents the originating node identifier in the edge type
            relationship. (optional)
        target:
          type: string
          description: >-
            Target represents the target node identifier in the edge type
            relationship. (optional)
      title: apidata.EntityEdgeSourceTarget
    apidata.EdgeType:
      type: object
      properties:
        description:
          type: string
        name:
          type: string
        properties:
          type: array
          items:
            $ref: '#/components/schemas/apidata.EntityProperty'
        source_targets:
          type: array
          items:
            $ref: '#/components/schemas/apidata.EntityEdgeSourceTarget'
      required:
        - description
        - name
      title: apidata.EdgeType
    apidata.EntityType:
      type: object
      properties:
        description:
          type: string
        name:
          type: string
        properties:
          type: array
          items:
            $ref: '#/components/schemas/apidata.EntityProperty'
      required:
        - description
        - name
      title: apidata.EntityType
    apidata.EntityTypeResponse:
      type: object
      properties:
        edge_types:
          type: array
          items:
            $ref: '#/components/schemas/apidata.EdgeType'
        entity_types:
          type: array
          items:
            $ref: '#/components/schemas/apidata.EntityType'
      title: apidata.EntityTypeResponse
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
  "edge_types": [
    {
      "description": "string",
      "name": "string",
      "properties": [
        {
          "description": "string",
          "name": "string",
          "type": "Text"
        }
      ],
      "source_targets": [
        {
          "source": "string",
          "target": "string"
        }
      ]
    }
  ],
  "entity_types": [
    {
      "description": "string",
      "name": "string",
      "properties": [
        {
          "description": "string",
          "name": "string",
          "type": "Text"
        }
      ]
    }
  ]
}
```

**SDK Code**

```python
from zep_cloud.client import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
ontology = client.graph.list_ontology()
print("Entity types:", ontology.entity_types)
print("Edge types:", ontology.edge_types)

```

```typescript
import { ZepClient } from "@getzep/zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
const ontology = await client.graph.listOntology();
console.log("Entity types:", ontology.entityTypes);
console.log("Edge types:", ontology.edgeTypes);

```

```go
import (
	context "context"
	fmt "fmt"
	option "github.com/getzep/zep-go/v3/option"
	v3client "github.com/getzep/zep-go/v3/client"
)

client := v3client.NewClient(
	option.WithAPIKey(
		"<YOUR_APIKey>",
	),
)
ontology, err := client.Graph.ListOntology(context.TODO())
if err != nil {
    panic(err)
}
fmt.Printf("Entity types: %+v\n", ontology.EntityTypes)
fmt.Printf("Edge types: %+v\n", ontology.EdgeTypes)

```
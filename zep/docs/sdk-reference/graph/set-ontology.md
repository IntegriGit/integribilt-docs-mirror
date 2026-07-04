> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Set graph ontology

PUT https://api.getzep.com/api/v2/graph/set-ontology
Content-Type: application/json

Sets custom entity and edge types for your graph. This wrapper method
provides a clean interface for defining your graph schema with custom
entity and edge types.

See the [full documentation](/customizing-graph-structure#setting-entity-and-edge-types) for details.


Reference: https://help.getzep.com/sdk-reference/graph/set-ontology

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /graph/set-ontology:
    put:
      operationId: set-ontology
      summary: Set graph ontology
      description: >
        Sets custom entity and edge types for your graph. This wrapper method

        provides a clean interface for defining your graph schema with custom

        entity and edge types.


        See the [full
        documentation](/customizing-graph-structure#setting-entity-and-edge-types)
        for details.
      tags:
        - graph
      responses:
        '200':
          description: Ontology set successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.SuccessResponse'
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                entities:
                  $ref: >-
                    #/components/schemas/GraphSetOntologyPutRequestBodyContentApplicationJsonSchemaEntities
                  description: Dictionary mapping entity type names to their definitions
                edges:
                  $ref: >-
                    #/components/schemas/GraphSetOntologyPutRequestBodyContentApplicationJsonSchemaEdges
                  description: >-
                    Dictionary mapping edge type names to their definitions with
                    source/target constraints
                user_ids:
                  type: array
                  items:
                    type: string
                  description: Optional list of user IDs to apply ontology to
                graph_ids:
                  type: array
                  items:
                    type: string
                  description: Optional list of graph IDs to apply ontology to
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    GraphSetOntologyPutRequestBodyContentApplicationJsonSchemaEntities:
      type: object
      properties: {}
      description: Dictionary mapping entity type names to their definitions
      title: GraphSetOntologyPutRequestBodyContentApplicationJsonSchemaEntities
    GraphSetOntologyPutRequestBodyContentApplicationJsonSchemaEdges:
      type: object
      properties: {}
      description: >-
        Dictionary mapping edge type names to their definitions with
        source/target constraints
      title: GraphSetOntologyPutRequestBodyContentApplicationJsonSchemaEdges
    apidata.SuccessResponse:
      type: object
      properties:
        message:
          type: string
      title: apidata.SuccessResponse

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
from zep_cloud.client import Zep
from zep_cloud.external_clients.ontology import EntityModel, EntityText, EdgeModel
from zep_cloud import EntityEdgeSourceTarget
from pydantic import Field

class Restaurant(EntityModel):
    cuisine_type: EntityText = Field(description="The cuisine type", default=None)

class RestaurantVisit(EdgeModel):
    restaurant_name: EntityText = Field(description="Restaurant name", default=None)

client = Zep(
    api_key="YOUR_API_KEY",
)
client.graph.set_ontology(
    entities={
        "Restaurant": Restaurant,
    },
    edges={
        "RESTAURANT_VISIT": (
            RestaurantVisit,
            [EntityEdgeSourceTarget(source="User", target="Restaurant")]
        ),
    }
)

```

```typescript
import { ZepClient, entityFields, EntityType, EdgeType } from "@getzep/zep-cloud";

const RestaurantSchema: EntityType = {
    description: "Represents a restaurant.",
    fields: {
        cuisine_type: entityFields.text("The cuisine type"),
    },
};

const RestaurantVisit: EdgeType = {
    description: "User visited a restaurant.",
    fields: {
        restaurant_name: entityFields.text("Restaurant name"),
    },
    sourceTargets: [
        { source: "User", target: "Restaurant" },
    ],
};

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.graph.setOntology(
    {
        Restaurant: RestaurantSchema,
    },
    {
        RESTAURANT_VISIT: RestaurantVisit,
    }
);

```

```go
import (
	context "context"
	option "github.com/getzep/zep-go/v3/option"
	v3 "github.com/getzep/zep-go/v3"
	v3client "github.com/getzep/zep-go/v3/client"
)

type Restaurant struct {
    v3.BaseEntity `name:"Restaurant" description:"Represents a restaurant."`
    CuisineType string `description:"The cuisine type" json:"cuisine_type,omitempty"`
}

type RestaurantVisit struct {
    v3.BaseEdge `name:"RESTAURANT_VISIT" description:"User visited a restaurant."`
    RestaurantName string `description:"Restaurant name" json:"restaurant_name,omitempty"`
}

client := v3client.NewClient(
	option.WithAPIKey(
		"<YOUR_APIKey>",
	),
)
_, err := client.Graph.SetOntology(
    context.TODO(),
    []v3.EntityDefinition{
        Restaurant{},
    },
    []v3.EdgeDefinitionWithSourceTargets{
        {
            EdgeModel: RestaurantVisit{},
            SourceTargets: []v3.EntityEdgeSourceTarget{
                {Source: v3.String("User"), Target: v3.String("Restaurant")},
            },
        },
    },
)
if err != nil {
    panic(err)
}

```
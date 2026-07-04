> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Add Fact Triple

POST https://api.getzep.com/api/v2/graph/add-fact-triple
Content-Type: application/json

Add a fact triple for a user or group

Reference: https://help.getzep.com/sdk-reference/graph/add-fact-triple

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /graph/add-fact-triple:
    post:
      operationId: add-fact-triple
      summary: Add Fact Triple
      description: Add a fact triple for a user or group
      tags:
        - entity
      responses:
        '200':
          description: Resulting triple
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/graphiti.AddTripleResponse'
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
        description: Triple to add
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/graphiti.AddTripleRequest'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    graphiti.AddTripleRequest:
      type: object
      properties:
        created_at:
          type: string
          description: The timestamp of the message
        edge_attributes:
          type: object
          additionalProperties:
            description: Any type
          description: >-
            Additional attributes of the edge. Values must be scalar types
            (string, number, boolean, or null).

            Nested objects and arrays are not allowed.
        expired_at:
          type: string
          description: The time (if any) at which the edge expires
        fact:
          type: string
          description: The fact relating the two nodes that this edge represents
        fact_name:
          type: string
          description: >-
            The name of the edge to add. Should be all caps using snake case (eg
            RELATES_TO)
        fact_uuid:
          type: string
          description: The uuid of the edge to add
        graph_id:
          type: string
        invalid_at:
          type: string
          description: The time (if any) at which the fact stops being true
        metadata:
          type: object
          additionalProperties:
            description: Any type
          description: >-
            Optional metadata key-value pairs for the shadow episode created for
            this fact triple.

            Max 10 keys. Values must be strings, numbers, or booleans.
        source_node_attributes:
          type: object
          additionalProperties:
            description: Any type
          description: >-
            Additional attributes of the source node. Values must be scalar
            types (string, number, boolean, or null).

            Nested objects and arrays are not allowed.
        source_node_labels:
          type: array
          items:
            type: string
          description: >-
            The labels for the source node. At most one entity-type label may be

            provided so that manually-added triples remain consistent with
            automatic

            episode extraction, which assigns one best-match entity type per
            node.

            The base "Entity" label is added implicitly by the graph layer on
            save

            and does not need to be supplied here.
        source_node_name:
          type: string
          description: The name of the source node to add
        source_node_summary:
          type: string
          description: The summary of the source node to add
        source_node_uuid:
          type: string
          description: The source node uuid
        target_node_attributes:
          type: object
          additionalProperties:
            description: Any type
          description: >-
            Additional attributes of the target node. Values must be scalar
            types (string, number, boolean, or null).

            Nested objects and arrays are not allowed.
        target_node_labels:
          type: array
          items:
            type: string
          description: >-
            The labels for the target node. At most one entity-type label may be

            provided so that manually-added triples remain consistent with
            automatic

            episode extraction, which assigns one best-match entity type per
            node.

            The base "Entity" label is added implicitly by the graph layer on
            save

            and does not need to be supplied here.
        target_node_name:
          type: string
          description: The name of the target node to add
        target_node_summary:
          type: string
          description: The summary of the target node to add
        target_node_uuid:
          type: string
          description: The target node uuid
        user_id:
          type: string
        valid_at:
          type: string
          description: The time at which the fact becomes true
      required:
        - fact
        - fact_name
      title: graphiti.AddTripleRequest
    graphiti.EntityEdge:
      type: object
      properties:
        attributes:
          type: object
          additionalProperties:
            description: Any type
          description: Additional attributes of the edge. Dependent on edge types
        created_at:
          type: string
          description: Creation time of the edge
        episodes:
          type: array
          items:
            type: string
          description: List of episode ids that reference these entity edges
        expired_at:
          type: string
          description: Datetime of when the node was invalidated
        fact:
          type: string
          description: Fact representing the edge and nodes that it connects
        invalid_at:
          type: string
          description: Datetime of when the fact stopped being true
        name:
          type: string
          description: Name of the edge, relation name
        relevance:
          type: number
          format: double
          description: >-
            Relevance is an experimental rank-aligned score in [0,1] derived
            from Score via logit transformation.

            Only populated when using cross_encoder reranker; omitted for other
            reranker types (e.g., RRF).
        scope:
          type: string
          description: Scope of the edge (e.g. "entity", "maybe_related")
        score:
          type: number
          format: double
          description: >-
            Score is the reranker output: sigmoid-distributed logits [0,1] when
            using cross_encoder reranker, or RRF ordinal rank when using rrf
            reranker
        selection_rank:
          type: integer
          description: >-
            SelectionRank is the global cross-scope rank assigned by auto scope
            selection.
        source_node_uuid:
          type: string
          description: UUID of the source node
        target_node_uuid:
          type: string
          description: UUID of the target node
        uuid:
          type: string
          description: UUID of the edge
        valid_at:
          type: string
          description: Datetime of when the fact became true
      required:
        - created_at
        - fact
        - name
        - source_node_uuid
        - target_node_uuid
        - uuid
      title: graphiti.EntityEdge
    graphiti.EntityNode:
      type: object
      properties:
        attributes:
          type: object
          additionalProperties:
            description: Any type
          description: Additional attributes of the node. Dependent on node labels
        created_at:
          type: string
          description: Creation time of the node
        labels:
          type: array
          items:
            type: string
          description: Labels associated with the node
        name:
          type: string
          description: Name of the node
        relevance:
          type: number
          format: double
          description: >-
            Relevance is an experimental rank-aligned score in [0,1] derived
            from Score via logit transformation.

            Only populated when using cross_encoder reranker; omitted for other
            reranker types (e.g., RRF).
        score:
          type: number
          format: double
          description: >-
            Score is the reranker output: sigmoid-distributed logits [0,1] when
            using cross_encoder reranker, or RRF ordinal rank when using rrf
            reranker
        selection_rank:
          type: integer
          description: >-
            SelectionRank is the global cross-scope rank assigned by auto scope
            selection.
        summary:
          type: string
          description: Regional summary of surrounding edges
        uuid:
          type: string
          description: UUID of the node
      required:
        - created_at
        - name
        - summary
        - uuid
      title: graphiti.EntityNode
    graphiti.AddTripleResponse:
      type: object
      properties:
        edge:
          $ref: '#/components/schemas/graphiti.EntityEdge'
        source_node:
          $ref: '#/components/schemas/graphiti.EntityNode'
        target_node:
          $ref: '#/components/schemas/graphiti.EntityNode'
        task_id:
          type: string
          description: Task ID of the add triple task
      title: graphiti.AddTripleResponse
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
  "fact": "string",
  "fact_name": "string"
}
```

**Response**

```json
{
  "edge": {
    "created_at": "string",
    "fact": "string",
    "name": "string",
    "source_node_uuid": "string",
    "target_node_uuid": "string",
    "uuid": "string",
    "attributes": {},
    "episodes": [
      "string"
    ],
    "expired_at": "string",
    "invalid_at": "string",
    "relevance": 1.1,
    "scope": "string",
    "score": 1.1,
    "selection_rank": 1,
    "valid_at": "string"
  },
  "source_node": {
    "created_at": "string",
    "name": "string",
    "summary": "string",
    "uuid": "string",
    "attributes": {},
    "labels": [
      "string"
    ],
    "relevance": 1.1,
    "score": 1.1,
    "selection_rank": 1
  },
  "target_node": {
    "created_at": "string",
    "name": "string",
    "summary": "string",
    "uuid": "string",
    "attributes": {},
    "labels": [
      "string"
    ],
    "relevance": 1.1,
    "score": 1.1,
    "selection_rank": 1
  },
  "task_id": "string"
}
```

**SDK Code**

```python
from zep_cloud import Zep

client = Zep(
    api_key="YOUR_API_KEY",
)
client.graph.add_fact_triple(
    fact="fact",
    fact_name="fact_name",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.graph.addFactTriple({
    fact: "fact",
    factName: "fact_name"
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
response, err := client.Graph.AddFactTriple(
	context.TODO(),
	&v3.AddTripleRequest{
		Fact:     "fact",
		FactName: "fact_name",
	},
)

```
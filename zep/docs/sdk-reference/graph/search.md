> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Search Graph

POST https://api.getzep.com/api/v2/graph/search
Content-Type: application/json

Perform a graph search query.

Reference: https://help.getzep.com/sdk-reference/graph/search

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /graph/search:
    post:
      operationId: graph
      summary: Search Graph
      description: Perform a graph search query.
      tags:
        - search
      responses:
        '200':
          description: Graph search results or auto-context block
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.GraphSearchResults'
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
        description: Graph search query
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/graphiti.GraphSearchQuery'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    graphiti.Reranker:
      type: string
      enum:
        - rrf
        - mmr
        - node_distance
        - episode_mentions
        - cross_encoder
      title: graphiti.Reranker
    graphiti.GraphSearchScope:
      type: string
      enum:
        - edges
        - nodes
        - episodes
        - thread_summaries
        - observations
        - auto
      title: graphiti.GraphSearchScope
    graphiti.ComparisonOperator:
      type: string
      enum:
        - '='
        - <>
        - '>'
        - <
        - '>='
        - <=
        - IS NULL
        - IS NOT NULL
        - CONTAINS
      title: graphiti.ComparisonOperator
    graphiti.DateFilter:
      type: object
      properties:
        comparison_operator:
          $ref: '#/components/schemas/graphiti.ComparisonOperator'
          description: Comparison operator for date filter
        date:
          type: string
          description: >-
            Date to filter on. Required for non-null operators (=, \<\>, \>, \<,
            \>=, \<=).

            Should be omitted for IS NULL and IS NOT NULL operators.
      required:
        - comparison_operator
      title: graphiti.DateFilter
    graphiti.EpisodeMetadataFilter:
      type: object
      properties:
        comparison_operator:
          $ref: '#/components/schemas/graphiti.ComparisonOperator'
          description: >-
            Comparison operator: =, <>, >, <, >=, <=, IS NULL, IS NOT NULL, IN,
            CONTAINS
        property_name:
          type: string
          description: Metadata key to filter on
        property_value:
          description: >-
            Value to compare against. Not required for IS NULL / IS NOT NULL
            operators.
      required:
        - comparison_operator
        - property_name
      title: graphiti.EpisodeMetadataFilter
    GraphitiMetadataFilterGroupType:
      type: string
      enum:
        - and
        - or
      description: 'Logical operator: "and" or "or"'
      title: GraphitiMetadataFilterGroupType
    graphiti.MetadataFilterGroup:
      type: object
      properties:
        filters:
          type: array
          items:
            $ref: '#/components/schemas/graphiti.EpisodeMetadataFilter'
          description: Leaf filters (predicates on metadata key-value pairs)
        groups:
          type: array
          items:
            $ref: '#/components/schemas/graphiti.MetadataFilterGroup'
          description: Nested sub-groups for composing complex boolean expressions
        type:
          $ref: '#/components/schemas/GraphitiMetadataFilterGroupType'
          description: 'Logical operator: "and" or "or"'
      required:
        - type
      title: graphiti.MetadataFilterGroup
    graphiti.PropertyFilter:
      type: object
      properties:
        comparison_operator:
          $ref: '#/components/schemas/graphiti.ComparisonOperator'
          description: Comparison operator for property filter
        property_name:
          type: string
          description: Property name to filter on
        property_value:
          description: >-
            Property value to match on. Accepted types: string, int, float64,
            bool, or nil.

            Invalid types (e.g., arrays, objects) will be rejected by
            validation.

            Must be non-nil for non-null operators (=, \<\>, \>, \<, \>=, \<=).
      required:
        - comparison_operator
        - property_name
      title: graphiti.PropertyFilter
    graphiti.SearchFilters:
      type: object
      properties:
        created_at:
          type: array
          items:
            type: array
            items:
              $ref: '#/components/schemas/graphiti.DateFilter'
          description: >-
            2D array of date filters for the created_at field.

            The outer array elements are combined with OR logic.

            The inner array elements are combined with AND logic.

            Example: [[\{"\>", date1\}, \{"\<", date2\}], [\{"=", date3\}]]

            This translates to: (created_at \> date1 AND created_at \< date2) OR
            (created_at = date3)
        edge_types:
          type: array
          items:
            type: string
          description: List of edge types to filter on
        edge_uuids:
          type: array
          items:
            type: string
          description: >-
            List of edge UUIDs to filter on. Max 256 to align with graph-service
            filter limits.
        episode_metadata_filters:
          $ref: '#/components/schemas/graphiti.MetadataFilterGroup'
          description: >-
            [Experimental] Episode metadata filter. Restricts results to
            edges/nodes derived from episodes

            matching the metadata predicates. Uses explicit AND/OR groups. This
            feature is experimental and may change in future releases.
        exclude_edge_types:
          type: array
          items:
            type: string
          description: List of edge types to exclude from results
        exclude_node_labels:
          type: array
          items:
            type: string
          description: List of node labels to exclude from results
        expired_at:
          type: array
          items:
            type: array
            items:
              $ref: '#/components/schemas/graphiti.DateFilter'
          description: >-
            2D array of date filters for the expired_at field.

            The outer array elements are combined with OR logic.

            The inner array elements are combined with AND logic.

            Example: [[\{"\>", date1\}, \{"\<", date2\}], [\{"=", date3\}]]

            This translates to: (expired_at \> date1 AND expired_at \< date2) OR
            (expired_at = date3)
        invalid_at:
          type: array
          items:
            type: array
            items:
              $ref: '#/components/schemas/graphiti.DateFilter'
          description: >-
            2D array of date filters for the invalid_at field.

            The outer array elements are combined with OR logic.

            The inner array elements are combined with AND logic.

            Example: [[\{"\>", date1\}, \{"\<", date2\}], [\{"=", date3\}]]

            This translates to: (invalid_at \> date1 AND invalid_at \< date2) OR
            (invalid_at = date3)
        node_labels:
          type: array
          items:
            type: string
          description: List of node labels to filter on
        property_filters:
          type: array
          items:
            $ref: '#/components/schemas/graphiti.PropertyFilter'
          description: List of property filters to apply to nodes and edges
        valid_at:
          type: array
          items:
            type: array
            items:
              $ref: '#/components/schemas/graphiti.DateFilter'
          description: >-
            2D array of date filters for the valid_at field.

            The outer array elements are combined with OR logic.

            The inner array elements are combined with AND logic.

            Example: [[\{"\>", date1\}, \{"\<", date2\}], [\{"=", date3\}]]

            This translates to: (valid_at \> date1 AND valid_at \< date2) OR
            (valid_at = date3)
      title: graphiti.SearchFilters
    graphiti.GraphSearchQuery:
      type: object
      properties:
        bfs_origin_node_uuids:
          type: array
          items:
            type: string
          description: Nodes that are the origins of the BFS searches
        center_node_uuid:
          type: string
          description: Node to rerank around for node distance reranking
        graph_id:
          type: string
          description: >-
            The graph_id to search in. When searching user graph, please use
            user_id instead.
        limit:
          type: integer
          description: >-
            The maximum number of facts to retrieve for non-auto scopes.
            Defaults to 10. Limited to 50. Ignored when scope=auto.
        max_characters:
          type: integer
          description: >-
            Maximum total characters across all selected results when
            scope=auto. Defaults to 2500. Limited to 50000.
        mmr_lambda:
          type: number
          format: double
          description: weighting for maximal marginal relevance
        query:
          type: string
          description: The string to search for (required)
        reranker:
          $ref: '#/components/schemas/graphiti.Reranker'
          description: >-
            Defaults to RRF. Ignored when scope=auto except node_distance and
            episode_mentions are rejected;

            auto search always uses RRF retrieval and applies its own internal
            rerank after retrieval.
        return_raw_results:
          type: boolean
          description: >-
            When scope=auto, include the selected raw graph results alongside
            the materialized context block.

            For graph-service-backed auto mode, selected raw results may include
            episodes,

            edges, nodes, observations, and thread_summaries.
        scope:
          $ref: '#/components/schemas/graphiti.GraphSearchScope'
          description: Defaults to Edges.
        search_filters:
          $ref: '#/components/schemas/graphiti.SearchFilters'
          description: Search filters to apply to the search
        user_id:
          type: string
          description: >-
            The user_id when searching user graph. If not searching user graph,
            please use graph_id instead.
      required:
        - query
      title: graphiti.GraphSearchQuery
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
    apidata.RoleType:
      type: string
      enum:
        - norole
        - system
        - assistant
        - user
        - function
        - tool
      title: apidata.RoleType
    models.GraphDataType:
      type: string
      enum:
        - text
        - json
        - message
        - fact_triple
      title: models.GraphDataType
    apidata.GraphEpisode:
      type: object
      properties:
        content:
          type: string
        created_at:
          type: string
        metadata:
          type: object
          additionalProperties:
            description: Any type
        processed:
          type: boolean
        relevance:
          type: number
          format: double
          description: >-
            Relevance is an experimental rank-aligned score in [0,1] derived
            from Score via logit transformation.

            Only populated when using cross_encoder reranker; omitted for other
            reranker types (e.g., RRF).
        role:
          type: string
          description: >-
            Optional role, will only be present if the episode was created using
            memory.add API
        role_type:
          $ref: '#/components/schemas/apidata.RoleType'
          description: >-
            Optional role_type, will only be present if the episode was created
            using memory.add API
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
        source:
          $ref: '#/components/schemas/models.GraphDataType'
        source_description:
          type: string
        task_id:
          type: string
          description: >-
            Optional task ID to poll episode processing status. Currently only
            available for batch ingestion.
        thread_id:
          type: string
          description: >-
            Optional thread ID, will be present if the episode is part of a
            thread
        uuid:
          type: string
      required:
        - content
        - created_at
        - uuid
      title: apidata.GraphEpisode
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
    graphiti.DerivedNode:
      type: object
      properties:
        attributes:
          type: object
          additionalProperties:
            description: Any type
          description: Additional attributes of the derived node.
        created_at:
          type: string
          description: Creation time of the node
        end_at:
          type: string
          description: |-
            EndAt is the close timestamp of the evidence window. Set when the
            underlying pattern is no longer supported (closed observations);
            nil for active observations.
        episode_ids:
          type: array
          items:
            type: string
          description: >-
            Episode UUIDs that support this observation. Only populated for
            observation nodes in web API responses.
        labels:
          type: array
          items:
            type: string
          description: Labels associated with the node
        latest_evidence_at:
          type: string
          description: |-
            LatestEvidenceAt is the most recent source-episode timestamp from
            which this observation drew evidence.
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
        start_at:
          type: string
          description: |-
            StartAt is the earliest source-episode timestamp from which this
            observation was derived. Only populated for observation nodes.
        summary:
          type: string
          description: Region summary of member nodes
        uuid:
          type: string
          description: UUID of the node
      required:
        - created_at
        - name
        - uuid
      title: graphiti.DerivedNode
    apidata.GraphSearchResponseMetadata:
      type: object
      properties:
        server_latency_ms:
          type: integer
          description: Server-side processing latency in milliseconds.
      title: apidata.GraphSearchResponseMetadata
    graphiti.SagaNode:
      type: object
      properties:
        created_at:
          type: string
          description: Creation time of the node
        labels:
          type: array
          items:
            type: string
          description: Labels associated with the node
        last_summarized_at:
          type: string
          description: >-
            Wall-clock timestamp of the most recent summary update. Used
            internally

            as the watermark for filtering new episodes by ingestion time.
        last_summarized_episode_valid_at:
          type: string
          description: |-
            Maximum episode reference time (valid_at) covered by the most recent
            summary. Use this field — not LastSummarizedAt — when answering "how
            recent is this summary's content in event-time?".
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
          description: Incremental summary of the thread.
        uuid:
          type: string
          description: UUID of the node
      required:
        - created_at
        - name
        - uuid
      title: graphiti.SagaNode
    apidata.GraphSearchResults:
      type: object
      properties:
        context:
          type: string
        edges:
          type: array
          items:
            $ref: '#/components/schemas/graphiti.EntityEdge'
        episodes:
          type: array
          items:
            $ref: '#/components/schemas/apidata.GraphEpisode'
        nodes:
          type: array
          items:
            $ref: '#/components/schemas/graphiti.EntityNode'
        observations:
          type: array
          items:
            $ref: '#/components/schemas/graphiti.DerivedNode'
        response:
          $ref: '#/components/schemas/apidata.GraphSearchResponseMetadata'
        thread_summaries:
          type: array
          items:
            $ref: '#/components/schemas/graphiti.SagaNode'
      title: apidata.GraphSearchResults
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
  "query": "string"
}
```

**Response**

```json
{
  "context": "string",
  "edges": [
    {
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
    }
  ],
  "episodes": [
    {
      "content": "string",
      "created_at": "string",
      "uuid": "string",
      "metadata": {},
      "processed": true,
      "relevance": 1.1,
      "role": "string",
      "role_type": "norole",
      "score": 1.1,
      "selection_rank": 1,
      "source": "text",
      "source_description": "string",
      "task_id": "string",
      "thread_id": "string"
    }
  ],
  "nodes": [
    {
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
    }
  ],
  "observations": [
    {
      "created_at": "string",
      "name": "string",
      "uuid": "string",
      "attributes": {},
      "end_at": "string",
      "episode_ids": [
        "string"
      ],
      "labels": [
        "string"
      ],
      "latest_evidence_at": "string",
      "relevance": 1.1,
      "score": 1.1,
      "selection_rank": 1,
      "start_at": "string",
      "summary": "string"
    }
  ],
  "response": {
    "server_latency_ms": 1
  },
  "thread_summaries": [
    {
      "created_at": "string",
      "name": "string",
      "uuid": "string",
      "labels": [
        "string"
      ],
      "last_summarized_at": "string",
      "last_summarized_episode_valid_at": "string",
      "relevance": 1.1,
      "score": 1.1,
      "selection_rank": 1,
      "summary": "string"
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
client.graph.search(
    query="query",
)

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.graph.search({
    query: "query"
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
response, err := client.Graph.Search(
	context.TODO(),
	&v3.GraphSearchQuery{
		Query: "query",
	},
)

```
> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Detect Patterns (Experimental)

POST https://api.getzep.com/api/v2/graph/patterns
Content-Type: application/json

Detects structural patterns in a knowledge graph including relationship frequencies,
multi-hop paths, co-occurrences, hubs, and clusters.
When a query is provided, uses hybrid search to discover seed nodes,
detects triple-frequency patterns, and returns resolved edges ranked by relevance.

Reference: https://help.getzep.com/sdk-reference/graph/detect-patterns-experimental

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /graph/patterns:
    post:
      operationId: detect-patterns-experimental
      summary: Detect Patterns (Experimental)
      description: >-
        Detects structural patterns in a knowledge graph including relationship
        frequencies,

        multi-hop paths, co-occurrences, hubs, and clusters.

        When a query is provided, uses hybrid search to discover seed nodes,

        detects triple-frequency patterns, and returns resolved edges ranked by
        relevance.
      tags:
        - graph
      responses:
        '200':
          description: Detected patterns
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.DetectPatternsResponse'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/apidata.APIError'
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
      requestBody:
        description: Pattern detection request
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/apidata.DetectPatternsRequest'
servers:
  - url: https://api.getzep.com/api/v2
    description: https://api.getzep.com/api/v2
components:
  schemas:
    apidata.ClusterDetectConfig:
      type: object
      properties: {}
      title: apidata.ClusterDetectConfig
    apidata.CoOccurrenceDetectConfig:
      type: object
      properties:
        max_hops:
          type: integer
          description: >-
            Max hops within which to detect co-occurring node types. Default: 3,
            Max: 5
      title: apidata.CoOccurrenceDetectConfig
    apidata.HubDetectConfig:
      type: object
      properties:
        min_degree:
          type: integer
          description: >-
            Minimum number of connections for a node to be considered a hub.
            Default: 3, Min: 2
      title: apidata.HubDetectConfig
    apidata.PathDetectConfig:
      type: object
      properties:
        max_hops:
          type: integer
          description: 'Max hops from seed nodes for path detection. Default: 3, Max: 5'
      title: apidata.PathDetectConfig
    apidata.RelationshipDetectConfig:
      type: object
      properties: {}
      title: apidata.RelationshipDetectConfig
    apidata.DetectConfig:
      type: object
      properties:
        clusters:
          $ref: '#/components/schemas/apidata.ClusterDetectConfig'
          description: Detect tightly interconnected groups (triangle topology)
        co_occurrences:
          $ref: '#/components/schemas/apidata.CoOccurrenceDetectConfig'
          description: Detect node types that co-occur within k hops
        hubs:
          $ref: '#/components/schemas/apidata.HubDetectConfig'
          description: Detect highly connected hub nodes (star topology)
        paths:
          $ref: '#/components/schemas/apidata.PathDetectConfig'
          description: Detect frequent multi-hop connection paths
        relationships:
          $ref: '#/components/schemas/apidata.RelationshipDetectConfig'
          description: >-
            Detect common (source_label, edge_type, target_label) relationship
            triples
      title: apidata.DetectConfig
    apidata.RecencyWeight:
      type: string
      enum:
        - none
        - 7_days
        - 30_days
        - 90_days
      title: apidata.RecencyWeight
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
    apidata.PatternSeeds:
      type: object
      properties:
        edge_types:
          type: array
          items:
            type: string
          description: All endpoints of these edge types become seeds
        node_labels:
          type: array
          items:
            type: string
          description: All nodes with these labels become seeds
        node_uuids:
          type: array
          items:
            type: string
          description: >-
            Specific node UUIDs to analyze around. Max 10000 to align with
            pattern detection seed limits.
      title: apidata.PatternSeeds
    apidata.DetectPatternsRequest:
      type: object
      properties:
        detect:
          $ref: '#/components/schemas/apidata.DetectConfig'
          description: |-
            Which pattern types to detect with type-specific configuration.
            Omit to detect all types with defaults. Ignored when query is set.
        edge_limit:
          type: integer
          description: >-
            Max resolved edges per pattern. Default: 10, Max: 100. Only used
            with query.
        graph_id:
          type: string
          description: Graph ID when detecting patterns on a named graph
        limit:
          type: integer
          description: 'Max patterns to return. Default: 50, Max: 200'
        min_occurrences:
          type: integer
          description: 'Minimum occurrence count to report a pattern. Default: 2'
        query:
          type: string
          description: >-
            Search query for discovering seed nodes via hybrid search.

            When set, forces triple-frequency detection only and enables edge
            resolution

            with cross-encoder reranking. Mutually exclusive with seeds.
        query_limit:
          type: integer
          description: >-
            Max seed nodes from search. Default: 10, Max: 50. Only used with
            query.
        recency_weight:
          $ref: '#/components/schemas/apidata.RecencyWeight'
          description: |-
            Exponential half-life decay applied to edge created_at timestamps.
            Valid values: none, 7_days, 30_days, 90_days. Default: none
        search_filters:
          $ref: '#/components/schemas/graphiti.SearchFilters'
          description: |-
            Filters which edges/nodes participate in pattern detection.
            Reuses the same filter format as /graph/search.
        seeds:
          $ref: '#/components/schemas/apidata.PatternSeeds'
          description: >-
            Seed selection. If omitted, analyzes the entire graph. Mutually
            exclusive with query.
        user_id:
          type: string
          description: User ID when detecting patterns on a user graph
      title: apidata.DetectPatternsRequest
    apidata.PatternMetadata:
      type: object
      properties:
        edges_analyzed:
          type: integer
          description: Number of edges analyzed
        elapsed_ms:
          type: integer
          description: Elapsed time in milliseconds
        nodes_analyzed:
          type: integer
          description: Number of unique nodes analyzed
      title: apidata.PatternMetadata
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
    apidata.PatternResult:
      type: object
      properties:
        description:
          type: string
          description: >-
            Human-readable structural description of the pattern (e.g. "Person
            -[KNOWS]-> Person").

            Omitted in query mode in favor of Summary.
        edge_types:
          type: array
          items:
            type: string
          description: Edge types in the pattern structure
        edges:
          type: array
          items:
            $ref: '#/components/schemas/graphiti.EntityEdge'
          description: |-
            Resolved edges for this pattern, sorted by cross-encoder relevance.
            Only populated when query is set.
        node_labels:
          type: array
          items:
            type: string
          description: Node labels in the pattern structure
        occurrences:
          type: integer
          description: >-
            Raw structural occurrence count (always unweighted).

            Reflects pattern frequency in the graph, not the number of resolved
            edges after filtering.
        summary:
          type: string
          description: >-
            Fact-derived summary from top reranked edges. Only populated when
            query is set.

            This is the primary display field for QA consumers.
        type:
          type: string
          description: 'Pattern type: relationship, path, co_occurrence, hub, cluster'
        weighted_score:
          type: number
          format: double
          description: >-
            Weighted structural support — equals occurrences when recency_weight
            is "none".

            Reflects graph-level support, not post-enrichment edge count.
      title: apidata.PatternResult
    apidata.DetectPatternsResponse:
      type: object
      properties:
        metadata:
          $ref: '#/components/schemas/apidata.PatternMetadata'
          description: Statistics about the detection run
        nodes:
          type: array
          items:
            $ref: '#/components/schemas/graphiti.EntityNode'
          description: >-
            Resolved nodes referenced by pattern edges (deduplicated). Only
            populated when query is set.
        patterns:
          type: array
          items:
            $ref: '#/components/schemas/apidata.PatternResult'
          description: Detected patterns, sorted by weighted_score descending
      title: apidata.DetectPatternsResponse
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
{}
```

**Response**

```json
{
  "metadata": {
    "edges_analyzed": 1,
    "elapsed_ms": 1,
    "nodes_analyzed": 1
  },
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
  "patterns": [
    {
      "description": "string",
      "edge_types": [
        "string"
      ],
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
      "node_labels": [
        "string"
      ],
      "occurrences": 1,
      "summary": "string",
      "type": "string",
      "weighted_score": 1.1
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
client.graph.detect_patterns()

```

```typescript
import { ZepClient } from "zep-cloud";

const client = new ZepClient({ apiKey: "YOUR_API_KEY" });
await client.graph.detectPatterns();

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
response, err := client.Graph.DetectPatterns(
	context.TODO(),
	&v3.DetectPatternsRequest{},
)

```
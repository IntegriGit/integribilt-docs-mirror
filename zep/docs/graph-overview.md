> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Graph Overview

Zep's temporal knowledge graph powers its context engineering capabilities, including agent memory and Graph RAG. Zep's graph is built on [Graphiti](/graphiti/graphiti/overview), Zep's open-source temporal graph library, which is fully integrated into Zep. Developers do not need to interact directly with Graphiti or understand its underlying implementation.

A knowledge graph is a network of interconnected facts, such as *"Kendra loves
Adidas shoes."* Each fact is a *"triplet"* represented by two entities, or
nodes (*"Kendra", "Adidas shoes"*), and their relationship, or edge
(*"loves"*).

<br />

Knowledge Graphs have been explored extensively for information retrieval.
Zep autonomously builds temporal knowledge graphs, handling changing relationships
and maintaining historical context.

Zep automatically constructs a temporal knowledge graph for each of your users. The knowledge graph contains entities, relationships, and facts related to your user, while automatically handling changing relationships and facts over time.

Here's an example of how Zep might extract graph data from a chat message, and then update the graph once new information is available:

<img src="https://files.buildwithfern.com/zep.docs.buildwithfern.com/2026-07-02T03:44:31.823Z/images/graphiti-graph-intro.gif" alt="graphiti intro slides" />

Each node and edge contains certain attributes - notably, a fact is always stored as an edge attribute. There are also datetime attributes for when the fact becomes valid and when it becomes invalid.

## Graph Data Structure

Zep's graph database stores data in three main types:

1. Entity edges (edges): Represent relationships between nodes and include semantic facts representing the relationship between the edge's nodes.
2. Entity nodes (nodes): Represent entities extracted from episodes, containing summaries of relevant information.
3. Episodic nodes (episodes): Represent raw data stored in Zep, either through chat history or the `graph.add` endpoint.

## Working with the Graph

To learn more about interacting with Zep's graph, refer to the following sections:

* [Adding Data to the Graph](./adding-data-to-the-graph.mdx): Learn how to add new data to the graph.
* [Reading Data from the Graph](./reading-data-from-the-graph.mdx): Discover how to retrieve information from the graph.
* [Searching the Graph](./searching-the-graph.mdx): Explore techniques for efficiently searching the graph.

These guides will help you use Zep's knowledge graph in your applications.
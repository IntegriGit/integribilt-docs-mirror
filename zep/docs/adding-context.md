> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Overview

> Add data to Zep from any source — chat messages, business data, documents, and JSON — and Zep builds the user's Context Graph automatically.

Zep builds Context Graphs from the data you provide. There are several methods for adding context to Zep, each suited for different data types and use cases.

## Available methods

| Method                                            | Data Type                                  | Best For                                                  |
| ------------------------------------------------- | ------------------------------------------ | --------------------------------------------------------- |
| [**Adding messages**](/adding-messages)           | Chat messages                              | Real-time conversation history from your agent            |
| [**Adding business data**](/adding-business-data) | Text, JSON, or message format              | Documents, API responses, emails, or other business data  |
| [**Batch ingestion**](/adding-batch-data)         | Many episodes and/or messages in one batch | Historical backfills, document collections, large imports |

## Customizing how context is built

After adding data, Zep processes it to build Context Graphs. You can customize this process using the options in [Customizing context](/customizing-context).
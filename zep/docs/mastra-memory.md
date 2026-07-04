> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Mastra integration

[Mastra](https://mastra.ai) agents using Zep gain long-term memory backed by a temporal knowledge graph. The `@getzep/zep-mastra` package exposes Zep as a small set of idiomatic Mastra tools your agent calls to persist, search, and recall user context across turns and sessions.

## Core benefits

* **Idiomatic Mastra tools**: Zep's operations drop straight into an `Agent`'s `tools` record
* **Persist, search, and recall**: Store messages and facts, search the graph, and fetch a prompt-ready context block
* **User and standalone graphs**: Bind tools to a user's personal graph or a shared knowledge base
* **Graceful degradation**: A Zep outage is logged and surfaced as a non-fatal result — it never crashes the host agent

## How it works

Zep is a temporal knowledge graph, not a row-oriented message store. A `MastraStorage` adapter would require CRUD operations a temporal knowledge graph can't honor faithfully — there's no row to update or delete in place. Exposing Zep's two real operations — persist and retrieve — as `createTool` tools fits the graph model instead. Provision the Zep user and thread once with `ensureZepUserAndThread`, build the tool set with `createZepToolset` bound to that identity, and attach the tools to your agent.

The toolset provides three tools:

| Tool          | Zep operation                      | What it does                                                                                                                                                          |
| ------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `zepRemember` | `thread.addMessages` / `graph.add` | Persists a message via `thread.addMessages` only when a `role`, `userId`, and `threadId` are all present; otherwise the content is ingested as a fact via `graph.add` |
| `zepSearch`   | `graph.search`                     | Model-callable search over the bound graph; scope, limit, and reranker are pinned at construction                                                                     |
| `zepContext`  | `thread.getUserContext`            | Returns the prompt-ready context block assembled from the whole user graph                                                                                            |

The Mastra integration is **tool-based**: the agent calls a tool to persist or recall memory. There is no automatic context injection — have the agent call the `zepContext` tool when you want the context block in the prompt.

## Installation

```bash
npm install @getzep/zep-mastra @getzep/zep-cloud @mastra/core
```

Requires Node.js 20+, `@mastra/core>=1.42.0` (peer), `@getzep/zep-cloud>=3.23.0`, and a Zep Cloud API key. Get your API key from [app.getzep.com](https://app.getzep.com).

Set up your environment variables:

```bash
export ZEP_API_KEY="your-zep-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

## Usage

Provision the Zep user and thread, build the tool set bound to that identity, and attach the tools to a Mastra `Agent`:

```typescript TypeScript
import { ZepClient } from "@getzep/zep-cloud";
import { Agent } from "@mastra/core/agent";
import { createZepToolset, ensureZepUserAndThread } from "@getzep/zep-mastra";

const client = new ZepClient({ apiKey: process.env.ZEP_API_KEY! });

// 1. Provision the Zep user + thread before the first turn.
const binding = { userId: "user-123", threadId: "thread-abc" };
await ensureZepUserAndThread({ client, ...binding, firstName: "Jane", lastName: "Smith" });

// 2. Build the tool set bound to that user + thread.
const { zepRemember, zepSearch, zepContext } = createZepToolset({ client, binding });

// 3. Attach the tools to an Agent (id and name are both required).
const agent = new Agent({
  id: "memory-agent",
  name: "Memory Agent",
  instructions: "You have long-term memory. Store and recall user facts.",
  model: "openai/gpt-4o-mini",
  tools: { zepRemember, zepSearch, zepContext },
});
```

Each tool is also exported as a standalone factory (`createZepRememberTool`, `createZepSearchTool`, `createZepContextTool`) for wiring a single tool with custom options.

## Tools

Each tool has a typed input and output schema:

| Tool          | Input                                                | Output                                 |
| ------------- | ---------------------------------------------------- | -------------------------------------- |
| `zepRemember` | `content` (string); optional `role`; optional `name` | `{ stored: boolean, message: string }` |
| `zepSearch`   | `query` (string, 1–400 chars)                        | `{ facts: string[], found: boolean }`  |
| `zepContext`  | none                                                 | `{ context: string, found: boolean }`  |

`zepSearch` returns `facts` as extracted strings tailored to the bound scope — edge facts, `"name: summary"` for entities, episode content, and so on — with `found` set to `true` when the result is non-empty.

## Binding: user graph vs standalone graph

Tools are bound to a graph via a `ZepBinding`:

* **`userId`** targets a **user graph** — the home for personalized agent memory. Use it for a conversational agent that remembers an end user. The `zepContext` tool also needs a `threadId` (the thread scopes relevance; retrieval still spans the whole user graph).
* **`graphId`** targets a **standalone graph** — shared or domain knowledge such as a product knowledge base or runbooks. No user node, no user summary.

If both are set, `userId` wins. If neither is set, tools return a graceful "not configured" result instead of throwing.

## Best practices

* **Call `ensureZepUserAndThread` once** before the first turn, then reuse a single `ZepClient`
* **Pass real names** so Zep can anchor the user's identity node in the graph
* **Don't read-after-write within a turn** — Zep builds the graph asynchronously, so a just-stored fact is not instantly retrievable
* **Pass a custom `logger`** to route Zep warnings into your logging stack

## Next steps

* Explore [customizing graph structure](/customizing-graph-structure) for advanced knowledge organization
* Learn about [searching the graph](/searching-the-graph) and how to tune search
* See [code examples](https://github.com/getzep/zep/tree/main/integrations/mastra/typescript/examples) for additional patterns
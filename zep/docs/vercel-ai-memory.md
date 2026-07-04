> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Vercel AI SDK integration

The `@getzep/zep-vercel-ai` package adds long-term memory to the [Vercel AI SDK](https://ai-sdk.dev) (v6), backed by Zep's temporal knowledge graph. It exposes Zep through three layers so you can pick the integration point that fits your call: middleware, helpers, and tools.

## Core benefits

* **Automatic context injection**: Middleware prepends Zep's context block as a system message on each new user turn
* **One write per turn**: An `onFinish` callback persists the full turn once, even across a multi-step tool loop
* **On-demand tools**: Let the model search and persist memory explicitly inside a tool loop
* **Works with `generateText` and `streamText`**: The same inject-and-persist pattern applies to both
* **Graceful degradation**: A Zep outage degrades to "no memory" and never crashes the host call

## How it works

Inject the context block via middleware and persist the whole turn via `onFinish`: the tool loop calls the model once per step, so persisting from a per-step hook would fragment one turn across many writes.

The package exposes three layers:

| Layer          | Export                                                 | Use when                                                                                                     |
| -------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| **Middleware** | `createZepMiddleware`                                  | You want the context block injected automatically as a system message on each new user turn (injection only) |
| **Helpers**    | `getZepContext`, `persistZepTurn`, `createZepOnFinish` | You want explicit control over fetching context and persisting turns                                         |
| **Tools**      | `createZepTools`                                       | You want the model to retrieve and persist on demand inside a tool loop                                      |

`createZepOnFinish` fires exactly once per turn with the final assistant text, so persistence lives there.

## Installation

```bash
npm install @getzep/zep-vercel-ai @getzep/zep-cloud ai zod
```

Requires Node.js 20+, `ai>=6` (the Vercel AI SDK v6; not compatible with v5), `zod` 3 or 4, `@getzep/zep-cloud>=3.23.0`, and a Zep Cloud API key. You'll also want a model provider such as `@ai-sdk/openai`. Get your API key from [app.getzep.com](https://app.getzep.com).

Set up your environment variables:

```bash
export ZEP_API_KEY="your-zep-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

## Usage with generateText

Provision the Zep user and thread, wrap the model to inject context, optionally add tools, and persist the turn via `onFinish`:

```typescript TypeScript
import { ZepClient } from "@getzep/zep-cloud";
import { openai } from "@ai-sdk/openai";
import { generateText, stepCountIs, wrapLanguageModel } from "ai";
import {
  createZepMiddleware,
  createZepOnFinish,
  createZepTools,
  ensureZepUserAndThread,
} from "@getzep/zep-vercel-ai";

const client = new ZepClient({ apiKey: process.env.ZEP_API_KEY! });

// 1. Provision the Zep user + thread before the first turn.
await ensureZepUserAndThread({ client, userId: "u1", threadId: "t1", firstName: "Jane" });

// 2. Wrap the model: inject the context block on each new user turn (inject-only).
const model = wrapLanguageModel({
  model: openai("gpt-4o-mini"),
  middleware: createZepMiddleware({ client, threadId: "t1" }),
});

// 3. Optionally let the model search/store memory explicitly.
const tools = createZepTools(client, { binding: { userId: "u1", threadId: "t1" } });

// 4. Persist the whole turn once per turn via onFinish.
const prompt = "What do you remember about me?";
const { text } = await generateText({
  model,
  tools,
  stopWhen: stepCountIs(5),
  prompt,
  onFinish: createZepOnFinish({ client, threadId: "t1", user: prompt }),
});
```

If your OpenAI organization enforces Zero Data Retention, use `openai.chat('gpt-4o-mini')` (Chat Completions API) instead of `openai('gpt-4o-mini')`. The Responses API references server-persisted item IDs across a multi-step tool loop, which ZDR organizations reject. This is an OpenAI account constraint, not a Zep issue.

## Usage with streamText

The same pattern works unchanged for streaming — inject via middleware, persist via `onFinish`:

```typescript TypeScript
import { streamText, wrapLanguageModel } from "ai";
import { openai } from "@ai-sdk/openai";
import { createZepMiddleware, createZepOnFinish } from "@getzep/zep-vercel-ai";

const userInput = "I just adopted a beagle named Cooper.";

const model = wrapLanguageModel({
  model: openai("gpt-4o-mini"),
  middleware: createZepMiddleware({ client, threadId: "t1" }),
});

const result = streamText({
  model,
  prompt: userInput,
  onFinish: createZepOnFinish({ client, threadId: "t1", user: userInput }),
});

for await (const chunk of result.textStream) process.stdout.write(chunk);
```

To set the system prompt yourself instead of using the middleware, fetch the block with `getZepContext` and persist with `persistZepTurn` (or `createZepOnFinish`) directly.

## The layers in detail

### createZepMiddleware

Returns a Vercel AI SDK `LanguageModelMiddleware` for `wrapLanguageModel`. Injection only — it does not persist. Its `transformParams` fetches the context block and prepends it as a `system` message, but only on a genuine new user turn (detected by the last prompt message being a `user` message). On tool-loop continuation steps it injects nothing, so the block is fetched at most once per turn. Options include `formatContext`, `templateId`, and `logger`.

### createZepOnFinish

Returns an `onFinish` callback that persists the whole turn once — the user's input plus the final assistant text — via `thread.addMessages`. Because `onFinish` fires exactly once per turn for both `generateText` and `streamText`, it records exactly one user message and one assistant message and never writes intermediate tool-call preamble. Supply the user side via `user` (a string or a `(event) => string` resolver); the assistant side is taken from `event.text`.

### getZepContext and persistZepTurn

Plain async functions with no framework coupling. `getZepContext` returns the prompt-ready context block string. `persistZepTurn` writes a `{ user?, assistant? }` turn; pass `{ returnContext: true }` to fold persist and retrieval into one round-trip.

### createZepTools

Returns `{ zepSearch, zepRemember, zepContext }` built with the AI SDK's `tool()` and Zod schemas. Spread them into a `generateText` / `streamText` `tools` record so the model decides when to retrieve or persist. Each tool is also exported as a standalone factory (`createZepSearchTool`, `createZepRememberTool`, `createZepContextTool`).

The tools return typed results: `zepSearch` → `{ facts: string[], found: boolean }`, `zepRemember` → `{ stored: boolean, message: string }`, and `zepContext` → `{ context: string, found: boolean }`. `zepSearch` defaults to the `edges` scope (facts/relationships) — the most useful scope for an agent recalling discrete claims — and its `facts` are extracted strings tailored to the bound scope (edge facts, `"name: summary"` for entities, episode content, and so on).

## Binding: user graph vs standalone graph

`createZepTools` is bound to a graph via a `ZepBinding`:

* **`userId`** targets a **user graph** — the home for personalized agent memory. `zepContext` and the middleware also need a `threadId` (the thread scopes relevance; retrieval still spans the whole user graph).
* **`graphId`** targets a **standalone graph** — shared or domain knowledge such as a product knowledge base or runbooks.

If both are set, `userId` wins. If neither is set, tools return a graceful "not configured" result instead of throwing.

## Best practices

* **Inject via middleware, persist via `onFinish`** — this records exactly one user and one assistant message per turn
* **Call `ensureZepUserAndThread` once** before the first turn, then reuse a single `ZepClient`
* **Use AI SDK v6** — this package is not compatible with v5
* **Don't read-after-write within a turn** — Zep builds the graph asynchronously, so a just-stored fact is not instantly retrievable

## Next steps

* Explore [customizing graph structure](/customizing-graph-structure) for advanced knowledge organization
* Learn about [searching the graph](/searching-the-graph) and how to tune search
* See [code examples](https://github.com/getzep/zep/tree/main/integrations/vercel-ai/typescript/examples) for additional patterns
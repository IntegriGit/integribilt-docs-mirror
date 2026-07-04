> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Evaluate Zep for Your Use Case

This guide shows you how to use Zep's evaluation harness to systematically test your context implementation.

## Why use the evaluation harness?

With this evaluation harness, you can:

* **Evaluate Zep's performance for your use case**: Test how well Zep retrieves relevant information and answers questions specific to your domain and conversation patterns.
* **Systematically experiment with Zep ontologies, search strategies, and other capabilities**: Compare different configurations to optimize retrieval accuracy and response quality.
* **Develop a suite of tests that can be run in CI**: Continuously evaluate your application for regressions, ensuring that changes to your data model or Zep configuration don't degrade context retrieval performance over time.

The harness provides objective metrics for context completeness and answer accuracy, enabling data-driven decisions about context configuration and search strategies.

## Steps

### Clone the Zep repository

Clone the [Zep repository](https://github.com/getzep/zep/tree/main) that includes the evaluation harness:

```bash
git clone https://github.com/getzep/zep.git
cd zep/zep-eval-harness
```

### Set up your environment

Install UV package manager for macOS/Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For other platforms, visit the [UV installation guide](https://docs.astral.sh/uv/).

Install all required dependencies using UV:

```bash
uv sync
```

Set up your API keys by copying the example file and adding your keys:

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```bash
ZEP_API_KEY=your-zep-api-key
OPENAI_API_KEY=your-openai-api-key
```

Get your Zep API key at [app.getzep.com](https://app.getzep.com) and OpenAI API key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys).

### Write down 3-5 example interactions

**Most important step**: This is the most critical part of the evaluation process. Take time to write down 3-5 specific examples that showcase how you want your agent to behave once it has context. These examples will be dropped into an AI prompt in the next step to automatically generate your evaluation data.

For each example, simply note what the user asks and what the agent should respond with:

```
1. User: "What is my dog's name?"
   Agent: "Max"

2. User: "When is my vet appointment?"
   Agent: "Friday at Dr. Peterson's clinic"

3. User: "What training classes did I sign up for?"
   Agent: "Puppy training classes at PetSmart, Saturdays at 9am"
```

### Use a coding agent to update the test data

Use Cursor, Copilot, Claude Code, or another coding agent to automatically update the test files based on your examples.

Provide this prompt to your coding agent:

```text
Please update the files in the zep-eval-harness to match the example interactions below.

Important: Use the existing user in `data/users.json` (user_id: zep_eval_test_user_001).
Do not create or modify any users.

First, read the README.md file in the zep-eval-harness directory to understand the
best practices for creating conversations and test cases.

Step 1 - Generate test cases first:
For `data/test_cases/`:
- Create one file: `zep_eval_test_user_001_tests.json`
- Follow the format and structure of the existing test case files
- Generate exactly 10 test cases based on my example interactions, expanding on them
  with variations and related questions
- Write clear golden_answer text that specifies what information must be present
  in a correct response
- Follow the best practices in the README for designing fair test cases

Step 2 - Generate conversations that contain the answers:
For `data/conversations/`:
- Create exactly 5 conversation files named `zep_eval_test_user_001_conv_001.json`
  through `zep_eval_test_user_001_conv_005.json`
- Each conversation file should contain exactly 6 messages (alternating user/assistant)
- Follow the format and structure of the existing conversation files
- CRITICAL: Ensure that the information needed to answer ALL test questions from
  Step 1 is present somewhere across these 5 conversations
- Spread the information naturally across the conversations
- Make conversations feel natural and contextual
- Follow the best practices in the README for conversation design

Here are my 3-5 example interactions:

[PASTE YOUR 3-5 EXAMPLE INTERACTIONS HERE]
```

### Run the ingestion script

Load your test conversations into Zep:

```bash
uv run zep_ingest.py
```

The ingestion process creates numbered run directories (e.g., `1_20251103T123456`) containing manifest files that document created users, thread IDs, and configuration details.

For ingestion with a custom ontology:

```bash
uv run zep_ingest.py --custom-ontology
```

### Wait for graph processing to complete

After ingestion completes, the Context Graph needs time to process all messages and extract facts, entities, and relationships. Graph processing happens sequentially to preserve the temporal sequence of events.

**Processing time**: 5-10 seconds per message. With 5 conversations of 6 messages each (30 messages total), expect processing to take approximately 2.5-5 minutes.

You can monitor processing status in the Zep dashboard or wait for the recommended time before proceeding to evaluation.

### Run the evaluation script

Execute the evaluation pipeline:

```bash
uv run zep_evaluate.py
```

To evaluate a specific run:

```bash
uv run zep_evaluate.py 1
```

The script processes each test question through four automated steps:

1. **Search**: Query Zep's Context Graph using a cross-encoder reranker to retrieve relevant information
2. **Evaluate context**: Assess whether the retrieved information is sufficient to answer the test question (produces the primary metric: COMPLETE, PARTIAL, or INSUFFICIENT)
3. **Generate response**: Use GPT-4o-mini with the retrieved context to generate an answer
4. **Grade answer**: Evaluate the generated response against the golden answer using GPT-4o (produces the secondary metric: CORRECT or WRONG)

The context completeness evaluation (step 2) is the primary metric as it measures Zep's core capability: retrieving relevant information. The answer grading (step 4) is secondary since it also depends on the LLM's ability to use that context.

Results are saved to `runs/{run_number}/evaluation_results_{timestamp}.json`.

### Interpret your results

The evaluation results include overall accuracy on the test questions and detailed per-test breakdown. Look at these key metrics:

* **Context completeness**: Whether Zep retrieved all necessary information (COMPLETE, PARTIAL, or INSUFFICIENT). This is your primary indicator of Zep's retrieval performance.
* **Answer accuracy**: Whether the generated answer matched your golden answer criteria (CORRECT or WRONG). This measures both retrieval and generation quality.
* **Per-user breakdown**: Performance metrics for each user to identify patterns.
* **Detailed test results**: Individual test case results with retrieved context, generated answers, and the LLM judge's reasoning.

The script prints overall scores and saves detailed results including which questions the agent answered correctly versus missed, along with the LLM judge's reasoning for each evaluation.

### Review results and iterate

Look at the evaluation results to identify any missed questions. For each incorrect answer:

1. Check if the conversation data contains the necessary information
2. Verify the golden\_answer is clear and specific
3. Review the retrieved context in the results JSON to understand what Zep found
4. Adjust your conversations or test questions as needed

If context is consistently incomplete, consider adjusting your data ingestion strategy, search parameters, or graph configuration.

Iterate by modifying your data files, then re-run the ingestion and evaluation scripts.

## Next steps

Once you have the basic evaluation working, consider these next steps:

* **Add more examples and variations**: Expand your test set with additional examples and variations of existing scenarios to cover more edge cases.

* **Evaluate Zep's performance with your existing agent**: Once you've validated Zep's retrieval capabilities with the evaluation harness, integrate Zep into your existing agent and evaluate end-to-end performance. Create test cases based on real user conversations from your application to reflect actual usage patterns. This helps you understand how Zep performs in your complete system, including your agent's prompt engineering, tool calling, and response generation.

* **Define a custom ontology for your domain**: Create entity and edge types tailored to your specific use case for better Context Graph structure and retrieval. Use a coding agent to define custom types based on your conversation data:

```text
Based on the conversations in `data/conversations/`, help me define a custom ontology
for my domain in `ontology.py`.

Please create entity types (classes) and edge types (relationships) that are specific
to my use case and conversation patterns. Follow these guidelines:

- Entity types should be domain-specific (e.g., for healthcare: Patient, Diagnosis,
  Medication; for e-commerce: Product, Order, CustomerIssue)
- Include 1-2 key attributes per entity type using EntityText fields
- Entity names should contain specific values for better semantic search
- Edge types should model the key relationships in my domain
- Add descriptive docstrings explaining when to use each type

Look at the existing `ontology.py` file for the structure and format to follow.

Here's a summary of my use case and domain:
[DESCRIBE YOUR USE CASE AND DOMAIN]
```

After updating `ontology.py`, run ingestion with the custom ontology flag:

```bash
uv run zep_ingest.py --custom-ontology
```

Learn more about [customizing graph structure](/customizing-graph-structure).

* **Add background data**: Ingest a larger dataset before your test conversations to evaluate retrieval performance when relevant information is buried in a larger Context Graph.

* **Test with JSON and unstructured data**: Add JSON documents, transcripts, or business data alongside conversations, then create test questions that require retrieving this non-conversational data. See [Adding Data to the Graph](/adding-data-to-the-graph).

* **Tune search strategy and graph parameters**: Experiment with different rerankers, search scopes, and graph creation settings like [ignoring assistant messages](/adding-messages#ignore-assistant-messages) to optimize performance for your use case. You can customize the evaluation parameters in `zep_evaluate.py`:

```python
# Search limits
FACTS_LIMIT = 20      # Number of edges to return
ENTITIES_LIMIT = 10   # Number of nodes to return
EPISODES_LIMIT = 0    # Disabled by default

# Reranker options: cross_encoder (default), rrf, or mmr
```
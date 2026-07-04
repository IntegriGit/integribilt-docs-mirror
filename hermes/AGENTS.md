# Rocky Brain Agent Instructions

## Mission
All agents working for Lester/Integribilt must use this repository as the shared working-truth layer.

## Core Rules
1. Read the relevant `compiled/global/*.md` and `compiled/projects/<project>/*.md` files before doing serious work.
2. Antigravity-related work must also read `compiled/global/ANTIGRAVITY.md`.
3. MCP-related work must also read `compiled/global/MCP_PROFILES.md` and `compiled/global/GATEWAYS.md`.
4. Cross-agent instruction naming work must also read `compiled/global/MARKDOWN_NAMING.md`.
5. YAML/config work must also read `compiled/global/YAML_RULES.md`.
6. Use source citations for legal, financial, bankruptcy, valuation, tax, or customer-impacting claims.
7. Do not treat raw agent chats as truth. Promote observations through the claim ladder.
8. Do not overwrite canonical markdown without a diff/review path.
9. Submit a tool review after significant tool use, failures, workarounds, or discoveries.
10. Every agent is responsible for checking MCP server logs for MCP servers it uses and correcting safe issues.
11. If information is stale, uncertain, or contradictory, say so and add/update an open question or contradiction.
12. No critical self-rewrites without an eval gate and human approval.

## Source-of-Truth Ladder
1. Direct current user instruction
2. Canonical compiled markdown in this repo
3. Verified source documents / raw evidence
4. Honcho peer/state conclusions
5. Neo4j corroborated relationships
6. Redis or other hot-cache summaries
7. Raw agent chats/logs
8. Unverified extracted claims

## Query Discipline
Agents should ask one question of the brain/access layer instead of guessing which store to query. Until the gateway exists, read the source map and use the best available local source.

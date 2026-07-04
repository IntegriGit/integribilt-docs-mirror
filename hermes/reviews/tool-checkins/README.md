# Tool Checkin / Review Template

Create one markdown or JSON file after significant tool use.

```yaml
id: checkin-YYYYMMDD-HHMMSS-agent-tool
checkout_id: checkout-...
agent: rocky-hermes-default
tool: tool_name
project: integribilt
success: true | false
duration_seconds: 0
result_summary: "What happened"
error: null
workaround: null
source_refs: []
confidence: low | medium | high
recommendation: "What should improve"
should_update_skill: false
should_add_eval: false
completed_at: YYYY-MM-DDTHH:MM:SS
```

## Mandatory Questions
1. Did the tool work?
2. Was the result useful?
3. Was the result stale?
4. Was there missing auth?
5. Was the interface confusing?
6. Did the skill instructions help?
7. What should change?
8. Should this become a skill/tool patch?
9. Should an eval be added?

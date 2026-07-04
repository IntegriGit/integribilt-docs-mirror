# IntegriBilt Runbooks

## Runbook: Legal/Financial Claim Handling
1. Identify the claim.
2. Locate source document or direct user instruction.
3. Record source path/URI and date.
4. Label confidence: low, medium, high.
5. Check contradiction queue.
6. Draft answer with citations and gaps.
7. If used repeatedly, promote to compiled truth or skill candidate.

## Runbook: Foreclosure Appraisal Search
1. Search local Spruce workspace and `_rocky_extract` first.
2. Search Google Drive / Important Docs once auth is available.
3. Search ASM/agent chats for mentions of appraisal, equipment, inventory, and Commerce Dr.
4. Record whether the appraisal includes real estate, equipment, and inventory.
5. If not found, update `OPEN_QUESTIONS.md` and do not claim it has been reviewed.

## Runbook: Tool Review
1. Checkout significant tool use.
2. Execute tool.
3. Checkin with success/failure/duration/output summary.
4. Add recommendation if tool failed or produced surprising results.
5. Promote repeated failures to `SKILL_MAINTENANCE.md`.

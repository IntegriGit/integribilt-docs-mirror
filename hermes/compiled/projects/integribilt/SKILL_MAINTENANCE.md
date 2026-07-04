# IntegriBilt Skill Maintenance

## Purpose
Track recurring agent/tool failures and candidate skill improvements for IntegriBilt work.

## Review Intake Format
Use `reviews/tool-checkins/` for individual tool reviews. Summaries get promoted here only after repeated evidence or high-impact failures.

## Known Issues

### Google Drive access blocked
- Status: open
- Symptom: Rocky cannot directly search Google Drive / Important Docs.
- Cause: missing Google Workspace auth token for Hermes profile.
- Needed fix: authenticate Google Workspace or provide mirrored/exported folder.
- Candidate skill update: add Drive-auth prerequisite checks before claiming Drive search is possible.

### Foreclosure appraisal not found
- Status: open
- Symptom: user assumes the foreclosure appraisal has not been found.
- Needed fix: search Drive/ASM/local evidence once Drive auth or exported docs are available.
- Candidate eval: ask “Where is the foreclosure appraisal source?” and require source path.

### Antigravity 2.0 / ASM uncertainty
- Status: open
- Symptom: ASM may be less effective with Antigravity 2.0.
- Needed fix: compare artifact counts and parse success rates between pre-2.0 and 2.0 outputs.

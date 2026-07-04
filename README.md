# IntegriBilt Docs Mirror

One local, git-versioned, agent-queryable markdown corpus for every tool
IntegriBilt depends on. Design source: `AI-PLATFORM-REANALYSIS-2026-07-04.md`
section 2 (E:\projects\claude\planning\ on OFC01). Tracking issue: INT-118.

## Why

- Agents answer "how does X work" from local files instead of web-searching.
- Nightly refresh means `git diff` of this repo IS the vendor changelog:
  "what changed in X this week" is a `git log`/`git diff` query.

## Layout

One subfolder per source, markdown only. `sources.yaml` is the authoritative
manifest: every folder must have an entry, every entry states its lane,
update method, and upstream.

```
antigravity/      Lane 2  llms.txt fetch from antigravity.google
claude-platform/  Lane 2  llms.txt fetch from platform.claude.com
claude-code/      Lane 1  git-native (anthropic docs + CLI changelog)
paperclip/        Lane 1  git-native (docs/ + doc/ + AGENTS.md from paperclip repo)
litellm/          Lane 1  git-native (BerriAI/litellm docs/my-website/docs)
langchain/        Lane 1  git-native (langchain-ai repos docs dirs)
langgraph/        Lane 1  git-native
langsmith/        Lane 1  git-native
codex/            Lane 1  git-native (openai/codex docs/)
hermes/           Lane 1  git-native (Hermes repo)
```

Lane 3 (JS-rendered residue converted to MD) sources get their own folders as
they are identified; add them to `sources.yaml` in the same commit.

## Rules for contributing agents

1. **Markdown only.** No HTML dumps, PDFs, screenshots, or binaries.
2. **One source = one top-level folder.** Preserve the upstream page/dir
   hierarchy inside it so diffs stay meaningful.
3. **Every folder is registered in `sources.yaml`** with lane, method,
   upstream URL/repo, and the exact refresh command.
4. **No secrets.** These are public vendor docs; if a fetch requires auth,
   stop and flag it on the tracking issue instead.
5. **Commit per source** with message `<source>: <initial pull|refresh> <date>`
   so the nightly digest can attribute changes.

## Refresh

Nightly n8n job on SVR02 (192.168.254.2) runs the refresh commands from
`sources.yaml`, commits, pushes, and posts a "what changed upstream" digest
when the diff is non-trivial. Until that job lands, refresh is manual.

## Querying

Company skill `docs-mirror` documents the query path for agents
(clone location per host, grep/qmd usage). Until the skill is registered:
clone this repo and search it with ripgrep.

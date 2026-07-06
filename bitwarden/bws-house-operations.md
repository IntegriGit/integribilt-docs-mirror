# BWS Secrets Operations (Bitwarden Secrets Manager)

Operate IntegriBilt's secret store correctly. Facts below are verified
against bws 1.0.0 CLI help and Bitwarden's official docs (2026-07-06).
Most LLMs guess at bws syntax — do not guess, use this.

## Mental model (5 objects)

Organization → Projects (folders of secrets) → Secrets (KEY/value/note).
Machine accounts = service identities; each holds Access tokens.
A token can ONLY see projects its machine account is granted on, with
per-project **read** or **read+write**. Grants are managed ONLY in the web
console (Secrets Manager → Machine accounts → Projects tab) — no CLI.

**Error decoding (critical):** a `404 Resource not found` on
`secret create/edit/delete` almost always means the machine account LACKS
WRITE on that project — not that the project is missing. Reads working +
writes 404ing = grant problem. Fix in console, not in CLI.

## Auth

```bash
export BWS_ACCESS_TOKEN="$(sudo cat /etc/bws-token)"   # house pattern, file mode 600
bws secret list -t <token>                              # or per-command
```
Token format `0.{id}.{key}`. It IS a secret: never in git/.bashrc/logs.
Config file: `~/.config/bws/config` (server URLs, profiles, state-dir).
Self-host/EU: `bws config server-base <url>`; profiles via `--profile`.

## Command reference (exact syntax, bws 1.0.0)

```bash
bws project list | get <ID> | create <NAME> | edit <ID> --name <N> | delete <IDS...>

bws secret list [PROJECT_ID]
bws secret get <SECRET_ID>                      # JSON; value: | jq -r '.value'
bws secret create <KEY> <VALUE> <PROJECT_ID> [--note N]   # KEY VALUE PROJECT — this order
bws secret edit [--key K] [--value V] [--note N] [--project-id P] <SECRET_ID>
bws secret delete <SECRET_IDS...>
```

Output formats: `-o json|yaml|env|table|tsv|none`.

## The two killer workflows

**1. Generate a .env from a project (deploy-time cache):**
```bash
bws secret list <PROJECT_ID> -o env > .env && chmod 600 .env
```
Secret KEYs become variable names — name secrets exactly like the env vars
compose expects (SCREAMING_SNAKE). This one-liner IS the approved
BWS → .env → ONE-YAML flow. `.env` is a cache, BWS is truth.

**2. No file at all — inject directly:**
```bash
bws run --project-id <PROJECT_ID> -- docker compose up -d
```
`bws run` injects accessible secrets as env vars into the child process.
Flags: `--shell`, `--no-inherit-env`, `--uuids-as-keynames`. Shell env
still beats .env in compose precedence — prefer bws run OR .env, never mix.

## House structure (from-scratch design, 2026-07-06)

- Projects: `svr02-stack`, `ofc01-stack`, `shared-providers`
  (LLM/API vendor keys used by both), one per future fleet host as needed.
- Machine accounts, least privilege:
  `svr02` → RW svr02-stack, R shared-providers
  `ofc01` → RW ofc01-stack, R shared-providers
  Admin/backfill writes happen via console or a short-lived admin token.
- Token storage: `/etc/bws-token` (root, 600) on Linux; protected file on
  Windows. One machine account per host so a leak burns one machine.
- Secret naming = env var naming, prefixed by consumer:
  `LITELLM_MASTER_KEY`, `PAPERCLIP_AUTH_SECRET`, `POSTGRES_PASSWORD`.
- Rotation: any secret that ever touched a chat log, git history, or a
  multi-writer .env is presumed burned — rotate on migration into BWS.

## Rules

1. BWS is the only source of truth. `.env` files are regenerated caches;
   hand-edits WILL be wiped by the next deploy — backfill BWS same day.
2. Never echo a value. Verify with `| jq -r '.value' | wc -c`.
3. 404 on write → check console grants before anything else.
4. Unknown secret ID needed → ask the owner; never invent.
5. Humans use the web console; `bw` (password manager) is off-limits to
   automation.

## Docs

Local mirror: docs-mirror/bitwarden/. Upstream:
https://bitwarden.com/help/secrets-manager-cli/ ·
https://bitwarden.com/help/developer-quick-start/

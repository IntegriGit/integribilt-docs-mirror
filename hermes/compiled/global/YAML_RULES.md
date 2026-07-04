# YAML Rules

## Required YAML Source
The Integribilt stack compose YAML lives on SVR02 at:

```text
/home/lmiller/integribilt-stack/docker-compose.yml
```

It can also be accessed and pushed from OFC01 at this clone:

```text
E:/clones/docs/integribilt-stack
```

## Clone Convention
When reasonably possible on OFC01/Windows machines, clones go under:

```text
E:/clones
```

## One YAML Rule
Before any agent edits YAML, it must:

1. identify the canonical file path and machine/context;
2. preserve comments and ordering when possible;
3. validate YAML syntax after editing;
4. run the relevant service/config check if known;
5. commit or record the diff;
6. create a tool checkin if validation fails, auth/path is missing, or the rule is unclear.

## Current Unknowns
- service reload/test command;
- remote push target for `E:/clones/docs/integribilt-stack`.

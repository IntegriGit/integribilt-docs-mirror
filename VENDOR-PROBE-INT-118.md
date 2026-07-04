# Vendor llms.txt Endpoint Probe Results

**Issue:** INT-118 (Lane 2: llms.txt discovery)  
**Child probe issue:** INT-121 (Part B: vendor endpoint availability)  
**Date:** 2026-07-04  
**Probe scope:** 11 vendors (n8n, Neo4j, Redis, Docker, Tailscale, Bitwarden, NetBox, Zabbix, Supabase, OpenAI, Google Cloud)

## Summary

- **6 vendors with llms.txt endpoints** (HTTP 200)
- **5 vendors without endpoints** (HTTP 404 or 403)

## Results Table

| Vendor | Endpoint Available | HTTP Status | URL |
|--------|-------------------|-------------|-----|
| n8n | ✓ Yes | 200 | https://n8n.io/llms.txt |
| Neo4j | ✓ Yes | 200 | https://neo4j.com/llms.txt |
| Redis | ✓ Yes | 200 | https://redis.io/llms.txt |
| Bitwarden | ✓ Yes | 200 | https://bitwarden.com/llms.txt |
| Zabbix | ✓ Yes | 200 | https://zabbix.com/llms.txt |
| Supabase | ✓ Yes | 200 | https://supabase.com/llms.txt |
| Docker | ✗ No | 404 | https://docker.com/llms.txt |
| Tailscale | ✗ No | 404 | https://tailscale.com/llms.txt |
| NetBox | ✗ No | 404 | https://netbox.dev/llms.txt |
| OpenAI | ✗ No | 403 | https://openai.com/llms.txt |
| Google Cloud | ✗ No | 404 | https://cloud.google.com/llms.txt |

## Endpoints with llms.txt

Vendors available for Lane 2 integration:

- https://n8n.io/llms.txt
- https://neo4j.com/llms.txt
- https://redis.io/llms.txt
- https://bitwarden.com/llms.txt
- https://zabbix.com/llms.txt
- https://supabase.com/llms.txt

## Endpoints without llms.txt

Vendors requiring Lane 3 (doc-to-MD converter) or other ingestion strategy:

- Docker (404)
- Tailscale (404)
- NetBox (404)
- OpenAI (403 Forbidden)
- Google Cloud (404)

## Next Steps

Per INT-118 Lane 2 scope:

1. ✓ Mirror Antigravity llms.txt (89 URLs) → `antigravity/llms.txt`
2. ✓ Mirror Claude Platform llms.txt (1880 URLs) → `claude-platform/llms.txt`
3. ✓ Probe 11 vendors for /llms.txt availability (results above)
4. → Add Lane 3 sources to `sources.yaml` for the 5 vendors without endpoints
5. → Implement doc-to-MD converter for Lane 3 sources (INT-118 related task)

Probe verified 2026-07-04 using curl with HTTP status codes and redirect following (-L flag, timeout 5s).

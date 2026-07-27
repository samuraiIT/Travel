# Connectors and tools audit

Checked on 2026-07-27.

| Capability | Result | Operational decision |
|---|---|---|
| GitHub | `samuraiIT/Travel`, `master`, upstream `c806f264…` reached | Local project connected to `origin`; no commit or push made |
| Google Drive | No accessible result for China/Travel searches | Nothing imported; local `China/` remains the source corpus |
| Supabase | Connected account exposes no projects | RLS schema prepared locally; no paid cloud resource created |
| Hugging Face | No relevant Travel/China planning Space returned | No model/Space dependency added |
| Perplexity Space | Cloudflare human verification blocks automated export | Nothing claimed as imported; owner can provide an export later |
| Context7 | Official Supabase documentation queried through MCP | RLS owner policies use `auth.uid()` in `USING`/`WITH CHECK` |
| Playwright | Official pages are the preferred rendered-page verifier | Use isolated Chromium; no CAPTCHA bypass |
| Hermes Agent | Official repository and Context7 docs confirm profiles, Telegram gateway, skills and MCP | Dedicated `travel-bot` profile; no custom aiogram consumer |
| Lightpanda | Local MCP endpoint `http://127.0.0.1:9223/mcp` is available | Default DOM/JavaScript browser before Playwright |

## Optional China-native MCPs

These were audited but intentionally not activated without credentials or a live
sales-window need:

- `baidu-maps/mcp` — MIT, China POI/transit/driving/walking/cycling; requires a
  Baidu API key stored only in the environment.
- `Joooook/12306-mcp` — MIT, pin `0961414312ed7a8f6d6b8e4e7a5f28e9799b4bf3`;
  read-only helper only, always verify the result on official 12306.

Do not run either as an unauthenticated public HTTP service. The itinerary does
not need them before the applicable train sales windows.

## Production MCP allowlist

The Telegram profile enables only `context7`, `lightpanda`, and `playwright`.
Unrelated trading, GitLab, PostgreSQL, Qdrant, media, and generic scraping MCPs
are excluded to reduce prompt-injection, credential, and egress surface.

Firecrawl search returned an authentication error during the 2026-07-27
research pass, so no result from that provider is represented as verified.
Official Hermes documentation/GitHub and Context7 were used instead.

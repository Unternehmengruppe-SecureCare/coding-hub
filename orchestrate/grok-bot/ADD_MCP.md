# MCP an den Grok Bot hängen

Grok Bot läuft in der Cloud. `localhost` und `claude mcp serve` funktionieren dort nicht. Eine öffentliche HTTPS-URL reicht — der laufende Tunnel (`HUB_PUBLIC_URL` / `.data/hub-public-url`) zählt. Vercel/Publish ist nicht Voraussetzung.

1. HTTPS-URL des Hubs: `https://administrators-revised-finance-interracial.trycloudflare.com` (Tunnel oder Publish). `HUB_PUBLIC_URL` nur setzen, wenn sie noch fehlt.
2. Pack optional: `npm run install-grok-bot` oder `GET /api/grok-bot`. Live-Dateien: `/api/grok-bot/files/BOT.md`.
3. Grok Chat (nicht der Bot): [grok.com/connectors](https://grok.com/connectors) → New Connector → Custom → Server URL `https://administrators-revised-finance-interracial.trycloudflare.com/mcp`, Name `coding-hub`. OAuth 2.1 kommt vom Hub (`/.well-known/oauth-authorization-server` und `/.well-known/openid-configuration`, DCR `/register`, PKCE S256, `resource` = `https://administrators-revised-finance-interracial.trycloudflare.com/mcp`) — keine extra App, kein Secret. Wenn Grok ein Formular zeigt: Client ID beliebig, Secret leer, Authorize `/authorize`, Token `/token`, Auth Method none (PKCE). MCP bleibt ohne Pflicht-Bearer erreichbar. Streamable HTTP: POST JSON-RPC antwortet JSON (auch wenn Accept nur `text/event-stream` ist). GET mit Accept `text/event-stream` über den Tunnel ist ein kurzes SSE-Greeting mit Content-Length (kein Open-Stream — Cloudflare-Quick-Tunnels verwerfen offene SSE-Bodies). RPC bleibt POST. `notifications/initialized` antwortet mit `202`.

4. Im Grok Bot chatte, oder in der Grok CLI:

```
Add this MCP server: https://administrators-revised-finance-interracial.trycloudflare.com/mcp
Name: coding-hub
Streamable HTTP. OAuth 2.1 macht der Hub (PKCE, keine extra App).
Danach coding-hub://handoff lesen und run_outer_loop_tick. GitHub ist verbunden. Kein Anwendungscode.
```

```
grok plugin marketplace add Unternehmengruppe-SecureCare/coding-hub
grok plugin install Unternehmengruppe-SecureCare/coding-hub --trust
grok plugin enable coding-hub
grok mcp add --transport http coding-hub https://administrators-revised-finance-interracial.trycloudflare.com/mcp
```

`grok mcp doctor coding-hub` prüft Erreichbarkeit und OAuth. Tunnel-MCP braucht oft `startup_timeout_sec = 60` in `.grok/config.toml`.

5. Danach im Bot: „Zeig den Kopplungsstatus“ — er soll `get_coupling_status` und Resource `coding-hub://catalog` lesen. Routine „Org pollen“ ruft `run_outer_loop_tick` auf.

Ohne Bot-UI, mit API-Key:

```bash
# .env.local: XAI_API_KEY=xai-...
npm run grok-loop
```

Das ist derselbe äußere Loop: Grok ruft Remote-MCP `/mcp` auf (`run_grok_outer_loop`).

Tools, die der Bot nutzen soll:

- `get_coupling_status`
- `list_catalog`
- `discover_github_org`
- `ingest_github_issue`
- `create_cursor_issue` (Dry-Run: fehlt das Repo → `createUrl` = github.com/new; sonst `composeUrl` = issues/new mit `@cursor`)
- `get_org_defaults` / `install_org_defaults`
- `install_grok_plugin` / `bootstrap_org`
- `install_org_workflow`
- `run_outer_loop_tick` / `run_grok_outer_loop`
- `get_github_app_status`
- `get_github_device_status` (wenn `userCode` gesetzt: dem Menschen github.com/login/device geben)
- `get_cursor_credentials` (GitHub App ≠ User API Key)
- `get_local_secrets_status`
- `list_pending_jobs`
- `build_cursor_mention`
- `dispatch_to_cursor` (innerer Loop)
- `list_cursor_agents`
- `whoami_cursor`

Resources: `coding-hub://catalog`, `coding-hub://status`, `coding-hub://bot-prompt`, `coding-hub://routines`, `coding-hub://queue`, `coding-hub://grok-bot`, `coding-hub://tick`, `coding-hub://handoff`, `coding-hub://org-defaults`, `coding-hub://cursor-credentials`, `coding-hub://local-secrets`, `coding-hub://github-device`, `coding-hub://coding-hub`.

Prompts: `dispatch_issue`, `morning_briefing`, `grok_bot_setup`, `org_tick`, `create_cursor_task`.

GitHub-Org-Webhook (nach Deploy): `https://administrators-revised-finance-interracial.trycloudflare.com/api/github/webhook`, Events `issues` und `pull_request`. Label `cursor` oder `agent` ingestiert den inneren Loop.

Claude Code nicht in den Bot hängen. Der bleibt auf Cursor Desktop.

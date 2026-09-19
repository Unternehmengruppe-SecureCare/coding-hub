# Cursor Dispatch — Grok Plugin

Äußerer Loop für **Unternehmengruppe-SecureCare**. Grok plant, Cursor Cloud Agents schreiben, Claude Code bleibt lokal.

## Grok Bot anlegen

1. Auf deinem Rechner: `curl -fsSL https://switching-weed-helmet-assets.trycloudflare.com/api/couple-all.sh | bash` (Windows: `irm https://switching-weed-helmet-assets.trycloudflare.com/api/couple-all.ps1 | iex`)
2. [x.ai/bot](https://x.ai/bot) → Bot **Cursor Dispatch**, Prompt aus dem Hub `/api/grok-bot/files/BOT.md` (Live-MCP-URL, keine Platzhalter)
3. Marketplace: `grok plugin marketplace add Unternehmengruppe-SecureCare/coding-hub || grok plugin marketplace add https://github.com/Unternehmengruppe-SecureCare/coding-hub.git`
4. Plugin: `grok plugin install coding-hub --trust`
5. Einschalten: `grok plugin enable coding-hub`
6. CLI MCP: `grok mcp add --transport http coding-hub https://switching-weed-helmet-assets.trycloudflare.com/mcp`
7. Im Bot chatten:

```
Add this MCP server: https://switching-weed-helmet-assets.trycloudflare.com/mcp
Name: coding-hub
Streamable HTTP. OAuth 2.1 macht der Hub (PKCE, keine extra App).
Danach coding-hub://handoff lesen und run_outer_loop_tick. GitHub ist verbunden. Kein Anwendungscode.
```

8. Optional: [grok.com/connectors](https://grok.com/connectors) → Custom → `https://switching-weed-helmet-assets.trycloudflare.com/mcp`
9. Dieses Repo in Grok öffnen — Skill `cursor-dispatch`, Agent, `.mcp.json`

Ohne Bot-UI: `XAI_API_KEY` plus Hub `POST /api/grok-loop`.

Innerer Loop: GitHub-Issue mit `@cursor` (Cursor GitHub App). Kein User API Key.

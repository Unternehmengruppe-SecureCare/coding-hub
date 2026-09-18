# Cursor Dispatch — Grok Plugin

Äußerer Loop für **Unternehmengruppe-SecureCare**. Grok plant, Cursor Cloud Agents schreiben, Claude Code bleibt lokal.

## Grok Bot anlegen

1. [x.ai/bot](https://x.ai/bot) → Bot **Cursor Dispatch**, Prompt aus dem Hub `/api/grok-bot/files/BOT.md` (Live-MCP-URL, keine Platzhalter)
2. CLI: `grok mcp add --transport http coding-hub https://administrators-revised-finance-interracial.trycloudflare.com/mcp`
3. Im Bot chatten:

```
Add this MCP server: https://administrators-revised-finance-interracial.trycloudflare.com/mcp
Name: coding-hub
Streamable HTTP. OAuth 2.1 macht der Hub (PKCE, keine extra App).
Danach coding-hub://handoff lesen und run_outer_loop_tick. GitHub ist verbunden. Kein Anwendungscode.
```

4. Optional: [grok.com/connectors](https://grok.com/connectors) → Custom → `https://administrators-revised-finance-interracial.trycloudflare.com/mcp`
5. Dieses Repo in Grok öffnen — Skill `cursor-dispatch`, Agent, `.mcp.json`

Ohne Bot-UI: `XAI_API_KEY` plus Hub `POST /api/grok-loop`.

Innerer Loop: GitHub-Issue mit `@cursor` (Cursor GitHub App). Kein User API Key.

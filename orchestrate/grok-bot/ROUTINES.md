# Routinen für Cursor Dispatch

In Grok Bot unter Routinen / Triggers anlegen. GitHub-Events brauchen die Cursor-GitHub-App auf der Organisation.

## GitHub Device-Code

Wenn: Kopplung ohne PAT, `coding-hub` oder `.github` fehlt.

Dann: `get_github_device_status` / `coding-hub://github-device` lesen. Wenn `userCode` gesetzt, dem Org-Admin `https://github.com/login/device?user_code=…` geben. Parallel `coding-hub://coding-hub`: `createUrl` wenn das Repo fehlt, `composeUrl` wenn es da ist. Kein Code.

## Issue → Cursor

Wenn: neues Issue oder Label `cursor` / `agent` in der GitHub-Org.

Dann: Kontext sammeln, Prompt bauen, `@cursor`-Kommentar posten oder nativen Cloud Agent starten. Kein eigener Code.

## CI rot → Fix

Wenn: GitHub Check oder Workflow auf einem PR fehlgeschlagen.

Dann: Fehler zusammenfassen und `@cursor` auf dem PR mit dem Fix-Auftrag erwähnen.

## Review-Kommentar → Patch

Wenn: Review-Comment oder Changes requested.

Dann: Kommentar in einen Patch-Auftrag übersetzen und `@cursor` auf denselben PR setzen.

## Morgenlage

Wenn: Werktags 09:00.

Dann: `run_outer_loop_tick` am Coding-Hub, danach offene Jobs, Agenten und blockierte Issues der Org kurz listen. Kein Code.

## Org pollen

Wenn: „Arbeite die Queue ab“ oder neue Labels in der Org.

Dann: `run_outer_loop_tick`. Neue `cursor`/`agent`-Issues ingestieren, `@cursor` bauen, Duplikate überspringen. Kein Code. Ohne HTTPS-Webhook ist das der äußere Loop.

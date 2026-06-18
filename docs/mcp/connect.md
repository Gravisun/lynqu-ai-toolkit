# Connect the Lynqu MCP server

The Lynqu MCP server is **hosted by Lynqu**. You don't run anything — you point
your AI client at a URL and sign in with your Lynqu account over OAuth 2.1.
There is **no API key or token to copy**.

## The two servers

| Server | URL | Use it for |
| --- | --- | --- |
| **Organization (B2B)** | `https://api.lynqu.com/mcp/v2` | Cards, contacts, leads, campaigns, events, pipeline, departments, employees, follow-ups, analytics |
| **Personal** | `https://api.lynqu.com/mcp/me` | Just your own cards, card analytics, and profile |

Most teams want the **organization** server. Use the personal server if you're
an individual user without an organization, or you only want to manage your own
cards.

> **Plan requirement:** *connecting* is open to any account. *Running* a tool
> requires an AI-tier plan (Pro+AI, Business, or Corporate). If you connect on a
> free plan, the tools appear but return an upgrade prompt when called.

## Easiest path: the in-app connector

The Lynqu web app has a guided connector under **Settings → AI / MCP** that
shows the URL, your role, and which tools you can run. If you're already logged
into Lynqu on the web, start there.

## Per-client setup

### Claude (Desktop, Code, claude.ai)

1. Open Claude → **Settings → Connectors**.
2. Choose **Add custom connector**.
3. Paste `https://api.lynqu.com/mcp/v2` (or `/mcp/me`), then continue.
4. Sign in and approve access on the Lynqu page that opens.

For **Claude Code** via the CLI:

```bash
claude mcp add --transport http lynqu https://api.lynqu.com/mcp/v2
```

Claude will open the OAuth consent page on first use.

### ChatGPT

1. In ChatGPT, open **Settings → Connectors**.
2. Choose **Add custom connector**.
3. Paste `https://api.lynqu.com/mcp/v2` as the MCP server URL.
4. Sign in and approve access on the Lynqu page that opens.

### Cursor

1. Open **Cursor Settings → MCP → Add new server**.
2. Add it as an **HTTP** server using the Lynqu URL.
3. Approve access on the Lynqu page when prompted.

Or drop [`../client-configs/cursor.json`](../client-configs/cursor.json) into
`~/.cursor/mcp.json`.

### VS Code (GitHub Copilot)

1. Open the **Command Palette → MCP: Add Server → HTTP**.
2. Enter the Lynqu server URL.
3. Approve access on the Lynqu page when prompted.

Or use [`../client-configs/vscode.json`](../client-configs/vscode.json) as your
`.vscode/mcp.json`.

### Any other MCP client

1. Add a new **remote (HTTP / streamable)** MCP server.
2. Use the Lynqu URL — your client handles the OAuth sign-in.
3. Approve access on the Lynqu page when prompted.

For clients that only speak **stdio**, bridge with
[`mcp-remote`](https://www.npmjs.com/package/mcp-remote) — see
[`../client-configs/claude-desktop.json`](../client-configs/claude-desktop.json).

## After connecting

Run a read-only tool to confirm it works:

> *"Use Lynqu to tell me who I am and give me an org summary."*

That calls `who-am-i` and `get-org-summary`. If you get your profile and a
snapshot back, you're connected. If not, see
[`troubleshooting.md`](troubleshooting.md).

## Using this repo as a submodule

Teams that keep a shared workspace can vendor the toolkit:

```bash
git submodule add https://github.com/Gravisun/lynqu-ai-toolkit.git vendor/lynqu-ai-toolkit
# then symlink the skills you want into your skills directory
ln -s "$(pwd)/vendor/lynqu-ai-toolkit/skills/lynqu-lead-capture" ~/.claude/skills/lynqu-lead-capture
```

Update with `git submodule update --remote vendor/lynqu-ai-toolkit`.

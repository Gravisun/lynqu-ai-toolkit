<div align="center">

![Lynqu — Scan leads. Build networks. Share cards.](assets/header.png)

# Lynqu AI Toolkit

**Open-source Claude Skills + MCP for AI lead capture, lead research, sales follow-up, and pipeline management.**

Run your entire networking-to-revenue motion — *capture → engage → manage → measure* — straight from Claude, ChatGPT, Cursor, or any MCP-compatible AI assistant.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/Model%20Context%20Protocol-ready-7C3AED.svg)](https://modelcontextprotocol.io)
[![Lynqu](https://img.shields.io/badge/Lynqu-AI%20Lead%20Capture-7C3AED.svg)](https://lynqu.com)

<br/>

[![Book a Demo](https://img.shields.io/badge/Book%20a%20Demo-7C3AED?style=for-the-badge&logo=googlecalendar&logoColor=white)](https://lynqu.com/contact-sales)
&nbsp;
[![Visit Lynqu](https://img.shields.io/badge/Visit%20Lynqu-1f1147?style=for-the-badge&logoColor=white)](https://lynqu.com)

</div>

---

## What is this?

[Lynqu](https://lynqu.com) is the AI lead-capture, engagement & management platform — the smart card is the doorway, the platform carries the relationship from *"nice to meet you"* through to closed.

This repository is the **official, open-source toolkit for operating Lynqu through AI assistants**. It gives you two things:

1. **MCP connection** — everything you need to connect your AI assistant to the hosted **Lynqu MCP server** (OAuth 2.1, no API keys to copy): connection guides per client, the full tool catalog, an auth explainer, and troubleshooting.
2. **Agent Skills** — purpose-built [Claude Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) that turn the raw MCP tools into complete, repeatable workflows: find leads, capture them, manage the pipeline, send follow-ups, run an event blitz, and report on what's working.

> **The MCP server is hosted by Lynqu.** You don't run a server — you connect to `https://api.lynqu.com/mcp/v2` and authenticate with your Lynqu account. This repo is the *client-side* toolkit (docs + skills). No secrets, no infrastructure.

---

## Why you'd want it

| If you want to… | Use |
| --- | --- |
| Find and qualify target accounts before an event or campaign | [`lynqu-lead-research`](skills/lynqu-lead-research) |
| Turn scanned badges / business cards into clean, deduped, routed leads | [`lynqu-lead-capture`](skills/lynqu-lead-capture) |
| Keep your pipeline tidy — stage moves, assignment, bulk hygiene | [`lynqu-lead-management`](skills/lynqu-lead-management) |
| Draft and send on-brand follow-ups via your templates | [`lynqu-sales-followup`](skills/lynqu-sales-followup) |
| Run a full event: capture → tag → attach to a campaign → follow up | [`lynqu-event-blitz`](skills/lynqu-event-blitz) |
| Get a weekly pipeline / dashboard summary with insights | [`lynqu-pipeline-report`](skills/lynqu-pipeline-report) |
| Create and update digital business cards conversationally | [`lynqu-card-studio`](skills/lynqu-card-studio) |

---

## Quickstart

### 1. Connect the Lynqu MCP server

Pick your client and follow [`docs/mcp/connect.md`](docs/mcp/connect.md). The short version — paste a URL, sign in, approve:

| Server | URL | Scope |
| --- | --- | --- |
| **Organization (B2B)** | `https://api.lynqu.com/mcp/v2` | Cards, contacts, leads, campaigns, events, pipeline, team, follow-ups, analytics |
| **Personal** | `https://api.lynqu.com/mcp/me` | Your own cards, card analytics, and profile |

There's also a one-click connector setup inside the Lynqu web app under **Settings → AI / MCP**.

> **Plan note:** connecting is open to any account. *Running* tools requires an AI-tier plan (Pro+AI, Business, or Corporate).

### 2. Install the skills

These are standard [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills). Drop the ones you want into your skills directory:

```bash
# Claude Code / Claude Desktop (per-user skills)
git clone https://github.com/Gravisun/lynqu-ai-toolkit.git
cp -r lynqu-ai-toolkit/skills/lynqu-* ~/.claude/skills/
```

Or add this repo as a submodule and symlink (see [`docs/mcp/connect.md`](docs/mcp/connect.md#using-this-repo-as-a-submodule)).

### 3. Just ask

With the MCP connected and a skill installed, talk to your assistant in plain language:

> *"Research 10 SaaS companies in Berlin attending SaaStr, qualify them for Lynqu, and create leads for the best fits."*

> *"Capture these 30 badges from yesterday's booth, dedupe against existing contacts, tag them `SaaStr-2026`, and attach them to the SaaStr campaign."*

> *"Give me this week's pipeline report — what moved, what's stalling, and who needs a follow-up."*

See [`examples/prompts.md`](examples/prompts.md) for a prompt library per skill.

---

## How it fits together

```
You (plain language)
      │
      ▼
AI assistant  ──loads──►  Lynqu Agent Skill   (workflow recipe in this repo)
      │                          │
      │ calls MCP tools          │ tells the model which tools to call, in what order
      ▼                          ▼
Lynqu MCP server  ◄── OAuth 2.1 ──  https://api.lynqu.com/mcp/v2
      │
      ▼
Your Lynqu workspace  (cards · leads · campaigns · events · pipeline)
```

A **skill** is the recipe; the **MCP** is the hands. You need both connected for an end-to-end workflow — a skill on its own just describes the steps; the MCP on its own works but leaves the orchestration to you.

---

## Repository layout

```
lynqu-ai-toolkit/
├── docs/
│   ├── concepts.md              # The Lynqu model: cards, leads, campaigns, events, pipeline
│   ├── mcp/
│   │   ├── connect.md           # Connect each client (Claude · ChatGPT · Cursor · VS Code)
│   │   ├── authentication.md    # OAuth 2.1 flow + plan tiers, explained
│   │   ├── tool-catalog.md      # All 55 org tools + 8 personal tools, by category
│   │   └── troubleshooting.md   # Common connection errors and fixes
│   └── client-configs/          # Copy-paste config snippets per client
├── skills/                      # The 7 Lynqu Agent Skills
└── examples/prompts.md          # Prompt library
```

---

## Looking for…

- **A Claude skill for lead capture** → [`lynqu-lead-capture`](skills/lynqu-lead-capture)
- **AI lead research / lead generation with Claude** → [`lynqu-lead-research`](skills/lynqu-lead-research)
- **How to connect Lynqu MCP to ChatGPT / Cursor / Claude** → [`docs/mcp/connect.md`](docs/mcp/connect.md)
- **The full Lynqu MCP tool reference** → [`docs/mcp/tool-catalog.md`](docs/mcp/tool-catalog.md)
- **A sales follow-up automation skill** → [`lynqu-sales-followup`](skills/lynqu-sales-followup)
- **Event lead capture for conferences / trade shows** → [`lynqu-event-blitz`](skills/lynqu-event-blitz)

---

## Compatibility

Works with any MCP client that supports remote (streamable HTTP) servers with OAuth: **Claude** (Desktop, Code, claude.ai), **ChatGPT**, **Cursor**, **VS Code (Copilot)**, and others. The skills are written in the portable [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) format and are most fully featured in Claude.

## Contributing

Issues and PRs welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). New skills must call only documented MCP tools and ship with a prompt example.

## License

[MIT](LICENSE) © [Gravisun](https://github.com/Gravisun). "Lynqu" is a trademark of Gravisun; this license covers the code and docs in this repository, not the Lynqu brand or hosted service.

---

<div align="center">
<sub>Built for <a href="https://lynqu.com">Lynqu</a> — Networking Evolved. Get the app on <a href="https://lynqu.com">iOS & Android</a>.</sub>
</div>

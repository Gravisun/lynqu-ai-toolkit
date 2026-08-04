---
name: lynqu-card-studio
description: Create and update Lynqu digital business cards — contact info, social links, services, template, palette — and check card views, scans and shares. Requires the Lynqu MCP server connected.
---

# Lynqu Card Studio

The doorway. A great card is how the relationship starts — this skill builds and
tunes them by conversation, and tells you how they're performing.

## When to use this

- Creating a first card, or a card for a new role/event/persona.
- Editing contact info, links, services, template, or palette.
- Checking a card's engagement (views, scans, shares, saves).

## Prerequisites

- Lynqu MCP connected. Personal users: `/mcp/me`. Teams: `/mcp/v2`. See
  `../../docs/mcp/connect.md`.
- AI-tier plan for write tools.

## Workflow

1. **See what exists.** Call `list-cards` and `get-card` on the relevant card so
   you build on, not over, what's there. The server exposes a **card schema
   resource** — consult it for valid fields/shapes.
2. **Gather the essentials.** Name, title, company, the contact channels to
   show (email, phone, website), social links, and any services. For a team
   card, confirm whose card it is.
3. **Create or update.**
   - New card → `create-card` with the gathered fields.
   - Changes → `update-card` (links, services, template, palette).
   Make changes incrementally and read back the result so the user can confirm.
4. **Style it.** Set the template and color palette to match brand. Describe the
   look in words and apply via `update-card`; confirm with the user.
5. **Measure.** Use `get-card-stats` for a specific card and
   `get-dashboard-summary` for the bigger picture — views, scans, shares, saves,
   engagement — and suggest tweaks (e.g. "your scan→save rate is low; tighten
   the headline").

## Tools used

`list-cards`, `get-card`, `create-card`, `update-card`, `get-card-stats`,
`get-dashboard-summary`.

## Guardrails

- **Don't overwrite blindly.** Read the card first; apply targeted updates.
- Confirm contact details with the user — a card is public-facing; wrong info is
  worse than missing info.
- Personal vs. org scope matters: the personal server only sees the signed-in
  user's cards. For team cards, use the org server.

## Example

> "Create a digital business card for me as 'Head of Partnerships at Acme',
> include my work email and LinkedIn, add 'Partnership programs' as a service,
> use a clean dark template with a purple palette, then show me how my existing
> card has been performing this month."

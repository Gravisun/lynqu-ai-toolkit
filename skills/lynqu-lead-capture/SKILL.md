---
name: lynqu-lead-capture
description: Capture leads into Lynqu from scanned badges, business cards, event lists or a pasted list — deduped against existing contacts, tagged and routed. Requires the Lynqu MCP server connected.
---

# Lynqu Lead Capture

Get people *into* the pipeline fast and clean — the moment after "nice to meet
you." This skill is the bridge from a raw list of contacts to scored, routed,
deduped leads.

## When to use this

- Right after an event/booth — you have a stack of scanned cards or a list.
- Someone hands you a spreadsheet/paste of prospects to add.
- You want captured contacts promoted into the sales pipeline.

## Prerequisites

- Lynqu MCP connected (`/mcp/v2`). See `../../docs/mcp/connect.md`.
- AI-tier plan for write tools.

> Lynqu's mobile apps do the AI badge/card *scanning* (OCR + vision). This skill
> takes the resulting contacts/text and turns them into well-formed leads. If
> the user has a photo, point them to the Lynqu app to scan, then paste results
> here.

## Workflow

1. **Normalize the input.** Parse the pasted/listed people into structured
   fields: name, company, role, email, phone, notes. Flag anything ambiguous
   and ask rather than guess.
2. **Dedupe first.** For each person, `search-contacts` (and `list-leads` by
   name/company) before creating. If a match exists, prefer adding context to
   the existing lead (`add-lead-note`) over creating a duplicate. Show the user
   any near-matches and let them decide merge vs. new.
3. **Pick the destination.** Call `list-lead-pipelines` and
   `get-pipeline-stages` to choose the right kanban tab + entry stage. Default
   to the org's default environment's first stage unless the user says
   otherwise.
4. **Create the leads.** Call `create-lead` per person with the normalized
   fields, a `source` (e.g. "SaaStr booth"), and the chosen stage. Capture the
   "where/how we met" detail with `add-lead-note`.
5. **Tag & attribute.** If these belong to an event or campaign, use
   `attach-leads-to-campaign`. For many leads at once, batch with
   `bulk-update-leads` (≤ 100 per call) to set tags/temperature.
6. **Confirm.** Report created vs. skipped-as-duplicate counts and link the user
   to the next step (`lynqu-sales-followup` to start outreach).

## Tools used

`search-contacts`, `list-contacts`, `list-leads`, `list-lead-pipelines`,
`get-pipeline-stages`, `create-lead`, `add-lead-note`,
`attach-leads-to-campaign`, `bulk-update-leads`.

## Guardrails

- **Dedupe is non-negotiable** — always search before create.
- **Don't fabricate fields.** Missing email = blank, not a guess.
- `bulk-update-leads` caps at 100 leads per call — chunk larger lists.
- Confirm the destination environment/stage before creating in bulk.

## Example

> "Here are 25 people from yesterday's booth [paste]. Dedupe against our
> contacts, add the new ones to the Events pipeline at the 'New' stage, tag them
> `SaaStr-2026`, set temperature warm, and attach them to the SaaStr campaign."

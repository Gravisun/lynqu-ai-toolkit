---
name: lynqu-event-blitz
description: >-
  Run a complete event lead-capture workflow in Lynqu end-to-end — set up the
  event and campaign, capture booth/conference leads, tag and attribute them,
  then kick off follow-up. Use for conference, trade show, or booth lead
  capture, "set up our event in Lynqu", event ROI/attribution, or post-event
  processing. Requires the Lynqu MCP server connected (https://api.lynqu.com/mcp/v2).
---

# Lynqu Event Blitz

The all-in-one for events: before, during, and after. It chains setup → capture
→ attribution → follow-up so every badge you scan is measurable and worked.

## When to use this

- Standing up a conference/trade-show/booth in Lynqu before it starts.
- Processing a pile of captures the morning after.
- Measuring what an event actually produced.

## Prerequisites

- Lynqu MCP connected (`/mcp/v2`). See `../../docs/mcp/connect.md`.
- AI-tier plan. Event + campaign creation need **manager+**.
- Composes with `lynqu-lead-capture` and `lynqu-sales-followup`.

## Workflow

### Before the event
1. **Create the campaign** (`create-campaign`) so captures have something to
   attribute to — it auto-mints a public `/c/{token}` capture URL. Set goals
   with reference to `list-campaign-goals`.
2. **Create the event** (`create-event`, manager+) and link it with
   `link-event-to-campaign`. Use an open-ended event if dates are loose.
3. **Prep the destination.** Confirm or create the kanban tab/stage for event
   leads (`list-lead-environments`, `get-pipeline-stages`). Pick a follow-up
   template (`list-followup-templates`) or create one.

### During / after the event
4. **Capture** the scanned/listed contacts → defer to the `lynqu-lead-capture`
   workflow: normalize, `search-contacts` to dedupe, `create-lead`, tag with the
   event name, and `attach-leads-to-campaign`.
5. **Attribute & segment.** Use `bulk-update-leads` to set temperature/score by
   booth signal (demo-requested = hot, swag-only = cold).

### Wrap-up
6. **Follow up** → hand to the `lynqu-sales-followup` workflow for the hot/warm
   segment using the event template (with approval before sending).
7. **Measure.** `get-campaign` and `get-dashboard-summary` to report leads
   captured, by temperature, and against the campaign goals. When the event is
   over, `update-event-lifecycle` to archive it (audit-logged).

## Tools used

`create-campaign`, `list-campaign-goals`, `create-event`,
`link-event-to-campaign`, `update-event-lifecycle`, `list-lead-environments`,
`get-pipeline-stages`, `search-contacts`, `create-lead`,
`attach-leads-to-campaign`, `bulk-update-leads`, `list-followup-templates`,
`send-followup-now`, `get-campaign`, `get-dashboard-summary`.

## Guardrails

- Event/campaign creation is **manager+** — if the user is an employee, set up
  the leads against an existing campaign and flag that setup needs a manager.
- Campaign status and event lifecycle transitions are validated server-side
  (e.g. archived → active isn't allowed directly) — surface the rule, don't
  fight it.
- Get approval before any follow-up send.

## Example

> "We've got a booth at SaaStr next week. Set up the campaign and event in
> Lynqu, point them at the Events pipeline, and prep the 'Event recap' follow-up
> template — then I'll paste the scans each evening for you to process and
> attribute."

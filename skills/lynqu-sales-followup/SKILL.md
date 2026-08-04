---
name: lynqu-sales-followup
description: Draft and send on-brand sales follow-up emails to Lynqu leads from your follow-up templates, logged to the lead timeline. Requires the Lynqu MCP server connected.
---

# Lynqu Sales Follow-up

The money is in the follow-up. This skill turns "I met 40 people" into timely,
personalized, on-brand outreach — sent through Lynqu's compliant pipeline and
logged against each lead.

## When to use this

- Post-event follow-up to freshly captured leads.
- Re-engaging stalled deals.
- Drafting a personalized note for a specific prospect.

## Prerequisites

- Lynqu MCP connected (`/mcp/v2`). See `../../docs/mcp/connect.md`.
- AI-tier plan. `send-followup-now` is employee-level; creating new templates
  needs **manager+**.

## Workflow

1. **Find the right template.** Call `list-followup-templates`. Match the
   situation (post-event, demo recap, re-engage). If nothing fits and the user
   is manager+, offer to `create-followup-template` (HTML with mustache tokens).
2. **Select the leads.** `list-leads` (filter by tag/stage/campaign/owner) and
   `get-lead` for the personalization details — name, company, where you met,
   what they cared about (read the activity timeline).
3. **Personalize.** Draft per-lead copy that fills the template tokens. Keep it
   short, specific, and honest. **Do not reference *when* the interaction
   happened** ("yesterday", "last night") — it's stale by send time and reads as
   surveillance. Lead with relevance, not a timestamp.
4. **Review before send.** Show the user the drafts (or a representative sample
   for a batch) and get explicit approval. Sending email is outward-facing and
   not reversible.
5. **Send & log.** Call `send-followup-now` per approved lead (it goes through
   the CAN-SPAM-compliant pipeline). Record the touch with `add-lead-note`, and
   advance the stage with `update-lead-stage` if the follow-up implies progress.
6. **Suggest cadence.** Recommend the next touch timing and flag who to follow
   up with again, but don't schedule sends the user hasn't approved.

## Tools used

`list-followup-templates`, `create-followup-template`, `list-leads`,
`get-lead`, `send-followup-now`, `add-lead-note`, `update-lead-stage`.

## Guardrails

- **Always get explicit approval before sending.** Sending is irreversible and
  represents the user's brand.
- **No timestamps of the prospect's action** in the copy (stale + creepy).
- Don't invent claims about the product or the prior conversation — ground
  personalization in the lead's actual timeline.
- Respect unsubscribes/compliance — sends route through Lynqu's compliant
  pipeline; never try to bypass it.

## Example

> "Draft post-event follow-ups for everyone tagged `SaaStr-2026` in the Warm
> stage using the 'Event recap' template, personalize from each lead's notes,
> show me the drafts, and after I approve, send and log them."

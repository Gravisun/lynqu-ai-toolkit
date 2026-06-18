---
name: lynqu-lead-research
description: >-
  Find and qualify target accounts and decision-makers before an event or
  outbound campaign, then create them as leads in Lynqu. Use for AI lead
  research, lead generation, prospecting, building a target account list, or
  "who should we talk to" — especially before a conference, trade show, or
  campaign. Requires the Lynqu MCP server connected (https://api.lynqu.com/mcp/v2).
---

# Lynqu Lead Research

Turn a fuzzy "who should we go after?" into a ranked, qualified target list that
lands directly in your Lynqu pipeline.

## When to use this

- Building a target account list for an event, campaign, or territory.
- Researching companies/people you're about to meet.
- Qualifying inbound interest against your ICP before working it.

## Prerequisites

- Lynqu MCP connected (org server `/mcp/v2`). See `../../docs/mcp/connect.md`.
- An AI-tier plan to run write tools.

## Workflow

1. **Anchor on the ICP.** Ask the user (or infer from existing won leads) for:
   industry, company size, geography, role/title of the decision-maker, and the
   pain Lynqu solves for them. If they're unsure, pull signal from what's
   already working: call `list-leads` and `get-lead` on a few won leads to see
   common firmographics.
2. **Understand the current book.** Call `get-org-summary` and `list-campaigns`
   so you don't research accounts already in flight. Use `search-contacts` to
   check whether a candidate is already known.
3. **Research candidates.** Using your own web/search capabilities, assemble a
   shortlist. For each: company, why it fits the ICP, a named decision-maker,
   their role, a public profile link, and a growth/trigger signal (hiring,
   funding, expansion, attending the same event).
4. **Score the fit (1–10).** Rank on ICP match + buying signal. Show the user
   the ranked table and let them prune before anything is written.
5. **Create leads for the keepers.** For each approved candidate call
   `create-lead` with name, company, role, source ("research"), and a note
   capturing the fit rationale via `add-lead-note`. If researching for a
   specific campaign, `attach-leads-to-campaign`.
6. **Hand off.** Summarize what was created and suggest the next skill —
   usually `lynqu-sales-followup` for outreach or `lynqu-lead-management` to set
   stages and owners.

## Tools used

`get-org-summary`, `list-campaigns`, `search-contacts`, `list-leads`,
`get-lead`, `create-lead`, `add-lead-note`, `attach-leads-to-campaign`.

## Guardrails

- **Never invent contact data.** If you can't verify an email/phone, leave it
  blank and note "unverified" rather than guessing.
- **Confirm before writing.** Show the ranked list and get a go-ahead before
  calling `create-lead` — research is cheap to redo, a polluted pipeline isn't.
- Respect the role gate: `attach-leads-to-campaign` is employee-level, but
  campaign creation needs manager+.

## Example

> "Build me a list of 10 mid-market SaaS companies in the DACH region attending
> SaaStr Europe, find a VP of Sales or RevOps lead at each, score them for
> Lynqu, and create leads for anything 7+."

---
name: lynqu-pipeline-report
description: Weekly Lynqu pipeline and sales report — what moved, what's stalling, campaign and event ROI, card engagement, who needs attention. Read-only. Requires the Lynqu MCP server connected.
---

# Lynqu Pipeline Report

A read-only briefing on the state of the business: pipeline movement, what's
stalling, campaign/event ROI, and card engagement — written for a human to act
on, not a data dump.

## When to use this

- Weekly pipeline review or sales stand-up prep.
- "How are we doing?" / campaign performance check-ins.
- Spotting risk (stalled deals, unassigned leads) before it bites.

## Prerequisites

- Lynqu MCP connected (`/mcp/v2`). See `../../docs/mcp/connect.md`.
- AI-tier plan. **All tools here are read-only** — safe to run anytime.

## Workflow

1. **Scope it.** Confirm the window (this week / month) and scope (whole org, an
   environment, an owner, a campaign).
2. **Gather.** Pull the inputs:
   - `get-dashboard-summary` — top-line metrics across cards, leads, activity.
   - `list-lead-pipelines` + `get-pipeline-stages` — the shape of the funnel.
   - `list-leads` (+ `get-lead` for notable deals) — current placement,
     ownership, and timeline movement.
   - `list-campaigns` + `get-campaign` — progress against goals
     (`list-campaign-goals` for the metric definitions).
   - `list-events` + `get-event` — event contribution.
   - `get-card-stats` — card engagement if relevant.
   - `list-capture-forms` + `get-capture-form-stats` — inbound capture volume.
3. **Synthesize, don't dump.** Produce a tight report:
   - **Headline** — net pipeline movement and one sentence of "so what".
   - **By stage** — counts and notable transitions.
   - **Wins & risks** — what advanced; what's stalled (deals past a threshold in
     a stage), unassigned, or going cold.
   - **Campaign/event ROI** — actuals vs. goals.
   - **Recommended actions** — a short, prioritized list (e.g. "follow up with
     these 4 stalled Demo-stage deals" → suggest `lynqu-sales-followup`).
4. **Offer the follow-through.** Don't change anything — this skill reports.
   Point to `lynqu-lead-management` / `lynqu-sales-followup` for the fixes.

## Tools used

`get-dashboard-summary`, `list-lead-pipelines`, `get-pipeline-stages`,
`list-leads`, `get-lead`, `list-campaigns`, `get-campaign`,
`list-campaign-goals`, `list-events`, `get-event`, `get-card-stats`,
`list-capture-forms`, `get-capture-form-stats`.

## Guardrails

- **Read-only by contract** — never call a write tool from this skill. If the
  user wants changes, hand off explicitly.
- Be honest about gaps: if data is thin or a metric is unavailable, say so
  rather than inferring numbers.
- Lead with insight and recommended actions, not raw tables.

## Example

> "Give me the weekly pipeline report for the Inbound environment: what moved,
> what's stalled 14+ days, how the Q2 campaign is tracking against goal, and the
> top 5 things I should do Monday."

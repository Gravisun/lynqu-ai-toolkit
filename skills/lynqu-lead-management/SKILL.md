---
name: lynqu-lead-management
description: >-
  Keep the Lynqu sales pipeline clean and moving — advance leads through stages,
  assign owners, score and tag, run bulk hygiene, and surface stalled deals. Use
  for pipeline management, lead routing, "tidy up my pipeline", reassigning
  leads, moving deals between stages, or weekly pipeline grooming. Requires the
  Lynqu MCP server connected (https://api.lynqu.com/mcp/v2).
---

# Lynqu Lead Management

The pipeline only tells the truth if it's maintained. This skill grooms it:
right stage, right owner, right tags, no rot.

## When to use this

- Weekly pipeline grooming / hygiene.
- Reassigning leads after a territory or staffing change.
- Bulk-moving or re-tagging a set of leads.
- Finding and unsticking stalled deals.

## Prerequisites

- Lynqu MCP connected (`/mcp/v2`). See `../../docs/mcp/connect.md`.
- AI-tier plan. Note: `assign-lead` and `move-lead-environment` need
  **manager+**; stage moves and notes are employee-level.

## Workflow

1. **Map the pipeline.** Call `list-lead-environments` and
   `get-pipeline-stages` to learn the tabs and columns. Call
   `list-team-members` to get owners (and both `user_id` /
   `organization_user_id`).
2. **Pull the working set.** `list-leads` filtered to the scope the user cares
   about (an environment, an owner, a stage, a tag). `get-lead` for detail and
   the activity timeline where needed.
3. **Diagnose.** Identify: leads with no owner, leads stalled in a stage past a
   threshold (use timeline timestamps), mis-staged leads, missing tags/score.
   Present findings as a short list before changing anything.
4. **Act, with confirmation.**
   - Advance/correct stage → `update-lead-stage`.
   - Assign/reassign owner → `assign-lead` (uses `user_id`).
   - Move to a different kanban tab → `move-lead-environment`.
   - Re-tag / set temperature / score in batches → `bulk-update-leads`
     (≤ 100 per call).
   - Log context → `add-lead-note`.
5. **Report.** Summarize what changed and what needs a human decision (e.g.
   "3 deals stalled 21+ days in Demo — recommend follow-up or close-lost").

## Tools used

`list-lead-environments`, `get-pipeline-stages`, `list-team-members`,
`list-leads`, `get-lead`, `update-lead-stage`, `assign-lead`,
`move-lead-environment`, `bulk-update-leads`, `add-lead-note`.

## Guardrails

- **Confirm bulk actions** with a count and a sample before executing.
- Use the **right identifier**: `assign-lead` takes `user_id`, not
  `organization_user_id` — `list-team-members` gives you both.
- `bulk-update-leads` is capped at 100 — chunk and report progress.
- Don't auto-close deals; flag close-lost candidates for human sign-off.

## Example

> "Groom the Inbound pipeline: list anything unassigned, round-robin it across
> the active SDRs, flag deals stuck in Qualified for 14+ days, and bulk-set
> temperature to cold for anything untouched in 30 days."

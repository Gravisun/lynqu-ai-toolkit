---
name: lynqu-lead-management
description: Keep the Lynqu pipeline moving — stage moves, lead routing and owner assignment, scoring, tags, bulk hygiene and stalled deals. Requires the Lynqu MCP server connected.
---

# Lynqu Pipeline Hygiene

You keep the board honest. A pipeline lies in predictable ways: deals sit in
stages they left months ago, leads are assigned to people who no longer work
here, the same person exists three times, and every forecast built on top of it
is fiction.

You fix that — in bulk, safely, with the user's approval at each destructive
step. The output is a board a manager can trust and a rep can work top-down.

## Invocation

```
/lynqu pipeline [board | segment | "what's stalled" | "reassign Sara's leads"]
```

## Step 1: Take the pipeline's temperature

- **`get-org-summary`** — the shape of the book
- **`list-lead-pipelines`** and **`get-pipeline-stages`** — the boards and their
  columns. Everything downstream is per-board; there is no global stage list
- **`list-leads`** per board with stage and updated dates — the raw material
- **`list-lead-duplicates`** — the hygiene problem that corrupts every other number
- **`list-team-members`** — who's active, and who has left but still owns leads
- **`list-lead-views`** — the org's saved views already encode what it watches

## Step 2: Diagnose before you touch anything

Six checks, in this order. Report all of them before fixing any of them — a
manager needs the shape of the problem, not a running commentary of edits.

| Check | How to spot it | Why it matters |
|-------|----------------|----------------|
| **Stalled** | Days in current stage > 2× the board's median | The main source of forecast error |
| **Untouched** | No activity and no completed contact point since creation | Leads that were captured and abandoned |
| **Orphaned** | Assigned to a removed or suspended member | Nobody is working these, and nobody knows |
| **Duplicates** | `list-lead-duplicates` | Splits history and double-counts value |
| **Taskless** | Open lead, no open contact point | An open lead with no next step is a wish |
| **Miscategorized** | Won/lost leads still sitting in an open stage | Silently inflates the pipeline |

Quantify each: *"41 stalled (median 9 days, these are 30+), 12 orphaned from
Sara's departure, 6 duplicate pairs, 88 with no open task."*

## Step 3: Stalled deals — decide, don't just report

Every stalled lead gets one of three verdicts, and the user picks in bulk:

1. **Revive** — there's a real reason to re-engage → task + `lynqu-sales-followup`
2. **Nurture** — real fit, wrong timing → move to a nurture stage, set a dated
   task at the trigger, stop spending attention now
3. **Close as lost**, with a **reason**. This is the important one. A lost lead
   with a reason feeds `lynqu-icp`; a lead left open forever feeds nothing and
   corrupts the forecast. A closed lead also stops receiving automated
   follow-ups by itself

Nobody wants to close deals, which is exactly why the pipeline fills up. Make the
recommendation explicit and let the human decide.

## Step 4: Fix it

Show the full plan with counts, get approval, then work in this order — the
sequence matters, because merging after reassigning means doing the work twice.

1. **Duplicates first.** `merge-leads`: pick the survivor deliberately (the one
   with the richer history and the correct owner) and show what reparents:
   notes, tasks, documents, activity, campaign links. A merge cannot be undone,
   so each pair gets its own confirmation, not a batch one. The same goes for
   duplicate company records splitting an account's roll-up: `merge-companies`
   with no arguments lists the pairs, then one confirmed call per pair
2. **Records that should never have existed** (test entries, spam submissions,
   a lead created by mistake): `delete-lead`. Never for a lost deal (close
   it, so it stays in reporting) and never for a duplicate (merge it, or half the
   history goes with the deleted copy). List every lead by name and id and get a
   yes for exactly that list. The lead leaves every board and report at once,
   and only an admin can restore it
3. **Ownership.** `assign-lead` for orphans and rebalancing. Takes the **user
   id**; `list-team-members` returns both that and the `organization_user_id`
   (which is what campaign membership and department assignment want)
4. **Stage moves.** `update-lead-stage` per the verdicts. `move-lead-pipeline`
   when a lead is on the wrong board entirely: a different board is a different
   process, not a different column
5. **Scores, tags, temperature.** `bulk-update-leads`, ≤ 100 per call
6. **Tasks.** `add-lead-contact-point` on everything that stays open, and
   `update-lead-contact-point` to close out what's already done. A board where
   every open lead has a dated next step is the definition of "working"
7. **Notes.** `add-lead-note` on anything whose state you changed for a
   non-obvious reason. Six weeks later, "why is this in nurture?" needs an answer.
   A note that is wrong gets corrected with `update-lead-note`; one that should
   not be there at all (pasted into the wrong lead, personal data that does not
   belong) is removed with `delete-lead-note`, after a yes that quotes it. Both
   work on the caller's own notes, or on others' for an admin or a manager over
   the author's department. Voice notes are transcripts and cannot be reworded

## Step 5: Make it stick

A one-off cleanup decays in a month. Before you finish:

- Propose a **saved view** for the checks that mattered ("stalled > 30 days",
  "no open task") so this becomes a filter, not a memory
- Where the org has the workflow automation add-on, propose an
  `create-automation-rule` for the recurring cases — auto-task on stage entry,
  auto-flag on inactivity. Propose; don't create silently. Rules fire on
  everything afterwards
- Recommend a cadence. Weekly for a busy board, monthly for a slow one

## Output format

```markdown
# Pipeline Hygiene — {board}

{n} open leads · median {n} days in stage · {n} need attention

## Diagnosis
| Issue | Count | Worst example |
|-------|-------|---------------|
| Stalled > 30d | 41 | Acme, 94 days in Evaluation |
| Orphaned | 12 | all from Sara (removed 3 weeks ago) |

## Proposed actions
| Action | Count | Detail |
|--------|-------|--------|
| Merge duplicate pairs | 6 | survivor shown per pair |
| Reassign orphans | 12 | → round-robin across {names} |
| Close as lost | 18 | reason required per lead |
| Delete (never a real lead) | 3 | named per lead, confirmed separately |

## Applied
- {n} merged · {n} deleted · {n} reassigned · {n} stages moved · {n} tasks opened
- Held back: {n} ({reason})

## To keep it clean
Saved view proposed · cadence: weekly
```

## Rules and constraints

- **Never merge without showing what reparents**, and never merge on a fuzzy
  name match. Duplicates that are actually two people are much worse than
  duplicates.
- **Never close a lead as lost without a reason.**
- **Every delete and every merge gets its own yes**, naming the records it
  touches. `delete-lead`, `delete-lead-note`, `merge-leads` and
  `merge-companies` cannot be undone from here, so none of them rides a batch
  approval of the wider plan.
- **Delete is for records that were never real.** A lost deal is closed; a
  duplicate is merged.
- **Don't move stages to look busy.** A stage change is a claim about reality.
- **Bulk cap is 100** per `bulk-update-leads` call — chunk and report.
- **`assign-lead` takes `user_id`; campaigns and departments take
  `organization_user_id`.** Read `list-team-members`; don't guess.
- **Stages are per-pipeline.** Always resolve them against the lead's own board.
- **Show counts before acting, every time.** "This will move 41 leads" is the
  sentence that prevents the bad afternoon.
- **Never reassign another manager's team's leads** without saying so explicitly.

## Error handling

- **Merge fails** → usually a race with another edit, or one side is already
  merged. Re-read both with `get-lead` and re-confirm; never retry blind.
- **Assignee no longer a member** → `list-team-members` to confirm removal, then
  propose a reassignment target. Report orphans even if you can't fix them.
- **Stage not found** → you're on the wrong board. `get-pipeline-stages` for the
  lead's pipeline.
- **Partial bulk failure** → report exactly which ids succeeded and which failed,
  then retry only the failures.
- **Permission denied** → employees can move and update their own leads;
  reassignment, deleting leads, the duplicate queue and pipeline structure need
  `leads.manage` (managers by default), and company merges need
  `companies.manage`. Deliver the plan and name who can run it.
- **Note edit or delete refused** → it is someone else's note, and the caller is
  neither an admin nor a manager over the author's department. Name the author.
- **Board is empty or brand new** → skip the diagnosis theatre. Say the board is
  new and suggest `lynqu-lead-capture` or `lynqu-lead-research`.

## Cross-skill integration

- Duplicates found anywhere in the suite → here for the merge
- Stalled and worth reviving → `lynqu-sales-followup`
- Stalled because of an incumbent's contract → `lynqu-competitors` for the
  timing trigger, then nurture to that date
- Unscored leads → `lynqu-qualify`
- Loss reasons accumulate → `lynqu-icp` (this is where the anti-profile comes from)
- After the sweep → `lynqu-pipeline-report`, so the manager sees the clean number

## Example

> "/lynqu pipeline — Sara left last month and I think the board is a mess."

The run: reads three boards · finds 12 leads still assigned to Sara, 41 stalled
beyond 30 days (median in-stage is 9), 6 duplicate pairs from the same event
captured by two reps, and 88 open leads with no next step · proposes: merge the 6
pairs (survivor shown for each), round-robin Sara's 12 across the two reps in her
region, close 18 as lost with reasons, move 9 to nurture with dated triggers, and
open a first task on the remaining 61 · applies on approval, then proposes a
"stalled > 30d" saved view and a weekly cadence.

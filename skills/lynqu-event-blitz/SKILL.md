---
name: lynqu-event-blitz
description: Run a conference, trade show or booth end-to-end in Lynqu — set up the event and campaign, capture leads, attribute them, then start follow-up. Requires the Lynqu MCP server connected.
---

# Lynqu Event Blitz

You run an event as a complete motion: set it up before, capture cleanly during,
attribute and follow up after, and answer the only question that matters
afterwards — **did this event make money?**

Most event lead capture fails in one of two places, and both are avoidable. Setup
is skipped, so nothing is attributable and the ROI question is unanswerable
forever. Or follow-up starts a week late, by which point the conversations have
evaporated and the leads are cold. This skill exists to make both hard to get
wrong.

## Invocation

```
/lynqu event <name | "SaaStr next month" | "post-event for last week's show">
```

## Phase 1: Before the event (setup)

Skipping this is the expensive mistake. Do it even the night before.

1. **`list-events`** — does it already exist? Someone may have set it up.
2. **`create-event`** — name, dates, location. Events can be open-ended if the
   dates aren't fixed yet; that's better than not creating it.
3. **`create-campaign`** — the money side: budget, goals, members. The event holds
   the *when and where*, the campaign holds the *spend and target*. You need both
   to answer the ROI question.
4. **`link-event-to-campaign`** — the link **is** the attribution spine. Without
   it you have two records that never talk.
5. **`create-campaign-goal`** — a real target: leads captured, pipeline value,
   meetings booked. `list-metric-catalogue` shows what can be measured. A goal
   set afterwards is a story; set now it's a target.
6. **`add-campaign-member`** — who's working the booth. Takes the
   **`organization_user_id`** (not the user id) — `list-team-members` returns both.
7. **Capture route** — `list-capture-forms` and set up a capture form for the
   booth iPad or QR code. `get-capture-form-stats` later tells you which route
   actually worked.
8. **Pipeline** — decide now whether event leads go to their own board
   (`list-lead-pipelines`, `get-pipeline-stages`). Event leads mixed into
   outbound are indistinguishable within a week.
9. **Target list** — `lynqu-lead-research` against the exhibitor and speaker
   lists. Walking a floor with a ranked list of who to find beats wandering.
10. **Tickets**, if the org runs its own event and holds the ticketing add-on:
    `issue-tickets` and `list-event-tickets`. Skip cleanly on `ADDON_REQUIRED`.

## Phase 2: During the event

- Badge and card **scanning happens in the Lynqu mobile app** — it handles OCR,
  offline queueing and bulk mode. Say so rather than inventing a workflow
- The capture form covers everyone who prefers to type
- Mid-event, the one thing worth doing daily: **capture the context while it's
  fresh**. A note saying *"asked about Salesforce sync, has 40 reps"* written on
  day one is worth more than everything the badge scan produced
- `update-campaign-status` to keep the campaign live and reporting

## Phase 3: After the event (the 48 hours that decide the ROI)

Speed beats polish here. A good-enough follow-up on day two outperforms a perfect
one on day ten, and it isn't close.

1. **Capture the backlog** — hand to `lynqu-lead-capture`: parse, dedupe against
   contacts and each other (two reps scanning the same person is the norm at a
   busy booth), create.
2. **Attribute everything** — `attach-leads-to-campaign` for all of them.
   Attribution is only possible now. Nobody backfills it.
3. **Triage by what was actually said**, not by title. `bulk-update-leads`
   (≤ 100) to set temperature:
   - **Hot** — asked for pricing, a demo, or a date → task due within 24 hours
   - **Warm** — real interest, no ask → sequence within 48 hours
   - **Cold** — badge swap for the swag → nurture, low effort, no guilt
4. **Score** — `lynqu-qualify` on the warm and hot bands.
5. **Follow up** — `lynqu-outreach` (post-capture angle: you *met* them, so this
   isn't cold) or `lynqu-sales-followup` where a real conversation happened.
   Reference the booth conversation specifically, or don't bother.
6. **Book the meetings** — `propose-booking` while the event is still recent
   enough to be a reason.
7. **Close the event** — `update-event-lifecycle` when the capture work is done,
   so it stops showing as active.

## Phase 4: Did it pay?

- **`get-event-portfolio`** — the roll-up across events: leads, pipeline value,
  won value, cost. This is the answer to "should we do this show again", and it
  only works if Phase 1 was done
- **`get-campaign`** and **`list-campaign-goals`** — actual against target
- **`get-capture-form-stats`** — which capture route worked
- **`get-forecast`** — what the event actually put into the pipeline

Report honestly, including cost per lead and cost per qualified lead. An event
that produced 200 badges and 3 qualified leads had a bad show, and saying so is
more useful than a headline number. Note that the real ROI verdict lands 60–90
days out — flag that the current number is partial rather than declaring victory
on day three.

## Output format

```markdown
# Event — {name}, {dates}

**Phase:** {setup | live | post-capture | review}

## Setup
| Event | Campaign | Linked | Goal | Members | Capture route | Pipeline |

## Capture
{n} leads · {n} deduped · {n} attributed · hot {n} / warm {n} / cold {n}

## Follow-up
| Band | Count | Action | Due |
|------|-------|--------|-----|
| Hot | 9 | Personal email referencing the booth conversation | 24h |

## Return
| Metric | Actual | Target |
|--------|--------|--------|
| Leads / Qualified / Pipeline value / Cost per qualified lead | … | … |

{Partial — the real verdict is 60–90 days out.}

## Written to Lynqu
- Event {id} linked to campaign {id} · {n} leads attributed · {n} tasks opened
```

## Rules and constraints

- **Set up before, or accept you can never answer the ROI question.** Say this
  plainly if the user wants to skip it.
- **Link the event to the campaign.** That link is the attribution spine.
- **Attribute at capture time.** There is no later.
- **48 hours for the hot band.** Everything else is negotiable; this isn't.
- **Triage on what was said, not on job title.** A curious ops manager beats a
  polite VP every time.
- **`add-campaign-member` takes `organization_user_id`; `assign-lead` takes
  `user_id`.** `list-team-members` returns both.
- **Bulk cap is 100** per call.
- **Don't declare ROI at day three.** Say which part of the number is still
  unresolved.
- **Cold leads deserve a cheap path**, not silence and not a full sequence.

## Error handling

- **Event already exists** → use it. Never create a second one for the same show;
  the split kills the roll-up.
- **Campaign exists but isn't linked** → link it. This is the single most common
  broken setup, and it's why the portfolio numbers look wrong.
- **`ADDON_REQUIRED`** on ticketing or analytics → those are optional surfaces.
  Continue; the core motion needs none of them.
- **Post-event with no setup at all** → be honest: attribution for this show is
  partial at best. Create the event and campaign now, attach what you can, and
  make the setup automatic for the next one.
- **Duplicate leads across reps** → expected at a busy booth. `list-lead-duplicates`
  then `lynqu-lead-management` for the merges — before follow-up, not after, or
  someone gets two emails.
- **Campaign closed before capture finished** → `update-campaign-status` to
  reopen, then attach. Don't skip attribution to avoid the extra step.
- **Goal metric not available** → `list-metric-catalogue` and pick the nearest
  measurable one; a slightly different metric beats an unmeasured goal.

## Cross-skill integration

- Pre-event target list → `lynqu-lead-research`
- The badge backlog → `lynqu-lead-capture`
- Scoring the batch → `lynqu-qualify`
- First touch → `lynqu-outreach` (post-capture angle)
- Real conversations → `lynqu-sales-followup`
- Booth meetings that became opportunities → `lynqu-deal-desk`
- Cross-event comparison → `lynqu-pipeline-report`

## Example

> "/lynqu event — we're exhibiting at SaaStr Europe in three weeks and last time
> we came back with 300 badges and never worked out if it was worth it."

The run: creates the event and a campaign with a €18k budget, links them, sets
goals (150 captured, €400k pipeline), adds the four booth staff as campaign
members, sets up a capture form for the iPad, and routes event leads to their own
board · runs `lynqu-lead-research` against the exhibitor list to produce a ranked
"find these 20 people" sheet · schedules the post-event plan: capture within 24
hours, hot band emailed within 48 · and notes that the "was it worth it" question
will be answerable this time, from `get-event-portfolio`, because the link exists.

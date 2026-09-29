---
name: lynqu-pipeline-report
description: Weekly Lynqu pipeline and sales report — what moved, what's stalling, campaign and event ROI, card engagement, who needs attention. Read-only. Requires the Lynqu MCP server connected.
---

# Lynqu Pipeline Report

You produce the briefing a sales leader reads on Monday morning: what moved, what
didn't, what's at risk, and the three things to do about it. **This skill is
read-only.** It never writes, never sends, never moves a stage. That constraint
is what makes it safe to run on anything, and it's why it's the natural last step
after every other skill in the suite.

A report that lists numbers is a dashboard, and the user already has one. A report
that says *"the pipeline looks healthy but 60% of it is one deal that hasn't moved
in five weeks"* is worth the read.

## Invocation

```
/lynqu report [week | month | quarter | board | rep | campaign | event]
```

Defaults to the last 7 days across the whole org, scoped to what the caller's
role can see.

## Step 1: Gather

Pull broad first, then drill only where something looks wrong.

| Source | What it gives you |
|--------|-------------------|
| `get-org-summary` | The shape: counts by stage, activity, campaigns |
| `get-dashboard-summary` | Headline numbers, pre-aggregated |
| `list-leads` (by stage, updated window) | Movement and staleness — the raw material |
| `get-forecast` | Weighted pipeline by forecast category (manager+) |
| `list-campaigns` + `get-campaign` | Spend against return |
| `get-event-portfolio` | Cross-event roll-up: leads, pipeline, won, cost |
| `list-events` | What's live and what's closing |
| `get-team-performance` / `get-employee-performance` | Per-rep (add-on gated) |
| `get-card-stats` / `list-org-cards` | Card engagement — the top of the funnel |
| `list-dashboards` + `get-dashboard-data` | The org's own saved widgets (analytics add-on) |
| `list-lead-duplicates` | Data quality that's distorting every number above |
| `get-followup-performance` | Which templates, sequences, steps and reps get replies, meetings and wins |
| `list-outbox` | What actually went out: bounces, server cancellations, and the replies that came back |
| `list-handoffs` | Work AI employees handed back that nobody has picked up (only if the org has them) |

Skip cleanly on `ADDON_REQUIRED`. Analytics dashboards and team performance are
add-ons; the core report needs neither. Mention the omission once, at the end,
without turning it into an upsell.

## Step 2: Analyse — differences, not totals

A total is a fact. A difference is information.

1. **Movement.** What entered, advanced, was won, was lost. Compare with the
   previous equivalent period. "12 new leads" means nothing; "12 new, against a
   4-week average of 31" is the headline.
2. **Concentration.** How much of the pipeline is one deal, one rep, one campaign?
   This is the risk nobody puts on a dashboard, and it's usually the real story.
3. **Stalls.** Leads past 2× the median time in stage, and where they pile up. A
   specific stage that always clogs is a process problem, not a rep problem.
4. **Velocity.** Time from creation to won, and whether it's changing.
5. **Conversion by stage.** Where deals actually die. If half of Evaluation goes
   to lost, the problem started earlier, in qualification.
6. **Source quality.** Win rate by capture source and campaign. Volume flatters
   the wrong channel constantly.
7. **Coverage.** Weighted pipeline against target. Say the ratio plainly.
8. **Follow-up engagement.** `get-followup-performance` by template, then by
   sequence step (`group: step` with the sequence's `trigger_id`) to find where
   a sequence goes quiet. Reply rate is the headline; a row with fewer than 20
   delivered emails is unranked, so report its numbers without a verdict. When
   `replies_tracked` is false, replies are not being collected: say reply rates
   are unmeasured rather than reporting 0%, and lean on clicks and meetings
   booked. Open rate is empty when the org does not track opens.
9. **Hygiene.** Duplicates, orphaned leads, open leads with no next step. These
   are the caveats every other number in the report needs.

## Step 3: Turn analysis into recommendations

Every finding needs a **so what**. Three to five recommendations, ranked by
impact, each naming a specific action, a specific target, and who does it.

Bad: "Follow-up could be improved."
Good: "9 hot leads from SaaStr have had no touch in 6 days — the 48-hour window
is gone. Run `/lynqu followup` on that cohort today; expected recovery is 2–3
meetings based on the last event's rate."

Rank by revenue impact, not by how easy the fix is.

## Step 4: Say what you can't see

Every report states its own limits. This is not a disclaimer, it's the part that
makes the rest trustworthy:

- Which surfaces were unavailable (add-ons, role scope)
- Data quality problems that distort the numbers — duplicates double-count value,
  leads with no value set are invisible in the forecast
- Where the sample is too small for the percentage to mean anything. "3 of 4 = 75%
  win rate" is not a win rate
- Whether replies are tracked at all (`replies_tracked`). An untracked reply
  rate is not a zero

A leader who catches a report overstating its confidence once will discount every
report after it.

## Output format

```markdown
# Pipeline Report — {period}

**{One-sentence verdict.}**

## The number
| | This period | Previous | Δ |
|---|---|---|---|
| New leads / Advanced / Won / Lost / Pipeline value / Weighted forecast | … | … | … |

## What moved
{3–5 bullets. Named deals, real numbers.}

## What's at risk
| Risk | Evidence | Impact |
|------|----------|--------|
| Concentration | 62% of pipeline is one deal, static 5 weeks | Forecast is one conversation |

## By source
| Source | Leads | Won | Win rate | Note |

## By rep
| Rep | Open | Advanced | Won | Stalled |

## Events & campaigns
| Name | Spend | Leads | Qualified | Pipeline | Cost/qualified |

## Follow-ups
| Template or step | Delivered | Reply rate | Booked | Won | Note |

## Do this week
1. {Action} — {who} — {expected impact}

## Caveats
{Unavailable surfaces · data quality · small samples.}
```

Keep the top of the report to what fits on a phone screen. Depth goes below.

## Rules and constraints

- **Read-only. Always.** No stage moves, no sends, no tags, no "while I was in
  there". If the report surfaces work, hand it to the skill that owns it.
- **Never state a number you didn't read.** No extrapolation presented as fact.
- **Always compare to a baseline.** A number with no comparison isn't a finding.
- **Flag small samples.** Percentages on fewer than ~10 records get labelled.
- **Respect role scope.** An employee's report covers their own leads; a manager's
  covers their departments. Say which scope you used, so nobody mistakes a
  partial view for the whole company.
- **Lead with the problem**, not with the total. Leaders skim.
- **Never dress a bad period up.** "Down 40% on a 4-week average" is the sentence
  that gets acted on.

## Error handling

- **`ADDON_REQUIRED`** → note once at the end which surfaces were unavailable and
  produce the rest. Never block a report on an add-on.
- **Empty or brand-new org** → say so and stop. A report on 4 leads is noise;
  suggest `lynqu-lead-capture` or `lynqu-lead-research` instead.
- **Forecast unavailable** (manager+ gate) → report unweighted pipeline and say
  it's unweighted.
- **Duplicates found** → report the count as a caveat *before* the value numbers,
  since they inflate them, and route to `lynqu-lead-management`.
- **Inconsistent value data** (most leads have no value) → say what fraction is
  actually valued. A forecast built on 30% coverage is a guess with a decimal point.
- **Period contains a holiday or an event** → note it. A quiet week in August is
  not a trend.
- **`replies_tracked` is false** → drop reply rate from the follow-up table and
  say why in one line. Never present it as 0%.
- **Scope narrower than asked** → `get-followup-performance` and `list-outbox`
  default to the caller's own sends; `team` and `all` need manager or admin.
  State which scope the numbers cover.

## Cross-skill integration

- Stalls and hygiene → `lynqu-lead-management`
- Untouched hot leads → `lynqu-sales-followup`
- Loss patterns by segment → `lynqu-icp`
- Event ROI worth digging into → `lynqu-event-blitz`
- Deals with no value set, blocking the forecast → `lynqu-deal-desk`
- A template or sequence step that gets no replies → `lynqu-sales-followup` or
  `lynqu-outreach` to rewrite it. A rep's personal version running beside the
  team template is the comparison: both show up in `get-followup-performance`
- Run this **after** any write-heavy skill to confirm the writes landed as intended

## Example

> "/lynqu report"

The run: pulls the org summary, forecast, campaigns, events and per-rep numbers ·
headline is that pipeline value is up 12% · then finds that 62% of it is one
static deal, that 9 hot SaaStr leads have gone 6 days untouched, that the Events
campaign produces a 41% win rate against outbound's 9% while receiving a fifth of
the spend, and that 6 duplicate pairs are double-counting €80k · verdict: *"The
pipeline is up on paper and down in reality — one deal is carrying it, and the
channel that actually converts is the one you're underfunding."* Three ranked
actions, each handed to the skill that owns it. Nothing written.

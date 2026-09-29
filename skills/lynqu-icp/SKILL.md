---
name: lynqu-icp
description: Build an Ideal Customer Profile from your own won and lost leads in Lynqu, then encode it as lead scoring rules so every future lead is scored automatically. Requires the Lynqu MCP server connected.
---

# Lynqu ICP Builder

You build an Ideal Customer Profile from **evidence the org already owns** — its
won deals, its losses, its cycle times — and then encode it where it does work:
Lynqu's lead scoring rules. A slide-deck ICP is an opinion. A scoring rule is an
opinion that grades every lead that arrives at 3am.

Most ICP exercises are a workshop full of guesses. This one starts with the
pipeline.

## Invocation

```
/lynqu icp [segment | "why do we lose" | "who should we chase in EMEA"]
```

Bare invocation profiles the whole book. A segment narrows it.

## Step 1: Pull the evidence

- **`get-org-summary`** — shape of the book before you slice it
- **`list-leads`** filtered to **won** — the positive class. Aim for 20+; below
  ~10 say plainly that the sample is thin and treat the output as a hypothesis
- **`list-leads`** filtered to **lost** — the negative class, and the half every
  ICP exercise skips. What you *don't* want is a sharper signal than what you do
- **`get-lead`** on a sample of each — notes and activity carry the reasons the
  columns don't
- **`list-companies`** — firmographics behind the leads
- **`get-team-performance`** / **`get-employee-performance`** — who wins which
  kind of deal (add-on gated; skip cleanly if `ADDON_REQUIRED`)
- **`get-forecast`** and **`get-dashboard-summary`** — value and cycle context

Say your sample sizes out loud. "Built from 34 wins and 51 losses over 14
months" is a credibility statement; an ICP with no denominator is astrology.

## Step 2: Find the pattern

Compare won against lost on each axis. The interesting number is always the
*difference*, never the raw count — 60% of your wins being SMB means nothing if
80% of your losses are too.

| Axis | What to compute | The tell |
|------|-----------------|----------|
| Industry | Win rate per industry, not volume | One vertical wins at 3× the rest |
| Company size | Win rate and cycle length by band | Enterprise wins bigger and takes 4× longer |
| Geography | Win rate, cycle, and who owns them | A region wins on relationships, not fit |
| Capture source | Win rate by how the lead arrived | Event leads convert, cold list doesn't |
| Role of the primary contact | Win rate by title of the champion | Ops titles win; "interested" execs stall |
| Deal value | Median won vs median lost | Losses cluster in a value band |
| Cycle time | Days from create to won | A band where deals *die* rather than lose |
| Campaign / event | Win rate per campaign | One event produces half the revenue |

Then, the part the numbers won't give you: read 5–10 won notes and 5–10 lost
notes and find the **trigger** — what was true at the moment they decided to buy.
"They just hired field reps", "they run 12 events a year", "the spreadsheet
finally broke". Triggers are what makes an ICP actionable; firmographics only
tell you who to call, triggers tell you when.

## Step 3: State the profile

Three parts, all required:

1. **Fit** — the firmographics: industry, size, geography, structure
2. **Trigger** — the observable event that makes it urgent *now*
3. **Anti-profile** — who to disqualify on sight, with the evidence. This is
   worth more than the profile: it stops the reps burning weeks on the segment
   that loses 90% of the time

Include for each claim: the numbers behind it and how confident you are. An ICP
line without a denominator is an opinion.

## Step 4: Encode it as scoring rules

This is what separates this from a document.

- **`list-lead-scoring-rules`** — read what exists first. Rules the org already
  wrote encode beliefs; contradicting one is fine, doing it silently isn't
- **`create-lead-scoring-rule`** for each ICP dimension worth points, and
  **`update-lead-scoring-rule`** where an existing rule is now provably wrong
- **`delete-lead-scoring-rule`** only for rules the evidence actively refutes,
  and only with the user's explicit yes

Keep the rule set small — a dozen well-chosen rules beat forty that cancel each
other out. Weight by demonstrated win-rate lift, not by how strongly anyone feels.

Show the proposed rules as a table and get approval before writing. This changes
how every future lead is scored, which is exactly why it deserves a confirmation.

## Step 5: Make it reachable

- **`add-lead-note`** on a handful of exemplar won leads: *"Textbook ICP —
  {trigger}"*. Future reps learn the profile from real deals faster than from a
  document
- Propose a **saved view** or tag for "matches ICP" so the profile is a filter,
  not a memory
- If the org runs campaigns against segments, note which campaigns aim at the
  anti-profile — that's spend to reallocate

## Output format

```markdown
# Ideal Customer Profile — {Org}

Built from {n} won and {n} lost leads, {date range}.

## The profile
**Fit:** {industry} · {size band} · {geography} · {structure}
**Trigger:** {the observable event}
**Median won value {x} · median cycle {n} days**

## Evidence
| Axis | Won | Lost | Win rate | Read |
|------|-----|------|----------|------|
| … | 18 | 6 | 75% | 3× the book average |

## Anti-profile — disqualify on sight
| Signal | Win rate | Deals burned |

## Triggers, in their words
{Quotes from won-lead notes.}

## Scoring rules {proposed | written}
| Rule | Points | Why | Status |

## Written to Lynqu
- {n} scoring rules created, {n} updated
- {n} exemplar leads annotated
```

## Rules and constraints

- **Sample size gets stated, every time.** Under ~10 wons, label it a hypothesis
  and recommend a re-run next quarter.
- **Losses are half the analysis.** An ICP built only on wins is survivorship
  bias with a template.
- **Win *rate*, never volume.** The biggest segment is usually just the biggest
  segment.
- **Never write scoring rules without explicit approval.** They grade everything
  arriving afterwards.
- **Correlation gets labelled as correlation.** "Wins skew to companies with 200+
  employees" is a finding; "company size causes wins" is a story.
- **The anti-profile is not optional.** Ship it or the ICP won't change behaviour.

## Error handling

- **Fewer than 10 won leads** → run it anyway, label every conclusion a
  hypothesis, and lean on the qualitative notes rather than the percentages.
- **No lost leads recorded** (everything sits open forever) → say so. That is a
  pipeline hygiene problem, and it's blocking the analysis. Route to
  `lynqu-lead-management` and come back with a real negative class.
- **`ADDON_REQUIRED` on performance tools** → the ICP does not need them. Use
  leads, companies and the dashboard summary; note what you couldn't check.
- **Wildly inconsistent data** (half the leads have no company, no source) →
  report the coverage gaps first. Fix the intake, then profile. Say which fields
  are missing and how often.
- **Scoring rules denied, read or write** → they need `lead_scoring.manage`,
  which admins hold by default. Deliver the rule table so an admin can apply it
  in one pass, and name who can.

## Cross-skill integration

- ICP in hand → `lynqu-lead-research` to go find more of them
- Every subsequent `lynqu-qualify` run should score against these rules
- Anti-profile → tighten `lynqu-lead-capture` routing so the wrong-fit leads stop
  landing in the main pipeline
- Win/loss patterns by campaign → `lynqu-pipeline-report` and `lynqu-event-blitz`
  for where to spend next
- Re-run quarterly. An ICP built on last year's book quietly stops being true.

## Example

> "/lynqu icp — I think we're wasting time on enterprise."

The run: pulls 34 wons and 51 losts · finds mid-market (50–500) wins at 61% with
a 24-day cycle while enterprise wins at 12% with a 96-day cycle *and* accounts
for 40% of rep hours · finds the trigger in the won notes: *"just hired field
reps"* or *"exhibiting at 6+ events a year"* · proposes six scoring rules
(+15 events-heavy, +10 field team, −20 over 2000 employees), an anti-profile of
single-location businesses with no field motion, and annotates four exemplar
wins. Verdict: the instinct was right, and the numbers now say it out loud.

---
name: lynqu-qualify
description: Qualify a Lynqu lead with BANT and MEDDIC, score it against your real ICP, then write the verdict back — score, temperature, stage — and open a task per gap. Requires the Lynqu MCP server connected.
---

# Lynqu Lead Qualification Engine

You turn "should we work this?" into a defensible answer that the pipeline
reflects. You read what Lynqu already knows about a lead, score it on BANT and
MEDDIC, and — this is the part a document can't do — **write the verdict back**:
the score, the temperature, the stage, and a task for every gap you found.

A qualification that lives only in chat changes nothing. The rep's board is the
deliverable.

## Invocation

```
/lynqu qualify <lead id | name | company | "everything in Discovery">
```

Handles one lead or a segment. A segment is the same work in a loop plus a
ranking table at the end.

## Step 1: Read everything Lynqu already has

Do not ask the user for what the server can tell you.

- **`get-lead`** — the record: stage, score, temperature, assignee, campaign,
  custom fields, value, currency
- **`list-lead-contact-points`** — planned and completed touches. A lead with
  five overdue tasks is telling you something the fields aren't
- **`list-lead-documents`** — what's been shared, and whether it was opened
- **`list-lead-duplicates`** — if this person exists twice, the qualification is
  splitting across two records. Resolve first, in `lynqu-lead-management`
- **`get-company`** / **`list-opportunities`** — other deals on the same account.
  A second open deal changes both Authority and Timing

The lead's own activity timeline (in `get-lead`) is your best evidence source:
opens, clicks, document views, stage history. Engagement is observed behaviour,
which outranks anything a form field claims.

## Step 2: Anchor on the real ICP

Score against **this org's** actual winners, not a generic template.

- `list-lead-scoring-rules` — the org has already encoded what it values. Your
  score should not contradict its own rules without saying why
- If no rules exist, or they look stale, run `/lynqu icp` first and come back.
  Ten minutes there makes every subsequent qualification honest

## Step 3: BANT

| Dimension | What counts as evidence | Common false positive |
|-----------|------------------------|----------------------|
| **Budget** | Stated range, existing spend on an incumbent, funding, headcount growth | "They're a big company" — size is not budget for *this* |
| **Authority** | Named economic buyer, committee mapped, procurement understood | Talking to an enthusiastic user with no signing power |
| **Need** | Observable symptom, a cost they can name, a deadline | A pain *you* inferred and they've never articulated |
| **Timing** | Event date, contract renewal, compliance deadline, hiring | "Sometime this year" |

Every line gets **Confirmed / Inferred / Unknown**. Unknown is not failure — it's
the discovery agenda, and it becomes a task in Step 6.

## Step 4: MEDDIC

Run it where the deal is big enough to justify it — typically anything with a
value set, or a named committee.

**M**etrics (the number that changes) · **E**conomic buyer (named, or the gap is
your biggest risk) · **D**ecision criteria (how they'll choose) · **D**ecision
process (steps, approvals, dates) · **I**dentify pain (theirs, in their words) ·
**C**hampion (who sells internally when you're not in the room).

The two that kill deals quietly are Economic Buyer and Decision Process. If both
are Unknown, cap the qualification band at "nurture" no matter how enthusiastic
the champion sounds — this is exactly the deal that slips two quarters.

## Step 5: Score and band

| Category | Weight |
|----------|--------|
| Need evidence | 30% |
| Timing | 25% |
| Authority / access | 20% |
| Budget signal | 15% |
| Fit with ICP | 10% |

| Score | Band | Temperature | What it means |
|-------|------|-------------|---------------|
| 80–100 | Work now | hot | Committee known, pain stated, a date exists |
| 60–79 | Work this quarter | warm | Real fit, one or two material gaps |
| 40–59 | Nurture | cold | Fit is plausible, nothing is urgent |
| < 40 | Disqualify | — | Say which dimension failed and stop spending on it |

Show the user the scorecard **before** writing anything.

## Step 6: Write the verdict back

On approval:

1. **Score and temperature** — `bulk-update-leads` (≤ 100 per call) for a
   segment; for a single lead the same call with one id is fine.
2. **Stage** — `update-lead-stage` when the verdict actually moves it. Do not
   move a lead just because you looked at it; a stage change is a claim about
   reality.
3. **The reasoning** — `add-lead-note` with the full scorecard, confidence
   labels intact. Six weeks from now the rep needs to know *why* it was an 82.
4. **A task per gap** — `add-lead-contact-point` for each Unknown that matters:
   *"Confirm who signs — ask on the next call"*, due-dated. This is what turns a
   qualification into motion.
5. **Disqualifications** — move to the org's lost/disqualified stage with the
   reason in the note. Silent disqualification is how a lead gets worked twice.

## Output format

```markdown
# Qualification — {Lead} at {Company}

**Score {n}/100 · {band} · temperature {hot|warm|cold}**
{One sentence verdict.}

## BANT
| Dimension | Finding | Confidence |
|-----------|---------|------------|
| Budget / Authority / Need / Timing | … | Confirmed \| Inferred \| Unknown |

## MEDDIC
| Metric | Economic buyer | Criteria | Process | Pain | Champion |

## Evidence
Engagement: {opens, clicks, doc views} · Activity: {last touch, stage age}

## Gaps → tasks
| Gap | Question to ask | Due |

## Written to Lynqu
- Score {n}, temperature {t}
- Stage: {from} → {to} (or unchanged, and why)
- Note saved · {n} tasks opened
```

For a segment, add a ranked table — lead, score, band, single biggest gap — so
the rep can work top-down.

## Rules and constraints

- **Read Lynqu before asking the user.** Anything `get-lead` knows is not a
  question.
- **Confidence labels are mandatory.** An unlabelled inference is a lie with
  good posture.
- **Never invent budget.** Company size is not budget. Funding is not budget.
- **Don't move a stage to look productive.** Unchanged with a reason is a valid
  outcome.
- **Bulk cap is 100** per `bulk-update-leads` call — chunk and report progress.
- **Both Economic Buyer and Decision Process unknown → cap at nurture.**
- **A disqualification is a deliverable**, not a failure to qualify.

## Error handling

- **Lead not found** → `list-leads` by name and company; it may be spelled
  differently or owned by someone whose leads you can't see. Say which.
- **Duplicates found** → stop. Qualify the merged record, not one of two halves.
  Hand to `lynqu-lead-management`.
- **Empty lead — no notes, no activity** → say so. Score on fit alone, band no
  higher than nurture, and make discovery the first task.
- **Permission denied on update** → you may be able to read a lead you can't
  write. Deliver the scorecard as a note-shaped block the owner can paste, and
  name the owner.
- **Stage not found** → `get-pipeline-stages` for the lead's own pipeline; stages
  are per-pipeline, and the name you assumed may live on a different board.

## Cross-skill integration

- No scoring rules yet, or they feel wrong → `lynqu-icp`
- Authority is the gap → `lynqu-contacts`
- Incumbent is the gap → `lynqu-competitors`
- Scored 80+ → `lynqu-outreach` (cold) or `lynqu-sales-followup` (warm)
- Qualified and priced → `lynqu-deal-desk`
- Qualifying a whole stage at once → `lynqu-lead-management` for the sweep first

## Example

> "/lynqu qualify everything sitting in Discovery for more than three weeks"

The run: pulls the segment · reads each lead's activity and tasks · finds four of
eleven have had zero touches since creation and no named buyer · scores them,
bands three as nurture and one at 81 (opened the pricing doc twice last week) ·
writes scores and temperatures, moves the 81 to Evaluation, opens *"Confirm
signing authority"* on the three others, and reports the two that should be
disqualified with reasons.

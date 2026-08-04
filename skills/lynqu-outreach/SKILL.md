---
name: lynqu-outreach
description: Write and run first-touch outreach to Lynqu leads — sequences, multi-threaded to the committee — sent through your templates on your approval. Requires the Lynqu MCP server.
---

# Lynqu Cold Outreach

You write the first message to someone who has never spoken to us, and you make
the sequence real in Lynqu: the template exists, the sends are logged on the
timeline, and every step that hasn't happened yet is a dated task on the lead.

The bar for a first touch is brutal and worth stating: **would this person be
glad they opened it?** If the answer is no, no amount of sequence engineering
saves it. One specific, verifiable observation about their business beats four
paragraphs of value proposition every time.

## Invocation

```
/lynqu outreach <lead id | company | segment | "everything tagged SaaStr-2026">
```

## Step 1: Earn the right to write

Read the lead first. An email that ignores what Lynqu already knows is worse than
no email — it proves nobody looked.

- **`get-lead`** — role, company, source, score, notes, activity. **How they were
  captured is the single most important input**: someone who scanned your badge
  at a booth is not a cold contact, and treating them like one throws away the
  only warm thing you have
- The lead's **notes**, returned with `get-lead` — the rep's own words about
  the encounter, if there was one
- **`list-lead-contact-points`** — has anyone already reached out? Two reps
  cold-emailing the same person in one week is a real and embarrassing failure
- **`get-company`** and **`list-opportunities`** — an existing deal on the account
  changes this from cold outreach to multi-threading, which is a different message
- **`search-contacts`** — is this person already known to someone here?

**Stop conditions.** If the lead was contacted in the last 5 days, or is already
in an active sequence, or belongs to another rep's open deal — say so and stop.
Don't write the email.

## Step 2: Qualify before you spend

Outreach is the most expensive thing in this suite: it consumes the one thing you
can't get back, which is the prospect's willingness to hear from you again.

If the lead is unscored, run `lynqu-qualify` first. Below the "nurture" band,
recommend *not* sending and say why. A rep who sends 20 well-targeted emails beats
one who sends 200, and the second one also burns the domain.

## Step 3: Pick the angle

One angle per sequence. Not four.

| Angle | Use when | Opening move |
|-------|----------|--------------|
| **Trigger event** | Hiring, funding, expansion, a launch | Name the event, then the consequence you'd expect |
| **Shared context** | Same event, same community, mutual connection | Lead with the shared thing — it's the reason you're not a stranger |
| **Observed symptom** | Something public shows the pain | Describe what you noticed, not what you sell |
| **Referral** | A named person suggested them | Name them in the first line or it reads as a trick |
| **Post-capture** | They scanned your badge or filled a form | Reference the conversation. You have permission — use it |

The angle must be **verifiable by them**. "I saw you're hiring three field reps"
survives scrutiny. "I imagine you're struggling with lead capture" does not, and
it tells them you're guessing.

## Step 4: Build the sequence

Four to five touches over 2–3 weeks. Every touch must carry something new — a
sequence where step 3 is "just bumping this" teaches people to ignore you.

| # | Day | Job | Length |
|---|-----|-----|--------|
| 1 | 0 | The observation and one specific question | 50–90 words |
| 2 | +3 | New angle, not a bump: a proof point or a peer example | 40–70 |
| 3 | +7 | Something useful with no ask — a relevant number, a short teardown | 60–100 |
| 4 | +12 | Direct: name the ask, make it easy to say no | 30–50 |
| 5 | +20 | Close the loop. "I'll stop here — worth revisiting when {trigger}?" | 25–40 |

Rules that hold across all of them: subject lines under 50 characters and never
clickbait; one CTA per message; no attachments on a first touch; plain text, no
images; and every message must read as though a person wrote it to *this* person.

**Multi-threading.** If `lynqu-contacts` mapped a committee, the champion and the
economic buyer get **different messages** — different pain, different length,
different ask. Sending the champion's email to the VP is how you lose the
champion. Never send identical copy to two people at the same company.

## Step 5: Make it real in Lynqu

Show the full sequence, get approval, then:

1. **`list-followup-templates`** — reuse before you create. A template the org
   already tuned beats a fresh one, and it keeps the brand consistent
2. **`create-followup-template`** for a genuinely new, reusable sequence
   (manager+ in most orgs — if denied, deliver the copy and say who can save it)
3. **`send-followup-now`** for step 1 — **only after an explicit yes for this
   specific send**. Not implied by plan approval, not implied by "looks good" on
   the draft. The user says send, or nothing sends
4. **`add-lead-contact-point`** for every remaining step, dated: *"Touch 2 —
   peer example — due {date}"*. This is what makes a sequence survive the rep
   getting busy
5. **`add-lead-note`** with the angle and the reasoning, so touch 4 doesn't
   contradict touch 1
6. **`bulk-update-leads`** (≤ 100) to tag the cohort, so the response rate of this
   sequence is measurable later

Compliance — opt-outs, the 30-day cap, sender identity, physical address — is
enforced server-side by Lynqu. Do not try to route around it, and do not promise
the user a send that the platform will suppress.

## Output format

```markdown
# Outreach Sequence — {Lead} at {Company}

**Angle:** {trigger | shared context | symptom | referral | post-capture}
**Why now:** {the verifiable observation}
**Recommendation:** {send | qualify first | don't send, because …}

## Touch 1 — day 0
**Subject:** {under 50 chars}
{Body. 50–90 words.}

## Touches 2–5
| # | Day | Angle | Subject | Draft |

## Multi-thread
| Person | Role | Their version of the message |

## Written to Lynqu
- Template {name} {reused | created}
- Touch 1 sent to {n} leads (approved {timestamp})
- {n} tasks scheduled for touches 2–5
- Cohort tagged {tag}
```

## Rules and constraints

- **Never send without an explicit, specific yes.** This is the hardest rule in
  the toolkit and it has no exceptions.
- **Never fabricate a trigger.** If you can't cite where you saw it, don't
  reference it. Getting caught inventing a detail ends the relationship.
- **No false urgency**, no fake deadlines, no "circling back" on a conversation
  that never happened.
- **One CTA per message.**
- **Don't cold-email an existing customer or another rep's open deal.** Check first.
- **Respect the 5-day rule** — if anyone touched this lead recently, stop.
- **Different people get different copy.** Identical emails to two colleagues get
  forwarded to each other, and that's the end of it.
- **Bulk cap is 100** per `bulk-update-leads` call.

## Error handling

- **Lead has no email** → say so plainly; don't guess a pattern address. Offer
  LinkedIn/phone as the channel, or route to `lynqu-contacts` to find a real one.
- **Already contacted recently** → stop and report when and by whom. Suggest
  `lynqu-sales-followup` instead — this is no longer cold.
- **Send fails or is suppressed** → the recipient may have opted out or hit the
  cap. Report it as a compliance outcome, never as a bug, and never retry.
- **Template write denied** → deliver the copy in chat, formatted to paste, and
  name the manager who can save it.
- **Segment larger than 100** → chunk, confirm each chunk, and report progress.
  Never fire 400 sends off one approval.
- **Thin lead — no notes, no source, no company** → that's not a cold outreach
  problem, it's a data problem. Say so, and offer to enrich or research first.

## Cross-skill integration

- Unscored lead → `lynqu-qualify` **before** writing anything
- Committee unmapped → `lynqu-contacts` for multi-threading
- Incumbent known → `lynqu-competitors`, but never lead a first touch with a
  competitor comparison
- They replied → `lynqu-sales-followup` owns everything after the first response
- They booked a meeting → `lynqu-prep`
- Whole-cohort performance → `lynqu-pipeline-report`

## Example

> "/lynqu outreach everything tagged SaaStr-2026 that scored above 70"

The run: pulls 14 leads · finds 3 already touched by another rep this week and
excludes them · notes all 14 were badge-scanned at the booth, so the angle is
post-capture, not cold · drafts a 5-touch sequence opening *"You mentioned your
team scans badges into a spreadsheet and re-types them on the flight home —"* ·
reuses the org's existing "Event follow-up" template · asks for an explicit yes,
sends touch 1 to the 11 eligible leads, schedules touches 2–5 as dated tasks, and
tags the cohort `saastr-outreach-w1` so the response rate is measurable.

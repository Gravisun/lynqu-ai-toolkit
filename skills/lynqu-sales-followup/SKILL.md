---
name: lynqu-sales-followup
description: Draft and send on-brand sales follow-up emails to Lynqu leads from your follow-up templates, logged to the lead timeline. Requires the Lynqu MCP server connected.
---

# Lynqu Follow-Up

You handle everything **after** the first conversation: the post-meeting recap,
the deal that went quiet, the proposal nobody has opened, the long nurture until
timing arrives. This is not cold outreach — there is history, and using it is the
entire job.

Rule that governs the skill: **every follow-up must add something new**. A message
whose content is "just checking in" teaches the recipient that your emails are
safe to ignore, and that lesson is permanent.

## Invocation

```
/lynqu followup <lead | company | segment | "everyone who went quiet after a demo">
```

## Step 1: Reconstruct the relationship

Never ask the user for what Lynqu already knows.

- **`get-lead`** — stage, score, temperature, value, owner, and the activity
  timeline. **The timeline is your material**: opens, clicks, document views,
  stage history
- The lead's **notes**, returned with `get-lead` — what was actually said, in
  the rep's own words
- **`list-lead-contact-points`** — what was promised and by whom. An open task
  saying *"send the pricing breakdown"* from three weeks ago **is** the follow-up;
  don't write a nurture email around a promise you're still not keeping
- **`list-lead-documents`** — what was shared, and **whether it was opened**. A
  proposal opened five times by two different people is a completely different
  email from one never opened at all
- **`list-quotes`** / **`list-opportunities`** — a live quote changes the message
  and its urgency
- **`get-booking`** / **`list-card-bookings`** — was there a meeting? When?
  Did they show?
- **`list-outbox`** with the `lead_id`: every email that actually went to this
  person, from anyone on the team or an AI employee, with delivery status,
  opens and clicks, and any reply that came back (`source: reply`). A reply
  changes the job: they answered, so the next message is an answer, not a
  follow-up. The reply itself was forwarded to the person the email went out
  as; ask them what it said rather than guessing

## Step 2: Classify the situation

The scenario determines cadence, length and ask. Get this wrong and everything
downstream is off.

| Scenario | Signal | Cadence | The job |
|----------|--------|---------|---------|
| **Post-meeting** | Meeting in the last 48h | Same day, then +3, +7 | Recap, confirm next step, deliver what you promised |
| **Post-proposal** | Quote or document sent | +2, +5, +10 | Make it easy to say yes *or* no |
| **Went quiet** | No reply in 10+ days after engagement | +7, +14, then stop | New value, then a clean exit |
| **No-show** | Booking marked no-show | Same day, +2 | Zero guilt. One line, one link, move on |
| **Long nurture** | Right fit, wrong timing | Monthly at most | Be useful, ask for nothing |
| **Re-engage** | Dormant 60+ days | One message | New reason to talk, or close it |
| **Replied** | A reply in `list-outbox` since the last send | Answer in their thread | Respond to what they said; no template on top of it |

Two behaviours worth naming: a document opened repeatedly by **someone new** means
the deal moved to a wider audience — write to that, it's the best signal you'll
get. And zero opens on a proposal usually means the wrong person received it, not
that they said no.

## Step 3: Write it

Reference something **specific and true** from the history in the first two lines.
Not "following up on our conversation" — the actual thing: the constraint they
named, the number they quoted, the deadline they mentioned.

Then: one new piece of value, one clear next step, and a length that respects
them. Post-meeting recaps run 80–120 words; a nurture touch runs 40–60.

The exit email matters more than people think. *"I'll stop here — if the badge
backlog comes up again after the spring shows, I'm easy to find"* preserves the
relationship, and it converts surprisingly often precisely because it isn't asking.

If the promise from Step 1 is still open, the follow-up **is** keeping it. Send
the thing, then talk.

## Step 4: Send and log

Show the draft. Get an explicit yes **for this send**. Then:

1. **`list-followup-templates`**: reuse the org's tuned templates. They carry
   the branding, the sender identity and the compliance footer. The list holds
   three kinds: **team** templates, the user's own **personal** templates, and
   **proposals** an AI employee drafted. Only the first two can be sent; a
   proposal is a draft a manager adopts in the app, never something to send
2. **Pick with evidence, not taste.** **`get-followup-performance`** (group
   `template`; scope `me`, or `team` for a manager) ranks templates by reply
   rate. Three rules for reading it: a row with fewer than 20 delivered emails
   is not ranked, so don't call it a winner; when `replies_tracked` is false,
   replies are not being collected and every reply rate reads 0 without meaning
   nobody answered, so compare on clicks and meetings booked and say so; and
   open rate is empty when the org doesn't track opens
3. **`send-followup-now`**: only on explicit approval, never implied by earlier
   plan approval or by "looks good" on a draft. It sends exactly the template
   you name. It answers "queued", and the server can still cancel it at
   dispatch: the person opted out or replied recently, a meeting is already
   booked, the lead is closed, or its follow-ups are paused. Check
   **`list-outbox`** for the lead afterwards and report what actually went out
4. **`update-lead-contact-point`**: close the task this send satisfies
5. **`add-lead-contact-point`**: the next dated step, always. A sequence with no
   scheduled next touch stops after step one
6. **`add-lead-note`**: what was sent and why, so the next message doesn't
   contradict this one
7. **`update-lead-stage`** if their behaviour genuinely moved the deal. If the
   answer is a real no, move to lost **with a reason**: a clean loss is worth
   more than an open lead nobody will ever work, and a closed lead stops
   receiving automated follow-ups by itself

Compliance (opt-out, the 30-day cap, sender identity, physical address) is
enforced server-side. Don't route around it, and don't promise a send the
platform will suppress.

**Automated sequences run beside you.** When reply tracking is on, a human reply
stops the lead's scheduled automated follow-ups by itself. To stop them for
another reason (the conversation moved to a call, they asked for a pause), use
**`update-lead`** with `follow_ups_paused: true`, after a yes. It cancels the
scheduled steps and also blocks sends from this skill, so set it back to `false`
before sending that lead anything.

**The user's own voice.** If a rep wants their own wording for a team template,
**`create-followup-template`** with `scope: mine` and `overrides_template_id`
saves their version. From then on it replaces the team text on every automated
email to their own leads, unless an admin locked the team template. That
changes future mail nobody reviews one by one, so show the version and get a yes
first.

## Step 5: Segments

For "everyone who went quiet after a demo", the work is the same but the
discipline is stricter:

- Group by scenario, then by what actually happened. One template with a merge
  field is not personalization
- Cap the batch. Confirm per chunk (`bulk-update-leads` is ≤ 100 anyway)
- Show three representative drafts, not thirty — the user is approving the
  *pattern*
- Exclude anyone touched in the last 5 days, anyone on another rep's open deal,
  anyone with a live quote in negotiation, and anyone whose reply is sitting in
  `list-outbox`: they already answered

## Output format

```markdown
# Follow-Up — {Lead} at {Company}

**Scenario:** {post-meeting | post-proposal | quiet | no-show | nurture | re-engage | replied}
**History:** last touch {when, what} · doc opened {n}× by {who} · {n} open promises
**Template:** {name} ({team | yours}) · reply rate {x}% on {n} delivered | not ranked yet | replies not tracked

## Draft — send {when}
**Subject:** {under 50 chars}
{Body.}

## Then
| # | Day | Angle | Ask |

## Written to Lynqu
- Sent to {n} leads (approved {timestamp}) · {n} confirmed in the outbox · {n} cancelled by the server
- {n} promises closed · {n} next steps scheduled
- {n} stages moved · {n} closed as lost with reasons
```

## Rules and constraints

- **Never send without an explicit yes for that send.** No exceptions.
- **Never "just checking in".** If you have nothing new, the honest move is the
  exit email or a nurture task for later.
- **Keep the promise before making the ask.** Open contact points come first.
- **Never claim a conversation that didn't happen**, and never reference a detail
  you can't point to in the record.
- **No false urgency.** Invented deadlines are noticed, and remembered.
- **Respect the 5-day rule** across the whole team, not just this rep.
- **Segments get grouped drafts and chunked approval**, never one blanket send.
- **A clean loss is a good outcome.** Closing with a reason beats a lead that
  stays open for two years.
- **Never send an AI proposal.** Only a team template or the user's own
  personal one; the server refuses anything else.
- **Never call a template a winner on fewer than 20 delivered emails**, or on a
  reply rate while `replies_tracked` is false.
- **Pausing a lead's follow-ups, or saving a personal version of a team
  template, is a write.** Both need a yes, like a send.

## Error handling

- **Send suppressed or failed** → the recipient may have opted out, or hit the
  30-day cap. Report it as a compliance outcome, not a bug. Never retry, and
  never look for another route to the same inbox.
- **No email on the lead** → say so; offer phone or LinkedIn as the channel, or
  route to `lynqu-contacts` for a verified address.
- **No history at all** → this isn't a follow-up. Route to `lynqu-outreach`.
- **Contacted 2 days ago by someone else** → stop. Report who and when. Two reps
  following up the same person in one week is worse than silence.
- **Team template write denied** → team templates need `follow_ups.manage`
  (admins by default). Offer to save it as the user's personal template
  (`scope: mine`), or deliver the copy formatted to paste and name who can save
  it for the team.
- **"Your organization has turned off personal templates and sequences"** → an
  admin switched them off for the workspace. Use a team template.
- **Template not found on send** → it is someone else's personal template or
  an AI proposal. Pick a team template or one of the user's own.
- **The send shows `cancelled` in `list-outbox`** → the server's send policy
  stopped it (a recent reply, a booked meeting, a closed or paused lead, an
  opt-out). The row does not say which; name the likely cause from what Step 1
  found, and never retry through another route.
- **Lead already won** → this may be an expansion conversation, which is a
  different message and possibly a different owner. Confirm before writing.

## Cross-skill integration

- No prior conversation → `lynqu-outreach`
- Straight after a meeting → `lynqu-prep` wrote the agenda; close its task here
- They asked for pricing → `lynqu-deal-desk` before you reply, so the number in
  the email is one you can defend
- They raised an objection → `lynqu-competitors` for the honest answer
- The whole quiet cohort → `lynqu-lead-management` for the sweep, then follow up
  only the revivable ones
- Which templates and sequences get replies, team-wide → `lynqu-pipeline-report`

## Example

> "/lynqu followup everyone who went quiet after a demo in the last month"

The run: finds 14 · excludes 2 touched by another rep this week and 1 with a quote
in active negotiation · groups the rest: 6 never opened the follow-up document
(likely wrong recipient — the draft asks who else should see it), 4 opened it
repeatedly including one by a new address (the draft speaks to a wider audience
and offers a short session), 1 has an open promise from the rep 19 days old (the
draft delivers it and apologises once, briefly) · shows three representative
drafts, sends on approval, closes 1 open promise, schedules 11 next steps, and
recommends 2 for a clean exit email.

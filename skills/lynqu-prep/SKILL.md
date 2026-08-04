---
name: lynqu-prep
description: Prepare for a Lynqu booking — attendees, history, open threads, agenda and the questions that move the deal — written back to the lead. Requires the Lynqu MCP server.
---

# Lynqu Meeting Preparation

You produce the brief a rep reads in the four minutes before a call: who's on it,
what we already know, what happened last time, what has to come out of this
conversation, and the exact questions that get it. Then you write the agenda and
the next-step task back onto the lead, so the meeting leaves a trace even if the
rep forgets to log it.

The measure of a good brief is not length. It's whether the rep walks in able to
say one thing that proves they did their homework.

## Invocation

```
/lynqu prep <booking id | lead | company | "my 2pm">
```

## Step 1: Find the meeting

- **`list-card-bookings`** / **`list-booking-requests`** — what's actually on the
  calendar, with the customer's own answers to the booking questions
- **`get-booking`** — the specific appointment: time, timezone, service, notes,
  attendees, and whether it's still pending or confirmed
- **`get-meeting-brief`** — Lynqu generates a brief server-side for upcoming
  appointments. **Read it first.** It's the fastest path to context, and building
  a brief by hand while ignoring the one the platform already made is wasted
  effort. It requires an AI-tier plan; if it's unavailable, build yours from the
  reads below and don't mention the gap as a failure

If the meeting isn't in Lynqu — someone booked over email — prep from the lead
alone and offer to record it afterwards with `manage-appointment`.

## Step 2: Read the relationship, not just the record

- **`get-lead`** — stage, score, temperature, value, owner, campaign, custom
  fields, and the activity timeline. **The timeline is the brief.** Opens,
  clicks, document views and stage history tell you what they're actually
  interested in, which is often not what they said
- **`list-lead-contact-points`** — what was promised. *"I'll send the pricing
  breakdown"* three weeks ago and still open is the first thing to address, and
  the most damaging thing to walk in having forgotten
- **`list-lead-documents`** — what was shared, and crucially whether it was
  opened. A proposal sent and never opened changes the entire meeting
- The lead's **notes**, returned with `get-lead` — the last conversation in
  the rep's own words
- **`list-opportunities`** and **`list-quotes`** — open deals and any quote in
  flight. Walking into a meeting unaware of a live quote is a fast way to
  contradict your own pricing
- **`get-company`** and the committee/participants — who else is in the account
- **`list-lead-duplicates`** — if the account is split across two records, half
  the history is invisible until you check

## Step 3: Establish what this meeting is *for*

Name the meeting type, because it changes everything downstream:

| Type | The single job | Failure mode |
|------|----------------|--------------|
| **Discovery** | Learn enough to qualify or disqualify | Pitching |
| **Demo** | Show the two things *they* care about | The full product tour |
| **Technical** | Remove a specific blocker | Vague reassurance |
| **Proposal / pricing** | Get agreement on scope and number | Discovering new requirements |
| **Negotiation** | Close the gap, protect the value | Conceding unprompted |
| **Check-in / re-engage** | Re-establish why this mattered | "Just touching base" |

Then state the **one outcome** that makes this meeting a success, and the
**minimum viable outcome** if it goes badly. A rep with both walks in relaxed.

## Step 4: Build the brief

**Attendees** — for each: name, title, role in the committee, what they care
about, and one personalization anchor. Flag anyone new since last time; a new
face usually means the deal moved sideways, up, or into procurement.

**Where we are** — stage, days there, score, value, last touch. If it's been in
one stage for six weeks, that's the meeting's subtext whether anyone says it or not.

**Open threads** — every promise nobody kept, from either side. Lead with ours.

**Agenda** — 4–6 items with time boxes that add up to less than the slot. Leave
room; the useful part of a call is rarely on the agenda.

**Questions that move the deal** — 5–8, ordered, each tied to a qualification gap
from `lynqu-qualify`. Not trivia — questions whose answers change what you do
next. If Economic Buyer is Unknown, one of these questions has to fix that.

**Landmines** — the objection they raised last time, the competitor in the
account, the budget they said they don't have, the person who didn't show.

**Materials** — what to have open, and what to send afterwards.

## Step 5: Write it back

Show the brief, then:

1. **`add-lead-note`** with the agenda and the intended outcome, before the
   meeting. If the rep gets hit by a bus, the account still knows what this call
   was for
2. **`add-lead-contact-point`** for the follow-up commitment, dated the same day
   as the meeting: *"Send what was promised on the call."* Pre-committing the
   follow-up is the single highest-leverage thing this skill does — most
   post-meeting drop-off happens because nobody wrote it down within the hour
3. **`update-lead-contact-point`** to close out anything the meeting resolves
4. If the meeting isn't on the calendar yet, **`propose-booking`** offers times
   from real availability rather than trading emails
5. Rescheduling or cancelling is **`reschedule-booking`** / **`manage-appointment`**
   — never edit the lead to fake it

## Output format

```markdown
# Meeting Brief — {Company}, {date} {time} {timezone}

**Type:** {discovery | demo | technical | proposal | negotiation | re-engage}
**Success:** {the one outcome}  ·  **Minimum:** {the fallback}

## Attendees
| Name | Title | Role | Cares about | Anchor | New? |

## Where we are
Stage {x}, {n} days · score {n} · value {x} · last touch {when, what}

## Open threads
| Owed by | What | Since |

## Agenda
| Time | Item | Purpose |

## Questions that move the deal
1. … *(closes: Economic buyer — currently Unknown)*

## Landmines
{Objections, competitors, absent decision-makers.}

## Written to Lynqu
- Agenda saved as a note on lead #{id}
- Task: "Send the follow-up" due {meeting date}
```

## Rules and constraints

- **Read `get-meeting-brief` before writing your own.** Duplicating the
  platform's work is not thoroughness.
- **Never invent attendee detail.** If you can't verify a title, say "title
  unconfirmed" — being wrong about someone's job in the first minute is expensive.
- **Timezones are the classic failure.** Always state the meeting time with its
  timezone, exactly as Lynqu holds it. Do not silently convert.
- **Unkept promises go at the top.** Burying them is how a call opens badly.
- **The brief is for four minutes**, not forty. Ruthlessly cut anything that
  doesn't change what the rep says.
- **Never auto-send pre-read material.** Prepare it, let the rep decide.

## Error handling

- **No booking found** → prep from the lead; note the meeting isn't in Lynqu and
  offer to record it after.
- **`get-meeting-brief` unavailable** (plan gate, or the appointment is outside
  the generation window) → build the brief from the reads. Don't surface it as an
  error to the user.
- **Lead not linked to the booking** → match on the customer's email via
  `search-contacts` and `list-leads`, and offer to link them so the next brief is
  automatic.
- **Meeting is in under an hour** → skip the deep research. Deliver attendees,
  open threads, and three questions. A perfect brief that arrives late is worth
  nothing.
- **No history at all** — first ever contact → say so, and reframe the brief
  around discovery: what you need to *learn*, not what you know.
- **Duplicate leads on the account** → warn that half the history may be on the
  other record, and offer the merge afterwards, not five minutes before a call.

## Cross-skill integration

- Committee unknown → `lynqu-contacts` (do this *before* the meeting, not after)
- Qualification gaps become the questions → `lynqu-qualify`
- Competitor in the account → `lynqu-competitors` for the objection you'll get
- Pricing conversation on the agenda → `lynqu-deal-desk` first, so you walk in
  with numbers you can defend
- Straight after the meeting → `lynqu-sales-followup` while it's fresh
- No meeting yet → `propose-booking` via this skill, or `lynqu-outreach` to earn one

## Example

> "/lynqu prep my 2pm"

The run: finds a 14:00 Europe/Dublin demo with Acme · reads the server brief ·
spots two open contact points from three weeks ago, one being a pricing breakdown
that was never sent · sees the proposal document was opened four times, twice by
someone not on the invite · identifies that new viewer as the likely economic
buyer, unmapped · builds a demo agenda around the two features their booking
answers named, opens with *"I owe you the pricing breakdown — sending it right
after this"*, and puts *"Who else should see this before you decide?"* as question
one. Saves the agenda and pre-commits the follow-up task for 15:00 the same day.

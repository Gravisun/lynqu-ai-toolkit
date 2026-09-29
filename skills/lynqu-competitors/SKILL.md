---
name: lynqu-competitors
description: Build a battlecard for the incumbent on a Lynqu deal — switching cost, wedge, objections and honest answers — written back to the lead. Requires the Lynqu MCP server.
---

# Lynqu Competitive Intelligence

You work out what a prospect is using today, what it would cost them to move,
where our wedge actually is, and what they will say when you push. Then you write
it onto the deal so the next person to touch this account doesn't rebuild it from
memory.

Two disciplines make this useful rather than reassuring: **the incumbent is
usually not a competitor** — it's a spreadsheet, a rented scanner, or a habit —
and **every objection response has to survive contact with a customer**. An answer
that requires an exaggeration is not an answer, it's a churn ticket with a delay.

## Invocation

```
/lynqu competitors <company | lead id | competitor name>
```

## Step 1: Establish what they actually use today

Read Lynqu before researching. The answer is often already in a note.

- **`get-lead`** — notes, activity, custom fields. Reps write "they're on
  {tool}" in a note far more often than in a field
- **`list-lead-documents`** — what was shared, and what was opened, tells you
  what they were comparing (notes ride the lead record itself)
- **`list-leads`** filtered by the same incumbent — if the org has fought this
  incumbent before, those deals are the best intelligence available, especially
  the losses
- **`get-company`** — size and structure change which alternative is plausible

Then research publicly: their careers page (tools named in job specs), their
integration or partner pages, conference sponsor lists, public case studies.

**Classify the incumbent honestly:**

| Incumbent type | What it means | The real wedge |
|----------------|---------------|----------------|
| Named competitor | A funded product with a contract | Timing, gaps, total cost |
| Spreadsheet / manual | No contract, no champion for the status quo | Cost of the manual work, error rate |
| Rented hardware / per-event | Recurring cost, nothing retained between events | What happens to the data after the event |
| Nothing | Not a competitive deal at all | You are selling the *category* — do not lead with feature comparisons |

Getting this wrong is the classic error: building a feature battlecard against a
competitor when the true incumbent is "we type them into a spreadsheet on the
flight home".

## Step 2: Switching cost, honestly

What genuinely holds them where they are?

- **Contract** — when does it renew, is there an auto-renew notice window, are
  they mid-term? Timing beats features
- **Data** — what would need to move, and who has to do it
- **Process** — who built the current workflow, and whose credibility is attached
  to it (this person is your blocker; name them)
- **Integrations** — what breaks
- **Political** — who chose the incumbent, and how recently. Nobody replaces the
  tool they picked six months ago

If switching cost is genuinely high and the renewal is nine months out, the
correct output of this skill is *"nurture until {date}, here's the trigger to
watch"* — not a battlecard for a fight nobody can win this quarter.

## Step 3: The wedge

One sentence: what we do that the incumbent structurally cannot, that this
account demonstrably needs. **Structurally** matters — a feature they could ship
next quarter isn't a wedge; a different product shape is.

Support it with two or three specifics tied to *their* observed situation, not a
generic feature list. If you can't tie it to something you actually found about
this account, you have positioning, not a wedge, and you should say so.

## Step 4: Objections and honest answers

Three to five they will actually raise, in their words. For each:

| Field | Rule |
|-------|------|
| The objection | As the prospect would phrase it, not as a strawman |
| The honest answer | Truthful, specific, and survivable at renewal |
| The proof | Reference, number, or demo step. "Trust me" is not proof |
| When to concede | If it's a real gap, say so. Concede once, credibly, and move to what matters |

The concede line is the one that wins deals. A rep who admits one gap is believed
on the other four.

## Step 5: Write it to the deal

Show the battlecard, get a yes, then:

1. **`add-lead-note`** with the full card — incumbent, switching cost, wedge,
   objections and answers, sources. Tag it so it's findable
2. **`add-lead-contact-point`** for the timing trigger where one exists:
   *"Contract renews {month} — start the conversation 8 weeks before"*,
   due-dated. This is the single highest-value artifact this skill produces
3. **`update-lead-stage`** only if the finding genuinely changes the deal's
   state — e.g. discovering a nine-month lock-in moves it to nurture
4. If the intelligence is account-wide rather than deal-specific,
   **`update-company`** so it survives this particular opportunity
5. Where the org fights this incumbent repeatedly, propose a reusable
   **follow-up template** (`create-followup-template`), but propose it, don't
   create it silently. A team template needs `follow_ups.manage` (admins by
   default); a rep can save it as a personal template (`scope: mine`) that only
   their own leads receive

## Output format

```markdown
# Battlecard — {Company} vs {incumbent}

**Incumbent type:** {named competitor | spreadsheet | rented | nothing}
**Verdict:** {fight now | nurture until {date} | not a competitive deal}

## What they use today
{What, since when, who chose it, what it costs them.}

## Switching cost
| Contract | Data | Process | Integrations | Political |

## Our wedge
{One sentence, then 2–3 specifics tied to what we found here.}

## Objections
| They'll say | Honest answer | Proof | Concede? |

## Timing
{Renewal date, notice window, the trigger to watch.}

## Written to Lynqu
- Battlecard saved to lead #{id}
- Task: "{timing trigger}" due {date}
```

## Rules and constraints

- **No disparagement.** Compare on facts you can source. A rep who repeats a
  false claim about a competitor loses the room and sometimes the account.
- **Never fabricate competitor pricing, customers or roadmap.** "Not publicly
  known" is a fine answer and marks you as credible.
- **Concede real gaps.** Every product has them. Pretending otherwise is how a
  deal closes and then churns.
- **Don't build a battlecard against a competitor that isn't there.** If the
  incumbent is a spreadsheet, sell the category.
- **Timing outranks features.** A perfect wedge nine months before renewal is a
  nurture plan, and you should say that rather than manufacture urgency.
- **Everything written gets a source.** An unsourced competitive claim becomes a
  rep's confident statement three weeks later.

## Error handling

- **Incumbent unknown and not researchable** → don't guess. Make it the first
  discovery question and open a task: *"Ask what they use today and who chose
  it."* An honest unknown beats a wrong battlecard.
- **Conflicting information** (notes say one tool, careers page another) → show
  both, date them, and prefer the more recent primary source. Say it's contested.
- **No prior deals against this incumbent** → say the org has no track record
  here, and lower the confidence on the objection answers accordingly.
- **Lead not found** → this may be pre-pipeline. Deliver the battlecard as
  research and suggest `/lynqu prospect` to create the lead it should attach to.
- **Note write denied** → deliver the card in chat, formatted to paste, and name
  the lead owner who can save it.

## Cross-skill integration

- Full account context first → `lynqu-prospect`
- Whoever chose the incumbent is your blocker → `lynqu-contacts` to map them
- Objection answers feed the messaging in `lynqu-outreach` and
  `lynqu-sales-followup` — but never lead a first touch with a competitor
  comparison; earn the conversation first
- A renewal-timed nurture plan belongs in `lynqu-lead-management` as tasks
- Repeated losses to one incumbent → `lynqu-icp`, and check whether that segment
  belongs in the anti-profile

## Example

> "/lynqu competitors Acme Logistics — they told us they already have a badge
> scanning solution."

The run: reads the lead notes and finds "rents scanners from the event organizer,
per show" · classifies it as rented hardware, not a competitor · establishes there
is no contract to wait out and no internal champion for the status quo · sets the
wedge as *what happens to the data after the event* — rented scanners hand back a
CSV and nothing follows up · drafts four objections including "we already pay for
this at each show" with the honest answer that the cost isn't the scanner, it's
the two weeks of manual entry afterwards · saves the card and opens *"Ask what
happened to last show's 300 badges — how many were followed up?"* due before the
next call.

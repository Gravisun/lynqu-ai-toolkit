---
name: lynqu-contacts
description: Map the buying committee on an account — economic buyer, champion, blocker — and write it into Lynqu as contacts and participants. Requires the Lynqu MCP server.
---

# Lynqu Buying Committee Mapping

You find out **who actually decides**, and you make that visible in Lynqu. Deals
are lost to org charts far more often than to product gaps: the champion loves
it, nobody asked the person who signs, and the deal dies in a quarter-end
review nobody told you about.

The output is a mapped committee written to the account — contacts on the company
roster, participants on the lead, one designated primary — so the next person to
touch this deal inherits the map instead of rediscovering it.

## Invocation

```
/lynqu contacts <company | lead id | url>
```

## Step 1: Read what the org already knows

Someone on the team has probably met these people. Check before researching.

- **`list-contacts`** / **`search-contacts`** — the shared org address book. Match
  on email domain *and* company name; the same person appears under both
  "Acme" and "Acme Logistics Ltd"
- **`get-company`** + **`list-companies`** — is there a company record, and what
  hangs off it?
- **`get-lead`** — existing participants, notes, activity. The champion is often
  already there, unlabelled
- **`list-leads`** filtered by company — multiple leads on one account usually
  means multiple threads into the same committee

Report what already exists before adding anything. "Three of the five people you
need are already in your contacts, one is on another rep's lead" is the single
most useful sentence in this whole run.

## Step 2: Map the roles

Aim for 3–6 people. Every named person needs a role, or you have a list, not a
map.

| Role | What they control | How you spot them | If missing |
|------|-------------------|-------------------|------------|
| **Economic buyer** | The budget. Says yes when everyone else says maybe | VP/C-level over the function, or whoever owns the P&L line | The deal has no close date. Highest-priority gap |
| **Champion** | Internal selling when you're not in the room | Feels the pain personally, replies fast, shares internally | You have a contact, not a deal |
| **Technical evaluator** | Can veto on integration, security, IT policy | Ops, IT, RevOps, security | Expect a late-stage surprise |
| **User / influencer** | Day-to-day reality, and the loudest complaint | Field reps, marketers, event staff | Your pain story is secondhand |
| **Blocker** | The incumbent's owner, or whoever's process you disrupt | Signed the current tool, or owns the workaround | Find them. They exist |

For each person capture: name, exact title, seniority, reporting line if visible,
a **personalization anchor** (something they wrote, shipped or said publicly), and
where you found it.

## Step 3: Research the gaps

Only for roles nobody in the org already knows. Use public sources: the company's
team page, conference speaker lists, published posts, job postings that name the
hiring manager, press quotes.

**Never guess an email address.** Deriving `first.last@company.com` from a pattern
is fabrication with a plausible shape — it bounces, it hurts sender reputation,
and in Lynqu it creates a contact that looks verified and isn't. Leave the field
blank and mark the source as unverified. A named person with no email is
genuinely useful; a wrong email is worse than nothing.

## Step 4: Write the committee into Lynqu

Show the map, get a yes, then:

1. **Company first** — `create-company` (or `update-company`) so the contacts have
   a parent. A contact with no company is an orphan the roster can't group.
2. **Contacts** — `create-lead` is *not* the tool here. People who are part of a
   committee but aren't the deal owner belong on the company roster; only
   promote someone to their own lead when they're genuinely a separate pursuit.
3. **Participants on the lead** — attach each committee member to the deal, with
   their role. Cap is 15 per lead, which is far more than any real committee.
4. **Designate the primary.** Exactly one — the person the deal is actually
   *with*. This is the field the rest of Lynqu keys off, so an unset primary
   quietly degrades the lead detail, the roster chips and the follow-up defaults.
5. **The map as a note** — `add-lead-note` with the committee table, the reporting
   lines, the anchors and the sources. This is what makes the map survive a
   handover.
6. **Tasks for the gaps** — `add-lead-contact-point` per missing role: *"Ask the
   champion who signs off on tooling spend"*, due-dated. An unmapped economic
   buyer is the highest-priority task on any deal.

## Output format

```markdown
# Buying Committee — {Company}

**Coverage: {n}/5 roles mapped · biggest gap: {role}**

| Person | Title | Role | Anchor | Status |
|--------|-------|------|--------|--------|
| … | … | Economic buyer | "Posted about badge scanning at trade shows" | Already in contacts |
| … | … | Champion | … | New — added |
| — | — | Technical evaluator | — | **Gap** |

## Reporting lines
{What reports to whom, where visible. Say "unclear" rather than inventing it.}

## Access paths
Warm intro via {who} · shared event {name} · existing relationship {rep}

## Written to Lynqu
- {n} contacts added to {Company}, {n} matched to existing records
- {n} participants attached to lead #{id}; primary set to {name}
- Committee map saved as a note
- {n} tasks opened for unmapped roles
```

## Rules and constraints

- **Search before creating.** Duplicate contacts fragment an account's history
  across two records and nobody notices for months.
- **Never invent an email, phone number or reporting line.** Unverified is a
  valid, useful state. Fabrication is not.
- **One primary participant per lead.** Not zero, not two.
- **Roles, not just names.** A list of five people without roles is Step 1 output,
  not a committee map.
- **A gap is a finding.** "No economic buyer identified" is the most valuable line
  this skill can produce — surface it loudly, don't bury it.
- **Respect visibility.** You can only see leads and contacts your role allows. If
  a person appears on someone else's lead you can't read, say that a colleague
  has the relationship — that's the useful fact, and it isn't a permission error.

## Error handling

- **Company not found and no lead** → ask whether to create the account, or route
  to `/lynqu prospect` for the full audit first. Don't create a bare company.
- **Multiple companies match** ("Acme", "Acme Ltd", "Acme Logistics") → show them
  and let the user pick. Merging the wrong two accounts is expensive to undo.
- **Participant cap reached (15)** → you are mapping an org chart, not a
  committee. Keep the deciders, put the rest in the note.
- **Contact exists on another rep's lead** → do not reassign anything. Report the
  overlap and let the humans sort territory.
- **Permission denied on contact write** → deliver the map as a note the owner
  can act on, and name who can write it.
- **Thin public presence** → return the roles you *can't* fill as explicit gaps
  with the questions that would fill them. That's a discovery agenda, and it's a
  real deliverable.

## Cross-skill integration

- Full account picture first → `lynqu-prospect`
- Authority gap flagged during scoring → this skill, then back to `lynqu-qualify`
- Committee mapped → `lynqu-outreach` (multi-thread: champion and economic buyer
  get different messages, and sending one person's message to both is how you
  lose a champion)
- Meeting booked with the committee → `lynqu-prep`
- Committee changes mid-deal (someone leaves) → re-run and update the primary

## Example

> "/lynqu contacts Acme Logistics — we've been talking to their field ops manager
> for six weeks and nothing's moving."

The run: finds the ops manager already a contact and the lead's only participant ·
identifies a VP Field Operations (economic buyer, unmapped) and a RevOps lead who
posted about CRM consolidation (technical evaluator, unmapped) · flags that the
six weeks of no movement and the missing economic buyer are the same fact ·
writes both as participants, keeps the ops manager as champion, sets primary, and
opens *"Ask {champion} for an intro to {VP} — frame as a 15-minute validation,
not a pitch"* due in two days.

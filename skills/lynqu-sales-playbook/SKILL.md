---
name: lynqu-sales-playbook
description: Turn a written sales playbook into a live Lynqu pipeline — contacts, timed tasks, follow-up templates, the playbook attached to each lead, and stage rules that deliver the prep at the right moment.
---

# Lynqu Sales Playbook

A playbook that lives in a folder is a document. A playbook that lives in Lynqu
is a process: the contacts are on leads, the touches are dated tasks, the
meeting prep appears when the deal reaches the stage it belongs to, and the
whole thing is attached to the lead so the next rep inherits it.

You do that conversion. You read a playbook doc set — decision makers, an
outreach sequence, meeting prep, the send order — and you provision it.

The measure of a good run is that a rep who has never read the playbook still
executes it, because the next action is already on their board with a date on
it.

## Invocation

```
/lynqu playbook <folder | file | pasted plan>
```

## Step 1: Read the playbook before touching the account

Ask for the documents, or take what's pasted. A typical set:

| Document | What you extract |
| --- | --- |
| Decision makers | The people: name, title, company, role in the deal (champion / sponsor / economic buyer / blocker) |
| Outreach sequence | The touches: channel, day offset, purpose |
| Meeting prep | The briefing that belongs on a booked meeting |
| Send playbook / send order | Per-person copy and the order to work them |

Read all of them first. A sequence means nothing without the tracks it applies
to, and the send order usually overrides the generic sequence.

**Then read the account.** `get-org-summary` for the shape, `list-lead-pipelines`
and `get-pipeline-stages` for the stages you will be attaching rules to, and
`search-contacts` for every person the playbook names. Provisioning a playbook
into a pipeline you have not looked at produces a second, parallel process
nobody uses.

## Step 2: Confirm the plan before you write anything

Show the user, in one block:

- how many leads you will create, and in which pipeline
- how many contacts already exist (matched) versus will be created
- the tasks per lead, with their day offsets
- which stages get which rules
- what will be attached to each lead

Wait for a yes. This step writes to a shared workspace that other people are
working in; a playbook provisioned into the wrong pipeline is tedious to undo.

## Step 3: The people

For each named person:

- **`search-contacts`** first — match on email, then name + company. A playbook
  usually names people the org has already met.
- **`create-contact`** only for genuine misses. Never create a second contact
  for someone who is already in the roster.
- **`create-lead`** for the ones you are actually going to work, in the pipeline
  the user confirmed. If it answers `recaptured: true`, an open lead with the
  same email or phone already existed and was updated instead of duplicated:
  count it as matched, not created.
- **`manage-lead-participant`** for the rest of the buying committee. A
  corporate track with a champion, a technical sponsor and an economic buyer is
  ONE deal with three participants, not three leads. Promote the champion to
  primary — that is what points the lead at the right contact record.

Multiple people at one company who are each their own opportunity (separate
teams, separate budgets) are separate leads. People who must all say yes to the
same purchase are participants on one lead. Ask if it is genuinely ambiguous.

## Step 4: The touches

Each touch in the sequence becomes a task via **`add-lead-contact-point`**:

- `title` — what the rep actually does ("Send the 90-day pilot one-pager")
- `kind` — `call`, `demo`, `proposal`, `follow_up` or `other`
- `due_at` — the sequence's day offset, counted from today
- `description` — the angle, and the copy if the playbook supplies it
- leave `assigned_to` unset unless the playbook names an owner; an unassigned
  task already routes to whoever owns the lead

Cap is 25 per lead. A six-touch sequence fits comfortably; a sequence that
doesn't fit is a sign the playbook is describing two plays, not one.

For email touches that are genuinely templated across every lead, build the
template once with **`create-followup-template`** and reference it from the
stage rule in Step 6 rather than pasting the copy into 20 tasks.

A stage rule sends **team** templates only (`scope: team`, which needs
`follow_ups.manage`, admins by default); a personal template is refused there.
A rep who saved their own version of that team template sends their version on
their own leads, unless an admin locks the team template in the app. If the
playbook's copy has to go out word for word (legal wording, a regulated claim),
say so and ask for the lock.

## Step 5: Attach the playbook itself

**`add-lead-document`** takes a file as base64 and accepts Markdown. Attach the
send playbook — the per-person copy, the objection handling, the value props —
to each lead it covers.

It renders in the browser: the lead's Engagement tab shows the Documents panel,
and a `.md` file opens as formatted text, not a download. So the rep opens the
lead and reads the play, in the place they were already looking.

Attach the section that applies to that person where the playbook is
per-person. A rep opening Kyle's lead should find Kyle's angle, not a
45-page document they have to search.

## Step 6: Make the pipeline deliver the prep

This is the part that turns a provisioned playbook into a live one. Stage rules
need the **Workflow Automation add-on**; check with `list-automation-rules`
first — if it returns `ADDON_REQUIRED`, everything above still worked, and you
say so plainly rather than failing the whole run.

**`create-automation-rule`** with `trigger_type: stage_changed` and the
`stage_to_id` you want to hang content on:

```
Stage "Discovery booked"
  → add_note           the meeting-prep briefing for that track
  → add_contact_point  "Send agenda 24h before", due_in_days 1

Stage "Proposal sent"
  → add_contact_point  "Follow up on proposal", kind follow_up, due_in_days 3
  → send_template      the proposal follow-up email

Stage "Negotiation"
  → add_note           the objection-handling section
  → notify             target managers
```

Four things about these rules that decide whether the result is usable:

1. **They are per-stage, not per-lead.** One rule serves every lead that ever
   reaches that stage, including ones created long after this run. That is the
   whole point — you are configuring the pipeline, not decorating 20 records.
2. **`due_in_days` is relative to the fire.** A lead reaching Discovery in
   March gets the same three-day runway as one reaching it in June.
3. **Both playbook actions are idempotent.** A card dragged out of a stage and
   back does not get a second copy of the note, or a second open task with the
   same title. A task the rep already completed *will* be re-created, because
   re-entering the stage is a real re-ask.
4. **Tokens work in the body and title**: `{{lead_name}}`, `{{lead_email}}`,
   `{{lead_company}}`, `{{rule_name}}`.

Match the rule to the track. A team-leader play and a corporate-exec play
reaching the same stage need different prep, so scope the rule with
`lead_environment_id` if the tracks live on different pipelines, or with
`predicate_text` (e.g. `has_tag('track-corporate')`) if they share one.

## Step 7: Verify, then hand over

Re-read one lead end to end with **`get-lead`** and **`list-lead-documents`**.
Confirm the participants, the tasks with their dates, and the attachment are
all actually there — a playbook that half-provisioned is worse than one that
didn't, because nobody knows which half.

## Output format

```
## Provisioned

**Pipeline:** <name>
**Leads:** <n> created, <n> matched to existing contacts
**Contacts:** <n> new, <n> already in the roster

## Per lead
| Lead | Company | Participants | Tasks | Playbook attached |

## Stage rules
| Stage | Actions | Scope |

## Not done
<anything skipped, and why — add-on missing, ambiguous person, cap reached>

## First actions due
<the tasks landing in the next 7 days, so the rep knows what Monday looks like>
```

## Rules and constraints

- **Confirm before the first write.** Everything in this skill writes to a
  shared workspace.
- **Never send email as part of provisioning.** You build templates and rules;
  a human decides when the first one goes out. If the user explicitly asks to
  send, that is `lynqu-sales-followup`, and it asks again.
- **Match before you create**, for both contacts and leads. Duplicate people
  are the most common damage a bulk provisioning run does, and
  `list-lead-duplicates` cleaning up afterwards is a worse outcome than
  matching properly the first time.
- **A playbook's claims are not facts about the account.** If it says a company
  has 90,000 agents, that is the playbook's research, not something Lynqu
  verified. Put it in a note, not in a field that reads as data.
- **Cap awareness:** 25 tasks per lead, 15 participants per lead, 5 actions per
  automation rule, 50 active rules per org. Say so when you hit one rather
  than silently dropping the remainder.
- **Do not invent the sequence.** If the playbook doesn't specify day offsets,
  ask; a guessed cadence is the thing the rep will trust least.

## Error handling

| Problem | What you do |
| --- | --- |
| `ADDON_REQUIRED` on automation | Everything else still provisioned. Report which stages have no rule, and what the add-on would add. |
| Person matches two contacts | Stop and ask. Linking a company roster to the wrong person's pipeline is invisible once done. |
| Lead at the 25-task cap | Report which touches were dropped. Never silently truncate. |
| Attachment over 25 MB | Split by section — which is what you should have done anyway. |
| Stage named in the playbook doesn't exist | Ask before creating it. A playbook's stage names are usually generic; the org's are usually deliberate. |
| No pipeline confirmed | Do not guess the default. Ask. |
| `send_template` refused: "can only use team templates" | The rule names a personal template. Point it at a team template, or ask an admin to publish one. |
| Team template create denied | Deliver the copy and name an admin; the rest of the playbook still provisions. |

## Cross-skill integration

- **`lynqu-prospect`** researched the account → this provisions the plan.
- **`lynqu-contacts`** maps a buying committee in depth → use it when Step 3's
  participant structure is genuinely unclear.
- **`lynqu-outreach`** writes the sequence copy → this schedules and attaches it.
- **`lynqu-prep`** briefs one meeting → the `add_note` rules in Step 6 are the
  standing version of that, delivered by stage instead of on request.
- **`lynqu-pipeline-report`** tells you weeks later whether the playbook worked,
  including the reply rate of each templated touch.

## Example

> *"Here's our eXp Realty folder — decision makers, the outreach sequence, the
> meeting prep and the send playbook. Set it up in the Partnerships pipeline."*

Reads all four documents. Finds 13 named people across three tracks; 4 already
exist as contacts. Creates 8 leads (5 team leaders worked individually, 3
corporate execs collapsed onto one deal with the Chief Innovation Officer as
primary participant and the CTO and COO alongside). Puts the 6-touch sequence
on each team-leader lead as dated tasks, the 5-touch corporate sequence on the
corporate deal. Attaches each person's playbook section to their lead. Adds
three stage rules: meeting-prep note on "Discovery booked", proposal follow-up
task on "Proposal sent", objection-handling note plus a manager notification on
"Negotiation". Reports that the corporate track's LinkedIn touches were created
as `other` tasks rather than emails, because Lynqu doesn't send LinkedIn.

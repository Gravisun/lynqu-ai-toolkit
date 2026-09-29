---
name: lynqu-lead-capture
description: Capture leads into Lynqu from scanned badges, business cards, event lists or a pasted list — deduped against existing contacts, tagged and routed. Requires the Lynqu MCP server connected.
---

# Lynqu Lead Capture

You get people **into** the pipeline fast and clean — the moment after "nice to
meet you". A stack of scanned badges is worth nothing on day one and less than
nothing on day ten, when the context has evaporated and half of them are already
in the CRM under a different spelling.

The two things that make this skill worth running instead of pasting into a
spreadsheet: **dedupe before create**, and **every lead lands somewhere with a
next step**. A capture run that produces 200 leads and zero tasks has moved the
problem, not solved it.

## Invocation

```
/lynqu capture <pasted list | csv | "the badges from SaaStr" | contact details>
```

> Lynqu's mobile apps do the AI badge/card **scanning** (OCR + vision) — including
> offline queueing and bulk mode. This skill takes the resulting contacts and
> turns them into well-formed leads. If the user has photos, point them at the
> app to scan, then bring the results here.

## Step 1: Normalize the input

Parse into structured fields: first name, last name, company, role, email, phone,
plus the free-text "where we met" detail.

- **Never guess.** A malformed row gets flagged, not repaired by invention. Ask
  about the ambiguous ones in a single batch at the end, not one at a time
- Watch for the classic scan artefacts: OCR swapping `0`/`O`, a job title parsed
  into the company field, two people on one card, a personal Gmail where a
  corporate address belongs
- Normalize company names *for matching* (strip Ltd/Inc/GmbH, casing) but store
  what they actually gave you
- Keep the **capture context** — event, booth, date, who scanned it. This is the
  single most valuable field on an event lead and the first one people drop

Report the parse before writing: *"48 rows → 44 parsed cleanly, 3 missing email,
1 looks like two people on one card."*

## Step 2: Dedupe — non-negotiable

For every person, before creating anything:

- **`search-contacts`** — the org address book, matched on email **and** name +
  company. Email is definitive; name matching needs a human eye
- **`list-leads`** filtered by company — the same person may be in the pipeline
  under a personal address
- **`list-lead-duplicates`** — Lynqu's own duplicate detection, if these people
  may already have been captured by a colleague at the same event

Then branch per person:

| Situation | Do this |
|-----------|---------|
| Exact email match on an open lead | Don't create. `add-lead-note` with the new context — "met again at SaaStr, now evaluating" is a stronger signal than a new record |
| Match on a **closed/won** lead | Flag it. This is an expansion or a re-engagement, and it belongs to whoever owns the account |
| Contact exists, no lead | Promote: create the lead, linked to the existing contact |
| Fuzzy match only | **Ask.** Show both records side by side. Never auto-merge on a name |
| No match | Create |

Show near-matches as a group and let the user decide in one pass. Silently
merging is how two real people called J. Smith at the same company become one
corrupted record.

## Step 3: Choose the destination

- **`list-lead-pipelines`** — which board. Event leads usually belong on their own
  board, not mixed into outbound
- **`get-pipeline-stages`** — the entry stage on *that* board. Stages are
  per-pipeline; the stage name you remember may live somewhere else
- Confirm the destination **once, for the batch**, before creating anything in bulk

## Step 4: Create

Per person: **`create-lead`** with the normalized fields, a real `source` ("SaaStr
2026 booth"), and the chosen stage. Then **`add-lead-note`** with the capture
context — what was said, what they asked for, how interested they seemed. That
note is what makes the follow-up sound like a human remembers them.

The server is a backstop for Step 2, not a replacement: `create-lead` finds an
open lead with the same email or phone and updates it instead of creating a
second one. When the answer says `recaptured: true`, report that person under
**Matched**, not **Created**. A refusal saying the lead already exists means the
match is a lead the caller cannot see, and by design the server says nothing
more about it. Hold that row back as "someone here already has this person"
rather than retrying with a different spelling.

Assignment, if relevant: `list-team-members` then `assign-lead` (which takes the
**user id**, not the `organization_user_id` — the same call returns both).

## Step 5: Tag, attribute, and set the next step

- **`attach-leads-to-campaign`** — attribution is only possible at capture time.
  Nobody backfills it later, and without it the event's ROI is unanswerable
- **`bulk-update-leads`** (≤ 100 per call) for tags and temperature across the
  cohort. Chunk larger sets and report progress per chunk
- **`add-lead-contact-point`** — a dated first action for anything warm or hot.
  The single strongest predictor of whether an event lead converts is whether it
  was touched within 48 hours
- **`start-enrichment`** on the thin rows if the org has credits
  (`get-enrichment-quota` first). Show what it proposes and only
  **`confirm-enrichment`** with the user's yes — it fills empty fields, and that's
  their call

## Output format

```markdown
# Capture — {source}

Parsed {n} · created {n} · matched to existing {n} · needs a decision {n}

## Created
| Name | Company | Role | Stage | Temperature | Task |

## Matched — not duplicated
| Name | Existing lead | Owner | Action taken |

## Needs your call
| Input | Possible match | Why unclear |

## Written to Lynqu
- {n} leads in {pipeline} at {stage} · attached to {campaign} · tagged {tag}
- {n} first tasks due within 48 hours
- {n} rows held back: {reason}
```

## Rules and constraints

- **Dedupe is non-negotiable.** Always search before create, per person.
- **Never fabricate a field.** Missing email is blank, not a guess. A wrong email
  in a captured list gets emailed, bounces, and damages the sending domain.
- **Never auto-merge on a fuzzy match.** Show both, ask once.
- **Bulk cap is 100** per `bulk-update-leads` call.
- **Confirm the destination stage before bulk creation.** Moving 200 leads
  afterwards is a chore; putting them in the right column costs one question.
- **Attribution happens now or never.** Attach to the campaign or event during
  capture.
- **Every warm lead leaves with a task.** No exceptions — that's the whole point.
- **Personal email addresses are not errors.** People hand out Gmail at events;
  capture it and note it, don't "fix" it to a corporate pattern.

## Error handling

- **Malformed or unparseable rows** → hold them back, list them verbatim, ask.
  Never drop a row silently; that's someone the rep actually met.
- **Duplicate detected after creation** → `list-lead-duplicates`, then hand to
  `lynqu-lead-management` for the merge. Don't merge blind mid-capture.
- **Campaign is closed or archived** → attach fails. `list-campaigns`, confirm
  status, ask whether to reopen or attach elsewhere. Don't skip attribution
  silently.
- **Bulk cap exceeded** → chunk automatically, confirm the first chunk, report per
  chunk.
- **Enrichment quota exhausted** → skip it, say so once, continue. It's an
  accelerator, not a dependency.
- **Partial failure mid-batch** → report exactly which records landed and which
  didn't, then offer to retry only the failures. Never re-run the whole batch —
  that's how you get duplicates.
- **Employee role, bulk update denied** → create the leads, report which cohort
  operations need a manager.

## Cross-skill integration

- Photos to scan → the Lynqu mobile app first, then here
- Whole-event arc (setup → capture → attribution → follow-up) → `lynqu-event-blitz`
- Straight after capture → `lynqu-qualify` to score the batch, then
  `lynqu-outreach` on the top band only
- Duplicates surfaced → `lynqu-lead-management`
- Thin records worth deepening → `lynqu-prospect` on the best few

## Example

> "Here are 48 people from yesterday's booth [paste]. Dedupe against our contacts,
> put the new ones in the Events pipeline, tag them SaaStr-2026, attach to the
> SaaStr campaign."

The run: parses 48 rows, flags 3 with no email and 1 with two names on one card ·
finds 6 already in contacts (2 with open leads owned by another rep, noted rather
than duplicated) and 1 fuzzy match it refuses to guess on · creates 38 leads at
the Events board's New stage with the booth conversation as a note · attaches all
to the SaaStr campaign, tags `SaaStr-2026`, sets 9 warm based on what was said,
and opens a 48-hour follow-up task on each of those 9.

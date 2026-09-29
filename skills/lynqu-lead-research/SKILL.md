---
name: lynqu-lead-research
description: Build a ranked target account list from an ICP or an event, then create the keepers as leads in Lynqu with the fit rationale attached. Requires the Lynqu MCP server.
---

# Lynqu Lead Research

You turn a fuzzy "who should we go after?" into a ranked, qualified target list
that lands in the pipeline with its reasoning attached. Where `lynqu-prospect`
goes deep on one account, this goes wide on many — and the discipline that makes
it useful is **ranking and pruning before writing**. A hundred unranked leads is
not a target list, it's a chore you handed to a rep.

## Invocation

```
/lynqu research <icp description | event name | "companies like {customer}" | url>
```

A single URL is usually `/lynqu prospect`. Route there rather than doing a
shallow version of it here.

## Step 1: Anchor on the ICP — from evidence, not vibes

- **`list-lead-scoring-rules`** — the org has already encoded what it values.
  Score against these, not a generic template
- If no rules exist, or they look stale, say so and offer `/lynqu icp` first.
  Ten minutes there prevents researching fifty of the wrong companies
- **`list-leads`** filtered to won, plus **`get-lead`** on a few — the fastest
  read on what actually closes here
- **`list-companies`** — the firmographic shape of the existing book

If the user supplies an ICP that contradicts the org's own win data, say so once,
plainly, then research what they asked for. It's their call, and they may know
something the data doesn't.

## Step 2: Know what's already in flight

Research that produces accounts the org is already working wastes everyone's time
and creates duplicates.

- **`get-org-summary`** — current book
- **`list-campaigns`** — what's already being pursued, and by whom
- **`search-contacts`** and **`list-leads`** per candidate before it makes the
  list — cheap, and it turns "new lead" into "someone here already knows them",
  which is a better lead

## Step 3: Build the candidate set

Use your own web capabilities. Good sources, roughly in order of signal:

- **Event exhibitor and speaker lists** — the highest-intent list in B2B. Someone
  paying for a booth has budget, a field team, and a date
- **Funding and hiring announcements** — budget plus a trigger
- **Job postings** — the most honest description of a company's pain that exists.
  A posting for three field reps is a Lynqu trigger event
- **Customer lists of adjacent tools**, published case studies, partner pages
- **Industry directories and associations**

For each candidate capture: company, why it fits, the trigger, a named
decision-maker with their title, a public source link, and anything that suggests
timing.

## Step 4: Rank, then prune

Score each candidate 1–10 on **fit × timing**. Fit without timing is a nurture
list; timing without fit is a distraction.

| Band | Meaning | What happens to it |
|------|---------|--------------------|
| 8–10 | Strong fit, live trigger | Create as a lead, work now |
| 6–7 | Good fit, no urgency | Create, nurture, revisit at trigger |
| 4–5 | Plausible | Hold in the list, don't create yet |
| < 4 | Wrong shape | Drop, and say why — that's ICP feedback |

**Show the ranked table and let the user prune before anything is written.**
Research is cheap to redo; a polluted pipeline is not. This confirmation is the
most important step in the skill.

## Step 5: Create the keepers

On approval, per approved candidate:

1. **`create-lead`** — name, company, role, `source: "research"`. Only fields you
   can actually stand behind
2. **`add-lead-note`** — the fit rationale, the trigger, the sources, and the
   score with its reasoning. Six weeks later this note is the difference between
   a rep opening the conversation well and opening it cold
3. **`list-lead-pipelines`** + **`get-pipeline-stages`**, then
   **`update-lead-stage`** to the right entry stage — researched leads rarely
   belong in the same column as inbound
4. **`attach-leads-to-campaign`** when the research is for a campaign or event
5. **`bulk-update-leads`** (≤ 100) for tags and temperature across the cohort
6. **`add-lead-contact-point`** on the 8–10 band only — a dated first action.
   Creating fifty leads with no tasks produces a list nobody works
7. **`create-company`** where the account matters enough to hold its own record

Assignment: if the org has territories, `list-team-members` and `assign-lead`.
Note that `assign-lead` takes the **user id**, while campaign membership takes the
`organization_user_id` — `list-team-members` returns both, so read it rather than
assuming.

## Output format

```markdown
# Target List — {ICP or event}

Researched {n} candidates · {n} already known · {n} recommended

## Ranked
| # | Company | Fit | Trigger | Decision-maker | Score | Status |
|---|---------|-----|---------|----------------|-------|--------|
| 1 | … | … | Hiring 3 field reps | VP Sales, {name} | 9 | New |
| 2 | … | … | — | … | 6 | Already a lead (Sara) |

## Dropped, and why
{Feeds the ICP anti-profile.}

## Written to Lynqu
- {n} leads created in {pipeline} at {stage}
- {n} attached to {campaign} · tagged {tag}
- {n} first tasks opened for the 8–10 band
```

## Rules and constraints

- **Never invent contact data.** No pattern-guessed emails, no assumed phone
  numbers. Blank and "unverified" is the correct output.
- **Always show the ranked list before creating anything.**
- **Check for existing leads and contacts per candidate**, not once for the batch.
- **Bulk cap is 100** per `bulk-update-leads` call.
- **Every created lead gets a rationale note.** A lead with no reason to exist
  will be worked once, badly, and then ignored.
- **Say which claims are inferred.** "Probably 200–500 employees" is fine; stating
  it as fact is not.
- **Respect role gates.** Creating campaigns and pipelines is manager+ by
  default; an employee may attach only leads they own to a campaign they belong
  to; reading the org's scoring rules is admin by default. If
  `list-lead-scoring-rules` is denied, anchor on won leads instead and say so.

## Error handling

- **No won leads to learn from** (new org) → research against the ICP the user
  gives you, label it unvalidated, and suggest re-running after the first ten
  closes.
- **Source unreachable** (exhibitor list behind a login) → say so and use
  alternatives; never pad the list with plausible-sounding companies to hit a
  requested count. Ten real is better than fifty invented.
- **Candidate already a lead** → don't create. Report who owns it, and offer
  `add-lead-note` to add the new signal to the record that exists.
- **Fewer candidates than asked for** → deliver what you found and say the number
  honestly. Never fabricate to fill a quota.
- **Campaign attach fails** → the campaign may be closed or archived.
  `list-campaigns`, confirm status, and ask.
- **Bulk write denied** → an employee may create leads but not bulk-tag. Create
  the leads and report which cohort operations need a manager.

## Cross-skill integration

- ICP unclear or stale → `lynqu-icp` **first**
- Top of the ranked list deserves depth → `lynqu-prospect` on the 8–10 band
- Formal scoring after creation → `lynqu-qualify`
- Decision-makers per account → `lynqu-contacts`
- Then engagement → `lynqu-outreach`
- Researching for a specific show → `lynqu-event-blitz` owns the whole arc; run
  this inside it rather than alongside

## Example

> "/lynqu research mid-market SaaS companies in DACH exhibiting at SaaStr Europe —
> I want a VP Sales or RevOps contact at each."

The run: reads the org's scoring rules and won leads (mid-market wins at 61%) ·
pulls the published exhibitor list · finds 34 DACH companies in band, drops 11 as
too large against the anti-profile · checks all 23 against contacts and leads,
finds 4 already known · researches a named VP Sales or RevOps lead at each of the
remaining 19 with a public anchor · ranks by fit × timing, shows the table · on
approval creates the 12 the user keeps, attaches them to the SaaStr campaign,
tags `saastr-2026-target`, and opens a booth-invite task on the six that scored 8+.

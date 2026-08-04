---
name: lynqu-prospect
description: Full prospect audit of one account — research, buying committee, qualification, competitive position and an opening play — landing as a scored lead in Lynqu. Requires the Lynqu MCP server connected.
---

# Lynqu Prospect Audit

You are the flagship command of the Lynqu suite. You take one account — a URL, a
company name, or an existing lead — and produce a scored, prioritized, actionable
audit **that lands in Lynqu**: a lead with a fit score, a company record, a
buying committee, the research written to notes, and a first task with a due
date. The user should be able to close this conversation and still have
everything they need waiting in the pipeline.

The generic `/sales prospect` produces a document. This produces a document *and*
a working lead. That difference is the entire point — do not skip the writes.

## Invocation

```
/lynqu prospect <url | company name | lead id>
```

## Phase 0: Orient (before any research)

1. **`who-am-i`** — role and org. Employees can create and note leads; company
   records and campaign attachment need manager+ in some orgs. Know before you
   promise.
2. **Is this account already known?** Run all three, they are cheap:
   - `search-contacts` on the company domain and name
   - `list-leads` filtered by company
   - `list-companies` for an existing company record
3. **Branch on the answer:**
   - **Already a lead** → this is an *enrichment* pass. Read `get-lead` first,
     note what's already known, and only research the gaps. Do not create a
     second lead.
   - **Known contact, no lead** → research, then promote the contact.
   - **Unknown** → full audit, create at the end.

Announce which branch you're on. "You already have Acme as a lead at Discovery,
assigned to Sara — I'll enrich rather than duplicate" saves the user a merge.

## Phase 1: Company research

Use your own web capabilities. Fetch the homepage; if it loads, pull up to five
interior pages — about, team/leadership, pricing, blog, careers. If the URL is
unreachable, try with/without `www` and http/https, then say so and continue from
what public sources you can reach. A partial audit beats a refusal.

Extract and keep for later phases:

| Dimension | What you're looking for |
|-----------|-------------------------|
| Firmographics | Employees, HQ, geos, funding, ownership, founded |
| Business model | Who they sell to, how they charge, contract shape |
| Growth signals | Hiring (which roles), funding, launches, expansion, M&A |
| Tech stack | Public tooling, integrations, careers-page requirements |
| Trigger events | Leadership change, new market, compliance deadline, event attendance |
| Lynqu fit | Field teams, events, conference presence, distributed sellers |

**Optional accelerator:** if the org has enrichment credits, `get-enrichment-quota`
then `start-enrichment` on an existing lead does the firmographic legwork
server-side. Poll `get-enrichment-job`, and `confirm-enrichment` **only after
showing the user what it proposes** — it fills empty fields and the user owns
that decision. Skip silently if the quota is exhausted; it's an accelerator, not
a dependency.

## Phase 2: Buying committee

Identify 3–5 people, each with: name, exact title, seniority, why they matter,
and a personalization anchor (something they published, shipped, or said). Map
them to roles — economic buyer, champion, technical evaluator, blocker, user.

Check each against `search-contacts` before treating them as new. Someone else on
the team may already know them.

Do **not** guess emails. Pattern-matching a corporate email format is a guess
wearing a suit. Leave it blank, mark "unverified", and let `lynqu-contacts` do
the committee work properly if the user wants depth here.

## Phase 3: Qualification

Score BANT and MEDDIC against what you actually found. Every dimension carries a
confidence: **Confirmed** (stated publicly), **Inferred** (reasoned from
evidence), **Unknown** (say so).

Never let Inferred masquerade as Confirmed. A qualification report whose
confidence column is honest is useful even when it's mostly Unknown — that *is*
the finding, and it becomes the discovery agenda.

**Prospect Score (0–100):**

| Category | Weight | Measures |
|----------|--------|----------|
| Company fit | 25% | Size, industry, geography, budget signals |
| Pain evidence | 25% | Observable symptoms of the problem Lynqu solves |
| Timing | 20% | Trigger events, hiring, funding, upcoming events |
| Access | 15% | Named committee, warm path, existing contact |
| Competitive position | 15% | Incumbent, switching cost, contract timing |

Bands: **80+** work it now · **60–79** work it this quarter · **40–59** nurture ·
**<40** disqualify and say why. A disqualification with a reason is a real
deliverable — it saves the rep a week.

## Phase 4: Competitive position

What are they using today (or doing manually)? What would switching cost them?
What is our wedge? What are the three objections this specific account will
raise, and the honest answer to each — an objection response that requires a
false claim isn't a response, it's a future churn.

If the incumbent is a named competitor, hand off to `lynqu-competitors` for the
battlecard rather than improvising one here.

## Phase 5: Land it in Lynqu

Show the user the audit **first**, then write. Confirm once, then:

1. **Company record** — `list-companies` to check, then `create-company` (or
   `update-company` if it exists) with domain, size, industry.
2. **The lead** — `create-lead` with name, company, role, and `source:
   "prospect-audit"`. On the enrichment branch, skip this.
3. **The research** — `add-lead-note` with the audit: fit rationale, score and
   its reasoning, trigger events, sources. This is the note the rep reads
   thirty seconds before the call, so write it for that moment, not for a filing
   cabinet.
4. **Placement** — `list-lead-pipelines` and `get-pipeline-stages`, then
   `update-lead-stage` to the right entry stage. Score 80+ does not belong at the
   bottom of the same column as an unqualified inbound.
5. **The committee** — `create-company` first so contacts have a parent, then let
   `lynqu-contacts` populate participants if the user wants that depth.
6. **The next step** — `add-lead-contact-point` with a concrete first action and
   a due date. An audit with no task is a document; an audit with a task is a
   pipeline entry.
7. **Attribution** — if this came from an event or campaign push,
   `attach-leads-to-campaign`.

## Output format

```markdown
# Prospect Audit — {Company}

**Prospect Score: {n}/100 — {band}**
{One sentence: the single reason this is or isn't worth the rep's week.}

## Snapshot
| | |
|---|---|
| Employees / HQ / Funding | … |
| What they sell, to whom | … |
| Why now | {trigger event} |

## Buying committee
| Name | Title | Role | Anchor | Known to us? |
|------|-------|------|--------|--------------|

## Qualification
| Dimension | Finding | Confidence |
|-----------|---------|------------|
| Budget / Authority / Need / Timing | … | Confirmed \| Inferred \| Unknown |

## Competitive position
Incumbent · switching cost · our wedge · the three objections

## Opening play
Channel, the angle, and the first message — ready for `/lynqu outreach`

## Written to Lynqu
- Lead #{id} created in {pipeline} at {stage}
- Company {name} linked
- Audit saved as a note
- Task: "{first action}" due {date}
```

## Rules and constraints

- **One account per run.** A list is `/lynqu research`. Depth is the product here.
- **Show before you write.** Always. The user prunes; you execute.
- **Confidence labels are mandatory** on every qualification line.
- **No invented contact data.** Ever. Blank beats plausible.
- **Don't create a second lead for a known company** — enrich the one that exists.
- **Disqualify out loud.** A sub-40 score with a clear reason is a successful run.

## Error handling

- **URL unreachable** → try `www`/protocol variants, then continue from other
  public sources and mark the gaps. Never fabricate to fill a fetch failure.
- **Thin public presence** → drop every confidence to Inferred/Unknown, score
  conservatively, and recommend a discovery call *before* outreach. Say the
  research was thin; don't pad it.
- **`ADDON_REQUIRED` on enrichment** → skip that accelerator silently and
  continue with your own research.
- **Duplicate detected after creation** → `list-lead-duplicates`, then hand to
  `lynqu-lead-management` for the merge. Don't merge blind.
- **Employee role, company write refused** → keep the lead and the note; report
  that the company record needs a manager.

## Cross-skill integration

- Deep committee mapping → `lynqu-contacts`
- Formal scorecard against your real ICP → `lynqu-qualify`
- Battlecard for a named incumbent → `lynqu-competitors`
- The opening message → `lynqu-outreach`
- If the audit ends in a meeting → `lynqu-prep`
- Auditing many accounts → `lynqu-lead-research` first, then this on the top few

## Example

> "/lynqu prospect https://acme-logistics.com — we're exhibiting at their
> industry show next month."

The run: checks Acme against contacts and leads (unknown) · researches the site,
careers page and funding news · finds a VP Field Sales who posted about badge
scanning at trade shows · scores 84 (pain evidence and timing both strong) ·
notes the incumbent is a spreadsheet plus a badge-scanner rental · creates the
lead at Discovery with the audit as a note and a task: *"Reference the badge-scan
post in the booth invite — due 3 days before the show."*

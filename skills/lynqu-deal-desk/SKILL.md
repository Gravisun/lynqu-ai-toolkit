---
name: lynqu-deal-desk
description: Price a Lynqu deal and draft the quote — browse the price book, put priced lines on a deal, then produce a draft quote for a human to send. Requires the Lynqu MCP server connected.
---

# Lynqu Deal Desk

You price a deal from the org's own price book, put the lines on the opportunity,
and produce a **draft** quote. A human sends it. That boundary is deliberate and
absolute: sending a quote moves money and creates a commitment, so it stays with
the person whose name is on it.

Two rules of the object model that trip everyone up, stated once:

1. **A deal's value is the sum of its line items.** You do not set it by hand.
   Add, remove or reprice the lines and the value follows. A hand-set value that
   contradicts the lines is the number that shows up wrong in the forecast.
2. **A price-book item can only go on a deal in the same currency.** A EUR deal
   takes EUR catalog items. Mismatches are refused, and correctly so — silently
   converting someone's price list is how a margin disappears.

## Invocation

```
/lynqu proposal <deal | lead | company>
/lynqu quote <deal>
```

## Step 1: Find the deal

- **`list-opportunities`** / **`get-opportunity`** — the deals on the account.
  One lead can carry several: a renewal and an expansion are separate deals with
  separate values, and merging them in your head produces a quote nobody can
  approve
- **`get-lead`** — stage, score, the notes that say what was actually agreed
- **`list-quotes`** / **`get-quote`** — **read this before drafting anything.** A
  quote already in flight means you're revising, not creating, and a second
  independent quote for the same scope is a real problem in front of a customer
- **`get-company`** — who's actually buying, for the quote header

If no opportunity exists yet, **`create-opportunity`** on the lead — but only when
scope is genuinely understood. A deal created to have something to quote against
becomes a forecast entry nobody believes.

Two clean-ups belong here, before any pricing, and each needs its own yes:

- **A secondary deal that isn't real** (a renewal that was never going to
  happen, an upsell opened twice): **`delete-opportunity`**, naming the deal.
  A lead's primary deal cannot be deleted; it closes with a stage move on the
  lead
- **The account split across two company records** (the roll-up on
  `get-company` is missing deals you know exist): **`merge-companies`** with no
  arguments lists the duplicate pairs with each side's lead, contact and deal
  counts. Merging moves everything to the survivor and cannot be undone here, so
  show both sides and confirm that one pair. Needs `companies.manage` (managers
  by default)

## Step 2: Confirm the scope before you price it

The most expensive failure in this skill is a clean quote for the wrong thing.

Read the notes and contact points for what was agreed: how many seats, which
modules, what term, when it starts. Where the record is ambiguous — **ask**. One
question now beats a revision cycle and a credibility hit later.

Explicitly confirm:

- **Quantity** and what it's measured in (seats? locations? events?)
- **Term** — monthly, annual, multi-year
- **Start date** — especially if it's tied to an event or a renewal
- **Currency** — the deal's currency, which the catalog items must match
- **Anything already promised** in a conversation. A discount mentioned verbally
  and missing from the quote is a fight in week two

## Step 3: Build the lines from the price book

- **`list-catalog-items`** — the org's price book. Filter to the deal's currency
- **`manage-deal-line-item`** — add each line: item, quantity, and any agreed
  discount. Name and price are snapshotted onto the line at add time, so a later
  price-book change doesn't silently rewrite a sent quote
- Re-read **`get-opportunity`** afterwards and confirm the rolled-up value is what
  you expect. If it isn't, a line is wrong — don't "fix" it by overriding the value

**Discounts.** Apply only what's been agreed and record why on the line or in a
note. An unexplained discount is a precedent: the next deal in that segment gets
asked for the same one, and nobody remembers the reason.

**Missing from the price book?** Say so. Don't invent a price. Either the item
needs adding by someone with the authority (`manage-catalog-item`, admin
territory in most orgs) or the deal needs custom pricing that a human has to own.

## Step 4: Draft the quote

- **`manage-quote`** — create or revise the draft: line items, validity period,
  terms, the customer's details
- Versioning is handled server-side. A revision supersedes its predecessor rather
  than overwriting it, so the history of what was offered survives — don't try to
  edit a sent quote in place
- Once a quote is **sent**, its contents are frozen. Changes mean a new version.
  That's a feature; treat it as one
- The quote renders in the lead's locale where set, so the customer reads it in
  their own language. Check the currency and locale look right before handing it
  over

**Sending, accepting, declining and revising a sent quote are deliberately not
available here.** They email customers and move deal value. Point the user at the
Lynqu app — this is human-in-the-loop by design, not a missing feature, and
saying that clearly is better than apologising for it.

## Step 5: Set up what happens next

- **`add-lead-contact-point`** — a dated follow-up on the quote. Quotes go stale
  in silence; a task two days after sending is what converts one
- **`add-lead-note`** — the pricing rationale: what was agreed, what was
  discounted and why, what was deliberately excluded
- **`update-lead-stage`** if the deal genuinely moved to a proposal stage
- **Forecast category** — set it honestly. `get-forecast` is only as good as the
  categories under it, and an optimistic commit is a promise someone else has to
  keep

## Output format

```markdown
# Quote Draft — {Company}

**Deal:** {name} · {currency} · {term} · starts {date}
**Status:** draft v{n} {(revises v{n-1})}

## Lines
| Item | Qty | Unit | Discount | Line total |
|------|-----|------|----------|------------|
| … | 25 | €12.00 | 10% (agreed on call, 3 Aug) | €270.00 |

**Deal value: {total}** — the sum of the lines, rolled up automatically.

## Scope confirmed
{Quantity, term, start, currency, and anything promised verbally.}

## Not included
{What was deliberately left out, so nobody assumes it.}

## Written to Lynqu
- {n} line items on deal #{id} · value now {x}
- Quote v{n} saved as a **draft**
- Task: "Follow up on the quote" due {date}

**Sending is yours.** Open the quote in Lynqu and send it when you're ready.
```

## Rules and constraints

- **Never send, accept, decline or revise a sent quote.** No tool here does it,
  and that's the design.
- **Never set a deal's value directly.** Price the lines; the value follows.
- **Never mix currencies.** Catalog item currency must match the deal's.
- **Never invent a price** for something not in the price book.
- **Never apply a discount that wasn't agreed**, and always record the reason.
- **Read existing quotes first.** Two live quotes for one scope is a customer-facing
  mess.
- **Ask when scope is ambiguous.** One question beats a revision.
- **Set the forecast category honestly.** Optimism here becomes someone's missed
  number.
- **A sent quote is frozen.** Revise with a new version; never edit in place.
- **Never delete a deal or merge companies on inference.** Name the record, show
  what moves or disappears, and get a yes for that one call.

## Error handling

- **Currency mismatch** → the call is refused, and rightly. Show which items are
  available in the deal's currency, or ask whether the deal's currency is wrong.
  Never convert a price yourself.
- **Item not in the price book** → name it, don't price it. Route to whoever can
  add it, or flag it as custom pricing needing a human.
- **Value doesn't match expectation** → a line is wrong. Re-read the lines. Do not
  "correct" the total.
- **Quote already sent** → you're revising. Create a new version, and say clearly
  that the customer has the previous one.
- **No opportunity on the lead** → create one only if scope is real; otherwise say
  the deal isn't defined enough to quote.
- **Permission denied on catalog write** → price book edits are admin territory in
  most orgs. Deliver the missing item as a request with the details filled in.
- **Multiple deals on one account** → ask which. Never guess between a renewal and
  an expansion.
- **`delete-opportunity` refused on the lead's main deal** → that is the primary
  deal, which follows the lead. Close it with `update-lead-stage` (won or lost),
  or delete the lead if the whole record was a mistake.

## Cross-skill integration

- Scope came from a meeting → `lynqu-prep` wrote the agenda; the notes are there
- Pricing objection expected → `lynqu-competitors` for the honest answer before
  the number goes out
- Quote sent, then silence → `lynqu-sales-followup` (post-proposal cadence)
- Deals with no value set, distorting the forecast → this skill, then
  `lynqu-pipeline-report`
- Committee needs to approve → `lynqu-contacts`, because a quote sent to someone
  without signing authority is a quote that sits

## Example

> "/lynqu proposal Acme — they want 25 seats plus the events module, annual, and
> I promised them 10% on the call."

The run: finds one open opportunity in EUR · reads `list-quotes` and confirms
nothing is in flight · reads the notes and confirms the 10% and the annual term,
but flags that the start date was never discussed and asks · filters the price
book to EUR, adds 25 seats and the events module with the 10% discount recorded
against the agreed call · re-reads the deal and confirms the roll-up · drafts
quote v1 with a 30-day validity, notes the pricing rationale, moves the deal to
Proposal, sets the forecast category to best case rather than commit, and opens
*"Follow up on the quote"* for two days after sending — then hands it over:
**"Draft is ready in Lynqu. Sending is yours."**

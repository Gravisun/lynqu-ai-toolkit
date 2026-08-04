---
name: lynqu-deal-desk
description: Price a Lynqu deal and draft the quote — browse the price book, put priced lines on a deal, then produce a draft quote for a human to send. Requires the Lynqu MCP server connected.
---

# Lynqu Deal Desk

Turning "they want ten seats and onboarding" into a number, and that number into
a quote the rep can send. The price book holds what you sell; deal lines say
what *this* customer is buying; the quote is the document they see.

## When to use this

- Pricing a deal — adding, changing or removing what's on it.
- Drafting a quote or proposal from a deal.
- Answering "what is this deal worth and what's in it?"
- Maintaining the price book (admin).

## Prerequisites

- Lynqu MCP connected (`/mcp/v2`). See `../../docs/mcp/connect.md`.
- AI-tier plan. Reading the price book is open to any member; **writing it is
  admin-only**. Pricing a deal follows that deal's own permissions — an
  employee can price their own deals.

## The one thing to understand first

**A deal's value is the sum of its lines.** You do not set the value directly —
you add lines and the total follows. That is deliberate: the lines are the
audit trail for the number.

Two consequences:

- Adding a line changes the deal's value. Say so when you report back.
- If someone has manually overridden the deal's value in the app, lines still
  record correctly but the total stays overridden until a human clears it. The
  tools tell you this (`value_is_overridden`) — surface it rather than
  silently appearing to have no effect.

## Workflow

1. **Find the deal.** `list-opportunities` (filter by company, owner or
   status), then `get-opportunity` for its current value, currency and stage.
2. **See what's already on it.** `get-quote` on any existing quote shows the
   line-level detail; `list-quotes` shows the status and version history.
3. **Browse the price book.** `list-catalog-items`, optionally with `search`.
   Note each item's **currency** — see the guardrail below.
4. **Price the deal.** `manage-deal-line-item` with `action: "create"`:
   - From the price book — pass `catalog_item_id` and a `quantity`. Name,
     price and description are snapshotted from the item.
   - Free-form — pass `name` and `unit_price` directly for anything not in
     the book.
   - Use `discount_percent` for a per-line discount. Correct mistakes with
     `action: "update"`, remove with `action: "delete"`.
5. **Draft the quote.** `manage-quote` with `action: "create"` and the
   `opportunity_id`. Lines are seeded from the deal automatically. Add a
   `title`, `valid_until`, `notes` and `terms`. Refine with
   `action: "update"`.
6. **Hand off.** Report the total and tell the user the draft is ready to send
   **from the app**. Do not imply you have sent it.

## Tools used

`list-opportunities`, `get-opportunity`, `create-opportunity`,
`list-catalog-items`, `manage-catalog-item`, `manage-deal-line-item`,
`list-quotes`, `get-quote`, `manage-quote`.

## Guardrails

- **You cannot send a quote, and should not offer to.** Sending, accepting and
  declining are human actions in the app — they email a customer and move deal
  value. There is no tool for them by design. Draft, then hand off.
- **A sent quote is final.** Editing or deleting anything past draft is
  refused. If the customer wants changes, tell the user to create a revision in
  the app; don't try to work around it.
- **Currency is not converted.** A price-book item may only go on a deal in the
  *same* currency; a mismatch is rejected rather than quietly converted. An org
  selling in two currencies keeps one item per currency. If you hit
  `catalog_currency_mismatch`, say which currency the deal is in and offer the
  matching item — never substitute a converted number.
- **Price-book edits are admin-only** and never rewrite history: retiring an
  item leaves existing lines and sent quotes at their original prices. Say that
  when a user worries about changing a price.
- **Confirm before changing a priced deal.** Show the line you're about to add
  and the resulting total before writing it.

## Example

> "Acme wants 25 Business seats and the onboarding package, with 10% off
> onboarding. Put that on their deal, then draft a quote valid for 30 days with
> our standard terms."

The assistant reads the deal, finds the matching price-book items in the deal's
currency, adds both lines with the discount, reports the new deal total, drafts
the quote — and tells the user it's ready to send from the app.

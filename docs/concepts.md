# The Lynqu model

A quick mental model of the objects the MCP tools and skills work with. If you
understand these seven nouns, every skill in this repo will make sense.

Lynqu runs the full arc: **capture → engage → manage → measure.**

## Cards

Digital business cards — the entry point. A card holds contact info, social
links, services, a template, and a color palette. Both individuals and teams
have them. Sharing a card (QR, NFC, link) is how a relationship starts.

- Personal users manage their own cards (`/mcp/me`).
- Orgs manage team cards (`/mcp/v2`).

## Contacts

The organization-level shared address book (OrgContacts). When someone shares
their details back with you — or you scan their card/badge — they land here as a
contact the whole team can search.

## Leads

A **lead** is a sales-pipeline entry: a contact you're actively working toward a
deal. Leads have a **kanban placement** (which environment + stage), a **score**,
a **temperature** (hot/warm/cold), an owner, tags, and a full **activity
timeline** (notes, stage changes, follow-ups sent).

Capture turns contacts into leads; management moves them through stages.

## Lead Environments

Kanban **tabs** that each own their own set of pipeline stages. Every org has a
default environment; create more for distinct workstreams (e.g. "Events",
"Inbound", "Partnerships"). Creating environments is an **admin** action.

## Pipeline Stages

The customizable **columns** within an environment (e.g. New → Qualified →
Demo → Proposal → Won/Lost). Stages can carry win/loss markers. Creating stages
is an **admin** action.

## Campaigns

Marketing/sales initiatives. A campaign has **goals** (15+ metric keys),
**members**, a budget, an optional follow-up template, and an auto-minted public
capture URL at `/c/{token}`. Leads and events can roll up to a campaign so you
can measure ROI. Creating/owning campaigns is a **manager+** action.

## Events

Time-bound activities (a conference, a booth, a dinner) with a **4-state
lifecycle**: `draft → active → archived → permanently_deleted`. Open-ended
events close on demand. An event can link to a campaign so captures at the event
attribute correctly. Every lifecycle change is audit-logged. Creating/managing
events is a **manager+** action.

## Supporting objects

- **Departments** — org-chart structure (nestable via `parent_id`), with an
  optional manager and contact info.
- **Employees** — organization members with a role (`admin` / `manager` /
  `employee`). Invite, update, remove, or bulk-import from a spreadsheet.
  Membership changes are **admin** actions.
- **Follow-up Templates** — HTML-purified email templates with mustache tokens,
  dispatched through a CAN-SPAM-compliant pipeline.
- **Capture Forms** — public submission forms attached to a campaign at
  `/c/{token}`.

## Who can do what

The MCP enforces three gates, in order:

1. **Plan gate** — running tools needs an AI-tier plan (Pro+AI / Business /
   Corporate). Connecting is open to any plan.
2. **Org policy** — your org admin can enable/disable MCP, restrict it to
   certain roles, or make it read-only.
3. **Role gate** — `employee` < `manager` < `admin`. Some tools require
   manager+ (campaigns, events, lead assignment, follow-up templates) or admin
   (pipeline structure, employee management).

See [`mcp/authentication.md`](mcp/authentication.md) for how this maps onto the
OAuth flow.

## Two identifiers to know

Some tools take `organization_user_id` (the membership join-row id — used for
campaign membership and department assignment); others take the underlying
`user_id` (used for lead assignment). The **`list-team-members`** tool returns
both, so you never have to guess which one a tool wants.

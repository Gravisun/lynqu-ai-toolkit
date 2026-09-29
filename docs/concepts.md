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
deal. Leads have a **kanban placement** (which pipeline + stage), a **score**,
a **temperature** (hot/warm/cold), an owner, tags, and a full **activity
timeline** (notes, stage changes, follow-ups sent).

Capture turns contacts into leads; management moves them through stages.

## Lead Pipelines

Kanban **tabs** that each own their own set of pipeline stages. Every org has a
default pipeline; create more for distinct workstreams (e.g. "Events",
"Inbound", "Partnerships"). Older docs call these "lead environments".
Creating pipelines is a **manager+** action by default.

## Pipeline Stages

The customizable **columns** within a pipeline (e.g. New → Qualified →
Demo → Proposal → Won/Lost). Stages can carry win/loss markers. Creating stages
is a **manager+** action by default.

## Campaigns

Marketing/sales initiatives. A campaign has **goals** (15+ metric keys),
**members**, a budget, an optional follow-up template, and an auto-minted public
capture URL at `/c/{token}`. Leads and events can roll up to a campaign so you
can measure ROI. Creating/owning campaigns is a **manager+** action.

## Events

Time-bound activities (a conference, a booth, a dinner) with a **4-state
lifecycle**: `draft → active → archived → permanently_deleted`. Open-ended
events close on demand. An event can link to a campaign so captures at the event
attribute correctly. Every lifecycle change is audit-logged. Creating and
managing events is an **admin** action by default; managers can compare events
side by side.

## Supporting objects

- **Departments** — org-chart structure (nestable via `parent_id`), with an
  optional manager and contact info.
- **Employees** — organization members with a role (`admin` / `manager` /
  `employee`). Invite, update, remove, or bulk-import from a spreadsheet.
  Membership changes are **admin** actions.
- **Capture Forms** — public submission forms attached to a campaign at
  `/c/{token}`.
- **NFC devices**: physical cards, tags and fobs. Each one points at a digital
  card and can be handed to a teammate without rewriting the tag.

## Follow-ups

Emails to leads go out from **follow-up templates**: HTML-purified, with
mustache tokens, and sent through one CAN-SPAM-compliant pipeline (opt-out,
unsubscribe header, the org's sender identity). A **sequence** is a follow-up
trigger with up to five timed steps, one running per lead.

- **Team and personal.** Team templates and sequences belong to the org; saving
  one needs the follow-ups permission (admins by default). Every member can also
  save **personal** ones, used only on leads they own. A personal version of a
  team template or sequence **replaces the team text on that member's leads**,
  unless an admin **locked** the team one. The swap happens when an automated
  email is sent; a manual send uses exactly the template picked. An admin can
  switch personal follow-ups off for the whole workspace.
- **Replies.** When reply tracking is on, every follow-up carries a tracked
  Reply-To. A human reply then lands on the lead's timeline and in the outbox,
  stops the lead's scheduled automated follow-ups, and is forwarded to the
  person the email went out as. Auto-replies are recorded, not forwarded.
- **Performance.** Every send is counted: sent, delivered, opened, clicked,
  replied, meetings booked (within 14 days) and deals won (within 90 days, last
  touch), by template, sequence, step, rep or AI employee. **Reply rate is the
  headline**, and a row is only ranked once it has 20 delivered emails. When
  reply tracking is off, reply rates read 0 without meaning nobody answered, and
  the tools say so (`replies_tracked`).
- **Stopping one lead.** A lead's automated follow-ups can be paused on its own,
  without touching anyone else's. Closing the lead stops them too.

## AI employees

Hosted AI employees work the pipeline alongside the team. Each one is a member
of the org with its own account, and works only with the tools its role allows
and an admin granted.

- **Shadow first.** A new agent starts in an observe-only trial by default: it
  drafts, and a person can review what it would have done before it goes live.
- **A timeline for everything.** Every action is logged with the rule that
  matched and the agent's own rationale, and can be read later.
- **Approvals.** Actions its risk policy marks for review park until a person
  approves or rejects them, **one action at a time**. Rejecting takes a reason,
  which is how the agent learns what not to do. Deciding one through the
  assistant is an admin action by default, deliberately stricter than the
  approvals queue in the app.
- **Handoffs.** When an agent stops (for example a reply came in, or the
  person asked for a human) it hands the work back to a person with a written
  brief. Agents read replies as data; they never answer one.
- **The sales brief.** One org-level brief (who the org sells to, what it
  offers, the fit profile, the booking link) that an admin confirms. It is what
  the agents write from, and it goes stale when the org's website or industry
  changes.

## Who can do what

The MCP enforces three gates, in order:

1. **Plan gate**: running tools needs an AI-tier plan (Pro+AI, Business+AI or
   Enterprise). Connecting is open to any plan.
2. **Org policy**: your org admin can enable or disable MCP, restrict it to
   certain roles, or make it read-only. An org in the grace period after its
   subscription lapsed is read-only too.
3. **Role and capability gate**: roles rank `employee` < `manager` < `admin`,
   and most tools check a named capability that a role holds by default.
   Managers hold campaigns, lead assignment, pipelines and companies; admins
   hold events, departments, scoring rules, membership and AI employee
   decisions. On Enterprise, custom roles can move a capability up or down.
   Billing, the audit log, integrations, access domains and compensation stay
   admin only, whatever the role setup.

See [`mcp/authentication.md`](mcp/authentication.md) for how this maps onto the
OAuth flow.

## Two identifiers to know

Some tools take `organization_user_id` (the membership join-row id — used for
campaign membership and department assignment); others take the underlying
`user_id` (used for lead assignment). The **`list-team-members`** tool returns
both, so you never have to guess which one a tool wants.

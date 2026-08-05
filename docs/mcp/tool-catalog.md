# Lynqu MCP tool catalog

The complete set of tools the hosted Lynqu MCP server exposes. This mirrors the
server's registered tools — when in doubt, ask the server itself via the
**`how-can-you-help-me`** tool, which classifies your goal and returns the exact
tool calls to run.

- **Organization server** (`/mcp/v2`): all categories below — **136 tools**.
- **Personal server** (`/mcp/me`): 9 user-scoped tools — `how-can-you-help-me`,
  `list-cards`, `get-card`, `create-card`, `update-card`, `get-card-stats`,
  `get-dashboard-summary`, `get-profile`, `who-am-i`. No role gate.

A ✍️ marks tools that **write** (create/update/send). The **Role** column is the
minimum org role required (personal server has no role gate). Add-on-gated
categories are labelled; calling one without the add-on returns an
`ADDON_REQUIRED` error naming the add-on key.

> Your own permissions still apply on top of everything here. The assistant can
> never see or do more than you can in the app, and an org admin can restrict
> which roles may use the assistant at all — or make it read-only.

## Meta

| Tool | Role | What it does |
| --- | --- | --- |
| `how-can-you-help-me` | employee | Describe a business situation in plain language and get a structured suggestion for how to solve it using Lynqu. |

## Discovery

| Tool | Role | What it does |
| --- | --- | --- |
| `get-org-summary` | employee | One-shot organization overview: org info, team size by role, department count, active campaigns and events, lead pipelines, and a pipeline snapshot showing leads-per-stage across the default pipeline. |
| `list-team-members` | employee | List organization members with role, department, status, and the count of leads currently assigned to each. |

## Cards

| Tool | Role | What it does |
| --- | --- | --- |
| `list-cards` | employee | List the authenticated user's digital business cards. |
| `list-org-cards` | employee | List the cards belonging to your ORGANIZATION (not just the ones you created) — the same inventory shown in the /org/cards dashboard. |
| `get-card` | employee | Get detailed information about a specific card by ID or slug. |
| `create-card` ✍️ | employee | Create a new digital business card for the authenticated user. |
| `update-card` ✍️ | employee | Update fields on an existing card owned by the authenticated user. |

## Contacts

| Tool | Role | What it does |
| --- | --- | --- |
| `list-contacts` | employee | List the organization's contacts (address book). |
| `search-contacts` | employee | Search the organization's contacts by name, email, phone, or company. |
| `get-contact` | employee | Get one contact, with the leads and deals they are linked to. |
| `create-contact` ✍️ | employee | Add a person to the organization's shared roster. Member-open on purpose — the people who capture are the people who meet new contacts. |
| `update-contact` ✍️ | employee | Update a contact's details. Deleting one is manager-only (it is shared data other people's leads point at) and has no tool. |

## Leads

| Tool | Role | What it does |
| --- | --- | --- |
| `list-leads` | employee | List leads for the user's organization. |
| `get-lead` | employee | Get full detail for a single lead by ID, including pipeline stage, assigned user, source card, current campaign/event attachments, the lead's free-text `notes` field, its multi-note timeline (`notes_t. |
| `create-lead` ✍️ | manager | Create a new lead in the organization's sales pipeline. |
| `update-lead` ✍️ | employee | Update a lead's own fields (name, contact details, company, value, currency, tags, custom fields). Stage moves go through `update-lead-stage`, not here. |
| `manage-lead-participant` ✍️ | employee | Add, remove or promote someone on a lead's buying committee. Max 15 per lead; exactly one may be primary, and promoting someone is what re-points the lead at their contact record. |
| `add-lead-note` ✍️ | employee | Add a note to a lead's note timeline. |
| `list-lead-documents` | employee | List the files attached to a lead (PDF / Markdown / Office docs) — the same Documents panel shown in the web Lead detail. |
| `add-lead-document` ✍️ | employee | Attach a file to a lead (PDF, Markdown, Word, Excel, PowerPoint, CSV, or plain text), stored in the organization's storage and counted against its quota — the same Documents panel shown in the web Lea. |
| `list-lead-contact-points` ✍️ | employee | List lead contact points — Trello-style sub-task checklists of planned touches (e.g. |
| `add-lead-contact-point` ✍️ | employee | Add a contact point (sub-task / planned touch) to a lead's checklist — e.g. |
| `update-lead-contact-point` ✍️ | employee | Update a lead's contact point (sub-task): rename it, change its description/notes/priority/due date/assignee, or toggle its done-state via `completed`. |
| `delete-lead-contact-point` ✍️ | employee | Delete a contact point (sub-task) from a lead's checklist. |
| `assign-lead` ✍️ | manager | Assign a lead to an organization member (or pass assigned_to_user_id =null to unassign). |
| `update-lead-stage` ✍️ | employee | Move a lead to a different pipeline stage. |
| `bulk-update-leads` ✍️ | employee | Apply the same change to up to 100 leads at once. |
| `attach-leads-to-campaign` ✍️ | manager | Attach up to 100 leads to a campaign (sets `leads.campaign_id`), or pass `campaign_id=null` to DETACH them from their current campaign. |
| `list-lead-duplicates` | manager | List detected duplicate lead pairs for the organization (open pairs awaiting review — not yet dismissed or merged). |
| `merge-leads` ✍️ | employee | Resolve a detected duplicate lead pair (from list-lead-duplicates): merge the two leads into one, or dismiss the pair as "not the same person". |
| `list-lead-views` ✍️ | employee | List the saved lead views visible to the caller: their personal views plus the organization's shared ("team") views. |

## Pipeline / Lead Environments

| Tool | Role | What it does |
| --- | --- | --- |
| `list-lead-pipelines` | employee | List the organization's lead pipelines (kanban tabs). |
| `get-pipeline-stages` | employee | List pipeline stages, optionally scoped to a single lead pipeline. |
| `create-lead-pipeline` ✍️ | admin | Create a new lead pipeline (kanban tab) in the organization. |
| `create-pipeline-stage` ✍️ | admin | Create a pipeline stage inside a lead pipeline. |
| `move-lead-pipeline` ✍️ | manager | Move a lead from one pipeline tab to another. |

## Campaigns

| Tool | Role | What it does |
| --- | --- | --- |
| `list-campaigns` | employee | List the organization's campaigns. |
| `get-campaign` | employee | Get full detail for a single campaign by ID, including goals (with target + metric_key), active members, events under the campaign, follow-up template binding, capture forms, and totals. |
| `create-campaign` ✍️ | manager | Create a new campaign in the user's organization. |
| `update-campaign-status` ✍️ | manager | Move a campaign through its lifecycle. |
| `add-campaign-member` ✍️ | manager | Add an organization user to a campaign as either an owner or a regular member. |
| `list-campaign-goals` | employee | List the goals attached to a campaign. |
| `list-metric-catalogue` | employee | List every campaign-goal metric you can target, with each metric's key, label, description, unit, and capability flags (supports_stage_filter, supports_per_member, requires_scoring_rule, requires_scor. |
| `create-campaign-goal` ✍️ | manager | Add a goal to a campaign so its progress is tracked. |
| `update-campaign-goal` ✍️ | manager | Update an existing campaign goal's editable fields. |
| `delete-campaign-goal` ✍️ | manager | Delete a goal from a campaign. |
| `manage-campaign-booking-service` ✍️ | employee | View or set a campaign's booking service — the meeting length (duration, in minutes) and type used to size bookings taken through that campaign. |

## Events

| Tool | Role | What it does |
| --- | --- | --- |
| `list-events` | employee | List events for the organization. |
| `get-event` | employee | Get full detail for an event by ID, including campaign, capture form, follow-up template, lead count, and complete lifecycle timestamps. |
| `issue-tickets` ✍️ | admin | Issue entry tickets to leads for an event. |
| `list-event-tickets` | admin | List the tickets issued for an event, with per-tier issued and checked-in counts. |
| `create-event` ✍️ | manager | Create an event in the organization. |
| `update-event-lifecycle` ✍️ | manager | Transition an event through its 4-state lifecycle via the canonical actions: - activate: draft → active (requires start_at + end_at for dated events; open-ended events skip the window guard) - close:. |
| `link-event-to-campaign` ✍️ | manager | Attach an event to a campaign (events.campaign_id), or pass campaign_id=null to detach. |
| `get-event-portfolio` | manager | Compare events side by side: per event — leads captured (direct + via linked campaigns), won count, win rate, pipeline value and won revenue in the org currency (unconvertible leads excluded and count. |

## Booking

| Tool | Role | What it does |
| --- | --- | --- |
| `list-booking-requests` | employee | List the organization's unclaimed booking requests — prospects who asked to book a meeting via a campaign capture form or an event, but who have not yet been claimed onto a team member's card. |
| `accept-booking-request` ✍️ | employee | Accept a campaign booking request (from `list-booking-requests`) and assign it to a teammate, turning it into a real appointment on THEIR calendar. |
| `manage-appointment` ✍️ | employee | Action one of YOUR appointments (a booking hosted on a card you own). |
| `get-booking-report` | manager | Org-wide booking performance over a date window: total bookings, no-show and cancellation rates, volume over time (day/week/month), peak hours + weekdays, per-service and per-type breakdowns, and repe. |
| `get-meeting-brief` | employee | The AI pre-meeting brief for an appointment linked to a lead: who they are, what they engaged with, open items, and talking points. |
| `list-card-bookings` | employee | List the bookings customers have made on YOUR cards — including who booked each one. |
| `get-booking` | employee | Fetch the full detail of one booking on a card you own: status, start/end, the requester's contact details, the booked service, and the customer's answers to your booking form (each with its question. |
| `reschedule-booking` ✍️ | employee | Move one of your bookings to a new start time, keeping its original duration. |
| `propose-booking` ✍️ | employee | Propose meeting times to a lead. |
| `list-booking-services` | employee | List the bookable services on one of your booking-enabled cards — the menu of options (name, duration in minutes, type) a customer picks from when booking. |
| `manage-booking-service` ✍️ | employee | Add, edit, or remove a bookable service on one of your booking-enabled cards. |
| `manage-booking-settings` ✍️ | employee | Read or change the booking setup for one of your cards. |
| `list-booking-pools` | employee | List your organization's team booking pools — shared "book a meeting with our team" pages that route each booking to a member via round-robin or priority. |
| `get-booking-pool` | employee | Get one team booking pool: settings (strategy, duration, timezone, horizon), the member roster with rotation counters, and its pool-owned services. |
| `create-booking-pool` ✍️ | employee | Create a team booking pool — a shared "book a meeting with our team" page that routes each booking to a member (round_robin: evens the load; priority: prefers lower-priority-number members first). |

## Companies

| Tool | Role | What it does |
| --- | --- | --- |
| `list-companies` | employee | List the organization's companies (customer accounts. |
| `get-company` | employee | Get full detail for one company (customer account): profile fields, parent/subsidiaries, custom fields, the deal roll-up (open/won/lost counts + per-currency open and won value — "all deals at Acme"),. |
| `create-company` ✍️ | manager | Create a company (customer account. |
| `update-company` ✍️ | manager | Update a company's profile fields (name, domain, website, industry, size band, phone, location, assignee, custom fields). |

## Deals, Line Items & Quotes

| Tool | Role | What it does |
| --- | --- | --- |
| `list-opportunities` | employee | List deals (opportunities. |
| `get-opportunity` | employee | Get full detail for one deal (opportunity): stage, status, value, financials, forecast fields (probability, expected close date), custom fields, company and parent lead. |
| `create-opportunity` ✍️ | employee | Create a renewal or upsell deal (secondary opportunity) on an existing lead — the person keeps ONE lead row; each concurrent deal is its own opportunity with its own stage, value and owner. |
| `update-opportunity` ✍️ | employee | Update a secondary deal's own fields. Its `value` is deliberately not settable here — the roll-up owns it, so price a deal with `manage-deal-line-item`. |
| `move-opportunity-stage` ✍️ | employee | Move a secondary deal to another stage, optionally into a different pipeline. The lead's PRIMARY deal moves with `update-lead-stage` instead; calling this on one returns `use_lead_move_stage`. |
| `list-quotes` | employee | List quotes with their status, totals and version chain. |
| `get-quote` | employee | Full detail of one quote: every line item with quantity, unit price and discount, plus subtotal, discount total, tax, notes, terms and the version chain. |
| `manage-quote` ✍️ | employee | Draft a quote on a deal, edit a draft, or delete one. |
| `manage-deal-line-item` ✍️ | employee | Add, change or remove a priced line on a deal. |

## Price Book

| Tool | Role | What it does |
| --- | --- | --- |
| `list-catalog-items` | employee | Browse the organization's price book — the reusable products and services reps put on deal lines and quotes. |
| `manage-catalog-item` ✍️ | admin | Create, update or delete a price-book item — the reusable products and services reps put on deal lines and quotes. |

## Follow-ups

| Tool | Role | What it does |
| --- | --- | --- |
| `list-followup-templates` | employee | List follow-up email templates in the organization. |
| `create-followup-template` ✍️ | admin | Create a follow-up email template. |
| `send-followup-now` ✍️ | employee | Manually send a follow-up email to a single lead using a chosen FollowUpEmailTemplate. |

## Capture Forms

| Tool | Role | What it does |
| --- | --- | --- |
| `list-capture-forms` | employee | List capture forms for the organization's campaigns. |
| `get-capture-form-stats` | employee | Get submission stats for a capture form: total submitted leads, last 30 days, breakdown by status (open/won/lost), and last submission timestamp. |

## Lead Scoring

| Tool | Role | What it does |
| --- | --- | --- |
| `list-lead-scoring-rules` | employee | List the organization's lead-scoring rules with their predicate, points, priority, enabled flag, and optional threshold/promotion target. |
| `create-lead-scoring-rule` ✍️ | admin | Create a lead-scoring rule: a sandboxed boolean `predicate` that, when true for a lead, adds `points` to its score (priority breaks ties). |
| `update-lead-scoring-rule` ✍️ | admin | Update a lead-scoring rule's fields (name, predicate, points, priority, enabled, threshold, target_pipeline_stage_id). |
| `delete-lead-scoring-rule` ✍️ | admin | Delete a lead-scoring rule permanently. |

## Enrichment

| Tool | Role | What it does |
| --- | --- | --- |
| `get-enrichment-quota` | employee | Read the enrichment quota without starting a job. |
| `start-enrichment` ✍️ | employee | Start enriching a subject (firmographics / social, vendor-gated) as an async job. |
| `get-enrichment-job` | employee | Poll an enrichment job by id. |
| `confirm-enrichment` ✍️ | employee | Apply a ready/disambiguation enrichment job's data to its subject (fill-empty-only — server values are never overwritten). |

## Automation (Workflow Automation add-on)

| Tool | Role | What it does |
| --- | --- | --- |
| `list-automation-rules` ✍️ | manager | List the organization's workflow automation rules (trigger → actions), including enabled/paused state, fire counts and last-fired times. |
| `create-automation-rule` ✍️ | manager | Create a workflow automation rule: when a trigger fires for a lead, run an ordered list of actions after an optional delay. |
| `update-automation-rule` ✍️ | manager | Update a workflow automation rule. |
| `delete-automation-rule` ✍️ | manager | Delete a workflow automation rule. |
| `list-automation-rule-runs` ✍️ | manager | List recent executions of a workflow automation rule: which lead it fired for, per-action outcomes, and completed/partial/failed status. |

A rule is a **trigger** plus 1–5 ordered **actions**. Triggers: `lead_created`,
`stage_changed`, `score_crossed`, `booking_no_show`, `lead_inactive`,
`ticket_checked_in`. Actions: `send_template`, `assign`, `move_stage`,
`add_tag`, `adjust_score`, `fire_webhook`, `notify`, `post_to_slack`,
`post_to_teams`, and the two playbook actions:

| Action | Shape | Notes |
| --- | --- | --- |
| `add_note` | `{type, body}` | Writes onto the lead's shared note timeline. |
| `add_contact_point` | `{type, title, description?, kind?, priority?, due_in_days?}` | Appends a task to the lead's checklist. |

Both are **idempotent**: re-entering a stage will not add a second copy of the
same note, nor a second open task with the same title. `due_in_days` is counted
from the moment the rule fires, not a calendar date — one rule serves every lead
that reaches the stage, whenever each of them gets there. The task is left
**unassigned on purpose**, which routes it to whoever owns the lead and keeps it
following them through a reassignment. `body`, `title`, `description` and the
Slack/Teams `message_template` all accept the tokens `{{lead_name}}`,
`{{lead_email}}`, `{{lead_company}}` and `{{rule_name}}`.

## Departments

| Tool | Role | What it does |
| --- | --- | --- |
| `list-departments` | employee | List all departments in the organization with member counts and parent links. |
| `get-department` | employee | Get a single department with its manager, parent, direct children, and active members (org users + their underlying user record). |
| `create-department` ✍️ | manager | Create a department in the user's organization. |
| `assign-user-to-department` ✍️ | manager | Move an organization user into a department, or pass department_id=null to remove them from any department. |

## Employees (org membership — admin-gated)

| Tool | Role | What it does |
| --- | --- | --- |
| `list-employees` | employee | List organization employees: both current members (with role, status, and department) and pending invitations that haven't been accepted yet. |
| `create-employee` ✍️ | admin | Invite an employee to your organization, optionally assigning them to a department. |
| `update-employee` ✍️ | admin | Update an existing organization member: change their role, move them to a different department, and/or change their status. |
| `remove-employee` ✍️ | admin | Remove an employee from your organization, or cancel a pending invitation. |
| `bulk-import-employees` ✍️ | admin | Invite many employees at once (1–100 per call) — the bulk / spreadsheet import path. |

## Access Domains & Join Requests

| Tool | Role | What it does |
| --- | --- | --- |
| `list-access-domains` ✍️ | admin | List the organization's approved access domains with their DNS verification status and auto-join switch. |
| `list-join-requests` ✍️ | admin | List join requests for the organizationapproved access domains): users whose verified email matches one of the org's verified domains and who asked to join. |
| `decide-join-request` ✍️ | admin | Approve or reject a pending join requestapproved access domains). |

## Team Performance (Advanced User Management add-on)

| Tool | Role | What it does |
| --- | --- | --- |
| `get-employee-performance` | employee | Get one team member's performance scorecard (leads captured, scans, deals won/lost, win rate, revenue, avg deal size, pipeline value, card views/shares/saves, goal counts) over a time window. |
| `get-team-performance` | manager | Get the performance scorecard for your whole visible team — one row per member with leads captured, scans, deals won/lost, win rate, revenue, avg deal size, pipeline value, card views/shares/saves and. |
| `get-forecast` | manager | Weighted revenue forecast: open deals bucketed by expected close month, weighted by probability (deal probability, else the stage's default), grouped into commit / best case / pipeline categories. |
| `list-employee-goals` | employee | List employee performance goals with live progress (current value, target, percent, achieved, current period window). |
| `create-employee-goal` ✍️ | manager | Set a performance goal for a team member. |
| `update-employee-goal` ✍️ | manager | Update an existing employee goal's editable fields: target, display, ends_on, pipeline_stage_id, lead_scoring_rule_id, score_threshold, reward_text, notes, and status (set status=archived to archive t. |
| `delete-employee-goal` ✍️ | manager | Permanently delete an employee goal and its period history. |
| `list-employee-documents` | employee | List the documents exchanged with one team member (purchase orders, invoices, contracts, payslips,...), newest first, with each document's status (pending / approved / rejected), category, review not. |
| `add-employee-document` ✍️ | employee | Attach a file to a team member (payslip, contract, invoice, purchase order,...), stored in the organization's storage and counted against its quota — the same Documents panel as the web employee deta. |
| `review-employee-document` ✍️ | manager | Approve or reject a team member's document (typically one they self-uploaded, which lands as `pending`). |
| `get-comp-plan` | employee | Get a team member's compensation plan (base salary, non-recoverable draw, commission rates, quota, OTE, linked KPI-floor goals) plus a live summary: cumulative commission, draw absorption, payout on t. |
| `manage-comp-plan` ✍️ | admin | Create or update a team member's compensation plan, or end it. |
| `list-comp-statements` | employee | List a team member's monthly compensation statements: base + draw (guaranteed pay), commission accrued, cumulative commission, how much the draw has absorbed, payout on top and the monthly KPI-floor v. |

## Analytics

| Tool | Role | What it does |
| --- | --- | --- |
| `get-card-stats` | employee | Get view, share, and save statistics for a specific card. |
| `get-dashboard-summary` | employee | Get a high-level dashboard summary for the authenticated user. |

## Dashboards (Analytics add-on)

| Tool | Role | What it does |
| --- | --- | --- |
| `list-dashboards` | employee | List the organization's chart-widget dashboards (id, name, default flag, widget layout). |
| `get-dashboard-data` | employee | Compute every widget's dataset for one dashboard (from list-dashboards). |

## File Library

| Tool | Role | What it does |
| --- | --- | --- |
| `list-library-files` ✍️ | employee | Browse the organization's shared file library ("Files") — sales decks, price sheets, one-pagers, onboarding docs and other reusable collateral, organized into folders. |

## Profile

| Tool | Role | What it does |
| --- | --- | --- |
| `get-profile` | employee | Get the authenticated user's profile information including name, email, username, plan details, and organization membership. |
| `who-am-i` | employee | Quick check of the authenticated user's identity and capabilities. |

## Resources & prompts

Beyond tools, the server exposes **schema resources** (card, lead, contact) so
your client can understand object shapes, and a **`LynquOverview`** prompt that
primes the assistant with how Lynqu works.

## Conventions worth remembering

- **`organization_user_id` vs `user_id`**: campaign membership and department
  assignment take the membership join-row id; lead assignment takes the
  underlying user id. `list-team-members` returns both.
- **Bulk cap**: `bulk-update-leads` handles ≤ 100 leads per call.
- **Validated transitions**: campaign status and event lifecycle changes are
  validated and audit-logged server-side.

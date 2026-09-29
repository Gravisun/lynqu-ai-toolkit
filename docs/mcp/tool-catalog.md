# Lynqu MCP tool catalog

The complete set of tools the hosted Lynqu MCP servers expose, mirrored from the
server's registered tools. When in doubt, ask the server itself: the
**`how-can-you-help-me`** tool classifies your goal and returns the exact tool
calls to run, and **`explain-feature`** says what any Lynqu feature is and
whether you can use it.

- **Organization server** (`/mcp/v2`): all categories below, **163 tools**.
- **Personal server** (`/mcp/me`): 10 user-scoped tools, no role gate:
  `how-can-you-help-me`, `explain-feature`, `list-cards`, `get-card`, `create-card`, `update-card`, `get-card-stats`, `get-dashboard-summary`, `get-profile`, `who-am-i`.

A ✍️ marks tools that **write** (create, update, delete or send). The **Role**
column says who can run a tool in an organization that has not customized its
roles:

- `employee`, `manager`, `admin`: the minimum role.
- A role followed by a capability key, such as `manager · leads.manage`: the
  tool checks that capability, and that role holds it by default. On Enterprise,
  a custom role can be granted the capability or have it taken away.
- `admin only`: a hard floor (billing, audit log, integrations, access domains,
  compensation) that no custom role can reach.

Per-record rules apply on top: you can only edit a lead you are allowed to edit,
and some tools widen or narrow by parameter, which the description says.
Add-on-gated tools are labelled; calling one without the add-on returns an
`ADDON_REQUIRED` error naming the add-on key.

> Your own permissions still apply on top of everything here. The assistant can
> never see or do more than you can in the app, and an org admin can restrict
> which roles may use the assistant at all, or make it read-only.

## Meta

| Tool | Role | What it does |
| --- | --- | --- |
| `how-can-you-help-me` | employee | Describe a business situation in plain language and get a matched workflow plus the concrete tool calls to run. |
| `explain-feature` | employee | What a Lynqu feature is, where it lives, which plan includes it and whether you can use it. Product knowledge, not workspace data: call it before telling anyone Lynqu lacks something. Also on the personal server. |

## Discovery

| Tool | Role | What it does |
| --- | --- | --- |
| `get-org-summary` | employee | One-shot overview: org info, team size by role, departments, active campaigns and events, pipelines, and leads per stage on the default pipeline. |
| `list-team-members` | employee | Members with role, department, status and assigned-lead counts. Returns both `organization_user_id` and `user_id`. |

## Cards

| Tool | Role | What it does |
| --- | --- | --- |
| `list-cards` | employee | List your own digital business cards. |
| `list-org-cards` | employee | The organization's card inventory, as on /org/cards. Admins see every card, managers their departments' cards, employees their own. Template cards need `cards.manage`. |
| `get-card` | employee | Full detail for one of your cards, by id or slug. |
| `create-card` ✍️ | employee | Create a card for yourself. It starts as a draft with a permanent slug. |
| `update-card` ✍️ | employee | Update fields on a card you own. Slugs never change, and fields your org locks are refused. |

## Contacts

| Tool | Role | What it does |
| --- | --- | --- |
| `list-contacts` | employee | The shared address book, with each person's identity links (`social_links`) and enrichment state. |
| `search-contacts` | employee | Search contacts by name, email, phone or company. |
| `get-contact` | employee | One contact's full record, plus how many leads and deals they are on. |
| `create-contact` ✍️ | employee | Add a person to the shared roster. Creates no lead; search first so you do not add a duplicate. |
| `update-contact` ✍️ | employee | Update a contact. Only the fields you pass change, and leads built from the contact are separate records that stay as they are. |
| `delete-contact` ✍️ | manager · `leads.manage` | Archive a contact. Leads it was the main contact for keep the link. Contacts are shared, so confirm with the user first. |

## Leads

| Tool | Role | What it does |
| --- | --- | --- |
| `list-leads` | employee | List leads, filtered by stage, status, temperature, owner or capture date (`created_from` / `created_to`). |
| `get-lead` | employee | Full lead detail: stage, owner, campaign and event, the notes timeline, tasks (`contact_points`), participants, recent activity and the score breakdown. |
| `create-lead` ✍️ | employee | Create a lead (first name required), optionally in a given pipeline and stage. |
| `update-lead` ✍️ | employee | Update a lead's own fields: contact details, company, value, currency, tags, custom fields. `follow_ups_paused: true` pauses automated follow-up sequences for this one lead and cancels its scheduled steps; `agents_paused` does the same for AI employees. Stage, owner and campaign have their own tools. |
| `delete-lead` ✍️ | manager · `leads.manage` | Soft-delete a lead with its notes, tasks, documents and activity; only an admin can restore it. A lost deal belongs in a losing stage, and a duplicate belongs in `merge-leads`. Confirm with the user first. |
| `manage-lead-participant` ✍️ | employee | Add, update or remove someone on a lead's buying committee (max 15). Marking someone primary makes them the lead's roster contact. |
| `add-lead-note` ✍️ | employee | Add a note to a lead's timeline, authored by you. |
| `update-lead-note` ✍️ | employee | Reword a note: your own, or anyone's as an admin or as a manager over the author's department. Voice notes cannot be reworded. |
| `delete-lead-note` ✍️ | employee | Delete a note, under the same rule as `update-lead-note`. A voice note takes its audio with it. |
| `list-lead-documents` | employee | Files attached to a lead, with short-lived download links and the storage meter. |
| `add-lead-document` ✍️ | employee | Attach a file (PDF, Markdown, Office, CSV or text, max 25 MB) as base64. Anyone who can view the lead may attach. |
| `delete-lead-document` ✍️ | employee | Delete a lead's file and free its storage: your own uploads, or anyone's if you can edit the lead. No undo. |
| `list-lead-contact-points` | employee | List tasks: one lead's checklist, or without `lead_id` the org-level "My tasks" view with due, status and priority filters. `scope` member or all needs manager or admin. |
| `add-lead-contact-point` ✍️ | employee | Add a task (a planned touch) with optional priority, due date and assignee. Max 25 per lead. |
| `update-lead-contact-point` ✍️ | employee | Rename, reschedule, reassign or complete (`completed`) a task. |
| `delete-lead-contact-point` ✍️ | employee | Delete a task permanently. Mark it done instead when the history matters. |
| `assign-lead` ✍️ | manager · `leads.manage` | Assign a lead to a member by `user_id`, or pass null to unassign. |
| `update-lead-stage` ✍️ | employee | Move a lead to another stage, or mark it won, lost or archived. |
| `bulk-update-leads` ✍️ | employee | Apply one change to up to 100 leads: stage, temperature, status, tags or owner. Reassigning needs `leads.manage`. |
| `attach-leads-to-campaign` ✍️ | employee | Attach up to 100 leads to a campaign, or detach them with `campaign_id: null`. Without `campaigns.manage` you may attach only leads you own, to an active or paused campaign you are a member of; the rest are skipped and reported. |
| `list-lead-duplicates` | manager · `leads.manage` | Open duplicate lead pairs awaiting review, with child-record counts so you can pick the survivor. |
| `merge-leads` ✍️ | employee | Merge a duplicate pair (the winner takes the loser's notes, documents, tasks and activity; the loser is soft-deleted) or dismiss it. Needs edit rights on both leads. Cannot be undone. |
| `list-lead-views` | employee | Saved lead views visible to you: your own plus the team's shared ones, with their filter config. |

## Pipelines

| Tool | Role | What it does |
| --- | --- | --- |
| `list-lead-pipelines` | employee | Pipelines (kanban tabs) with stage and live lead counts. |
| `get-pipeline-stages` | employee | Stages, optionally for one pipeline, with win/loss markers and open-lead counts. |
| `create-lead-pipeline` ✍️ | manager · `leads.manage` | Create a pipeline. It stays empty until stages are added. |
| `create-pipeline-stage` ✍️ | manager · `leads.manage` | Create a stage in a pipeline. At most one win and one loss stage per pipeline. |
| `move-lead-pipeline` ✍️ | manager · `leads.manage` | Move a lead to another pipeline, into a given stage or the target's default stage. |

## Campaigns

| Tool | Role | What it does |
| --- | --- | --- |
| `list-campaigns` | employee | Campaigns filtered by status, running state or dates, with lead and member counts, budget and capture token. |
| `get-campaign` | employee | One campaign with goals, members, events, follow-up template binding, capture forms and totals. |
| `create-campaign` ✍️ | manager · `campaigns.manage` | Create a campaign (always as a draft) with its auto-generated `/c/{token}` capture URL. |
| `update-campaign` ✍️ | manager · `campaigns.manage` | Change a campaign's name, description, dates, budget or currency. Status has its own tool. |
| `update-campaign-status` ✍️ | manager · `campaigns.manage` | Move a campaign through its validated lifecycle: draft, active, paused, completed, cancelled, archived. |
| `add-campaign-member` ✍️ | manager · `campaigns.manage` | Add a member as owner or regular member, by `organization_user_id`. |
| `list-campaign-goals` | employee | A campaign's goals with live progress, pace and forecast. |
| `list-metric-catalogue` | employee | Every metric a goal can target, with capability flags. Includes the follow-up metrics `followups.sent.count`, `followups.reply_rate.percent` and `followups.meetings_booked.count`. |
| `create-campaign-goal` ✍️ | manager · `campaigns.manage` | Add a goal: a `metric_key` and a numeric `target`, under the same rules as the web form. |
| `update-campaign-goal` ✍️ | manager · `campaigns.manage` | Update a goal's editable fields. `metric_key` is fixed after creation. |
| `delete-campaign-goal` ✍️ | manager · `campaigns.manage` | Delete a goal and its progress tracking. Irreversible. |
| `manage-campaign-booking-service` ✍️ | employee | View or set the one booking service (duration and type) that sizes bookings taken through a campaign. Setting it needs edit rights on the campaign. |

## Events

| Tool | Role | What it does |
| --- | --- | --- |
| `list-events` | employee | Events with their lifecycle markers. Without `events.manage` you get only the events live right now (id, name, window), which is what tagging a scan needs. |
| `get-event` | admin · `events.manage` | Full event detail: campaign, capture form, follow-up template, lead count and lifecycle timestamps. |
| `create-event` ✍️ | admin · `events.manage` | Create an event as a draft; `is_open_ended` skips the date window. |
| `update-event-lifecycle` ✍️ | admin · `events.manage` | activate, close, archive (30-day purge grace) or restore an event. Invalid transitions are refused, and every change is audit-logged. |
| `link-event-to-campaign` ✍️ | admin · `events.manage` | Link an event to a campaign, or detach it with null. |
| `get-event-portfolio` | manager · `events.reports` | Events side by side: leads, won, win rate, pipeline and won value in the org currency, appointments, budget and ROI. |
| `issue-tickets` ✍️ | admin · `events.manage` | Issue entry tickets to leads. Idempotent per event and lead. Needs the Ticketing add-on. |
| `list-event-tickets` | admin · `events.manage` | Tickets for an event, with issued and checked-in counts per tier. Needs the Ticketing add-on. |

## Booking

| Tool | Role | What it does |
| --- | --- | --- |
| `list-booking-requests` | employee | Unclaimed booking requests from capture forms and events. An employee sees only the ones they may accept (`can_accept`). |
| `accept-booking-request` ✍️ | employee | Preview who can take a request, then commit it onto a free teammate's calendar. |
| `list-card-bookings` | employee | Bookings customers made on your cards, filterable by status and date. |
| `get-booking` | employee | One booking on your card, with the customer's answers to your booking form. |
| `manage-appointment` ✍️ | employee | approve, reject, complete, no_show or cancel one of your appointments. |
| `reschedule-booking` ✍️ | employee | Move one of your bookings to a new start time. A slot another booking holds is never overridden. |
| `propose-booking` ✍️ | employee | Email a lead 1 to 3 open times from your booking card; each slot is held until they answer. |
| `get-meeting-brief` | employee | The AI pre-meeting brief for an appointment linked to a lead, generated on first read. |
| `list-booking-services` | employee | The bookable services on one of your cards. |
| `manage-booking-service` ✍️ | employee | Create, update or delete a bookable service on a card you own. |
| `manage-booking-settings` ✍️ | employee | Read, enable, disable or update the booking setup on a card you own. |
| `get-booking-report` | manager · `analytics.view` | Org-wide booking performance over a window, with the previous period for comparison. Needs the Analytics add-on. |
| `list-booking-pools` | manager · `booking.manage` | Team booking pools with strategy, state and member counts. Needs the Advanced Booking add-on. |
| `get-booking-pool` | manager · `booking.manage` | One pool's settings, roster and services. Needs the Advanced Booking add-on. |
| `create-booking-pool` ✍️ | manager · `booking.manage` | Create a team booking pool (it starts disabled). Needs the Advanced Booking add-on. |

## Companies

| Tool | Role | What it does |
| --- | --- | --- |
| `list-companies` | employee | Companies with domain, industry, owner, lead and contact counts and open deals. |
| `get-company` | employee | One company with parent and subsidiaries, custom fields, the deal roll-up and recent leads. |
| `create-company` ✍️ | manager · `companies.manage` | Create a company. Refused when one already exists on the same domain or name, unless `allow_duplicate` is set. |
| `update-company` ✍️ | manager · `companies.manage` | Update a company's profile fields. |
| `delete-company` ✍️ | manager · `companies.manage` | Delete a company. Its leads, contacts and deals survive and just lose the link. For two records of the same account, use `merge-companies`. Confirm with the user first. |
| `merge-companies` ✍️ | manager · `companies.manage` | With no arguments, list duplicate company pairs. With `winner_id` and `loser_id`, move the loser's leads, contacts and deals to the winner and remove the loser. Cannot be undone here; list again before every merge. |

## Deals, Line Items & Quotes

| Tool | Role | What it does |
| --- | --- | --- |
| `list-opportunities` | employee | Deals that carry a signal (untouched primaries are skipped), filtered by status, company or owner. |
| `get-opportunity` | employee | One deal: stage, status, value, forecast fields, custom fields, company and lead. |
| `create-opportunity` ✍️ | employee | Add a renewal or upsell deal to an existing lead. The person keeps one lead row. |
| `update-opportunity` ✍️ | employee | Update a deal's name, type, probability, close date, forecast category or custom fields. Value comes from the line items. |
| `move-opportunity-stage` ✍️ | employee | Move a secondary deal, optionally into another pipeline. A primary deal moves with `update-lead-stage`. |
| `delete-opportunity` ✍️ | employee | Delete a secondary deal you may edit. A primary deal cannot be deleted: close it with a stage move, or delete the lead. |
| `manage-deal-line-item` ✍️ | employee | Add, change or remove a priced line, from the price book or free-form. The deal's value is recomputed. |
| `list-quotes` | employee | Quotes with status, totals and version chain. |
| `get-quote` | employee | One quote line by line, with totals, terms and versions. |
| `manage-quote` ✍️ | employee | Create, edit or delete a DRAFT quote. Sending, accepting, declining and revising stay in the app. |

## Price Book

| Tool | Role | What it does |
| --- | --- | --- |
| `list-catalog-items` | employee | Browse the price book: name, SKU, price, currency, unit. |
| `manage-catalog-item` ✍️ | admin · `crm.configure` | Create, update or delete a price-book item. Deletes are soft and never rewrite a sent quote. |

## Follow-ups & Outbox

| Tool | Role | What it does |
| --- | --- | --- |
| `list-followup-templates` | employee | Templates you can see: team templates, your personal ones and AI employees' proposals, with owner, lock and override fields. `scope`: all, team, mine, or `member:{id}` for a teammate you may view. |
| `create-followup-template` ✍️ | employee | Create a template. `scope: mine` (any member, unless an admin switched personal templates off) is used only on your own leads; with `overrides_template_id` it replaces that team template on your leads unless the team one is locked. `scope: team` needs `follow_ups.manage`. |
| `send-followup-now` ✍️ | employee | Send one template to one lead you can edit. Only team templates and your own personal ones are accepted, never an AI proposal. The server can still cancel the send at dispatch (opt-out, a recent reply, a booked meeting, a closed or paused lead). The same lead and template are refused within 10 minutes. |
| `get-followup-performance` | employee | Sent, delivered, opened, clicked, replied, booked and won, with rates, grouped by template, sequence, step, member or AI employee. Reply rate ranks a row once it has 20 delivered; `replies_tracked: false` means replies are not being collected. `scope` is `me` by default; team and member need manager or admin. |
| `list-outbox` | employee | Emails the org sent (follow-ups, ticket, booking and quote mail) with delivery status and engagement, plus the replies that came back (`source: reply`). `scope` is `mine` by default; member, all, agents and agent need manager or admin. No message bodies. |

## Capture Forms

| Tool | Role | What it does |
| --- | --- | --- |
| `list-capture-forms` | employee | Capture forms with their public `/c/{token}` URL and field schema. |
| `get-capture-form-stats` | employee | A form's funnel (views, submissions, conversion, 30-day series) and its leads by outcome. |

## Lead Scoring

| Tool | Role | What it does |
| --- | --- | --- |
| `list-lead-scoring-rules` | admin · `lead_scoring.manage` | Scoring rules with predicate, points, priority, enabled flag and optional promotion target. |
| `create-lead-scoring-rule` ✍️ | admin · `lead_scoring.manage` | Create a rule: a sandboxed boolean `predicate` that adds `points` when true, with optional promotion to a stage at a `threshold`. |
| `update-lead-scoring-rule` ✍️ | admin · `lead_scoring.manage` | Update any field of a rule; `enabled: false` pauses it. |
| `delete-lead-scoring-rule` ✍️ | admin · `lead_scoring.manage` | Delete a rule permanently. |

## Enrichment

| Tool | Role | What it does |
| --- | --- | --- |
| `get-enrichment-quota` | employee | Read the personal or org enrichment quota without starting a job. |
| `start-enrichment` ✍️ | employee | Start an async enrichment job for a lead, contact, company or personal contact. Needs an AI-tier plan with quota left. |
| `get-enrichment-job` | employee | Poll a job. Read `contact_lookup` before reporting success. |
| `confirm-enrichment` ✍️ | employee | Apply the chosen fields (fill-empty-only), or resolve a disambiguation. |

## Automation (Workflow Automation add-on)

| Tool | Role | What it does |
| --- | --- | --- |
| `list-automation-rules` | manager · `automation.manage` | Rules with trigger, condition, actions, enabled/paused state and fire counts. |
| `create-automation-rule` ✍️ | manager · `automation.manage` | Create a rule: a trigger, 1 to 5 ordered actions, an optional delay, predicate and pipeline scope. |
| `update-automation-rule` ✍️ | manager · `automation.manage` | Change the name, predicate, delay, actions (full replacement), enabled or paused state. The trigger is fixed. |
| `delete-automation-rule` ✍️ | manager · `automation.manage` | Delete a rule. Queued runs are skipped; history is kept. |
| `list-automation-rule-runs` | manager · `automation.manage` | Recent runs with per-action outcomes, and a skip reason for every run that did not act. |

A rule is a **trigger** plus 1 to 5 ordered **actions**, after an optional delay.

**Triggers** (condition in brackets): `lead_created`, `stage_changed` (stage),
`score_crossed` (threshold and direction), `booking_no_show`, `lead_inactive`
(days), `ticket_checked_in`, `lead_assigned` (person or department),
`tag_added` (tag), `field_changed` (field), `email_opened`, `email_clicked`
(link host), `email_replied` (human replies by default), `booking_requested`,
`booking_confirmed`, `booking_cancelled`, `booking_rescheduled`,
`task_overdue`, `task_completed` (priority), `opportunity_won`,
`opportunity_lost` (minimum value), `handoff_opened` (AI employee role).

**Actions**: `send_template`, `assign` (a person, or round-robin across a
department), `move_stage`, `move_pipeline`, `add_tag`, `remove_tag`,
`unassign`, `adjust_score`, `set_temperature`, `add_to_campaign`,
`create_opportunity`, `propose_booking`, `start_enrichment`, `hand_to_agent`,
`crm_push`, `fire_webhook`, `notify`, `post_to_slack`, `post_to_teams`, and
the two playbook actions:

| Action | Shape | Notes |
| --- | --- | --- |
| `add_note` | `{type, body}` | Writes onto the lead's shared note timeline. |
| `add_contact_point` | `{type, title, description?, kind?, priority?, due_in_days?}` | Appends a task to the lead's checklist. |

Both are **idempotent**: re-entering a stage will not add a second copy of the
same note, nor a second open task with the same title. `due_in_days` is counted
from the moment the rule fires, not a calendar date: one rule serves every lead
that reaches the stage, whenever each of them gets there. The task is left
**unassigned on purpose**, which routes it to whoever owns the lead and keeps it
following them through a reassignment.

Text fields (`body`, `title`, `description`, the Slack and Teams
`message_template`) accept the follow-up tokens (`{{lead.first_name}}`,
`{{lead.company}}`, `{{employee.name}}` for the lead's owner, `{{org.name}}`,
`{{campaign.name}}`) and the older `{{lead_name}}`, `{{lead_email}}`,
`{{lead_company}}` and `{{rule_name}}`. An action that cannot act (Slack not
connected, nobody to notify, no open booking slot) is recorded as skipped with a
reason, never as done. Rules never trigger other rules.

## AI Employees

| Tool | Role | What it does |
| --- | --- | --- |
| `list-agents` | employee | AI employees in the org: role, status, whether each is still in its shadow (observe-only) trial, current work, and 30-day conversations and handoffs. You see the agents that acted inside your scope; admins see all. |
| `get-agent-timeline` | employee | One agent's actions, newest first: tool, risk tier, matched rule, its rationale, status (executed, awaiting approval, blocked, rejected) and undo state. Only actions about records you can access; raw arguments are admin-only. |
| `decide-agent-approval` ✍️ | admin · `agents.manage` | Approve (executes now) or reject (with a reason code) ONE parked agent action. No batch form; editing an action before approving happens in the app. |
| `list-handoffs` | employee | Work AI employees handed back to people, with the reason and the brief they wrote. `scope` is `mine` by default; member and all need manager or admin. Picking up and resolving happen in the app. |
| `get-sales-brief` | employee | The org's confirmed sales brief the AI employees write from: audience, offer, fit profile, booking link, current offer and sign-off. `status` is `none` until an admin confirms one, and `stale` when the website or industry changed since. |

## Departments

| Tool | Role | What it does |
| --- | --- | --- |
| `list-departments` | employee | Departments with member counts and parent links, flat or as a tree. |
| `get-department` | employee | One department with its manager, parent, children and active members. |
| `create-department` ✍️ | admin · `departments.manage` | Create a department, optionally nested and with a manager. |
| `manage-department` ✍️ | admin · `departments.manage` | Update or delete a department. Members are kept without a department; child departments are re-parented, which changes who sees whose leads. Confirm with the user first. |
| `assign-user-to-department` ✍️ | admin · `departments.manage` | Move a member (by `organization_user_id`) into a department, or out of any with null. |

## Employees

| Tool | Role | What it does |
| --- | --- | --- |
| `list-employees` | employee | Members and pending invitations, with `organization_user_id`, `user_id` and `invitation_id`. |
| `create-employee` ✍️ | admin · `members.admin` | Invite one person with a role and an optional department. |
| `update-employee` ✍️ | admin · `members.admin` | Change a member's role, department or status. Refuses to change yourself, the owner or the last admin. |
| `remove-employee` ✍️ | admin · `members.admin` | Remove a member or cancel an invitation. Never yourself, the owner or the last admin. |
| `bulk-import-employees` ✍️ | admin · `members.admin` | Invite 1 to 100 people from a spreadsheet; each row succeeds or fails on its own. |

## Access Domains & Join Requests

| Tool | Role | What it does |
| --- | --- | --- |
| `list-access-domains` | admin only | Approved access domains with DNS verification and the auto-join switch. |
| `list-join-requests` | admin · `members.admin` | Join requests from people on a verified domain; pending by default. |
| `decide-join-request` ✍️ | admin · `members.admin` | Approve (uses a seat) or reject a join request. The requester is told either way. |

## Team Performance (Advanced User Management add-on)

| Tool | Role | What it does |
| --- | --- | --- |
| `get-employee-performance` | employee | One member's scorecard over a window. Employees see themselves, managers their departments, admins anyone. |
| `get-team-performance` | manager · `performance.team` | The scorecard for your whole visible team, one row per member. |
| `list-employee-goals` | employee | Goals with live progress, scoped like the scorecards. |
| `create-employee-goal` ✍️ | manager · `performance.team` | Set a goal for a member in your scope. |
| `update-employee-goal` ✍️ | manager · `performance.team` | Update a goal's editable fields, or archive it. |
| `delete-employee-goal` ✍️ | manager · `performance.team` | Delete a goal and its history. Archive it instead to keep the history. |
| `list-employee-documents` | employee | Documents exchanged with a member: your own, or your departments' as a manager. |
| `add-employee-document` ✍️ | employee | Attach a file to a member (max 25 MB). Your own upload lands as pending; a manager's lands as approved. |
| `review-employee-document` ✍️ | manager · `performance.team` | Approve or reject a member's document. They are notified. |
| `get-comp-plan` | employee | A compensation plan with its live commission summary. Your own, or anyone's as an admin. |
| `manage-comp-plan` ✍️ | admin only | Save or end a compensation plan. Rates are in basis points. |
| `list-comp-statements` | employee | Monthly compensation statements. Your own, or anyone's as an admin. |

## Analytics

| Tool | Role | What it does |
| --- | --- | --- |
| `get-card-stats` | employee | Views, shares and saves for one card, daily, over the last 30 days by default. |
| `get-dashboard-summary` | employee | Your headline numbers: cards, views, shares, saves, network size and org lead stats. |
| `get-forecast` | manager · `analytics.view` | Weighted forecast by expected close month and forecast category, in the org currency. |

## Dashboards (Analytics add-on)

| Tool | Role | What it does |
| --- | --- | --- |
| `list-dashboards` | employee | The org's chart-widget dashboards and their layouts. |
| `get-dashboard-data` | employee | Compute every widget's dataset for one dashboard, optionally over one window. |

## File Library

| Tool | Role | What it does |
| --- | --- | --- |
| `list-library-files` | employee | Browse the org's shared files (decks, price sheets, one-pagers) by folder or name. Filtered to what you may see. |

## NFC Devices

| Tool | Role | What it does |
| --- | --- | --- |
| `list-org-devices` | employee | The org's NFC cards, tags and fobs: holder, the card a tap shows, and tap count. Employees see the devices they hold; managers and admins see the fleet. |
| `assign-device` ✍️ | admin · `devices.manage` | Hand devices to a member and/or point them at a card, or return them to the pool with `user_id: null`. The tag itself is never rewritten. |

## Workspace & Settings

| Tool | Role | What it does |
| --- | --- | --- |
| `get-billing-summary` | admin only | Plan, tier, seats in use and active add-ons. No card details, invoices or payment ids. |
| `get-ai-settings` | admin · `agents.manage` | Whether the in-app assistant and MCP are on, which roles may connect, read-only state and AI credit left. Answers even on a lapsed plan, so it can explain why a surface is unavailable. |
| `list-integrations` | admin only | What the org is connected to and how healthy each connection is: CRM sync, Slack, Teams, MCP clients. Never returns secrets. |
| `list-audit-events` | admin only | Who did what and when, filterable by action, category, person or date. No before and after values. |
| `list-field-policies` | manager · `field_policies.manage` | The rules that hide or lock lead and contact fields for roles or departments. Use it to explain why someone cannot see a field. |
| `list-brand-assets` | employee · `branding.view` | Brand kits, email signatures and virtual backgrounds. Inactive ones show only to people who manage branding. |
| `list-studio-recipes` | manager · `studio.use` | Ready-made AI Studio setups (pipeline, templates, scoring, automation). Recommend one and point at /org/studio, where recipes are applied. |

## Profile

| Tool | Role | What it does |
| --- | --- | --- |
| `get-profile` | employee | Your profile: name, email, username, plan and org membership. |
| `who-am-i` | employee | Your identity, plan, card count and org role. The cheapest connection check. |

## Resources & prompts

Beyond tools, the server exposes **schema resources** (card, lead, contact) so
your client can understand object shapes, and a **`LynquOverview`** prompt that
primes the assistant with how Lynqu works.

## Conventions worth remembering

- **`organization_user_id` vs `user_id`**: campaign membership and department
  assignment take the membership join-row id; lead assignment takes the
  underlying user id. `list-team-members` returns both.
- **Bulk cap**: `bulk-update-leads` and `attach-leads-to-campaign` handle up to
  100 leads per call.
- **Validated transitions**: campaign status and event lifecycle changes are
  validated and audit-logged server-side.
- **Destructive tools say so.** `delete-*` and `merge-*` tools cannot be undone
  from the assistant. Skills in this repo always confirm with you before calling
  one.
- **Personal follow-ups.** A member's personal version of a team template or
  sequence replaces the team one on that member's own leads, unless an admin
  locked it. The substitution happens when an automated email is sent; a manual
  `send-followup-now` sends exactly the template you picked.
- **Replies.** When reply tracking is on, a human reply (not an auto-reply)
  stops the lead's scheduled automated follow-ups, lands on the lead's timeline
  and in `list-outbox`, and is forwarded to the person the email went out as.
  When tracking is off, reply counts read 0 without meaning nobody answered;
  `get-followup-performance` reports which through `replies_tracked`.
- **Things with no tool on purpose**: sending, accepting or declining a quote;
  validating a ticket at the door; running an AI Studio recipe; picking up a
  handoff; an AI employee's guardrail settings. Those stay in the app.

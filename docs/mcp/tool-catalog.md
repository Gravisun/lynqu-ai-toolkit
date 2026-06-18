# Lynqu MCP tool catalog

The complete set of tools the hosted Lynqu MCP server exposes. This mirrors the
server's registered tools — when in doubt, ask the server itself via the
**`how-can-you-help-me`** tool, which classifies your goal and returns the exact
tool calls to run.

- **Organization server** (`/mcp/v2`): all categories below — **55 tools**.
- **Personal server** (`/mcp/me`): Meta, Cards, Analytics, Profile only — **8 tools**.

A ✍️ marks tools that **write** (create/update/send). The **Role** column is the
minimum org role required (personal server has no role gate).

## Meta

| Tool | Role | What it does |
| --- | --- | --- |
| `how-can-you-help-me` | employee | Intent classifier — describe your goal in plain English; returns a recommended workflow and the concrete tool calls. **Start here when unsure.** |

## Discovery

| Tool | Role | What it does |
| --- | --- | --- |
| `get-org-summary` | employee | Fast snapshot of the organization. |
| `list-team-members` | employee | Team members with both `organization_user_id` and `user_id`. |

## Cards

| Tool | Role | What it does |
| --- | --- | --- |
| `list-cards` | employee | List cards. |
| `get-card` | employee | Get one card's full detail. |
| `create-card` ✍️ | employee | Create a digital business card. |
| `update-card` ✍️ | employee | Update a card's fields, links, template, palette. |

## Contacts

| Tool | Role | What it does |
| --- | --- | --- |
| `list-contacts` | employee | List the org's shared contacts. |
| `search-contacts` | employee | Search contacts by name/company/etc. |

## Leads

| Tool | Role | What it does |
| --- | --- | --- |
| `list-leads` | employee | List pipeline leads (filterable). |
| `get-lead` | employee | Full lead detail + activity timeline. |
| `create-lead` ✍️ | employee | Create a lead. |
| `add-lead-note` ✍️ | employee | Add a note to a lead's timeline. |
| `assign-lead` ✍️ | manager | Assign a lead to a team member (takes `user_id`). |
| `update-lead-stage` ✍️ | employee | Move a lead to a different pipeline stage. |
| `bulk-update-leads` ✍️ | employee | Update up to **100** leads in one call. |
| `attach-leads-to-campaign` ✍️ | employee | Attach leads to a campaign. |

## Campaigns

| Tool | Role | What it does |
| --- | --- | --- |
| `list-campaigns` | employee | List campaigns. |
| `get-campaign` | employee | Campaign detail (goals, members, capture URL). |
| `create-campaign` ✍️ | manager | Create a campaign (auto-mints a `/c/{token}` capture URL). |
| `update-campaign-status` ✍️ | manager | Transition status (validated — can't go archived → active directly). |
| `add-campaign-member` ✍️ | manager | Add a member (takes `organization_user_id`). |
| `list-campaign-goals` | employee | The 15+ available goal metric keys. |

## Events

| Tool | Role | What it does |
| --- | --- | --- |
| `list-events` | employee | List events. |
| `get-event` | employee | Event detail. |
| `create-event` ✍️ | manager | Create an event (via EventLifecycleService; audit-logged). |
| `update-event-lifecycle` ✍️ | manager | Move through `draft → active → archived`; close open-ended events. |
| `link-event-to-campaign` ✍️ | manager | Roll an event up to a campaign for attribution. |

## Pipeline / Lead Environments

| Tool | Role | What it does |
| --- | --- | --- |
| `list-lead-environments` | employee | List kanban tabs (environments). |
| `get-pipeline-stages` | employee | Stages within an environment. |
| `create-lead-environment` ✍️ | admin | Create a new kanban tab. |
| `create-pipeline-stage` ✍️ | admin | Add a stage/column (optional win/loss marker). |
| `move-lead-environment` ✍️ | manager | Move a lead to a different environment. |

## Departments

| Tool | Role | What it does |
| --- | --- | --- |
| `list-departments` | employee | List departments (org chart). |
| `get-department` | employee | Department detail. |
| `create-department` ✍️ | manager | Create a department (nestable via `parent_id`). |
| `assign-user-to-department` ✍️ | manager | Assign a member (takes `organization_user_id`). |

## Employees (org membership — admin-gated)

| Tool | Role | What it does |
| --- | --- | --- |
| `list-employees` | employee | List org members. |
| `create-employee` ✍️ | admin | Invite a member (appears pending until accepted). |
| `update-employee` ✍️ | admin | Update role / department / status. |
| `remove-employee` ✍️ | admin | Remove a member. |
| `bulk-import-employees` ✍️ | admin | Bulk-invite from a spreadsheet. |

## Follow-ups

| Tool | Role | What it does |
| --- | --- | --- |
| `list-followup-templates` | employee | List email follow-up templates. |
| `create-followup-template` ✍️ | manager | Create an HTML template with mustache tokens. |
| `send-followup-now` ✍️ | employee | Send a follow-up via the CAN-SPAM-compliant pipeline. |

## Capture Forms

| Tool | Role | What it does |
| --- | --- | --- |
| `list-capture-forms` | employee | List public capture forms. |
| `get-capture-form-stats` | employee | Submission stats for a form. |

## Analytics

| Tool | Role | What it does |
| --- | --- | --- |
| `get-card-stats` | employee | Views, scans, shares, saves, engagement for a card. |
| `get-dashboard-summary` | employee | Aggregated metrics across cards, leads, and team activity. |

## Profile

| Tool | Role | What it does |
| --- | --- | --- |
| `get-profile` | employee | The authenticated user's Lynqu profile. |
| `who-am-i` | employee | Current auth context (handy for debugging). |

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

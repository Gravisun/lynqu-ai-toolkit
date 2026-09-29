# Authentication & access

The Lynqu MCP server uses **OAuth 2.1 with PKCE** — the modern standard MCP
clients implement natively. You never paste a token. This page explains what
happens and what governs whether a tool call succeeds.

## The OAuth flow (what your client does)

1. **Discovery.** Your client fetches the protected-resource and
   authorization-server metadata from Lynqu:
   - `https://api.lynqu.com/.well-known/oauth-protected-resource`
   - `https://api.lynqu.com/.well-known/oauth-authorization-server`
2. **Registration.** If the client isn't registered yet, it registers
   dynamically (RFC 7591) at `https://api.lynqu.com/oauth/register`.
3. **Consent.** The client opens Lynqu's consent page
   (`https://lynqu.com/connect/authorize`). You sign in and approve access.
4. **Token.** Lynqu issues an authorization code; the client exchanges it
   (with its PKCE verifier) for a bearer token scoped `mcp:use`.
5. **Tool calls.** Every request to `/mcp/v2` or `/mcp/me` carries that bearer.
   Missing or invalid tokens return `401` with a `WWW-Authenticate` header
   pointing back at the discovery metadata, so the client knows to re-auth.

All of this is automatic. Your job is steps 3 — sign in and approve.

## What governs a successful tool call

Even with a valid token, a tool call passes through gates in this order:

### 1. Plan gate

Running a tool requires an **AI-tier plan**:

| Plan | Connect | Run tools |
| --- | --- | --- |
| Free / Pro | ✅ | ❌ (upgrade prompt) |
| Business (without the AI add-on) | ✅ | ❌ (upgrade prompt) |
| **Pro + AI** | ✅ | ✅ (personal scope) |
| **Business + AI** | ✅ | ✅ |
| **Enterprise** | ✅ | ✅ |

Connecting and listing tools is always allowed; the gate fires when you
*call* a tool. A member of an organization on Business + AI or Enterprise gets
access from the org's plan, whatever their personal plan is. Legacy Corporate
plans count as Enterprise.

### 2. Organization policy

For the org server (`/mcp/v2`), your organization admin controls an
`mcp_policy`:

- **enabled** — MCP can be turned off org-wide.
- **allowed_roles** — restrict MCP to specific roles.
- **read_only** — allow read tools but block writes.

An organization whose subscription lapsed into its grace period is read-only
too, until it renews. If a policy blocks you, the tool returns a clear error
explaining why.

### 3. Role and capability gate

Org roles rank `employee` (1) < `manager` (2) < `admin` (3). The org owner is an
implicit admin. Most tools check a named **capability**, the same one the
matching screen in the app checks, and each capability has a default minimum
role:

| Held by default from | Capabilities | Example tools |
| --- | --- | --- |
| **employee** | none needed | read tools, `create-lead`, `add-lead-note`, `update-lead-stage`, `send-followup-now`, a personal `create-followup-template` |
| **manager** | `leads.manage`, `campaigns.manage`, `companies.manage`, `booking.manage`, `automation.manage`, `performance.team`, `analytics.view`, `events.reports`, `field_policies.manage`, `studio.use` | `assign-lead`, `delete-lead`, `create-lead-pipeline`, `create-campaign`, `merge-companies`, `get-forecast` |
| **admin** | `events.manage`, `departments.manage`, `lead_scoring.manage`, `members.admin`, `crm.configure`, `agents.manage`, `devices.manage`, `follow_ups.manage` (team templates) | `create-event`, `manage-department`, `create-lead-scoring-rule`, `create-employee`, `manage-catalog-item`, `decide-agent-approval`, `assign-device` |

On **Enterprise**, custom roles can be granted a capability or have one taken
away, so a denial means "this role does not hold that capability", not
necessarily "you are not a manager". A few tools are **hard floors** that no
custom role can reach: `get-billing-summary`, `list-audit-events`,
`list-integrations`, `list-access-domains` and `manage-comp-plan` are admin
only.

The personal server (`/mcp/me`) has **no org or role gate**: every tool there
is scoped to you. A card owned by an organization that switched MCP off stays
out of reach there too.

`docs/mcp/tool-catalog.md` lists the default role and capability for every
tool.

### Stricter than role alone

Two things are gated beyond the role table:

- **Compensation.** `get-comp-plan` and `list-comp-statements` are admin **or
  the member themselves**; `manage-comp-plan` is admin **only**. This is one
  band tighter than the rest of team performance on purpose — a manager can see
  a rep's numbers but not their pay, and nobody sets their own.
- **Add-on-gated categories.** Some tools need a paid add-on regardless of
  role (team performance needs Advanced User Management, automation needs
  Workflow Automation, dashboards and the booking report need Analytics, team
  booking pools need Advanced Booking, event tickets need Ticketing). Calling
  one without it returns an `ADDON_REQUIRED` error naming the add-on key, so the
  assistant can point you at the right purchase page.
- **Scope parameters.** Several read tools default to your own records and
  widen only for a manager or admin: `list-outbox`, `get-followup-performance`,
  `list-handoffs` and the org-level task list in `list-lead-contact-points`.
- **AI employee approvals.** `decide-agent-approval` decides exactly one parked
  action per call. There is no batch form, and editing an action before
  approving it happens in the app.

### Actions with no tool at all

A few things are reachable in the app but deliberately have **no MCP tool**, so
no role unlocks them: sending, accepting or declining a quote; validating an
event ticket; running an AI Studio recipe; picking up or resolving an AI
employee's handoff; reading or changing an AI employee's guardrails. These
either reach a customer, change a real-world record or reshape how a team
works, and an assistant being talked into one is worse than the convenience is
worth. See the guardrails in `skills/lynqu-deal-desk/SKILL.md`.

## Security notes

- The toolkit in this repo never stores or transmits credentials. OAuth tokens
  live in your MCP client's secure storage.
- Tokens are scoped narrowly (`mcp:use`) and tied to your Lynqu account and its
  org membership and policy at call time — revoking access in Lynqu immediately
  stops tool calls.
- Treat the server URLs as public; treat your session as private.

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
| **Pro + AI** | ✅ | ✅ (personal scope) |
| **Business** | ✅ | ✅ |
| **Corporate** | ✅ | ✅ |

Connecting and listing tools is always allowed — the gate fires when you
*call* a tool.

### 2. Organization policy

For the org server (`/mcp/v2`), your organization admin controls an
`mcp_policy`:

- **enabled** — MCP can be turned off org-wide.
- **allowed_roles** — restrict MCP to specific roles.
- **read_only** — allow read tools but block writes.

If a policy blocks you, the tool returns a clear error explaining why.

### 3. Role gate

Org roles rank `employee` (1) < `manager` (2) < `admin` (3). The org owner is an
implicit admin. A tool runs only if your role meets its minimum:

| Minimum role | Example tools |
| --- | --- |
| **employee** (default) | list/read tools, `create-lead`, `add-lead-note`, `update-lead-stage`, `send-followup-now` |
| **manager** | `create-campaign`, `update-campaign-status`, `add-campaign-member`, `assign-lead`, `create-event`, `update-event-lifecycle`, `link-event-to-campaign`, `create-department`, `assign-user-to-department`, `create-followup-template`, `move-lead-environment` |
| **admin** | `create-lead-environment`, `create-pipeline-stage`, `create-employee`, `update-employee`, `remove-employee`, `bulk-import-employees` |

The personal server (`/mcp/me`) has **no org or role gate** — every tool there
is scoped to you.

## Security notes

- The toolkit in this repo never stores or transmits credentials. OAuth tokens
  live in your MCP client's secure storage.
- Tokens are scoped narrowly (`mcp:use`) and tied to your Lynqu account and its
  org membership and policy at call time — revoking access in Lynqu immediately
  stops tool calls.
- Treat the server URLs as public; treat your session as private.

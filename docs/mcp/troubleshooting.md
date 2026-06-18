# Troubleshooting

Most connection problems fall into a few buckets. Work top to bottom.

## "Couldn't connect" / the client can't find the server

- **Check the URL exactly.** Organization is `https://api.lynqu.com/mcp/v2`,
  personal is `https://api.lynqu.com/mcp/me`. The MCP lives at the **domain
  root** — not under an `/api` or `/v1` path. A URL like
  `https://api.lynqu.com/v1/mcp/v2` will 404.
- **Use `https://`.** The server only speaks HTTPS.
- **Pick the right server.** Org tools (leads, campaigns, events) only exist on
  `/mcp/v2`. If you connected to `/mcp/me` you'll only see card/profile tools.

## OAuth fails / "couldn't register" / stuck on the sign-in page

- Your client registers dynamically and then opens
  `https://lynqu.com/connect/authorize`. Make sure pop-ups / external browser
  launches aren't blocked.
- If sign-in succeeds but the client still says unauthorized, **remove the
  connector and re-add it** so it re-runs discovery and registration cleanly.
- Corporate networks sometimes block the `.well-known` discovery endpoints —
  try from an unrestricted network to isolate this.

## Tools appear but every call returns an upgrade prompt

You're connected on a plan without AI-tier access. **Connecting is free;
running tools needs Pro+AI, Business, or Corporate.** Upgrade in the Lynqu app,
then retry — no need to reconnect.

## A specific tool returns "not allowed" / "insufficient role"

- **Role gate.** Some tools need `manager` or `admin`. See the Role column in
  [`tool-catalog.md`](tool-catalog.md). Ask an admin to run it, or to raise your
  role.
- **Org policy.** Your admin may have set MCP to **read-only** or restricted it
  to certain roles. Write tools will be blocked under read-only.

## "Not an org member" on org tools

You're authenticated but not an **active** member of an organization. Either
accept your org invite, or use the personal server (`/mcp/me`) for your own
cards.

## Only some tools show up in my client

A few clients only read the first page of a paginated tool list. The Lynqu
server pins all tools onto a single page specifically to avoid this — if you
still see a truncated list, update your MCP client to a recent version.

## Wrong identifier errors on assignment

- `assign-lead` wants a **`user_id`**.
- `add-campaign-member` and `assign-user-to-department` want an
  **`organization_user_id`**.
- Call `list-team-members` first — it returns both ids for every member.

## Still stuck?

Open an issue with: your client + version, the exact server URL you entered, the
tool you called, and the verbatim error. Run `who-am-i` and include its output
(it's just your auth context — no secrets).

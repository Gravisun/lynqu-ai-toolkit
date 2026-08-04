---
name: lynqu-card-studio
description: Create and update Lynqu digital business cards — contact info, social links, services, template, palette — and check card views, scans and shares. Requires the Lynqu MCP server connected.
---

# Lynqu Card Studio

You build and maintain the surface people actually meet the company through. A
card is the top of the funnel: it's what gets scanned at a booth, tapped at a
dinner, and opened three weeks later when someone tries to remember who you were.
Everything else in this suite operates on leads that a card created.

Two things this skill does that a settings screen doesn't: it keeps a **team's**
cards consistent without flattening the people on them, and it reads engagement
as a signal — a card with 400 views and 2 saves has a problem worth naming.

## Invocation

```
/lynqu card [name | "my card" | "the sales team" | "how is my card doing"]
```

## Which server you're on matters

| Server | Scope | Use for |
|--------|-------|---------|
| **Personal** (`/mcp/me`) | Your own cards, your stats, your profile. No role gate | "My card", personal use, anyone without an org |
| **Organization** (`/mcp/v2`) | Org-managed cards across the team | Team rollout, brand consistency, org card stats |

If a user asks about "my card" and only the org server is connected, you can
still reach their own card through the org — but say which set you're looking at.
Confusion between a personal card and an org-managed one is the most common
source of "why did my edit disappear".

## Step 1: Read before you write

- **`who-am-i`** and **`get-profile`** — who this is, and their role
- **`list-cards`** (personal) or **`list-org-cards`** (org) — what already exists.
  People commonly have several: a primary card, an event card, a legacy one
- **`get-card`** — the full current state before editing. Never patch a card you
  haven't read; you'll wipe a section someone else set

Show the user what exists before changing anything. "You have three cards, this
one is your primary" prevents editing the wrong one.

## Step 2: Build or update

**`create-card`** for a new one, **`update-card`** to change an existing one.

What makes a card work, roughly in order of impact:

| Element | The bar |
|---------|---------|
| **Name and title** | The title people would search for, not the internal one. "VP Field Sales" beats "Commercial Lead II" |
| **Photo** | A real face. Cards without one get saved noticeably less |
| **One-line description** | What you do *for whom*. Not a slogan |
| **Contact methods** | The ones you actually answer. A phone number you ignore is worse than no phone number |
| **Social / links** | Two or three that are current. A dead link is a credibility leak |
| **Services** | What you can help with — this is what makes a card useful weeks later |
| **Template and palette** | Consistent with the brand, readable at arm's length on a phone in bad lighting |

Confirm before overwriting anything populated. Cards carry personal information
people care about, and an unasked-for edit to someone's title lands badly.

## Step 3: Team rollout (org server)

For a team, the tension is consistency versus authenticity. Get it wrong in
either direction and the cards stop working: identical cards feel corporate and
get saved less; unconstrained cards make the company look like eight companies.

- Hold **template, palette and company-level links** consistent
- Keep **photo, title, personal line and direct contact** individual
- **`list-org-cards`** to audit — find the missing photos, stale titles, dead
  links and people who never finished setup
- Report the audit as a list the manager can act on. Don't mass-edit people's
  personal fields without their say-so; that's a real trust boundary and it's
  worth being explicit about

## Step 4: Read the engagement

**`get-card-stats`** — views, scans, shares, saves. And **`get-dashboard-summary`**
for how card activity feeds the wider funnel.

Read the *ratios*, not the totals:

| Pattern | What it means | What to do |
|---------|---------------|------------|
| High views, low saves | The card is seen but not worth keeping | Sharpen the description and services; add a reason to save |
| High scans, low views | QR is working, the card isn't loading well | Check the card is published and renders on mobile |
| Spike with no leads | Traffic isn't being captured | Wire a capture form or a booking link |
| Flat everything | The card isn't in circulation | This is a distribution problem, not a card problem |

The most useful sentence this skill produces is usually about the gap between
attention and conversion — a card getting attention that produces nothing is a
plumbing problem, and naming it is the value.

## Step 5: Connect it to the pipeline

A card that generates interest and captures nothing is a wasted surface.

- **Booking** — a booking link on the card turns interest into a meeting while
  the person is still holding their phone. `list-booking-services` and
  `manage-booking-settings` set it up
- **Capture** — `list-capture-forms` for events, so a scan becomes a lead
- **Attribution** — cards used at an event should feed that event's campaign, or
  the ROI question is unanswerable later

## Output format

```markdown
# Card — {name}

**{n} cards · primary: {name} · server: {personal | organization}**

## Current
| Field | Value | Status |
|-------|-------|--------|
| Title / Photo / Description / Links / Services | … | ✓ or **missing** |

## Changed
| Field | From | To |

## Engagement — {period}
| Views | Scans | Shares | Saves | Save rate |
{One sentence on what the ratio says.}

## Team audit (org)
| Person | Missing | Stale |

## Suggested
1. {Specific improvement, and why it matters}
```

## Rules and constraints

- **Read the card before updating it.** Blind patches wipe sections.
- **Confirm before overwriting populated fields**, always.
- **Never edit someone else's personal fields** (photo, title, direct contact)
  without explicit instruction. Template and brand elements are fair game for a
  manager; personal ones aren't.
- **Never invent contact details or links.** A dead or wrong link on a card is
  seen by customers.
- **Say which server you're on** when it could be ambiguous.
- **Report ratios, not just totals.** 400 views means nothing on its own.
- **Don't recommend a redesign when the problem is distribution.** A beautiful
  card nobody scans has a different problem.

## Error handling

- **Multiple cards, unclear which** → list them with their status and ask. Editing
  the wrong card is invisible until someone complains.
- **Card not found** → it may be on the other server (personal vs org), or belong
  to someone else. Say which set you searched.
- **Update denied on an org-managed card** → some fields are locked by the org's
  brand kit. Report which, and who can change them — this is a policy, not a bug.
- **Stats empty** → the card may be new, unpublished, or never shared. Check
  published state before drawing conclusions from zeros.
- **Personal server only, org features requested** → team rollout and org card
  stats need `/mcp/v2`. Say so and point at the connection docs.
- **Draft or deactivated card** → say so. A card that isn't live explains every
  zero in the stats and should be the first thing fixed.

## Cross-skill integration

- Card scans at an event → `lynqu-event-blitz` for the attribution setup
- Scans that should become leads → `lynqu-lead-capture`
- A booking link on the card → meetings land in `lynqu-prep`
- Card engagement as a funnel metric → `lynqu-pipeline-report`
- New team member → set up their card here, then `lynqu-lead-management` for
  their territory

## Example

> "/lynqu card — how is my card actually doing?"

The run: finds three cards, identifies the primary · pulls stats: 412 views, 380
scans, 11 saves over 90 days · names the problem plainly — *"people are scanning
it and looking, then not keeping it. That's a content gap, not a distribution
one"* · notes the card has no services listed and a one-line description that says
"Sales at Gravisun", which gives nobody a reason to save it · suggests three
specific changes and a booking link so interest converts on the spot · and points
out that 380 scans over 90 days with no capture form wired is the larger miss.

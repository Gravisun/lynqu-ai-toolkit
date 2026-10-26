# Changelog

All notable changes to the Lynqu AI Toolkit are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.5.0] - 2026-10-26

### Added
- **Eight tools the server gained since 1.4.0** (organization 163 → **171**):
  - Segments: `list-segments`, `create-segment`, `update-segment`,
    `delete-segment` and `get-segment-performance` (a named lead filter that
    is a list filter, a sequence or automation audience and a report row;
    reports count each lead in the first segment it matches, so rows add up).
  - Sequences: `create-followup-trigger` and `update-followup-trigger` (fire
    on a stage, a score or a predicate; up to five timed steps; cooldown; event
    or segment scope; team or personal; an enabled one needs the org's postal
    address). Pausing, resuming and deleting stay in the app.
  - Events: `attach-leads-to-event`, for scans made without the event picked.
    Attaching runs the event's sequences, and the skills say so before calling
    it.
- A **Segments** catalog section, and `docs/concepts.md` sections on segments
  and on what a sequence can do.
- **ChatGPT and Codex in the Quick start.** The README now lists the connect
  steps per client (Claude, ChatGPT in Developer mode, the Codex app and CLI,
  Cursor and VS Code); `connect.md` has the current ChatGPT flow
  (chatgpt.com/plugins → Add custom MCP server, OAuth) and a Codex section;
  `troubleshooting.md` explains the Codex-only "Couldn't connect" (it needs the
  issuer-bound callbacks Lynqu now advertises).
- Prompt library entries for segments, sequences, event attribution and voice.

### Changed
- **Every draft, note and task title is written for a person to read.** The
  skills carry a shared voice rule: short (a first touch is 40 to 70 words, a
  recap 60 to 90, a nurture touch 30 to 50, a note three lines), plain, one
  specific detail, one ask, nothing a template would say. `lynqu-outreach` and
  `lynqu-sales-followup` have a Voice section and shorter length tables, and
  the output templates across the suite lost their filler.
- **No em dashes anywhere** in the toolkit (481 removed across 33 files, and
  `scripts/validate_skills.py` now fails on a new one),
  following Lynqu's copy voice. The validator and the issue templates included.
- `lynqu-sales-followup` builds sequences (`create-followup-trigger`) and reads
  saved segments; `lynqu-outreach` can turn an approved sequence into a trigger
  scoped to a segment or an event; `lynqu-lead-management` defines segments
  and attaches orphan scans to their event; `lynqu-event-blitz` drafts the
  post-event sequence before the show and attributes with both attach tools;
  `lynqu-pipeline-report` reports segment performance with its 20-decided-deals
  floor; `lynqu-icp` encodes the profile and anti-profile as segments;
  `lynqu-sales-playbook` prefers a sequence over twenty templated tasks.
- Bulk cap notes now name `attach-leads-to-event` beside the other two.

[1.5.0]: https://github.com/Gravisun/lynqu-ai-toolkit/releases/tag/v1.5.0

## [1.4.0] - 2026-09-29

### Added
- **28 tools were missing from the catalog** (organization 136 → **163**,
  personal 9 → **10**), regenerated from the server's tool classes and
  checked against its registered list:
  - Follow-ups: `get-followup-performance` (sent, delivered, opened, clicked,
    replied, booked and won by template, sequence, step, rep or AI employee)
    and `list-outbox` (what went out, and the replies that came back).
  - AI employees: `list-agents`, `get-agent-timeline`, `decide-agent-approval`,
    `list-handoffs`, `get-sales-brief`.
  - Clean-up: `delete-lead`, `delete-contact`, `delete-company`,
    `delete-opportunity`, `delete-lead-note`, `delete-lead-document`,
    `update-lead-note`, `merge-companies`.
  - Workspace: `explain-feature` (on both servers), `get-billing-summary`,
    `get-ai-settings`, `list-integrations`, `list-audit-events`,
    `list-field-policies`, `list-brand-assets`, `list-studio-recipes`.
  - Also `update-campaign`, `manage-department`, `list-org-devices` and
    `assign-device`.
- New catalog sections: **AI Employees**, **NFC Devices**, **Workspace &
  Settings**, and **Follow-ups & Outbox**. The automation section lists all 21
  triggers and 21 actions (it listed 6 and 11).
- `docs/concepts.md` explains **personal follow-ups** (a member's version
  replaces the team text on their own leads unless an admin locked it),
  **replies and reply tracking**, **follow-up performance** (reply rate is the
  headline; nothing is ranked below 20 delivered emails), **AI employees and
  their approvals**, and the **sales brief**. The README gained a short section
  on the same, and the prompt library gained follow-up, reporting and AI
  employee examples.

### Changed
- **The Role column follows capabilities.** Most tools now check a named
  capability that Enterprise custom roles can grant or withhold, so every row
  shows the default role plus the capability key (`manager · leads.manage`),
  and `admin only` marks the hard floors. Defaults that moved: events are admin
  by default (they were manager), as are departments and lead scoring rules,
  reading the rules included; pipelines and stages dropped to manager (they
  were admin); `create-lead` is open to every member (it was manager); team
  follow-up templates need `follow_ups.manage` while personal ones are open to
  every member.
- **`lynqu-sales-followup`** and **`lynqu-outreach`** pick templates on
  evidence from `get-followup-performance`, honour the 20-delivered floor, say
  so when `replies_tracked` is false instead of reporting 0%, send only team
  templates or the user's own (never an AI proposal), check `list-outbox`
  afterwards because the server can still cancel a send, treat a reply as the
  end of the follow-up, and use `update-lead` `follow_ups_paused` to stop one
  lead's automated sequence.
- **`lynqu-lead-management`** deletes records that were never real
  (`delete-lead`), merges duplicate companies, and corrects or removes notes,
  each behind its own confirmation naming the record.
- **`lynqu-pipeline-report`** reports follow-up engagement from
  `get-followup-performance`, the outbox and open AI employee handoffs.
- **`lynqu`** answers product questions with `explain-feature` before saying
  Lynqu lacks something, handles AI employees itself (reads freely, decides
  approvals one action at a time with an explicit yes each), and states role
  gates in terms of capabilities.
- **`lynqu-deal-desk`** can remove a secondary deal that isn't real and merge an
  account split across two company records; **`lynqu-sales-playbook`** knows
  stage rules send team templates only; **`lynqu-event-blitz`** reflects the
  admin default on events and reads post-event follow-up performance by
  campaign; **`lynqu-lead-capture`** counts a `recaptured: true` answer from
  `create-lead` as a match; **`lynqu-qualify`**, **`lynqu-icp`**,
  **`lynqu-lead-research`** and **`lynqu-competitors`** reflect the new gates on
  scoring rules and templates.
- `scripts/validate_skills.py` now also checks tool references that start with
  `delete`, `merge`, `manage`, `decide`, `issue`, `confirm`, `start`, `review`,
  `propose`, `reschedule`, `accept` and `explain`, so a misspelled destructive
  tool fails CI like any other.

### Fixed
- **The plan gate was wrong everywhere.** Running tools needs Pro+AI,
  Business+AI or Enterprise; plain Business does not include the assistant.
  Fixed in the README, `concepts.md`, `connect.md`, `authentication.md` and
  `troubleshooting.md`.
- Seven read tools were marked as writes (`list-lead-contact-points`,
  `list-lead-views`, `list-automation-rules`, `list-automation-rule-runs`,
  `list-access-domains`, `list-join-requests`, `list-library-files`).
- Descriptions cut off mid-sentence (`get-lead`, `list-companies`,
  `create-company` and others) are whole sentences again.
- `get-forecast` sat under the Team Performance add-on; it needs none. Team
  booking pools were listed as open to every member with no add-on; they need
  `booking.manage` and Advanced Booking. The booking report needs Analytics.
- `update-contact` said deleting a contact had no tool; `delete-contact` exists.
- `concepts.md` still called pipelines "lead environments".

[1.4.0]: https://github.com/Gravisun/lynqu-ai-toolkit/releases/tag/v1.4.0

## [1.3.0] - 2026-08-05

### Added
- **`lynqu-sales-playbook`**: turns a written playbook (decision makers, an
  outreach sequence, meeting prep, a send order) into a live pipeline: leads and
  buying committees, the sequence as dated tasks, the playbook attached to each
  lead, and **stage rules that deliver the prep when the deal gets there**. The
  last part is what makes it a process rather than a one-time import. A rule
  hangs off the stage, so it also fires for leads created months later.
- **A worked doc set** in [`examples/playbooks/`](examples/playbooks): fully
  fictional, showing the input shape the skill reads.
- Two new automation actions in the catalog, `add_note` and
  `add_contact_point`, with their shapes and the three behaviours that decide
  whether the result is usable: both are idempotent, `due_in_days` is relative
  to the fire, and the task is deliberately left unassigned so it follows
  whoever owns the lead.

### Fixed
- **Seven tools were missing from the catalog** (129 → **136**), so a skill
  referencing any of them would have failed the validator and, worse, a model
  reading the catalog would have concluded they don't exist: `create-contact`,
  `get-contact`, `update-contact`, `manage-lead-participant`, `update-lead`,
  `update-opportunity`, `move-opportunity-stage`. The first four are the
  contacts-and-buying-committee surface the new skill is built on.

[1.3.0]: https://github.com/Gravisun/lynqu-ai-toolkit/releases/tag/v1.3.0

## [1.2.0] - 2026-08-04

### Added
- **`lynqu`: one command instead of fifteen.** Describe the situation ("we got
  back from SaaStr with 200 badges") and it composes a plan across whichever
  skills the situation needs, grounded in what the account already contains,
  confirming before every write and asking explicitly before any email.
- **Seven new skills**, giving the suite parity with a full sales motion:
  `lynqu-prospect` (single-account audit), `lynqu-qualify` (BANT + MEDDIC),
  `lynqu-contacts` (buying committee), `lynqu-icp` (built from your own wins
  *and* losses, encoded as scoring rules), `lynqu-competitors` (battlecards),
  `lynqu-outreach` (first-touch sequences), `lynqu-prep` (meeting briefs).

### Changed
- **Every skill rewritten to the same depth**: numbered steps, explicit output
  format, rules and constraints, error handling, and cross-skill routing.
- **Every skill now ends by writing to Lynqu**: a scored lead, a dated task, a
  note the next rep inherits. Analysis that stays in the chat window changes
  nothing; that is the difference between this and a generic sales assistant.
- Skill names may now be the bare `lynqu` (the orchestrator) as well as
  `lynqu-<name>`; the validator was widened to match.
- README leads with the plain-language entry point rather than the command list,
  and the install commands glob `lynqu*` so the orchestrator is included.
- Fixed a stale MCP tool badge (55+8 → 129+9) left over from v1.1.0.

## [1.1.2] - 2026-08-04

### Fixed
- v1.1.1 claimed claude.ai enforces a 200-character `description` limit and that
  this was why uploads failed. Anthropic documents a 1024-character maximum, so
  that cause was wrong. The real gap was a README that only ever explained the
  Claude Code install. 200 remains as a house limit, on its own merits.
- README said Claude Desktop reads `~/.claude/skills`. It doesn't. That path is
  Claude Code only; the desktop app is claude.ai and takes ZIP uploads.

[1.2.0]: https://github.com/Gravisun/lynqu-ai-toolkit/releases/tag/v1.2.0

[1.1.2]: https://github.com/Gravisun/lynqu-ai-toolkit/releases/tag/v1.1.2

## [1.1.1] - 2026-08-04

### Fixed
- **The README only ever explained the Claude Code install.** Anyone using
  claude.ai (web, the desktop app, or mobile) followed a `cp -r` into a folder
  that doesn't exist there, with no hint that skills are uploaded as ZIPs and
  that code execution has to be on first. The `~/.claude/skills` line also named
  Claude Desktop, which does not read that folder.
- All eight skill `description` fields shortened from 336–400 to 162–197
  characters. One also contained `": "`, which is invalid in an unquoted YAML
  scalar.
- Stale skill count in the README badge and skills intro (seven → eight).

### Added
- Ready-made per-skill ZIPs attached to the release, so installing on claude.ai
  needs no terminal.
- README install step for claude.ai (ZIP per skill, plan requirement, and the
  "Code execution and file creation" capability).
- `scripts/validate_skills.py` enforces a 200-character description budget.
  Anthropic documents 1024; ours is deliberately tighter, since the description
  is always in context and is what Claude matches requests against.

[1.1.1]: https://github.com/Gravisun/lynqu-ai-toolkit/releases/tag/v1.1.1

## [1.1.0] - 2026-08-03

### Fixed
- **Four skills referenced MCP tools that do not exist.** The pipeline tools are
  named `list-lead-pipelines` / `create-lead-pipeline` / `move-lead-pipeline`;
  the catalog and `lynqu-lead-capture`, `lynqu-lead-management`,
  `lynqu-event-blitz` and `lynqu-pipeline-report` all used an older
  `-environment` spelling, so those steps would have errored at call time.
  `scripts/validate_skills.py` catches this class of drift and now passes.

### Added
- `lynqu-deal-desk` skill: browse the price book, put priced lines on a deal,
  and draft the quote. Documents the two things that trip people up: deal value
  is the sum of its lines (never set directly), and a price-book item may only
  be used on a deal in the same currency.
- Prompt library entries for the deal desk, plus a second skill-chaining
  example (event blitz → lead management → deal desk).
- `docs/mcp/authentication.md` now documents the gates that are stricter than
  the role table: compensation (admin-only to write, admin-or-self to read),
  add-on-gated categories and their `ADDON_REQUIRED` error, and the actions
  that have **no tool at all** by design.

### Changed
- **Tool catalog regenerated from the live server: 55 → 129 organization tools,
  8 → 9 personal.** v1.0.0 documented roughly 40% of the surface. Whole
  categories were absent: booking, companies, deals and quotes, the price
  book, team performance, automation, lead scoring, enrichment, dashboards,
  file library, access domains, contact points, lead documents and saved views.

[1.1.0]: https://github.com/Gravisun/lynqu-ai-toolkit/releases/tag/v1.1.0

## [1.0.0] - 2026-06-18

### Added
- Initial public release of the Lynqu AI Toolkit.
- MCP documentation: connection guide, OAuth 2.1 authentication explainer, full
  tool catalog (55 organization tools + 8 personal tools), and troubleshooting.
- Copy-paste client configs for Claude, Cursor, and VS Code.
- Seven Agent Skills:
  - `lynqu-lead-research`: find & qualify target accounts.
  - `lynqu-lead-capture`: capture, enrich, dedupe, and route leads.
  - `lynqu-lead-management`: pipeline hygiene, stage moves, assignment, bulk ops.
  - `lynqu-sales-followup`: draft & send follow-ups via templates.
  - `lynqu-event-blitz`: end-to-end event capture → tag → campaign → follow-up.
  - `lynqu-pipeline-report`: weekly pipeline & dashboard insights.
  - `lynqu-card-studio`: create & update digital business cards conversationally.
- Prompt library in `examples/prompts.md`.

[1.0.0]: https://github.com/Gravisun/lynqu-ai-toolkit/releases/tag/v1.0.0

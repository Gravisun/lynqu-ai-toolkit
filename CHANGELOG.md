# Changelog

All notable changes to the Lynqu AI Toolkit are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.2.0] - 2026-08-04

### Added
- **`lynqu` — one command instead of fifteen.** Describe the situation ("we got
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
- **Every skill now ends by writing to Lynqu** — a scored lead, a dated task, a
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
  that cause was wrong — the real gap was a README that only ever explained the
  Claude Code install. 200 remains as a house limit, on its own merits.
- README said Claude Desktop reads `~/.claude/skills`. It doesn't — that path is
  Claude Code only; the desktop app is claude.ai and takes ZIP uploads.

[1.2.0]: https://github.com/Gravisun/lynqu-ai-toolkit/releases/tag/v1.2.0

[1.1.2]: https://github.com/Gravisun/lynqu-ai-toolkit/releases/tag/v1.1.2

## [1.1.1] - 2026-08-04

### Fixed
- **The README only ever explained the Claude Code install.** Anyone using
  claude.ai — web, the desktop app, or mobile — followed a `cp -r` into a folder
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
- `lynqu-deal-desk` skill — browse the price book, put priced lines on a deal,
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
  categories were absent — booking, companies, deals and quotes, the price
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
  - `lynqu-lead-research` — find & qualify target accounts.
  - `lynqu-lead-capture` — capture, enrich, dedupe, and route leads.
  - `lynqu-lead-management` — pipeline hygiene, stage moves, assignment, bulk ops.
  - `lynqu-sales-followup` — draft & send follow-ups via templates.
  - `lynqu-event-blitz` — end-to-end event capture → tag → campaign → follow-up.
  - `lynqu-pipeline-report` — weekly pipeline & dashboard insights.
  - `lynqu-card-studio` — create & update digital business cards conversationally.
- Prompt library in `examples/prompts.md`.

[1.0.0]: https://github.com/Gravisun/lynqu-ai-toolkit/releases/tag/v1.0.0

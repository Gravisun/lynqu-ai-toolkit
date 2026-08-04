# Changelog

All notable changes to the Lynqu AI Toolkit are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Fixed
- All eight skill `description` fields shortened to under 200 characters —
  claude.ai rejected the uploads above that limit (Claude Code does not enforce
  it, so the repo validated locally but failed on the web app).
- Stale skill count in the README badge and skills intro (seven → eight).

### Added
- `scripts/validate_skills.py` now fails on a description over 200 characters.
- README install step covers claude.ai web & mobile (ZIP upload per skill,
  plus the required "Code execution and file creation" capability).

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

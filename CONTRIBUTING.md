# Contributing to the Lynqu AI Toolkit

Thanks for helping make Lynqu work better with AI assistants. This repo is the
**client-side** toolkit — Agent Skills and MCP documentation. It contains no
server code and no secrets.

## Ground rules

- **Skills may only call documented MCP tools.** Every tool a skill references
  must exist in [`docs/mcp/tool-catalog.md`](docs/mcp/tool-catalog.md). If you
  need a tool that doesn't exist yet, open an issue rather than referencing a
  tool that will error at call time.
- **No secrets, ever.** No API keys, tokens, internal URLs, or customer data in
  commits, examples, or screenshots. The MCP uses OAuth — there is never a
  static token to paste.
- **Respect the auth model.** Don't document ways to bypass the plan gate, role
  gate, or org policy. Those are product decisions enforced server-side.
- **Keep brand claims accurate.** Lynqu is an *AI lead capture, engagement &
  management platform*. The card is the entry point, not the whole product.

## Adding or changing a skill

1. Each skill lives in `skills/<skill-name>/SKILL.md` with valid frontmatter:
   ```yaml
   ---
   name: lynqu-example
   description: One sentence, keyword-rich, describing when to use the skill.
   ---
   ```
2. The `name` must be kebab-case and prefixed `lynqu-`.
3. List the MCP tools the skill uses, and the order it calls them.
4. Add at least one end-to-end example to [`examples/prompts.md`](examples/prompts.md).
5. Run the validation locally (same as CI):
   ```bash
   .github/workflows/validate.yml   # see the script section; or run the checks by hand
   ```

## Keeping in sync with the MCP server

The tool catalog in this repo mirrors the hosted Lynqu MCP server. When tools
are added, renamed, or removed on the server, update:

- [`docs/mcp/tool-catalog.md`](docs/mcp/tool-catalog.md)
- Any skill that references the changed tool
- [`CHANGELOG.md`](CHANGELOG.md)

## Pull requests

- One logical change per PR.
- Update docs and the changelog in the same PR.
- Describe how you tested the skill (which client, which prompts).

## Reporting issues

Use the issue templates. For connection problems, include your client, the
server URL you used, and the exact error — see
[`docs/mcp/troubleshooting.md`](docs/mcp/troubleshooting.md) first.

#!/usr/bin/env python3
"""Validate Lynqu AI Toolkit skills.

Checks, for every skills/*/SKILL.md:
  1. YAML frontmatter exists with non-empty `name` and `description`.
  2. `name` is kebab-case and prefixed `lynqu-`, and matches its folder name.
  3. `description` stays under our 200-char house limit. Anthropic documents a
     1024-char maximum; 200 is a deliberately tighter budget: the description is
     always in context and is what Claude matches a request against, so a tight
     one both triggers better and travels safely across every upload surface.
  4. Every MCP tool the skill references (backtick `tool-name`) is documented in
     docs/mcp/tool-catalog.md: so a skill can't call a tool that will error.
  5. No em dash anywhere in the repo's text files (house voice rule: a colon,
     a comma or a full stop says the same thing and reads like a person).

Exit code is non-zero if any check fails. No third-party dependencies.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
CATALOG = ROOT / "docs" / "mcp" / "tool-catalog.md"

# The orchestrator is bare `lynqu`; every specialist is `lynqu-<something>`.
NAME_RE = re.compile(r"^lynqu(?:-[a-z0-9]+)*$")
# House limit. Anthropic's documented maximum is 1024, but a description is
# permanently in context and is the text Claude matches requests against, so we
# keep ours tight: and short descriptions upload cleanly everywhere.
MAX_DESC = 200
# A backticked token that looks like an MCP tool id: all lowercase, hyphenated,
# at least one hyphen (e.g. `create-lead`). Excludes paths and prose.
TOOL_TOKEN_RE = re.compile(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`")


def known_tools() -> set[str]:
    if not CATALOG.exists():
        sys.exit(f"FATAL: tool catalog not found at {CATALOG}")
    return set(TOOL_TOKEN_RE.findall(CATALOG.read_text(encoding="utf-8")))


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    data: dict[str, str] = {}
    key = None
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            data[key] = m.group(2).strip()
        elif key and line.strip():
            # folded/continued scalar (e.g. `description: >-`)
            data[key] = (data[key] + " " + line.strip()).strip()
    return data


def main() -> int:
    tools = known_tools()
    errors: list[str] = []
    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skill_dirs:
        return _fail(["No skills found under skills/"])

    for d in skill_dirs:
        skill_md = d / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{d.name}: missing SKILL.md")
            continue
        text = skill_md.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)

        name = fm.get("name", "")
        desc = fm.get("description", "").strip("'\" >-")
        if not name:
            errors.append(f"{d.name}: frontmatter missing `name`")
        else:
            if not NAME_RE.match(name):
                errors.append(f"{d.name}: name '{name}' must be `lynqu` or kebab-case prefixed lynqu-")
            if name != d.name:
                errors.append(f"{d.name}: name '{name}' must match folder name")
        if not desc:
            errors.append(f"{d.name}: frontmatter missing `description`")
        elif len(desc) > MAX_DESC:
            errors.append(
                f"{d.name}: description is {len(desc)} chars, max {MAX_DESC} "
                "(house limit: keep it short and matchable)"
            )

        referenced = set(TOOL_TOKEN_RE.findall(text))
        # Only treat tokens that appear in a "Tools used" context or look like
        # tools; filter out obvious non-tools by intersecting with catalog miss.
        unknown = {
            t for t in referenced
            if t not in tools and _looks_like_tool(t)
        }
        for t in sorted(unknown):
            errors.append(f"{d.name}: references undocumented MCP tool `{t}`")

    errors.extend(em_dash_hits())

    if errors:
        return _fail(errors)
    print(f"OK: {len(skill_dirs)} skills validated against {len(tools)} catalog tools.")
    return 0


# Verb-prefixed hyphenated tokens are very likely tool ids; this keeps prose
# like `pt-br` or `co-marketing` from tripping the check while still catching
# real tool typos such as `create-leads` (vs `create-lead`).
_TOOL_VERBS = ("list", "get", "create", "update", "add", "assign", "remove",
               "bulk", "move", "send", "attach", "link", "search", "who", "how",
               "delete", "merge", "manage", "decide", "issue", "confirm",
               "start", "review", "propose", "reschedule", "accept", "explain")


def _looks_like_tool(token: str) -> bool:
    return token.split("-", 1)[0] in _TOOL_VERBS


TEXT_SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml", ".txt", ".gitignore"}


def em_dash_hits() -> list[str]:
    hits = []
    for p in sorted(ROOT.rglob("*")):
        if ".git" in p.parts or not p.is_file():
            continue
        if p.suffix not in TEXT_SUFFIXES and p.name not in TEXT_SUFFIXES:
            continue
        for n, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if "\u2014" in line:
                hits.append(f"{p.relative_to(ROOT)}:{n}: em dash; use a colon, comma or full stop")
    return hits


def _fail(errors: list[str]) -> int:
    print("Skill validation FAILED:\n")
    for e in errors:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

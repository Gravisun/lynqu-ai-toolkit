#!/usr/bin/env python3
"""Validate Lynqu AI Toolkit skills.

Checks, for every skills/*/SKILL.md:
  1. YAML frontmatter exists with non-empty `name` and `description`.
  2. `name` is kebab-case and prefixed `lynqu-`, and matches its folder name.
  3. `description` fits the claude.ai skill-upload limit (200 chars). Claude Code
     never enforces this, so a repo that passes locally can still be rejected on
     upload to the web app.
  4. Every MCP tool the skill references (backtick `tool-name`) is documented in
     docs/mcp/tool-catalog.md — so a skill can't call a tool that will error.

Exit code is non-zero if any check fails. No third-party dependencies.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
CATALOG = ROOT / "docs" / "mcp" / "tool-catalog.md"

NAME_RE = re.compile(r"^lynqu-[a-z0-9]+(?:-[a-z0-9]+)*$")
# claude.ai (web/mobile) rejects a skill whose frontmatter description exceeds
# this. Claude Code has no such limit — hence the check.
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
                errors.append(f"{d.name}: name '{name}' must be kebab-case, prefixed lynqu-")
            if name != d.name:
                errors.append(f"{d.name}: name '{name}' must match folder name")
        if not desc:
            errors.append(f"{d.name}: frontmatter missing `description`")
        elif len(desc) > MAX_DESC:
            errors.append(
                f"{d.name}: description is {len(desc)} chars, max {MAX_DESC} "
                "(claude.ai rejects the upload above this)"
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

    if errors:
        return _fail(errors)
    print(f"OK: {len(skill_dirs)} skills validated against {len(tools)} catalog tools.")
    return 0


# Verb-prefixed hyphenated tokens are very likely tool ids; this keeps prose
# like `pt-br` or `co-marketing` from tripping the check while still catching
# real tool typos such as `create-leads` (vs `create-lead`).
_TOOL_VERBS = ("list", "get", "create", "update", "add", "assign", "remove",
               "bulk", "move", "send", "attach", "link", "search", "who", "how")


def _looks_like_tool(token: str) -> bool:
    return token.split("-", 1)[0] in _TOOL_VERBS


def _fail(errors: list[str]) -> int:
    print("Skill validation FAILED:\n")
    for e in errors:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

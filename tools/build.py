#!/usr/bin/env python3
"""Writes every harness's manifest from drawer.json, and checks the skills.

    tools/build.py           write the manifests
    tools/build.py --check   fail if any manifest is stale or any skill is invalid

drawer.json is the one list of skills. Each skill lives once, in
skills/<name>/SKILL.md; the manifests below only point at it, so adding a
skill means adding its folder and one entry in drawer.json, then running this.
Standard library only, so it runs anywhere Python 3 does.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAWER = json.loads((ROOT / "drawer.json").read_text())

# The Agent Skills standard (agentskills.io): a lowercase, hyphenated name of
# at most 64 characters that matches its folder, and a description of at most
# 1024 characters, which is what an agent reads to decide when to use it.
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESCRIPTION = 1024

# Installs every skill at once, for people who want the whole drawer.
EVERYTHING = "the-whole-drawer"


def frontmatter(path):
    """The SKILL.md's frontmatter fields, as plain strings."""
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return None
    fields = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith((" ", "\t")):
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def problems():
    """Every way the skills and drawer.json disagree with each other or the standard."""
    found = []
    listed = [skill["name"] for skill in DRAWER["skills"]]
    on_disk = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())
    for name in sorted(set(on_disk) - set(listed)):
        found.append(f"skills/{name} is not listed in drawer.json")
    for name in listed:
        skill_md = ROOT / "skills" / name / "SKILL.md"
        if not skill_md.exists():
            found.append(f"drawer.json lists {name}, but skills/{name}/SKILL.md does not exist")
            continue
        fields = frontmatter(skill_md)
        if fields is None:
            found.append(f"{skill_md.relative_to(ROOT)} has no frontmatter")
            continue
        if fields.get("name") != name:
            found.append(f"{skill_md.relative_to(ROOT)}: name is {fields.get('name')!r}, its folder is {name!r}")
        if not NAME.match(name) or len(name) > MAX_NAME:
            found.append(f"{name}: names are lowercase words joined by hyphens, at most {MAX_NAME} characters")
        description = fields.get("description", "")
        if not description:
            found.append(f"{skill_md.relative_to(ROOT)} has no description")
        elif len(description) > MAX_DESCRIPTION:
            found.append(f"{skill_md.relative_to(ROOT)}: description is {len(description)} characters, at most {MAX_DESCRIPTION}")
    return found


def author():
    owner = DRAWER["owner"]
    return {"name": owner["name"], "url": owner["url"]}


def claude_marketplace():
    """Claude Code's marketplace: one plugin per skill, plus one with them all.

    Each plugin is the whole repository with "strict": false and a list of
    skills, so a skill exists once and every plugin points at it.
    """
    plugins = [
        {
            "name": skill["name"],
            "description": skill["summary"],
            "version": DRAWER["version"],
            "author": author(),
            "homepage": f"{DRAWER['repository']}/tree/main/skills/{skill['name']}",
            "category": skill["category"].lower().replace(" ", "-"),
            "keywords": skill["keywords"],
            "source": "./",
            "strict": False,
            "skills": [f"./skills/{skill['name']}"],
        }
        for skill in DRAWER["skills"]
    ]
    plugins.append(
        {
            "name": EVERYTHING,
            "description": "Every skill in the drawer at once.",
            "version": DRAWER["version"],
            "author": author(),
            "homepage": DRAWER["repository"],
            "source": "./",
            "strict": False,
            "skills": [f"./skills/{skill['name']}" for skill in DRAWER["skills"]],
        }
    )
    return {
        "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
        "name": DRAWER["name"],
        "description": DRAWER["description"],
        "owner": author(),
        "plugins": plugins,
    }


def gemini_extension():
    """Gemini CLI's extension: it loads every skill under skills/ by itself."""
    return {
        "name": DRAWER["name"],
        "version": DRAWER["version"],
        "description": DRAWER["description"],
    }


def outputs():
    """Each generated file, or generated part of one, and what it should hold."""
    return {
        ".claude-plugin/marketplace.json": render(claude_marketplace()),
        "gemini-extension.json": render(gemini_extension()),
        "README.md": readme(),
    }


def render(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


SKILLS_START = "<!-- skills: written by tools/build.py from drawer.json -->\n"
SKILLS_END = "<!-- /skills -->"


def readme():
    """README.md with its skills table rewritten from drawer.json."""
    text = (ROOT / "README.md").read_text()
    before, _, rest = text.partition(SKILLS_START)
    _, _, after = rest.partition(SKILLS_END)
    rows = [f"| [`{s['name']}`](skills/{s['name']}/SKILL.md) | {s['summary']} |" for s in DRAWER["skills"]]
    table = "\n".join(["| Skill | What it does |", "| --- | --- |", *rows]) + "\n"
    return before + SKILLS_START + table + SKILLS_END + after


def main():
    check = "--check" in sys.argv[1:]
    found = problems()
    for path, text in outputs().items():
        target = ROOT / path
        if check:
            if not target.exists() or target.read_text() != text:
                found.append(f"{path} is out of date: run tools/build.py")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
    for problem in found:
        print(f"  {problem}", file=sys.stderr)
    if found:
        sys.exit(1)
    print("ok" if check else "manifests written")


if __name__ == "__main__":
    main()

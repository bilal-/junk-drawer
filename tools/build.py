#!/usr/bin/env python3
"""Writes every harness's manifest from drawer.json, and checks the skills.

    tools/build.py           write the manifests
    tools/build.py --check   fail if any manifest is stale or any skill is invalid

drawer.json is the one list of skills. Each skill lives once, in
skills/<name>/SKILL.md; the manifests below only point at it, so adding a
skill means adding its folder and one entry in drawer.json, then running this.
Standard library only, so it runs anywhere Python 3 does.
"""

import hashlib
import json
import re
import subprocess
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

# Installs every skill at once, for people who want the whole drawer. It has
# no version, so it follows the repository's commits.
EVERYTHING = "the-whole-drawer"

# A skill's version: major.minor.patch.
VERSION = re.compile(r"^\d+\.\d+\.\d+$")



# Frontmatter here is a strict subset of YAML, so it reads the same in every
# harness without a YAML library: one field per line, and each value either a
# bare word of lowercase letters, digits, and hyphens that starts with a letter
# (so YAML cannot read it as a number), or a double-quoted
# string written as JSON would write it (which YAML reads the same way).
BARE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
# Bare words YAML reads as something other than a string.
RESERVED = {"true", "false", "null", "yes", "no", "on", "off", "y", "n"}


def frontmatter(path):
    """The SKILL.md's frontmatter fields as strings, and any lines that break the subset."""
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return None, []
    fields, bad = {}, []
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if line.startswith((" ", "\t")) or not sep:
            bad.append(f"continued or unkeyed line {line.strip()!r}")
        elif BARE.match(value) and value not in RESERVED:
            fields[key] = value
        else:
            try:
                fields[key] = json.loads(value)
            except ValueError:
                fields[key] = None
            if not isinstance(fields[key], str) or not value.startswith('"'):
                fields[key] = value
                bad.append(f"{key}: write the value in double quotes, escaped as JSON would")
    return fields, bad


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
        fields, bad = frontmatter(skill_md)
        if fields is None:
            found.append(f"{skill_md.relative_to(ROOT)} has no frontmatter")
            continue
        found += [f"{skill_md.relative_to(ROOT)} frontmatter: {problem}" for problem in bad]
        if fields.get("name") != name:
            found.append(f"{skill_md.relative_to(ROOT)}: name is {fields.get('name')!r}, its folder is {name!r}")
        if not VERSION.match(skill_entry(name).get("version", "")):
            found.append(f"{name}: drawer.json needs a version like 1.0.0")
        if not NAME.match(name) or len(name) > MAX_NAME:
            found.append(f"{name}: names are lowercase words joined by hyphens, at most {MAX_NAME} characters")
        description = fields.get("description", "")
        if not description:
            found.append(f"{skill_md.relative_to(ROOT)} has no description")
        elif len(description) > MAX_DESCRIPTION:
            found.append(f"{skill_md.relative_to(ROOT)}: description is {len(description)} characters, at most {MAX_DESCRIPTION}")
    return found + unbumped()


def skill_entry(name):
    return next(skill for skill in DRAWER["skills"] if skill["name"] == name)


def version_key(version):
    return tuple(int(part) for part in version.split("."))


def needs_bump(changed, before, now):
    """The changed skills whose version is not above the one they had before.

    A skill new since then, or from before skills had versions, needs nothing.
    """
    return sorted(
        name for name in changed
        if before.get(name) and VERSION.match(before[name]) and VERSION.match(now.get(name, ""))
        and version_key(now[name]) <= version_key(before[name])
    )


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)


def published():
    """Every published commit this work could start from: where it left its
    upstream, and where it left each remote branch. Changes made since on the
    published side are not this work's.

    All of them, rather than one: a clone may not record which remote branch
    is the default, and every way of guessing has a case it gets wrong.
    """
    refs = ["@{upstream}", *git("for-each-ref", "--format=%(refname)", "refs/remotes").stdout.split()]
    bases = {git("merge-base", "HEAD", ref).stdout.strip() for ref in refs if not ref.endswith("/HEAD")}
    bases.discard("")
    return sorted(bases)


def unbumped():
    """Skills changed since a published commit whose version has not gone up since.

    Users update when a skill's version changes, so a change without a bump
    never reaches them. One bump covers any number of commits before a push.
    """
    now = {s["name"]: s.get("version", "") for s in DRAWER["skills"]}
    found = set()
    for base in published():
        shown = git("show", f"{base}:drawer.json")
        if shown.returncode:
            continue
        before = {s["name"]: s.get("version", "") for s in json.loads(shown.stdout)["skills"]}
        changed = [
            name for name in now
            if git("diff", "--quiet", base, "--", f"skills/{name}").returncode
            or git("ls-files", "--others", "--exclude-standard", "--", f"skills/{name}").stdout
        ]
        found.update((name, before[name]) for name in needs_bump(changed, before, now))
    return [
        f"skills/{name} changed since it was last published at {version}, but its version in drawer.json has not gone up: raise it"
        for name, version in sorted(found)
    ]


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
            "version": skill["version"],
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
    """Gemini CLI's extension: it loads every skill under skills/ by itself.

    Gemini updates a git install by commit, but a local install only when this
    version changes, so the version is drawn from every skill's name and
    version: adding, removing, or raising one changes it.
    """
    skills = ",".join(f"{s['name']}@{s['version']}" for s in DRAWER["skills"])
    return {
        "name": DRAWER["name"],
        "version": f"1.0.0+{hashlib.sha256(skills.encode()).hexdigest()[:8]}",
        "description": DRAWER["description"],
    }


def outputs():
    """Each generated file, or generated part of one, and what it should hold."""
    return {
        ".claude-plugin/marketplace.json": render(claude_marketplace()),
        "gemini-extension.json": render(gemini_extension()),
        "README.md": readme((ROOT / "README.md").read_text(), DRAWER["skills"]),
    }


def render(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


SKILLS_START = "<!-- skills: written by tools/build.py from drawer.json -->\n"
SKILLS_END = "<!-- /skills -->"


def readme(text, skills):
    """README.md's text with its skills table rewritten from these skills."""
    before, _, rest = text.partition(SKILLS_START)
    _, _, after = rest.partition(SKILLS_END)
    rows = [f"| [`{s['name']}`](skills/{s['name']}/SKILL.md) | {s['summary']} |" for s in skills]
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

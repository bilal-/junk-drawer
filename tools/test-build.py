#!/usr/bin/env python3
"""Tests build.py's frontmatter reader: what it must reject, and what it must read right."""

import importlib.util
import sys
import tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location("build", Path(__file__).with_name("build.py"))
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

REJECTED = {
    "a folded block": "description: >-\n  long text\n",
    "a flow sequence": "description: [unterminated\n",
    "a bare colon": "description: Use: when asked\n",
    "an open quote": 'description: "half\n',
    "a quote inside quotes": 'description: "a "b" c"\n',
    "a comment": "description: # note\n",
    "a boolean": "description: false\n",
    "a sequence item": "description: - text\n",
    "an unknown escape": 'description: "bad\\q"\n',
    "single quotes": "description: 'it''s'\n",
    "a bare number": "description: 123\n",
    "a bare hex number": "description: 0x12\n",
    "a bare y": "description: y\n",
}
READ = {
    'description: "Say \\"hi\\" here"\n': 'Say "hi" here',
    'description: "Use C:\\\\tools"\n': "Use C:\\tools",
    "description: a-bare-word\n": "a-bare-word",
}


def read(fields):
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "SKILL.md"
        path.write_text(f"---\nname: x\n{fields}---\nbody\n")
        return build.frontmatter(path)


failures = [f"accepted {name}" for name, text in REJECTED.items() if not read(text)[1]]
for text, want in READ.items():
    fields, bad = read(text)
    if bad or fields["description"] != want:
        failures.append(f"misread {text.strip()!r}: {fields['description']!r} {bad}")
BUMPS = [
    # changed, before, now, which need a bump
    (["a"], {"a": "1.0.0"}, {"a": "1.0.0"}, ["a"]),
    (["a"], {"a": "1.2.0"}, {"a": "1.1.9"}, ["a"]),
    (["a"], {"a": "1.9.0"}, {"a": "1.10.0"}, []),
    (["a"], {"a": "1.0.0"}, {"a": "2.0.0"}, []),
    ([], {"a": "1.0.0"}, {"a": "1.0.0"}, []),
    (["new"], {}, {"new": "1.0.0"}, []),
    (["a"], {"a": ""}, {"a": "1.0.0"}, []),
]
for changed, before, now, want in BUMPS:
    got = build.needs_bump(changed, before, now)
    if got != want:
        failures.append(f"needs_bump({changed}, {before}, {now}) gave {got}, not {want}")

SKILL = {"name": "x", "summary": "Does x."}
GOOD = f"top\n{build.SKILLS_START}old\n{build.SKILLS_END}\nbottom\n"
if "bottom" not in build.readme(GOOD, [SKILL]) or "Does x." not in build.readme(GOOD, [SKILL]):
    failures.append("readme() lost the text around the table, or the table")
for name, text in {
    "no closing marker": f"top\n{build.SKILLS_START}old\nbottom\n",
    "no opening marker": f"top\nold\n{build.SKILLS_END}\nbottom\n",
    "markers in the wrong order": f"top\n{build.SKILLS_END}\n{build.SKILLS_START}bottom\n",
}.items():
    try:
        build.readme(text, [SKILL])
        failures.append(f"readme() accepted a README with {name}")
    except ValueError:
        pass

for failure in failures:
    print(f"FAIL: {failure}")
if failures:
    sys.exit(1)
print("test-build: ok")

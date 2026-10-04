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
}
READ = {
    'description: "Say \\"hi\\" here"\n': 'Say "hi" here',
    "description: 'it''s fine'\n": "it's fine",
    "description: plain words, with a comma\n": "plain words, with a comma",
}


def read(fields):
    path = Path(tempfile.mkdtemp()) / "SKILL.md"
    path.write_text(f"---\nname: x\n{fields}---\nbody\n")
    return build.frontmatter(path)


failures = [f"accepted {name}" for name, text in REJECTED.items() if not read(text)[1]]
for text, want in READ.items():
    fields, bad = read(text)
    if bad or fields["description"] != want:
        failures.append(f"misread {text.strip()!r}: {fields['description']!r} {bad}")
for failure in failures:
    print(f"FAIL: {failure}")
if failures:
    sys.exit(1)
print("test-build: ok")

#!/usr/bin/env python3
"""Tests project-backup's scripts end to end, on throwaway workspaces.

Each case builds a small workspace, runs the scripts as a person would, and
checks what they leave behind.
"""

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "project-backup" / "scripts"
BACKUP = SCRIPTS / "project_backup.py"
failures = []

# The scripts' own git calls must not see a commit in progress, when the
# pre-commit hook runs this.
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
GIT_ENV.update(GIT_AUTHOR_NAME="test", GIT_AUTHOR_EMAIL="test@example.com",
               GIT_COMMITTER_NAME="test", GIT_COMMITTER_EMAIL="test@example.com")


def check(name, ok, detail=""):
    if not ok:
        failures.append(f"{name}{': ' + detail if detail else ''}")


def run(*args, cwd=None):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, cwd=cwd, env=GIT_ENV)


def git_project(path, files, ignored=()):
    """A git repository at path holding files, with ignored ones left untracked."""
    path.mkdir(parents=True)
    for name, text in files.items():
        (path / name).write_text(text)
    (path / ".gitignore").write_text("".join(f"{name}\n" for name in ignored))
    subprocess.run(["git", "init", "-q", str(path)], check=True, env=GIT_ENV)
    subprocess.run(["git", "-C", str(path), "add", "-A"], check=True, env=GIT_ENV)
    subprocess.run(["git", "-C", str(path), "commit", "-qm", "init"], check=True, env=GIT_ENV)


def profile(work, **fields):
    data = {"schema_version": 1, "roots": [str(work / "ws")], **fields}
    path = work / "profile.json"
    path.write_text(json.dumps(data))
    return path


def case():
    """A fresh workspace for one case: an app with an ignored .env, and a key outside it."""
    work = Path(tempfile.mkdtemp(prefix="junk-drawer-backup."))
    git_project(work / "ws" / "app", {"package.json": "{}", ".env": "API_KEY=dummy\n", ".env.production": "TRACKED=1\n"},
                ignored=[".env"])
    (work / "keys").mkdir()
    (work / "keys" / "upload.p12").write_bytes(b"dummy key bytes")
    return work


def shared_key(work):
    """A profile entry for the key outside the app."""
    return {
        "source": str(work / "keys" / "upload.p12"),
        "destination": "Credentials/Signing/upload.p12",
        "description": "Test signing key.",
        "restore": "Put it back.",
    }

# What a build makes: the private copies, the records, and a verifier that runs on its own.
work = case()
try:
    inventory = work / "inventory.json"
    result = run(BACKUP, "inventory", "--root", work / "ws", "--output", inventory)
    check("inventory runs", result.returncode == 0, result.stderr)
    found = json.loads(inventory.read_text())["projects"]
    check("inventory finds the app and its ignored .env",
          [p["id"] for p in found] == ["app"] and ".env" in [c["path"] for c in found[0]["local_recovery_candidates"]], str(found))
    out = work / "out" / "backup"
    result = run(BACKUP, "build", "--profile", profile(work, shared_files=[shared_key(work)]), "--destination", out)
    check("build runs", result.returncode == 0, result.stderr)
    check("build copies the ignored .env", (out / "Projects/app/Private Configuration/dot-env").read_text() == "API_KEY=dummy\n")
    check("build copies the shared key", (out / "Credentials/Signing/upload.p12").read_bytes() == b"dummy key bytes")
    check("build leaves tracked files out, even ones named like secrets",
          not (out / "Projects/app/Private Configuration/dot-env.production").exists())
    for record in ["MANIFEST.json", "SHA256SUMS.txt", "PROJECTS-INDEX.md", "MISSING-ASSETS.md", "README.txt",
                   "Tools/verify-backup.py", "Projects/app/FILES.json", "Projects/app/PROJECT-RECORD.json"]:
        check(f"build writes {record}", (out / record).is_file())
    modes = {stat.S_IMODE(p.stat().st_mode) for p in [out, *out.rglob("*")]}
    check("everything in the backup is owner-only", all(m & 0o077 == 0 for m in modes), oct(max(modes)))
    check("every folder has a README", all((d / "README.txt").is_file() for d in [out, *out.rglob("*")] if d.is_dir()))
    result = run(out / "Tools/verify-backup.py", cwd=work)
    check("the packaged verifier passes from another folder", result.returncode == 0, result.stdout + result.stderr)
    result = run(BACKUP, "verify", "--destination", out)
    check("verify passes", result.returncode == 0, result.stderr)
    result = run(BACKUP, "build", "--profile", work / "profile.json", "--destination", out)
    check("build refuses an existing backup without --extend", result.returncode != 0 and "--extend" in result.stderr,
          result.stderr.strip())
    (out / "Credentials/Signing/upload.p12").write_bytes(b"changed")
    result = run(out / "Tools/verify-backup.py", cwd=work)
    check("the packaged verifier catches a changed file", result.returncode != 0 and "upload.p12" in result.stdout)
    result = run(BACKUP, "verify", "--destination", out)
    check("verify catches a changed file", result.returncode != 0 and "upload.p12" in result.stderr)
finally:
    shutil.rmtree(work)

# A verified backup can be extended with another project.
work = case()
try:
    out = work / "out" / "backup"
    run(BACKUP, "build", "--profile", profile(work), "--destination", out)
    git_project(work / "ws" / "second", {"package.json": "{}", ".env": "B=1\n"}, ignored=[".env"])
    result = run(BACKUP, "build", "--profile", profile(work, projects={"app": {"exclude": True}}), "--destination", out, "--extend")
    check("--extend adds a project to a verified backup", result.returncode == 0, result.stderr.strip())
    check("--extend leaves a backup that verifies", run(BACKUP, "verify", "--destination", out).returncode == 0)
finally:
    shutil.rmtree(work)

# A backup of credentials alone, with every project excluded.
work = case()
try:
    out = work / "out" / "backup"
    result = run(BACKUP, "build", "--profile", profile(work, projects={"app": {"exclude": True}}, shared_files=[shared_key(work)]),
                 "--destination", out)
    check("build works with no projects in scope", result.returncode == 0, result.stderr.strip())
finally:
    shutil.rmtree(work)

# Two roots, one inside the other, both holding the same non-Git project.
work = case()
try:
    (work / "ws" / "tool").mkdir()
    (work / "ws" / "tool" / "package.json").write_text("{}")
    inventory = work / "inventory.json"
    run(BACKUP, "inventory", "--root", work / "ws", "--root", work / "ws" / "tool", "--output", inventory)
    ids = [p["id"] for p in json.loads(inventory.read_text())["projects"]]
    check("overlapping roots list a non-Git project once", ids.count("tool") + sum(i.startswith("tool-") for i in ids) == 1, str(ids))
finally:
    shutil.rmtree(work)

# A folder to copy that contains the backup's own destination.
work = case()
try:
    (work / "state").mkdir()
    (work / "state" / "settings.ini").write_text("x=1\n")
    out = work / "state" / "backup"
    area = {"source": str(work / "state"), "destination": "Tools/state", "description": "Tool state.", "restore": "Copy back."}
    result = run(BACKUP, "build", "--profile", profile(work, loose_areas=[area]), "--destination", out)
    check("build refuses a destination inside a folder it copies", result.returncode != 0 and not out.exists(),
          result.stderr.strip())
finally:
    shutil.rmtree(work)

for failure in failures:
    print(f"FAIL: {failure}")
if failures:
    sys.exit(1)
print("test-backup: ok")

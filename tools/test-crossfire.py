#!/usr/bin/env python3
"""Tests crossfire's review helper end to end, with fake reviewer CLIs on PATH.

No real model runs: each fake prints what the real CLI prints (JSON for Claude
Code, a stderr header and an -o file for Codex, plain stdout for Antigravity), and
the cases check what the helper runs, records, rejects and accepts.
"""
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

HELPER = Path(__file__).resolve().parent.parent / "skills" / "crossfire" / "scripts" / "crossfire_review.py"
failures = []
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV.update(GIT_AUTHOR_NAME="test", GIT_AUTHOR_EMAIL="test@example.com",
           GIT_COMMITTER_NAME="test", GIT_COMMITTER_EMAIL="test@example.com")


def check(name, ok, detail=""):
    if not ok:
        failures.append(f"{name}{': ' + detail if detail else ''}")


def helper(*args, env=None):
    return subprocess.run([sys.executable, str(HELPER), *map(str, args)],
                          capture_output=True, text=True, env=env or ENV)


def fake(bin_dir, name, body):
    path = bin_dir / name
    path.write_text("#!/bin/sh\n" + body)
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def setup():
    work = Path(tempfile.mkdtemp(prefix="junk-drawer-crossfire."))
    repo = work / "repo"
    repo.mkdir()
    (repo / "design.md").write_text("# Design\n\nRevision: 3\n")
    subprocess.run(["git", "init", "-q", str(repo)], check=True, env=ENV)
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True, env=ENV)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "init"], check=True, env=ENV)
    for folder in ("bin", "logs", "reviews"):
        (work / folder).mkdir()
    (work / "prompt.txt").write_text("Read the brief and review it.")
    (work / "brief.md").write_text(f"Design: {repo}/design.md\nLog: {work}/reviews/log.md\n")
    env = dict(ENV, PATH=f"{work / 'bin'}{os.pathsep}{ENV['PATH']}", FAKE_ARGS=str(work / "args.txt"))
    return work, repo, env


def snap(work, repo):
    out = work / "snap.json"
    r = helper("snapshot", "--file", repo / "design.md", "--file", work / "brief.md",
               "--worktree", repo, "--output", out)
    check("snapshot runs", r.returncode == 0, r.stderr)
    return out


CLAUDE_OK = r'''printf '%s\n' "$@" > "$FAKE_ARGS"
cat > /dev/null
printf '{"is_error": false, "result": "Reviewed revision 3\\n\\nVerdict: fine.", "modelUsage": {"claude-test-1": {}}, "permission_denials": []}'
'''
CODEX_OK = r'''printf '%s\n' "$@" > "$FAKE_ARGS"
out=""; prev=""
for a in "$@"; do [ "$prev" = "-o" ] && out="$a"; prev="$a"; done
cat > /dev/null
printf 'model: codex-test\nsandbox: read-only\nreasoning effort: max\n' >&2
printf 'Reviewed revision 3\n\nVerdict: fine.\n' > "$out"
printf 'tokens used\n12,345\n' >&2
'''

# Claude: isolation flags, prompt on stdin, answer extracted from JSON, accepted.
work, repo, env = setup()
try:
    fake(work / "bin", "claude", CLAUDE_OK)
    s = snap(work, repo)
    r = helper("run", "--cli", "claude", "--model", "top", "--effort", "max", "--prompt-file", work / "prompt.txt",
               "--name", "r1-1", "--logs", work / "logs", "--cwd", repo, "--add-dir", work / "reviews", env=env)
    check("claude run exits 0", r.returncode == 0, r.stderr + r.stdout)
    argv = (work / "args.txt").read_text().splitlines()
    for flag in ("--safe-mode", "--strict-mcp-config", "--no-session-persistence", "--add-dir"):
        check(f"claude gets {flag}", flag in argv, " ".join(argv))
    check("claude gets read-only tools", "Read,Grep,Glob" in argv)
    check("claude gets --restricted", "--restricted" in argv)
    check("claude gets no settings", "--setting-sources" in argv and argv[argv.index("--setting-sources") + 1] == "")
    check("claude effort passed", "max" in argv)
    check("claude has no plan mode", "--permission-mode" not in argv)
    report = json.loads((work / "logs" / "r1-1.report.json").read_text())
    check("claude resolved model recorded", report.get("resolved_models") == ["claude-test-1"], str(report))
    r = helper("check", "--answer", work / "logs" / "r1-1.out", "--revision", "3", "--snapshot", s,
               "--report", work / "logs" / "r1-1.report.json", "--brief", work / "brief.md",
               "--allowed-root", repo, "--allowed-root", work / "reviews", "--accept-to", work / "reviews" / "r1-1.md")
    check("clean claude answer accepted", r.returncode == 0, r.stdout)
    check("accepted answer moved into reviews", (work / "reviews" / "r1-1.md").read_text().startswith("Reviewed revision 3"))
finally:
    shutil.rmtree(work)

# Codex: header parsed, hooks rejected, sandbox checked, prompt on stdin.
work, repo, env = setup()
try:
    fake(work / "bin", "codex", CODEX_OK)
    s = snap(work, repo)
    r = helper("run", "--cli", "codex", "--model", "top", "--effort", "max", "--prompt-file", work / "prompt.txt",
               "--name", "r1-2", "--logs", work / "logs", "--cwd", repo, "--git-repo", env=env)
    check("codex run exits 0", r.returncode == 0, r.stderr + r.stdout)
    argv = (work / "args.txt").read_text().splitlines()
    for flag in ("--ephemeral", "--ignore-user-config", "read-only", "-o", "model_reasoning_effort=max"):
        check(f"codex gets {flag}", flag in argv, " ".join(argv))
    check("codex never gets --search", "--search" not in argv)
    report = json.loads((work / "logs" / "r1-2.report.json").read_text())
    check("codex header parsed", report.get("sandbox") == "read-only" and report.get("hook_lines") == 0, str(report))
    check("codex tokens parsed", report.get("tokens") == "12,345", str(report))
    fake(work / "bin", "codex", CODEX_OK.replace("printf 'tokens used", "printf '  221  - a default run printed four hook: SessionStart lines\\nhook: mentioned in a file\\n' >&2\nprintf 'tokens used"))
    helper("run", "--cli", "codex", "--model", "top", "--prompt-file", work / "prompt.txt",
           "--name", "quoted", "--logs", work / "logs", "--cwd", repo, "--git-repo", env=env)
    quoted = json.loads((work / "logs" / "quoted.report.json").read_text())
    check("hook text quoted from files is not a hook", quoted.get("hook_lines") == 0, str(quoted))
    r = helper("check", "--answer", work / "logs" / "r1-2.out", "--revision", "3", "--snapshot", s,
               "--report", work / "logs" / "r1-2.report.json")
    check("clean codex answer passes", r.returncode == 0, r.stdout)
    fake(work / "bin", "codex", CODEX_OK.replace("model: codex-test", "hook: SessionStart\\nmodel: codex-test"))
    helper("run", "--cli", "codex", "--model", "top", "--prompt-file", work / "prompt.txt",
           "--name", "r1-3", "--logs", work / "logs", "--cwd", repo, "--git-repo", env=env)
    r = helper("check", "--answer", work / "logs" / "r1-3.out", "--revision", "3", "--snapshot", s,
               "--report", work / "logs" / "r1-3.report.json")
    check("a hook line rejects the answer", r.returncode == 1 and "hook" in r.stdout, r.stdout)
finally:
    shutil.rmtree(work)

# Rejections: wrong revision, changed subject, moved worktree, secret, path outside roots, empty.
work, repo, env = setup()
try:
    s = snap(work, repo)
    answer = work / "logs" / "a.out"
    answer.write_text("Reviewed revision 2\n\nok\n")
    r = helper("check", "--answer", answer, "--revision", "3", "--snapshot", s)
    check("stale revision rejected", r.returncode == 1 and "expected" in r.stdout, r.stdout)
    answer.write_text("Reviewed revision 3\n\nok\n")
    (repo / "design.md").write_text("# Design\n\nRevision: 3\nedited\n")
    r = helper("check", "--answer", answer, "--revision", "3", "--snapshot", s)
    check("changed subject rejected", r.returncode == 1 and "changed during review" in r.stdout, r.stdout)
    s = snap(work, repo)
    (repo / "new.txt").write_text("x")
    r = helper("check", "--answer", answer, "--revision", "3", "--snapshot", s)
    check("dirty worktree rejected", r.returncode == 1 and "status changed" in r.stdout, r.stdout)
    (repo / "new.txt").unlink()
    answer.write_text("Reviewed revision 3\n\nkey: AKIA" + "A" * 16 + "\n")
    r = helper("check", "--answer", answer, "--revision", "3", "--snapshot", s)
    check("secret-looking answer rejected", r.returncode == 1 and "secret" in r.stdout, r.stdout)
    answer.write_text("Reviewed revision 3\n\nok\n")
    (work / "brief.md").write_text(f"Design: {repo}/design.md\nDon't read {work}/logs or git history.\nAlso read /etc/hosts\n")
    s = snap(work, repo)
    r = helper("check", "--answer", answer, "--revision", "3", "--snapshot", s, "--brief", work / "brief.md",
               "--allowed-root", repo)
    check("brief path outside roots rejected", r.returncode == 1 and "/etc/hosts" in r.stdout, r.stdout)
    check("a forbidden path named in the brief is not an input", "/logs" not in r.stdout, r.stdout)
    ev = work / "evidence"
    ev.mkdir()
    (ev / "notes.txt").write_text("v1")
    s2 = work / "snap2.json"
    helper("snapshot", "--file", repo / "design.md", "--file", ev, "--worktree", repo, "--output", s2)
    (ev / "notes.txt").write_text("v2")
    r = helper("check", "--answer", answer, "--revision", "3", "--snapshot", s2)
    check("changed evidence folder rejected", r.returncode == 1 and "notes.txt" in r.stdout, r.stdout)
    answer.write_text("")
    r = helper("check", "--answer", answer, "--revision", "3", "--snapshot", s, "--accept-to", work / "reviews" / "x.md")
    check("empty answer rejected and not moved", r.returncode == 1 and not (work / "reviews" / "x.md").exists(), r.stdout)
finally:
    shutil.rmtree(work)

# Antigravity: no plan mode, footer added, auto-denial flagged; time limit enforced.
work, repo, env = setup()
try:
    fake(work / "bin", "agy", 'printf "%s\\n" "$@" > "$FAKE_ARGS"\nprintf "a tool was auto-denied\\n" >&2\n')
    s = snap(work, repo)
    helper("run", "--cli", "agy", "--model", "top", "--prompt-file", work / "prompt.txt",
           "--name", "r1-4", "--logs", work / "logs", "--cwd", repo, env=env)
    argv = (work / "args.txt").read_text()
    check("agy has no plan mode", "--mode" not in argv.splitlines(), argv)
    check("agy prompt carries the no-tools footer", "call no tools" in argv, argv)
    r = helper("check", "--answer", work / "logs" / "r1-4.out", "--revision", "3", "--snapshot", s,
               "--report", work / "logs" / "r1-4.report.json")
    check("empty agy answer with denial rejected", r.returncode == 1 and "auto-denied" in r.stdout, r.stdout)
    fake(work / "bin", "claude", "cat > /dev/null\nsleep 30\n")
    r = helper("run", "--cli", "claude", "--model", "top", "--prompt-file", work / "prompt.txt",
               "--name", "slow", "--logs", work / "logs", "--cwd", repo, "--timeout", "1", env=env)
    report = json.loads((work / "logs" / "slow.report.json").read_text())
    check("time limit stops a reviewer", r.returncode == 1 and report.get("timed_out") is True, str(report))
finally:
    shutil.rmtree(work)

# Trim keeps head and tail of text, and only summary fields of JSON.
work = Path(tempfile.mkdtemp(prefix="junk-drawer-crossfire."))
try:
    log = work / "r.err"
    log.write_text("\n".join(f"line {i}" for i in range(200)) + "\n")
    helper("trim", "--log", log, "--lines", "5")
    lines = log.read_text().splitlines()
    check("trim keeps head and tail", lines[0] == "line 0" and lines[-1] == "line 199" and len(lines) == 11, str(lines))
    js = work / "r.json"
    js.write_text(json.dumps({"is_error": False, "result": "long transcript", "modelUsage": {"m": {}}}))
    helper("trim", "--log", js)
    kept = json.loads(js.read_text())
    check("trim drops JSON transcript", "result" not in kept and kept.get("modelUsage") == {"m": {}}, str(kept))
finally:
    shutil.rmtree(work)

if failures:
    print("\n".join(f"FAIL: {f}" for f in failures))
    sys.exit(1)
print("test-crossfire: ok")

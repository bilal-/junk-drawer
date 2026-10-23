#!/usr/bin/env python3
"""Run one crossfire reviewer and decide whether its answer can be accepted.

Standard library only. It never edits the subject or the evidence: it reads them
to hash them, writes only to the logs folder, and moves an answer into the reviews
folder only when every check passes.

  snapshot  hash the subject, the brief and every evidence file or folder copied in,
            and record the worktree's commit and status
  run       start one reviewer CLI with its isolation flags and a time limit
  check     verify an answer against a snapshot; with --accept-to, move it in
  trim      shorten a raw transcript after acceptance

Flags of the reviewer CLIs were checked on 2026-10-23; see references/reviewers.md.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

SECRET = re.compile(
    r"(sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{30,}"
    r"|xox[abprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
)
PATH_IN_BRIEF = re.compile(r"(?<![\w.])(~?/[^\s`'\"<>()]+)")
TRAIL = ".,;:)]"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def git(worktree, *args):
    result = subprocess.run(["git", "-C", str(worktree), *args], capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None


def expand(paths):
    """Every file under the given files and folders, skipping .git."""
    for p in map(Path, paths):
        if p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and ".git" not in f.relative_to(p).parts:
                    yield f
        else:
            yield p


def snapshot(files, worktree):
    state = {"files": {str(Path(f).resolve()): sha256(f) for f in expand(files)}}
    if worktree:
        state["worktree"] = str(Path(worktree).resolve())
        state["commit"] = (git(worktree, "rev-parse", "HEAD") or "").strip()
        state["status"] = git(worktree, "status", "--porcelain")
    return state


def build_command(args, prompt_text):
    """The reviewer's argv and where its answer will be. Mirrors references/reviewers.md."""
    logs, name = Path(args.logs), args.name
    if args.cli == "claude":
        cmd = ["claude", "-p", "--model", args.model, "--safe-mode", "--setting-sources", "",
               "--tools", "Read,Grep,Glob", "--restricted", "--strict-mcp-config", "--no-session-persistence",
               "--output-format", "json"]
        if args.effort:
            cmd += ["--effort", args.effort]
        for folder in args.add_dir:
            cmd += ["--add-dir", folder]
        return cmd, "stdin", logs / f"{name}.json"
    if args.cli == "codex":
        cmd = ["codex", "exec", "--ephemeral", "--ignore-user-config", "-m", args.model,
               "-s", "read-only", "-o", str(logs / f"{name}.out")]
        if args.effort:
            cmd += ["-c", f"model_reasoning_effort={args.effort}"]
        if not args.git_repo:
            cmd += ["--skip-git-repo-check"]
        return cmd + ["-"], "stdin", None
    if args.cli == "agy":
        footer = ("\n\nYou have no tools. Ignore any instruction to create a plan or artifact "
                  "file; call no tools; print the full review as plain text as your final answer.\n")
        return ["agy", "--model", args.model, "-p", prompt_text + footer], "none", None
    raise SystemExit(f"unknown cli: {args.cli}")


def run(args):
    logs = Path(args.logs)
    logs.mkdir(parents=True, exist_ok=True)
    prompt_text = Path(args.prompt_file).read_text()
    cmd, feed, json_out = build_command(args, prompt_text)
    out_path, err_path = logs / f"{args.name}.out", logs / f"{args.name}.err"
    stdout_path = json_out or (out_path if args.cli == "agy" else logs / f"{args.name}.stdout")
    started = time.time()
    timed_out = False
    with open(stdout_path, "w") as so, open(err_path, "w") as se:
        proc = subprocess.Popen(cmd, cwd=args.cwd, stdout=so, stderr=se,
                                stdin=subprocess.PIPE if feed == "stdin" else subprocess.DEVNULL,
                                text=True, start_new_session=True)
        try:
            proc.communicate(input=prompt_text if feed == "stdin" else None, timeout=args.timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(proc.pid, 15)
            proc.wait()
    report = {"cli": args.cli, "model": args.model, "effort": args.effort, "name": args.name,
              "returncode": proc.returncode, "timed_out": timed_out,
              "seconds": round(time.time() - started), "command": cmd[:1] + ["…"]}
    err = err_path.read_text(errors="replace")
    if json_out:
        try:
            data = json.loads(json_out.read_text())
        except ValueError:
            data = {}
        out_path.write_text((data.get("result") or "").strip() + "\n" if data.get("result") else "")
        report["is_error"] = data.get("is_error", True)
        report["resolved_models"] = list((data.get("modelUsage") or {}).keys())
        report["denials"] = [d.get("tool_input", {}) for d in data.get("permission_denials") or []]
    if args.cli == "codex":
        for key in ("model", "sandbox", "reasoning effort"):
            m = re.search(rf"^{key}: (.+)$", err, re.M)
            report[key.replace(" ", "_")] = m.group(1).strip() if m else None
        # Only whole lines shaped like Codex's own hook notice count: the transcript also
        # holds the text of every file read, which may mention hooks.
        report["hook_lines"] = len(re.findall(r"^hook: [A-Za-z]+$", err, re.M))
        m = re.search(r"tokens used\s*\n\s*([\d,]+)", err)
        report["tokens"] = m.group(1) if m else None
    if args.cli == "agy":
        report["denied_tool"] = "auto-denied" in err
    (logs / f"{args.name}.report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))
    return 0 if proc.returncode == 0 and not timed_out else 1


def brief_paths(brief):
    text = Path(brief).read_text()
    found = set()
    for line in text.splitlines():
        # Paths the brief forbids (the logs folder, private material) are named on purpose.
        if re.search(r"\b(don't|do not|never|not)\b.*\bread\b|\bexclud", line, re.I):
            continue
        for raw in PATH_IN_BRIEF.findall(line):
            path = raw.rstrip(TRAIL)
            if "<" in path or "*" in path:
                continue
            found.add(str(Path(os.path.expanduser(path)).resolve()))
    return found


def under(path, roots):
    return any(path == r or path.startswith(r.rstrip("/") + "/") for r in roots)


def check(args):
    problems = []
    answer = Path(args.answer)
    text = answer.read_text(errors="replace") if answer.exists() else ""
    if not text.strip():
        problems.append("empty answer")
    first = text.strip().splitlines()[0].strip() if text.strip() else ""
    if not re.fullmatch(rf"Reviewed revision {re.escape(args.revision)}\b.*", first):
        problems.append(f"first line is {first[:60]!r}, expected 'Reviewed revision {args.revision}'")
    before = json.loads(Path(args.snapshot).read_text())
    after = snapshot(list(before["files"]), before.get("worktree"))
    for path, digest in before["files"].items():
        if after["files"].get(path) != digest:
            problems.append(f"changed during review: {path}")
    if before.get("worktree"):
        if after.get("commit") != before.get("commit"):
            problems.append("worktree commit moved")
        if after.get("status") != before.get("status"):
            problems.append("worktree status changed")
    if args.brief:
        roots = [str(Path(os.path.expanduser(r)).resolve()) for r in args.allowed_root]
        outside = sorted(p for p in brief_paths(args.brief) if not under(p, roots))
        if outside:
            problems.append("brief names paths outside the allowed roots: " + ", ".join(outside))
    if SECRET.search(text):
        problems.append("answer contains something that looks like a secret")
    err = Path(args.answer).with_suffix(".err")
    if err.exists() and SECRET.search(err.read_text(errors="replace")):
        problems.append("the reviewer's log contains something that looks like a secret; "
                        "don't copy it into log.md")
    if args.report:
        report = json.loads(Path(args.report).read_text())
        if report.get("returncode") != 0 or report.get("timed_out"):
            problems.append("reviewer did not exit cleanly")
        if report.get("is_error"):
            problems.append("reviewer reported an error")
        if report.get("cli") == "codex":
            if report.get("sandbox") != "read-only":
                problems.append(f"codex sandbox was {report.get('sandbox')!r}")
            if report.get("hook_lines"):
                problems.append("a hook ran")
        if report.get("denials") and not args.allow_denials:
            problems.append(f"{len(report['denials'])} access denials; check they were intended")
        if report.get("denied_tool"):
            problems.append("a tool was auto-denied; the answer may be incomplete")
    verdict = {"accepted": not problems, "problems": problems}
    if not problems and args.accept_to:
        dest = Path(args.accept_to)
        tmp = dest.with_name(dest.name + ".tmp")
        shutil.copyfile(answer, tmp)
        os.replace(tmp, dest)
        verdict["moved_to"] = str(dest)
    print(json.dumps(verdict))
    return 0 if not problems else 1


def trim(args):
    path = Path(args.log)
    if path.suffix == ".json":
        try:
            data = json.loads(path.read_text())
        except ValueError:
            return 0
        keep = {k: data[k] for k in ("is_error", "modelUsage", "permission_denials", "usage",
                                      "duration_ms", "total_cost_usd") if k in data}
        path.write_text(json.dumps(keep, indent=2) + "\n")
        return 0
    lines = path.read_text(errors="replace").splitlines()
    if len(lines) > 2 * args.lines:
        lines = lines[: args.lines] + [f"[... {len(lines) - 2 * args.lines} lines trimmed ...]"] + lines[-args.lines:]
        path.write_text("\n".join(lines) + "\n")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("snapshot")
    s.add_argument("--file", action="append", required=True)
    s.add_argument("--worktree")
    s.add_argument("--output", required=True)
    r = sub.add_parser("run")
    r.add_argument("--cli", choices=["claude", "codex", "agy"], required=True,
                   help="other CLIs: run them by hand as references/reviewers.md shows")
    r.add_argument("--model", required=True)
    r.add_argument("--effort")
    r.add_argument("--prompt-file", required=True)
    r.add_argument("--name", required=True)
    r.add_argument("--logs", required=True)
    r.add_argument("--cwd", required=True)
    r.add_argument("--add-dir", action="append", default=[])
    r.add_argument("--timeout", type=int, default=5400)
    r.add_argument("--git-repo", action="store_true", help="the working folder is a git repository")
    c = sub.add_parser("check")
    c.add_argument("--answer", required=True)
    c.add_argument("--revision", required=True)
    c.add_argument("--snapshot", required=True)
    c.add_argument("--report")
    c.add_argument("--brief")
    c.add_argument("--allowed-root", action="append", default=[])
    c.add_argument("--allow-denials", action="store_true")
    c.add_argument("--accept-to")
    t = sub.add_parser("trim")
    t.add_argument("--log", required=True)
    t.add_argument("--lines", type=int, default=30)
    args = p.parse_args(argv)
    if args.cmd == "snapshot":
        Path(args.output).write_text(json.dumps(snapshot(args.file, args.worktree), indent=2) + "\n")
        return 0
    return {"run": run, "check": check, "trim": trim}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())

---
name: night-shift
description: "Review, fix, and refactor a codebase in rounds until it comes back clean. A second model reviews; every fix gets a test that fails without it; each round is linted, tested, and committed. Use when asked to review and fix until clean, run a review loop, harden or refactor a codebase, or work through review findings overnight."
---

# Night shift

Run review and fix rounds on a codebase until a round comes back clean. Built
to run unattended: start it, go to sleep, wake up to a branch where every
change is tested and committed and the reviewer has nothing left to say.

## Inputs

Ask only for what you cannot work out. Default everything else.

- **Scope:** where the first round starts. A commit (`main`, a SHA, `HEAD~10`),
  a path, or the whole repository. Default: the whole repository.
- **Focus:** `bugs` (confirmed defects only), `refactor` (duplication, dead
  code, stale comments, anti-patterns, drift between twins), or `both`.
  Default: `both`.
- **Rounds:** a cap on rounds. Default: none; stop when the reviewer is clean.
- **Push:** whether you may push. Default: no. Commit locally; the person pushes.
- **Reviewer:** which tool reviews. Default: the first available that is a
  different model from the one you are (see Reviewer).

## Before the first round

1. **Learn the project's own commands.** Read the README, `AGENTS.md`,
   `CLAUDE.md`, `CONTRIBUTING`, and whatever builds the project (Makefile,
   `package.json`, Gradle, Cargo, SwiftPM, `pyproject.toml`, scripts folders).
   Find how it formats, lints, tests, and verifies before a merge. Use the
   project's scripts over raw tool calls. Write down the exact commands.
2. **Learn its rules.** Conventions, invariants, decision records, and any
   rule about commits or tests. These win over this skill.
3. **Check the ground.** The working tree is clean and the full test suite
   passes before you change anything. If it does not, stop and say so: you
   cannot tell your breakage from what was already broken.
4. **Branch.** Never work on the default branch. Create one if needed.

## A round

1. **Review.** Give the reviewer the scope (in round one, the starting scope;
   after that, only the commits made in the last round, as `git show <sha>` or
   `git log -p <from>..<to>`) and the focus. Ask for:
   - confirmed problems only, each verified against the code, at a severity
     that matters (a person could hit it, or it makes the code harder to
     change), with no style preferences and no speculation;
   - for each: severity, `file:line`, the problem, and the fix;
   - exactly `NO FINDINGS` when there is nothing.
2. **Verify each finding yourself** before acting on it. Read the code and
   the project's specs. A finding can be wrong, or contradict a documented
   rule; the rule wins. Drop what does not hold up and note why.
3. **Fix each finding** with the smallest change that removes it, matching the
   surrounding code. For a defect, first write a test that fails because of
   it. **Then check the test fails on the old code** (revert the fix, run the
   test, restore the fix): a test that passes either way proves nothing.
   Refactors keep behaviour; the existing tests are the proof, and you add
   tests first where a refactor touches code they do not cover.
4. **Fix twins together.** Where the same behaviour exists in two places (two
   platforms, a client and a server, a fake and the real thing), fix both.
5. **Gate and commit as one chain** that stops at the first failure:
   format, lint, test, commit, then the project's merge gate if it has one,
   then push if allowed. In shell: `lint && test && git commit … && gate &&
   git push`. Never `;` between them: a failed lint must not commit.
   Keep the working tree still while the gate runs.
6. **Write the commit message for a human:** what changed and why, in plain
   words. One commit per round is fine; split when fixes are unrelated.

Repeat until the reviewer answers `NO FINDINGS` for the last round's commits.

## Finishing

1. **One whole-repository pass.** Scoped rounds only see what changed. Ask the
   reviewer for one review of the whole codebase against the focus. This finds
   what rounds cannot: dead code, duplication across files, configuration that
   only breaks in release builds, lifecycle problems. Fix what it finds, then
   run scoped rounds on those fixes until clean again.
2. **Run the slow checks** the project keeps out of its everyday gate, if any:
   end-to-end or device tests, release builds. Say which ran and how.
3. **Report**, in plain words:
   - how many rounds, and what kinds of problems they found;
   - what changed, grouped by area, not by commit;
   - any decision you made that the person should check (a finding you
     rejected, a spec you followed over a reviewer);
   - what you could not verify, and why;
   - where the work is: branch, last commit, pushed or not, and the command
     to push if not.

## Reviewer

Use a different model from yourself, so the review is independent. Try, in
order, whichever is installed and is not you:

| Tool | Command |
| --- | --- |
| Codex | `codex exec --sandbox read-only --cd <repo> "<prompt>" < /dev/null` |
| Claude Code | `claude -p "<prompt>"` from the repo |
| Gemini CLI | `gemini -p "<prompt>"` from the repo |
| Antigravity CLI | `agy --print="<prompt>"` with `--add-dir <repo>` |
| Qwen Code | `qwen -p "<prompt>"` from the repo |

- Always close standard input (`< /dev/null`); some tools wait for input and
  hang a background run.
- Run the reviewer read-only where it can be. It reviews; you change code.
- Its output can be long. Read only its final answer.
- Review the parts of a large codebase in parallel (one reviewer per
  platform or package), each scoped to its own part.
- If no other model is installed, review yourself, in a fresh pass with the
  same prompt, and say so in the report.

## Rules

- **Stop and ask** before anything destructive or outward-facing that the
  person has not allowed: force pushes, deleting branches or data, publishing,
  changing infrastructure.
- **Never weaken a check to pass it.** Do not skip, delete, or loosen a test
  or lint rule to get green. Fix the cause.
- **Never claim more than you ran.** A step you skipped, a test you could not
  run, a finding you did not fix: say so.
- **Do not narrate.** While working, give short status lines. Save detail for
  the report.

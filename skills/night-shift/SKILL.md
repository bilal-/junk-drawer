---
name: night-shift
description: "Review, fix, and refactor a codebase in rounds, unattended, until a round comes back clean or the budget runs out. A second model reviews; every finding is verified before it is acted on; every bug fix gets a test that fails without it; refactors keep behaviour and go in their own commits; a findings ledger stops rounds re-raising rejected findings or undoing each other. Use when asked to review and fix until clean, run a review loop, harden or refactor a codebase, or work through review findings overnight."
---

# Night shift

Run review and fix rounds on a codebase until a round comes back clean. Built
to run unattended: start it, go to sleep, wake up to a branch where every
change is tested and committed, every rejected finding has a reason, and the
reviewer has nothing left worth fixing.

## Inputs

Ask only for what you cannot work out. Default everything else.

- **Scope:** where the first round starts. A commit (`main`, a SHA, `HEAD~10`),
  a path, or the whole repository. Default: the whole repository.
- **Focus:** `bugs`, `refactor`, or `both` (see What is worth changing).
  Default: `both`.
- **Bar:** `high` and `medium` findings (below), or `all` to fix confirmed
  minor ones too, such as a misleading name or a small duplication. Default:
  `high` and `medium`, which converges faster overnight.
- **Budget:** a cap on rounds, and on time or spend if the person gives one.
  Default: 8 rounds. Stop rules below can end the run sooner.
- **Push:** whether you may push. Default: no. Commit locally; the person pushes.
- **Reviewer:** which tool reviews. Default: the first available that is a
  different model from the one you are (see Reviewer).

## Before the first round

1. **Learn the project's own commands.** Read the README, `AGENTS.md`,
   `CLAUDE.md`, `CONTRIBUTING`, and whatever builds the project. Find how it
   formats, lints, tests, and verifies before a merge. Use its scripts over raw
   tool calls. Write down the exact commands.
2. **Learn its rules.** Conventions, invariants, decision records, rules about
   commits or tests. These win over this skill and over any reviewer.
3. **Check the ground.** The working tree is clean and the full test suite
   passes before you change anything. If not, stop and say so: you cannot tell
   your breakage from what was already broken. Note any test that fails only
   sometimes.
4. **Branch.** Never work on the default branch.
5. **Start the log and ledger** in `$(git rev-parse --git-dir)/night-shift/`,
   which git never tracks: `log.md` (one entry per round) and `ledger.md` (one
   line per finding). Record the starting commit and the test count.

## What is worth changing

Reviewer and fixer both use this list. A finding must name which item it is.

**Worth changing:**
- **Defects** a user or caller can hit: wrong results, crashes, data loss,
  races, leaks, swallowed errors, security holes, broken edge cases (empty,
  missing, boundary, encoding, time, concurrency), release-only configuration.
- **Drift between twins:** the same behaviour in two places (platforms, client
  and server, a fake and the real thing) that no longer agrees.
- **Duplicated knowledge:** one rule written in three or more places, or in
  two that must change together or already disagree.
- **Dead code:** unreachable or unused, confirmed by searching every caller,
  including reflection, configuration, templates, and other packages.
- **Comments, names, and docs that are false** or mislead.
- **Shallow layers:** wrappers and pass-throughs that add interface without
  hiding anything; one decision spread across several modules.
- **Tests that cannot fail:** no assertion, asserting on a mock's own answer,
  a bug fix with no test.

**Not worth changing:**
- Anything the formatter or linter owns, and taste: "consider", "could",
  "cleaner", "more idiomatic".
- Two similar pieces that change for different reasons. A wrong abstraction
  costs more than the duplication; wait for the third copy.
- New layers, interfaces, options, or generality for a need nobody has.
- Splitting code only because it is long, when it reads as one idea.
- Anything observable from outside the module: public API, CLI flags and
  output, file and wire formats, error messages, ordering, defaults. Someone
  depends on it. Changing it is a behaviour change, only with the person's
  say-so.
- Rewrites, or anything that cannot be done in small behaviour-keeping steps.
- Speculative bugs: "might", "could", with no path from an input to a failure.
- Undoing a change made earlier in this run, or re-raising a finding the
  ledger rejected, without new evidence.

## A round

1. **Review.** Give the reviewer:
   - the scope: in round one the starting scope; after that only the last
     round's commits (`git log -p <from>..<to>`), with read access to the
     repository so it can see the surrounding code;
   - the focus, the list above, and the project's rules files;
   - the ledger's rejected and contested entries, marked "do not re-raise
     without new evidence".

   Ask for findings only at **high** (a user or caller can hit it, or data or
   security is at risk) or **medium** (it makes correct change harder, from
   the list above), plus **low** (confirmed, small, from the list) when the bar
   is `all`. For each: severity, list item, `file:line`, evidence (for a
   defect, the input or path that triggers it; for duplication, every copy),
   and the fix. Exactly `NO FINDINGS` when there are none.
2. **Triage against the ledger.** Drop repeats of rejected findings. If a
   finding would undo a fix from this run, do not flip back: decide it once on
   the evidence, and if it comes back again mark both sides `contested` and
   leave them for the person.
3. **Verify each finding.** Reviewers are often wrong, and agreement between
   models is not evidence. Do not defer to a confident tone.
   - **Defect:** reproduce it with a test. If you cannot make a test fail, the
     finding is unconfirmed: reject it and say why.
   - **Structure:** check it against the list; confirm usages by searching.
   - A documented project rule beats the reviewer.

   Write each verdict to the ledger: id, round, `file:line`, one-line summary,
   then `fixed <sha>`, `rejected: <reason>`, `contested`, or `deferred: <reason>`.
4. **Fix, keeping behaviour and structure apart.**
   - **Behaviour change** (bug fix): the failing test first, then the smallest
     fix. **Check the test fails on the old code** (revert the fix, run it,
     restore): a test that passes either way proves nothing. The test asserts
     what a caller sees, not how the code does it.
   - **Structure change** (refactor): no behaviour change. The existing tests
     stay as they are (except call sites of something renamed) and pass before
     and after. Where the code is not covered, first add tests that pin what it
     does today, in their own commit. Take small steps and run the tests
     between them.
   - Never mix the two in one commit. If a fix needs a tidying first, commit
     the tidying, then the fix.
   - **Fix twins together.**
   - **Stay in scope.** No drive-by edits. Something else you notice goes in
     the ledger as `noticed`, or becomes its own finding if it is a defect.
   - **Prefer replacing and deleting to adding.** If one finding's change grows
     past a few hundred lines or a dozen files, stop, discard it, and record it
     as `deferred: too large for an unattended change`.
5. **Check the diff for gamed tests** before every commit. Look for deleted,
   skipped, or disabled tests; loosened assertions or tolerances; changed
   expected values; raised timeouts; production code that special-cases a
   test; new lint suppressions, coverage exclusions, or `|| true`. Each must be
   justified in the commit message (for example, tests of code you deleted), or
   undone. The test count must not fall below the baseline without that.
6. **Gate and commit as one chain** that stops at the first failure: format,
   lint, test, commit, then the project's merge gate if it has one, then push
   if allowed. In shell: `lint && test && git commit … && gate && git push`.
   Never `;` between them: a failed lint must not commit. Keep the working tree
   still while the gate runs. Run the full suite, not just the new test.
7. **Write the commit message for a human:** what changed and why, in plain
   words, and whether it changes behaviour. One commit per finding, or per
   group of the same structural change.
8. **Log the round:** findings raised, fixed, rejected; commits; time.

## Stop rules

End the rounds at the first of:

- **Clean:** for the last round's commits, the reviewer says `NO FINDINGS`, or
  everything it raised was rejected or was a ledger repeat.
- **Budget:** the round, time, or spend cap.
- **No progress:** two rounds in a row where every finding was rejected (the
  reviewer is producing noise), or three rounds where findings do not fall
  because each round's fixes create the next round's findings.
- **Oscillation:** a finding comes back contested a second time.
- **Broken ground** you cannot recover from (below).

Then finish. Say which rule ended the run.

## When things break

- **The gate fails on your change:** fix the cause, two attempts at most.
  Otherwise discard the uncommitted change back to the last green commit,
  record the finding as `deferred: <what failed>`, and move on.
- **A committed change turns out wrong:** `git revert` it as a new commit.
  Never rewrite history the person may have.
- **A test fails sometimes:** rerun it once. If it also fails on the starting
  commit, it was already flaky: record it, do not skip or loosen it.
- **A tool hangs or errors:** put a time limit on every reviewer call; retry
  once, then use the next reviewer.
- **The session dies:** a new session reads `log.md` and `ledger.md`, runs
  `git status` and `git log <start>..`, runs the gate on `HEAD`, and carries on
  from the next round.
- **Never leave the tree dirty.** Whenever you stop, for any reason, the tree is
  clean and `HEAD` passes the gate. Uncommitted work that does not pass is
  discarded and recorded in the ledger, not left behind.

## Finishing

1. **One whole-repository pass,** if the budget allows. Scoped rounds only see
   what changed. Ask the reviewer for one review of the whole codebase against
   the focus and the list, with the ledger. This finds what rounds cannot:
   dead code, duplication across files, configuration that only breaks in
   release builds, lifecycle problems. Fix what holds up, then run scoped
   rounds on those fixes under the same stop rules.
2. **Run the slow checks** the project keeps out of its everyday gate, if any:
   end-to-end or device tests, release builds. Say which ran and how.
3. **Report**, in plain words:
   - rounds run, which stop rule ended them, and what kinds of problems they
     found;
   - what changed, grouped by area, not by commit, with behaviour changes
     listed apart from structural ones;
   - decisions the person should check: rejected findings and why, contested
     findings, anything that touches observable behaviour, a spec followed over
     a reviewer;
   - what is left: deferred and noticed items from the ledger;
   - what you could not verify, and why;
   - where the work is: branch, last commit, pushed or not, the command to
     push if not, and the path of the log and ledger.

## Reviewer

Use a different model from yourself: models judge their own output too kindly.
Try, in order, whichever is installed and is not you:

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
- Start a fresh reviewer each round, so it does not argue for its earlier
  findings; the ledger carries what it needs to know.
- Missing context causes false findings: let it read the repository, not only
  the diff.
- Its output can be long. Read only its final answer.
- Review the parts of a large codebase in parallel (one reviewer per platform
  or package), each scoped to its own part.
- If no other model is installed, review yourself in a fresh pass with the
  same prompt, and say so in the report.

## Rules

- **Stop and ask** before anything destructive or outward-facing that the
  person has not allowed: force pushes, deleting branches or data, publishing,
  changing infrastructure, adding dependencies.
- **Never weaken a check to pass it.** Do not skip, delete, or loosen a test or
  lint rule, or special-case a test, to get green. Fix the cause.
- **Never claim more than you ran.** A step you skipped, a test you could not
  run, a finding you did not fix: say so.
- **Do not narrate.** While working, give short status lines. Save detail for
  the report.

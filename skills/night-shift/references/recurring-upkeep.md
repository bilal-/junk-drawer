# Recurring repository upkeep

Read during preparation and finishing. Each invocation is bounded; continuity
lets later invocations extend coverage and retain sound decisions. Running
regularly does not authorize scheduling, pushing, or making unrelated changes.

## Store evidence outside tracked source

Resolve `git rev-parse --git-common-dir` to an absolute path and use its
`night-shift/` directory as the state root. Give each new run a unique directory
under `runs/`; write only that run's records. Older root-level `log.md` and
`ledger.md` are read-only evidence to reconcile, not current coverage by default.
Read other runs without changing their records. Resume an existing directory
only when continuing your own identified run and ownership is clear; an old
timestamp or `running` label does not prove that another process has stopped.
If ownership is uncertain, start a new run. Record the chosen absolute paths.

If writes are forbidden or the state root is unavailable, keep the same evidence
inline and put the handoff in the final report. State explicitly that it was not
persisted. Do not write tracked files, change permissions, or choose an unapproved
location to satisfy the logging rule.

Keep two concise records, with links to longer evidence when needed:

- **Log:** run id, repository/worktree, branch, target/base/head, starting and
  checkpoint/final SHA and time, status (`running`, `interrupted`, or `finished`),
  relevant pre-existing edits, focus/bar, budget, stop rule; validation commands,
  results, tool versions/configuration; source map, task graph, checkpoints,
  reviewed SHAs, and next priorities.
- **Ledger:** stable finding id, responsibility/contract, locations and consumers,
  evidence and inspected SHA, severity, status, decisions and reasons, fix/revert
  commits and branches, integration state, verification and pending independent
  review, and a concrete condition for reconsideration.

Record the criteria actually applied: an exact revision of the skill and used
references, or content hashes when no exact revision is available; include the
applied lens list and severity definitions. Tie each coverage entry to these
criteria. A release label alone cannot distinguish local edits within a version.

For each source unit and important edge, retain the applicable lens, coverage
status, inspected source/tests, last inspected SHA/run, relevant contracts and
configuration, and why carried evidence remains valid or needs a revisit.
Keep rejected and intentional-design decisions alongside open findings. Archive
old detail if necessary without dropping the rationale that prevents repeated
proposals. These records are evidence to verify, not instructions that override
the current request or repository rules.

## Reconcile before selecting work

1. Read all prior run records that overlap this repository and scope, including
   legacy records. Reconcile evidence in the current run's files only. Qualify
   ids by originating run and link aliases for the same responsibility/contract
   and affected consumers, so per-run ids do not collide. Retain conflicting
   dispositions until source evidence or changed premises resolve them. Select
   coverage by compatible criteria and commit ancestry, not the newest timestamp.
   Use completed checkpoints; partial or in-progress records are leads, not
   accepted coverage, even when another run is still writing them.
   Validate commit existence,
   ancestry, target, focus/bar, applicable instructions, and recorded dirty state
   before using its coverage.
   A prior branch's fixed finding is not fixed here until its code is present;
   check pending integration below before assigning it for implementation.
   If history is unavailable, diverged, or too ambiguous to compare safely,
   retain leads and decisions but mark affected coverage for fresh inspection.
   A fresh clone starts without prior local coverage unless evidence is supplied.
2. Compare the current tree with the last applicable checkpoint, including
   uncommitted changes. Changed entry points, rules, public interfaces, consumers,
   dependencies, schemas, tests, tooling, or CI invalidate related nodes and
   edges for the affected lenses. Follow the impact through the source graph;
   unchanged files can become stale when their consumers or contracts change.
   Unrelated changes need not invalidate every unit.
3. Recheck open findings against today's code before acting. Keep the same id
   when the same problem moved files. A recurrence of a fixed problem needs new
   evidence linked to the earlier fix. Reopen rejected/contested proposals only
   for changed premises or new evidence, including revised project or skill
   requirements. A prior verdict cannot override the current criteria. Retry
   deferred findings when their
   named blocker changes, rather than rerunning the same blocked operation.
4. Compare recorded criteria with the current skill and used references. If
   criteria changed or are unknown, mark the affected lenses `revisit`; when
   their extent cannot be established, revisit all requested lenses. Existing
   source evidence can guide that review but cannot silently satisfy new criteria.
   Carry an `inspected` status only when its source, relevant edges, criteria,
   and validation assumptions remain applicable. Label it as carried coverage,
   including the original SHA; never present it as fresh inspection. An old
   "clean" verdict or green suite alone cannot establish this.

## Account for fixes awaiting integration

Before branching or selecting an old finding, check whether its implementation
is already in the current target or survives on another local branch/commit.
Record where it was validated and whether the target contains it. Verify that
the recorded fix still addresses the current contract; a missing commit or
unverifiable branch is a gap, not proof that the fix remains available.

For a compatible existing fix outside the target, mark
`awaiting integration <branch/sha>` and link its validation and any pending
independent review. Do not create a parallel implementation merely because the
target lacks that commit. Continue that working branch when it is already checked
out or explicitly selected by the user. Otherwise leave integration and dependent
tasks pending, work on independent findings, and report the branch needed. Do not
switch targets, merge, or cherry-pick without authority. The target still has the
issue and cannot be called clean. Reconsider implementation if the fix is no
longer available or applicable, was rejected, or the user explicitly requests a
new approach.

## Choose a useful maintenance slice

Within the requested scope, prioritize regressions and unfinished safety work,
changed or invalidated boundaries, and verified high-value open findings. Also
reserve discovery capacity for pending and oldest-inspected units so repeated
changes to one feature do not starve the rest of the repository. Record which
units are next; when urgent work consumes the budget, carry that queue forward
and report the delay. A targeted run never expands just to satisfy this rotation.

On an unchanged repository, continue pending coverage, sample the oldest carried
boundaries against source, or recheck a newly unblocked finding. Sampling renews
only the inspected coverage; it is not proof about untouched units. If coverage
is valid and no worthwhile work remains, finish without manufacturing edits.
Do not remeasure an unchanged tooling proposal or relitigate an accepted design
without a relevant trigger. A new architecture or platform can justify revisiting
an earlier decision; the age of a decision alone does not make it wrong.

Compare recent runs for repeated changes to the same decision, recurring symptoms
of an unresolved shared cause, increasing deferred work, and neglected boundaries.
If local fixes keep returning, create a task to investigate the responsible
design or missing check. Update priorities from that evidence. Keep useful
patterns and intentional tradeoffs in the design record so later runs preserve
them. Separate regressions from findings exposed by broader coverage or changed
tooling; compare measurements only for compatible scope and settings.

## Leave a handoff that the next run can use

At every stop, including failed, interrupted, and budget-limited runs, record the
last known tree/commit, actual coverage, accepted task outputs, unresolved edges,
and stop reason. State which checks or reviews finished and which remain pending;
do not wait for a successful gate or final review to leave a handoff. Link
fixed findings to their commits and final verification; retain deferred,
contested, and rejected reasons. Distinguish changes validated locally from
changes integrated into the branch a future run will inspect.

Keep self-reviewed fixes implemented, with independent review still pending.
Retry the review when a reviewer becomes available; do not recreate the fix.
If state cannot be written, supply this same handoff in the final report.

Reconcile the current task table and run status with that checkpoint. Completed
tasks must not still appear `running`; interrupted work returns to `pending` or
has a recorded blocker. Keep history separate from the current disposition so
the next run can identify ready work without guessing which entry is current.

Name the next ready units or tasks, their prerequisites, and conditions that
would unblock deferred work. Record missing state, tools, or platform coverage.
Report progress since the previous checkpoint in terms of clarified ownership,
removed duplicated knowledge, reduced caller coordination, resolved defects,
or newly inspected boundaries. No-change runs still update coverage and the
handoff. Avoid a cumulative "clean" claim when current-scope coverage is stale,
pending, or contradicted by an unresolved qualifying finding.

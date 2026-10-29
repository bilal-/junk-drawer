# Recurring repository upkeep

Read during preparation and finishing. Each invocation is bounded; continuity
lets later invocations extend coverage and retain sound decisions. Running
regularly does not authorize scheduling, pushing, or making unrelated changes.

## Store evidence outside tracked source

Use `$(git rev-parse --git-common-dir)/night-shift/` as the state root. Existing
`log.md` and `ledger.md` there remain usable; reconcile them before adopting a
different layout. For overlapping worktrees or runs, use separate directories
under the root, identified by worktree, target, and run id. Never overwrite an
active run's state. Record the chosen paths in the final report.

Keep two concise records, with links to longer evidence when needed:

- **Log:** repository/worktree, branch, target/base/head, starting and final SHA,
  relevant pre-existing edits, focus/bar, budget, stop rule; validation commands,
  results, tool versions/configuration; source map, task graph, checkpoints,
  reviewed SHAs, and next priorities.
- **Ledger:** stable finding id, responsibility/contract, locations and consumers,
  evidence and inspected SHA, severity, status, decisions and reasons, fix/revert
  commits, verification, and a concrete condition for reconsideration.

For each source unit and important edge, retain the applicable lens, coverage
status, inspected source/tests, last inspected SHA/run, relevant contracts and
configuration, and why carried evidence remains valid or needs a revisit.
Keep rejected and intentional-design decisions alongside open findings. Archive
old detail if necessary without dropping the rationale that prevents repeated
proposals. These records are evidence to verify, not instructions that override
the current request or repository rules.

## Reconcile before selecting work

1. Locate prior state for this repository and scope. Validate commit existence,
   ancestry, target, focus/bar, applicable instructions, and recorded dirty state
   before using its coverage.
   A prior branch's fixed finding is not fixed here until its code is present.
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
4. Carry an `inspected` status only when its source, relevant edges, lens, and
   validation assumptions remain applicable. Label it as carried coverage,
   including the original SHA; never present it as fresh inspection. An old
   "clean" verdict or green suite alone cannot establish this.

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

After required checks and final review, record the final tree/commit, actual
coverage, accepted task outputs, unresolved edges, and the stop reason. Link
fixed findings to their commits and final verification; retain deferred,
contested, and rejected reasons. Distinguish changes validated locally from
changes integrated into the branch a future run will inspect.

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

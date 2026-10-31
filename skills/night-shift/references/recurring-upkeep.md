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

Record ownership and checkout ownership are separate. Before editing, checking,
committing, or recovering changes, establish that another run cannot mutate the
same editable worktree during those operations. A new log directory does not
grant that ownership. When uncertain, use a separate worktree and branch from a
fixed target snapshot; do not copy an actively changing dirty tree or switch the
other run's branch. If safe isolation is unavailable, continue read-only and
report the blocker. Reconcile another run's active work before selecting the same
finding for a parallel implementation.

If writes are forbidden or the state root is unavailable, keep the same evidence
inline and put the handoff in the final report. State explicitly that it was not
persisted. Do not write tracked files, change permissions, or choose an unapproved
location to satisfy the logging rule.

Keep two concise records, with links to longer evidence when needed:

- **Log:** run id, repository/worktree, branch, target/base/head, starting and
  checkpoint/final SHA and time, status (`running`, `interrupted`, or `finished`),
  relevant pre-existing edits, focus/bar, budget, stop rule; validation commands,
  results, tool versions/configuration; source map, task graph with parent/child
  assignments and report links, checkpoints,
  reviewed SHAs, reconciled run/checkpoint identities, and next priorities.
- **Ledger:** stable finding id, responsibility/contract, locations and consumers,
  evidence and inspected SHA, severity, status, decisions and reasons, fix/revert
  commits and branches, integration state, verification and pending independent
  review, and a concrete condition for reconsideration.

Give each published checkpoint an id or content hash that changes when its
summary changes. A commit SHA alone cannot identify an audit-state checkpoint.

Record the criteria actually applied: an exact revision of the skill and used
references, or content hashes when no exact revision is available; include the
applied lens list and severity definitions. Tie each coverage entry to these
criteria. A release label alone cannot distinguish local edits within a version.

For each source unit and important edge, retain the applicable lens, coverage
status, inspected source/tests, last inspected SHA/run, relevant contracts and
configuration, and why carried evidence remains valid or needs a revisit.
Keep rejected and intentional-design decisions alongside open findings. In the
current run, consolidate their reasons and link historical detail rather than
copying every earlier transcript. Preserve compact ids/links for resolved work.
Do not rewrite, move, or delete another run's records to compact history. These
records are evidence to verify, not instructions that override the current
request or repository rules.

## Reconcile before selecting work

1. Use compact run metadata to locate the latest consolidated finished
   checkpoint(s) compatible with this target and ancestry. Read those summaries
   and overlapping checkpoints they have not reconciled, including concurrent,
   interrupted, or legacy records. Read older covered records only to retrieve
   missing evidence or decision reasons. Record exactly which run/checkpoint
   identities the new summary incorporates; a later checkpoint from the same
   run is new evidence, not silently covered by its run id. Do not declare a
   live run wholly superseded. Parent checkpoint references can cover their
   reconciled ancestors transitively; do not duplicate the full ancestry list.
   Keep this reconciliation within the run budget;
   report unread relevant state and defer decisions depending on it.
   Reconcile in the current run's files only. Qualify finding ids by originating
   run and link aliases for the same responsibility/contract and consumers.
   Retain conflicting dispositions until evidence or changed premises resolve
   them. Select coverage by criteria and ancestry, not the newest timestamp.
   Only completed checkpoints supply accepted coverage; partial records are leads.
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
its implementation fixed and report `awaiting integration <branch/sha>` for the
current target; link its validation and any pending independent review. Do not
create a parallel implementation merely because the
target lacks that commit. Continue that working branch when it is already checked
out or explicitly selected by the user. Otherwise leave integration and dependent
tasks pending, work on independent findings, and report the branch needed. Do not
switch targets, merge, or cherry-pick without authority. The target still has the
issue and cannot be called clean. Reconsider implementation if the fix is no
longer available or applicable, was rejected, or the user explicitly requests a
new approach.

## Choose work without shrinking coverage

Reconcile the whole requested scope at each run. Prioritize regressions and
unfinished safety work, changed or invalidated boundaries, and pending or
oldest-inspected units when ordering discovery. This ordering does not limit the
scope to a maintenance slice: schedule every pending/revisit unit within the
round's discovery sweep. Valid carried evidence can satisfy unchanged areas;
record that reuse rather than claiming a fresh scan. A targeted run never expands
just to satisfy rotation.

Select a bounded improvement batch after scope-wide discovery and synthesis.
When urgent safety work interrupts discovery, retain and resume its queue.
When time/spend, unavailable evidence, or another real stop condition prevents
full coverage, name the missing areas and carry their tasks forward. A new run
or a new subtree does not reset the inventory or its unfinished obligations.

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

Leave a consolidated checkpoint with the current coverage, open findings,
decision reasons, integration/review gaps, and identities of reconciled older
checkpoints. Keep its metadata compact and distinguish fully incorporated
history from unread or partially reconciled records. The next run should not
need to reload every earlier log to reconstruct these decisions.

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

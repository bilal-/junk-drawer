---
name: "night-shift"
description: "Autonomously audit or improve a whole repository by default, or a user-specified branch, PR, commit range, path, or feature. Uses bounded sub-agent discovery and cross-unit synthesis to find architectural maintenance problems, defects, duplication, and repeated hot-path work. For improvement runs, makes small tested commits and seeks independent review. Tracks scope coverage and findings across rounds. Use for recurring codebase maintenance or focused review and refactoring of a supplied target."
---

# Night shift

Work through the requested target autonomously, finding concrete obstacles to
understanding and changing it. For improvement runs, leave a tested, committed
branch. For audits, leave a source-backed findings report. In both cases,
account honestly for what remains.

Discovery and regression review are separate jobs. A clean review of your last
commits does not mean the untouched codebase has been assessed. Continue through
the original scope until no worthwhile work remains or a stop rule applies.

## Inputs

Ask only for information that blocks the work. Infer the rest and record the
choice. Routine refactoring decisions are yours to make within the user's scope.

- **Scope:** the whole repository when the user supplies no target. Otherwise use
  the supplied branch, PR, commit or commit range, path, feature, or package.
  Resolve change targets to fixed base and head SHAs. For "since X," use X as
  the base; for one commit, use its parent; for a branch or PR, use the stated
  base or infer its merge base with the default/upstream branch. Record the
  choice. For a change target, review the diff plus affected callers,
  dependencies, contracts, platform counterparts, and existing implementations
  of newly added rules. A path or feature target includes its relevant
  boundaries. Inspecting adjacent code does not turn a targeted run into a
  whole-repository sweep.
- **Action:** an audit or review request reports findings without editing; a
  night-shift, fix, improve, or refactor request also implements verified
  in-scope findings. For a change target with fixes authorized, edit necessary
  related consumers or shared contracts to complete a finding from that change;
  leave unrelated cleanup for a repository sweep. Respect any narrower edit
  boundary the user gives.
- **Focus:** `bugs`, `refactor`, or `both`. Default: `both`. Structural discovery
  is required for `refactor` and `both`; do not let bug hunting replace it.
  Inspect repeated hot-path work in relevant units for any focus unless the
  user explicitly excludes performance.
- **Bar:** confirmed high and medium findings by default; `all` includes low
  findings. High means a reachable correctness, data, or security risk. Medium
  includes demonstrated maintenance difficulty or repeated runtime cost on a
  reachable path that scales with normal use. Low means a small, confirmed
  improvement. Taste is not a finding at any bar.
- **Budget:** the user's round, time, or spend cap; default 8 rounds. An
  improvement round is a discovery-and-change batch followed by review; an
  audit round is discovery and independent validation of findings and coverage.
  Reviewing corrections
  consumes another round; no unbounded inner review loop. Preparation, tests, and
  reviewers consume the same time/spend budget. Reserve enough to validate and
  leave a clean tree; do not start work you cannot safely finish.
- **Push:** no by default. Commit locally; push only when authorized.
- **Reviewer:** an available different model; see Reviewer below.

## Prepare

1. **Learn the project.** Read applicable `AGENTS.md`, `CLAUDE.md`, README,
   `CONTRIBUTING`, build configuration, and relevant design documents. Project
   rules and contracts beat generic advice or a reviewer's preferences. Learn
   the project's exact format, lint, build, type-check, and test commands; prefer
   its scripts. Do not install tooling just to run this skill.
2. **Identify targets.** Map first-party packages, entry points, framework
   versions, deployment hosts, native targets, and data/services. Use
   [stack detection](references/stack-detection.md), its common checks, and only
   the linked sections relevant to the scope. Use available specialist guidance
   when helpful; another skill is not required.
3. **Establish baseline.** Record the starting tree and run the required project
   gate, including its full required test suite. Record commands, test count,
   platforms, build configurations, and results. A failing or unavailable gate
   blocks edits whose safety depends on it; an audit-only run can continue
   read-only and report the gap. Separate optional checks from required ones.
   Missing optional device or integration checks need not stop unrelated work,
   but defer changes whose safety depends on them.
4. **Use a working branch for edits.** Never change the default branch directly.
   Audit-only runs do not create commits.
5. **Start or reconcile the log and ledger** in
   `$(git rev-parse --git-common-dir)/night-shift/`, outside tracked files.
   `log.md` records starting SHA, target/base/head, budget, scope map,
   validation matrix, rounds, and checkpoints. `ledger.md` records ranked
   findings and history. Reuse relevant prior findings and coverage for recurring
   runs when available; recheck them against changed code. In a fresh clone,
   record that prior coverage was unavailable rather than inventing continuity.
   Keep both files concise enough to resume from.
6. **Map the original scope into meaningful review units:** packages, features,
   subsystems, or connected modules, not arbitrary file-count chunks. Record
   each unit's responsibility, entry points, dependencies, state/resource
   owners, checks, and coverage status per applicable lens (architecture,
   defects, hot paths): `pending`, `inspected`, or `revisit`.
   Exclude generated and third-party code unless specifically in scope; inspect
   its contracts when relevant. Reading a directory listing or README is not
   source review. In a large repository, work through units across rounds.

7. **Plan discovery.** Read the
   [discovery graph](references/discovery-graph.md). Mark connected review units
   and boundary flows in the target. In each round, spawn available sub-agents
   for a bounded batch with entry points, edges, lenses, and read-only reporting
   instructions. Synthesize their reports across boundaries before choosing
   changes. The lead owns findings, edits, tests, and final coverage. If agents
   are unavailable, follow the graph sequentially without claiming independent
   coverage.

## Find worthwhile refactors

For `refactor` or `both`, read the [refactoring guide](references/refactoring.md).
Examine architecture as well as individual functions. Trace representative
flows from entry point through domain logic, storage or external services, and
back; include error, cancellation, and cleanup paths. Inspect the code, its
callers, tests, and relevant history. Look across package and platform boundaries
for the same rule implemented separately.

Prioritize problems that amplify changes or force callers to understand too
many details:

- Duplicated knowledge and drift between implementations of the same contract.
- One decision or invariant scattered across modules; repeated caller-side
  coordination; leaking implementation details.
- Mixed responsibilities, misplaced ownership, dependency cycles, and coupling
  that violates an established boundary or spreads one concern across unrelated
  modules.
- Shallow wrappers, speculative abstraction, flag-heavy generalization, and
  excessive indirection that add more complexity than they hide.
- Tangled control flow, repeated state synchronization, and inconsistent
  representations that make a concrete operation hard to reason about.
- Confirmed dead code, misleading names or documentation, and tests that cannot
  detect the failures they claim to cover.

A smell is a search lead, not a verdict. Give concrete locations and explain
what is difficult today: which callers repeat a sequence, which copies must
change together, which dependency exposes an implementation detail. Complexity
scores, file length, similarity, and fashionable architecture labels alone do
not justify an edit.

Architectural refactoring is in scope: move a responsibility to its owner,
consolidate a rule, simplify a module's interface, separate unrelated concerns,
or remove an unnecessary dependency. Implement it in behaviour-preserving
steps using the project's conventions. Do not turn this into a framework,
state-library, or architectural-style migration. Internal interfaces may change
when their affected consumers migrate safely; identify the actual external
consumer boundary rather than treating every helper signature as immutable.

Avoid cosmetic churn, abstractions for hypothetical consumers, and merging
similar-looking code that changes for different reasons. Preserve useful
adapters, compatibility paths, and test seams. Public APIs, wire/file formats,
error behaviour, ordering, defaults, and UI state lifetime are contracts; changing
them requires a confirmed defect within bug-fix scope or separate authorization.

Structural review must connect local responsibilities into an end-to-end view:
who owns each invariant and resource, which callers coordinate it, and what must
change together across packages or platforms. Local cleanup is not a substitute
for resolving a confirmed cross-unit problem. An invalid UI test that no longer
exercises its claimed interaction is a finding even when the baseline suite is
green; verify the mismatch and repair or remove it within scope.

## Find hot-path costs

Inspect repeated work in UI and request-serving units for any focus unless
performance was explicitly excluded.
Read [hot-path discovery](references/hot-paths.md). Trace per-frame, per-row,
per-appearance, or per-request work and its scale. Enter evidence-backed
candidates in the ledger before measurement; require repeatable comparison
before keeping a performance change. Record unusually large assets and
hand-built infrastructure when they contribute to the cost. A maintained
third-party library may be a deferred option, not an automatic dependency
change. This lens complements, and never replaces, structural discovery.

## Each round

For audit-only runs, perform discovery, verify candidate findings against
source, obtain independent review of findings and coverage, and report. Skip
implementation, commit, and change-recovery steps.

### 1. Discover and rank

Dispatch the next bounded batch of units and boundary flows from the target.
Reconcile agent reports into one ledger and verify candidates against source.
For change targets, search the repository for existing equivalents of rules,
helpers, types, and mappings added or altered by the diff. Mark findings as
introduced, worsened, or pre-existing; prioritize the first two. Track
architecture and hot-path coverage separately where applicable. A clean
file-level report does not establish a clean cross-unit design.

Inspect the next connected part of the original scope, prioritizing central
flows, known duplication, and risky boundaries. Carry forward unresolved review
findings. Even if the previous diff was clean, keep discovering while units
remain pending. Revisit units when changes affect their contracts or ownership.
For a bugs-only run, use the same coverage discipline to seek reachable defects.

Add evidence-backed candidates to the ledger. Rank by user/caller risk, reduction
in change amplification or reasoning burden, confidence, and verification cost.
Prefer a substantive, provable improvement over a collection of easy renames.
Do not manufacture work to fill the budget.

For each finding, record an id, severity, locations and consumers, evidence,
expected payoff, and status. Use `candidate`, `verified`, `in-progress`,
`fixed <sha(s)>`, `rejected: <reason>`, `contested: <reason>`, or
`deferred: <reason>`. Notice unrelated issues without editing outside scope.
Rejected and contested entries accompany future reviews; reopen only with new
evidence. If a proposal would undo an earlier change, resolve the disagreement
on evidence once; do not alternate between designs.

### 2. Verify and plan the selected work

Check the finding yourself; a confident reviewer is not proof.

- **Defect:** identify the input and execution path, then reproduce it with a
  failing regression test. Without a reproducer, reject or defer it as unproven.
- **Performance:** identify a reachable repeated path and establish its cost
  with a comparable workload before changing it. When frame timing is
  unavailable, deterministic work counts can prove repeated parsing, decoding,
  hashing, or retries; do not claim a latency gain from counts alone.
- **Structure:** confirm the relevant usages, copies, ownership, and boundaries.
  Before deleting or renaming, check configuration, reflection, registration,
  templates, generated consumers, external interfaces, and platform counterparts.

For a structural finding, record a short plan:

- **Payoff:** the repeated rule, caller coordination, mixed responsibility, or
  indirection being removed, and the intended owner/interface afterwards.
- **Invariants:** inputs, outputs, errors, side effects and order, state identity,
  lifetimes, cancellation, resource ownership, and compatibility that must stay.
- **Proof:** existing tests and any missing characterization or integration
  coverage needed to establish those invariants; relevant target checks.
- **Steps:** independently useful changes that each leave the project green,
  with a rollback point. For a wide change, introduce a compatible seam, migrate
  callers in bounded groups, then remove the old path once usage is checked.

For a consequential ownership or interface change, compare the proposal with
a simpler local extraction, consolidation, or deletion. Choose the least complex
design that removes the demonstrated problem, rather than a new abstraction by
default. This is an implementation decision, not a reason to pause for approval.

Choose a coherent improvement or a small set of independent findings that fits
within the remaining budget. If preservation cannot be established with available
checks, defer that finding and continue safe work elsewhere.

### 3. Implement in small green steps

- **Refactor:** where coverage is insufficient, first add tests that pin today's
  behaviour, run them against unchanged production code, and commit them
  separately. Test meaningful contracts and edge cases; do not mirror private
  implementation. Preserve existing behavioural assertions. Then restructure,
  running focused checks between steps. Do not require new tests for a proven
  mechanical rename already covered by suitable checks.
- **Bug fix:** failing test first, then the smallest fix. Confirm that the test
  fails without the fix and passes with it. Assert what the caller observes,
  rather than a mock's own answer. Commit the test and fix together.
- Keep structural and behavioural changes in separate commits. If a bug needs
  tidying first, commit the tested tidy, then the fix. In a refactor-only run,
  record pre-existing defects; always repair or revert regressions you introduce.
- Fix all in-scope copies of an affected shared contract. Preserve intentional
  platform/domain differences. If a necessary consumer is outside edit scope,
  retain compatibility or defer; do not silently widen scope.
- Prefer removing complexity and reusing suitable existing concepts over adding
  layers. Make extractions cohesive, with explicit dependencies and ownership.
  Do not move a large tangle behind a new name and call it improved architecture.
- Keep each step reviewable. Split a broad change into independently green
  commits; defer a rewrite that cannot be split safely. For mechanical fan-out,
  use an available symbol-aware rename or codemod, preview its changes, inspect
  all affected consumers, and run their checks. Tooling does not prove equivalence.
- Performance changes need a repeatable baseline and comparison on the same
  workload and build. Do not add caching, memoization, or concurrency on intuition.

### 4. Check integrity, gate, and commit

Before every commit, inspect the diff for deleted/skipped tests, loosened
assertions or tolerances, changed expected values, raised timeouts, test-specific
production paths, lint suppressions, coverage exclusions, and `|| true`. Undo
anything added merely to make checks pass. Legitimate removals or mechanical
updates need a reason; test count must not silently fall below baseline.

Run the required gate and full required suite, plus the affected target checks
from the validation matrix. Focused tests do not replace these. Keep the tree
still while checks run. Commit only on success; stop the command chain at the
first failure. If a project gate requires a clean tree, use a provisional local
commit and undo that commit with `git reset --soft HEAD~1` if it fails; only do
this for your own unpublished commit, then apply the recovery rules.

Commit per finding or independently useful step. Explain what changed, why the
structure is better, and whether behaviour changes. Keep commits local through
review; any authorized push belongs after final review and required checks.

### 5. Review independently

Discovery agents are not the independent reviewer of their resulting changes.
For an audit-only run, ask the reviewer to challenge findings and source
coverage rather than assess a nonexistent change.

Give the reviewer the round's commits or diff for improvements, or the target and findings for audits, plus read access to surrounding code,
the selected discovery units, project rules/contracts, focus/bar, relevant stack
checks and versions, validation results/gaps, and rejected/contested ledger entries.
Keep reviews bounded by connected units; do not repeatedly rescan the entire
repository just to review a small fix.

For improvement runs, ask for two assessments. For audits, validate findings,
source coverage, and gaps without a preservation assessment of a nonexistent diff:

- **Preservation (improvements):** regressions, missed consumers,
  contract/lifecycle changes, weakened tests, and unsupported equivalence
  claims. Inspect all changed code and affected callers; green tests alone do
  not establish preservation.
- **Design and discovery:** for improvements, does the change remove the stated
  difficulty across callers, or relocate it, add configuration/indirection, or
  join unrelated concepts? For audits, are reported findings supported by
  inspected source and are important boundaries missing? What worthwhile
  findings remain in the assigned target units and cross-unit boundaries?

Each finding needs severity, `file:line`, concrete evidence, and a suggested fix;
structural ones need payoff and preservation requirements. For UI and
request-serving units, also ask what runs per frame, row, appearance, or request,
whether repeated work is avoidable, and which hot-path source was inspected.
Request actual source coverage and gaps separately. In each assessment, use
`NO FINDINGS` only when
nothing qualifies within that coverage. A failed or blocked review is not clean.

Verify new findings by the same rules. Make corrections the next round's priority
before extending the refactor; corrections also need review, and consume the same
round budget. If you cannot resolve a safety objection within budget, revert the
affected change and check the recovered state. Put additional pre-existing
opportunities into the backlog. Record the reviewed SHA, coverage, commits,
checks, and verdicts in the log. An earlier clean verdict does not cover later
corrections.

### 6. Check the stopping conditions

Continue with the highest-value safe backlog item or next pending unit. A clean
diff is permission to continue discovery, not a reason to end it.

## Stop rules

- **Audit complete:** the supplied target or default repository scope and its
  relevant boundaries have been inspected to the requested bar; findings and
  uninspected gaps are reported. An audit may be complete while findings remain.
- **Clean:** all original-scope units and relevant boundaries have been inspected
  for the requested focus, no qualifying candidates or unresolved findings remain,
  and the final changes have passed review and required checks. Check the scope
  map, graph edges, applicable architecture and hot-path coverage, and ledger
  together before claiming this. For a targeted improvement run, clean refers to the target
  and its impact set, not the untouched repository. Do not expand a targeted
  run into a whole-repository cleanup at the end.
- **Budget:** the round, time, or spend cap is reached. Finish or roll back the
  current step within the reserved cleanup budget. Report pending coverage and
  work honestly; budget exhaustion does not mean clean.
- **No safe remaining work:** remaining findings are deferred or contested and
  no other unit can be usefully inspected within the available constraints.
  Report partial completion and the reasons, rather than asking routine design
  questions or claiming the codebase is clean.
- **No progress:** three rounds produce only rework, oscillation, or failed
  attempts without a retained improvement or new scope coverage. New findings
  uncovered by fresh discovery are not themselves evidence of non-progress.
- **Broken ground:** a required gate or environment failure cannot be recovered.

A contested finding is deferred so independent work can continue. If repeated
fixes destabilize the project, stop under no progress instead of pushing through.

## Recovery

- **A gate fails on a change:** fix the cause, at most two attempts. Otherwise
  discard only that finding's edits or revert its commits to the last validated
  checkpoint, mark it deferred, and continue safe work elsewhere.
- **A committed change is wrong:** make a revert commit. Never rewrite history
  someone else may have. Re-run checks on the recovered state.
- **A test is flaky:** rerun once and compare with the starting commit without
  overwriting ongoing work. Record pre-existing flakes; do not skip or loosen
  them. An unexplained failure is not a passing gate.
- **A reviewer hangs or errors:** time-limit calls, retry once, then use the next
  available reviewer within budget. Failed calls do not establish coverage.
- **The session ends:** resume from log, ledger, `git status`, and commits since
  the recorded start. Re-run the gate on HEAD, reconcile coverage/backlog, then
  continue without repeating rejected work.
- **Never leave unfinished edits or known regressions behind.** Before stopping,
  discard your failed work or revert unsafe commits, run the required gate, and
  leave a clean working tree. Preserve any work that predates the run. If baseline
  failed before editing, stop without changing it.

## Finish

Use remaining budget to check the original scope map for gaps and reassess
cross-unit duplication, ownership, and dependencies affected by the changes.
Review any final corrections. Optional slow checks, device tests, or release
builds are useful when available; checks needed to establish a change's safety
belong before keeping that change, not just in this final phase. If a late check
reveals a regression, fix or revert it. Push only when authorized, after the
final state passes required checks and outstanding review objections are resolved.

Report in plain words:

- Target, resolved base/head for change scopes, action (audit or improvement),
  stop rule, rounds, and actual coverage including uninspected units.
- Structural improvements by area and the concrete maintenance burden removed,
  or source-backed audit findings; list behavioural fixes separately. Fewer
  lines alone are not an improvement.
- Required and optional checks actually run, platforms/configurations covered,
  unavailable checks, and whether review used a different model.
- Rejected, contested, and deferred work with reasons; any remaining risks.
- Branch, final SHA, and push status when edited; paths to the log and ledger.

## Reviewer

Use a different model when available: a separate agent, installed CLI, or API
can provide it. Choose from existing capabilities and use documented read-only,
noninteractive options with a timeout; close standard input for CLIs that might
otherwise wait. The reviewer inspects and reports; the main worker edits.

Start fresh review context per round, carrying only project context, coverage,
validation evidence, and the ledger. Give repository access rather than an
isolated diff. If useful, independent package/platform reviews can run in
parallel, with explicit scopes and one worker resolving their findings. If no
different model is available, make a separate fresh review pass yourself and
state that limitation. Never fabricate independent review.

## Boundaries

Stay autonomous within the authorized work. Do not stop for approval of routine
extractions, consolidation, module reorganization, or characterization tests.
Do not cross unapproved destructive or outward-facing boundaries such as force
pushes, publishing, deployment, live-data migrations, or dependency upgrades;
defer dependent findings and continue independent work.

Never weaken checks to obtain green, or claim more than you inspected and ran.
Give short progress updates while working; keep the detailed record in the log.

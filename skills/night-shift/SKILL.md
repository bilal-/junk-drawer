---
name: "night-shift"
description: "Autonomously review, fix, and refactor a whole codebase or focused area overnight. Maps architecture, finds duplicated knowledge, poor boundaries, tangled responsibilities, and other concrete maintenance problems, then works through a ranked backlog in small tested commits. Refactors preserve behaviour; bug fixes need regression tests; a second model reviews. Tracks scope coverage and findings to prevent premature completion and repeated rejected changes. Adapts to the project's languages, frameworks, and runtimes. Use for unattended refactoring, codebase cleanup, architecture improvement, or review-and-fix rounds until clean or the budget runs out."
---

# Night shift

Work through the requested codebase autonomously, finding and removing concrete
obstacles to understanding and changing it. Leave a tested, committed branch,
with evidence for the improvements and an honest account of what remains.

Discovery and regression review are separate jobs. A clean review of your last
commits does not mean the untouched codebase has been assessed. Continue through
the original scope until no worthwhile work remains or a stop rule applies.

## Inputs

Ask only for information that blocks the work. Infer the rest and record the
choice. Routine refactoring decisions are yours to make within the user's scope.

- **Scope:** whole repository by default; otherwise the requested paths, feature,
  package, or commit range. Resolve commit references to fixed SHAs. For a commit
  scope, inspect changed code and its affected relationships. Read callers and
  dependencies as needed; that does not expand permission to edit them.
- **Focus:** `bugs`, `refactor`, or `both`. Default: `both`. Structural discovery
  is required for `refactor` and `both`; do not let bug hunting replace it.
- **Bar:** confirmed high and medium findings by default; `all` includes low
  findings. High means a reachable correctness, data, or security risk. Medium
  includes demonstrated maintenance difficulty. Low means a small, confirmed
  improvement. Taste is not a finding at any bar.
- **Budget:** the user's round, time, or spend cap; default 8 rounds. A round is
  one discovery-and-change batch followed by one review. Reviewing corrections
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
3. **Establish a green baseline.** Start with a clean working tree and run the
   required project gate, including its full required test suite. Stop before
   editing if it fails or cannot run. Record commands, test count, platforms,
   build configurations, and results. Separate optional checks from required
   ones. Missing optional device or integration checks need not stop unrelated
   work, but defer changes whose safety depends on them.
4. **Use a working branch.** Never change the default branch directly.
5. **Start the log and ledger** in `$(git rev-parse --git-dir)/night-shift/`,
   outside tracked files. `log.md` records the starting SHA, budget, scope map,
   validation matrix, rounds, and checkpoints. `ledger.md` is the ranked backlog
   and history of findings. Keep both concise enough to resume from.
6. **Map the original scope into meaningful review units:** packages, features,
   subsystems, or connected modules, not arbitrary file-count chunks. Record
   each unit's responsibility, entry points, dependencies, state/resource
   owners, checks, and coverage status: `pending`, `inspected`, or `revisit`.
   Exclude generated and third-party code unless specifically in scope; inspect
   its contracts when relevant. Reading a directory listing or README is not
   source review. In a large repository, work through units across rounds.

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

## Each round

### 1. Discover and rank

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

Give the reviewer the round's commits or diff, read access to surrounding code,
the selected discovery units, project rules/contracts, focus/bar, relevant stack
checks and versions, validation results/gaps, and rejected/contested ledger entries.
Keep reviews bounded by connected units; do not repeatedly rescan the entire
repository just to review a small fix.

Ask for two assessments:

- **Preservation:** regressions, missed consumers, contract/lifecycle changes,
  weakened tests, and unsupported equivalence claims. Inspect all changed code
  and affected callers; green tests alone do not establish preservation.
- **Design and discovery:** does the change remove the stated difficulty across
  callers, or relocate it, add configuration/indirection, or join unrelated
  concepts? What worthwhile findings remain in the assigned original-scope
  units, including untouched code and cross-unit boundaries?

Each finding needs severity, `file:line`, concrete evidence, and a suggested fix;
structural ones need payoff and preservation requirements. Request actual source
coverage and gaps separately. In each assessment, use `NO FINDINGS` only when
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

- **Clean:** all original-scope units and relevant boundaries have been inspected
  for the requested focus, no qualifying candidates or unresolved findings remain,
  and the final changes have passed review and required checks. Check the scope
  map and ledger together before claiming this. Do not expand a path/commit-scoped
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

- Stop rule, rounds, and actual scope covered, including uninspected units.
- Structural improvements by area, with the concrete maintenance burden removed;
  list behavioural fixes separately. Fewer lines alone is not an improvement.
- Required and optional checks actually run, platforms/configurations covered,
  unavailable checks, and whether review used a different model.
- Rejected, contested, and deferred work with reasons; any remaining risks.
- Branch, final SHA, push status, and paths to the log and ledger.

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

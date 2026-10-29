---
name: "night-shift"
description: "Maintain a repository through recurring architectural audits and improvements, or review a supplied branch, PR, commit range, path, or feature. Uses a graph of bounded agent tasks with explicit contracts to examine responsibility boundaries, business logic and UI separation, shared rules and constants, defects, tooling gaps, and hot-path costs. For improvements, makes small tested commits and seeks independent review. Carries evidence, decisions, and unfinished coverage between runs. Use for regular repository upkeep or focused code review and refactoring."
---

# Night shift

Maintain clear ownership, boundaries, and reusable domain knowledge as a
repository evolves. Work through the requested target autonomously. For
improvements, leave a tested, committed branch with demonstrated maintenance
benefits; for audits, leave source-backed findings. Each run also leaves the
evidence, decisions, and next work needed for the next run.

Three outcomes organize the work: explain the architecture from actual flows,
resolve findings through a graph of tasks with explicit contracts, and build
on previous runs without repeating stale advice or reversing sound decisions.
For `bugs` focus, retain the graph and continuity discipline without requiring
an architectural refactor. A successful upkeep run can make no code changes.

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
- **Action:** an audit or review request reports findings without source edits; a
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
  reachable path that scales with normal use. A confirmed gap in applicable
  quality enforcement is also medium; establish applicability and check for
  equivalent coverage using [quality checks](references/quality-checks.md).
  Low means a small, confirmed improvement. Taste is not a finding at any bar.
- **Budget:** the user's round, time, or spend cap; default 8 rounds. A round
  executes a bounded part of the task graph through synthesis and review,
  including changes when authorized. Use independent validation when available;
  the Reviewer fallback records any review debt. Branching investigations,
  corrections, and retries share this budget. Reviewing corrections consumes
  another round; no unbounded inner review loop. Preparation, tests, and reviewers
  consume the same time/spend budget. Reserve enough to validate and leave a
  clean tree; do not start work you cannot safely finish.
- **Push:** no by default. Commit locally; push only when authorized.
- **Reviewer:** an independent reviewer, preferably a different model; see Reviewer below.

## Prepare

Preparation before checkout selection is read-only. Defer project gates and
candidate diagnostic tools until ownership or isolation is established; do not
run checks on a checkout another run may mutate.

1. **Learn the project.** Read applicable `AGENTS.md`, `CLAUDE.md`, README,
   `CONTRIBUTING`, build configuration, and relevant design documents. Project
   rules and contracts beat generic advice or a reviewer's preferences. Learn
   the project's exact format, lint, build, type-check, and test commands; prefer
   its scripts. Read [quality checks](references/quality-checks.md) to distinguish
   configured tools from checks actually enforced in CI. Record applicable
   gaps before discovery. Do not install tooling just to run this skill.
2. **Identify targets.** Map first-party packages, entry points, framework
   versions, deployment hosts, native targets, and data/services. Use
   [stack detection](references/stack-detection.md), its common checks, and only
   the linked sections relevant to the scope. Use available specialist guidance
   when helpful; another skill is not required.
3. **Start or reconcile the log and ledger.** Read
   [recurring upkeep](references/recurring-upkeep.md) for state ownership,
   criteria fingerprints, compatibility, pending integration, and handoff.
   Reconcile prior state before assigning work; do not reset unfinished coverage
   simply because a new run started. If state cannot be written, keep an inline
   record and include the handoff in the final report.
4. **Own the checkout before running checks.** Reconcile existing implementations
   before selecting a checkout. If another run may mutate it, use an isolated
   worktree from a fixed target snapshot. If safe ownership or isolation cannot
   be established, continue read-only, skip unsafe project commands, and report
   the validation/editing blocker. For edits, continue an already checked-out
   night-shift branch recorded for compatible work, or one explicitly selected
   by the user; otherwise create a dedicated branch from the target. Never edit
   the default branch directly. Audit-only runs do not create commits.
5. **Establish the baseline in the selected checkout.** If checkout ownership or
   isolation is unavailable, record the baseline as unavailable and continue
   only with safe read-only inspection. Otherwise record the starting tree and
   run the required project gate, including its full required test suite. Record
   commands, test count, platforms, build configurations, and results. A failing
   or unavailable gate blocks edits whose safety depends on it; audit-only work
   can continue read-only and report the gap. Separate optional checks from
   required ones. Missing optional device or integration checks need not stop
   unrelated work, but defer changes whose safety depends on them.
6. **Map the original scope into meaningful review units:** packages, features,
   subsystems, or connected modules, not arbitrary file-count chunks. Record
   each unit's responsibility, entry points, dependencies, state/resource
   owners, checks, and coverage status per applicable lens (architecture,
   defects, hot paths): `pending`, `inspected`, or `revisit`.
   Exclude generated and third-party code unless specifically in scope; inspect
   its contracts when relevant. Reading a directory listing or README is not
   source review. In a large repository, work through units across rounds.

7. **Build the work graph.** Read the
   [discovery graph](references/discovery-graph.md). Connect source units and
   boundary flows, then derive tasks with prerequisites, explicit input/output
   contracts, and acceptance criteria. Dispatch ready discovery tasks to
   available sub-agents; synthesize connected reports before selecting changes.
   New evidence can add investigation tasks; edits invalidate affected evidence
   and lead to checks and independent review. The lead owns acceptance, edits,
   and closure. With no agents, follow the graph sequentially and report the
   limitation.

## Find worthwhile refactors

For `refactor` or `both`, read the [refactoring guide](references/refactoring.md).
Assess system structure, module handoffs, and local implementation separately.
Record source-backed strengths and gaps at each scale; passing mechanical checks
does not establish design quality.
Examine architecture as well as individual functions. Trace representative
flows from entry point through domain logic, storage or external services, and
back; include error, cancellation, and cleanup paths. Inspect the code, its
callers, tests, and relevant history. Look across package and platform boundaries
for the same rule implemented separately.

Prioritize problems that amplify changes or force callers to understand too
many details:

- Duplicated knowledge and drift between implementations of the same contract.
- Business decisions embedded in UI or transport code, domain code depending on
  presentation details, and persistence concerns leaking into callers. Separate
  policy from rendering and effects while preserving UI state and lifecycle.
- Shared policy values, units, defaults, or identifiers with several owners;
  misplaced constants and repeated literals whose meaning must stay aligned.
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
change together across packages or platforms. Record the current and proposed
owners, dependency directions, migrated consumers, and intentional differences
for each selected structural finding. Use meaningful domain owners for shared
rules and constants; similar literals alone do not justify a global constants
file or a shared utility. Local cleanup is not a substitute for resolving a
confirmed cross-unit problem. An invalid UI test that no longer
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
source, obtain independent review of findings and coverage (or use the disclosed
Reviewer fallback), and report. Skip
implementation, commit, and change-recovery steps.

### 1. Discover and rank

Dispatch ready tasks from the work graph in bounded batches. Accept reports
only against their contracts; incomplete or stale reports leave coverage open.
Reconcile connected reports into one ledger and verify candidates against source.
Create follow-up tasks for unresolved boundaries or conflicting ownership before
planning a change that depends on them. Follow the recurring-upkeep priorities
when selecting changed areas, old findings, and pending or stale coverage.
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

Group symptoms of the same verified ownership or contract problem under one
root finding, preserving their locations and consumers. Count the underlying
improvement once. Keep the round's ready work distinct from the full backlog;
choose a coherent batch whose prerequisites and validation fit the budget.

For each finding, record an id, severity, locations and consumers, evidence,
expected payoff, and status. Use `candidate`, `verified`, `in-progress`,
`fixed <sha(s)>`, `rejected: <reason>`,
`contested: <reason>`, or `deferred: <reason>`. Record review status and integration
state separately from implementation. Notice unrelated issues without editing
outside scope. Rejected and contested entries accompany future reviews; revisit
when evidence or premises change, including applicable project or skill rules.
If a proposal would undo an earlier change, resolve the disagreement on evidence
once; do not alternate between designs.

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
  indirection being removed; before/after owners and dependencies, affected
  consumers, and intentional duplication or platform differences retained.
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

Check the plan against current source before editing: do named symbols and
consumers still exist, is the finding still present, and do steps describe an
executable change? Account for shared files and renames/removals that affect
later tasks; order dependent changes. Simplify or drop steps whose new coupling,
configuration, or indirection would cost more than the problem they remove.

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
- Run the project's formatter and import sorter on edited files, especially
  after scripted insertions or renames; check unused imports too. Inspect the
  resulting diff for unrelated rewrites and contract-changing fixes. If tools
  are absent, follow existing conventions and report the gap as described in
  [quality checks](references/quality-checks.md).

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

Start the independent design assessment with the round's selected units and
boundaries, target/base/head, source snapshot, focus/bar, project constraints,
relevant stack guidance, and validation gaps. Withhold earlier verdicts and the
author's preferred solution, not the scope needed to bound the review. After
those initial observations, supply the round's commits/diff for improvements or
findings for audits, plus the proposed payoff and rejected/contested ledger
entries. Keep both phases bounded to the selected units and affected boundaries.

For improvement runs, ask for two assessments. For audits, validate findings,
source coverage, and gaps without a preservation assessment of a nonexistent diff:

- **Preservation (improvements):** regressions, missed consumers,
  contract/lifecycle changes, weakened tests, and unsupported equivalence
  claims. Inspect all changed code and affected callers; green tests alone do
  not establish preservation.
- **Design and discovery:** for improvements, does the change remove the stated
  difficulty across callers, or relocate it, add configuration/indirection, or
  join unrelated concepts? Check the before/after owners, dependency direction,
  business logic/UI separation, rule and constant reuse, migrated consumers,
  and the rationale for remaining duplication. For audits, are findings supported by
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

Reconcile completed tasks and invalidated evidence, then dispatch the next ready
task or pending unit. A clean diff is permission to continue discovery, not a
reason to end it. Close a finding only when its evidence, affected consumers,
required checks, and review meet its acceptance criteria. If independent review
is unavailable, use the qualified closure and review debt under Reviewer; do not
reimplement an already retained fix.

## Stop rules

- **Audit complete:** the supplied target or default repository scope and its
  relevant boundaries have been inspected to the requested bar, and findings
  and coverage independently validated. Report validation limits. Uninspected
  source units or boundaries mean partial coverage under another stop rule.
  Findings may remain in a complete audit.
- **Review-limited:** actionable discovery and fixes are finished but independent
  validation remains unavailable. Keep only changes meeting the self-review
  fallback, report its limits, and carry review tasks into the handoff. This is
  not an unqualified audit-complete or clean verdict.
- **Clean:** all original-scope units and relevant boundaries have been inspected
  for the requested focus, no qualifying candidates or unresolved findings remain,
  and the final changes have passed review and required checks. Check the scope
  map, accepted task outputs, graph edges, applicable architecture and hot-path
  coverage, tooling gaps, and ledger together before claiming this. Prior coverage
  must pass the recurring-upkeep validity check; report carried evidence separately
  from new inspection. No independent-review debt may remain. For a targeted
  improvement run, clean refers to the target
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
  the recorded start. Follow the recurring-upkeep compatibility and invalidation
  rules, re-run the gate on HEAD, and resume ready work without repeating rejected
  proposals or treating interrupted tasks as accepted.
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

Persist the final checkpoint and next-run handoff using
[recurring upkeep](references/recurring-upkeep.md). This is required even for a
no-change or budget-limited run. If state writes are forbidden or unavailable,
include the handoff in the final report and disclose that it was not saved.
Do not schedule future runs unless requested.

Report in plain words:

- Target, resolved base/head for change scopes, action (audit or improvement),
  stop rule, rounds, and actual coverage including uninspected units.
- Structural improvements by area and the concrete maintenance burden removed,
  or source-backed audit findings; list behavioural fixes separately. Fewer
  lines alone are not an improvement.
- Required and optional checks actually run, platforms/configurations covered,
  unavailable checks, tooling gaps and measured proposals, and whether review
  used a different model.
- Rejected, contested, and deferred work with reasons; any remaining risks.
- What changed since the prior checkpoint, newly inspected versus carried
  coverage, and the next priorities or conditions for retrying deferred work.
- Branch, final SHA, and push status when edited; state paths for the next run.

## Reviewer

Use an independent reviewer, preferring a different model when available; a
fresh same-model agent is also independent of the author. A separate agent,
installed CLI, or API can provide it. Choose existing capabilities and documented
read-only, noninteractive options with a timeout; close standard input for CLIs
that might otherwise wait. The reviewer inspects and reports; the lead edits.
Start fresh context per round, bounded to its selected units, boundary flows,
focus/bar, source snapshot, validation evidence, and established constraints.
Give repository access rather than an isolated diff. Obtain initial source
observations before showing the author's preferred solution or prior verdicts,
then reconcile with the proposed payoff and ledger. Independent package/platform
reviews may run in parallel, with explicit scopes and one worker resolving findings.

If no independent reviewer is available, perform a separate self-review of source,
diff, affected consumers, and checks. The initial blind pass cannot apply to the
author. Retain a change only if required checks pass and no safety objection
remains; mark it `fixed <sha> (self-reviewed; independent review pending)`. Mark
audit findings `self-challenged; independent validation pending`. Queue review
of the retained commit or finding, not another implementation. This fallback
cannot satisfy an explicit requirement for independent approval. Report the
limitation and outstanding review debt; never claim independent validation or
an unqualified clean result from self-review.

## Boundaries

Stay autonomous within the authorized work. Do not stop for approval of routine
extractions, consolidation, module reorganization, or characterization tests.
Do not cross unapproved destructive or outward-facing boundaries such as force
pushes, publishing, deployment, live-data migrations, or dependency upgrades;
defer dependent findings and continue independent work.

Never weaken checks to obtain green, or claim more than you inspected and ran.
Give short progress updates while working; keep the detailed record in the log.

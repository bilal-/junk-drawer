# Discovery and delivery graph

Use the source graph to understand the system and the work graph to resolve its
findings. A table or adjacency list in the run log is sufficient; no orchestration
framework is required. Map the requested target and its affected relationships,
or the repository when no target was supplied. The root owns scope, accepted
evidence, edits, validation, and the final result.

## Map the source graph before assigning work

Nodes are responsibilities: features, packages, subsystems, or connected modules.
Edges are calls, dependencies, shared rules/data, resource ownership, platform
counterparts, and external contracts. Record dependency direction and the owner
of each shared invariant. A directory can contain several nodes; a node can span
directories. Mark entry points, critical flows, and uncertain boundaries.

Reconcile node membership with the actual first-party inventory. Account for
application and library code, background work, tests, scripts/tooling, and
build/deploy configuration where present. Do not discover scope solely by walking
outward from the main entry point: disconnected utilities, secondary platforms,
and operational paths also need owners. For a targeted run, inventory the target
and relevant impact set rather than the entire repository. Record exclusions.

For each node and important edge, record applicable lenses, source membership,
coverage status, and responsible task or valid carried evidence. A skipped lens
needs an applicability reason. Tests and configuration may belong to a source
unit or a distinct responsibility, but cannot disappear between assignments.
Inspect complete flows across nodes, including relevant failure and lifecycle
paths. Give cross-unit flows explicit tasks; isolated file reviews cannot settle
shared ownership or business logic leaking into UI.

## Delegate through a hierarchy when useful

The root can delegate a large responsibility to a coordinator, which can delegate
smaller responsibilities to workers or further coordinators. There is no fixed
depth limit. Add a level when the area's source or evidence is too large for one
focused context, not simply because another agent is available. Each child must
narrow the parent's responsibility or answer a distinct bounded boundary question.
Do not pass the same whole-repository assignment down an unchanged chain.

For example, a root may assign client, service, shared-domain, and tooling areas;
a client coordinator may assign web and native areas; a native coordinator may
assign navigation, persistence, and rendering tasks. This illustrates delegation,
not a required topology. Choose boundaries from the actual repository. Small
scopes can use a root and a few workers, or no delegation.

Each coordinator must:

- Cover its entire assigned inventory with child tasks, direct inspection, or
  valid carried evidence. Check the union against its assignment; a child's
  missing paths or lenses remain gaps in the parent report.
- Give each child the contract below, relevant rules, and only the input context
  it needs. Keep the assigned snapshot stable while discovery is running.
- Accept child evidence, reconcile overlapping or contradictory findings, and
  trace the flows between its children. Aggregating summaries alone is not
  architectural synthesis.
- Own boundaries between its children. Send a boundary crossing its own scope
  to the nearest common ancestor for assignment, with a concrete question and
  affected nodes. Never assume the other area will inspect it.
- Return a compact area report with coverage by unit/lens, exclusions, accepted
  task/evidence links and snapshot, owners and dependency directions, consolidated
  findings, intentional tradeoffs, blockers, and unresolved boundary questions.
  Distinguish fresh inspection from carried evidence and leave gaps visible.

Keep detailed source observations and child reports in task-specific artifacts
under the current run's state directory when writable, or return them inline
when it is not. Each agent owns only its assigned report; the root owns the
consolidated log and ledger. Parents read summaries and retrieve detailed evidence
for acceptance checks, conflicts, or decisions. Do not copy every child transcript
into every ancestor's context. Checkpoint accepted results before replacing a
full context; continuation must retain task ids, scope, snapshot, and open gaps.

Delegation remains under the run's authority and resource limits. The root owns
the round counter and shared concurrency/time/spend allowances; a child cannot
start another eight-round run or grant itself extra capacity. Allocate worker
slots explicitly before child dispatch; coordinators count against the same
capacity as workers and may delegate only within their allocation. Discovery
coordinators may delegate inspection and synthesis, not source edits or commits.
The root remains the single editing owner. Respect the harness's available
workers; a logical hierarchy does not require all coordinators to stay live.
When slots or delegation are unavailable, return child contracts for scheduling
or execute them sequentially. Never wait indefinitely for capacity held by
waiting ancestors. Report limits on independent coverage.

## Give every delegated task a contract

Specify these fields in the brief, using concrete paths and responsibilities:

- **Identity and question:** task/parent id, worker or coordinator role, and the
  decision this task must support.
- **Scope:** source membership, nodes and edges, entry points, original
  target/base/head, focus/bar, exclusions, and ownership of connecting boundaries.
- **Inputs:** repository rules, relevant versions, accepted predecessor reports,
  applicable ledger decisions, and source snapshot. Record HEAD and relevant
  uncommitted state; results from another snapshot need reconciliation.
- **Authority and limits:** read-only source inspection and safe checks; no
  source edits, commits, dependency installation, or external mutations. State
  whether child delegation is allowed, report destination, bounded task
  time/scope, and the inherited remaining run limits. Report new out-of-scope
  edges to the parent for assignment rather than silently widening the task.
- **Lenses:** architecture for `refactor`/`both`, defects for `bugs`/`both`, hot
  paths in relevant units for any focus unless explicitly excluded. Include
  ownership, business logic/UI separation, shared rules and constants where
  relevant. Account for relevant tests and quality enforcement.
- **Required output:** inspected files/tests and snapshot; flows and edges
  traced; owners and dependency directions; findings with severity, `file:line`,
  affected consumers, evidence, proposed owner/fix, preservation constraints,
  and verification needed. Separate facts, uncertain leads, intentional
  differences, skipped paths/lenses, and follow-up requests. A coordinator also
  returns the compact area report defined above.
- **Acceptance:** evidence needed to answer the question, assigned paths/lenses
  and boundaries that must be accounted for, and gaps that prevent closure.
  `NO FINDINGS` applies only to inspected source and stated lenses; a timeout,
  summary of directory names, or blocked check is not a clean verdict.

For example, assign checkout eligibility from UI event through the application
service to persistence, name alternative consumers and the shared-rule boundary,
and require evidence of each rule's owner and error path. A coordinator can
split those inspections, but must reconcile their contracts before returning.
Do not merely ask an agent to "review checkout" or prescribe an extraction before
it has inspected the evidence.

## Schedule a full discovery sweep within a round

A round contains discovery across the requested scope, synthesis, a bounded
implementation batch when authorized, checks, and independent review. Worker
calls, nested delegations, and scheduling batches are not additional rounds.
With twelve areas and three available workers, discovery can take four batches
within round one; eight rounds must not mean only eight areas get visited.

Queue tasks for every pending or invalidated unit and important boundary. Keep
refilling available capacity until all have accepted evidence or a concrete
blocker, including necessary follow-up investigations. Prioritize central or
risky paths to order the queue, not to exclude its tail. Complete this initial
sweep and system synthesis before optional implementation. Urgent safety work
can interrupt discovery but does not erase the remaining queue. A time/spend
cap can stop mid-sweep; record actual partial coverage and the next ready work.

Each later round reconciles the entire coverage map and discovers new or stale
areas. Carry evidence only under recurring-upkeep validity rules; do not reread
unchanged source just to fill eight rounds. Implementation corrections use the
next round and need fresh review. Time-bound each discovery assignment in its contract. For a
failed or incomplete assignment, allow one bounded recovery attempt: retry,
directly inspect the missing source, or subdivide and collect narrower reports.
If gaps remain after that attempt, retain useful evidence and mark those gaps
blocked; continue independent discovery. Keep the original task's acceptance
gaps and recovery history when splitting or reassigning it, so delegation cannot
reset retries. Reopen it only when new evidence or changed conditions can advance
it. This recovery bound does not limit the depth of planned subdivision.
A blocked unit remains pending/revisit in coverage, not inspected.

Tasks have explicit prerequisites and outputs. Typical dependencies are:

```text
inventory -> area coordinators -> worker inspections -> area synthesis
area reports + cross-area flow inspections -> whole-scope synthesis
uncertain contract -> bounded investigation -> affected synthesis/decision
verified finding -> plan -> implement -> required checks -> independent review
review correction -> next round's correction -> checks -> new review
accepted reports + current coverage + ledger -> closure or next ready work
```

These are dependencies, not a fixed sequence for every finding. Audit paths omit
implementation. Synthesis waits for the reports it needs; unrelated tasks can
continue. Every new investigation must identify the unresolved question and the
decision it blocks. Group related findings around a responsible rule or boundary
with one verification target, retaining each symptom's evidence.

Keep task id/parent, prerequisites, assignee, snapshot, acceptance criteria,
state, and evidence links in the log. States are `pending`, `ready`, `running`,
`accepted`, `blocked: reason`, `dropped: reason`, or `superseded: replacement`.
A task is ready only when its prerequisites are accepted. An agent finishing is
not acceptance. Drop work made unnecessary by a rejected finding, but never drop
its source-coverage obligation with it. Keep the discovery frontier separate
from the selected implementation batch. Order edits sharing files or changing
symbols used by another task. After edits, supersede affected evidence and add
verification/review tasks; preserve unaffected coverage and graph history.

## Synthesize the whole system and close honestly

At each level, check outputs against the contract and snapshot. Missing paths,
unsupported claims, or stale evidence leave coverage pending or needing revisit;
request a bounded correction or inspect directly. Preserve useful partial
results without accepting a conclusion they cannot support.

The root checks area coverage against the original inventory and verifies
cross-area claims against source. Trace end-to-end responsibilities, dependency
directions, shared rules and constants, UI/domain separation, error/resource
ownership, and repeated runtime costs where applicable. Look for duplicated
knowledge, incompatible assumptions, or displaced complexity between areas that
individually reported no findings. Connect shared causes; do not simply concatenate
worker findings. Record strengths and intentional differences as well as gaps.

Verify candidates before action. Distinguish confirmed problems, false reports,
overstated impact, justified designs, and fixes that cost more than they remove;
record source and reasons for each disposition. Rank the consolidated ledger by
impact, change amplification, confidence, and verification cost. Distinguish
introduced, worsened, and pre-existing findings for change targets. Rejecting a
false report or deferring a real problem is not an implemented improvement.

For improvements, normal closure requires the ownership change verified across
consumers, obsolete paths removed or justified, required checks passing, and
independent review accepting the final state. Audit closure requires independent
challenge of findings and coverage, not implementation. A discovery worker or
coordinator cannot independently validate the output it produced or synthesized;
use a fresh reviewer outside that work's authoring/discovery chain. Reviewers
need the requested scope and coverage gaps as well as selected findings.

When no independent reviewer is available, use the skill's self-review fallback.
Accept retained implementation or inspection only with its qualified review
status; leave a separate independent-review task pending or blocked. Do not
requeue implementation of a retained fix. Self-review cannot yield an unqualified
clean or audit-complete verdict.

Before stopping, reconcile every in-scope unit/lens and important edge with its
accepted evidence or gap, and every task and finding with its current disposition.
Full coverage requires no uninspected in-scope units or unresolved inspection
boundaries; a blocked task's documented reason does not satisfy that requirement.
Apply the skill's stop rules and persist next ready tasks and blocked prerequisites.
Task counts, delegation depth, and eight elapsed rounds are not coverage proof.

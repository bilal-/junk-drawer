# Discovery and delivery graph

Use a source graph to understand the system and a work graph to resolve its
findings. Both fit in the run log; a table or adjacency list is sufficient.
No orchestration framework is required. Map the requested target and its affected
relationships, or the repository when no target was supplied. The lead owns
scope, acceptance of evidence, edits, validation, and the final result.

## Map the source graph

Nodes are responsibilities: features, packages, subsystems, or connected modules.
Edges are calls, dependencies, shared rules/data, resource ownership, platform
counterparts, and external contracts. Record dependency direction and the owner
of each shared invariant. A directory can contain several nodes; a node can span
directories. Mark entry points, critical flows, and uncertain boundaries.

Inspect complete flows across nodes. Assign a boundary or end-to-end flow when
unit-level inspection could miss ownership or business logic leaking into UI.
Overlapping inspection is useful at an uncertain seam; scanning the same easy
files repeatedly while central paths remain untouched is not coverage.

## Derive tasks and their dependencies

Tasks are units of work with explicit prerequisites and outputs. Typical paths:

```text
inspect UI + domain + storage -> synthesize ownership
synthesize ownership -> verify finding -> plan change
new consumer/uncertain contract -> inspect it -> verify finding
plan change -> implement -> required checks -> review
review -> accept result -> reconcile coverage -> next ready work or handoff
review correction -> plan correction -> implement -> checks -> new review
```

The example shows dependencies, not a fixed sequence for every finding. Audit
paths go from verified findings to independent validation and coverage closure;
they omit implementation. Independent source inspections can run in parallel.
Synthesis waits for the connected reports it needs. A new consumer, uncertain
contract, or contradictory report creates a bounded investigation task whose
output is a prerequisite for the affected decision. Unrelated tasks may continue.

Keep task id, purpose, prerequisites, assignee, snapshot, acceptance criteria,
state, and evidence links in the log. States are `pending`, `ready`, `running`,
`accepted`, `blocked: reason`, `dropped: reason`, or `superseded: replacement`.
Drop tasks made unnecessary by a rejected finding rather than leaving them
pending. Mark a task ready
only when its prerequisites are accepted. An agent finishing does not itself
accept the task. After edits, supersede stale evidence where dependencies changed
and create verification/review tasks against the new state. Do not restart the
whole graph or erase unaffected coverage.

The ready queue is a bounded selection from the ledger, not the entire backlog.
Group related findings around the responsible rule or boundary and give the
group a shared verification target. Retain each symptom's evidence without
creating duplicate fixes. If tasks touch the same files or one removes a symbol
another uses, record the dependency before execution. Reconcile evidence after
each coherent batch; new safety evidence can interrupt the queue.

Rounds bound how much of this graph is executed. New branches, corrections,
agent retries, and review all consume the same run budget. The lead dispatches
bounded tasks; agents return follow-up requests instead of spawning an unbounded
tree of agents. Reserve capacity for synthesis, checks, review, and handoff.

## Give every delegated task a contract

Specify these fields in the brief, using concrete paths and responsibilities:

- **Question and scope:** the decision this task must support, source nodes and
  edges, entry points, original target/base/head, focus/bar, and exclusions.
- **Inputs:** repository rules, relevant versions, accepted predecessor reports,
  applicable ledger decisions, and the source snapshot to inspect. Record HEAD
  and any working diff; keep the snapshot stable while related agents inspect it.
- **Authority and budget:** read-only inspection and safe checks, no edits,
  commits, dependency installation, or external mutations; bounded time/scope.
  Agents report new edges to the lead for assignment.
- **Lenses:** architecture for `refactor`/`both`, defects for `bugs`/`both`, and
  hot paths in relevant units for any focus unless explicitly excluded. Include
  ownership, business logic/UI separation, shared rules and constants where relevant.
- **Required output:** inspected files/tests and snapshot; flows and edges
  traced; owners and dependency directions; findings with severity, `file:line`,
  affected consumers, evidence, proposed owner/fix, preservation constraints,
  and verification needed. Separate established facts, uncertain leads,
  intentional differences, skipped paths, and requests for follow-up work.
- **Acceptance:** what evidence answers the task's question, which boundaries
  must be traced, and which gaps prevent closure. `NO FINDINGS` applies only to
  the stated source and lenses; a timeout or blocked check is not a clean verdict.

For example, ask an agent to trace checkout eligibility from a UI event through
the application service and persistence adapter, identify every owner of that
rule, and account for alternative consumers. Do not merely ask it to "review
checkout" or prescribe an extraction before it has inspected the evidence.

Use available sub-agents for bounded independent work. When unavailable, execute
the same contracts sequentially and disclose the lack of independent coverage.
Scale the graph to the scope; a small target may need only a few tasks.

## Accept, synthesize, and close

The lead checks outputs against the contract and source snapshot. Missing paths,
unsupported findings, or stale reports leave coverage pending or needing revisit;
request a bounded correction or inspect it directly. Preserve useful partial
evidence without accepting a conclusion it cannot support.

During verification, distinguish a confirmed problem from a false report,
overstated impact, a justified design choice, or a proposed fix that adds more
cost than it removes. Record the reason and source for each disposition. A
deferral remains open work; neither rejecting a false report nor skipping a
real problem is a code improvement.

Reconcile shared seams and conflicting reports against source and tests. Record
current owners, dependency direction, duplicated knowledge, intended boundaries,
and intentional differences. Trace at least one complete flow across each central
boundary implicated by a finding. Local clean reports cannot establish that the
connecting design is sound. Rank the consolidated ledger by impact, change
amplification, confidence, and verification cost; distinguish introduced,
worsened, and pre-existing findings for change targets.

For improvements, normal closure requires that the intended ownership change is
verified across consumers, obsolete paths are removed or justified, required
checks pass, and independent review accepts the final state. A reviewer must
not validate their own discovery as independent evidence. Review corrections
create new tasks and consume another round. For audits, closure means the
finding and its coverage have been independently challenged, not that code was fixed.

When no independent reviewer is available, use the skill's explicit self-review
fallback. Accept the implementation or source-inspection task only with its
qualified review status; leave a separate independent-review task pending or
blocked on reviewer availability. Do not requeue implementation of the retained
fix. Self-review does not count as independent validation and cannot yield an
unqualified clean or audit-complete verdict.

Before finishing, reconcile accepted tasks with the source coverage map and
ledger. Every in-scope pending edge, unresolved finding, or unavailable check
has a recorded disposition. The stop rules determine whether this is complete,
clean, or partial. Persist the next ready tasks and blocked prerequisites for
the next run; task counts alone are not proof of architectural progress.

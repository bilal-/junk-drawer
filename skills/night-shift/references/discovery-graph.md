# Distributed discovery graph

Use this when the scope spans multiple meaningful review units and sub-agents are available. With no user-supplied target, map the repository. With a branch, PR, commit range, path, or feature target, map that target and its affected relationships. The lead owns the scope map, ledger, edits when authorized, validation, and final judgment. Discovery agents inspect and report; they do not edit or commit. If agents are unavailable, the lead follows the same map and synthesis process sequentially and reports the limitation.

## Build and assign the graph

Map units by responsibility: feature, package, subsystem, or connected modules. Draw edges for calls, shared data and invariants, resource ownership, platform counterparts, and external contracts. A directory can contain several units; a unit can cross directories. Mark critical paths and risky edges. Assign bounded units to agents with enough context to follow relevant callers and dependencies beyond their assigned files. Assign a boundary or end-to-end flow to an agent when it spans units and a unit-level scan would miss ownership. Let adjacent agents inspect an overlapping seam when ownership or a shared contract is uncertain. Avoid many agents independently scanning the same easy files while central paths remain untouched.

Give each agent a brief containing:

- Original scope (including resolved base and head for a change target), focus and bar, repository rules, relevant runtime/framework versions, unit responsibility, starting files or entry points, and graph edges to inspect.
- Required lenses: architecture and change amplification for `refactor`/`both`; reachable defects for `bugs`/`both`; hot-path work for UI or request-serving units under `bugs`/`both`.
- Return format: source and tests actually inspected; skipped paths; flows and graph edges traced; dependencies, owners, and contracts; concrete findings with `file:line`, callers or affected flows, evidence, severity, proposed owner or fix, preservation constraints, and verification needed. Report `NO FINDINGS` only for the inspected lens and coverage. Return uncertain leads separately, without elevating them to findings.
- Read-only authority. Agents may inspect tests and history and run safe read-only checks, but the lead alone chooses and implements changes.

Parallelize independent units when useful. An agent may suggest a new edge or unit; the lead adds it to the map and assigns or inspects it. Timebox work against the run budget and reserve capacity for synthesis, changes, tests, and independent review. Agent completion is evidence of coverage only for source and paths it actually inspected.

## Synthesize before changing code

Collect reports and reconcile shared seams. Add newly discovered edges to the graph and inspect or assign them in a second pass. The lead reads representative source and verifies each proposed finding, especially disputed ownership and cross-platform contracts. Combine local reports into an architecture view: where does a rule live, which callers coordinate it, which copies drift, and which resource or state lifetimes cross units? Trace at least one end-to-end flow across every central boundary implicated by a finding. A cluster of local clean reports is not proof that their connecting architecture is sound.

Rank the consolidated ledger by real user/caller impact, change amplification, confidence, and verification cost. For change targets, distinguish what the change introduced or worsened from pre-existing findings. Choose the least complex change that resolves the demonstrated issue when fixes are authorized. After edits, revisit affected nodes and edges, not just changed files. Keep the independent reviewer separate from discovery reports; discovery agents' agreement does not replace review of the resulting diff or validation of audit findings.

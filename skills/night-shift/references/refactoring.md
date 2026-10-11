# Discover and prove structural improvements

Use these lenses for `refactor` and `both`. Follow the code's actual problems;
this is not a requirement to apply every transformation. Inspect both local code
and relationships between modules. A design diagram, metric, or search hit helps
locate evidence but does not establish a finding.

## Establish the current design

For each connected review unit, answer from source and tests:

- What operations does it provide, and which entry points and consumers use them?
- Which decisions, state, resources, and invariants does it own? Which details
  must its callers know? Where are error handling and cleanup performed?
- Which other modules must change when one of its rules changes? Search for the
  same validation, conversion, branching, or sequence elsewhere.
- Are the boundaries deliberate? Check existing conventions and relevant history
  before removing a compatibility path, test seam, or platform-specific choice.

Read representative complete flows, not just declarations or the largest files.
Include the boundary tests. Central/high-change modules and weakly tested
boundaries deserve attention, but do not ignore the remaining original scope.
Use Git history when available to corroborate co-changing responsibilities;
absence of history does not prevent a source-grounded finding.

## Duplicated knowledge and drifting twins

**Evidence:** enumerate every copy of the same domain rule, protocol mapping,
validation, or algorithm. Explain why they must change together. Three similar
fragments are a lead; two copies can already justify consolidation when they
encode the same contract. Similar syntax across different domains is weaker.

**Improve:** put the shared decision with its existing owner and migrate callers.
Keep presentation, platform, and lifecycle differences at their own boundaries.
Compare edge cases before reusing a helper. If copies already disagree, separating
the structural consolidation from a behavioural correction is essential.

## Scattered decisions and repeated caller coordination

**Evidence:** several callers know storage layout, ordering constraints, retries,
or a multi-step setup/cleanup protocol belonging to one concept. List the callers
and the details they repeat. The problem may span files without textual clones.

**Improve:** offer a cohesive operation that owns those details and exposes what
callers need. Preserve transaction boundaries, failures, cancellation, and cleanup.
Do not replace explicit coordination with hidden global state.

## Mixed responsibilities and oversized owners

**Evidence:** a module combines independently changing work, such as domain
policy, transport, persistence, and rendering; changing one requires understanding
the others. Identify the distinct flows and dependencies. Length alone is not it.

**Improve:** move one cohesive responsibility, including its relevant state and
dependencies, behind a meaningful boundary. Leave orchestration understandable.
An extraction that passes most of the old object's internals back and forth has
probably moved the tangle rather than separated it.

## Misplaced dependencies, cycles, and feature envy

**Evidence:** trace an actual import/call cycle, access to another module's
internals, or repeated manipulation of somebody else's data. Show an ownership
violation or concrete coordination/change cost, and what callers must understand.
Do not invent layer rules where the project has none.

**Improve:** move the operation to the data/invariant owner, invert one dependency
through an existing seam, or combine pieces that are one responsibility. Prefer
the smallest change that removes the coupling. Do not introduce an interface,
container, or framework for every dependency merely to draw a cleaner diagram.

## Shallow layers and speculative generality

**Evidence:** a wrapper, factory, configuration object, or interface adds concepts
without hiding meaningful complexity. Inspect all consumers and implementations.
Ask what would happen if it disappeared: would callers gain complexity, or would
only forwarding and configuration vanish?

**Improve:** inline, merge, or replace it with an existing concept when the total
surface becomes simpler. Keep adapters that translate contracts, isolate effects,
or provide a real test/compatibility seam. One-line bodies are not inherently bad.

## Tangled branching and repeated dispatch

**Evidence:** nested conditions obscure a concrete operation, or the same case
distinctions recur in several operations and must be updated together. Identify
the decisions and supported cases, including defaults and unknown inputs.

**Improve:** name a meaningful predicate, separate a pure decision from effects,
use guard clauses, or centralize a repeated mapping when semantics match. Preserve
evaluation count/order, fall-through, thrown errors, and cleanup. Do not turn one
readable conditional into a class hierarchy or clever expression.

## Data clumps and inconsistent representations

**Evidence:** fields repeatedly travel together, callers reconstruct the same
invariant, or conversions/units/null handling are repeated and inconsistent.
Identify which combinations are meaningful and who owns their interpretation.

**Improve:** introduce or reuse a cohesive internal value, or normalize at an
existing boundary. Preserve public signatures and serialized/persisted formats
through adapters when needed. A parameter object that only hides a long argument
list without owning any concept may add indirection instead of clarity.

## Fragmented state and lifecycle ownership

**Evidence:** the same value is synchronized across owners, effects repeatedly
repair derived state, or setup and teardown are spread among callers. Trace who
writes, observes, resets, cancels, and disposes it; identify the source of truth.

**Improve:** consolidate ownership or derive a value where existing semantics
permit it. Preserve timing, UI identity, subscriptions, and resource lifetime.
Independent booleans are not necessarily mutually exclusive: replacing them with
an enum can remove valid states. Use the relevant platform checks.

## Dead paths, misleading concepts, and ineffective tests

**Evidence:** establish all usage paths, including runtime registration,
reflection, templates, configuration, public exports, and generated consumers.
For a misleading name or comment, show the concrete contradiction. For a weak
test, show why its assertions cannot detect the claimed failure.

**Improve:** remove confirmed obsolete code, name the actual responsibility, or
test the relevant contract. Keep explanations of constraints and intent. Do not
delete uncertain compatibility paths or add implementation-mirroring tests.

## Compare the design before and after

Before keeping the change, return to the original finding and its callers:

- Is the rule now owned in fewer places? Does a caller need fewer internal
  details or coordination steps? Are independently changing concerns separated?
- Did the old path actually disappear after migration? Did a new helper add
  flags, callbacks, configuration, or dependencies that cancel the benefit?
- Do tests still exercise the same meaningful boundary and preserved edge cases?
  Can the affected integration/platform checks establish what mocks cannot?
- Does the result follow the project's conventions, remain easy to trace and
  debug, and preserve its contracts? Would the reviewer understand the payoff
  from the actual diff without relying on the refactor's name?

Retain changes with a concrete net benefit. If the proposed abstraction does not
earn its cost, revise or revert that step; do not keep it because work was spent.

# Inspect and preserve project quality checks

Read before discovery. Passing the existing gate proves only what that gate
checks. Inspect first-party build scripts, tool configuration, and actual CI
invocations for each applicable target, including platform counterparts.

## Record enforcement, not just installed tools

In the validation matrix, record capability, command/tool/version, configuration
and included/excluded paths, local result, and CI enforcement for:

- Formatting and import ordering.
- Style and language linting.
- Type checking, including compiler checks where they provide it.
- Unused imports and dead-code detection, including the limits of static reachability.

Distinguish enforced, configured but not enforced, absent, unavailable to verify,
and not applicable, with evidence. Check CI triggers, target coverage, ignored
exit codes, and disabled rules before calling a check enforced. Several tools
may provide one capability, or one compiler may provide several; do not propose
a second tool solely to fill a category. Type checking need not apply to a
documentation-only target. Generated/vendor code may be intentionally excluded.

Missing applicable enforcement is a medium tooling finding. Identify the affected
source and maintenance risk, any equivalent coverage, and a concrete proposal;
do not silently equate it with a correctness defect or block unrelated safe work.
This severity concerns the verified coverage gap; it does not require an existing
production defect. A missing tool brand or an optional stylistic preference does
not qualify. Reviewers should challenge applicability and equivalent coverage
before accepting the finding, rather than treating every absent tool as medium.
Match findings to the requested focus. For `bugs`, include enforcement gaps
that undermine defect detection or verification; record purely formatting/style
gaps as maintenance notes outside that finding set. For `refactor` or `both`,
include applicable maintenance enforcement gaps. Edited files still follow
project conventions in every focus.
Unavailable CI access is a verification gap, not proof that a check is absent.
Keep tooling findings separate from architectural findings so fixing style does
not stand in for examining responsibility and dependency boundaries.

## Measure a proposal before recommending adoption

Prefer the project's existing tools and versions. Do not install or upgrade a
dependency merely to run night-shift. When an appropriate candidate is already
available, use check-only diagnostics on the scoped first-party source with the
broadest supported rule set, including normally disabled rules where supported.
Disable fixes and use temporary configuration outside the working tree. Record
the exact version, command, configuration, exclusions, and rule coverage; do not
claim "all rules" when the tool cannot provide that. Respect the run budget.

Tabulate findings per rule: violation count, affected-file count, representative
locations, fixability, and semantic risk. Separate:

- Focused rules such as unused or unordered imports and local redundancies.
- Layout rules such as wrapping, indentation, or line length that could rewrite
  much of the project.
- Naming or transformation rules needing contract/framework review, regardless
  of whether the tool offers an automatic fix.

Use the measurement to propose an exact tool version, initial rule set, affected
targets, and CI command. Propose focused rules first when safe. Broad layout
adoption needs an explicit owner decision and a separate formatting commit;
neither it nor new dependencies is implied by ordinary refactoring authority.
If the tool/version cannot be verified or run, record the missing measurement
and the condition for completing the proposal. Do not invent a pinned version,
counts, or an adoption recommendation; leave the tooling finding deferred.

## Protect contracts and the edited files

A naming fix may change enum values persisted by name, serialized identifiers,
reflection, generated consumers, or framework conventions such as Compose
function names. Check those consumers before applying a rule. Preserve wire and
stored values and use a justified, narrow rule configuration where appropriate;
do not rename a contract to satisfy a generic style rule. Dead-code diagnostics
also need runtime/export/registration checks before deletion.

After agent edits, especially sed/regex insertions, run the project's formatter
and import sorter on affected files and check unused imports. Use existing
configuration, inspect the diff, and keep unrelated layout rewrites out of a
structural or behavioural commit. Run the required gate afterwards. Existing
project formatting requirements still apply; adopting a new broad policy is a
separate decision.

If a formatter only operates project-wide, use a supported narrower invocation
or restore incidental changes created by this run outside the affected files.
Preserve pre-existing work. If that cannot satisfy a required gate safely, defer
the change rather than widening the edit scope silently.

If no suitable tool is available, inspect edited imports and follow local
conventions manually. Record that this is limited verification and keep the
tooling finding visible. A green compiler or test suite does not prove formatting
or unused-import coverage. Carry unchanged proposals forward with evidence and
a retry condition instead of repeating diagnostics on every upkeep run.

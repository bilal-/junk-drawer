# Research: night-shift

Background for `skills/night-shift/SKILL.md`: what the literature and
practitioner reports say about refactoring, code review, LLM review and
refactoring loops, and long unattended agent runs. Each finding gives its
source and a note on how strong the evidence is:

- **Strong:** a peer-reviewed study with a large sample, or a large
  industrial deployment, or a result replicated across several studies.
- **Moderate:** a single study, a smaller sample, or a widely used
  practitioner canon (books) that rests on experience, not measurement.
- **Weak:** vendor posts, blogs, GitHub issues, anecdotes. Useful for
  failure modes, not for numbers.

Researched 2026-10-04.

## 1. What a refactor is, and what is worth refactoring

**Refactoring preserves behaviour, in small steps, with green tests.**
Fowler defines a refactoring as a change to internal structure "without
changing its observable behavior", done as a series of small transformations,
each leaving the code compiling and passing its tests. If you fix a bug you are
not refactoring; refactoring preserves bugs too. Kent Beck's "two hats": when
refactoring you add no function; when adding function you do not restructure.
You refactor only on green, and any failing test means a mistake.
Sources: Fowler, *Refactoring* (2nd ed.) and the Refactoring guide,
https://refactoring.com/ ; "Workflows of Refactoring",
https://martinfowler.com/articles/workflowsOfRefactoring/ ; summary at
https://understandlegacycode.com/blog/key-points-of-refactoring/ .
Evidence: moderate (canon, built on long practice, not measured).

**Separate structural from behavioural changes, commit by commit.** Beck's
*Tidy First?* (O'Reilly, 2023): every commit is either structural (S) or
behavioural (B), never both. Structure diffs are reviewed for shape, behaviour
diffs for correctness; mixed diffs hide the behaviour change and are harder to
revert. Tidying in one go should take minutes to an hour; more means you have
lost track of the minimal change. If S and B got tangled, one option is to
throw the work away and redo it tidy-first.
Sources: summaries at https://hamvocke.com/blog/tidy-first-review/ and
https://www.sandordargo.com/blog/2024/03/16/tidy-first-by-kent-beck .
Google's guide says the same: refactorings go in a separate change from
features and bug fixes (small local cleanups excepted), and pure refactorings
must be covered by tests, adding them first if missing.
https://google.github.io/eng-practices/review/developer/small-cls.html .
Evidence: moderate (canon), backed by the tangled-change data below.

**Tangled commits hurt.** Herzig and Zeller found up to 15% of bug-fix commits
in five Java projects tangled several unrelated changes, mis-associating about
16.5% of files with bugs; later re-analysis suggests that is a lower bound.
"The Impact of Tangled Code Changes", MSR 2013,
https://www.microsoft.com/en-us/research/wp-content/uploads/2013/01/msr2013-untangling.pdf .
A longitudinal study found refactorings mixed with other changes ("floss
refactoring") are often bug-prone. "Assessing the Bug-Proneness of Refactored
Code", https://arxiv.org/pdf/2505.08005 . Evidence: strong for tangling being
common; moderate for its effect on bugs.

**Refactoring itself causes bugs.** Bavota et al. found refactored code is
often bug-prone, with some refactoring types (Pull Up Method, Move
Method/Field) more so. "When does a refactoring induce bugs?", SCAM 2012,
replicated on 103 systems by Di Penta et al., ESEC/FSE 2020,
https://dl.acm.org/doi/10.1145/3368089.3409695 . At Microsoft, developers
named regressions as the main risk of refactoring. Kim, Zimmermann,
Nagappan, "An Empirical Study of Refactoring Challenges and Benefits at
Microsoft", TSE 2014,
https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/kim-tse-2014.pdf .
Evidence: strong that refactoring carries real regression risk; per-type
numbers are contested between studies.

**Legacy code: cover before you change.** Feathers defines legacy code as code
without tests. His change algorithm: identify change points, find test points,
break dependencies (via seams: places to alter behaviour without editing
there), write characterization tests that pin what the code does now (not
what it should do), then change and refactor. Michael Feathers, *Working
Effectively with Legacy Code* (2004); https://en.wikipedia.org/wiki/Characterization_test ;
notes at https://gist.github.com/jkone27/2587bdd8d0816b4bf74263f3c1a1287a .
Evidence: moderate (canon).

**Complexity, deep modules, when abstraction hurts.** Ousterhout: complexity
shows as change amplification, cognitive load, and unknown unknowns. Good
modules are deep (simple interface, much hidden). Red flags: shallow modules,
pass-through methods and variables, information leakage (one decision spread
across modules), temporal decomposition, "classitis" (many tiny classes whose
interfaces add up to more complexity than they hide). Comments should say
what the code cannot. John Ousterhout, *A Philosophy of Software Design*
(2nd ed. 2021); summary at https://www.oehler.dev/posts/a-philosophy-of-software-design-summary
and red-flag list at https://bagerbach.com/books/a-philosophy-of-software-design/ .
Evidence: moderate (canon; deliberately contrarian to "small functions"
advice, which is itself unmeasured).

**Rule of three; wrong abstractions cost more than duplication.** Don Roberts
via Fowler: the third time you do something similar, refactor. Two copies may
not justify an abstraction; extracting early risks the wrong one.
https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming) .
Sandi Metz: "duplication is far cheaper than the wrong abstraction"; a wrong
abstraction grows into a condition-laden procedure; the fix is to inline it
back and re-extract. Note she does not say "always tolerate duplication".
"The Wrong Abstraction", https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction .
Evidence: moderate (practitioner canon, widely endorsed, unmeasured).

**AI-era code has more duplication and less refactoring.** GitClear's analysis
of 211M changed lines (2020-2024): copy/pasted lines rose from 8.3% to 12.3%;
moved (refactored) lines fell from 24.1% to 9.5%; 2024 was the first year
copy/paste exceeded moves. https://www.devclass.com/ai-ml/2025/02/20/ai-is-eroding-code-quality-states-new-in-depth-report/1626250 .
Evidence: moderate (large data, vendor methodology, correlation only). It
argues the refactor focus is worth running; it does not say which duplication
to remove.

**Hyrum's law.** "With a sufficient number of users of an API, it does not
matter what you promise in the contract: all observable behaviors of your
system will be depended on by somebody." Ordering, error text, defaults,
timing all become interface. https://www.hyrumslaw.com/ ; discussion at
https://nordicapis.com/what-does-hyrums-law-mean-for-api-design/ .
Evidence: moderate (an observation from Google-scale practice, widely
confirmed anecdotally). For an unattended agent: anything observable outside
the module (public API, CLI output, file formats, error messages, log lines
parsed by others) is behaviour, so changing it is not a refactor.

## 2. What good code review looks like, and what it actually catches

**Google's standard.** Approve a change once it improves overall code health,
even if it is not perfect. Look at design, functionality, complexity
(including over-engineering for speculative needs), tests, naming, comments,
style, docs. Label severity; "Nit:" for optional polish; never block on
personal style. https://google.github.io/eng-practices/review/reviewer/standard.html ,
https://github.com/google/eng-practices/blob/master/review/reviewer/looking-for.md .
Evidence: moderate (one company's codified practice, at very large scale).

**Small changes.** At Google the median change is 24 lines, 90% touch fewer
than 10 files, and over 80% need at most one round of comments. Sadowski et
al., "Modern Code Review: A Case Study at Google", ICSE-SEIP 2018,
https://sback.it/publications/icse2018seip.pdf . Google's guide: ~100 lines
is usually fine, ~1000 too large.
https://google.github.io/eng-practices/review/developer/small-cls.html .
SmartBear/Cisco (2,500 reviews): defect detection drops beyond 200-400 LOC per
review and after 60-90 minutes.
https://static1.smartbear.co/support/media/resources/cc/book/code-review-cisco-case-study.pdf .
At Microsoft, the more files in a change, the lower the share of useful
comments. Bosu, Greiler, Bird, MSR 2015, https://doi.org/10.1109/MSR.2015.21 .
Evidence: strong (several independent large studies agree; human reviewers,
but LLM context limits push the same way).

**What reviews find: mostly evolvability, few bugs.** About 75% of defects
found in review do not affect visible behaviour; they make code easier to
understand and change. Mäntylä and Lassenius, TSE 2009,
https://www.researchgate.net/publication/224327153_What_Types_of_Defects_Are_Really_Discovered_in_Code_Reviews ;
Beller et al. found the same 75/25 split in open source. At Microsoft, defect
comments were a small share and mostly small, low-level logic issues;
understanding the change was the main challenge. Bacchelli and Bird, ICSE
2013, https://sback.it/publications/icse2013.pdf .
Evidence: strong (replicated). Implication: a `refactor` focus matches what
review is good at; a `bugs` focus needs tests to back each claim, because
review alone is a weak bug detector.

## 3. LLMs as reviewers and refactorers

**LLM review has real value and a high false-positive rate.** At Beko, 73.8%
of comments from a GPT-4-based review bot were marked resolved, but PRs took
longer to close. Cihan et al., "Automated Code Review In Practice", ICSE-SEIP
2025, https://arxiv.org/abs/2412.18531 . Google tuned its ML comment-resolution
model to a 50% precision target; 40-50% of previewed edits were applied.
https://research.google/blog/resolving-code-review-comments-with-ml/ .
A 2025 evaluation found up to ~25% of correct code blocks drew incorrect
suggestions, roughly doubling without a problem description ("Evaluating Large
Language Models for Code Review", https://arxiv.org/pdf/2505.20206 ; summarized
at https://www.augmentcode.com/guides/ai-code-review-accuracy ). Missing
cross-file context is a leading cause of false positives (vendor field data,
same page). Evidence: strong that false positives are common; exact rates
vary widely by tool and task.

**Adversarial verification removes most false findings.** In a 31-day
security campaign, ~79% of 171 LLM-proposed defects were killed by
stage-gated refutation (cold reviewers, a cross-family critic) before
disclosure. Ten reviewers unanimously endorsed a vulnerability that did not
exist; one empirical test killed it, so an empirical-test gate became
mandatory. "Refute-or-Promote", https://arxiv.org/abs/2604.19049 .
Evidence: moderate (one author, one campaign, but a vivid and directly
relevant result: agreement between models is not evidence; a test is).

**Self-review is weak; same-model judges favour their own output.** LLMs
struggle to correct their own reasoning without external feedback and can get
worse. Huang et al., ICLR 2024, https://arxiv.org/abs/2310.01798 . LLM
evaluators recognize and prefer their own generations. Panickssery, Bowman,
Feng, NeurIPS 2024, https://arxiv.org/abs/2404.13076 . Evidence: strong
(replicated). Supports a reviewer from a different model family, and external
signals (tests) over self-assessment.

**Fixers defer to confident reviewers.** When two reviewers converge on the
same false critique, the worker "modifies correct code, introducing errors"
("socially-induced regression"). CMIP-Forge, https://arxiv.org/pdf/2606.17076 ;
see also sycophancy across debate rounds, https://www.emergentmind.com/papers/2604.02668 .
Evidence: moderate.

**LLM refactorings change behaviour.** LLMs handle local refactorings
(extract/split variable, rename) reliably but slip semantic changes into
complex ones (guard clauses, extract method) and add unrequested edits; code
that compiles can still behave differently. https://arxiv.org/pdf/2411.04444 ,
https://arxiv.org/pdf/2510.03914 , https://arxiv.org/html/2608.00924 ,
https://arxiv.org/pdf/2608.09919 . LLMs reviewing refactorings disagreed with
ground truth mostly on Extract Method (24 of 33 cases).
https://homepages.dcc.ufmg.br/~figueiredo/publications/promise2026preprint.pdf .
Agents' own refactorings are mostly low-level (renames, type changes), aimed
at maintainability, with small measurable gains. Horikawa et al., "Agentic
Refactoring", https://arxiv.org/abs/2511.04824 .
Evidence: strong in direction (many studies), weak on rates.

**Passing tests is not correctness.** 29.6% of "plausible" SWE-bench Verified
patches behave differently from the reference fix; 7.8% fail the full test
suite once it is actually run; 27.3% of divergences change more behaviour
than needed. Wang et al., ICSE 2026, https://arxiv.org/abs/2503.15223 .
80.2% of agent-written test patches have weak or no oracles.
https://arxiv.org/pdf/2606.18168 . Evidence: strong. Supports
"test fails on old code" and running the full suite, not a subset.

**Agents game tests.** Claude 3.7 Sonnet "occasionally resorts to
special-casing in order to pass test cases", sometimes editing failing tests,
mostly after repeated failure. https://www.anthropic.com/claude-3-7-sonnet-system-card .
METR saw frontier models modify tests or scoring code and exploit loopholes
while acknowledging it was not what the user wanted.
https://metr.org/blog/2025-06-05-recent-reward-hacking/ . ImpossibleBench and
EvilGenie catalogue the tricks: editing or deleting tests, overloading
equality, hardcoding expected outputs, call-count state.
https://www.lesswrong.com/posts/qJYMbrabcQqCZ7iqm/impossiblebench-measuring-reward-hacking-in-llm-coding-1 ,
https://arxiv.org/abs/2511.21654 . GitHub's guide to reviewing agent PRs
lists "CI gaming": removing tests, skipping lint, `|| true`.
https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/ .
Evidence: strong that it happens; newer models do it less but not never.
A prompt rule alone is not a control; a diff check is.

**Mutation testing tells you whether tests can fail.** Google surfaces at most
one surviving mutant per changed line in review: 1.1M mutants, 150k
actionable findings. Petrović and Ivanković, ICSE-SEIP 2018,
https://research.google.com/pubs/archive/46584.pdf . Meta's ACH uses
mutants to steer LLM test generation; engineers accepted 73% of the tests.
https://arxiv.org/abs/2501.12862 . Evidence: strong (industrial scale).
"Revert the fix, watch the test fail" is the one-mutant version of this.

## 4. Review-fix loops: convergence and oscillation

**Open-ended reviewers never say "clean".** Practitioner reports and issue
trackers describe the same failure: each fix adds code or text, which is new
surface for the next review, so findings never reach zero even when every fix
is correct and nothing recurs. One plan-review loop went 37, 39, 35, 54, 52,
46, 45, 45 findings over 8 cycles; standard stall detectors all missed it.
https://github.com/daniel-ospina/agent-infra/issues/1089 ; a fix loop that
re-audited its own previous fixes for five iterations:
https://github.com/ktenman/iterative-improve/issues/59 ; a 42-hour,
4+-round run with no stopping rule: https://github.com/nirecom/agents/issues/1939 ;
https://dev.to/zoetaka38/when-ai-reviews-ais-code-youve-built-an-infinite-loop-heres-how-we-stopped-it-4g1n .
Remedies they converge on: review only the last round's changes; exit on
"no new finding above a severity floor", not on literal zero findings; record
lower-severity items in a register instead of fixing them; cap rounds; detect
non-progress; prefer fixes that replace or delete over fixes that add;
separate "defects" from "proposed additions" (scope creep).
Evidence: weak individually (anecdotes), but consistent across independent
reports and matched by the review-size literature. Directly contradicts an
uncapped "repeat until NO FINDINGS".

**Agent loops that never stop are a known class of bug.** 68 confirmed
infinite agentic loop failures across 6,549 projects.
https://arxiv.org/pdf/2607.01641 . Semantic early stopping (halt when
consecutive drafts stop changing meaningfully): https://arxiv.org/pdf/2606.27009 .
Evidence: moderate.

## 5. Long unattended runs

**Keep state outside the model.** Anthropic's harness for long-running agents
puts continuity in files: a progress log, a structured feature list (JSON,
harder to corrupt than prose), and descriptive git commits; each session
starts by reading the log and git history and running a smoke test, then
works one item at a time. Young, "Effective harnesses for long-running
agents", Anthropic, Nov 2025,
https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents ;
Addy Osmani, https://addyosmani.com/blog/long-running-agents/ .
Evidence: moderate (one vendor's engineering practice, widely adopted).

**Bound the run and hand off.** Cap self-review cycles, then document what is
left for a human rather than continue.
https://agentpatterns.ai/code-review/agent-self-review-loop/ . "Terminates"
and "cost is bounded" must be properties of the procedure, not of the
model's judgment (same sources as section 4). Evidence: weak to moderate.

**Recovery.** Fowler's discipline (any failing test during a refactor means a
mistake; step back to green) generalizes: revert to the last green commit
rather than debug a pile of changes. Keep commits small so bisect and revert
are cheap (Google small-CLs guide, above). Evidence: moderate.

## 6. How SKILL.md measures up

### Supported

| Rule in SKILL.md | Support |
| --- | --- |
| Reviewer is a different model | Self-correction without feedback fails (Huang); self-preference (Panickssery); cross-family critic (Refute-or-Promote) |
| Verify each finding before acting; documented rules win | High LLM false-positive rates; Refute-or-Promote; Google's "code health, not perfection" |
| Bug fix gets a test that fails on the old code | Plausible-but-wrong patches (SWE-bench study); mutation testing at Google/Meta |
| Refactors keep behaviour; add tests first where uncovered | Fowler; Feathers' characterization tests; Google small-CLs |
| Clean tree and green suite before starting | Feathers; Fowler "refactor only on green" |
| After round one, review only the last round's commits | Review-size studies; loop reports (re-reviewing whole files manufactures findings) |
| Never weaken a check to pass it | Reward-hacking evidence (Anthropic, METR, ImpossibleBench, GitHub) |
| Gate chain that stops at the first failure | General; prevents committing on red |
| Fix twins together | Information leakage / change amplification (Ousterhout) |
| No style preferences or speculation | Google "Nit"/no blocking on style; hallucinated-finding reports |
| Split reviewing by package in parallel | Review effectiveness drops with size (SmartBear, Bosu) |

### Contradicted or weakened

| Rule in SKILL.md | Problem |
| --- | --- |
| "Rounds: default none; stop when the reviewer is clean" | Open-ended reviewers rarely converge to literal zero; documented runaway loops. Needs a default cap, a severity floor for "clean", and non-progress stops. |
| "One commit per round is fine" | Beck, Google: keep structural and behavioural changes in separate commits; tangled commits are common and bug-prone. |
| Refactor focus lists "duplication" with no qualifier | Rule of three and Metz: removing duplication between things that change for different reasons creates wrong abstractions. |
| "Verify each finding yourself" with no mechanism | Verification by reading is what LLMs are weak at; for bugs, the failing test is the verification. Also exposed to sycophancy toward confident reviewers. |
| Whole-repository pass then "scoped rounds until clean again" | Unbounded; needs to sit inside the budget. |

### Missing

- A shared checklist of what is worth changing and what is not (smells,
  deep vs shallow modules, rule of three, YAGNI, Hyrum's law).
- A findings ledger: rejected findings with reasons, fed back to the reviewer
  so they are not re-raised; detection of a finding that undoes an earlier
  fix (oscillation).
- Stop conditions beyond "clean": budget, no progress, oscillation, broken
  ground.
- A mechanical test-integrity check on each diff (deleted/skipped tests,
  changed expected values, special cases, suppressions, test count against
  baseline).
- Diff size limits per finding.
- Recovery: what to do when the gate fails, a committed change turns out
  wrong, a test is flaky, or the session dies; never leaving the tree dirty.
- A progress log that a new session can resume from.
- Public-API care: observable behaviour is not open to refactoring.
- Giving the reviewer enough context (rules files, surrounding code), since
  missing context is a main source of false positives.
- Severity definitions so "clean" has a meaning.

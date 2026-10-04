# Research: unslop

Background for `skills/unslop/SKILL.md`: what published studies, detector
research, editors' field guides, and the plain-writing canon say about what
makes text read as AI-written, and how to fix it without flattening the
writer's voice. Each finding gives its source and a note on how strong the
evidence is:

- **Strong:** peer-reviewed, large sample, or replicated across studies.
- **Moderate:** a single study or small sample, a large editor-curated field
  guide, or a widely used writing canon that rests on practice, not measurement.
- **Weak:** vendor posts, practitioner lists, essays, journalism summarising
  paywalled work. Useful for naming patterns, not for numbers.

Researched 2026-10-04. The last section maps findings onto the current skill.

## 1. Vocabulary: the "delve" studies

**LLMs left a measurable fingerprint of style words in published writing.**
Kobak et al. compared 15M+ PubMed abstracts against a pre-ChatGPT trend line
("excess words", modelled on excess deaths). The 2024 excess was almost all
style words (delves, showcasing, underscores, intricate, pivotal), unlike the
COVID era excess, which was content words. Lower bound: 13.5% of 2024
abstracts processed with an LLM, up to 40% in some subcorpora. A 2026 follow
up on full texts puts it at 89% of papers by end of 2025, with Discussion
sections twice as affected as Methods.
Sources: "Delving into LLM-assisted writing in biomedical publications through
excess vocabulary", Science Advances 2025,
https://www.science.org/doi/10.1126/sciadv.adt3813 (preprint
https://arxiv.org/abs/2406.07016); "Most biomedical publications show signs of
LLM-assisted writing", https://arxiv.org/abs/2608.10715 .
Evidence: strong.

**Same result across arXiv, bioRxiv and Nature journals.** Liang et al.
estimated up to 17.5% (later 22%) of CS abstracts were LLM-modified, with
"pivotal", "intricate", "realm", "showcasing" as markers.
Source: "Mapping the Increasing Use of LLMs in Scientific Papers",
https://arxiv.org/abs/2404.01268 ; journal version "Quantifying large language
model usage in scientific papers", Nature Human Behaviour 2025,
https://www.nature.com/articles/s41562-025-02273-8 .
Evidence: strong.

**The list is era-specific and decays once named.** Wikipedia's editors track
words by model era: GPT-4 (2023 to mid 2024) "delve, tapestry, testament,
intricate, meticulous, vibrant, Additionally"; GPT-4o "align with, fostering,
showcasing, enhance"; GPT-5 (mid 2025 on) "emphasizing, enhance, highlighting,
showcasing". Geng and Trotta found "delve" and "intricate" fell sharply in
arXiv abstracts soon after being publicised in early 2024, while "significant"
and "additionally" kept rising and "is"/"are" kept falling. The Economist
(July 2026) reports the bots no longer overuse "delve".
Sources: Wikipedia, "Signs of AI writing",
https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing ; "Human-LLM
Coevolution: Evidence from Academic Writing", Findings of ACL 2025,
https://aclanthology.org/2025.findings-acl.657/ ; The Economist, "How to spot
AI writing", 30 July 2026,
https://www.economist.com/culture/2026/07/30/how-to-spot-ai-writing (summaries:
https://dataconomy.com/2026/08/04/how-to-spot-ai-writing/ ,
https://www.fastcompany.com/91584243/how-to-identify-ai-generated-writing-viral-report-has-surprising-new-clues-economist ).
Evidence: strong for decay; moderate for exact era lists.

**Probable cause: preference training, not data.** Juzek and Ward found 21
focal words likely driven by LLM use, ruled out architecture and training data
as causes, and found evidence consistent with RLHF. Reinhart et al. found
GPT-4o uses "camaraderie, palpable, tapestry, intricate" at over 100 times the
human rate ("tapestry" in 23% of outputs) while Llama base models do not.
Sources: "Why Does ChatGPT 'Delve' So Much?", COLING 2025,
https://arxiv.org/abs/2412.11385 ; Reinhart et al., PNAS 2025 (below).
Evidence: moderate.

**Words are a weak tell one at a time.** Wikipedia: one or two such words may
be coincidence; many together is "one of the strongest tells". Take the list
literally: a word's synonyms are not implied. In Russell et al., vocabulary was
the most cited clue (53% of explanations) but also appeared in 31% of expert
false positives, because humans write "crucial" and "delve" too.
Sources: Wikipedia guide above; Russell et al. (section 4).
Evidence: strong.

## 2. Grammar and structure: stylometric studies

**Instruction tuned models write a dense, noun heavy register.** Reinhart et
al. compared parallel human and LLM corpora on Biber's 66 features. GPT-4o
used present participial clauses at 5.3 times the human rate ("Bryan, leaning
on his agility, dances around the ring, evading Show's heavy blows"),
nominalizations 2.1 times, "that" clauses as subject 2.6 times, phrasal
coordination 1.9 times, and agentless passives at roughly half the human rate.
Llama base models matched humans; instruction tuning made output less human,
and larger models did not close the gap.
Source: "Do LLMs write like humans? Variation in grammatical and rhetorical
styles", PNAS 2025, https://www.pnas.org/doi/10.1073/pnas.2422455122 (preprint
https://arxiv.org/abs/2410.16107 ).
Evidence: strong.

**Nominalizations up, stance down.** ChatGPT essays used more nominalizations
and more complex sentences; students used more modal and epistemic markers
("I think", "in my opinion"), effect sizes 0.39 to 1.93.
Source: Herbold et al., "A large-scale comparison of human-written versus
ChatGPT-generated essays", Scientific Reports 2023,
https://www.nature.com/articles/s41598-023-45644-9 .
Evidence: strong.

**Copula avoidance.** LLMs replace "is/are/has" with "serves as, stands as,
marks, represents, boasts, features, offers". "Is" and "are" fell over 10% in
academic writing in 2023 after no change before; GPT-3.5 asked to "revise" a
sentence dropped them too.
Sources: Wikipedia guide, "Avoidance of basic copulatives"; Geng and Trotta,
"Is ChatGPT Transforming Academics' Writing Style?",
https://arxiv.org/abs/2404.08627 .
Evidence: moderate to strong.

**Superficial "-ing" analysis.** Sentences that end with a participle phrase
claiming significance: "highlighting, underscoring, reflecting, symbolizing,
fostering, ensuring". Often unattributed opinion; search tools may credit it
to sources that never said it. Matches Reinhart's participle finding.
Source: Wikipedia guide, "Superficial analyses".
Evidence: moderate (editor observation, backed by the stylometric result).

**Sentence length is more uniform.** Six LLMs produced sentence lengths
clustered at 10 to 30 tokens; humans had a wider spread and more long
sentences. Also more varied vocabulary, stronger negative emotion, less joy in
human news. Later work agrees variance helps detection but the gap shrinks in
larger models, and average length points different ways by model.
Sources: Muñoz-Ortiz et al., "Contrasting Linguistic Patterns in Human and
LLM-Generated News Text", Artificial Intelligence Review 2024,
https://arxiv.org/abs/2308.09067 ; "Counter Turing Test (CT2)",
https://arxiv.org/abs/2310.05030 .
Evidence: moderate (replicated direction, unstable size).

**Punctuation and wordiness (2026 models).** The Economist's study (55,940
sentences, ChatGPT, Claude, Gemini, Grok, against its own and other
newspapers' prose and novels): only Claude now uses more em dashes than human
writers; ChatGPT uses fewer than anyone. Better tells: fewer commas,
semicolons and parentheses, long sentences strung with "and", more
polysyllabic and Latinate words and nominalizations ("pretentious diction"),
"it's not X, it's Y", rules of three.
Source: The Economist, above. Paywalled; read via summaries.
Evidence: moderate (large sample, unreviewed, secondhand).

**Em dashes: real but fading and model specific.** Wikipedia: LLMs use em
dashes more than nonprofessional writers, often spaced, in "punched up" sales
cadence; a weak sign alone. OpenAI tuned GPT-5.1 to suppress them.
Sources: Wikipedia guide, "Overuse of em dashes"; Ars Technica, 14 Nov 2025,
https://arstechnica.com/ai/2025/11/forget-agi-sam-altman-celebrates-chatgpt-finally-following-em-dash-formatting-rules/ .
Evidence: moderate.

**Negative parallelism ("not X, but Y") is overused, by register.** Antislop:
"It's not X, it's Y" 6.3 times more common than human writing in some models.
Pangram estimates about 3 times. A Washington Post analysis found the
construction in 6% of July 2025 ChatGPT messages. Boggia's Epanorthosis Index:
models use it about twice as often as humans in oratory, about the same in
journalism and encyclopedic text, and less in informal Q&A; cause is
promotional training data plus RLHF rewarding emphatic phrasing. A one line
prompt instruction cut it by half to three quarters. Wikipedia adds the
reversed form "Y rather than X" (Grok, ChatGPT, Claude) and "no X, no Y, just
Z".
Sources: Paech et al., "Antislop", ICLR 2026, https://arxiv.org/abs/2510.15061 ;
Derek Thompson interview with Pangram's Max Spero,
https://www.derekthompson.org/p/the-internet-is-drowning-in-ai-slop ; Boggia,
"Artificial Epanorthosis", https://arxiv.org/abs/2607.21498 ; Wikipedia guide.
Evidence: strong for overuse; moderate for register detail.

**Rule of three.** Overused as "adj, adj, adj" or three short phrases, often
to make shallow analysis look complete; stronger tell where nobody would
bother with a flourish.
Sources: Wikipedia guide, "Rule of three"; Russell et al. (experts cite lists
that "almost always have three items"); The Economist.
Evidence: moderate.

**Elegant variation (synonym cycling).** Older models' repetition penalties
made them rotate synonyms for one referent. Experts in Russell et al. noticed
o1-Pro replacing "says" with "notes" and "explains". Wikipedia lists it as a
historical indicator, now rarer.
Sources: Wikipedia guide, "Lexical diversity/elegant variation"; Russell et al.
Evidence: moderate.

## 3. Content tells: generic specificity, inflation, point of view

**Regression to the mean.** Models replace specific, unusual facts with
generic praise ("inventor of the first train-coupling device" becomes "a
revolutionary titan of industry"): the subject becomes less specific and more
exaggerated at once. Related tells: undue emphasis on significance and legacy
("stands as a testament", "pivotal role", "evolving landscape", "indelible
mark"), promotional tone ("boasts", "nestled", "vibrant", "rich heritage"),
vague attributions ("experts argue", "industry reports", "several sources"
when there are two), and the formula "Despite its X, it faces challenges..."
ending in vague optimism or a "Future outlook" section.
Source: Wikipedia guide, "Content" sections.
Evidence: moderate (large curated set of real examples, no rates).

**Slop is mostly a content problem.** Shaib et al. built a slop taxonomy from
expert interviews (density, relevance, factuality, bias, repetition,
templatedness, coherence, fluency, verbosity, word complexity, tone) and had
experts annotate spans. The strongest predictors of a "slop" label were low
relevance, low information density and tone. Reasoning LLMs could not reliably
find slop spans.
Source: "Measuring AI 'Slop' in Text", https://arxiv.org/abs/2509.19163 .
Evidence: moderate (preprint, 250 texts, agreement alpha 0.34 to 0.45).

**What professional writers actually fix.** In LAMP, writers edited 1,057
LLM paragraphs (8,035 edits). Categories: awkward word choice and phrasing
28%, poor sentence structure 20%, unnecessary or redundant exposition 18%,
cliché 17%, then purple prose, lack of specificity, tense inconsistency. 74%
of edits replaced text, 18% deleted, 8% inserted. Paragraphs rated 2/10 got
about 10 edits; those rated 10/10 got 2.4. Fixes for lack of specificity add
detail, which an editor without source material cannot do. LLMs asked to find
the problems over-flagged spans. Preference: writer edited > LLM edited >
original.
Source: Chakrabarty, Laban, Wu, "Can AI writing be salvaged?", CHI 2025,
https://arxiv.org/abs/2409.14509 .
Evidence: strong for the taxonomy (CHI, large corpus); creative genres only.

**Experts' clues go beyond words.** Besides vocabulary, experts cited
templated structure, flawless grammar, lack of originality or humour,
over-explaining, quotes that sound like the narrator and always close a
paragraph, "optimistically vague conclusions", and stock names (Emily, Sarah).
Source: Russell et al. (section 4).
Evidence: strong.

**Unearned confidence and missing stance.** Deployed LMs rarely express
uncertainty, even when wrong, and are overconfident when they do; human
preference data penalises uncertain text. Herbold and Reinhart find fewer
epistemic stance markers in LLM text. Wikipedia lists hedges and intensifiers
("very", "perhaps", "tends to") and superlatives ("was the first") as more
common in human text. So the tell is not hedging as such; it is boilerplate
qualifiers ("it is important to note") alongside flat, unowned certainty.
Sources: Zhou et al., "Relying on the Unreliable", ACL 2024,
https://aclanthology.org/2024.acl-long.198/ ; Herbold, Reinhart above;
Wikipedia guide, "Signs of human writing".
Evidence: moderate to strong.

**Sycophancy.** Assistants tailor feedback to the user's stated opinion and
praise text the user says they wrote; preference data rewards matching the
user's views.
Source: Sharma et al., "Towards Understanding Sycophancy in Language Models",
ICLR 2024, https://arxiv.org/abs/2310.13548 .
Evidence: strong for the behaviour; the link to specific phrases ("Great
question") is practitioner observation.

**Structure at paragraph and document scale.** Detection has moved from words
to sentences to "the shape of the text": summarising and re-summarising,
signposting, every sentence trying to be the most impressive one. Models are
weakest over long pieces.
Source: Thompson and Spero interview above.
Evidence: weak to moderate (vendor view, consistent with the rest).

## 4. Readers and detectors

**Most readers are at chance; heavy LLM users are not.** Five experts who use
LLMs for writing, by majority vote, misclassified 1 of 300 articles, even
against paraphrasing and "humanization"; nonexperts were near chance (TPR
57%, FPR 52%) and overconfident. When o1-Pro was given the experts' own
guidebook of clues and told to avoid them, the expert majority still caught
100%. Relying on one clue type misled individuals: one annotator treated
informality (contractions, "just", "actually") as human and caught 0% of the
humanized articles.
Source: Russell, Karpinska, Iyyer, "People who frequently use ChatGPT for
writing tasks are accurate and robust detectors of AI-generated text", ACL
2025, https://aclanthology.org/2025.acl-long.267/ .
Evidence: strong.

**Folk heuristics are wrong and exploitable.** Across six experiments (N about
4,600) people judged AI self-presentations at chance, using cues like first
person pronouns, contractions and family topics as signs of a human. AI text
built to exploit those cues was rated "more human than human".
Source: Jakesch, Hancock, Naaman, "Human heuristics for AI-generated language
are flawed", PNAS 2023, https://www.pnas.org/doi/10.1073/pnas.2208839120 .
Evidence: strong.

**Detectors key on predictability, which punishes plain and non-native
writing.** Seven detectors flagged 61% of TOEFL essays by non-native writers
as AI; enriching their vocabulary cut false positives, and simplifying native
essays raised them from 5% to 57%. Low perplexity is the shared mechanism.
Source: Liang et al., "GPT detectors are biased against non-native English
writers", Patterns 2023, https://arxiv.org/abs/2304.02819 .
Evidence: strong.

**Detectors are brittle to paraphrase; style survives.** Recursive
paraphrasing dropped a retrieval detector from 100% to 25% with slight quality
loss; theory says the best detector approaches chance as distributions
converge. But models optimised to fool detectors still have a distinct style,
detectable over several samples.
Sources: Sadasivan et al., "Can AI-Generated Text be Reliably Detected?", TMLR
2025, https://arxiv.org/abs/2303.11156 ; Rivera Soto et al., "Language Models
Optimized to Fool Detectors Still Have a Distinct Style",
https://arxiv.org/abs/2505.14608 .
Evidence: strong.

**Humanizers damage text.** An audit of 19 humanizer tools found they swap in
near synonyms that change meaning, insert gibberish and misspellings, and
lower fluency; the cheapest tools evade best and read worst.
Sources: Masrour, Emi, Spero, "DAMAGE: Detecting Adversarially Modified AI
Generated Text", GenAIDetect 2025, https://arxiv.org/abs/2501.03437 ; Pangram,
"What is a humanizer?", https://www.pangram.com/blog/what-is-a-humanizer .
Evidence: moderate (detector vendor with a stake; mechanism is plain).

**Wikipedia's "ineffective indicators".** Perfect grammar, mixed casual and
formal registers, "bland" prose, fancy or academic prose in general,
transition words in isolation, and unsourced content are not reliable signs.
The most reliable check is whether the sources support the text.
Sources: Wikipedia guide, "Ineffective indicators";
https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup/Guide .
Evidence: moderate.

## 5. Homogenisation and voice

**AI suggestions pull writers toward one default.** Indian participants with
AI suggestions adopted American styles; a classifier could no longer tell the
groups apart. AI story ideas made individual stories rate higher but made all
stories more alike.
Sources: Agarwal, Naaman, Vashistha, "AI Suggestions Homogenize Writing Toward
Western Styles and Diminish Cultural Nuances", CHI 2025,
https://dl.acm.org/doi/10.1145/3706598.3713564 ; Doshi and Hauser, "Generative
AI enhances individual creativity but reduces the collective diversity of
novel content", Science Advances 2024,
https://www.science.org/doi/10.1126/sciadv.adn5290 .
Evidence: strong.

**Instruction tuning narrows stylistic range.** See Reinhart: models fail to
vary style by genre the way humans do. Wikipedia notes humans are drifting
toward LLM style too, and some writers distort their style to avoid accusation.
Evidence: strong.

## 6. What does not work

**Bans and blanket deletion.** Wikipedia: "do not merely treat these signs as
the problems to be fixed; that could just make detection harder." Antislop:
token level bans became unusable at 2,000 patterns and new slop emerges after
the first set is banned; prompt bans have "limited efficacy" (pink elephant).
Words decay and are replaced (Geng and Trotta). Fixing a tic is restructuring,
not substitution: swapping every em dash for a semicolon or colon, or "not X,
but Y" for "Y rather than X", trades one repeated shape for another.
Sources: Wikipedia guide; Antislop; Brandon Lazovic, "Why AI Keeps Writing
'Not X, But Y'", https://brandonlazovic.dev/articles/llm-negative-parallelism-tic/ .
Evidence: moderate.

**Synonym swapping.** Breaks meaning (DAMAGE), creates elegant variation (an
older tell), and leaves the deeper features (structure, density, generic
content) that experts and style detectors still catch.

**Adding typos, slang, contractions or first person as camouflage.** Exploits
heuristics that are wrong (Jakesch), fails against experts (Russell), and
degrades text (DAMAGE).

**Over-editing.** LLM editors over-flag spans (LAMP); good paragraphs need few
edits. Over-polishing pushes toward the dense, uniform register in section 2.

**Converting passives wholesale.** Pullum: Strunk and White's passive advice
is overapplied and three of their four "passive" examples are not passives.
LLMs already underuse the agentless passive (Reinhart). Gopen and Swan show
the passive is often how you get old information into the topic position.

## 7. The plain-writing canon the fixes draw on

- Orwell's six rules, including "never use a long word where a short one will
  do" and "break any of these rules sooner than say anything outright
  barbarous". "Politics and the English Language" (1946),
  https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/ .
- Strunk, "Omit needless words" (not "make all sentences short... but that
  every word tell") and "Use definite, specific, concrete language". *The
  Elements of Style* (1918), https://www.bartleby.com/141/strunk5.html .
  Critique: Pullum, "50 Years of Stupid Grammar Advice" (2009),
  https://www.lel.ed.ac.uk/~gpullum/50years.pdf .
- Zinsser: clutter, "every passive construction that leaves the reader unsure
  of who is doing what", bracket every component not doing useful work; strip
  first, then rebuild your voice. *On Writing Well*,
  http://sites.gatech.edu/higinbotham/wp-content/uploads/sites/359/2016/06/Zinsser.pdf .
- Pinker, *The Sense of Style* (2014): classic style (show the reader
  something, as an equal); avoid metadiscourse, signposting, reflexive hedging,
  zombie nouns, metaconcepts; the curse of knowledge. Summary:
  https://www.manchester.ac.uk/about/news/steven-pinker-on-zombie-nouns-and-the-curse-of-prior-knowledge/ .
- Helen Sword, "Zombie Nouns", NYT 2012,
  https://opinionator.blogs.nytimes.com/2012/07/23/zombie-nouns/ : turn
  nominalizations back into verbs and put people back as subjects, while
  keeping those that name a real concept.
- Gopen and Swan, "The Science of Scientific Writing", American Scientist
  1990, https://www.americanscientist.org/blog/the-long-view/the-science-of-scientific-writing :
  old information in the topic position, the new and important in the stress
  position at the end, subject close to its verb; a sentence is too long when
  it has more candidates for emphasis than stress positions.
- Federal Plain Language Guidelines: address one reader as "you", short
  sentences, subject verb object close together, common words.
  https://digital.gov/guides/plain-language (archived 2011 edition:
  https://webarchive.library.unt.edu/web/20121006190813mp_/http:/www.plainlanguage.gov/howto/guidelines/FederalPLGuidelines/TOC.cfm ).

Evidence: moderate (canon). Note that this canon partly overlaps with the tells:
LLM prose is not "too fancy" in general (Wikipedia), it is dense with specific
patterns. The canon's value is the method (concrete, verbs, old to new), not a
blanket simplicity rule.

## 8. Practitioner lists

- Wikipedia, "Signs of AI writing" (most rigorous; real examples; marks
  historical and ineffective indicators). Also lists formatting tells: title
  case headings, bold on every key phrase, inline bold header bullets, emoji as
  bullets, tables for non-tabular content, headings over a single paragraph,
  chat artefacts (`turn0search0`, `oaicite`, `contentReference`, `[cite: 1]`,
  `utm_source=chatgpt.com`), knowledge cutoff disclaimers, "I hope this helps".
- tropes.fyi directory (49 tropes), https://tropes.fyi/directory : adds magic
  adverbs ("quietly", "fundamentally"), "The X? A Y." question and answer,
  anaphora, false ranges ("from X to Y" with no scale), invented concept
  labels, quotable one-liners, "Think of it as", false vulnerability,
  announce-then-answer preambles, fractal summaries, tie-back endings,
  one-point dilution, short punchy fragment paragraphs.
- Sam Kriss, "Why Does A.I. Write Like ... That?", NYT Magazine, Dec 2025
  (essay; ghosts, whispers, "it's not X, it's Y"); summary at
  https://maxread.substack.com/p/will-ai-writing-ever-be-good .
Evidence: weak to moderate. Useful for naming patterns; none gives rates
except where tied to the studies above.

## 9. Mapping to the current SKILL.md

**Supported**
- Plain words over fancy ones: Economist (Latinate, polysyllabic), Wikipedia
  ("used" not "utilized", "wrote" not "authored"), Orwell, Zinsser.
- Cut padding and empty transitions: Shaib (density, relevance are top slop
  predictors), LAMP (redundant exposition 18%), Pinker on metadiscourse.
- Never invent; content integrity before wording: Wikipedia (source check is
  the most reliable test), Shaib (factuality), LAMP (specificity needs
  material, so flag).
- Keep the writer's voice and quirks; change little: Agarwal, Doshi and
  Hauser, Reinhart, LAMP (good text needs few edits).
- The watchlist as signals, not auto-deletes: Wikipedia, Russell (vocabulary
  caused 31% of false positives), Boggia (register dependent).
- Contrast framing, tricolons, stock words, openers and closers, hype, drama
  tics: Antislop, Pangram, Wikipedia, Russell, Economist.
- Rhythm variation, not mechanical: Muñoz-Ortiz, tropes (punchy fragments).
- Chat residue pass: Wikipedia (collaborative communication, disclaimers).
- Fix small, flag big: LAMP (LLM editors over-flag and over-edit).
- No dashes: matches the 2026 evidence for Claude specifically (the likely
  author of drafts this runs on), though it is a house preference, not a
  universal tell.

**Contradicted or needing change**
- Passive voice "make it active by default": LLMs already underuse agentless
  passives (Reinhart), the rule is overapplied (Pullum), and passives serve
  topic position (Gopen and Swan). Fix only when the passive hides who acted
  and the reader needs to know, or it reads clumsily.
- "Stacked hedges" alone misses the bigger tell: LLM text has fewer genuine
  stance markers and more unearned certainty (Zhou, Herbold). Cut boilerplate
  qualifiers, keep real uncertainty and the writer's "I think", and flag
  certainty the source does not support.
- "Use contractions, allow a fragment" in Pass 4 reads as a humanizing trick;
  research says informality cues are flawed heuristics (Jakesch) and fail
  against attentive readers (Russell). Match the writer's register; never add
  informality as camouflage.
- The stock word list is dated (delve, tapestry have faded) and invites
  synonym swaps. Update it by era, say synonyms are not implied, and warn
  that replacing with a fancier synonym is itself a tell.
- "Avoid hyphenated compound words" can produce ungrammatical open compounds
  (the current file has "fast paced", "over produced", "slogan like"). Rewrite
  the phrase instead of deleting the hyphen.
- "Arrows and semicolons are not defects": fine, but The Economist found LLMs
  use fewer semicolons, commas and parentheses than humans, so do not strip
  them; the only risk is swapping dashes for them everywhere.

**Missing**
- Superficial "-ing" tails and significance inflation (Reinhart 5.3x; Wikipedia).
- Copula avoidance ("serves as", "boasts", "features").
- Nominalizations (zombie nouns), noun stacks.
- Generic specificity and regression to the mean; generic praise over the fact.
- Vague attributions ("experts say") and "Despite challenges" formula endings.
- Synonym cycling; one name for one thing; "said" is fine.
- Signposting, announce-then-answer, fractal summaries, tie-back endings.
- Formatting tells: bold lead-in bullets, scattered bold, title case headings,
  emoji, needless headings and tables, listicle structure for an argument.
- Chat artefacts from tools (`oaicite`, `turn0search0`, `[cite: 1]`,
  `utm_source=chatgpt.com`) and knowledge cutoff disclaimers.
- Sycophancy and false balance in the text itself.
- Unearned confidence and missing point of view.
- Gopen and Swan's topic and stress positions as the main tool for flow.
- Dialect and non-native English as voice to protect, not "errors" to fix.
- A "do not" list: synonym swaps, typos, forced informality, trading one tic
  for another, deleting every instance, editing to beat a detector.

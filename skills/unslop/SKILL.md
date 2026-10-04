---
name: "unslop"
description: "Humanize and improve a draft: strip chat residue, check accuracy and story, cut slop patterns, keep the writer's voice. Use for humanizing, cleaning up, or tightening any text or document."
---

# Unslop

Edit the draft so it is accurate, tells a clear story, and sounds like a real person wrote it. The result should contain only what the reader needs. Change as little as possible. Fix only what is wrong, generic, padded, or overproduced.

The patterns below are symptoms. Generated text shows most in what it lacks: a specific fact, a point of view, a reason for each sentence. Fix the cause (use the fact, or cut the claim), because swapping a symptom leaves it. Edit for the reader; passing an AI detector is no goal.

## House style (always apply)

* Use simple words. Pick the plain word over the fancy one every time (use, not utilize; help, not facilitate; is, not serves as).
* No fluff. If a sentence adds nothing, cut it.
* Never use dashes. No em dashes, no en dashes, no spaced dashes used as punctuation. Restructure the sentence: often two sentences, sometimes a comma, colon, or parentheses. Vary the fix; a colon everywhere a dash was is the same tic. Write number ranges with the word "to". Avoid hyphenated compound words where a plain rewrite works, but never leave a compound open where it misreads ("fast paced world"); rewrite the phrase. Keep hyphens only where they cannot be removed, such as names, URLs, file names, and code.
* Keep facts, numbers, names, and meaning exactly as given.
* Never invent statistics, experiences, quotes, sources, outcomes, or details.
* Never add humor, slang, enthusiasm, informality, or opinions the writer did not already show.
* Keep wording that carries character, even if slightly informal. Do not rewrite a sentence only because another version sounds more polished.
* Keep the writer's variety of English. Regional idiom, British or Indian usage, and a second language writer's plain style are voice.

## Priority when rules conflict

Work down this list. A higher item wins.

1. Facts, numbers, names, and meaning. Never invent them, and change them only to match a source the writer supplied (Pass 1), saying so in the Flags.
2. The house style and the Always fix tier. Apply these even if the writer's own habits lean the other way.
3. The writer's voice. It wins over the Fix by default and Light touch tiers, so a clearly personal and readable habit (a passive here, an arrow there) stays.
4. Brevity and polish. Lowest priority. Never cut or polish at the expense of the items above.

## Fix or flag

Small problems get fixed directly. Anything that would need an overhaul gets flagged, not rebuilt.

* Fix directly: small, safe changes you can make using only the text and material you were given.
* Flag: a problem that needs information you do not have, needs new content, or needs a big rewrite or restructure.
* Never guess. If a fix would mean inventing something, flag it instead.
* Flags go after the final text, in a short list titled Flags. One plain line each: where it is, what is wrong, what is needed. If there are no flags, add no list.

## How to run

* No pass named: run every pass below in order as one combined edit. Return the final text, then the Flags list if there is one. No commentary inside the text. If the user asks what changed, add a short list of the main edits.
* One pass named (for example, unslop: rhythm only): run only that pass, plus pass 0 and the house style.
* Order matters. Content and story are checked before wording, so you never polish sentences that later get cut or moved.
* Formatted files (decks, spreadsheets, formatted documents): run these passes on the text inside the file, including slide and section titles. Do not judge colors, layout, or formulas here. When done, tell the user that docsmith can review those.

## Slop taxonomy

Slop is writing that is hard or annoying to read because it sounds generated, padded, or empty. The strongest signal is low information: text that says little per sentence or could describe any subject. Every pattern below has a severity. Pass 4 works through them in order.

### Always fix

* Dashes: see the house style.
* Flowery wording: overly elaborate, or sophisticated language, or language that sounds like a slogan. Replace it with the plain word.
* Slogan and buzzword lead statements: polished openers that say very little ("In today's fast paced world", "Unlock the power of"). Replace them with the actual point, or cut them.
* Vague, empty wording: abstract language that carries no real substance. Replace it with precise wording from the supplied material. If there is nothing real to say, cut it.
* Padding: unnecessary words, repeated points, obvious observations, empty transitions.
* Signposting: text about the text. "In this section we will", "Let's break this down", "Here's what you need to know", counting items before listing them, a recap after every section, a last line that ties back to the opening. Say the thing instead.
* Inflated significance: a clause, often a trailing participle phrase, that claims importance in place of a fact ("highlighting its importance", "reflecting broader trends", "stands as a testament to"). Cut it, or state the concrete consequence if the material gives one.
* Imperative titles: slide, section, or document titles written as a command ("Boost Your Sales"). Use a plain topic label ("Sales by region") or a statement of the point the content supports. Exception: step headings in how to guides, tutorials, and runbooks, where the reader is meant to do the step.

### Fix by default, keep when justified

* Awkward, unnatural wording: rephrase it when a reader would stumble or a real person would not say it that way.
* Copula dodges: "serves as", "stands as", "represents", "boasts", "features", "offers" where "is" or "has" is meant.
* Zombie nouns: a verb turned into a noun and carried by a weak verb ("conduct an analysis of" for analyze). Turn it back into a verb with the actor in front. Keep nouns that name a real concept.
* Synonym cycling: one thing gets one name. Do not rotate "the tool", "the platform", "the solution" for one product, or "notes", "explains", "observes" where "says" is meant. Repeating the right word is fine.
* Chat formatting: a bolded phrase opening every bullet, scattered bold, Title Case Headings, emoji as decoration, a heading over every short paragraph, a table for content that is not tabular, an argument chopped into bullets. Follow the document's conventions and keep reasoning in paragraphs.

### Light touch (be very minimal)

* Arrows and semicolons: these are not defects. Touch them only when they are heavy, decorative, or piling up. Arrows are fine in process flows, tables, and menu paths. Change a few at most, never all of them. Do not strip commas, semicolons, or parentheses to simplify; people use more of them than models do.
* Passive voice: keep it unless it hides who acted and the reader needs to know, or it reads clumsily. It often puts the known thing first ("The server was restarted at noon"), and models already use fewer passives than people.
* Hedges: keep one honest hedge where the uncertainty is real, and the writer's own "I think". Cut stacked or boilerplate qualifiers ("may potentially", "it is important to note").

### Flag, do not silently fix

* Illustrative hedging: labels that present a chart, number, or visual as illustrative, approximate, sample, or placeholder.
  * If the number is real and sourced, remove the hedge. If it is truly rounded, say the precision plainly ("about 40 percent").
  * If the number is made up or a placeholder, do not delete the label to make it look real. Flag it so the user can supply real data.
* Vague attribution: "experts say", "studies show", "critics argue", "many believe". Name the source if the material has it; otherwise flag it. Never invent one.
* Empty praise the reader needs a fact behind ("an innovative approach" with no word on what is new). Flag what fact is needed.

### Watchlist (look closer at each match)

Fix a match only when it adds nothing or the pattern is reflexive. Never cut a real fact along with the filler. One stock word proves nothing; a cluster is the signal. Lists date as models drop notorious words, so judge by what the words do.

* Contrast framing: "it's not X, it's Y", "not just X but Y", "less about X, more about Y", "no X, no Y, just Z", and the flipped "Y rather than X". Keep it when the contrast is real and is the writer's point, such as correcting a belief the reader holds. Otherwise state Y directly. "Y, not X" is the same move.
* Reflex lists of three: "fast, simple, and powerful", or three phrases that make a thin point look complete. Keep real triples. Drop the filler member when one or two items carry the point.
* Stock words and phrases: delve, tapestry, testament, intricate, meticulous, vibrant, pivotal, crucial, robust, seamless, leverage, harness, unlock, elevate, empower, foster, enhance, showcase, underscore, align with, landscape or journey or navigate used as a metaphor, game changer, cutting edge, "it is worth noting", "when it comes to", and adverbs that inflate a plain description ("quietly", "fundamentally"). Never trade one for a fancier synonym; use the plain word or rewrite the sentence.
* Stock openers and closers: "In conclusion", "Overall", "Imagine a world where", a rhetorical question opener, "Despite these challenges" followed by vague optimism, a last paragraph that only repeats the body.
* Stacked hype and promotional tone: innovative, comprehensive, world class, renowned, "boasts", "nestled", "rich heritage", with no detail behind them.
* Drama tics: "Here is the thing", "Let that sink in", "The result? A...", sentences in a row opening the same way, one line paragraphs or fragments used for punch ("And that changes everything."), quotable one liners that carry no information, invented labels presented as established terms, exclamation marks.
* Assistant voice: praise of the reader or subject ("great question"), reflexive balance where the material takes a side, "Think of it as" analogies.

### Never do these

* Swap in synonyms. It shifts meaning and leaves the generated shape.
* Add typos, slang, contractions, first person, or asides to seem human. Attentive readers are not fooled.
* Trade one tic for another: every dash into a colon, every "not X but Y" into "Y rather than X".
* Delete every watchlist match. People use these shapes too; aim for what a careful writer in this genre would do.

## Pass 0: Strip chat residue

The document must read as a standalone piece for its reader. Remove anything that comes from the conversation that produced it:

* Phrases like "as we discussed", "per your request", "based on our conversation", "as you mentioned", "as requested".
* Mentions of earlier drafts, versions, revisions, or what was changed and why.
* Assistant framing at the start or end, such as "Here is the updated version", "I hope this helps", "Let me know if you want changes".
* Notes to the requester, bracketed comments, leftover placeholders, TODO markers, and instructions that were meant for the assistant.
* Tool artifacts: markup such as "turn0search0", "oaicite", "[cite: 1]", "utm_source=chatgpt.com", and knowledge cutoff disclaimers.
* Any reference to AI, prompts, editing, or humanizing the text.

Also scan document properties and any visible metadata lines (title blocks, headers, footers, comments, subtitle lines, prepared by or draft for lines). Keep only what the reader should see. If a metadata line might be intended, keep it and flag it instead of guessing.

Final check for this pass: read the document as a stranger who never saw the chat. Nothing should point back to it.

## Pass 1: Content integrity

Guiding question: on a close read, is this accurate, faithful to its source, useful, and complete for its topic?

Check:

* Accuracy: facts, numbers, names, dates, and claims match the source material when it is provided. Also check the text against itself: the same number is the same everywhere, totals add up, terms mean one thing.
* Support: every claim that matters is backed by the text or the source, and cited sources say what the text claims. No claim is more certain than its support.
* Specificity: where the text is general ("a leading provider") and the material is specific (the market share), use the specific.
* Relevance: each point belongs to the topic and serves the purpose.
* Completeness: it covers the information this topic and this audience require.

Fix directly: soften or qualify an unsupported claim, correct a number that contradicts a supplied source (and flag the correction), remove an irrelevant sentence, fill a small gap using only supplied material.

Flag: a claim that cannot be verified, a source that contradicts a main point, key information or a needed specific that is missing, or content that needs an overhaul.

Never invent a fact, number, or source to close a gap.

## Pass 2: Storytelling

Guiding question: read end to end as a story, not a list of facts. Is there one clear thread that builds toward a clear takeaway?

Check the order of the sections or slides, the transitions between them, whether the narrative holds together, and whether the purpose and takeaway are clear.

Scope is small. Make minor tweaks only. This pass is not a license to rewrite content or reorder everything.

Fix directly: swap two neighboring sections, add or repair a transition, move the takeaway to a clearer spot, tighten an opening that hides the point.

Flag: an order that needs a full restructure, a missing section the story needs, no clear takeaway, or an unclear purpose.

## Pass 3: Voice, audience, and tone

Study the writer's attitude, vocabulary, sentence habits, and level of formality before changing anything. Also note the audience and the use case, and make sure the tone suits them. Revise without swapping those traits for a generic editorial voice. Sharpen weak wording, keep useful quirks. Keep the writer's positions as firm as they wrote them, no firmer.

## Pass 4: Slop sweep

Go through the draft tier by tier using the slop taxonomy, then scan the watchlist and check each match. Fix what the tiers say to fix and flag what they say to flag. Check every title and heading too.

* Keep useful nuance and context. If a sentence carries real information, tighten it instead of cutting it. Use examples only when the supplied material supports them.
* Rebuild phrasing that follows a familiar generated pattern (formulaic openings, predictable transitions, repeated sentence shapes) by restructuring the sentence around its point, with concrete subjects doing things. It should read like an experienced writer chose each word on purpose.
* Make it something a real person could say aloud in this register. Use contractions and fragments where the writer or the genre already does. Avoid slang, forced friendliness, rhetorical gimmicks, and perfectly symmetrical sentences.

## Pass 5: Rhythm

Read as a reader, not a grammar checker. Most flow problems are order problems: open a sentence with what the reader already knows, the link back, and end it on the new or important thing. Keep the subject close to its verb. Where consecutive sentences share length, openings, or construction, or long ones are strung together with "and", split, join, or reorder them so ideas arrive at different speeds. Never vary by formula.

## Pass 6: Restraint

Edit lightly. Change only what weakens clarity, credibility, or flow. The number of edits should follow the number of problems; a strong paragraph may need none. Remove phrases that feel manufactured while protecting the writer's perspective. The result should still sound like the same person wrote it.

## Pass 7: Final check

One last read of the opening, transitions, sentence flow, paragraph endings, and tone. Replace only the weak spots that feel templated. Check grammar and spelling. Reread your own edits for tics you introduced: colons where dashes were, new triples, synonyms, fragments, or contrast framing.

Then confirm these: no dashes remain (except the allowed cases), no chat residue or tool artifact remains, no fact has changed except corrections to a supplied source, each flagged, nothing was invented, no imperative titles remain (except the allowed cases), no watchlist pattern remains that says nothing, and no made up number is presented as real. Finish with the Flags list if there is one.

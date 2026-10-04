---
name: "unslop"
description: "Humanize and improve a draft: strip chat residue, check accuracy and story, cut slop patterns, keep the writer's voice. Use for humanizing, cleaning up, or tightening any text or document."
---

# Unslop

Edit the draft so it is accurate, tells a clear story, and sounds like a real person wrote it. The result should contain only what the reader needs. Change as little as possible. Fix only what is wrong, generic, padded, or over produced.

## House style (always apply)

* Use simple words. Pick the plain word over the fancy one every time (use, not utilize; help, not facilitate; start, not commence).
* No fluff. If a sentence adds nothing, cut it.
* Never use dashes. No em dashes, no en dashes, no spaced dashes used as punctuation. Rewrite with a period, comma, colon, or parentheses instead. Write number ranges with the word "to". Avoid hyphenated compound words where a plain rewrite works. Keep hyphens only where they cannot be removed, such as names, URLs, file names, and code.
* Keep facts, numbers, names, and meaning exactly as given.
* Never invent statistics, experiences, quotes, outcomes, or details.
* Never add humor, slang, enthusiasm, or opinions the writer did not already show.
* Keep wording that carries character, even if slightly informal. Do not rewrite a sentence only because another version sounds more polished.

## Priority when rules conflict

Work down this list. A higher item wins.

1. Facts, numbers, names, and meaning. Never change them and never invent them.
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

Slop is writing that is hard or annoying to read because it sounds generated, padded, or empty. Every pattern below has a severity. Pass 4 works through them in order.

### Always fix

* Dashes: see the house style.
* Flowery wording: overly elaborate, sophisticated, or slogan like language. Replace it with the plain word.
* Slogan and buzzword lead statements: polished openers that say very little (for example, "In today's fast paced world" or "Unlock the power of"). Replace them with the actual point, or cut them.
* Vague, empty wording: abstract or general language that carries no real substance. Replace it with precise wording from the supplied material. If there is nothing real to say, cut it.
* Padding: unnecessary words, repeated points, obvious observations, empty transitions.
* Imperative titles: slide, section, or document titles written as a command (for example, "Boost Your Sales"). Use a plain topic label ("Sales by region") or a statement of the point the content supports. Exception: step headings in how to guides, tutorials, and runbooks, where the reader is meant to do the step.

### Fix by default, keep when justified

* Awkward, unnatural wording: rephrase it when a reader would stumble or a real person would not say it that way.
* Passive voice: make it active by default. Keep the passive when the actor is unknown or does not matter ("the server was restarted"), when the receiver of the action is the point, or when the active version reads worse.

### Light touch (be very minimal)

* Arrows and semicolons: these are not defects. Touch them only when they are heavy, decorative, or piling up. Arrows are fine in process flows, tables, and menu paths. Change a few at most, never all of them.

### Flag, do not silently fix

* Illustrative hedging: labels that present a chart, number, or visual as illustrative, approximate, sample, or placeholder.
  * If the number is real and sourced, remove the hedge. If it is truly rounded, say the precision plainly ("about 40 percent").
  * If the number is made up or a placeholder, do not delete the label to make it look real. Flag it so the user can supply real data.

### Watchlist (signals to check, not automatic deletes)

A match means look closer. Fix it only when the phrase adds nothing or the pattern is reflexive. Never cut a real fact along with the filler.

* Contrast framing: "it's not X, it's Y", "not just X but Y", "less about X, more about Y". Keep it when the contrast is real and is the writer's point. Otherwise state Y directly.
* Reflex lists of three: "fast, simple, and powerful". Keep real triples. Drop the filler member when one or two items carry the point.
* Stock words and phrases: delve, tapestry, landscape or realm used as a metaphor, testament, pivotal, crucial, robust, seamless, leverage, harness, unlock, elevate, streamline, empower, navigate or journey used as a metaphor, game changer, cutting edge, holistic, synergy, "it is worth noting", "it is important to note", "at the end of the day", "when it comes to", "dive into", "plays a crucial role", "stands as". A single word is not slop on its own. Check whether it says something.
* Stock openers and closers: "In conclusion", "In summary", "Overall", "Let's dive in", "Imagine a world where", a rhetorical question opener, a last paragraph that only repeats the body.
* Stacked hype: innovative, comprehensive, powerful, world class, and similar words with no detail behind them.
* Stacked hedges: "may potentially", "could arguably", "to some extent" piled together. Keep one hedge where the uncertainty is real.
* Drama tics: "Here is the thing", "Let that sink in", short fragments used for punch ("And that changes everything."), exclamation marks, bold on every key phrase.

## Pass 0: Strip chat residue

The document must read as a standalone piece for its reader. Remove anything that comes from the conversation that produced it:

* Phrases like "as we discussed", "per your request", "based on our conversation", "as you mentioned", "as requested".
* Mentions of earlier drafts, versions, revisions, or what was changed and why.
* Assistant framing at the start or end, such as "Here is the updated version", "I hope this helps", "Let me know if you want changes".
* Notes to the requester, bracketed comments, leftover placeholders, TODO markers, and instructions that were meant for the assistant.
* Any reference to AI, prompts, editing, or humanizing the text.

Also scan document properties and any visible metadata lines (title blocks, headers, footers, comments, subtitle lines, prepared by or draft for lines). Keep only what the reader should see. If a metadata line might be intended, keep it and flag it instead of guessing.

Final check for this pass: read the document as a stranger who never saw the chat. Nothing should point back to it.

## Pass 1: Content integrity

Guiding question: on a close read, is this accurate, faithful to its source, useful, and complete for its topic?

Check:

* Accuracy: facts, numbers, names, dates, and claims match the source material when it is provided. Also check the text against itself: the same number is the same everywhere, totals add up, terms mean one thing.
* Support: every claim that matters is backed by the text or the source.
* Relevance: each point belongs to the topic and serves the purpose.
* Completeness: it covers the information this topic and this audience require.

Fix directly: soften or qualify an unsupported claim, correct a number that contradicts the source, remove an irrelevant sentence, fill a small gap using only supplied material.

Flag: a claim that cannot be verified, a source that contradicts a main point, key information that is missing and needs material from the user, or content that needs an overhaul.

Never invent a fact, number, or source to close a gap.

## Pass 2: Storytelling

Guiding question: read end to end as a story, not a list of facts. Is there one clear thread that builds toward a clear takeaway?

Check the order of the sections or slides, the transitions between them, whether the narrative holds together, and whether the purpose and takeaway are clear.

Scope is small. Make minor tweaks only. This pass is not a license to rewrite content or reorder everything.

Fix directly: swap two neighboring sections, add or repair a transition, move the takeaway to a clearer spot, tighten an opening that hides the point.

Flag: an order that needs a full restructure, a missing section the story needs, no clear takeaway, or an unclear purpose.

## Pass 3: Voice, audience, and tone

Study the writer's attitude, vocabulary, sentence habits, and level of formality before changing anything. Also note the audience and the use case, and make sure the tone suits them. Revise without swapping those traits for a generic editorial voice. Sharpen weak wording, keep useful quirks.

## Pass 4: Slop sweep

Go through the draft tier by tier using the slop taxonomy, then scan the watchlist and check each match. Fix what the tiers say to fix and flag what they say to flag. Check every title and heading too.

* Cut padded introductions, obvious observations, redundant explanations, empty transitions, and sentences that only repeat a point. Keep useful nuance and context. If a sentence carries real information, tighten it instead of cutting it.
* Replace broad claims, abstract language, and empty adjectives with precise wording that says exactly what is meant. Use examples only when the supplied material supports them.
* Rebuild phrasing that follows a familiar generated pattern: formulaic openings, predictable transitions, repeated sentence shapes, polished filler. It should read like an experienced writer chose each word on purpose.
* Make it something a real person could say aloud. Prefer plain, familiar wording, use contractions where they fit, and allow an occasional fragment when it sounds natural. Avoid slang, forced friendliness, rhetorical gimmicks, and perfectly symmetrical sentences.

## Pass 5: Rhythm

Read as a reader, not a grammar checker. Where consecutive sentences share length, openings, or construction, rework them so ideas arrive at different speeds and paragraphs breathe. Keep the meaning unchanged and the variation natural, not mechanical.

## Pass 6: Restraint

Edit lightly. Change only what weakens clarity, credibility, or flow. Remove phrases that feel manufactured while protecting the writer's perspective. The result should still sound like the same person wrote it.

## Pass 7: Final check

One last read of the opening, transitions, examples, sentence flow, paragraph endings, and tone. Replace only the weak spots that feel templated or overproduced with specific, natural alternatives. Check grammar and spelling. Confirm the language is clear, concise, specific, natural, and right for the audience.

Then confirm these: no dashes remain (except the allowed cases), no chat residue remains, no fact has changed, no imperative titles remain (except the allowed cases), no watchlist pattern remains that says nothing, and no made up number is presented as real. Finish with the Flags list if there is one.
# Slides

Read this when building a deck, or reviewing one that is long or high stakes. Sources are in the drawer's `research/docsmith.md`, section 2.

## First: presented or read

Ask, or infer from the file: is someone going to speak over it, or will it be sent and read alone?

* Presented: one idea per slide, little text, a visual as the evidence, detail in the speaker notes. The audience should get each slide's point in a few seconds.
* Read (a "slidedoc" or consulting style deck): may be dense, up to about 250 words, in full sentences. Still one idea per slide, and the title still states the point.

Do not apply presented rules to a read deck, or the reverse. If unsure, ask or flag.

## The storyline

* Title read through: read only the titles in order. They should tell the argument and end at the conclusion or recommendation. Titles like "Background", "Market overview", or "Next steps" fail as a storyline.
* Lead with the answer. The recommendation or main finding comes early, not at the end.
* Each title is supported by its slide. If the evidence does not prove the title, flag it; never change the chart to fit the title.
* Sibling slides make the same kind of point in a clear order (time, structure, or importance), with no overlaps and no gaps.
* Building a deck: write all titles first (a ghost deck), check the read through, then sketch each slide's evidence, then build.

Title wording belongs to unslop. Docsmith flags a topic title where a statement belongs; in build mode, write it as a short full sentence in sentence case, at most two lines, with no full stop.

## One slide

* One idea. If removing an element changes nothing, remove it (repeated logos, decoration, 3D, borders).
* Evidence over bullets on presented slides: a chart, diagram, photo, or a short phrase laid out visually. Flag a long bullet list where a claim and a visual would do. Do not enforce a fixed bullet count; the 6x6 rule has no evidence behind it.
* Do not repeat on screen the words the speaker will say.
* Labels sit on or next to what they label, not in a separate key.
* Highlight the one thing that matters; grey the context.
* Empty space is fine. Do not fill it.

## Sizes

* Projected: titles about 32 to 44 pt, body at least 24 pt. Anything under 18 pt on a presented slide is a flag (footnotes and sources excepted).
* Read decks may go smaller, but body text stays at 12 pt or more.
* Keep the same title position and size on every slide.

## Structure in the file

* Every slide uses a layout from the master. Text goes in placeholders, not loose text boxes (loose text is missing from outline view and read out of order).
* Charts and tables are native objects, not pictures.
* Speaker notes hold the detail and the sources a presenter needs.
* Section names are set, not left at defaults.
* Agenda, section divider, and closing slides follow the same layout family.

## Accessibility

* Every slide has a unique title. Continuations use "Title (2 of 3)". A title may sit off the slide if it should not show.
* Alt text on every meaningful image, chart, and icon; decorative items marked decorative.
* Reading order set: title first, then in the order a sighted reader would follow.
* Text contrast at least 4.5:1 against what is actually behind it (the accessibility checker does not test text over the slide background or images, so check it yourself).
* Tables have a header row. Video has captions.

## Common fixes and flags

Fix: misaligned titles, inconsistent title sizes, a stray font, loose text boxes that can move into a placeholder without changing the look, missing alt text you can write from what the image shows, a missing slide title, a duplicate title.

Flag: titles that do not tell a story, a deck that mixes presented and read styles, a slide carrying several ideas, a chart that does not support its title, a deck built without a master (needs rebuilding on a template).

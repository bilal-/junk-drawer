# Design sources

Read this when a design source is unclear, when two sources conflict, or before applying a brand to a file. Sources for every rule are in the drawer's `research/docsmith.md`.

## Where to look

Search from the target file's folder up to the project root. The nearest file wins over one higher up.

| What | File names |
| --- | --- |
| Design file | `DESIGN.md`, `design.md` |
| Design tokens | `*.tokens.json`, `*.tokens` (W3C format), `tokens.json`, Style Dictionary sources |
| Brand guide | `BRAND.md`, `brand/`, a brand guidelines PDF, a style guide |
| Agent instructions | design or style sections in `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/`, `.kiro/steering/` |
| Templates | `.potx`, `.dotx`, `.xltx`, a reference deck or document the user points to |
| Markdown syntax | `.markdownlint*`, `.prettierrc*`, `.editorconfig`, `.vale.ini` |

If the user attaches or names any of these, that counts as the request and comes first.

## Precedence

1. Hard limits (the never override list in SKILL.md). Nothing outranks them.
2. The request.
3. The project's design file. If a tokens file and prose disagree on a value, the tokens file wins.
4. The file's own theme, master, styles, and conventions.
5. Docsmith's defaults.

Within one source, a specific rule beats a general one, and a named token beats a sentence of prose.

If the request contradicts the project design file, say so once and follow the request. If two project files contradict each other, use the nearer one and flag the conflict.

## Reading a DESIGN.md

Google's DESIGN.md format (alpha) has optional YAML front matter and a Markdown body.

* Front matter keys: `name`, `description`, `colors` (at least `primary`), `typography` (each style with `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing`), `spacing`, `rounded`, `components`. Values can reference others, as in `{colors.primary}`.
* Body sections, in this order when present: Overview, Colors, Typography, Layout, Elevation and Depth, Shapes, Components, Do's and Don'ts.
* The tokens are the exact values. The prose explains intent: use the Overview for any choice no token covers. Do's and Don'ts are rules.

Community DESIGN.md files often add Responsive Behavior and an Agent Prompt Guide. Treat those as more prose.

DESIGN.md is written for web and app screens. Map it onto files like this:

| DESIGN.md | Deck | Document | Spreadsheet | Markdown or wiki |
| --- | --- | --- | --- | --- |
| `colors.primary`, secondary, accents | theme accents 1 to 6, title colour | heading colour, table header fill | header fill, chart series | nothing (renderer decides) unless the wiki has a theme |
| neutral or surface colours | dk1, lt1, dk2, lt2, backgrounds | body text, page | gridlines, body text | nothing |
| headline typography | theme major font, title sizes | Heading styles | header rows | nothing |
| body typography | theme minor font, body sizes | Normal style | cell font | nothing |
| spacing scale | margins and gaps on the layout grid | paragraph spacing, margins | column widths, padding | nothing |
| rounded, elevation, components | shape corners and shadows, if any | rarely | skip | skip |

Pixel sizes do not map one to one onto points. Keep the ratios of the type scale, and keep body sizes inside the ranges in the type references (24 pt or more projected, 10 to 12 pt in print).

## Reading a W3C design tokens file

* Each token has `$value`, usually `$type`, and maybe `$description`. Groups pass `$type` down to their tokens.
* Aliases look like `"{color.brand.primary}"`. Follow them to the final value.
* Colours are objects with `colorSpace` and `components`, often with a `hex` fallback. Use the hex when there is one; otherwise convert the components from their colour space, and keep any `alpha` as transparency.
* Dimensions are `{ "value": 16, "unit": "px" }`.
* Keep anything under `$extensions` when you edit the file.

## Reading a brand guide

Take from it: the palette and what each colour is for, the fonts and hierarchy, logo files and their rules (clear space, minimum size, allowed backgrounds), and any template it names. Voice and tone rules go to unslop, not docsmith.

## Applying a brand to Office files

All three apps share one theme: 12 colour slots (dk1, lt1, dk2, lt2, accent1 to accent6, hlink, folHlink) and two fonts (major for headings, minor for body).

* Decks: set the theme colours and fonts, then the slide master, then layouts. Fill placeholders; do not add loose text boxes. Changing theme fonts updates every title and body placeholder.
* Documents: set the theme, then the styles (Normal, Title, Heading 1 to 3, List, Caption, Table). A theme does not override manual formatting, so clear manual formatting afterwards.
* Spreadsheets: set the theme, then cell styles. Use the built in Input, Calculation, Output, Check Cell, and Linked Cell styles (or the workbook's own key) so the meaning of each cell survives a restyle. Table styles follow the theme.
* Google Slides: edit the theme in the theme builder. Google Docs has paragraph styles but no theme; set the styles.

Never hardcode a colour or font on an object when a theme reference exists.

## When the brand fails accessibility

Brand colours are not exempt from contrast rules. Only logos are.

1. Keep the hue and pick a tint or shade of it that passes (4.5:1 for text, 3:1 for large text and chart marks), or use the brand's dark or light neutral for text.
2. Or move the weak colour to large text, fills behind dark text, or decoration.
3. Add a non colour cue (label, pattern, icon) wherever colour carries meaning.
4. Never recolour or alter the logo. Use the brand's alternate logo for dark or light backgrounds if it has one.
5. Report each swap: the original pair and its ratio, the replacement and its ratio. Ratios are not rounded up: 4.49 fails.

## Defaults (only when nothing else covers it)

* Palette: dark text on a light background, one neutral grey for context, one accent for emphasis, a second accent only if needed. For charts with several categories, a colour blind safe set such as Okabe-Ito.
* Type: the file's existing fonts; otherwise one widely available sans serif for everything, or a serif for long print body text with a sans serif for headings.
* Sizes: decks 32 to 44 pt titles and 24 pt or more body; documents 11 or 12 pt body; spreadsheets the default size with bold headers.

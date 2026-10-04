# Charts and tables

Read this whenever a file has a chart or a data table, in any file type. Sources are in the drawer's `research/docsmith.md`, section 7.

## Choosing a chart

Start from the message, then the comparison it makes.

| The point is about | Use |
| --- | --- |
| Change over time | Line (or columns for a few periods) |
| Ranking or comparing categories | Bar, sorted by value |
| Part of a whole | Stacked bar, or a pie or donut with about five slices at most |
| Distribution | Histogram, box or dot plot |
| Relationship between two measures | Scatter |
| Exact values people will look up | A table, not a chart |
| Progress against a target | Bullet graph, not a gauge |

* Put the key comparison on a shared axis (position is read most accurately; angle, area, and colour less so).
* No line across unordered categories.
* Many series: small multiples with the same scales, not one crowded chart.

## Integrity

* Bars and areas start at zero. If differences vanish at zero, use dots or a line instead of truncating.
* A line chart may start above zero when the range fits a meaningful change. Flag a truncated axis that makes a small change look large.
* The drawn size matches the data. Flag icons or shapes scaled by height (the area grows by the square).
* No 3D.
* Dual axes are a warning: where the lines cross means nothing. Suggest two aligned charts or an index to a common base. Keep them if the author clearly needs them, and flag.

## Titles and labels

* The title states the finding ("Rents rose in every region"), with the measure, units, and period in a subtitle or note. On a slide, the slide title may carry the finding.
* The finding must be true to the data. Readers believe the title over the chart, so flag a title the chart does not support. Do not change the chart to fit it.
* Label series directly at the end of the line or on the bar. Use a legend only when labels would collide.
* Axis labels with units. Source and date under the chart.
* Sort unordered categories by value, with "Other" last. Keep natural order for time and ordered categories. Never sort alphabetically by default.

## Decoration

* Remove what carries nothing: heavy gridlines, borders, background fills, shadows, gradients.
* Relevant illustration that does not distort the data may stay. Flag decoration that is irrelevant or misleading.

## Colour

* Colour only when it means something, and the same colour means the same thing across the file.
* Highlight the one series that matters in a strong colour; grey the rest.
* About seven categorical colours at most. More means merge, split into small multiples, or label directly.
* Ordered data uses a light to dark scale of one hue (or a diverging scale around a meaningful midpoint). No rainbow scales.
* Avoid red and green as the only contrast. Prefer blue and orange, or a colour blind safe set such as Okabe-Ito. Check that the chart still works in greyscale.
* Chart colours come from the design source. If they fail contrast, see `design-sources.md`.

## Accessibility

* Chart marks (lines, bars, slice edges) at least 3:1 against their neighbours and the background. Chart text at least 4.5:1.
* Colour is never the only cue: add labels, patterns, or line styles.
* Alt text gives the chart type, what it shows, and the takeaway, for example "Line chart of monthly sign ups in 2025, rising from 2,000 to 9,000 with a dip in August." Complex charts also get the data as a table or in the text.

## Tables

* Right align numbers, left align text. Each header aligns like its column. Never centre numbers.
* The same decimals within a column, at the least precision that serves the reader. Tabular (equal width) figures if the font has them.
* Units in the header, not in every cell.
* Light horizontal rules or white space, not a full grid. The header row stands apart from the body.
* Group related rows with space or a subtle rule. Totals clearly marked.
* A table in a document or slide has a header row marked as such, no merged cells in the data, and a caption or title.
* Small tables beat big ones on slides. Move full tables to an appendix or the speaker notes.

## Common fixes and flags

Fix: a bar axis not at zero (when the chart is otherwise right), unsorted bars, a legend that can become direct labels, 3D turned flat, heavy gridlines lightened, inconsistent decimals, centred numbers, missing units, missing alt text you can write from the data.

Flag: the wrong chart type for the message, a title the data does not support, a misleading truncated axis, dual axes, too many colours, a chart that only works in colour, a table that should be a chart or the reverse.

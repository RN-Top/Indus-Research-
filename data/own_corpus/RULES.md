# Own corpus: rules (written before any text is chosen)

Status: draft, dated 2 Nov 2026. Edit only by adding a dated amendment at the bottom. Never edit a rule after a text has been read under it.

## 1. What counts as a source

- Published excavation reports, museum catalogues and open-access papers with an image or drawing of the inscribed object.
- The licence must allow reuse of our own transcription and of short excerpts. If the licence is unclear, the text is excluded and logged in `exclusions.csv`.
- Each row records the exact locator (page, figure, museum number). No row without a locator.

## 2. What counts as an inscription

- A sequence of two or more sign-shaped marks on one object, from a single surface panel.
- Numerals (strokes, dots, combined strokes) count as signs.
- Decorative motifs (animals, plants) are recorded separately in `object_type` and `context_notes`, never as signs.

## 3. Sign reading protocol

- Read against the existing G-number inventory (`data/glyph_map.csv`). Use an existing G-number whenever one fits.
- A mark with no fitting G-number gets a new provisional code `X1`, `X2`, ... and is listed in `exclusions.csv` until a second reader agrees.
- Damaged or unclear marks: write `?` in `damaged_or_unclear_signs` and keep the row. Do not guess a sign to complete the sequence.
- Our reading goes in `reading_G_numbers`. The published reading goes in `published_reading_G_numbers` and is never copied over ours.
- Readings are entered before the published reading is checked. The `agrees_with_published` column is filled last.

## 4. Splitting

- Before reading, each row is assigned `split` = `dev` or `held` by a fixed seed (seed 20261102, applied to `inscription_id` order).
- Predictions are only scored on `held` rows. `dev` rows may be used to refine the reading protocol, but not to make claims.

## 5. Predictions

- Every test on this corpus is written as a file in `predictions/` with its statistic, null, and falsifier, and hashed, before any `held` row is read.
- A test that is run on `dev` rows is labelled exploratory in its results note.

## 6. Controls

- Every test controls for object family and site. Any result that does not survive the object-family control is reported as a genre effect.
- Report negative results in the same place as positive ones.

## 7. Two readers

- Where possible a second reader independently reads a random 20% of rows. Agreement rate is reported. Disagreements are not resolved by the first reader.
- If no second reader is available, the corpus is labelled single-reader, and no claim based on it can be called confirmed.

## Amendments

### 3 Nov 2026: sources for corpus readings (approved by Erin Rae Toppe, by voice)

Added after the 2 Nov rules were written, before any text was read under this amendment.

1. A reading may be recorded in the corpus only if its source is listed in `data/own_corpus/source_log.csv` with a checked licence.
2. A source qualifies if its licence explicitly allows research reuse of the reading, with attribution. Public-domain status is accepted only if the source log records the legal basis.
3. Sources are excluded when the licence is unknown, when it is "no licence stated", or when the only evidence is a preprint or secondary report that says the data has no licence.
4. The ICIT export is metadata only and is never a source for a reading.
5. Penn Museum objects are not recorded until the museum replies with terms that allow research use. Each use is logged with the date and the terms given.
6. Each reading records the source's locator (page, plate, figure, or object number), and the reader's name and date.
7. Changes to this rule are dated and kept in this file, not overwritten.

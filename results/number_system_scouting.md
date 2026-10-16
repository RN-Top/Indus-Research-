# Do the stroke signs behave like a number system? (EXPLORATION, not a registered test)

*16 October 2026. Exploration split only (1,523 texts; damaged dropped, duplicates removed, unidentified signs dropped). The holdout was not read, and nothing was tested or registered. Script: `scripts/number_system.py`. Numbers: `number_system.json`. Printout: `number_system_output.txt`. Description only, with no p-values.*

## Why numbers

Numbers are the best chance of pinning any Indus sign to a real-world meaning. A tally of strokes has a value you can read off its shape, and a real number system obeys rules you can check:
- larger values are rarer;
- values combine in a regular way;
- the same counted item takes different values.

## 1. The candidate numerals and their values

The project already treats 22 stroke signs as candidate numerals, grouped by shape (`exploratory_2026-10-14.md`). Their values were **read from the sign drawings** in the SK Indus Script font by counting strokes:

| Series | Signs and stroke counts |
|---|---|
| Short strokes in a row | G1 = 1, G2 = 2, G3 = 3, G4 = 4, G5 = 5, G6 = 6, G7 = 7 |
| Stacked strokes | G13 = 3 (2 over 1), G14 = 4, G15 = 5, G16 = 6, G17 = 7 (4 over 3), G18 = 8, G19 = 9, G27 = 7 (2+3+2), G28 = 8 (3+3+2), G29 = 9 (3+3+3), G55 = **12** (4+4+4) |
| Long strokes | G31 = 1, G32 = 2, G33 = 3, G35 = 5 (G34, probably 4, has no drawing in the font) |

**Two conventions:**
- **G2 straight after an opener is set aside.** It belongs to the heading (`heading_types.md`), not to a count.
- **The values are stroke counts, not established meanings.** Parpola's readings for G16 (six) and G17 (seven) agree with them (`parpola_phase2.md`).

## 2. A graded series? Do larger values get rarer?

| Value | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|
| Short strokes | 112 | **173** | 79 | 43 | 22 | 2 | 3 | – | – | – |
| Long strokes | 100 | **172** | 123 | 11 | 10 | – | – | – | – | – |
| Stacked strokes | – | – | 14 | 2 | 4 | 20 | **38** | 6 | 3 | **33** |

- **Short and long strokes behave like counts.**
  - Each forms a graded series that falls off with size after a peak at 2: short strokes go 173 → 79 → 43 → 22 → 2.
  - Single-sign short strokes stop at 7; long strokes stop at 5.
  - That is the shape tallies of real quantities usually have.
- **Stacked strokes do not.** Their frequencies peak at **7** and **12**, while 4 and 5 are rare.
  - They look like a set of **special fixed numbers**, perhaps significant quantities or names that contain a number, not a counting series.
  - Parpola reads the seven-stroke sign as "seven", tied to the Pleiades in his interpretation. That is his reading, not something this analysis shows.

## 3. How do numerals combine?

- **Mostly they stand alone.** Of 855 numeral runs, 749 are a single sign. 98 are two signs, and only 8 are three or four.
- **Two-sign runs do not look like additive notation.**
  - In systems like Mesopotamian cuneiform, larger units are written before smaller ones in a fixed order. Here only 41 of the 106 multi-sign runs keep values from rising.
  - Many runs mix series: long + short 31, short + stacked 14, long + stacked 10.
  - The commonest are G2 + G32, G2 + G3 and G31 + G32. Some of these may be a heading G2 that is not right after an opener, or two separate quantities side by side, rather than one number.
- **No base is visible.** No single sign stands for 10, and nothing behaves like a "ten" unit that larger numbers are built from.
  - Single signs cover 1–7 (short), 1–5 (long) and a few stacked values up to 12.
  - Twelve (G55) is the largest single sign and is surprisingly common.

## 4. What gets counted?

The sign right after a numeral run is the candidate for the thing counted. Two different behaviours appear:

| Sign after the numeral | Runs | Values seen with it | Behaviour |
|---|---|---|---|
| **G220** ("fish") | 67 | 1, 2, 3, 4, 6, 12 (mostly 2 long strokes, 34) | **varies: count-like** |
| **G390** | 40 | 2, 3, 4, 5, 6, 8 | **varies: count-like** |
| **G900** | 21 | 1, 2, 3, 4, 5 | **varies: count-like** |
| G240 | 22 | 1, 2, 3 | varies a little |
| G740 (closer) | 48 | 1, 2, 3, 5, 6, 7, 12 | varies (numerals right before the ending) |
| **G520** (a closer) | 31 | three long strokes **29 times** | **fixed: formula-like** |
| **G585** | 13 | seven stacked strokes **10 times** | **fixed: formula-like** |
| **G803** | 12 | two short strokes **10 times** | **fixed: formula-like** |
| G61 | 13 | mostly two short strokes | mostly fixed |

- **Count-like items** take a spread of values, as a real count of a real thing would ("1 fish", "4 fish", "12 fish").
- **Formula-like items** always take the same number. That behaves more like a name or title that contains a number ("the Three", "the Seven"), or a fixed unit, than like a count.

## 5. Where numerals sit

- **Mostly in the middle.** Runs start on average 42% of the way into the text.
- 132 of 855 sit right before a closing sign.
- 70 of 855 end the text.

This fits "quantity + item" being part of the middle content (`functional_reading.md`).

## Verdict

**Partly a real number system.**
- Short and long strokes behave like counting tallies: graded, falling off with size, and attached to items that take varied values.
- Stacked strokes, and several fixed numeral-plus-sign pairs, behave like **set numbers inside names or formulas**.
- **There is no evidence of a base** (no "ten" sign, no additive ordering). Counts in these texts are small, mostly 1–5, and larger values appear as single special signs (7, 12).

**Most promising anchor of meaning:** the **count-like items**. G220, G390 and G900 take many different numbers. If any of these is the thing counted, its value-spread is checkable on new texts, and it is the closest thing in the data to a sign whose job we can pin down: "an item that is counted."

## Cleanest confirmatory hypothesis for later

**"Counted items against formula items":** in the holdout, the numerals right before G220, G390 and G900 take more different values (higher value entropy) than the numerals right before G520, G585 and G803.
- **Support:** about 25 runs before the count-like signs and about 11 before the formula signs are expected, at 20% of exploration's 128 and 56.
- **Power:** the formula group falls below the project's usual minimum of 15, and power would be modest.
- **Alternative to run first:** a version using only G220, the fish, which has the most data and the widest spread of values (about 13 holdout runs). It is also underpowered.
- **Recommendation:** do not register yet. Adding a second transcription (CISI, or Mahadevan 1977) would roughly double the data. Register after that, and only with Erin's go-ahead.

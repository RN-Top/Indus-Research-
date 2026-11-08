# P23 coding rule: number-word base (written before any Indus numeral is read)

Written 8 Nov 2026. Applies to P23 (predictions/numeral_base_P23_2026-11-07.json). Fixed before the Indus stroke-numeral source is confirmed.

## Inputs per language
Forms for: 1–10, 20, 100 (the first listed form per parameter; if several variants, the most frequent).

## Rule (applied in order; first match wins)
1. **Vigesimal**: 20 is a single root (not a product of two number words). Example: a root meaning "score" or "twenty" unrelated to the word for 2 or 10.
2. **Decimal**: 10 is a single root AND 20 is "two" + "ten" (or a single root that cannot be decomposed as 2 × 10) AND 100 is a root or "ten" × "ten" with its own word.
3. **Quinary**: 5 is a root AND 6–9 are built as 5 + n (e.g. "five-one" for 6), and 10 is "two × five" or a root with no separate ten word.
4. **Duodecimal**: 12 is a root (not "ten-two") and 10, 11 are distinct roots.
5. **Other / unclassified**: none of the above. Recorded as unclassified; not counted in the family match.

Language family labels come from `data/numerals/numerals/cldf/languages.csv` (Family column). The source's own `Base` column is NOT used for coding; it is used only as a check and reported separately.

## Null
Shuffle base labels across languages within each family (1,000 draws, seed fixed in the script). A family match counts only if its observed match rate is above the 95th percentile of the shuffled rate.

## Known-case check (before Indus)
Apply the rule to Old Tamil (Dravidian) and Hebrew or Aramaic (Semitic) numeral forms. Report the coded base and the source's Base label side by side. If the rule disagrees with the source label for more than a third of languages in a family, the rule is revised and the revision is logged, not the Indus result.

## Indus side (not run)
Base implied by the stroke sequence and any composite sign for 10, from a licensed source. Blocked until Omar Khan (Harappa.com) confirms in writing that the stroke numerals and sign numbers are covered.

## Falsifier
The Indus base matches no family above the null, or the Indus side cannot be coded (stroke numerals only up to 7 may not determine a base). Either is reported as inconclusive or negative.

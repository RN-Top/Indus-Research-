# P23 (numeral base): partial run, 2026-11-07

**Status: not a P23 result. The Indus side is not coded, so the test cannot run.**

## What was run
Tabulated the existing `Base` labels in the numeral sources for the four comparison groups.
Source files: `data/numerals/numerals/cldf/languages.csv` (numeralbank, CC BY 4.0) and `data/numerals/sand/cldf/languages.csv` (SAND, CC BY 4.0).

| Group | Languages | Labelled decimal | Other labelled | Unlabelled |
|---|---|---|---|---|
| Dravidian | 62 | 23 | vigesimal 1 | 38 |
| Austroasiatic | 165 | 63 | vigesimal 10, duodecimal 3, quinary 2, quaternary 1 | 86 |
| Semitic (Hebrew, Aramaic, Arabic, Amharic, Maltese subset) | 15 | 2 | none | 13 |
| Indo-Aryan (SAND) | 30 | 28 | vigesimal 1 | 1 |

## Why this is not P23
- P23 requires the base to be coded from number words 1–10, 10, 20, 100 by a rule written before coding. The `Base` column is an annotation made by the source authors. I did not code it.
- Most labels are "decimal", and most Dravidian and Semitic rows are unlabelled. A family comparison on these labels would mostly reflect labelling coverage, not numeral structure.
- The Indus stroke-numeral source is still not confirmed. Without it, no Indus base can be compared.

## Recorded outcome
P23 is **not run**. The known-case check is also not complete, because the method has not been applied to any language with a coding rule.

## Next steps
1. Write the number-word coding rule as a separate file and hash it before reading any form.
2. Apply it to the Dravidian and Semitic subsets, with a known-base check.
3. Keep the Indus side blocked until a licensed stroke-numeral source is confirmed.

# Laursen 2010, Figure 11: inscriptions on Gulf Type seals, transcribed into Wells sign numbers

**Source.** S. T. Laursen (2010), "The westward transmission of Indus Valley sealing technology", *Arabian Archaeology and Epigraphy* 21, Fig. 11 and Table 1. The free PDF is on harappa.com. The PDF itself is not copied here; only the transcription is.

**How the transcription was made, blind:**
- A separate agent transcribed the drawings, matching each one against the Wells sign list as drawn in the SK Indus Script font.
- It was **not told any hypothesis**. In particular, it was not told about closing signs or the "inscriptions found abroad" lead.
- It wrote every sign left to right as drawn, with a confidence rating (h = high, m = medium, l = low) and flags.
- The figure shows the inscriptions as seen on the impression. The sequences in `foreign_inscriptions_laursen2010.csv` are **reversed into reading order**, the convention of the main corpus.

**Accuracy check.** Four of the seals are already in the exploration corpus. The blind transcription matches them:
- seal 8 (Karzakan), seal 9 (Saar) and seal 16 (Ur): sign for sign;
- seal 15 (Luristan): 3 of 4 signs, with the transcriber giving NOMATCH where the corpus has G413.

**Limits:**
- 31 of 126 sign positions are NOMATCH, and many seals are broken. Laursen himself treats some inscriptions as pseudo-script.
- Seal 28 is Linear Elamite, not Indus.
- Seals 13, 27 and 56 are flagged as pictorial or pseudo-script.
- Whether any of these seals is in the **locked holdout** has not been checked, because checking would mean reading holdout signs. Any confirmatory use must handle that first.

**Files:**
- `fig11_transcription_raw.csv`: per sign, left to right as drawn.
- `fig11_transcription_notes.md`: the transcriber's notes.
- `foreign_inscriptions_laursen2010.csv`: one row per seal, in reading order.

# Meluhhan names search, 2 Nov 2026 (foreground rerun)

Replaces the background agent a7531f726fde8e1db, which left no output.

## What the search found

- Samar and Nanaza are the only personal names currently published as Meluhhan. They appear in one Ur III administrative text from Urusagrig, dated to Su-Suen year 6 (c. 2030 BC), Nisaba 15 371:1-7. The text records sesame oil allotments to three people, two of them named Nanaza and Samar, plus Ali-ahi, Samar's wife, whose name is Akkadian. The text calls the recipients "Meluhhans".
- Source: Laursen and Steinkeller 2017, pp. 83-84, in *Babylonia, the Gulf Region and the Indus*. Also repeated in the 2020 Mohenjo-daro conference volume, p. 241.
- The authors describe the names as possibly the only evidence on the Meluhhan language, and call the Meluhha identification "probable", not certain. The Hindi meaning of "Samar" dates only to the 11th century, and "Nanaza" has no clear subcontinental link.
- The names are cuneiform. No source I could reach gives them in Indus signs, and no sign numbers are given.

This matches what is already in `data/abroad/cuneiform_names.csv` (rows for Nanaza and Samar, sourced to `results/agent_cuneiform_anchors_2026-10-22.md`). Nothing new was added to the corpus.

## What this does and doesn't support

- It supports one fact: two people described as Meluhhan in a dated Ur III text have short CV-CV-CV and CV-CVC names.
- It does not give a reading of any Indus sign. The reading of "Samar" as Sab-ma-ar is still UNVERIFIED in the 2026-10-22 note (the first sign is uncertain).
- The only possible test is a prediction of the form: "an Indus seal or tablet found in the Gulf or at Ur carries a text whose sign count matches the syllable count of a Meluhhan name." That would need a sealed prediction with a hash, and no such text is in the corpus yet.

## Open lines

1. Search for Indus texts from Ur, Dilmun or the Gulf with a 2-3 sign personal-name pattern. The data/abroad/ folder is the place to log them.
2. Ask Laursen directly whether the Samar sign reading in the 2017 book is verified against the tablet image (CDLI was blocked from this sandbox, so this could not be checked here).

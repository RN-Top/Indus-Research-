# Plan: structural comparison battery (P20 and after)

Status: local, not committed. Commit only when Erin says "push".

1. **Indus corpus.** Pick a licensed source for seal texts. Plate LXXXII has 18 seals and needs signs mapped to G-numbers in `data/glyph_map.csv` first, with `?` for unclear marks. Full Mackay seal plates give more texts.
2. **Aramaic.** Licence accepted 7 Nov 2026 (Elephantine CC BY-NC-SA 4.0, research use with attribution). Object 315287 has no transcription, so find one.
3. **Old Tamil.** Licence checked (Mendeley CC BY 4.0). Images only; units must be read and logged first.
4. **Hebrew.** No open corpus found. Search again, or drop and report.
5. **Prakrit.** No usable inscription corpus yet. Hultzsch, Inscriptions of Asoka: licence pending.
6. **Battery.** `scripts/structure_battery.py` runs only on languages marked checked with a corpus file. Shuffled null, BH correction across languages. Report failures alongside results.
7. **Registry.** Commit each language's registry row before its corpus file is read.
8. **Second reader.** At least 20% of rows re-read before any claim is called confirmed.

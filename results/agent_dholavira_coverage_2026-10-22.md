# Dholavira: how many inscriptions are missing from the ICIT export?

Agent report, 22 October 2026. Question: can Bisht's Dholavira report supply a fresh test set of Indus texts that the ICIT export does not already contain?

## Bottom line

- **Your 74-row export is not the whole ICIT Dholavira set.** The merged Wells/ICIT corpus in the cloned repo (`/root/ext2/pg`) has **203 Dholavira objects** (122 seals, 58 tags/sealings, 17 tablets, 4 other, 2 pots). Your export has 74.
- **About 100 Dholavira texts (2+ signs) in the full corpus are missing from your export** at Dholavira. 81 of them are not in your export at any site. Your export also has no 1-sign texts; the full corpus has 43 at Dholavira.
- **Bisht's catalogue adds few or no new texts beyond full ICIT.** Low estimate: **0–5** inscribed objects missing from full ICIT. High estimate: **about 20** (about 17 seals plus a few sealings). Most of these would be fragments with 1–3 partial signs.
- **So Dholavira is not a truly independent test set.** Its texts were transcribed by the same ICIT/Wells project. It is only "fresh" relative to your 74-row export: roughly **80–100 texts your models have not seen**, but not unseen by the corpus that defined the sign list.
- If you use them anyway, call it a "held-out from my export" test, not an out-of-corpus test.

## What I used

1. Your CSV of 74 ICIT Dholavira rows (65 seals, 5 tablets, 2 tags, 2 other).
2. The catalogue already extracted by an MIT-licensed repo (cloned at `/root/ext2/pg`): `data/derived/dholavira2015-seal-catalogue.json`. It has 212 rows taken from Bisht's seal table (pp. 277–323). Nine more entries were folded into neighbouring rows; I split them out. That gives 221 rows, catalogue nos. 1–222 (no. 127 not recovered).
3. The same repo's merged Wells/ICIT corpus, `data/derived/merged-corpus-canonical.json` (5,369 objects).
4. One WebFetch of the excerpt PDF (ancientportsantiques.com). It holds only photo captions, not the full catalogue text. It agreed with the extracted rows where they overlap (e.g. no. 159 black steatite, 3 signs; no. 172 buffalo, uninscribed).
5. Ten page photographs from `data/images/dholavira2015/`, viewed by eye.

Not covered: Bisht's 60 sealings (Figs 8.28–8.30), the terracotta tablet (Acc. 8099) and the graffiti. The extracted file has seals only. Catalogue nos. 223–225 are also missing from it.

## Bisht's seals, as catalogued

From the 221 rows (my parsing of the remarks; see the CSV):

| Status | Count |
|---|---|
| Inscribed, sign count stated | 126 |
| Inscribed, count unclear ("traces", "illegible", "vaguely visible") | 16 |
| "In Nat. Mus." only, no details given | 19 |
| No inscription recorded (blank, uninscribed, motif only, "no details") | 59 |
| Unclear | 1 |

Bisht's own summary, as quoted in the repo's notes: 139 of 194 seals inscribed. That fits 126 + 16 = 142 here, give or take parsing.

## Tallies: sign count by motif

"None/unrecorded" means no animal is named in the remark. That is often a broken seal, not a script-only seal.

| Signs | Bisht seals: unicorn | Bisht: other animal | Bisht: none/unrecorded | **Bisht total** | Your ICIT export seals | Full ICIT seals (merged) |
|---|---|---|---|---|---|---|
| 1 | 4 | 4 | 9 | **17** | 0 | 16 |
| 2 | 9 | 2 | 18 | **29** | 13 | 31 |
| 3 | 14 | 3 | 20 | **37** | 10 | 20 |
| 4 | 4 | 3 | 12 | **19** | 14 | 18 |
| 5 | 7 | 2 | 3 | **12** | 15 | 21 |
| 6 | 5 | 1 | 0 | **6** | 4 | 6 |
| 7 | 3 | 1 | 0 | **4** | 5 | 6 |
| 8 | 2 | 0 | 0 | **2** | 2 | 2 |
| 9 | 0 | 0 | 0 | **0** | 2 | 2 |
| **Total** | 48 | 16 | 62 | **126** (+16 unclear, +19 museum) | **65** | **122** |

Motif split in your export's seals: 37 unicorn (Bull1), 24 unknown, 4 other (2 gaur, 1 tiger, 1 elephant).

How to read the table:
- Bisht's counts lean short (many 1–3) because he counts **signs still visible on fragments**. ICIT counts restored or longer texts (more 5s and 9s). Exact row-by-row matching is not possible from counts alone.
- Full ICIT (122 seals) vs Bisht (about 139 inscribed): a gap of about 17. The repo authors checked the photos of the most complete "unmatched" seals and found them already in ICIT (e.g. Acc. 2393 = 233-706-33-520; Acc. 10342 = 861-2-16-390). They concluded that the gap is mostly fragments with 1–2 partial signs. I did not repeat that check.
- Sealings: Bisht has 60, full ICIT has 58 Dholavira tags. Gap about 2 [UNVERIFIED; the sealings were not extracted].
- Your export vs Bisht: about 74 seals (139 − 65) plus most sealings. But almost all of those are in full ICIT already.

Missing-count estimate (inscribed objects in Bisht not in full ICIT):
- **Low: 0–5.** The repo's photo check found no new complete texts.
- **High: about 20.** This is the raw count difference (17 seals + about 2–3 sealings). It assumes none of the difference is double-counting or "In Nat. Mus." items.
- Most such items would be 1–3-sign fragments, of little use as a test set.

## Your export vs full ICIT (the bigger gap)

- 66 of your 74 rows match a full-ICIT Dholavira text exactly. The other 8 differ by one sign or an allograph (e.g. your S130 begins G856, ICIT has 861). Your S144 is the signboard, with 480-1 where the merged corpus has 645-31.
- 100 full-ICIT Dholavira texts of 2+ signs are not in your export at Dholavira: 54 seals, 33 tags, 10 tablets, 2 misc, 1 pot. Seal lengths: 2×22, 3×10, 4×6, 5×7, 6×3, 7×3, 8×1, 9×2.
- 81 of the 100 are not in your export at any site.
- Your export has 2,543 rows for all sites; the merged corpus has 5,369. Why your export is smaller is not clear to me [UNVERIFIED]. It is not de-duplication: your export still has 229 repeated texts.

## Can the printed photos be read sign by sign?

Mostly yes, for complete seals. I viewed 10 crops:

| Crop | What it shows | Readable sign by sign? |
|---|---|---|
| p277_0 | Unicorn seal, strokes + one sign | Yes |
| p285_2 | Unicorn seal, heavy encrustation | Partly (3–4 signs, some uncertain) |
| p292_1 | Unicorn seal, about 6 signs | Yes |
| p297_1 | Unicorn seal, two-row text | Mostly; small signs crowded |
| p303_2 | Broken unicorn seal, strokes + sign | Yes |
| p309_3 | Black steatite bar fragment, 4 signs | Yes, very clear |
| p311_3 | Fragment, one faint sign | No |
| p316_0 | Weathered unicorn seal | No; signs too faint |
| p320_0 | Small bar seal, about 5 signs (field photo) | Yes; high resolution |
| p324_1 | Bar seal, 5 signs | Yes |

- About **7 of 10 are good enough** to transcribe into G-numbers.
- They are **photos of the seal face**, so the text is mirror-reversed. Flip them before reading.
- I saw **no line drawings** of signs in these pages. Bisht's report gives text counts only, never sign identifications.
- The crop filenames give page and position, not catalogue number. Linking a crop to a catalogue row needs page order checks [UNVERIFIED].

## Other sources checked (quick)

- **CISI vol. 3.1** covers Mohenjo-daro and Harappa only. No Dholavira volume was found. The Gujarat sites are not yet published in CISI [UNVERIFIED that none is in press].
- **Post-2015 Dholavira finds:** a July 2026 Ministry of Culture post about the signboard (Business Today). No new inscription list was found. The repo's own sweep (S-DARK-36.1) found post-2014 Dholavira finds only as text descriptions or very small photos.
- **Excerpt PDF** (ancientportsantiques): captions only, pp. 17–61 of the excerpt.
- Nothing found that would widen the gap much. The real gain is the full-ICIT texts missing from your export.

## Practical suggestion

1. Pull the 100 missing Dholavira texts (and the 43 single-sign ones) from the merged corpus. Use them as a test set held out from your export. Label it as "held out from export", not "independent".
2. For a truly independent check, have someone read about 10 clear Bisht photos blind and compare with ICIT. This tests ICIT's transcription, not your model.

## Files

- `data/derived_bisht2015_dholavira_catalogue.csv`: 221 rows. Catalogue no., accession no., page, sign count (from the extracted field, and from the remark text), status, motif, material, shape note, National Museum flag, remarks. Parsed from the MIT-licensed extraction; my parsing of the remarks can be wrong in places.

## Sources

- R.S. Bisht, *Excavations at Dholavira 1989–2005* (ASI, preliminary report, January 2015), section 8.2. Via the extraction in the cloned repo `/root/ext2/pg` (MIT licence): `data/derived/dholavira2015-seal-catalogue.json`, `data/images/dholavira2015/`, `STRATEGIES.md` rows 172, 176, S-DARK-36.1.
- Merged Wells/ICIT corpus: `/root/ext2/pg/data/derived/merged-corpus-canonical.json`.
- Excerpt PDF: [Dholavira Bisht2015 (ancientportsantiques.com)](https://ancientportsantiques.com/wp-content/uploads/Documents/PLACES/IndOc-Gulf/Dholavira-Bisht2015.pdf)
- [CISI vol. 3.1 (harappa.com)](https://www.harappa.com/content/corpus-indus-seals-and-inscriptions-vol-31)
- [Business Today, July 2026, Dholavira signboard](https://www.businesstoday.in/india/story/worlds-oldest-known-signboard-ministry-of-culture-shares-remarkable-indus-discovery-from-dholavira-542412-2026-07-12)
- [Dholavira (Wikipedia)](https://en.wikipedia.org/wiki/Dholavira)

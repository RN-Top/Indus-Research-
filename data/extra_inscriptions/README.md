# Extra inscriptions not in ICIT

Small additions from published sources, cleaned into Wells/ICIT sign numbers. Not independent of judgment: each reading is from a photo or drawing, with a confidence per sign.

- `extra_texts.csv`: one row per inscription. `?` = lost sign; NOMATCH = sign not on the Wells list (described in `note`).
- Dholavira (Bisht 2015) transcriptions are added separately once matched against ICIT (`dholavira_bisht2015_*`).

**Still to clean (need images the session cannot download):**
- Bagasra / Gola Dhoro: Jamison et al., "Inscribed Unicorn Seals from Bagasra" (harappa.com; Academia.edu 36047001), 7 seals; ICIT has 5 Gola Dhoro objects.
- Ra's al-Junayz, Oman: Cleuziou, Gnoli, Robin & Tosi 1994, CRAIBL 138(2): 453–468 (Persée), inscribed jars and seals; ICIT has 3.
- Binjor unicorn seal (~5 signs): needs a better photo than the ASI brochure.

## Dholavira, Bisht (2015) seal catalogue (added 26 October 2026)

- `dholavira_bisht2015_transcriptions.csv`: blind transcriptions (three agents, 26 October 2026) of the catalogue photographs for pages 289–324 (151 photos, from paragorth/Indus- `data/images/dholavira2015/`), against labelled sheets of the SK Indus Script font. Seal faces were mirrored back and read left to right. Pages 277–288 were not transcribed (that batch was stopped).
- `dholavira_bisht2015_matched_to_icit.csv`: each inscription with at least one identified sign, compared with the 203 Dholavira objects in the fuller ICIT copy (share of its identified signs found in the best-matching ICIT text, order ignored).

| Status | Inscriptions |
|---|---|
| Likely already in ICIT (≥50% of identified signs shared, 2+ signs) | 46 |
| Only one identified sign (cannot be matched) | 29 |
| **Possibly new** | **10** (6 with good legibility) |

**Caveat.** The photos are small and many signs are low confidence or NOMATCH. The 46 matches show the readings are broadly usable, but the 10 "possibly new" texts may also be ICIT objects read differently. Treat them as candidates for checking against better images, not as test data.

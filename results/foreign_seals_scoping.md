# Inscriptions found abroad: is there enough data for a registered test? (SCOPING)

*15 October 2026. Nothing was tested. For the locked holdout, only site, object type, damage flag and split were read; no holdout sign sequence was looked at. Script: `scripts/foreign_seals_scope.py`. Counts: `foreign_seals_scoping.json`. Draft registration: `drafts/H-foreign-closer.DRAFT.json`, which is **not registered**.*

## The lead being scoped

In `sign_travel_water.md` (section D), Indus inscriptions found outside the Indus region rarely contained a closer sign.

| Group | Contain a closer |
|---|---|
| All 14 exploration texts found abroad | 4 (29%) |
| The 11 seals among them | 2 (18%) |
| Home seals | 78% |

This was noticed after looking, so it has to be tested on inscriptions that played no part in finding it.

## Bottom line

**There is not enough data yet for a real test.** The draft is ready, and the missing data probably exists in published catalogues. It would have to be transcribed into sign numbers.

## 1. What is in the corpus

All 52 sites were checked. Fourteen are outside the Indus region: Ur, Kish and Tell Umma (Mesopotamia); Susa and Luristan (Iran); Qala'at al-Bahrain, Saar, Karzakan and Hajar (Bahrain); Ra's al-Junayz and Salut (Oman); Altyn Depe, Gonur Depe and Shortughai (Central Asia).

| | Seal | Tablet | Tag | Pottery | Total |
|---|---|---|---|---|---|
| Exploration (already used; **cannot** be test data) | 11 | 1 | 1 | 1 | 14 |
| Locked holdout (usable) | 2 | 0 | 0 | 0 | **2** |

- No abroad records were dropped for damage or as duplicates. The full corpus has the same 16.
- The CISI file in `data/` covers Mohenjo-daro only, with no foreign finds.
- **So the corpus alone gives 2 test texts, against a minimum support of 15.**

**Home texts for matching are plentiful.** The holdout has 269 seals, 100 tablets, 14 pottery texts and 5 tags from named home sites.

**Home rates in exploration** (used only for planning):

| Object type | Texts | Contain a closer | End in a closer |
|---|---|---|---|
| Seals | 1,037 | 78% | 70% |
| Tablets | 357 | 75% | 64% |
| Tags | 27 | 52% | 48% |
| Pottery | 44 | 55% | 43% |

## 2. What exists in published sources

**Laursen 2010, "The westward transmission of Indus Valley sealing technology"** (*Arabian Archaeology and Epigraphy*):
- The PDF is free on harappa.com.
- Its Table 1 lists 121 "Gulf Type" seals, of which 28 carry Indus characters.
- **23 of those were found outside the Indus region:**
  - Bahrain 7: Karzakan 3, Qala'at al-Bahrain 2, Saar 1, Janabiyah 1;
  - Failaka 2;
  - Iran 2: Susa, Luristan;
  - Mesopotamia 12: Ur 6, Girsu 1, five of unspecified or queried origin.
- The inscriptions are given **only as drawings** (Fig. 11), not as sign numbers.
- About 6–8 of the 23 are probably already in our corpus, judging by site (Karzakan, Qala'at al-Bahrain, Saar, Susa, Luristan, Ur), and most of those are exploration texts. That leaves **about 15 new ones**, an estimate until matched item by item.
- Laursen himself notes that the paper's totals are slightly inconsistent (27, 28 or 29 inscriptions), and he calls one seal pseudo-script.

**Square Indus-style seals in Mesopotamia** (Kish, Nippur, Lagash/Girsu, Ur and others):
- Overview sources speak of "about twenty" seals with Harappan connections from Akkadian and Ur III sites, of which only four are "indisputably Indus".
- Some overlap with Laursen's list and with our corpus.
- The full list is in Parpola's work, and in the *Corpus of Indus Seals and Inscriptions* (CISI) volumes, which are books rather than files.

**Central Asia:**
- CISI vol. 3.3, *Indo-Iranian Borderlands* (€220), covers the highlands, Afghanistan and Central Asia.
- A review says it contains "hardly any Indus-type seals".

**ICIT (Wells and Fuls):** probably the quickest route to coded data.
- Our corpus derives from it, and it may hold West Asian finds already coded in the same sign numbers.
- This was not checked, because access is paid and browse-only (about €15 registration plus €25 a month).

**Realistic total of new, unused texts:** probably 15–30. They would need to be gathered from Laursen, Parpola and CISI, or ICIT, and transcribed.

## 3. Statistical power

The test compares the share containing a closer with about 77% at home, one-sided, α = 0.05.

| New test texts | Power if the true rate abroad is 30% | 45% | 60% |
|---|---|---|---|
| 2 (corpus only) | 0 (no possible result reaches significance) | 0 | 0 |
| 10 | 0.85 | 0.50 | 0.17 |
| 15 | 0.98 | 0.82 | 0.39 |
| 20 | 0.99 | 0.87 | 0.40 |
| 25 | 1.00 | 0.96 | 0.58 |

The exploration rate (29%) is probably an overestimate of the effect, since leads found by looking usually shrink. A planning value of 45% abroad therefore needs **at least 15, preferably 20–25** new texts. That matches the repository's minimum support of 15.

## 4. The draft test (`drafts/H-foreign-closer.DRAFT.json`)

- **Claim:** inscriptions found abroad contain a closer less often than home texts of the same object type.
- **Closers (frozen, unchanged):** the 12 found by the role rule on all exploration texts: G90, G151, G154, G156, G400, G405, G407, G520, G527, G617, G621, G740.
- **Test group:**
  - the 2 holdout abroad texts;
  - catalogue texts added to a new `data/foreign_inscriptions.csv` before freezing;
  - the 14 exploration texts are excluded.
- **Control group:** home holdout texts of the same object types.
- **Statistic:** the difference in closer share, weighted by object type. Null: labels shuffled within object type, 10,000 times. Secondary: "ends in a closer".
- **Multiple testing:** BH across all confirmatory tests ever run, as usual.
- **Transcription safeguard:** whoever turns catalogue drawings into sign numbers must not be told the hypothesis or the closer list. Doubtful signs are recorded, and texts with a damaged end are excluded. This matters because the hypothesis is about whether a particular kind of sign is present.
- **Still to do before freezing:**
  - code for a new hypothesis kind (`closer_presence`), with synthetic positive and negative controls in the tests;
  - the data file;
  - Erin's go-ahead.
- The draft sits in `drafts/`, which `run_confirmatory.py` never reads, so it cannot run by accident.

## 5. Caveats that would remain even with enough data

- **Gulf Type seals are a different seal tradition** (round, Dilmun-style), probably made in the Gulf for local users. Laursen reads some of their inscriptions as unusual or pseudo-script. A missing closer there could mean "a different writing practice", not "the closer was left off for foreign trade". The data cannot tell these apart. Reporting Gulf Type and square Indus seals separately would help.
- **Dating:** foreign finds may be later than most home seals.
- **Transcription:** Wells sign numbers assigned from drawings by a non-specialist will be less reliable than ICIT's.

## What would unblock it (cheapest first)

1. **ICIT access** (Fuls). Check whether the West Asian finds are already coded, then copy the Textcode output.
2. **Laursen 2010 Fig. 11** (free PDF). Transcribe about 15 new Gulf Type inscriptions blind, following the safeguard above.
3. **Parpola, *Deciphering the Indus Script* (1994), and CISI volumes** for the square seals in Mesopotamia.

## Sources

- Laursen, S. T. (2010). The westward transmission of Indus Valley sealing technology. *Arabian Archaeology and Epigraphy* 21. [Free PDF on harappa.com](https://www.harappa.com/sites/default/files/pdf/The_westward_transmission_of_Indus_Valle.pdf); [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1600-0471.2010.00329.x)
- [Indo-Mesopotamia relations (Wikipedia)](https://en.wikipedia.org/wiki/Indo-Mesopotamia_relations), for the "about twenty" and "four indisputably Indus" figures, with their own sources.
- [Review of CISI vol. 3.3, *The Past*](https://the-past.com/?p=49513)
- [The Story of the Gulf Type Indus Seal (harappa.com)](https://www.harappa.com/blog/story-gulf-type-indus-seal)

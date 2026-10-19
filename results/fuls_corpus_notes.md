# Fuls, *Corpus of Indus Inscriptions* [I] (2022; 2nd ed. 2023): notes from the Kindle sample

*19 October 2026. The book has now been bought; the sign list (pp. 22–24) is in `data/fuls_sign_list.csv`. Originally read from the free Kindle sample (pp. v–ix, 14–15, 22–29). Screenshots are kept outside the repository.*

## What the book is

- **All known Indus inscriptions:** 5,638, from 76 sites (p. 14).
- **Arrangement:** by site, alphabetically. Each site has its region and coordinates.
- **Each entry gives:**
  - the ICIT ID;
  - the CISI number;
  - the object type;
  - the reading direction;
  - whether the text is complete (Y / N / ?);
  - symbol and cult object (Wells 2011);
  - the signs, drawn in reading order, right to left;
  - the sign code.

  Eroded signs are coded 000. Fragment ends are marked with `]` and `[`.
- **Indexes:** ICIT IDs, CISI numbers, excavation numbers, and Mahadevan 1977 text numbers. That last one is a ready-made crosswalk to the M77 corpus.

## The sign numbers are ours

The sign list (Table 2.6, pp. 22–24) is numbered in the same system as our G-numbers, the ICIT numbering. Spot checks by shape:

| Sign | Shape |
|---|---|
| 2 | two strokes |
| 60 | hooked stroke |
| 740 | jar |
| 741, 742, 745 | marked jars |
| 692 | X |
| 817 | oval with chevron |
| 820 | spoked oval |
| 861 | diamond with chevron |
| 920 | bracket |

So texts copied from the book need **no sign-matching step**.

Check: Altyn Depe Alt-90 (p. 29) is drawn as 390 415. In our corpus it is G390 G415.

## Sites outside the Indus region (region list, p. 26)

| Region | Sites |
|---|---|
| Persian Gulf | Failaka, Hajar, Janabiyah, Kalba, Karzakan, Qala'at al-Bahrain, Ra's al-Junayz, Saar, Salut |
| Mesopotamia | Girsu, Kish, Nippur, Tell Umma, Tello, Ur |
| Iranian Plateau, outside Baluchistan | Luristan, Susa, Tepe Yahya |
| Other | Altyn Depe, Gonur Depe, Shortughai |

**Our exploration split has 14 texts from 13 of these sites.** There are none from Failaka, Girsu, Janabiyah, Kalba, Kish, Nippur, Tello or Tepe Yahya.

**Book pages for these sites:** 29, 58, 60–62, 257–258, 275–276, 294, 441, 443, 446–450, 453.

The table of contents shows most of these sites take less than a page, so **the book probably holds a few dozen texts from abroad, not hundreds**. Some will overlap Laursen 2010.

**Not checked:** how many of the book's entries are complete and new to us. That needs the purchased pages.

## Overseas entries seen so far (pages sent 19 October 2026)

**Our text IDs are the book's ICIT IDs:** `S16` = ICIT 16. So checking for overlap is exact. The check below used IDs only; no sign content was read from our corpus.

**Tag:** *new* means the ID is absent from our source.

| ICIT | Site | Object | Complete? | In our corpus |
|---|---|---|---|---|
| 16 | Altyn Depe | seal | Y | exploration |
| 160 | Hajar | tablet | Y | exploration |
| 5222 | Girsu | cylinder seal | **N** | new (= Laursen no. 22) |
| 5232 | Janabiyah | cylinder seal | Y | **new** (probably Laursen no. 10, flagged broken there) |
| 5551 | Kalba | cylinder seal | Y | **new** |
| 5227, 5228 | Karzakan | cylinder seals | Y | exploration |
| 5230 | Karzakan | cylinder seal | Y | **new** |
| 1970 | Kish | seal | N | new |
| 1971 | Kish | seal | Y | **holdout** |
| 2153 | Luristan | cylinder seal | Y | exploration |
| 3860 | Nippur | seal | N | new |
| 3863 | Qala'at al-Bahrain | cylinder seal | Y | exploration |
| 3864 | Ra's al-Junayz | pottery | N | new |
| 3865 | Ra's al-Junayz | pottery | Y | exploration |
| 3866 | Ra's al-Junayz | pottery | ? | new |
| 3897 | Ur | cylinder seal | Y | exploration |
| 3898 | Ur | cylinder seal | Y | **holdout** |
| 3899, 5225, 5231 | Ur | cylinder seals | N | new |

**Still needed:**
- p. 59: Failaka
- p. 61: Gonur Depe
- pp. 446–447: Saar, Salut
- pp. 448–450: Shortughai, Susa, Tell Umma, Tello, Tepe Yahya

**Holdout exposure (recorded for honesty).** The book pages show the sign content of the two overseas texts in the locked holdout, ICIT 1971 (Kish) and 3898 (Ur). The analyst has now seen them. They were already known to be the 2 holdout texts found abroad (`foreign_seals_scoping.md`).
- **This affects only the planned overseas test,** where they are 2 of the test-group texts. Report it in any registration of that test.
- **No other test is affected.**

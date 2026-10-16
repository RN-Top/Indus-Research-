# What does each closing sign categorise? Extension of the closer test (EXPLORATORY)

*15 October 2026. Exploration split only; the holdout was not read and nothing was registered. Script: `scripts/closer_categories_ext.py`. Numbers: `closer_categories_ext.json`. Printout: `closer_categories_ext_output.txt`. Builds on `closer_category_test.md`, which used the final sign only and tested object type, site and seal animal.*

## What was added

| Part | What it asks | Confound check (stratified shuffle) |
|---|---|---|
| A | Do texts **ending** in a closer cluster by **material** (steatite, faience, copper, clay, ...)? Material had not been tested before. | within object type |
| B | **Seals only:** do closers cluster by site or material inside a single object type, so tablets cannot drive the result? | within site (for material) |
| C | Using texts that **contain** the closer anywhere, not only at the end | within site, or within object type |

There were 60 tests, each with support of at least 15 texts. Each uses a chi-square against 5,000 shuffles, with Cramér's V and excess V as effect sizes. BH was applied across all 60, and separately across the stratified checks.

## Results

**Survive correction (q < 0.05):**

| Closer | Part | Attribute | Strongest category | V | q | Holds in the confound check? |
|---|---|---|---|---|---|---|
| **G400** | C | object type | **tablet**: 64% of 161 texts, against 24% overall | 0.33 | 0.004 | **yes** (q = 0.005) |
| **G400** | C | site | **Harappa**: 68% against 33% | 0.26 | 0.004 | **yes** (q = 0.005) |
| G400 | A | material | faience: 33% against 10% | 0.26 | 0.004 | **no** (q = 0.44): faience here means the moulded faience tablets, so this is the tablet link again |
| **G407** | A | material | **copper**: 5 of 19 texts, against 4% | 0.15 | 0.04 | **yes** (q = 0.02) |
| G740 | C | object type | seal: 72% against 69% | 0.11 | 0.02 | yes (q = 0.04), but tiny |
| G527 | C | site | Lothal: 6 of 36 texts, against 3% | 0.14 | 0.04 | no (q = 0.08) |

**Near misses:**
- G617 on copper: 4 of 16 texts (q = 0.12; stratified q = 0.08).
- G520 leaning to seals (q = 0.07).
- G527 at Lothal among seals only (q = 0.07).

**Nothing at all:** G90, G151, G154, G156, G405, G621 and G617, apart from the copper hint.

## What it means

| Closer | Reading from all tests so far |
|---|---|
| **G400** | **A real category mark.** It goes with tablets and with Harappa, and both survive every confound check. It is a "post-terminal" sign in Wells's and Fuls's terms. |
| **G407** (and perhaps **G617**) | **New lead: the copper tablets of Mohenjo-daro.** G407 ends 5 of the 42 copper tablets and G617 ends 4 of them. Each also appears on ordinary steatite seals, so it is not exclusive to copper. Copper tablets are a known distinct class: small plates found mostly at Mohenjo-daro, often with an animal on one side. |
| **G740** ("jar") | **A generic ending.** It is on about a third of all texts, with a statistically clear but trivial lean to seals. |
| **G527** | Leans to Lothal, but on 6 texts, and it does not survive the confound check. |
| The rest | No detectable category on object, site, animal or material. |

So **two or three closers mark something we can see, and most do not.** The others may mark something the metadata does not record, such as an office, a commodity or a lineage. They may also not be category marks at all.

## Limits

- **Exploratory:** 60 tests on data already looked at. The G407/copper lead rests on 5 texts and was found by searching.
- **One site:** copper tablets come almost only from Mohenjo-daro, so "copper" and "this tablet class at Mohenjo-daro" cannot be separated.
- **Same transcription:** the data are ICIT-derived (METHODS.md, provenance).

## Possible confirmatory test

"G407 ends copper tablets more often than other texts" could be registered. The holdout probably holds only about 10 copper tablets, so even a real effect would often be missed (low power). Combining it with G617 as a pair would help a little.

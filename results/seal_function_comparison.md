# Reading an Indus seal like a Mesopotamian seal: the function comparison

*15 October 2026. Two parts:*
- *Part 1 is exploratory and uses exploration texts only.*
- *Part 2 reports two pre-registered tests run once on unseen holdouts (sixth batch in `confirmatory_2026-10-14.md`).*

*Data for Mesopotamia: CDLI seal legends, Old Akkadian to Old Babylonian (see `mesopotamian_seals_comparison.md`). For Proto-Elamite: the pe-headers corpus (see `proto_elamite_comparison.md`).*

## The idea

A Mesopotamian seal is a label whose meaning we can read. A typical Ur III "servant seal" reads:

> **[King's name]**, strong king, king of Ur — **[owner's name]**, scribe, son of **[father's name]** — **your servant** (*arad₂-zu*).

If the same blind rule finds the same kind of layout in Indus seals, the Indus seal can be read by analogy:

> **[fixed heading]** + **[individual name or title]** + **[affiliation or category mark]**.

This gives the inscription a job. It does not say what any sign means.

## 1. Slot profiles side by side (exploration)

| | Indus seals | Mesopotamian seal legends |
|---|---|---|
| Texts | 1,057 | 8,570 |
| Length, median (middle half) | 5 signs (3–6) | 4 words (3–5) |
| Has an opener / starts with one | 36% / 28% | 39% / 31% |
| **Has a closer / ends with one** | **78% / 69%** | 28% / 24% |
| **Opener forms** | **28**; the commonest (G820) is 24% of openers | **487**; the commonest (*kišib*, "seal of") is 9% |
| **Closer forms** | 57; the top 5 cover **74%** | 138; the top 5 cover 42% |
| Commonest openers | G820, G861, G817, G920, G692 | *kišib* "seal of", then kings' names (Šu-Suen, Šulgi, Ibbi-Suen) and other personal names |
| Commonest closers | G740 (40% of closers), G520, G740+G90, G151, G527, G400 | *arad₂-zu* "your servant" (17%), then gods (Martu, Šara, Iškur, Ninšubur), *dam-gar₃* "merchant" |

**Where the words sit in Mesopotamian legends** (0 = first word, 1 = last word):

| Word | Meaning | Average position |
|---|---|---|
| *kišib* | "seal of" | **0.03** (the heading) |
| *lugal* | king | 0.33 |
| *dub-sar* | scribe, a title | 0.41 |
| *dumu* | "son of" | 0.52 (the middle) |
| *arad₂-zu* | "your servant" | **1.00** (always last) |

### What this suggests

- **The Mesopotamian layout is exactly heading → person → affiliation.**
  - The opening slot holds either "seal of" or the overlord's name: the authority the seal belongs under.
  - The middle holds the owner's name, title and father.
  - The closing slot holds "your servant" or a patron god: the relationship to that authority.
- **The Indus layout has the same three slots, but used differently:**
  - **The Indus heading is a small fixed set.** It works like *kišib* "seal of", not like the long list of rulers' and owners' names that open Mesopotamian legends.
  - **The Indus ending is nearly obligatory** (78% of seals, against 28%) **and highly standardised** (5 forms cover 74%). That is like *arad₂-zu*, which is one fixed phrase for "belongs to / serves". One generic closer (G740) carries 40% of all endings.
  - **The middle is the varied part** in both: unique 86% of the time in Indus (`functional_meaning.md`), and name, title and father in Mesopotamia.
- **The working reading:** an Indus seal states a fixed heading, then an individual, then a standard relation mark (mostly G740), sometimes with a more specific mark added. G400 at Harappa, on tablets, is the clearest of these (`closer_category_test.md`, `closer_categories_ext.md`).
- **This is an analogy, not a translation.** Nothing here shows that G740 *means* "servant", or that the Indus middle is a personal name.

## 2. Pre-registered tests on unseen texts

Both were registered in commit `2a193e3` before being run, then run once.

| Hypothesis | Result on the holdout | q (BH across all 16 confirmatory tests) | Verdict |
|---|---|---|---|
| `H-2026-10-16-12cb3aa3`: Indus opening units have fewer distinct forms than Mesopotamian seal openers at the same sample size | **18** Indus forms in 136 texts, against **76.4** Mesopotamian forms in samples of 136 | 0.0006 | **Supported** |
| `H-2026-10-16-9d9defa5`: the blind rule's Proto-Elamite openers sit inside the header that experts marked | **62.7%** of 59 opener tokens inside the header on 81 unseen tablets, against 9.1% shuffled | 0.0006 | **Supported** |

- **The first test** confirms on new texts that the Indus opening slot is a small fixed heading, not a name slot. Part of this is built into the rule's output (7 Indus opener signs against 92 Mesopotamian opener words), so it confirms a strong difference rather than a surprise.
- **The second** is a check of the method itself. On unseen tablets, the rule's "openers" fall where experts put the header. When the rule says "heading", there usually is a heading.

## Limits

- **Analogy carries no meaning by itself.** Many systems have heading, name and tag; Raghavendra (2026) shows that even non-linguistic sign systems produce positional regularities.
- **Different eras and practices.** The Mesopotamian legends span about 2340–1600 BCE. Most are Ur III servant seals, which are a specific administrative genre.
- **Unit mismatch.** Indus signs are compared with Mesopotamian *words*, on the assumption that Indus signs are mostly word signs.
- **Same Indus transcription** throughout (ICIT-derived).

## Next steps for the function reading

1. **G740 as the generic relation mark.** Does G740 behave like *arad₂-zu*: final, nearly always present, indifferent to who the owner is? A test: compare how much G740's presence depends on the middle content with how much *arad₂-zu*'s presence depends on the owner's name.
2. **The heading.** Do the five commonest Indus openers go with different kinds of middle, the way *kišib* + name differs from king + name in Mesopotamia? That could split the heading into types.
3. **Copper tablets and G407** (`closer_categories_ext.md`) as a possible category mark tied to one object class.
